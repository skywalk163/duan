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

    # 1. 查找包
    pkg_dir = _find_package_dir(name)
    if not pkg_dir:
        print(f"错误: 未找到包 {name}")
        print(f"提示: 使用 'duanpkg search' 查看可用包")
        return 1

    pkg_info = _read_package_json(pkg_dir)
    if not pkg_info:
        print(f"错误: {pkg_dir} 缺少 duan.json")
        return 1

    # 2. 安装到 installed/
    install_dir = Path(DEFAULT_INSTALL) / pkg_info["name"]
    if install_dir.exists():
        if not args.force:
            print(f"包 {name} 已安装。使用 --force 强制覆盖")
            return 0
        shutil.rmtree(install_dir)

    shutil.copytree(pkg_dir, install_dir, dirs_exist_ok=True)

    # 3. 更新注册表
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


def cmd_publish(args):
    """发布包到本地注册表"""
    pkg_dir = Path(args.dir or os.getcwd())
    pkg_info = _read_package_json(pkg_dir)

    if not pkg_info:
        print(f"错误: 当前目录没有 duan.json。请先运行 'duanpkg init'")
        return 1

    name = pkg_info["name"]
    version = pkg_info["version"]

    # 复制到 contrib/
    contrib_dir = Path(DEFAULT_CONTRIB) / name
    if contrib_dir.exists():
        if not args.force:
            print(f"包 {name} 已存在于 contrib/。使用 --force 覆盖")
            return 1
        shutil.rmtree(contrib_dir)

    shutil.copytree(pkg_dir, contrib_dir, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))

    # 更新注册表
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
    pkg_dir = _find_package_dir(name)

    if not pkg_dir:
        # 也检查 installed/
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


def main():
    parser = argparse.ArgumentParser(
        prog='duanpkg',
        description='段言包管理器 v4.0'
    )
    sub = parser.add_subparsers(dest='command', help='命令')

    # init
    p_init = sub.add_parser('init', help='初始化新包')
    p_init.add_argument('name', nargs='?', help='包名')
    p_init.add_argument('--dir', help='目标目录')

    # install
    p_install = sub.add_parser('install', help='安装包')
    p_install.add_argument('package', help='包名')
    p_install.add_argument('--force', '-f', action='store_true', help='强制覆盖')

    # publish
    p_publish = sub.add_parser('publish', help='发布包到本地注册表')
    p_publish.add_argument('--dir', help='包目录')
    p_publish.add_argument('--force', '-f', action='store_true', help='强制覆盖')

    # search
    p_search = sub.add_parser('search', help='搜索包')
    p_search.add_argument('query', nargs='?', help='搜索关键词')

    # list
    sub.add_parser('list', help='列出已安装包')

    # info
    p_info = sub.add_parser('info', help='查看包信息')
    p_info.add_argument('package', help='包名')

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