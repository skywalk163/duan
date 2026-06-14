"""
段言标准库 - 时间模块

提供时间相关函数：当前时间, 暂停, 格式化时间, 计时
"""

import time as _time
from typing import Optional


def 当前时间() -> float:
    """获取当前时间戳（秒，浮点数）"""
    return _time.time()


def 暂停(秒数: float) -> None:
    """暂停执行指定秒数"""
    if 秒数 < 0:
        raise RuntimeError(f"暂停时间不能为负数: {秒数}")
    _time.sleep(秒数)


def 格式化时间(时间戳: Optional[float] = None, 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化时间
    
    参数:
        时间戳: 时间戳（默认当前时间）
        格式: 格式字符串（默认 '%Y-%m-%d %H:%M:%S'）
    
    返回:
        格式化后的时间字符串
    
    格式说明:
        %Y - 四位年份
        %m - 两位月份 (01-12)
        %d - 两位日期 (01-31)
        %H - 两位小时 (00-23)
        %M - 两位分钟 (00-59)
        %S - 两位秒 (00-59)
    """
    if 时间戳 is None:
        时间戳 = _time.time()
    return _time.strftime(格式, _time.localtime(时间戳))


def 当前日期(时间戳: Optional[float] = None) -> str:
    """获取当前日期字符串 YYYY-MM-DD"""
    return 格式化时间(时间戳, '%Y-%m-%d')


def 当前时间字符串(时间戳: Optional[float] = None) -> str:
    """获取当前时间字符串 HH:MM:SS"""
    return 格式化时间(时间戳, '%H:%M:%S')


def 计时开始() -> float:
    """开始计时，返回当前时间戳"""
    return _time.perf_counter()


def 计时结束(开始时间: float) -> float:
    """
    结束计时，返回经过的秒数
    
    用法:
        设 开始 等于 计时开始。
        # ... 执行操作 ...
        设 耗时 等于 计时结束 开始。
        打印 "耗时：" 加 转字符串 耗时 加 "秒"。
    """
    return _time.perf_counter() - 开始时间


def 日期部分(时间戳: Optional[float] = None) -> dict:
    """
    获取日期各部分
    
    返回:
        { '年': 2026, '月': 6, '日': 14, '时': 10, '分': 30, '秒': 45 }
    """
    if 时间戳 is None:
        时间戳 = _time.time()
    t = _time.localtime(时间戳)
    return {
        '年': t.tm_year,
        '月': t.tm_mon,
        '日': t.tm_mday,
        '时': t.tm_hour,
        '分': t.tm_min,
        '秒': t.tm_sec,
    }


__all__ = [
    '当前时间', '暂停', '格式化时间',
    '当前日期', '当前时间字符串',
    '计时开始', '计时结束', '日期部分',
]