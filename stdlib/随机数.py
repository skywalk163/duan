"""
随机数模块 - 各种分布与种子管理

提供丰富的随机数生成功能，包括：
- 基础随机数生成
- 均匀分布、正态分布、泊松分布等
- 随机采样与洗牌
- 种子管理
"""
import random
import math
import time
from typing import List, Tuple, Any


_全局种子 = None


def 设置种子(种子: int = None):
    """设置随机种子"""
    global _全局种子
    _全局种子 = 种子 if 种子 is not None else int(time.time())
    random.seed(_全局种子)


def 获取种子() -> int:
    """获取当前种子"""
    return _全局种子


def 随机() -> float:
    """返回 [0.0, 1.0) 之间的随机浮点数"""
    return random.random()


def 随机整数(最小: int = 0, 最大: int = 100) -> int:
    """返回 [最小, 最大] 之间的随机整数"""
    return random.randint(最小, 最大)


def 随机范围(开始: int = 0, 结束: int = None, 步长: int = 1) -> int:
    """返回指定范围内的随机整数"""
    if 结束 is None:
        开始, 结束 = 0, 开始
    return random.randrange(开始, 结束, 步长)


def 随机浮点数(最小: float = 0.0, 最大: float = 1.0) -> float:
    """返回 [最小, 最大) 之间的随机浮点数"""
    return random.uniform(最小, 最大)


def 均匀分布(最小: float = 0.0, 最大: float = 1.0) -> float:
    """均匀分布"""
    return random.uniform(最小, 最大)


def 正态分布(均值: float = 0.0, 标准差: float = 1.0) -> float:
    """正态分布（高斯分布）"""
    return random.gauss(均值, 标准差)


def 对数正态分布(均值: float = 0.0, 标准差: float = 1.0) -> float:
    """对数正态分布"""
    return random.lognormvariate(均值, 标准差)


def 指数分布(均值: float = 1.0) -> float:
    """指数分布"""
    return random.expovariate(1.0 / 均值)


def 泊松分布(均值: float = 1.0) -> int:
    """泊松分布"""
    return random.poissonvariate(均值)


def 二项分布(试验次数: int = 10, 成功概率: float = 0.5) -> int:
    """二项分布"""
    return random.binomial(试验次数, 成功概率)


def 伽马分布(形状: float = 1.0, 尺度: float = 1.0) -> float:
    """伽马分布"""
    return random.gammavariate(形状, 尺度)


def 贝塔分布(阿尔法: float = 1.0, 贝塔: float = 1.0) -> float:
    """贝塔分布"""
    return random.betavariate(阿尔法, 贝塔)


def 威布尔分布(阿尔法: float = 1.0, 贝塔: float = 1.0) -> float:
    """威布尔分布"""
    return random.weibullvariate(阿尔法, 贝塔)


def 三角分布(低: float = 0.0, 高: float = 1.0, 众数: float = 0.5) -> float:
    """三角分布"""
    return random.triangular(低, 高, 众数)


def 随机选择(序列: List[Any]) -> Any:
    """从序列中随机选择一个元素"""
    return random.choice(序列)


def 随机选择多个(序列: List[Any], 数量: int = 1, 可重复: bool = False) -> List[Any]:
    """从序列中随机选择多个元素"""
    if 可重复:
        return [random.choice(序列) for _ in range(数量)]
    return random.sample(序列, 数量)


def 随机洗牌(序列: List[Any]) -> List[Any]:
    """随机打乱序列"""
    结果 = list(序列)
    random.shuffle(结果)
    return 结果


def 随机权重选择(序列: List[Any], 权重: List[float]) -> Any:
    """按权重随机选择"""
    return random.choices(序列, weights=权重, k=1)[0]


def 随机权重选择多个(序列: List[Any], 权重: List[float], 数量: int = 1) -> List[Any]:
    """按权重随机选择多个"""
    return random.choices(序列, weights=权重, k=数量)


def 随机布尔() -> bool:
    """返回随机布尔值"""
    return random.choice([True, False])


def 随机字符(字符集: str = 'abcdefghijklmnopqrstuvwxyz') -> str:
    """返回随机字符"""
    return random.choice(字符集)


def 随机字符串(长度: int = 10, 字符集: str = 'abcdefghijklmnopqrstuvwxyz0123456789') -> str:
    """返回随机字符串"""
    return ''.join(random.choice(字符集) for _ in range(长度))


def 随机颜色() -> Tuple[int, int, int]:
    """返回随机RGB颜色"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def 随机颜色十六进制() -> str:
    """返回随机十六进制颜色"""
    return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def 随机日期(开始年份: int = 1970, 结束年份: int = 2030) -> Tuple[int, int, int]:
    """返回随机日期 (年, 月, 日)"""
    年 = random.randint(开始年份, 结束年份)
    月 = random.randint(1, 12)
    
    if 月 in [4, 6, 9, 11]:
        最大日 = 30
    elif 月 == 2:
        if (年 % 4 == 0 and 年 % 100 != 0) or 年 % 400 == 0:
            最大日 = 29
        else:
            最大日 = 28
    else:
        最大日 = 31
    
    日 = random.randint(1, 最大日)
    return (年, 月, 日)


def 生成随机序列(长度: int, 分布: str = 'uniform', **参数) -> List[float]:
    """生成指定分布的随机序列"""
    分布函数 = {
        'uniform': 均匀分布,
        'normal': 正态分布,
        'exponential': 指数分布,
        'poisson': 泊松分布,
        'binomial': 二项分布,
        'gamma': 伽马分布,
        'beta': 贝塔分布,
        'weibull': 威布尔分布,
        'triangular': 三角分布,
        'lognormal': 对数正态分布,
    }
    
    if 分布 not in 分布函数:
        raise ValueError(f'未知分布: {分布}')
    
    return [分布函数[分布](**参数) for _ in range(长度)]


def 随机排列(n: int) -> List[int]:
    """返回 0 到 n-1 的随机排列"""
    return random.sample(range(n), n)