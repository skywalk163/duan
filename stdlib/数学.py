"""
段言标准库 - 数学模块

提供数学运算函数：pow, sqrt, sin, cos, tan, random, floor, ceil, round, pi
"""

import math
import random as _random
import statistics as _stats
from typing import Union, List, Optional

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


# =============================================================================
# 统计函数
# =============================================================================

def 平均数(数据: List[Number]) -> float:
    """
    算术平均数

    参数:
        数据: 数字列表

    返回:
        平均数
    """
    return _stats.mean(数据)


def 中位数(数据: List[Number]) -> float:
    """
    中位数

    参数:
        数据: 数字列表

    返回:
        中位数
    """
    return _stats.median(数据)


def 众数(数据: List[Number]) -> Number:
    """
    众数（出现最多的值）

    参数:
        数据: 数字列表

    返回:
        众数
    """
    try:
        return _stats.mode(数据)
    except _stats.StatisticsError:
        raise RuntimeError("众数不存在：所有值出现次数相同")


def 标准差(数据: List[Number]) -> float:
    """
    总体标准差

    参数:
        数据: 数字列表

    返回:
        标准差
    """
    return _stats.pstdev(数据)


def 样本标准差(数据: List[Number]) -> float:
    """
    样本标准差（自由度 n-1）

    参数:
        数据: 样本数据列表

    返回:
        样本标准差
    """
    if len(数据) < 2:
        raise RuntimeError("样本数量不足，至少需要 2 个数据")
    return _stats.stdev(数据)


def 方差(数据: List[Number]) -> float:
    """
    总体方差

    参数:
        数据: 数字列表

    返回:
        方差
    """
    return _stats.pvariance(数据)


def 样本方差(数据: List[Number]) -> float:
    """
    样本方差（自由度 n-1）

    参数:
        数据: 样本数据列表

    返回:
        样本方差
    """
    if len(数据) < 2:
        raise RuntimeError("样本数量不足，至少需要 2 个数据")
    return _stats.variance(数据)


def 范围(数据: List[Number]) -> float:
    """
    范围（最大值 - 最小值）

    参数:
        数据: 数字列表

    返回:
        范围值
    """
    if not 数据:
        raise RuntimeError("数据列表为空")
    return max(数据) - min(数据)


def 求和(数据: List[Number]) -> Number:
    """
    求和

    参数:
        数据: 数字列表

    返回:
        总和
    """
    return sum(数据)


def 累积和(数据: List[Number]) -> List[Number]:
    """
    累积和

    参数:
        数据: 数字列表

    返回:
        累积和列表（每个元素为到该位置为止的和）
    """
    result = []
    total = 0
    for v in 数据:
        total += v
        result.append(total)
    return result


def 线性回归(x数据: List[Number], y数据: List[Number]) -> dict:
    """
    线性回归（斜率、截距、相关系数）

    参数:
        x数据: X 轴数据列表
        y数据: Y 轴数据列表

    返回:
        {'斜率': slope, '截距': intercept, '相关系数': r}
    """
    if len(x数据) != len(y数据):
        raise RuntimeError("X 和 Y 数据长度不匹配")
    if len(x数据) < 2:
        raise RuntimeError("数据点不足，至少需要 2 个点")
    try:
        slope, intercept = _stats.linear_regression(x数据, y数据)
    except _stats.StatisticsError as e:
        raise RuntimeError(f"线性回归失败: {e}")

    # 计算相关系数
    n = len(x数据)
    mx, my = _stats.mean(x数据), _stats.mean(y数据)
    sx, sy = _stats.pstdev(x数据), _stats.pstdev(y数据)
    if sx == 0 or sy == 0:
        r = 1.0
    else:
        r = sum((x数据[i] - mx) * (y数据[i] - my) for i in range(n)) / (n * sx * sy)

    return {
        '斜率': slope,
        '截距': intercept,
        '相关系数': r,
    }


__all__ = [
    '绝对值', '最大值', '最小值',
    '幂', '平方根',
    '正弦', '余弦', '正切',
    '弧度转角度', '角度转弧度',
    '向上取整', '向下取整', '四舍五入',
    '随机整数', '随机浮点', '随机选择',
    '圆周率', '自然常数',
    '阶乘', '对数', '自然对数',

    # 统计函数
    '平均数', '中位数', '众数',
    '标准差', '样本标准差', '方差', '样本方差',
    '范围', '求和', '累积和',
    '线性回归',
]