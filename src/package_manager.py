"""
段言（Duan）包管理器

负责：
1. package.toml 项目配置文件的解析
2. 项目目录初始化（package.toml + 主.duan）
3. 入口模块发现与项目级编译入口

设计原则：
- 不依赖外部 toml 库，内置极简解析
- 所有文件操作均有异常安全保护
- 与 src/compiler.py、src/module_resolver.py 解耦
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class PackageConfig:
    """从 package.toml 解析出的包配置"""

    name: str = "未命名"
    version: str = "0.1.0"
    entry: str = "主.duan"
    dependencies: Dict[str, str] = field(default_factory=dict)
    authors: List[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "entry": self.entry,
            "dependencies": dict(self.dependencies),
            "authors": list(self.authors),
            "description": self.description,
        }


@dataclass
class Package:
    """解析后的完整包信息（包含模块 AST 等）"""

    config: PackageConfig
    root_path: Path
    modules: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# package.toml 极简解析器
# ---------------------------------------------------------------------------

class TomlParser:
    """极简 TOML 解析器（仅支持项目所需子集）

    支持语法：
      [section]
      key = "字符串"
      key = 123
      key = 1.5
      key = true / false / yes / no
      key = [ "a", "b" ]
      key = { sub = "value" }

    不支持：多行字符串、嵌套数组、[[arrays_of_tables]]。
    """

    _TRUE_VALUES = {"true", "True", "TRUE", "yes", "YES", "是", "真", "对"}
    _FALSE_VALUES = {"false", "False", "FALSE", "no", "NO", "否", "假", "错"}

    def parse(self, content: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        current_section: Optional[str] = None
        # 行内对象 / 数组可能跨多行，这里不处理，按单行来

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue

            # [section]
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].strip()
                continue

            # key = value
            if "=" in line:
                key, _, raw_val = line.partition("=")
                key = key.strip()
                raw_val = raw_val.strip()
                value = self._parse_value(raw_val)
                target = result
                if current_section is not None:
                    if current_section not in result:
                        result[current_section] = {}
                    target = result[current_section]
                target[key] = value
            # 否则：忽略无法解析的行

        return result

    def _parse_value(self, raw: str) -> Any:
        # 去掉行尾注释（仅在顶级分隔符之外时有效，这里做简单处理）
        # 查找不在字符串内的 #
        in_str = False
        comment_pos = -1
        for i, ch in enumerate(raw):
            if ch == '"':
                in_str = not in_str
            elif ch == "#" and not in_str:
                comment_pos = i
                break
        if comment_pos > 0:
            raw = raw[:comment_pos].strip()

        if not raw:
            return ""

        # 字符串 "..."
        if raw.startswith('"') and raw.endswith('"') and len(raw) >= 2:
            return raw[1:-1]
        # 单引号字符串
        if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
            return raw[1:-1]

        # 数组 [...]
        if raw.startswith("[") and raw.endswith("]"):
            return self._parse_array(raw)

        # 对象 {...}
        if raw.startswith("{") and raw.endswith("}"):
            return self._parse_inline_table(raw)

        # 布尔值
        if raw in self._TRUE_VALUES:
            return True
        if raw in self._FALSE_VALUES:
            return False

        # 数字
        try:
            if "." in raw or "e" in raw or "E" in raw:
                return float(raw)
            return int(raw)
        except (ValueError, TypeError):
            pass

        # 原样字符串（非标准，但更容错）
        return raw

    def _parse_array(self, raw: str) -> List[Any]:
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items: List[Any] = []
        # 按顶层逗号切分（忽略字符串内的逗号）
        parts = self._split_top_level(inner, ",")
        for part in parts:
            part = part.strip()
            if not part:
                continue
            items.append(self._parse_value(part))
        return items

    def _parse_inline_table(self, raw: str) -> Dict[str, Any]:
        inner = raw[1:-1].strip()
        if not inner:
            return {}
        result: Dict[str, Any] = {}
        parts = self._split_top_level(inner, ",")
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if "=" in part:
                k, _, v = part.partition("=")
                result[k.strip()] = self._parse_value(v.strip())
        return result

    @staticmethod
    def _split_top_level(text: str, sep: str) -> List[str]:
        """按顶层分隔符切分（忽略字符串、括号内的分隔符）"""
        depth = 0
        in_str = False
        parts: List[str] = []
        start = 0
        for i, ch in enumerate(text):
            if ch == '"' or ch == "'":
                in_str = not in_str
            elif not in_str and ch in "([{":
                depth += 1
            elif not in_str and ch in ")]}":
                depth -= 1
            elif not in_str and depth == 0 and ch == sep:
                parts.append(text[start:i])
                start = i + 1
        parts.append(text[start:])
        return parts


# ---------------------------------------------------------------------------
# PackageManager
# ---------------------------------------------------------------------------

class PackageManager:
    """段言包管理器。

    典型用法：
        pm = PackageManager(project_root)
        pm.init_project("myproject")    # 新建项目
        config = pm.load_config()       # 读取 package.toml
        result = pm.build_project()     # 编译整个项目
        status = pm.run_project()       # 运行
    """

    DEFAULT_CONFIG_TOML = """# 段言项目配置
[package]
name = "{name}"
version = "0.1.0"
entry = "主.duan"
authors = []
description = ""

[dependencies]
"""

    DEFAULT_MAIN_SOURCE = """段 主():
    打印("你好，段言！")
结束。
"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = Path(project_root or os.getcwd())
        self.config: Optional[PackageConfig] = None
        self.loaded_modules: Dict[str, Any] = {}
        self.search_paths: List[Path] = [self.project_root]

    # ------------------------------------------------------------------
    # 项目初始化
    # ------------------------------------------------------------------
    def init_project(self, name: Optional[str] = None) -> bool:
        """在 project_root 下创建 package.toml 与 主.duan。

        如果目录不存在则自动创建；文件已存在时返回 True（视为幂等）。
        """
        try:
            self.project_root.mkdir(parents=True, exist_ok=True)
            pkg_name = name or self.project_root.name or "新项目"
            toml_text = self.DEFAULT_CONFIG_TOML.format(name=pkg_name)

            toml_path = self.project_root / "package.toml"
            main_path = self.project_root / "主.duan"

            if not toml_path.exists():
                toml_path.write_text(toml_text, encoding="utf-8")
            if not main_path.exists():
                main_path.write_text(self.DEFAULT_MAIN_SOURCE, encoding="utf-8")

            # 读入新配置
            self.load_config()
            return True
        except OSError as e:
            print(f"[PackageManager] 初始化失败（IO错误）: {e}")
            return False
        except Exception as e:  # 容错兜底
            print(f"[PackageManager] 初始化失败: {e}")
            return False

    # ------------------------------------------------------------------
    # 配置加载
    # ------------------------------------------------------------------
    def load_config(self) -> Optional[PackageConfig]:
        """加载 project_root/package.toml。

        返回 PackageConfig 或 None（文件不存在或解析失败）。
        """
        config_path = self.project_root / "package.toml"
        if not config_path.exists():
            self.config = None
            return None
        try:
            text = config_path.read_text(encoding="utf-8")
            data = TomlParser().parse(text)

            pkg_section = data.get("package", {}) or {}
            deps_section = data.get("dependencies", {}) or {}

            # 支持 dependencies.dep = { version = "1.0", path = "..." }
            normalized_deps: Dict[str, str] = {}
            for dep_key, dep_val in deps_section.items():
                if isinstance(dep_val, dict):
                    normalized_deps[dep_key] = str(dep_val.get("version", ""))
                else:
                    normalized_deps[dep_key] = str(dep_val)

            authors_raw = pkg_section.get("authors", [])
            if isinstance(authors_raw, str):
                authors = [authors_raw]
            elif isinstance(authors_raw, list):
                authors = [str(a) for a in authors_raw]
            else:
                authors = []

            self.config = PackageConfig(
                name=str(pkg_section.get("name", self.project_root.name or "未命名")),
                version=str(pkg_section.get("version", "0.1.0")),
                entry=str(pkg_section.get("entry", "主.duan")),
                dependencies=normalized_deps,
                authors=authors,
                description=str(pkg_section.get("description", "")),
            )
            self.search_paths = [self.project_root]
            return self.config
        except UnicodeDecodeError as e:
            print(f"[PackageManager] package.toml 编码错误: {e}")
            self.config = None
            return None
        except Exception as e:
            print(f"[PackageManager] 读取 package.toml 失败: {e}")
            self.config = None
            return None

    # ------------------------------------------------------------------
    # 模块查找
    # ------------------------------------------------------------------
    def find_module(self, module_name: str) -> Optional[Path]:
        """根据模块名找到对应的 .duan 文件。

        支持格式：
          - 数学        ->  数学.duan
          - 数学.工具   ->  数学/工具.duan
          - 数学/工具   ->  数学/工具.duan
        """
        if not module_name:
            return None

        candidates: List[str] = [
            f"{module_name}.duan",
            module_name.replace(".", os.sep) + ".duan",
            module_name.replace("/", os.sep) + ".duan",
        ]
        # 去重保持顺序
        seen: Set[str] = set()
        unique_candidates: List[str] = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                unique_candidates.append(c)

        for base in self.search_paths:
            if not base.exists():
                continue
            for name in unique_candidates:
                path = base / name
                if path.is_file():
                    return path
        return None

    # ------------------------------------------------------------------
    # 构建与运行
    # ------------------------------------------------------------------
    def build_project(self) -> Dict[str, Any]:
        """编译整个项目：加载 package.toml，编译入口模块及依赖。

        返回字典：
            {
                'success': bool,
                'config': PackageConfig | None,
                'project_root': str,
                'entry': str,
                'modules': { module_name: {...} },
                'order': [module_name, ...],  # 拓扑排序
                'errors': [str, ...],
            }
        """
        # 加载配置
        if self.config is None:
            cfg = self.load_config()
            if cfg is None:
                return {
                    "success": False,
                    "error": "未找到 package.toml",
                    "config": None,
                    "project_root": str(self.project_root),
                    "entry": "",
                    "modules": {},
                    "order": [],
                    "errors": ["未找到 package.toml"],
                }

        entry_path = self.project_root / self.config.entry
        if not entry_path.exists():
            return {
                "success": False,
                "error": f"入口文件不存在: {self.config.entry}",
                "config": self.config,
                "project_root": str(self.project_root),
                "entry": str(self.config.entry),
                "modules": {},
                "order": [],
                "errors": [f"入口文件不存在: {self.config.entry}"],
            }

        # 依赖 DuanCompiler（延迟导入以避免循环）
        try:
            sys.path.insert(0, str(self.project_root.parent))
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from compiler import DuanCompiler
        except ImportError as e:
            return {
                "success": False,
                "error": f"导入 DuanCompiler 失败: {e}",
                "config": self.config,
                "project_root": str(self.project_root),
                "entry": str(self.config.entry),
                "modules": {},
                "order": [],
                "errors": [f"导入 DuanCompiler 失败: {e}"],
            }

        try:
            compiler = DuanCompiler(project_root=str(self.project_root))
            return compiler.compile_project(str(self.project_root))
        except Exception as e:
            return {
                "success": False,
                "error": f"编译失败: {e}",
                "config": self.config,
                "project_root": str(self.project_root),
                "entry": str(self.config.entry),
                "modules": {},
                "order": [],
                "errors": [f"编译失败: {e}"],
            }

    def run_project(self) -> int:
        """先构建，再尝试翻译入口模块并在隔离命名空间内 exec。

        返回 0 表示成功，非 0 表示失败。
        """
        result = self.build_project()
        if not result.get("success"):
            print(f"[PackageManager] 构建失败: {result.get('errors', [])}")
            return 1

        try:
            from code_generator import PythonCodeGenerator  # type: ignore
        except Exception:
            PythonCodeGenerator = None  # type: ignore

        try:
            from duan_parser_v3 import DuanParser  # type: ignore
        except Exception:
            DuanParser = None  # type: ignore

        entry_path = self.project_root / self.config.entry
        try:
            source = entry_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[PackageManager] 读取入口文件失败: {e}")
            return 2

        if PythonCodeGenerator is None or DuanParser is None:
            print(f"[PackageManager] code_generator/duan_parser_v3 不可用")
            print("[PackageManager] 源码：")
            print(source)
            return 2

        try:
            parser = DuanParser()
            ast_node = parser.parse(source)
            gen = PythonCodeGenerator()
            python_code = gen.generate(ast_node)
        except Exception as e:
            print(f"[PackageManager] 翻译失败: {e}")
            return 2

        print("=" * 50)
        print("[PackageManager] 生成的 Python 代码:")
        print("=" * 50)
        print(python_code)
        print("=" * 50)
        print("[PackageManager] 执行输出:")
        print("=" * 50)
        try:
            exec(python_code, {"__name__": "__main__"})
            return 0
        except Exception as e:
            print(f"[PackageManager] 运行时错误: {e}")
            return 3


# ---------------------------------------------------------------------------
# 顶层便捷函数
# ---------------------------------------------------------------------------

def load_package(project_root: Optional[Path] = None) -> Optional[PackageConfig]:
    """加载段言项目配置"""
    pm = PackageManager(project_root)
    return pm.load_config()


def init_package(project_root: Optional[Path] = None, name: Optional[str] = None) -> bool:
    """初始化段言项目"""
    pm = PackageManager(project_root)
    return pm.init_project(name)


def build_package(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """编译段言项目"""
    pm = PackageManager(project_root)
    return pm.build_project()


def run_package(project_root: Optional[Path] = None) -> int:
    """编译并运行段言项目"""
    pm = PackageManager(project_root)
    return pm.run_project()


# ===========================================================================
# 命令行（仅在直接运行该脚本时使用）
# ===========================================================================

if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "build"

    if cmd == "init":
        name = args[1] if len(args) > 1 else None
        ok = init_package(Path.cwd(), name)
        sys.exit(0 if ok else 1)
    elif cmd == "build":
        result = build_package(Path.cwd())
        if result.get("success"):
            print("✓ 构建成功")
            sys.exit(0)
        else:
            print(f"✗ 构建失败: {result.get('errors', [])}")
            sys.exit(1)
    elif cmd == "run":
        code = run_package(Path.cwd())
        sys.exit(code)
    else:
        print(f"用法: python package_manager.py {{init|build|run}}")
        sys.exit(2)
