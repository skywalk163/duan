"""
段言标准库 - 时间模块

封装 time 模块，提供时间相关的底层操作，
与日期时间模块互补，侧重秒级时间戳、性能计时等。
"""

import time
import datetime
from typing import Tuple, Optional


def 时间戳() -> float:
    """获取当前时间戳（秒级，浮点数）"""
    return time.time()


def 时间戳毫秒() -> int:
    """获取当前时间戳（毫秒级整数）"""
    return int(time.time() * 1000)


def 时间戳纳秒() -> int:
    """获取当前时间戳（纳秒级整数）"""
    return time.time_ns()


def 休眠(秒数: float) -> None:
    """休眠指定秒数"""
    time.sleep(秒数)


def 等待(秒数: float) -> None:
    """等待指定秒数（休眠的别名）"""
    time.sleep(秒数)


def 性能计数器() -> float:
    """
    获取高精度性能计数器值（用于测量短时间间隔）
    
    返回:
        性能计数器值（秒）
    """
    return time.perf_counter()


def 性能计数器纳秒() -> int:
    """获取高精度性能计数器值（纳秒）"""
    return time.perf_counter_ns()


def 单调时间() -> float:
    """
    获取单调时钟值（不会因为系统时间调整而倒退）
    
    返回:
        单调时钟值（秒）
    """
    return time.monotonic()


def 进程时间() -> float:
    """
    获取进程CPU时间（用户+系统）
    
    返回:
        进程CPU时间（秒）
    """
    return time.process_time()


def 线程时间() -> float:
    """
    获取线程CPU时间
    
    返回:
        线程CPU时间（秒）
    """
    return time.thread_time()


def 测量执行时间(函数, *参数, **关键字参数) -> tuple:
    """
    测量函数执行时间
    
    参数:
        函数: 要测量的函数
        参数: 函数位置参数
        关键字参数: 函数关键字参数
    
    返回:
        (返回值, 耗时秒数)
    """
    开始 = time.perf_counter()
    结果 = 函数(*参数, **关键字参数)
    结束 = time.perf_counter()
    return 结果, 结束 - 开始


def 本地时间(时间戳: float = None) -> time.struct_time:
    """
    获取本地时间元组
    
    参数:
        时间戳: 时间戳，None表示当前时间
    
    返回:
        时间元组
    """
    if 时间戳 is None:
        return time.localtime()
    return time.localtime(时间戳)


def UTC时间(时间戳: float = None) -> time.struct_time:
    """
    获取UTC时间元组
    
    参数:
        时间戳: 时间戳，None表示当前时间
    
    返回:
        UTC时间元组
    """
    if 时间戳 is None:
        return time.gmtime()
    return time.gmtime(时间戳)


def 时间元组转时间戳(时间元组: time.struct_time) -> float:
    """时间元组转时间戳"""
    return time.mktime(时间元组)


def 格式化时间(格式: str = "%Y-%m-%d %H:%M:%S", 时间戳: float = None) -> str:
    """
    格式化时间
    
    参数:
        格式: 格式化字符串
        时间戳: 时间戳，None表示当前时间
    
    返回:
        格式化后的时间字符串
    """
    if 时间戳 is None:
        return time.strftime(格式, time.localtime())
    return time.strftime(格式, time.localtime(时间戳))


def 解析时间(时间字符串: str, 格式: str = "%Y-%m-%d %H:%M:%S") -> time.struct_time:
    """
    解析时间字符串为时间元组
    
    参数:
        时间字符串: 时间字符串
        格式: 格式化字符串
    
    返回:
        时间元组
    """
    return time.strptime(时间字符串, 格式)


def 时区偏移() -> int:
    """
    获取本地时区与UTC的偏移量（秒）
    
    返回:
        偏移秒数，负数表示在UTC以东（如中国为-28800）
    """
    return time.timezone


def 时区名称() -> str:
    """获取本地时区名称"""
    return time.tzname[0]


def 夏令时() -> bool:
    """当前是否为夏令时"""
    return time.daylight != 0


class 秒表:
    """秒表 - 用于测量经过时间"""
    
    def __init__(self, 自动启动: bool = True):
        self._开始时间 = None
        self._累计时间 = 0.0
        self._运行中 = False
        if 自动启动:
            self.启动()
    
    def 启动(self) -> None:
        """启动秒表"""
        if not self._运行中:
            self._开始时间 = time.perf_counter()
            self._运行中 = True
    
    def 停止(self) -> float:
        """停止秒表，返回累计时间"""
        if self._运行中:
            self._累计时间 += time.perf_counter() - self._开始时间
            self._运行中 = False
        return self._累计时间
    
    def 重置(self) -> None:
        """重置秒表"""
        self._开始时间 = None
        self._累计时间 = 0.0
        self._运行中 = False
    
    def 读取(self) -> float:
        """读取当前经过时间（不停止）"""
        if self._运行中:
            return self._累计时间 + (time.perf_counter() - self._开始时间)
        return self._累计时间
    
    def 打点(self, 名称: str = None) -> float:
        """记录一个时间点，返回从开始到现在的时间"""
        当前时间 = self.读取()
        return 当前时间


def 创建秒表(自动启动: bool = True) -> 秒表:
    """创建秒表（便捷函数）"""
    return 秒表(自动启动)


__all__ = [
    '时间戳', '时间戳毫秒', '时间戳纳秒',
    '休眠', '等待',
    '性能计数器', '性能计数器纳秒',
    '单调时间', '进程时间', '线程时间',
    '测量执行时间',
    '本地时间', 'UTC时间',
    '时间元组转时间戳',
    '格式化时间', '解析时间',
    '时区偏移', '时区名称', '夏令时',
    '秒表', '创建秒表',
]
