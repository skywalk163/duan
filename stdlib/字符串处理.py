"""
段言标准库 - 字符串处理模块

提供字符串操作函数：长度、拼接、分割、替换、查找、大小写转换等
"""

from typing import List, Optional


def 长度(s: str) -> int:
    """返回字符串长度"""
    return len(s)


def 拼接(*args: str) -> str:
    """拼接多个字符串"""
    return ''.join(args)


def 分割(s: str, sep: str = '') -> List[str]:
    """分割字符串，默认按空格分割"""
    if not sep:
        return s.split()
    return s.split(sep)


def 替换(s: str, old: str, new: str, 次数: int = -1) -> str:
    """替换字符串中的子串"""
    if 次数 < 0:
        return s.replace(old, new)
    return s.replace(old, new, 次数)


def 查找(s: str, sub: str) -> int:
    """查找子串位置，未找到返回 -1"""
    return s.find(sub)


def 大写(s: str) -> str:
    """转换为大写"""
    return s.upper()


def 小写(s: str) -> str:
    """转换为小写"""
    return s.lower()


def 去除空格(s: str) -> str:
    """去除两端空格"""
    return s.strip()


def 去空格(s: str) -> str:
    """去除两端空格（别名）"""
    return s.strip()


def 判断开头(s: str, prefix: str) -> bool:
    """判断字符串是否以指定前缀开头"""
    return s.startswith(prefix)


def 判断结尾(s: str, suffix: str) -> bool:
    """判断字符串是否以指定后缀结尾"""
    return s.endswith(suffix)


def 格式化(template: str, *args) -> str:
    """格式化字符串"""
    return template.format(*args)


def 截取(s: str, start: int, end: Optional[int] = None) -> str:
    """截取子串"""
    if end is None:
        return s[start:]
    return s[start:end]


def 重复(s: str, n: int) -> str:
    """重复字符串 n 次"""
    return s * n


def 计数(s: str, sub: str) -> int:
    """统计子串出现次数"""
    return s.count(sub)


def 反转(s: str) -> str:
    """反转字符串"""
    return s[::-1]