"""
段言标准库 - 迭代工具模块

提供常用的迭代器工具函数：range、enumerate、zip、map、filter等。
"""

from typing import Any, Callable, Iterable, Iterator, List, Optional, TypeVar, Union


T = TypeVar('T')
U = TypeVar('U')


def 范围(开始: int, 结束: Optional[int] = None, 步长: int = 1) -> List[int]:
    """
    生成整数序列

    参数:
        开始: 起始值（包含）
        结束: 结束值（不包含），为 None 时表示从 0 开始
        步长: 步进值（默认 1）

    返回:
        整数列表
    """
    if 结束 is None:
        结束 = 开始
        开始 = 0
    return list(range(开始, 结束, 步长))


def 枚举(序列: Iterable[T], 起始索引: int = 0) -> List[tuple]:
    """
    返回序列的索引和值对

    参数:
        序列: 可迭代对象
        起始索引: 起始索引（默认 0）

    返回:
        [(0, item0), (1, item1), ...]
    """
    return list(enumerate(序列, 起始索引))


def 压缩(*序列列表: Iterable) -> List[tuple]:
    """
    并行遍历多个序列

    参数:
        序列列表: 多个可迭代对象

    返回:
        [(a0, b0, ...), (a1, b1, ...), ...]
    """
    return [tuple(序列[i] for 序列 in 序列列表)
            for i in range(min(len(s) for s in 序列列表))]


def 映射(函数: Callable[[T], U], 序列: Iterable[T]) -> List[U]:
    """
    对序列每个元素应用函数

    参数:
        函数: 转换函数
        序列: 可迭代对象

    返回:
        转换后的列表
    """
    return [函数(item) for item in 序列]


def 过滤(条件: Callable[[T], bool], 序列: Iterable[T]) -> List[T]:
    """
    过滤序列中满足条件的元素

    参数:
        条件: 过滤函数，返回 True 保留
        序列: 可迭代对象

    返回:
        过滤后的列表
    """
    return [item for item in 序列 if 条件(item)]


def 累积(函数: Callable[[Any, T], Any], 序列: Iterable[T], 初始值: Any = None) -> List[Any]:
    """
    累积计算

    参数:
        函数: 累积函数
        序列: 可迭代对象
        初始值: 初始值

    返回:
        累积结果列表
    """
    from functools import reduce
    if 初始值 is not None:
        return [reduce(函数, 序列[:i+1], 初始值) for i in range(len(序列))]
    return [reduce(函数, 序列[:i+1]) for i in range(len(序列))]


def 展平(嵌套列表: Iterable) -> List[Any]:
    """
    扁平化嵌套列表（一层）

    参数:
        嵌套列表: 嵌套的列表

    返回:
        扁平化后的列表
    """
    结果 = []
    for item in 嵌套列表:
        if isinstance(item, (list, tuple)):
            结果.extend(item)
        else:
            结果.append(item)
    return 结果


def 批量(序列: Iterable[T], 每组大小: int) -> List[List[T]]:
    """
    将序列分成固定大小的组

    参数:
        序列: 可迭代对象
        每组大小: 每组元素数量

    返回:
        分组后的列表
    """
    结果 = []
    当前组 = []
    for item in 序列:
        当前组.append(item)
        if len(当前组) == 每组大小:
            结果.append(当前组)
            当前组 = []
    if 当前组:
        结果.append(当前组)
    return 结果


def 分组(序列: Iterable[T], 大小: int) -> List[List[T]]:
    """
    按固定大小分组（别名）

    参数:
        序列: 可迭代对象
        大小: 每组元素数量

    返回:
        分组后的列表
    """
    return 批量(序列, 大小)


def 全部(序列: Iterable) -> bool:
    """
    检查是否所有元素都为真

    参数:
        序列: 可迭代对象

    返回:
        是否所有元素都为真
    """
    for item in 序列:
        if not item:
            return False
    return True


def 任意(序列: Iterable) -> bool:
    """
    检查是否有任意元素为真

    参数:
        序列: 可迭代对象

    返回:
        是否有任意元素为真
    """
    for item in 序列:
        if item:
            return True
    return False


def 是否为空(序列: Iterable) -> bool:
    """
    检查序列是否为空

    参数:
        序列: 可迭代对象

    返回:
        是否为空
    """
    for _ in 序列:
        return False
    return True


def 第一(序列: Iterable[T], 默认值: T = None) -> T:
    """
    获取序列的第一个元素

    参数:
        序列: 可迭代对象
        默认值: 默认值（序列为空时返回）

    返回:
        第一个元素或默认值
    """
    for item in 序列:
        return item
    return 默认值


def 最后(序列: Iterable[T], 默认值: T = None) -> T:
    """
    获取序列的最后一个元素

    参数:
        序列: 可迭代对象
        默认值: 默认值（序列为空时返回）

    返回:
        最后一个元素或默认值
    """
    结果 = 默认值
    for item in 序列:
        结果 = item
    return 结果


def nth(序列: Iterable[T], 索引: int, 默认值: T = None) -> T:
    """
    获取序列指定索引的元素

    参数:
        序列: 可迭代对象
        索引: 元素索引（从0开始）
        默认值: 默认值（索引超出范围时返回）

    返回:
        指定索引的元素或默认值
    """
    for i, item in enumerate(序列):
        if i == 索引:
            return item
    return 默认值


__all__ = [
    '范围', '枚举', '压缩', '映射', '过滤',
    '累积', '展平', '批量', '分组',
    '全部', '任意', '是否为空',
    '第一', '最后', 'nth',
]
