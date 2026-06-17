"""
段言标准库 - JSON 处理模块

提供 JSON 的解析、序列化等功能。
"""

import json
from typing import Any, Optional


def 解析JSON(text: str) -> Any:
    """
    解析 JSON 字符串为段言值（列表/字典/字符串/数字/布尔/空）
    
    参数:
        text: JSON 格式字符串
    
    返回:
        解析后的值
    
    示例:
        解析JSON('{"name": "段言", "version": 1}')  # {'name': '段言', 'version': 1}
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON 解析失败: {e}")


def 序列化JSON(value: Any, 缩进: Optional[int] = None) -> str:
    """
    将段言值序列化为 JSON 字符串
    
    参数:
        value: 要序列化的值（列表、字典、字符串、数字、布尔、空）
        缩进: 缩进空格数，None 为紧凑输出
    
    返回:
        JSON 格式字符串
    
    示例:
        序列化JSON({'name': '段言'})       # '{"name": "段言"}'
        序列化JSON({'name': '段言'}, 2)    # 格式化输出
    """
    try:
        if 缩进 is not None:
            return json.dumps(value, ensure_ascii=False, indent=缩进)
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise RuntimeError(f"JSON 序列化失败: {e}")


def 美化JSON(value: Any) -> str:
    """
    美化 JSON 输出（带缩进）
    
    参数:
        value: 要格式化的值
    
    返回:
        美化后的 JSON 字符串
    """
    return 序列化JSON(value, 缩进=2)


def 读取JSON文件(path: str) -> Any:
    """
    从文件读取并解析 JSON
    
    参数:
        path: 文件路径
    
    返回:
        解析后的值
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"文件不存在: '{path}'")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON 文件解析失败 '{path}': {e}")


def 写入JSON文件(path: str, value: Any, 美化: bool = False) -> None:
    """
    将值序列化为 JSON 写入文件
    
    参数:
        path: 文件路径
        value: 要序列化的值
        美化: 是否格式化输出
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, indent=2 if 美化 else None)
    except Exception as e:
        raise RuntimeError(f"写入 JSON 文件失败 '{path}': {e}")


__all__ = [
    '解析JSON', '序列化JSON', '美化JSON',
    '读取JSON文件', '写入JSON文件',
]