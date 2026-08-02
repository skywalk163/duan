"""
矩阵运算模块 - 多维数组与向量化计算

提供类似 NumPy 的基础矩阵运算功能，包括：
- 多维数组创建与操作
- 元素级运算
- 矩阵乘法
- 形状操作
- 统计聚合
"""
from typing import List, Tuple, Union, Callable, Any
import math


class 数组:
    """多维数组类"""
    
    def __init__(self, 数据: Union[List, Tuple], 形状: Tuple = None):
        if 形状 is None:
            self._数据 = list(数据)
            self._形状 = self._计算形状(self._数据)
        else:
            self._数据 = self._扁平化(数据)
            self._形状 = 形状
            self._数据 = self._重塑(self._扁平化(数据), 形状)
    
    def _计算形状(self, 数据) -> Tuple:
        """递归计算数组形状"""
        if isinstance(数据, (list, tuple)):
            return (len(数据),) + self._计算形状(数据[0]) if 数据 else ()
        return ()
    
    def _扁平化(self, 数据) -> List:
        """将多维数组扁平化为一维"""
        结果 = []
        if isinstance(数据, (list, tuple)):
            for 元素 in 数据:
                结果.extend(self._扁平化(元素))
        else:
            结果.append(数据)
        return 结果
    
    def _重塑(self, 扁平数据: List, 形状: Tuple) -> List:
        """将扁平数据重塑为指定形状"""
        if len(形状) == 1:
            return list(扁平数据[:形状[0]])
        尺寸 = 形状[0]
        剩余形状 = 形状[1:]
        每个部分大小 = math.prod(剩余形状)
        return [self._重塑(扁平数据[i*每个部分大小:(i+1)*每个部分大小], 剩余形状) 
                for i in range(尺寸)]
    
    def __getitem__(self, 索引: Union[int, Tuple]) -> Any:
        """获取元素"""
        if isinstance(索引, tuple):
            数据 = self._数据
            for i in 索引:
                数据 = 数据[i]
            return 数据
        return self._数据[索引]
    
    def __setitem__(self, 索引: Union[int, Tuple], 值: Any):
        """设置元素"""
        if isinstance(索引, tuple):
            数据 = self._数据
            for i in 索引[:-1]:
                数据 = 数据[i]
            数据[索引[-1]] = 值
        else:
            self._数据[索引] = 值
    
    def __len__(self) -> int:
        return len(self._数据)
    
    def __repr__(self) -> str:
        return f'数组({self._数据}, 形状={self._形状})'
    
    def __add__(self, 其他: Union['数组', int, float]) -> '数组':
        return self._逐元素运算(其他, lambda a, b: a + b)
    
    def __sub__(self, 其他: Union['数组', int, float]) -> '数组':
        return self._逐元素运算(其他, lambda a, b: a - b)
    
    def __mul__(self, 其他: Union['数组', int, float]) -> '数组':
        return self._逐元素运算(其他, lambda a, b: a * b)
    
    def __truediv__(self, 其他: Union['数组', int, float]) -> '数组':
        return self._逐元素运算(其他, lambda a, b: a / b)
    
    def __pow__(self, 其他: Union['数组', int, float]) -> '数组':
        return self._逐元素运算(其他, lambda a, b: a ** b)
    
    def __neg__(self) -> '数组':
        return self._逐元素运算(0, lambda a, b: -a)
    
    def _逐元素运算(self, 其他, 运算: Callable) -> '数组':
        """逐元素运算"""
        扁平数据 = self._扁平化(self._数据)
        if isinstance(其他, 数组):
            if self._形状 != 其他._形状:
                raise ValueError(f'形状不匹配: {self._形状} vs {其他._形状}')
            其他扁平 = 其他._扁平化(其他._数据)
            结果 = [运算(a, b) for a, b in zip(扁平数据, 其他扁平)]
        else:
            结果 = [运算(a, 其他) for a in 扁平数据]
        return 数组(结果, self._形状)
    
    def 形状(self) -> Tuple:
        """返回数组形状"""
        return self._形状
    
    def 维度(self) -> int:
        """返回数组维度"""
        return len(self._形状)
    
    def 大小(self) -> int:
        """返回数组元素总数"""
        return math.prod(self._形状)
    
    def 重塑(self, 新形状: Tuple) -> '数组':
        """重塑数组形状"""
        if math.prod(新形状) != self.大小():
            raise ValueError(f'无法重塑: {self._形状} -> {新形状}')
        return 数组(self._扁平化(self._数据), 新形状)
    
    def 转置(self) -> '数组':
        """矩阵转置（仅支持二维）"""
        if self.维度() != 2:
            raise ValueError('转置仅支持二维数组')
        行数, 列数 = self._形状
        结果 = [[0 for _ in range(行数)] for _ in range(列数)]
        for i in range(行数):
            for j in range(列数):
                结果[j][i] = self[i, j]
        return 数组(结果)
    
    def 扁平化(self) -> List:
        """返回扁平化列表"""
        return self._扁平化(self._数据)
    
    def 求和(self, 轴: int = None) -> Union['数组', float, int]:
        """求和"""
        if 轴 is None:
            return sum(self._扁平化(self._数据))
        return self._沿轴运算(轴, sum)
    
    def 均值(self, 轴: int = None) -> Union['数组', float]:
        """均值"""
        if 轴 is None:
            return sum(self._扁平化(self._数据)) / self.大小()
        return self._沿轴运算(轴, lambda x: sum(x) / len(x))
    
    def 最大值(self, 轴: int = None) -> Union['数组', float, int]:
        """最大值"""
        if 轴 is None:
            return max(self._扁平化(self._数据))
        return self._沿轴运算(轴, max)
    
    def 最小值(self, 轴: int = None) -> Union['数组', float, int]:
        """最小值"""
        if 轴 is None:
            return min(self._扁平化(self._数据))
        return self._沿轴运算(轴, min)
    
    def _沿轴运算(self, 轴: int, 运算: Callable) -> '数组':
        """沿指定轴进行运算"""
        if 轴 < 0:
            轴 += self.维度()
        if 轴 >= self.维度():
            raise ValueError(f'轴索引超出范围: {轴}')
        
        def 递归处理(数据, 当前轴: int) -> List:
            if 当前轴 == 轴:
                return 运算(self._扁平化数据) if isinstance(数据[0], (list, tuple)) else 运算(数据)
            return [递归处理(子数据, 当前轴 + 1) for 子数据 in 数据]
        
        结果 = 递归处理(self._数据, 0)
        return 数组(结果)


def 创建数组(数据: Union[List, Tuple], 形状: Tuple = None) -> 数组:
    """创建数组"""
    return 数组(数据, 形状)


def 全零(形状: Tuple) -> 数组:
    """创建全零数组"""
    大小 = math.prod(形状)
    return 数组([0] * 大小, 形状)


def 全一(形状: Tuple) -> 数组:
    """创建全一数组"""
    大小 = math.prod(形状)
    return 数组([1] * 大小, 形状)


def 随机数组(形状: Tuple, 最小值: float = 0, 最大值: float = 1) -> 数组:
    """创建随机数组"""
    import random
    大小 = math.prod(形状)
    return 数组([random.uniform(最小值, 最大值) for _ in range(大小)], 形状)


def 范围数组(开始: int = 0, 结束: int = None, 步长: int = 1) -> 数组:
    """创建范围数组"""
    if 结束 is None:
        开始, 结束 = 0, 开始
    return 数组(list(range(开始, 结束, 步长)))


def 矩阵乘法(a: 数组, b: 数组) -> 数组:
    """矩阵乘法"""
    if a.维度() != 2 or b.维度() != 2:
        raise ValueError('矩阵乘法仅支持二维数组')
    a_rows, a_cols = a.形状()
    b_rows, b_cols = b.形状()
    if a_cols != b_rows:
        raise ValueError(f'矩阵维度不匹配: {a_cols} != {b_rows}')
    
    结果 = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    for i in range(a_rows):
        for j in range(b_cols):
            for k in range(a_cols):
                结果[i][j] += a[i, k] * b[k, j]
    return 数组(结果)


def 点积(a: 数组, b: 数组) -> float:
    """向量点积"""
    if a.维度() != 1 or b.维度() != 1:
        raise ValueError('点积仅支持一维数组')
    if a.大小() != b.大小():
        raise ValueError(f'向量长度不匹配: {a.大小()} != {b.大小()}')
    return sum(x * y for x, y in zip(a.扁平化(), b.扁平化()))


def 外积(a: 数组, b: 数组) -> 数组:
    """向量外积"""
    if a.维度() != 1 or b.维度() != 1:
        raise ValueError('外积仅支持一维数组')
    a_len = a.大小()
    b_len = b.大小()
    结果 = [[0 for _ in range(b_len)] for _ in range(a_len)]
    for i in range(a_len):
        for j in range(b_len):
            结果[i][j] = a[i] * b[j]
    return 数组(结果)


def 连接(数组列表: List[数组], 轴: int = 0) -> 数组:
    """连接多个数组"""
    if not 数组列表:
        raise ValueError('数组列表不能为空')
    
    第一个 = 数组列表[0]
    形状 = list(第一个.形状())
    
    for arr in 数组列表[1:]:
        if arr.维度() != 第一个.维度():
            raise ValueError('所有数组必须具有相同维度')
        for i in range(第一个.维度()):
            if i != 轴 and arr.形状()[i] != 形状[i]:
                raise ValueError(f'非轴维度必须相同')
    
    形状[轴] = sum(arr.形状()[轴] for arr in 数组列表)
    
    def 递归连接(数组列表, 当前轴: int):
        if 当前轴 == 轴:
            结果 = []
            for arr in 数组列表:
                结果.extend(arr._数据)
            return 结果
        else:
            子数组列表 = []
            for i in range(len(数组列表[0]._数据)):
                子数组列表.append([arr._数据[i] for arr in 数组列表])
            return [递归连接(sl, 当前轴 + 1) for sl in 子数组列表]
    
    return 数组(递归连接(数组列表, 0))


def 切片(数组: 数组, 起始: int = None, 结束: int = None, 步长: int = None) -> 数组:
    """切片一维数组"""
    if 数组.维度() != 1:
        raise ValueError('切片仅支持一维数组')
    数据 = 数组.扁平化()
    return 数组(数据[起始:结束:步长])