"""
段言标准库 - 正则表达式模块

提供正则匹配、查找、替换等功能。
"""

import re
from typing import List, Optional


def 匹配(模式: str, 字符串: str) -> Optional[str]:
    """
    检查字符串开头是否匹配正则模式
    
    参数:
        模式: 正则表达式模式
        字符串: 要匹配的字符串
    
    返回:
        匹配到的字符串，无匹配返回空
    
    示例:
        匹配('^段\\w+', '段言语言')  # '段言语言'
    """
    m = re.match(模式, 字符串)
    return m.group(0) if m else None


def 搜索(模式: str, 字符串: str) -> Optional[str]:
    """
    在字符串中搜索正则模式的第一个匹配
    
    参数:
        模式: 正则表达式模式
        字符串: 要搜索的字符串
    
    返回:
        第一个匹配的字符串，无匹配返回空
    """
    m = re.search(模式, 字符串)
    return m.group(0) if m else None


def 查找所有(模式: str, 字符串: str) -> List[str]:
    """
    查找字符串中所有正则匹配
    
    参数:
        模式: 正则表达式模式
        字符串: 要搜索的字符串
    
    返回:
        所有匹配字符串的列表
    """
    return re.findall(模式, 字符串)


def 替换(模式: str, 替换文本: str, 字符串: str) -> str:
    """
    使用正则替换字符串中的匹配
    
    参数:
        模式: 正则表达式模式
        替换文本: 替换文本（支持 \\1 反向引用）
        字符串: 要处理的字符串
    
    返回:
        替换后的字符串
    """
    try:
        return re.sub(模式, 替换文本, 字符串)
    except re.error as e:
        raise RuntimeError(f"正则替换失败: {e}")


def 分割(模式: str, 字符串: str) -> List[str]:
    """
    使用正则分割字符串
    
    参数:
        模式: 正则表达式模式
        字符串: 要分割的字符串
    
    返回:
        分割后的字符串列表
    """
    return re.split(模式, 字符串)


def 是否匹配(模式: str, 字符串: str) -> bool:
    """
    检查字符串是否完全匹配正则模式
    
    参数:
        模式: 正则表达式模式
        字符串: 要检查的字符串
    
    返回:
        是否匹配
    """
    return bool(re.fullmatch(模式, 字符串))


def 分组匹配(模式: str, 字符串: str) -> Optional[List[str]]:
    """
    获取正则匹配的分组
    
    参数:
        模式: 正则表达式模式（含分组）
        字符串: 要匹配的字符串
    
    返回:
        分组列表，无匹配返回空
    
    示例:
        分组匹配('(\\d{4})-(\\d{2})-(\\d{2})', '2026-06-16')
        # ['2026', '06', '16']
    """
    m = re.match(模式, 字符串)
    if m:
        return list(m.groups())
    return None


__all__ = [
    '匹配', '搜索', '查找所有',
    '替换', '分割', '是否匹配',
    '分组匹配',
]