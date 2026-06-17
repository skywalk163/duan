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


# =============================================================================
# 时间差与计算
# =============================================================================

def 时间差(开始时间戳: float, 结束时间戳: Optional[float] = None) -> dict:
    """
    计算时间差

    参数:
        开始时间戳: 起始时间戳
        结束时间戳: 结束时间戳（默认当前时间）

    返回:
        {'天': d, '时': h, '分': m, '秒': s, '总秒数': total}
    """
    if 结束时间戳 is None:
        结束时间戳 = _time.time()
    diff = 结束时间戳 - 开始时间戳
    if diff < 0:
        diff = 0
    days = int(diff // 86400)
    hours = int((diff % 86400) // 3600)
    minutes = int((diff % 3600) // 60)
    seconds = diff % 60
    return {
        '天': days,
        '时': hours,
        '分': minutes,
        '秒': seconds,
        '总秒数': round(diff, 6),
    }


def 日期转时间戳(年: int, 月: int, 日: int, 时: int = 0, 分: int = 0, 秒: int = 0) -> float:
    """
    将日期时间转换为时间戳

    参数:
        年: 年份
        月: 月份 (1-12)
        日: 日期 (1-31)
        时: 小时 (0-23)
        分: 分钟 (0-59)
        秒: 秒 (0-59)

    返回:
        时间戳（秒）
    """
    try:
        t = (年, 月, 日, 时, 分, 秒, 0, 0, -1)
        return _time.mktime(t)
    except Exception as e:
        raise RuntimeError(f"日期时间无效: {年}-{月}-{日} {时}:{分}:{秒}")


def 星期几(时间戳: Optional[float] = None) -> int:
    """
    获取星期几（0=周一，6=周日）

    参数:
        时间戳: 时间戳（默认当前时间）

    返回:
        0-6 的整数
    """
    if 时间戳 is None:
        时间戳 = _time.time()
    t = _time.localtime(时间戳)
    return t.tm_wday


def 星期名称(时间戳: Optional[float] = None) -> str:
    """
    获取星期名称

    参数:
        时间戳: 时间戳（默认当前时间）

    返回:
        '星期一' 到 '星期日'
    """
    days = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return days[星期几(时间戳)]


def 是否工作日(时间戳: Optional[float] = None) -> bool:
    """
    判断是否为工作日（周一至周五）

    参数:
        时间戳: 时间戳（默认当前时间）

    返回:
        是否为工作日
    """
    return 星期几(时间戳) < 5


def 是否周末(时间戳: Optional[float] = None) -> bool:
    """
    判断是否为周末（周六或周日）

    参数:
        时间戳: 时间戳（默认当前时间）

    返回:
        是否为周末
    """
    return 星期几(时间戳) >= 5


def N天后(天数: int, 基准时间: Optional[float] = None) -> float:
    """
    获取 N 天后的时间戳

    参数:
        天数: 天数（负数表示之前）
        基准时间: 基准时间戳（默认当前时间）

    返回:
        N 天后的时间戳
    """
    if 基准时间 is None:
        基准时间 = _time.time()
    return 基准时间 + 天数 * 86400


def N小时后(小时数: float, 基准时间: Optional[float] = None) -> float:
    """
    获取 N 小时后的时间戳

    参数:
        小时数: 小时数（负数表示之前）
        基准时间: 基准时间戳（默认当前时间）

    返回:
        N 小时后的时间戳
    """
    if 基准时间 is None:
        基准时间 = _time.time()
    return 基准时间 + 小时数 * 3600


def 解析时间(时间字符串: str, 格式: str = '%Y-%m-%d %H:%M:%S') -> float:
    """
    将时间字符串解析为时间戳

    参数:
        时间字符串: 时间字符串
        格式: 格式字符串（与 格式化时间 中的格式一致）

    返回:
        时间戳
    """
    try:
        t = _time.strptime(时间字符串, 格式)
        return _time.mktime(t)
    except Exception as e:
        raise RuntimeError(f"无法解析时间字符串 '{时间字符串}': {e}")


__all__ = [
    '当前时间', '暂停', '格式化时间',
    '当前日期', '当前时间字符串',
    '计时开始', '计时结束', '日期部分',

    # 时间差与计算
    '时间差', '日期转时间戳',
    '星期几', '星期名称',
    '是否工作日', '是否周末',
    'N天后', 'N小时后', '解析时间',
]