"""
段言标准库 - 日期时间模块

提供日期时间获取、格式化、解析、计算等功能。
"""

import time
from datetime import datetime, timedelta, date
from typing import Optional, Union


def 当前时间(format_string: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    获取当前日期时间字符串
    
    参数:
        format_string: 格式模板（默认 '%Y-%m-%d %H:%M:%S'）
    
    返回:
        格式化后的日期时间字符串
    
    示例:
        当前时间()               # '2026-06-16 10:30:00'
        当前时间('%Y年%m月%d日')  # '2026年06月16日'
    """
    return datetime.now().strftime(format_string)


def 当前日期(format_string: str = '%Y-%m-%d') -> str:
    """
    获取当前日期字符串
    
    参数:
        format_string: 格式模板（默认 '%Y-%m-%d'）
    
    返回:
        格式化后的日期字符串
    """
    return date.today().strftime(format_string)


def 时间戳() -> float:
    """
    获取当前 Unix 时间戳（秒）
    
    返回:
        浮点数时间戳
    """
    return time.time()


def 格式化时间(时间对象: Union[str, float], 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    将时间戳或时间字符串格式化为指定格式
    
    参数:
        时间对象: Unix 时间戳（浮点数）或 'YYYY-MM-DD HH:MM:SS' 格式字符串
        格式: 目标格式模板
    
    返回:
        格式化后的时间字符串
    """
    if isinstance(时间对象, (int, float)):
        dt = datetime.fromtimestamp(时间对象)
    else:
        # 尝试多种格式解析
        for fmt in [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
        ]:
            try:
                dt = datetime.strptime(时间对象, fmt)
                break
            except ValueError:
                continue
        else:
            raise RuntimeError(f"无法解析时间字符串: '{时间对象}'")
    
    return dt.strftime(格式)


def 解析时间(time_str: str, format_string: str = '%Y-%m-%d %H:%M:%S') -> float:
    """
    解析时间字符串为 Unix 时间戳
    
    参数:
        time_str: 时间字符串
        format_string: 输入格式模板
    
    返回:
        Unix 时间戳（浮点数）
    """
    try:
        dt = datetime.strptime(time_str, format_string)
        return dt.timestamp()
    except ValueError as e:
        raise RuntimeError(f"时间解析失败: {e}")


def 创建日期(年: int, 月: int, 日: int) -> str:
    """
    创建日期字符串
    
    参数:
        年: 年份
        月: 月份（1-12）
        日: 日（1-31）
    
    返回:
        'YYYY-MM-DD' 格式日期字符串
    """
    try:
        d = date(年, 月, 日)
        return d.isoformat()
    except ValueError as e:
        raise RuntimeError(f"无效日期: {e}")


def 时间加减(时间对象: str, 天数: int = 0, 小时: int = 0, 分钟: int = 0, 秒: int = 0) -> str:
    """
    时间加减运算
    
    参数:
        时间对象: 'YYYY-MM-DD HH:MM:SS' 格式时间字符串
        天数: 要加的天数（负数表示减）
        小时: 要加的小时数
        分钟: 要加的分钟数
        秒: 要加的秒数
    
    返回:
        计算后的时间字符串
    """
    try:
        dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            dt = datetime.strptime(时间对象, '%Y-%m-%d')
        except ValueError:
            raise RuntimeError(f"无法解析时间: '{时间对象}'，需为 'YYYY-MM-DD HH:MM:SS' 格式")
    
    delta = timedelta(days=天数, hours=小时, minutes=分钟, seconds=秒)
    result = dt + delta
    return result.strftime('%Y-%m-%d %H:%M:%S')


def 日期差(日期1: str, 日期2: str) -> int:
    """
    计算两个日期之间的天数差
    
    参数:
        日期1: 第一个日期 'YYYY-MM-DD'
        日期2: 第二个日期 'YYYY-MM-DD'
    
    返回:
        天数差（日期2 - 日期1）
    """
    try:
        d1 = datetime.strptime(日期1, '%Y-%m-%d').date()
        d2 = datetime.strptime(日期2, '%Y-%m-%d').date()
    except ValueError as e:
        raise RuntimeError(f"日期格式无效: {e}")
    
    return (d2 - d1).days


def 获取年(时间对象: str) -> int:
    """从日期时间字符串中获取年份"""
    try:
        dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        dt = datetime.strptime(时间对象, '%Y-%m-%d')
    return dt.year


def 获取月(时间对象: str) -> int:
    """从日期时间字符串中获取月份"""
    try:
        dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        dt = datetime.strptime(时间对象, '%Y-%m-%d')
    return dt.month


def 获取日(时间对象: str) -> int:
    """从日期时间字符串中获取日"""
    try:
        dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        dt = datetime.strptime(时间对象, '%Y-%m-%d')
    return dt.day


def 获取时(时间对象: str) -> int:
    """从日期时间字符串中获取小时"""
    dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    return dt.hour


def 获取分(时间对象: str) -> int:
    """从日期时间字符串中获取分钟"""
    dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    return dt.minute


def 获取秒(时间对象: str) -> int:
    """从日期时间字符串中获取秒"""
    dt = datetime.strptime(时间对象, '%Y-%m-%d %H:%M:%S')
    return dt.second


__all__ = [
    '当前时间', '当前日期', '时间戳',
    '格式化时间', '解析时间', '创建日期',
    '时间加减', '日期差',
    '获取年', '获取月', '获取日',
    '获取时', '获取分', '获取秒',
]