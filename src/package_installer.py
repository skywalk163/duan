# -*- coding: utf-8 -*-
"""
段言（Duan）包安装器

负责从远程仓库下载并安装段言包。

功能：
  - duan install <包名>          从注册中心安装
  - duan install --git <url>     从 Git 仓库安装
  - duan install --path <路径>   从本地路径安装
  - duan install --list          列出已安装的包
  - duan install --search <关键词> 搜索包

包注册中心：
  - 内置注册表（常用包索引）
  - 支持自定义注册中心 URL
  - 支持 GitHub / Gitee 仓库
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


# ===========================================================================
# 内置包注册表
# ===========================================================================

BUILTIN_REGISTRY = {
    "packages": {
        "标准数学扩展": {
            "name": "标准数学扩展",
            "version": "1.0.0",
            "description": "扩展数学函数库：矩阵运算、复数、统计函数",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-math-ext.git",
            "keywords": ["数学", "矩阵", "统计"]
        },
        "网络请求": {
            "name": "网络请求",
            "version": "1.0.0",
            "description": "HTTP 客户端库：GET/POST 请求、JSON 解析",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-http.git",
            "keywords": ["网络", "HTTP", "API"]
        },
        "命令行工具": {
            "name": "命令行工具",
            "version": "1.0.0",
            "description": "CLI 开发工具：参数解析、进度条、颜色输出",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-cli-utils.git",
            "keywords": ["CLI", "命令行", "终端"]
        },
        "测试框架": {
            "name": "测试框架",
            "version": "1.0.0",
            "description": "单元测试框架：断言、测试套件、覆盖率",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-test.git",
            "keywords": ["测试", "单元测试", "断言"]
        },
        "数据库": {
            "name": "数据库",
            "version": "1.0.0",
            "description": "数据库操作库：SQL 查询、连接池、ORM",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-db.git",
            "keywords": ["数据库", "SQL", "ORM"]
        },
        "模板引擎": {
            "name": "模板引擎",
            "version": "1.0.0",
            "description": "文本模板引擎：变量替换、循环、条件渲染",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-template.git",
            "keywords": ["模板", "渲染", "HTML"]
        },
        "日志": {
            "name": "日志",
            "version": "1.0.0",
            "description": "日志记录库：分级日志、文件输出、格式化",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-log.git",
            "keywords": ["日志", "调试", "记录"]
        },
        "配置管理": {
            "name": "配置管理",
            "version": "1.0.0",
            "description": "配置文件管理：TOML/JSON/YAML 读写",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-config.git",
            "keywords": ["配置", "TOML", "JSON"]
        },
        "加密": {
            "name": "加密",
            "version": "1.0.0",
            "description": "加密工具库：哈希、对称加密、Base64",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-crypto.git",
            "keywords": ["加密", "哈希", "安全"]
        },
        "图像处理": {
            "name": "图像处理",
            "version": "1.0.0",
            "description": "图像处理库：缩放、裁剪、滤镜",
            "author": "段言团队",
            "git": "https://github.com/duan-lang/duan-image.git",
            "keywords": ["图像", "图片", "处理"]
        },
    },
    "updated_at": "2026-07-08"
}


# ===========================================================================
# 数据模型
# ===========================================================================

@dataclass
class PackageInfo:
    """包信息"""
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    git: str = ""
    path: str = ""
    keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "git": self.git,
            "path": self.path,
            "keywords": self.keywords
        }


# ===========================================================================
# 包安装器
# ===========================================================================

class PackageInstaller:
    """段言包安装器

    典型用法：
        installer = PackageInstaller()
        installer.install("标准数学扩展")        # 从注册中心安装
        installer.install_from_git("https://github.com/user/repo.git")
        installer.install_from_path("./local-package")
        installer.list_installed()               # 列出已安装
        installer.search("网络")                  # 搜索
    """

    def __init__(self, project_root: Optional[Path] = None, registry_url: Optional[str] = None):
        self.project_root = Path(project_root or os.getcwd()).resolve()
        self.registry_url = registry_url
        self._packages_dir = self.project_root / "packages"
        self._cache_dir = self._get_cache_dir()
        self._registry = self._load_registry()

    def _get_cache_dir(self) -> Path:
        """获取缓存目录"""
        if os.name == 'nt':
            base = Path(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')))
        else:
            base = Path(os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache')))
        cache = base / 'duan' / 'packages'
        cache.mkdir(parents=True, exist_ok=True)
        return cache

    def _load_registry(self) -> Dict:
        """加载包注册表"""
        registry = dict(BUILTIN_REGISTRY)

        # 尝试从远程加载注册表
        if self.registry_url:
            try:
                import urllib.request
                with urllib.request.urlopen(self.registry_url, timeout=10) as resp:
                    remote = json.loads(resp.read().decode('utf-8'))
                    if isinstance(remote, dict) and 'packages' in remote:
                        registry['packages'].update(remote['packages'])
            except Exception:
                pass

        # 尝试从本地缓存加载
        cache_registry = self._cache_dir / 'registry.json'
        if cache_registry.exists():
            try:
                cached = json.loads(cache_registry.read_text(encoding='utf-8'))
                if isinstance(cached, dict) and 'packages' in cached:
                    registry['packages'].update(cached['packages'])
            except Exception:
                pass

        return registry

    def _save_registry_cache(self):
        """保存注册表缓存"""
        cache_registry = self._cache_dir / 'registry.json'
        try:
            cache_registry.write_text(
                json.dumps(self._registry, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 搜索
    # ------------------------------------------------------------------

    def search(self, keyword: str) -> List[PackageInfo]:
        """搜索包"""
        results = []
        keyword_lower = keyword.lower()
        packages = self._registry.get('packages', {})

        for name, info in packages.items():
            if keyword_lower in name.lower():
                results.append(PackageInfo(**{k: v for k, v in info.items() if k in PackageInfo.__dataclass_fields__}))
                continue
            for kw in info.get('keywords', []):
                if keyword_lower in kw.lower():
                    results.append(PackageInfo(**{k: v for k, v in info.items() if k in PackageInfo.__dataclass_fields__}))
                    break
            if keyword_lower in info.get('description', '').lower():
                results.append(PackageInfo(**{k: v for k, v in info.items() if k in PackageInfo.__dataclass_fields__}))

        return results

    def list_registry(self) -> List[PackageInfo]:
        """列出注册表中所有包"""
        packages = self._registry.get('packages', {})
        return [
            PackageInfo(**{k: v for k, v in info.items() if k in PackageInfo.__dataclass_fields__})
            for info in packages.values()
        ]

    # ------------------------------------------------------------------
    # 安装
    # ------------------------------------------------------------------

    def install(self, package_name: str, version: Optional[str] = None) -> bool:
        """从注册中心安装包

        Args:
            package_name: 包名
            version: 版本号（可选）

        Returns:
            是否安装成功
        """
        packages = self._registry.get('packages', {})
        info = packages.get(package_name)

        if not info:
            print(f"错误: 未找到包 '{package_name}'")
            print(f"提示: 使用 'duan install --search {package_name}' 搜索")
            return False

        git_url = info.get('git', '')
        if not git_url:
            print(f"错误: 包 '{package_name}' 没有配置 Git 仓库地址")
            return False

        print(f"正在安装: {package_name} v{info.get('version', '?')}")
        print(f"  来源: {git_url}")

        return self._install_from_git(package_name, git_url)

    def install_from_git(self, git_url: str, package_name: Optional[str] = None) -> bool:
        """从 Git 仓库安装包

        Args:
            git_url: Git 仓库 URL
            package_name: 包名（可选，默认从 URL 提取）

        Returns:
            是否安装成功
        """
        if not package_name:
            package_name = git_url.rstrip('/').split('/')[-1].replace('.git', '')

        print(f"正在从 Git 安装: {package_name}")
        print(f"  仓库: {git_url}")

        return self._install_from_git(package_name, git_url)

    def install_from_path(self, local_path: str) -> bool:
        """从本地路径安装包

        Args:
            local_path: 本地包路径

        Returns:
            是否安装成功
        """
        src_path = Path(local_path).resolve()
        if not src_path.exists():
            print(f"错误: 路径不存在: {local_path}")
            return False

        package_name = src_path.name
        print(f"正在从本地安装: {package_name}")
        print(f"  路径: {src_path}")

        dest_dir = self._packages_dir / package_name
        try:
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(str(src_path), str(dest_dir))
            print(f"  已安装到: {dest_dir}")
            self._update_dependencies(package_name, f"path = \"packages/{package_name}\"")
            return True
        except Exception as e:
            print(f"错误: 复制失败: {e}")
            return False

    def _install_from_git(self, package_name: str, git_url: str) -> bool:
        """从 Git 仓库下载并安装"""
        # 检查 git 是否可用
        if not self._check_git():
            print("错误: 未找到 git 命令，请安装 Git")
            return False

        dest_dir = self._packages_dir / package_name
        cache_dir = self._cache_dir / package_name

        try:
            # 使用缓存或克隆
            if cache_dir.exists():
                print(f"  更新缓存: {cache_dir}")
                result = subprocess.run(
                    ['git', '-C', str(cache_dir), 'pull', '--ff-only'],
                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                    timeout=60
                )
                if result.returncode != 0:
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    return self._clone_repo(git_url, cache_dir, dest_dir, package_name)
            else:
                return self._clone_repo(git_url, cache_dir, dest_dir, package_name)

            return self._copy_from_cache(cache_dir, dest_dir, package_name)

        except subprocess.TimeoutExpired:
            print("错误: Git 操作超时")
            return False
        except Exception as e:
            print(f"错误: 安装失败: {e}")
            return False

    def _clone_repo(self, git_url: str, cache_dir: Path, dest_dir: Path, package_name: str) -> bool:
        """克隆仓库"""
        print(f"  克隆仓库...")
        cache_dir.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ['git', 'clone', '--depth', '1', git_url, str(cache_dir)],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=120
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if 'not found' in error_msg.lower() or 'repository' in error_msg.lower():
                print(f"错误: 仓库不存在或无权限访问: {git_url}")
            else:
                print(f"错误: Git 克隆失败: {error_msg[:200]}")
            return False

        return self._copy_from_cache(cache_dir, dest_dir, package_name)

    def _copy_from_cache(self, cache_dir: Path, dest_dir: Path, package_name: str) -> bool:
        """从缓存复制到项目 packages 目录"""
        try:
            if dest_dir.exists():
                shutil.rmtree(dest_dir)

            self._packages_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(str(cache_dir), str(dest_dir))

            # 清理 .git 目录
            git_dir = dest_dir / '.git'
            if git_dir.exists():
                shutil.rmtree(git_dir, ignore_errors=True)

            print(f"  已安装到: {dest_dir}")
            self._update_dependencies(package_name, f"path = \"packages/{package_name}\"")
            return True
        except Exception as e:
            print(f"错误: 复制文件失败: {e}")
            return False

    # ------------------------------------------------------------------
    # 依赖管理
    # ------------------------------------------------------------------

    def _update_dependencies(self, package_name: str, dep_value: str):
        """更新 package.toml 中的依赖"""
        toml_path = self.project_root / "package.toml"
        if not toml_path.exists():
            print(f"  提示: 项目没有 package.toml，跳过依赖更新")
            return

        try:
            content = toml_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            new_lines = []
            in_deps = False
            found_dep = False
            dep_line = f"{package_name} = {{ {dep_value} }}"

            for line in lines:
                stripped = line.strip()
                if stripped == '[dependencies]':
                    in_deps = True
                    new_lines.append(line)
                    continue
                if in_deps and stripped.startswith('['):
                    if not found_dep:
                        new_lines.append(dep_line)
                    new_lines.append(line)
                    in_deps = False
                    continue
                if in_deps and stripped.startswith(package_name):
                    new_lines.append(dep_line)
                    found_dep = True
                    continue
                new_lines.append(line)

            if in_deps and not found_dep:
                new_lines.append(dep_line)

            toml_path.write_text('\n'.join(new_lines), encoding='utf-8')
            print(f"  已更新 package.toml 依赖")
        except Exception as e:
            print(f"  警告: 更新 package.toml 失败: {e}")

    # ------------------------------------------------------------------
    # 已安装列表
    # ------------------------------------------------------------------

    def list_installed(self) -> List[Dict]:
        """列出已安装的包"""
        installed = []
        if self._packages_dir.exists():
            for d in sorted(self._packages_dir.iterdir()):
                if d.is_dir() and not d.name.startswith('.'):
                    duan_files = list(d.glob('*.duan'))
                    pkg_toml = d / 'package.toml'
                    version = '?'
                    desc = ''
                    if pkg_toml.exists():
                        try:
                            from package_manager import TomlParser
                            data = TomlParser().parse(pkg_toml.read_text(encoding='utf-8'))
                            pkg = data.get('package', {})
                            version = pkg.get('version', '?')
                            desc = pkg.get('description', '')
                        except Exception:
                            pass
                    installed.append({
                        'name': d.name,
                        'version': version,
                        'description': desc,
                        'files': len(duan_files),
                        'path': str(d.relative_to(self.project_root))
                    })
        return installed

    def uninstall(self, package_name: str) -> bool:
        """卸载包"""
        pkg_dir = self._packages_dir / package_name
        if not pkg_dir.exists():
            print(f"错误: 包 '{package_name}' 未安装")
            return False

        try:
            shutil.rmtree(pkg_dir)
            print(f"已卸载: {package_name}")
            self._remove_dependency(package_name)
            return True
        except Exception as e:
            print(f"错误: 卸载失败: {e}")
            return False

    def _remove_dependency(self, package_name: str):
        """从 package.toml 中移除依赖"""
        toml_path = self.project_root / "package.toml"
        if not toml_path.exists():
            return

        try:
            content = toml_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(package_name) and '=' in stripped:
                    continue
                new_lines.append(line)
            toml_path.write_text('\n'.join(new_lines), encoding='utf-8')
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 工具
    # ------------------------------------------------------------------

    @staticmethod
    def _check_git() -> bool:
        """检查 git 是否可用"""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True, text=True, encoding='utf-8', errors='replace',
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False


# ===========================================================================
# 命令行接口
# ===========================================================================

def run_install(args):
    """运行安装命令"""
    project_root = Path(args.project or '.').resolve()
    installer = PackageInstaller(project_root=project_root)

    if args.list:
        _cmd_list(installer)
        return

    if args.search:
        _cmd_search(installer, args.search)
        return

    if args.uninstall:
        installer.uninstall(args.uninstall)
        return

    if args.git:
        installer.install_from_git(args.git, args.package)
        return

    if args.path:
        installer.install_from_path(args.path)
        return

    if args.package:
        installer.install(args.package)
        return

    if args.registry:
        _cmd_list_registry(installer)
        return

    # 默认：显示帮助
    print("用法: duan install <包名> [选项]")
    print()
    print("选项:")
    print("  <包名>              从注册中心安装指定包")
    print("  --git <URL>         从 Git 仓库安装")
    print("  --path <路径>       从本地路径安装")
    print("  --search <关键词>   搜索包")
    print("  --list              列出已安装的包")
    print("  --registry          列出注册中心所有包")
    print("  --uninstall <包名>  卸载包")
    print("  -p, --project <目录> 指定项目目录")
    print()
    print("示例:")
    print("  duan install 标准数学扩展")
    print("  duan install --git https://github.com/user/repo.git")
    print("  duan install --path ./my-package")
    print("  duan install --search 网络")
    print("  duan install --list")


def _cmd_list(installer: PackageInstaller):
    """列出已安装的包"""
    installed = installer.list_installed()
    if not installed:
        print("(没有已安装的包)")
        print()
        print("使用 'duan install --registry' 查看可用包")
        print("使用 'duan install <包名>' 安装包")
        return

    print("已安装的包:")
    print("-" * 60)
    for pkg in installed:
        print(f"  {pkg['name']:<20} v{pkg['version']:<8} 文件: {pkg['files']}")
        if pkg['description']:
            print(f"    {pkg['description']}")
    print("-" * 60)
    print(f"共 {len(installed)} 个包")


def _cmd_search(installer: PackageInstaller, keyword: str):
    """搜索包"""
    results = installer.search(keyword)
    if not results:
        print(f"未找到与 '{keyword}' 相关的包")
        print()
        print("使用 'duan install --registry' 查看所有可用包")
        return

    print(f"搜索 '{keyword}' 的结果:")
    print("-" * 60)
    for pkg in results:
        print(f"  {pkg.name:<20} v{pkg.version:<8}")
        print(f"    描述: {pkg.description}")
        if pkg.keywords:
            print(f"    标签: {', '.join(pkg.keywords)}")
        print(f"    安装: duan install {pkg.name}")
        print()
    print("-" * 60)
    print(f"共 {len(results)} 个结果")


def _cmd_list_registry(installer: PackageInstaller):
    """列出注册中心所有包"""
    packages = installer.list_registry()
    if not packages:
        print("注册中心没有可用包")
        return

    print("注册中心可用包:")
    print("-" * 60)
    for pkg in packages:
        print(f"  {pkg.name:<20} v{pkg.version:<8}")
        print(f"    描述: {pkg.description}")
        if pkg.keywords:
            print(f"    标签: {', '.join(pkg.keywords)}")
        print(f"    安装: duan install {pkg.name}")
        print()
    print("-" * 60)
    print(f"共 {len(packages)} 个包")
    print()
    print("安装: duan install <包名>")


if __name__ == '__main__':
    # 命令行测试
    class Args:
        project = '.'
        package = None
        git = None
        path = None
        search = None
        list = False
        registry = False
        uninstall = None

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('package', nargs='?')
    ap.add_argument('--git')
    ap.add_argument('--path')
    ap.add_argument('--search')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--registry', action='store_true')
    ap.add_argument('--uninstall')
    ap.add_argument('-p', '--project', default='.')

    test_args = ap.parse_args()
    run_install(test_args)