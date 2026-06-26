"""段言标准库 - 系统信息模块"""

import os
import sys
import platform as _platform

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False


def 操作系统() -> str:
    """返回操作系统名称"""
    if sys.platform.startswith("linux"):
        return "Linux"
    elif sys.platform == "darwin":
        return "macOS"
    elif sys.platform == "win32":
        return "Windows"
    return sys.platform


def Python版本() -> str:
    """返回 Python 版本"""
    return sys.version


def CPU数量() -> int:
    """返回 CPU 核心数"""
    if _HAS_PSUTIL:
        return psutil.cpu_count(logical=False) or 1
    return os.cpu_count() or 1


def 内存总量() -> int:
    """返回总内存（字节）"""
    if _HAS_PSUTIL:
        return psutil.virtual_memory().total
    return 0


def 内存可用() -> int:
    """返回可用内存（字节）"""
    if _HAS_PSUTIL:
        return psutil.virtual_memory().available
    return 0


def 当前进程ID() -> int:
    """返回当前进程 ID"""
    return os.getpid()


def 线程数() -> int:
    """返回当前线程数"""
    if _HAS_PSUTIL:
        return psutil.Process().num_threads()
    import threading
    return threading.active_count()


def 主机名() -> str:
    """返回主机名"""
    return _platform.node()


def 用户名() -> str:
    """返回当前用户名"""
    if _HAS_PSUTIL:
        return psutil.Process().username()
    return os.getlogin()
