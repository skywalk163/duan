"""
段言（DuanLang）版本信息集中管理

本模块提供统一的版本号、发布日期、版本名称等信息。
所有需要版本号的模块应从此处导入，而非各自定义。
"""

# 版本号
__version__ = "6.0.0"
VERSION = "6.0.0"
VERSION_MAJOR = 6
VERSION_MINOR = 0
VERSION_PATCH = 0

# 版本名称
VERSION_NAME = "v6.0 全面自举与生态建设版"

# 发布日期
RELEASE_DATE = "2026-10-29"

# 版本阶段: dev / alpha / beta / rc / stable
RELEASE_STAGE = "stable"

# 支持的语法层级
SUPPORTED_LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7"]

# 支持的编译器后端
COMPILER_BACKENDS = ["python", "llvm", "c", "wasm"]

# 版本描述
VERSION_DESCRIPTION = """
段言 v6.0 是自 v5.1 以来的重大版本，历时 12 周开发。

核心亮点：
- 完全自举：Level 8 编译器全部用段言自身编写，4 轮编译收敛
- 类型系统完善：泛型、联合类型、模式匹配
- 调试体验增强：统一错误格式、编译错误精准定位、REPL 完善
- 模块系统与包管理器：包注册表、版本管理、依赖循环检测
- 生态建设：VSCode 扩展、文档站点、在线 Playground
- 性能优化：LLVM 优化 Pass 管线、增量编译、DWARF 调试信息
- 跨平台支持：Windows/Linux/macOS 全平台 CI
- 测试覆盖：1918+ 测试用例全面覆盖
"""

# 最低 Python 版本要求
MINIMUM_PYTHON_VERSION = (3, 10)

# 推荐 Python 版本
RECOMMENDED_PYTHON_VERSION = (3, 12)


def get_version_info() -> dict:
    """获取版本信息字典"""
    return {
        "version": VERSION,
        "major": VERSION_MAJOR,
        "minor": VERSION_MINOR,
        "patch": VERSION_PATCH,
        "name": VERSION_NAME,
        "release_date": RELEASE_DATE,
        "stage": RELEASE_STAGE,
        "supported_levels": SUPPORTED_LEVELS,
        "compiler_backends": COMPILER_BACKENDS,
        "min_python": MINIMUM_PYTHON_VERSION,
        "recommended_python": RECOMMENDED_PYTHON_VERSION,
    }


def get_version_string() -> str:
    """获取人类可读的版本字符串"""
    stage = f"-{RELEASE_STAGE}" if RELEASE_STAGE != "stable" else ""
    return f"{VERSION}{stage} ({RELEASE_DATE})"


def get_full_version_string() -> str:
    """获取完整版本字符串"""
    return f"段言 DuanLang v{VERSION}「{VERSION_NAME}」— {RELEASE_DATE}"