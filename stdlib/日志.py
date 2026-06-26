"""
段言标准库 - 日志模块

提供分级日志输出功能：调试、信息、警告、错误、致命。
"""

import sys
import time as _time
from typing import Optional, TextIO


_LOG_LEVELS = {
    '调试': 10,
    '信息': 20,
    '警告': 30,
    '错误': 40,
    '致命': 50,
}

_current_level = 20
_format = '[{级别}] {时间} - {消息}'
_output_file: Optional[TextIO] = None


def _输出(级别: str, 消息: str) -> None:
    级别值 = _LOG_LEVELS.get(级别, 0)
    if 级别值 < _current_level:
        return
    时间_str = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())
    行 = _format.format(级别=级别, 时间=时间_str, 消息=消息)
    print(行, flush=True)
    if _output_file is not None:
        _output_file.write(行 + '\n')
        _output_file.flush()


def 调试(消息: str) -> None:
    """输出调试级别日志"""
    _输出('调试', 消息)


def 信息(消息: str) -> None:
    """输出信息级别日志"""
    _输出('信息', 消息)


def 警告(消息: str) -> None:
    """输出警告级别日志"""
    _输出('警告', 消息)


def 错误(消息: str) -> None:
    """输出错误级别日志"""
    _输出('错误', 消息)


def 致命(消息: str) -> None:
    """输出致命级别日志"""
    _输出('致命', 消息)


def 设置级别(级别: str) -> None:
    """
    设置日志级别

    参数:
        级别: '调试'、'信息'、'警告'、'错误'、'致命'
    """
    global _current_level
    if 级别 not in _LOG_LEVELS:
        raise RuntimeError(f"无效的日志级别: '{级别}'，可选：调试、信息、警告、错误、致命")
    _current_level = _LOG_LEVELS[级别]


def 设置格式(格式字符串: str) -> None:
    """
    设置日志格式

    可用占位符:
        {级别} - 日志级别
        {时间} - 当前时间
        {消息} - 日志消息

    默认格式: '[{级别}] {时间} - {消息}'
    """
    global _format
    _format = 格式字符串


def 设置输出文件(文件路径: Optional[str] = None) -> None:
    """
    设置日志输出文件

    参数:
        文件路径: 输出文件路径，为空则关闭文件输出
    """
    global _output_file
    if _output_file is not None:
        _output_file.close()
        _output_file = None
    if 文件路径 is not None:
        _output_file = open(文件路径, 'a', encoding='utf-8')


__all__ = [
    '调试', '信息', '警告', '错误', '致命',
    '设置级别', '设置格式', '设置输出文件',
]
