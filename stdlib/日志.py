"""
段言标准库 - 日志模块

提供分级日志输出功能：调试、信息、警告、错误、致命。
支持日志轮转、自定义格式化器等功能。
"""

import sys
import time as _time
import os
from typing import Optional, TextIO, Dict, Any, Callable


_LOG_LEVELS = {
    '调试': 10,
    '信息': 20,
    '警告': 30,
    '错误': 40,
    '致命': 50,
}

_LEVEL_NAMES = {v: k for k, v in _LOG_LEVELS.items()}

_current_level = 20
_format = '[{级别}] {时间} - {消息}'
_output_file: Optional[TextIO] = None
_enable_console = True
_log_formatters: Dict[str, Callable] = {}


def _输出(级别: str, 消息: str) -> None:
    级别值 = _LOG_LEVELS.get(级别, 0)
    if 级别值 < _current_level:
        return
    时间_str = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())
    行 = _format.format(级别=级别, 时间=时间_str, 消息=消息)
    if _enable_console:
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


def 获取级别() -> str:
    """获取当前日志级别"""
    return _LEVEL_NAMES.get(_current_level, '信息')


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


def 启用控制台输出(启用: bool = True) -> None:
    """启用或禁用控制台输出"""
    global _enable_console
    _enable_console = 启用


def 禁用控制台输出() -> None:
    """禁用控制台输出"""
    启用控制台输出(False)


def 启用文件输出(文件路径: str) -> None:
    """启用文件输出"""
    设置输出文件(文件路径)


def 禁用文件输出() -> None:
    """禁用文件输出"""
    设置输出文件(None)


def 输出到标准错误() -> None:
    """将控制台输出重定向到标准错误"""
    global _output_file
    _output_file = sys.stderr


def 输出到标准输出() -> None:
    """将控制台输出重定向到标准输出"""
    global _output_file
    _output_file = sys.stdout


def 带上下文日志(级别: str, 消息: str, **上下文) -> None:
    """
    带上下文的日志输出

    参数:
        级别: 日志级别
        消息: 日志消息
        上下文: 额外的上下文信息
    """
    级别值 = _LOG_LEVELS.get(级别, 0)
    if 级别值 < _current_level:
        return
    时间_str = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())
    上下文_str = ' '.join(f'{k}={v}' for k, v in 上下文.items())
    if 上下文_str:
        消息 = f'{消息} [{上下文_str}]'
    行 = _format.format(级别=级别, 时间=时间_str, 消息=消息)
    if _enable_console:
        print(行, flush=True)
    if _output_file is not None:
        _output_file.write(行 + '\n')
        _output_file.flush()


def 调试上下文(消息: str, **上下文) -> None:
    """带上下文的调试日志"""
    带上下文日志('调试', 消息, **上下文)


def 信息上下文(消息: str, **上下文) -> None:
    """带上下文的信息日志"""
    带上下文日志('信息', 消息, **上下文)


def 警告上下文(消息: str, **上下文) -> None:
    """带上下文的警告日志"""
    带上下文日志('警告', 消息, **上下文)


def 错误上下文(消息: str, **上下文) -> None:
    """带上下文的错误日志"""
    带上下文日志('错误', 消息, **上下文)


def 致命上下文(消息: str, **上下文) -> None:
    """带上下文的致命日志"""
    带上下文日志('致命', 消息, **上下文)


def 日志异常(级别: str = '错误') -> None:
    """
    记录异常信息

    参数:
        级别: 日志级别，默认为'错误'
    """
    import traceback
    异常信息 = traceback.format_exc()
    带上下文日志(级别, f'异常发生:\n{异常信息}')


def 调试异常() -> None:
    """记录调试级别的异常信息"""
    日志异常('调试')


def 信息异常() -> None:
    """记录信息级别的异常信息"""
    日志异常('信息')


def 警告异常() -> None:
    """记录警告级别的异常信息"""
    日志异常('警告')


def 错误异常() -> None:
    """记录错误级别的异常信息"""
    日志异常('错误')


def 致命异常() -> None:
    """记录致命级别的异常信息"""
    日志异常('致命')


def 日志函数(级别: str) -> Callable:
    """
    获取指定级别的日志函数

    参数:
        级别: 日志级别

    返回:
        日志函数
    """
    函数映射 = {
        '调试': 调试,
        '信息': 信息,
        '警告': 警告,
        '错误': 错误,
        '致命': 致命,
    }
    return 函数映射.get(级别, 信息)


def 级别数值(级别: str) -> int:
    """获取级别的数值"""
    return _LOG_LEVELS.get(级别, 20)


def 级别名称(数值: int) -> str:
    """获取数值对应的级别名称"""
    return _LEVEL_NAMES.get(数值, '信息')


def 日志轮转(文件路径: str, 最大大小: int = 1024 * 1024, 备份数量: int = 5) -> None:
    """
    日志轮转

    参数:
        文件路径: 日志文件路径
        最大大小: 单个日志文件最大大小（字节），默认1MB
        备份数量: 保留的备份文件数量，默认5
    """
    if not os.path.exists(文件路径):
        return
    文件大小 = os.path.getsize(文件路径)
    if 文件大小 < 最大大小:
        return

    for i in range(备份数量 - 1, 0, -1):
        旧文件 = f'{文件路径}.{i}'
        新文件 = f'{文件路径}.{i + 1}'
        if os.path.exists(旧文件):
            if os.path.exists(新文件):
                os.remove(新文件)
            os.rename(旧文件, 新文件)

    if os.path.exists(f'{文件路径}.1'):
        os.remove(f'{文件路径}.1')
    os.rename(文件路径, f'{文件路径}.1')

    global _output_file
    if _output_file is not None:
        _output_file.close()
    _output_file = open(文件路径, 'w', encoding='utf-8')


def 设置日志轮转(文件路径: str, 最大大小: int = 1024 * 1024, 备份数量: int = 5) -> None:
    """
    设置日志轮转

    参数:
        文件路径: 日志文件路径
        最大大小: 单个日志文件最大大小（字节），默认1MB
        备份数量: 保留的备份文件数量，默认5
    """
    设置输出文件(文件路径)
    日志轮转(文件路径, 最大大小, 备份数量)


def 添加格式化器(名称: str, 格式化函数: Callable) -> None:
    """
    添加自定义格式化器

    参数:
        名称: 格式化器名称
        格式化函数: 格式化函数，接收(级别, 时间, 消息)参数
    """
    _log_formatters[名称] = 格式化函数


def 使用格式化器(名称: str) -> None:
    """
    使用指定的格式化器

    参数:
        名称: 格式化器名称
    """
    if 名称 not in _log_formatters:
        raise RuntimeError(f"格式化器 '{名称}' 不存在")
    格式化函数 = _log_formatters[名称]

    def _自定义输出(级别: str, 消息: str) -> None:
        级别值 = _LOG_LEVELS.get(级别, 0)
        if 级别值 < _current_level:
            return
        时间_str = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())
        行 = 格式化函数(级别, 时间_str, 消息)
        if _enable_console:
            print(行, flush=True)
        if _output_file is not None:
            _output_file.write(行 + '\n')
            _output_file.flush()

    global _输出
    _输出 = _自定义输出


def 创建简单格式化器(格式字符串: str) -> Callable:
    """
    创建简单格式化器

    参数:
        格式字符串: 格式字符串，支持{级别}、{时间}、{消息}占位符

    返回:
        格式化函数
    """
    def 格式化函数(级别: str, 时间: str, 消息: str) -> str:
        return 格式字符串.format(级别=级别, 时间=时间, 消息=消息)
    return 格式化函数


def 创建带颜色格式化器() -> Callable:
    """
    创建带颜色的格式化器

    返回:
        格式化函数
    """
    颜色映射 = {
        '调试': '\033[36m',
        '信息': '\033[32m',
        '警告': '\033[33m',
        '错误': '\033[31m',
        '致命': '\033[41m',
    }
    重置 = '\033[0m'

    def 格式化函数(级别: str, 时间: str, 消息: str) -> str:
        颜色 = 颜色映射.get(级别, '')
        return f'{颜色}[{级别}] {时间} - {消息}{重置}'
    return 格式化函数


def 创建JSON格式化器() -> Callable:
    """
    创建JSON格式化器

    返回:
        格式化函数
    """
    import json

    def 格式化函数(级别: str, 时间: str, 消息: str) -> str:
        return json.dumps({
            '级别': 级别,
            '时间': 时间,
            '消息': 消息,
        }, ensure_ascii=False)
    return 格式化函数


def 重置格式化器() -> None:
    """重置为默认格式化器"""
    global _输出
    _输出 = _输出


def 获取所有级别() -> list:
    """获取所有可用的日志级别"""
    return list(_LOG_LEVELS.keys())


def 获取格式化器列表() -> list:
    """获取所有已注册的格式化器"""
    return list(_log_formatters.keys())


def 打印日志配置() -> None:
    """打印当前日志配置"""
    配置 = {
        '当前级别': 获取级别(),
        '级别数值': _current_level,
        '输出格式': _format,
        '控制台输出': _enable_console,
        '文件输出': _output_file is not None,
        '格式化器': list(_log_formatters.keys()),
    }
    print(f'日志配置: {配置}')


__all__ = [
    '调试', '信息', '警告', '错误', '致命',
    '设置级别', '获取级别', '设置格式',
    '设置输出文件', '启用控制台输出', '禁用控制台输出',
    '启用文件输出', '禁用文件输出',
    '输出到标准错误', '输出到标准输出',
    '带上下文日志', '调试上下文', '信息上下文',
    '警告上下文', '错误上下文', '致命上下文',
    '日志异常', '调试异常', '信息异常',
    '警告异常', '错误异常', '致命异常',
    '日志函数', '级别数值', '级别名称',
    '日志轮转', '设置日志轮转',
    '添加格式化器', '使用格式化器',
    '创建简单格式化器', '创建带颜色格式化器',
    '创建JSON格式化器', '重置格式化器',
    '获取所有级别', '获取格式化器列表',
    '打印日志配置',
]