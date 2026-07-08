"""
统计函数模块 - 均值、方差、相关系数

提供基础统计分析功能，包括：
- 描述性统计：均值、中位数、众数
- 离散度统计：方差、标准差、极差
- 相关性分析：皮尔逊相关系数、协方差
- 分布检验：偏度、峰度
"""
import math
from typing import Any
from typing import List, Tuple, Union


def 均值(数据: List[Union[int, float]]) -> float:
    """计算均值"""
    if not 数据:
        raise ValueError('数据不能为空')
    return sum(数据) / len(数据)


def 中位数(数据: List[Union[int, float]]) -> float:
    """计算中位数"""
    if not 数据:
        raise ValueError('数据不能为空')
    排序数据 = sorted(数据)
    n = len(排序数据)
    if n % 2 == 0:
        return (排序数据[n//2 - 1] + 排序数据[n//2]) / 2
    return 排序数据[n//2]


def 众数(数据: List[Union[int, float]]) -> List[Union[int, float]]:
    """计算众数（可能有多个）"""
    if not 数据:
        raise ValueError('数据不能为空')
    频率 = {}
    for 值 in 数据:
        频率[值] = 频率.get(值, 0) + 1
    最大频率 = max(频率.values())
    return [值 for 值, 次数 in 频率.items() if 次数 == 最大频率]


def 求和(数据: List[Union[int, float]]) -> float:
    """求和"""
    return sum(数据)


def 最小值(数据: List[Union[int, float]]) -> Union[int, float]:
    """求最小值"""
    if not 数据:
        raise ValueError('数据不能为空')
    return min(数据)


def 最大值(数据: List[Union[int, float]]) -> Union[int, float]:
    """求最大值"""
    if not 数据:
        raise ValueError('数据不能为空')
    return max(数据)


def 极差(数据: List[Union[int, float]]) -> float:
    """计算极差（最大值 - 最小值）"""
    if not 数据:
        raise ValueError('数据不能为空')
    return max(数据) - min(数据)


def 方差(数据: List[Union[int, float]], 总体: bool = True) -> float:
    """计算方差"""
    if not 数据:
        raise ValueError('数据不能为空')
    n = len(数据)
    if n == 1:
        return 0.0
    均值 = sum(数据) / n
    平方差之和 = sum((x - 均值) ** 2 for x in 数据)
    if 总体:
        return 平方差之和 / n
    return 平方差之和 / (n - 1)


def 标准差(数据: List[Union[int, float]], 总体: bool = True) -> float:
    """计算标准差"""
    return math.sqrt(方差(数据, 总体))


def 标准差系数(数据: List[Union[int, float]], 总体: bool = True) -> float:
    """计算标准差系数（变异系数）"""
    均值 = sum(数据) / len(数据)
    if 均值 == 0:
        return 0.0
    return 标准差(数据, 总体) / 均值


def 协方差(数据1: List[Union[int, float]], 数据2: List[Union[int, float]]) -> float:
    """计算协方差"""
    if len(数据1) != len(数据2):
        raise ValueError('数据长度必须相同')
    n = len(数据1)
    if n == 0:
        raise ValueError('数据不能为空')
    
    均值1 = sum(数据1) / n
    均值2 = sum(数据2) / n
    
    return sum((数据1[i] - 均值1) * (数据2[i] - 均值2) for i in range(n)) / n


def 皮尔逊相关系数(数据1: List[Union[int, float]], 数据2: List[Union[int, float]]) -> float:
    """计算皮尔逊相关系数"""
    if len(数据1) != len(数据2):
        raise ValueError('数据长度必须相同')
    n = len(数据1)
    if n == 0:
        raise ValueError('数据不能为空')
    
    均值1 = sum(数据1) / n
    均值2 = sum(数据2) / n
    
    协方差 = sum((数据1[i] - 均值1) * (数据2[i] - 均值2) for i in range(n)) / n
    标准差1 = math.sqrt(sum((x - 均值1) ** 2 for x in 数据1) / n)
    标准差2 = math.sqrt(sum((x - 均值2) ** 2 for x in 数据2) / n)
    
    if 标准差1 == 0 or 标准差2 == 0:
        return 0.0
    
    return 协方差 / (标准差1 * 标准差2)


def 偏度(数据: List[Union[int, float]]) -> float:
    """计算偏度"""
    if len(数据) < 3:
        raise ValueError('数据至少需要3个元素')
    n = len(数据)
    均值 = sum(数据) / n
    标准差 = math.sqrt(sum((x - 均值) ** 2 for x in 数据) / n)
    
    if 标准差 == 0:
        return 0.0
    
    三阶矩 = sum((x - 均值) ** 3 for x in 数据) / n
    return 三阶矩 / (标准差 ** 3)


def 峰度(数据: List[Union[int, float]]) -> float:
    """计算峰度"""
    if len(数据) < 4:
        raise ValueError('数据至少需要4个元素')
    n = len(数据)
    均值 = sum(数据) / n
    标准差 = math.sqrt(sum((x - 均值) ** 2 for x in 数据) / n)
    
    if 标准差 == 0:
        return 0.0
    
    四阶矩 = sum((x - 均值) ** 4 for x in 数据) / n
    return 四阶矩 / (标准差 ** 4) - 3


def 分位数(数据: List[Union[int, float]], 分位: float = 0.5) -> float:
    """计算分位数"""
    if not 数据:
        raise ValueError('数据不能为空')
    if 分位 < 0 or 分位 > 1:
        raise ValueError('分位值必须在0到1之间')
    
    排序数据 = sorted(数据)
    n = len(排序数据)
    位置 = (n - 1) * 分位
    整数部分 = int(位置)
    小数部分 = 位置 - 整数部分
    
    if 整数部分 >= n - 1:
        return 排序数据[-1]
    
    return 排序数据[整数部分] * (1 - 小数部分) + 排序数据[整数部分 + 1] * 小数部分


def 四分位数(数据: List[Union[int, float]]) -> Tuple[float, float, float]:
    """计算四分位数 (Q1, Q2, Q3)"""
    return 分位数(数据, 0.25), 分位数(数据, 0.5), 分位数(数据, 0.75)


def 四分位距(数据: List[Union[int, float]]) -> float:
    """计算四分位距 (IQR)"""
    q1, _, q3 = 四分位数(数据)
    return q3 - q1


def 箱线图数据(数据: List[Union[int, float]]) -> Tuple[float, float, float, float, float]:
    """计算箱线图数据 (最小值, Q1, 中位数, Q3, 最大值)"""
    q1, 中位数, q3 = 四分位数(数据)
    return min(数据), q1, 中位数, q3, max(数据)


def 几何均值(数据: List[Union[int, float]]) -> float:
    """计算几何均值"""
    if not 数据:
        raise ValueError('数据不能为空')
    乘积 = 1.0
    for 值 in 数据:
        if 值 <= 0:
            raise ValueError('几何均值要求所有数据必须大于0')
        乘积 *= 值
    return 乘积 ** (1.0 / len(数据))


def 调和均值(数据: List[Union[int, float]]) -> float:
    """计算调和均值"""
    if not 数据:
        raise ValueError('数据不能为空')
    倒数之和 = sum(1.0 / x for x in 数据)
    if 倒数之和 == 0:
        return 0.0
    return len(数据) / 倒数之和


def 加权均值(数据: List[Union[int, float]], 权重: List[float]) -> float:
    """计算加权均值"""
    if len(数据) != len(权重):
        raise ValueError('数据和权重长度必须相同')
    总权重 = sum(权重)
    if 总权重 == 0:
        raise ValueError('权重总和不能为0')
    return sum(数据[i] * 权重[i] for i in range(len(数据))) / 总权重


def 变异系数(数据: List[Union[int, float]]) -> float:
    """计算变异系数（标准差/均值）"""
    均值 = sum(数据) / len(数据)
    if 均值 == 0:
        return 0.0
    return 标准差(数据) / 均值


def 数据范围(数据: List[Union[int, float]]) -> Tuple[Union[int, float], Union[int, float]]:
    """返回数据范围（最小值, 最大值）"""
    if not 数据:
        raise ValueError('数据不能为空')
    return min(数据), max(数据)


def 计数(数据: List[Any]) -> int:
    """计数"""
    return len(数据)


def 唯一值数量(数据: List[Any]) -> int:
    """唯一值数量"""
    return len(set(数据))


def 频率表(数据: List[Any]) -> dict:
    """生成频率表"""
    频率 = {}
    for 值 in 数据:
        频率[值] = 频率.get(值, 0) + 1
    return 频率


def 累计频率(数据: List[Union[int, float]]) -> List[float]:
    """计算累计频率"""
    排序数据 = sorted(数据)
    n = len(排序数据)
    return [(i + 1) / n for i in range(n)]


def 归一化(数据: List[Union[int, float]], 方法: str = 'minmax') -> List[float]:
    """数据归一化"""
    if not 数据:
        raise ValueError('数据不能为空')
    
    if 方法 == 'minmax':
        最小值 = min(数据)
        最大值 = max(数据)
        范围 = 最大值 - 最小值
        if 范围 == 0:
            return [0.0] * len(数据)
        return [(x - 最小值) / 范围 for x in 数据]
    
    elif 方法 == 'zscore':
        均值 = sum(数据) / len(数据)
        标准差 = math.sqrt(sum((x - 均值) ** 2 for x in 数据) / len(数据))
        if 标准差 == 0:
            return [0.0] * len(数据)
        return [(x - 均值) / 标准差 for x in 数据]
    
    else:
        raise ValueError(f'未知方法: {方法}')