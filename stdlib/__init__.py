"""
段言标准库

提供内置函数和模块支持

使用方式（段言代码）：
    内置函数直接可用：打印("你好"), 随机整数(1, 100)
    模块导入：从《JSON》导入《解析JSON》，《序列化JSON》。
"""

from .builtins import *

# 核心运行时模块
try:
    from .日期时间 import *
except ImportError:
    pass  # 依赖不可用时优雅降级

try:
    from .JSON import *
except ImportError:
    pass

try:
    from .哈希 import *
except ImportError:
    pass

try:
    from .正则表达式 import *
except ImportError:
    pass

# FFI 直通层模块
try:
    from .日志系统增强 import *
except ImportError:
    pass

try:
    from .进制转换 import *
except ImportError:
    pass

try:
    from .迭代工具 import *
except ImportError:
    pass

try:
    from .终端颜色 import *
except ImportError:
    pass

try:
    from .系统接口 import *
except ImportError:
    pass

try:
    from .配置 import *
except ImportError:
    pass

try:
    from .表格 import *
except ImportError:
    pass

try:
    from .随机数据 import *
except ImportError:
    pass

try:
    from .对象池缓存 import *
except ImportError:
    pass

try:
    from .CSV读写器 import *
except ImportError:
    pass

try:
    from .临时文件 import *
except ImportError:
    pass

try:
    from .外部命令 import *
except ImportError:
    pass

try:
    from .参数解析 import *
except ImportError:
    pass

try:
    from .美化输出 import *
except ImportError:
    pass

try:
    from .复制 import *
except ImportError:
    pass

try:
    from .文件系统 import *
except ImportError:
    pass

try:
    from .对象序列化 import *
except ImportError:
    pass

try:
    from .枚举 import *
except ImportError:
    pass

try:
    from .文本差异 import *
except ImportError:
    pass

try:
    from .压缩 import *
except ImportError:
    pass

try:
    from .字符串常量 import *
except ImportError:
    pass

try:
    from .函数工具 import *
except ImportError:
    pass

try:
    from .集合工具 import *
except ImportError:
    pass

try:
    from .FFI import *
except ImportError:
    pass

# P9 特色标准库模块
try:
    from .中文文本 import *
except ImportError:
    pass

try:
    from .历法 import *
except ImportError:
    pass

try:
    from .排版 import *
except ImportError:
    pass