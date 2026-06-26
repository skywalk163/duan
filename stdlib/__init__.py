"""
段言标准库

提供内置函数和模块支持

使用方式（段言代码）：
    内置函数直接可用：打印("你好"), 随机整数(1, 100)
    模块导入：从《JSON》导入《解析JSON》，《序列化JSON》。
"""

from .builtins import *

# 新模块导入
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
    from .正则 import *
except ImportError:
    pass

# 新增标准库模块
try:
    from .日志 import *
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
    from .命令行参数 import *
except ImportError:
    pass

try:
    from .终端颜色 import *
except ImportError:
    pass

try:
    from .系统信息 import *
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
    from .缓存 import *
except ImportError:
    pass

try:
    from .CSV import *
except ImportError:
    pass