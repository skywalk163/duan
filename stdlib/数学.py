"""
段言标准库 - 数学模块

提供数学运算函数：pow, sqrt, sin, cos, tan, random, floor, ceil, round, pi
"""

import math
import random as _random
from typing import Union, List

Number = Union[int, float]


def 绝对值(x: Number) -> Number:
    """绝对值"""
    return abs(x)


def 最大值(甲: Number, 乙: Number) -> Number:
    """最大值"""
    return max(甲, 乙)


def 最小值(甲: Number, 乙: Number) -> Number:
    """最小值"""
    return min(甲, 乙)


def 幂(底数: Number, 指数: Number) -> float:
    """幂运算：底数 ^ 指数"""
    return pow(底数, 指数)


def 平方根(x: Number) -> float:
    """平方根"""
    if x < 0:
        raise RuntimeError(f"不能对负数求平方根: {x}")
    return math.sqrt(x)


def 正弦(x: Number) -> float:
    """正弦（弧度）"""
    return math.sin(x)


def 余弦(x: Number) -> float:
    """余弦（弧度）"""
    return math.cos(x)


def 正切(x: Number) -> float:
    """正切（弧度）"""
    return math.tan(x)


def 弧度转角度(弧度: Number) -> float:
    """弧度转角度"""
    return math.degrees(弧度)


def 角度转弧度(角度: Number) -> float:
    """角度转弧度"""
    return math.radians(角度)


def 向上取整(x: Number) -> int:
    """向上取整"""
    return math.ceil(x)


def 向下取整(x: Number) -> int:
    """向下取整"""
    return math.floor(x)


def 四舍五入(x: Number, 小数位数: int = 0) -> float:
    """四舍五入"""
    return round(x, 小数位数)


def 随机整数(最小值: int, 最大值: int) -> int:
    """随机整数 [最小值, 最大值]"""
    return _random.randint(最小值, 最大值)


def 随机浮点() -> float:
    """随机浮点数 [0.0, 1.0)"""
    return _random.random()


def 随机选择(列表: List) -> object:
    """从列表中随机选择一个元素"""
    return _random.choice(列表)


def 圆周率() -> float:
    """圆周率 π"""
    return math.pi


def 自然常数() -> float:
    """自然常数 e"""
    return math.e


def 阶乘(n: int) -> int:
    """阶乘 n!"""
    if n < 0:
        raise RuntimeError(f"不能对负数求阶乘: {n}")
    return math.factorial(n)


def 对数(x: Number, 底数: Number = math.e) -> float:
    """对数：log_底数(x)"""
    return math.log(x, 底数)


def 自然对数(x: Number) -> float:
    """自然对数 ln(x)"""
    if x <= 0:
        raise RuntimeError(f"不能对非正数求自然对数: {x}")
    return math.log(x)


__all__ = [
    '绝对值', '最大值', '最小值',
    '幂', '平方根',
    '正弦', '余弦', '正切',
    '弧度转角度', '角度转弧度',
    '向上取整', '向下取整', '四舍五入',
    '随机整数', '随机浮点', '随机选择',
    '圆周率', '自然常数',
    '阶乘', '对数', '自然对数',
]