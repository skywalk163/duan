"""
段言标准库 - 缓存模块

提供基础缓存、LRU 缓存和记忆化装饰器等功能。
"""

from collections import OrderedDict
from typing import Any, Callable, Dict, Optional


def 创建缓存() -> dict:
    """
    创建新的缓存字典
    
    返回:
        空的缓存字典
    """
    return {}


def 设置缓存(缓存: dict, 键, 值) -> None:
    """
    设置缓存项
    
    参数:
        缓存: 缓存字典
        键: 缓存键
        值: 缓存值
    """
    缓存[键] = 值


def 获取缓存(缓存: dict, 键, 默认值: Any = None) -> Any:
    """
    获取缓存项
    
    参数:
        缓存: 缓存字典
        键: 缓存键
        默认值: 未找到时的默认值（默认 None）
    
    返回:
        缓存值或默认值
    """
    return 缓存.get(键, 默认值)


def 清除缓存(缓存: dict) -> None:
    """
    清空缓存
    
    参数:
        缓存: 缓存字典
    """
    缓存.clear()


class LRU缓存:
    """
    LRU（最近最少使用）缓存类
    
    使用 OrderedDict 实现，当缓存满时自动淘汰最久未使用的项。
    """
    
    def __init__(self, 最大容量: int = 128):
        """
        初始化 LRU 缓存
        
        参数:
            最大容量: 缓存最大容量（默认 128）
        """
        self._最大容量 = 最大容量
        self._缓存: OrderedDict = OrderedDict()
    
    def get(self, 键, 默认值: Any = None) -> Any:
        """
        获取缓存项
        
        参数:
            键: 缓存键
            默认值: 未找到时的默认值（默认 None）
        
        返回:
            缓存值或默认值
        """
        if 键 not in self._缓存:
            return 默认值
        self._缓存.move_to_end(键)
        return self._缓存[键]
    
    def put(self, 键, 值) -> None:
        """
        设置缓存项
        
        参数:
            键: 缓存键
            值: 缓存值
        """
        if 键 in self._缓存:
            self._缓存.move_to_end(键)
        self._缓存[键] = 值
        if len(self._缓存) > self._最大容量:
            self._缓存.popitem(last=False)
    
    def clear(self) -> None:
        """
        清空缓存
        """
        self._缓存.clear()
    
    def __len__(self) -> int:
        return len(self._缓存)


def 记忆化(函数: Callable) -> Callable:
    """
    记忆化装饰器
    
    为函数添加缓存，相同参数的后续调用直接返回缓存结果。
    
    参数:
        函数: 需要记忆化的函数
    
    返回:
        包装后的函数
    """
    缓存: Dict[tuple, Any] = {}
    
    def 包装(*args, **kwargs):
        键 = (args, tuple(sorted(kwargs.items())))
        if 键 not in 缓存:
            缓存[键] = 函数(*args, **kwargs)
        return 缓存[键]
    
    包装._缓存 = 缓存
    包装._原函数 = 函数
    return 包装


__all__ = [
    '创建缓存', '设置缓存', '获取缓存', '清除缓存',
    'LRU缓存', '记忆化',
]
