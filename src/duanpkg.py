# -*- coding: utf-8 -*-
"""
段言包管理器 (duanpkg) v4.0
管理 .duan 包的安装、发布、搜索

用法:
  python duanpkg.py init [name]      初始化新包
  python duanpkg.py install <pkg>    安装包
  python duanpkg.py publish          发布包到本地注册表
  python duanpkg.py search [query]   搜索包
  python duanpkg.py list             列出已安装包
  python duanpkg.py info <pkg>       查看包信息
  python duanpkg.py remove <pkg>     卸载包
"""
import os
import sys
import json
import shutil
import argparse
import urllib.request
import urllib.error
import base64
import io
import zipfile
from pathlib import Path
from datetime import datetime

# 默认注册表路径
DEFAULT_REGISTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'contrib', 'registry.json')
DEFAULT_CONTRIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'contrib')
DEFAULT_INSTALL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'contrib', 'installed')


def _ensure_registry():
    """确保注册表文件存在"""
    os.makedirs(os.path.dirname(DEFAULT_REGISTRY), exist_ok=True)
    if not os.path.exists(DEFAULT_REGISTRY):
        with open(DEFAULT_REGISTRY, 'w', encoding='utf-8') as f:
            json.dump({"packages": {}, "updated": str(datetime.now())}, f, indent=2, ensure_ascii=False)


def _load_registry():
    """加载注册表"""
    _ensure_registry()
    with open(DEFAULT_REGISTRY, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_registry(reg):
    """保存注册表"""
    reg["updated"] = str(datetime.now())
    with open(DEFAULT_REGISTRY, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)


def _find_package_dir(name):
    """在 contrib/ 中查找包目录"""
    contrib = Path(DEFAULT_CONTRIB)
    candidates = list(contrib.glob(f"{name}*"))
    for c in candidates:
        if c.is_dir() and (c / "duan.json").exists():
            return c
    return None


def _read_package_json(pkg_dir):
    """读取包的 duan.json"""
    pkg_file = Path(pkg_dir) / "duan.json"
    if pkg_file.exists():
        with open(pkg_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def cmd_init(args):
    """初始化新包"""
    name = args.name or os.path.basename(os.getcwd())
    pkg_dir = Path(args.dir or os.getcwd())

    pkg_json = {
        "name": name,
        "version": "0.1.0",
        "description": f"{name} - 段言包",
        "author": "",
        "license": "MIT",
        "duan_version": "4.0.0",
        "keywords": [],
        "dependencies": {},
        "entry": "main.duan",
        "files": ["main.duan"]
    }

    pkg_file = pkg_dir / "duan.json"
    main_file = pkg_dir / "main.duan"

    if pkg_file.exists():
        print(f"错误: duan.json 已存在于 {pkg_dir}")
        return 1

    with open(pkg_file, 'w', encoding='utf-8') as f:
        json.dump(pkg_json, f, indent=2, ensure_ascii=False)

    if not main_file.exists():
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(f'# {name} - 段言包\n\n印("你好，{name}！")\n')

    print(f"已初始化包 {name} v0.1.0")
    print(f"  duan.json -> {pkg_file}")
    print(f"  main.duan -> {main_file}")
    return 0


def cmd_install(args):
    """安装包"""
    name = args.package
    print(f"正在安装 {name}...")

    # 远程安装
    if args.registry:
        return _remote_install(args.registry, name, args.version)

    # 本地安装
    pkg_dir = _find_package_dir(name)
    if not pkg_dir:
        print(f"错误: 未找到包 {name}")
        print(f"提示: 使用 'duanpkg search' 查看可用包")
        return 1

    return _install_local(pkg_dir, args.force)


def cmd_publish(args):
    """发布包到本地或远程注册表"""
    pkg_dir = Path(args.dir or os.getcwd())
    pkg_info = _read_package_json(pkg_dir)

    if not pkg_info:
        print(f"错误: 当前目录没有 duan.json。请先运行 'duanpkg init'")
        return 1

    name = pkg_info["name"]
    version = pkg_info["version"]

    # 远程发布
    if args.registry:
        return _remote_publish(args.registry, pkg_info, pkg_dir)

    # 本地发布
    contrib_dir = Path(DEFAULT_CONTRIB) / name
    if contrib_dir.exists():
        if not args.force:
            print(f"包 {name} 已存在于 contrib/。使用 --force 覆盖")
            return 1
        shutil.rmtree(contrib_dir)

    shutil.copytree(pkg_dir, contrib_dir, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))

    reg = _load_registry()
    reg["packages"][name] = {
        "version": version,
        "description": pkg_info.get("description", ""),
        "author": pkg_info.get("author", ""),
        "published_at": str(datetime.now()),
        "keywords": pkg_info.get("keywords", [])
    }
    _save_registry(reg)

    print(f"已发布 {name} v{version}")
    print(f"  contrib/{name}/")
    return 0


def cmd_search(args):
    """搜索包"""
    # 远程搜索
    if args.registry:
        return _remote_search(args.registry, args.query or "")

    # 本地搜索
    query = (args.query or "").lower()
    reg = _load_registry()
    packages = reg.get("packages", {})

    if not packages:
        print("注册表中暂无包。使用 'duanpkg publish' 发布包。")
        # 也扫描 contrib/ 目录
        _scan_contrib_packages()
        return 0

    results = []
    for name, info in packages.items():
        desc = info.get("description", "")
        author = info.get("author", "")
        kw = " ".join(info.get("keywords", []))
        search_text = f"{name} {desc} {author} {kw}".lower()
        if not query or query in search_text:
            results.append((name, info))

    if not results:
        print(f"未找到匹配 '{args.query}' 的包")
    else:
        print(f"找到 {len(results)} 个包:\n")
        print(f"{'名称':<20} {'版本':<10} {'描述'}")
        print("-" * 60)
        for name, info in sorted(results):
            print(f"{name:<20} v{info.get('version','?'):<9} {info.get('description','')[:40]}")

    return 0


def _scan_contrib_packages():
    """扫描 contrib/ 目录中的包"""
    contrib = Path(DEFAULT_CONTRIB)
    if not contrib.exists():
        return

    found = []
    for item in sorted(contrib.iterdir()):
        if item.is_dir() and (item / "duan.json").exists():
            pkg_info = _read_package_json(item)
            if pkg_info:
                found.append((item.name, pkg_info))

    if found:
        print(f"\ncontrib/ 目录中的包 ({len(found)} 个):\n")
        print(f"{'名称':<20} {'版本':<10} {'描述'}")
        print("-" * 60)
        for name, info in found:
            print(f"{name:<20} v{info.get('version','?'):<9} {info.get('description','')[:40]}")


def cmd_list(args):
    """列出已安装包"""
    install_dir = Path(DEFAULT_INSTALL)
    if not install_dir.exists():
        print("暂无已安装的包")
        return 0

    installed = []
    for item in sorted(install_dir.iterdir()):
        if item.is_dir():
            pkg_info = _read_package_json(item)
            if pkg_info:
                installed.append((item.name, pkg_info))

    if not installed:
        print("暂无已安装的包")
    else:
        print(f"已安装 {len(installed)} 个包:\n")
        print(f"{'名称':<20} {'版本':<10} {'描述'}")
        print("-" * 60)
        for name, info in installed:
            print(f"{name:<20} v{info.get('version','?'):<9} {info.get('description','')[:40]}")

    return 0


def cmd_info(args):
    """查看包信息"""
    name = args.package

    # 远程信息
    if args.registry:
        return _remote_info(args.registry, name)

    # 本地信息
    pkg_dir = _find_package_dir(name)

    if not pkg_dir:
        install_dir = Path(DEFAULT_INSTALL) / name
        if install_dir.exists():
            pkg_dir = install_dir
        else:
            print(f"错误: 未找到包 {name}")
            return 1

    pkg_info = _read_package_json(pkg_dir)
    if not pkg_info:
        print(f"错误: {pkg_dir} 缺少 duan.json")
        return 1

    print(f"名称: {pkg_info['name']}")
    print(f"版本: {pkg_info.get('version', '?')}")
    print(f"描述: {pkg_info.get('description', '无')}")
    print(f"作者: {pkg_info.get('author', '未知')}")
    print(f"许可: {pkg_info.get('license', '?')}")
    print(f"段言版本: {pkg_info.get('duan_version', '?')}")
    print(f"入口: {pkg_info.get('entry', 'main.duan')}")
    print(f"路径: {pkg_dir}")

    deps = pkg_info.get('dependencies', {})
    if deps:
        print(f"依赖: {json.dumps(deps, ensure_ascii=False)}")

    files = pkg_info.get('files', [])
    if files:
        print(f"文件: {', '.join(files)}")

    return 0


def cmd_remove(args):
    """卸载包"""
    name = args.package
    install_dir = Path(DEFAULT_INSTALL) / name

    if not install_dir.exists():
        print(f"错误: 包 {name} 未安装")
        return 1

    shutil.rmtree(install_dir)

    # 更新注册表
    reg = _load_registry()
    if name in reg["packages"]:
        del reg["packages"][name]
        _save_registry(reg)

    print(f"已卸载 {name}")
    return 0


# =============================================================================
# 远程注册表操作
# =============================================================================

def _http_get(url: str) -> dict:
    """HTTP GET 请求"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'duanpkg/4.1'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else ''
        try:
            err = json.loads(body)
            print(f"远程错误: {err.get('error', body)}")
        except:
            print(f"HTTP {e.code}: {body}")
        return None
    except urllib.error.URLError as e:
        print(f"连接失败: {e.reason}")
        return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def _http_post(url: str, data: dict) -> dict:
    """HTTP POST 请求"""
    try:
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'duanpkg/4.1'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else ''
        try:
            err = json.loads(body)
            print(f"远程错误: {err.get('error', body)}")
        except:
            print(f"HTTP {e.code}: {body}")
        return None
    except urllib.error.URLError as e:
        print(f"连接失败: {e.reason}")
        return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def _http_download(url: str) -> bytes:
    """HTTP 下载二进制文件"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'duanpkg/4.1'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except Exception as e:
        print(f"下载失败: {e}")
        return None


def _install_local(pkg_dir, force=False):
    """本地安装包"""
    pkg_info = _read_package_json(pkg_dir)
    if not pkg_info:
        print(f"错误: {pkg_dir} 缺少 duan.json")
        return 1

    install_dir = Path(DEFAULT_INSTALL) / pkg_info["name"]
    if install_dir.exists():
        if not force:
            print(f"包 {pkg_info['name']} 已安装。使用 --force 强制覆盖")
            return 0
        shutil.rmtree(install_dir)

    shutil.copytree(pkg_dir, install_dir, dirs_exist_ok=True)

    reg = _load_registry()
    reg["packages"][pkg_info["name"]] = {
        "version": pkg_info["version"],
        "description": pkg_info.get("description", ""),
        "author": pkg_info.get("author", ""),
        "installed_at": str(datetime.now()),
        "path": str(install_dir)
    }
    _save_registry(reg)

    print(f"已安装 {pkg_info['name']} v{pkg_info['version']}")
    if pkg_info.get("description"):
        print(f"  {pkg_info['description']}")
    return 0


def _remote_publish(registry_url: str, pkg_info: dict, pkg_dir: Path) -> int:
    """发布包到远程注册表"""
    url = registry_url.rstrip('/') + '/api/packages/publish'

    # 创建包 zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(pkg_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith('.pyc') or file.startswith('.'):
                    continue
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, pkg_dir)
                zf.write(full_path, arcname)

    pkg_data = buf.getvalue()
    content_b64 = base64.b64encode(pkg_data).decode('ascii')

    payload = {
        'name': pkg_info['name'],
        'version': pkg_info['version'],
        'metadata': {
            'description': pkg_info.get('description', ''),
            'author': pkg_info.get('author', ''),
            'license': pkg_info.get('license', 'MIT'),
            'dependencies': pkg_info.get('dependencies', {}),
        },
        'content': content_b64,
    }

    print(f"正在发布到 {url} ...")
    result = _http_post(url, payload)
    if result:
        print(f"已发布 {result.get('name')} v{result.get('version')}")
        print(f"  SHA256: {result.get('sha256', 'N/A')[:16]}...")
        return 0
    return 1


def _remote_install(registry_url: str, name: str, version: str = None) -> int:
    """从远程注册表安装包"""
    base = registry_url.rstrip('/')

    # 获取包信息
    info_url = f'{base}/api/packages/{name}'
    if version:
        info_url += f'/{version}'

    info = _http_get(info_url)
    if not info:
        return 1

    print(f"找到 {info.get('name', name)} v{info.get('version', info.get('latest_version', '?'))}")

    # 下载包
    dl_url = f'{base}/api/packages/{name}/download'
    if version:
        dl_url += f'?version={version}'

    print(f"正在下载...")
    data = _http_download(dl_url)
    if not data:
        return 1

    # 解压到 installed/
    install_dir = Path(DEFAULT_INSTALL) / name
    if install_dir.exists():
        shutil.rmtree(install_dir)

    os.makedirs(install_dir, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(install_dir)

    # 更新注册表
    reg = _load_registry()
    reg["packages"][name] = {
        "version": info.get('version', info.get('latest_version', '0.0.0')),
        "description": info.get('description', ''),
        "author": info.get('author', ''),
        "installed_at": str(datetime.now()),
        "path": str(install_dir),
        "source": registry_url,
    }
    _save_registry(reg)

    print(f"已安装 {name}")
    return 0


def _remote_search(registry_url: str, query: str) -> int:
    """在远程注册表搜索包"""
    url = registry_url.rstrip('/') + '/api/search'
    if query:
        url += f'?q={query}'

    result = _http_get(url)
    if not result:
        return 1

    results = result.get('results', [])
    if not results:
        print(f"未找到匹配 '{query}' 的包")
    else:
        print(f"找到 {len(results)} 个包:\n")
        print(f"{'名称':<20} {'版本':<12} {'下载':<8} {'描述'}")
        print("-" * 70)
        for pkg in results:
            print(f"{pkg['name']:<20} v{pkg.get('latest_version','?'):<11} {pkg.get('downloads',0):<8} {pkg.get('description','')[:40]}")

    return 0


def _remote_info(registry_url: str, name: str) -> int:
    """从远程注册表查看包信息"""
    url = registry_url.rstrip('/') + f'/api/packages/{name}'

    info = _http_get(url)
    if not info:
        return 1

    print(f"名称: {info.get('name', name)}")
    print(f"版本: {info.get('latest_version', info.get('version', '?'))}")
    print(f"描述: {info.get('description', '无')}")
    print(f"作者: {info.get('author', '未知')}")
    print(f"许可: {info.get('license', '?')}")
    print(f"下载量: {info.get('downloads', 0)}")
    print(f"更新时间: {info.get('updated', '?')}")

    versions = info.get('versions', [])
    if versions:
        print(f"可用版本: {', '.join(versions)}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        prog='duanpkg',
        description='段言包管理器 v4.1'
    )
    sub = parser.add_subparsers(dest='command', help='命令')

    # init
    p_init = sub.add_parser('init', help='初始化新包')
    p_init.add_argument('name', nargs='?', help='包名')
    p_init.add_argument('--dir', help='目标目录')

    # install
    p_install = sub.add_parser('install', help='安装包')
    p_install.add_argument('package', help='包名')
    p_install.add_argument('--registry', '-r', help='远程注册表地址')
    p_install.add_argument('--version', '-v', help='指定版本')
    p_install.add_argument('--force', '-f', action='store_true', help='强制覆盖')

    # publish
    p_publish = sub.add_parser('publish', help='发布包')
    p_publish.add_argument('--dir', help='包目录')
    p_publish.add_argument('--registry', '-r', help='远程注册表地址')
    p_publish.add_argument('--force', '-f', action='store_true', help='强制覆盖')

    # search
    p_search = sub.add_parser('search', help='搜索包')
    p_search.add_argument('query', nargs='?', help='搜索关键词')
    p_search.add_argument('--registry', '-r', help='远程注册表地址')

    # list
    sub.add_parser('list', help='列出已安装包')

    # info
    p_info = sub.add_parser('info', help='查看包信息')
    p_info.add_argument('package', help='包名')
    p_info.add_argument('--registry', '-r', help='远程注册表地址')

    # remove
    p_remove = sub.add_parser('remove', help='卸载包')
    p_remove.add_argument('package', help='包名')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    commands = {
        'init': cmd_init,
        'install': cmd_install,
        'publish': cmd_publish,
        'search': cmd_search,
        'list': cmd_list,
        'info': cmd_info,
        'remove': cmd_remove,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())