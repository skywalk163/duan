"""
段言标准库 - 正则表达式模块

提供正则表达式匹配、搜索、替换、分割等操作

用法：
    从《正则》导入《匹配》，《查找》，《替换》。
    设 结果 为 匹配 "^\\d+" "123abc"。
"""

import re
from typing import List, Optional, Tuple, Any


def 匹配(模式: str, 字符串: str) -> Optional[dict]:
    """
    在字符串开头匹配模式

    参数:
        模式: 正则表达式模式
        字符串: 待匹配的字符串

    返回:
        匹配结果字典，包含 '匹配' 和 '分组' 字段；无匹配时返回空值
    """
    m = re.match(模式, 字符串)
    if m is None:
        return None
    return {
        '匹配': m.group(),
        '分组': m.groups(),
    }


def 搜索(模式: str, 字符串: str) -> Optional[dict]:
    """
    在字符串中搜索匹配

    参数:
        模式: 正则表达式模式
        字符串: 待搜索的字符串

    返回:
        匹配结果字典，包含 '匹配' 和 '分组' 字段；无匹配时返回空值
    """
    m = re.search(模式, 字符串)
    if m is None:
        return None
    return {
        '匹配': m.group(),
        '分组': m.groups(),
    }


def 全部匹配(模式: str, 字符串: str) -> List[str]:
    """
    查找所有匹配的子串

    参数:
        模式: 正则表达式模式
        字符串: 待搜索的字符串

    返回:
        所有匹配字符串的列表
    """
    return re.findall(模式, 字符串)


def 替换(模式: str, 替换为: str, 字符串: str, 次数: int = 0) -> str:
    """
    替换匹配的子串

    参数:
        模式: 正则表达式模式
        替换为: 替换后的字符串
        字符串: 原始字符串
        次数: 最大替换次数（0 表示全部替换）

    返回:
        替换后的字符串
    """
    return re.sub(模式, 替换为, 字符串, count=次数 if 次数 > 0 else 0)


def 分割(模式: str, 字符串: str, 最大分割: int = 0) -> List[str]:
    """
    按模式分割字符串

    参数:
        模式: 正则表达式模式
        字符串: 待分割的字符串
        最大分割: 最大分割次数（0 表示全部分割）

    返回:
        分割后的字符串列表
    """
    return re.split(模式, 字符串, maxsplit=最大分割 if 最大分割 > 0 else 0)


def 匹配迭代(模式: str, 字符串: str) -> List[dict]:
    """
    遍历所有匹配（返回每个匹配的详细信息）

    参数:
        模式: 正则表达式模式
        字符串: 待搜索的字符串

    返回:
        匹配结果字典列表，每个字典包含 '匹配'、'开始'、'结束' 字段
    """
    results = []
    for m in re.finditer(模式, 字符串):
        results.append({
            '匹配': m.group(),
            '开始': m.start(),
            '结束': m.end(),
            '分组': m.groups(),
        })
    return results


def 编译(模式: str) -> Any:
    """
    编译正则表达式（提高重复使用性能）

    参数:
        模式: 正则表达式模式

    返回:
        编译后的正则表达式对象
    """
    return re.compile(模式)


def 是否匹配(模式: str, 字符串: str) -> bool:
    """
    检查字符串是否完全匹配模式

    参数:
        模式: 正则表达式模式
        字符串: 待检查的字符串

    返回:
        是否完全匹配
    """
    return re.fullmatch(模式, 字符串) is not None


def 转义(字符串: str) -> str:
    """
    转义正则表达式中的特殊字符

    参数:
        字符串: 需要转义的原始字符串

    返回:
        转义后的安全字符串
    """
    return re.escape(字符串)


__all__ = [
    '匹配', '搜索', '全部匹配',
    '替换', '分割',
    '匹配迭代', '编译', '是否匹配', '转义',
]