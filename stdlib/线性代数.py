"""
线性代数模块 - 矩阵分解、求解方程组

提供线性代数基础功能，包括：
- 矩阵运算：行列式、逆矩阵、转置
- 线性方程组求解：高斯消元法
- 矩阵分解：LU分解、QR分解、特征值分解
- 向量运算：范数、正交化
"""
import math
from typing import List, Tuple, Union


def 行列式(矩阵: List[List[float]]) -> float:
    """计算方阵的行列式"""
    n = len(矩阵)
    if n == 0:
        return 1.0
    if n == 1:
        return 矩阵[0][0]
    if n == 2:
        return 矩阵[0][0] * 矩阵[1][1] - 矩阵[0][1] * 矩阵[1][0]
    
    结果 = 0.0
    for j in range(n):
        符号 = (-1) ** j
        子矩阵 = []
        for i in range(1, n):
            子行 = []
            for k in range(n):
                if k != j:
                    子行.append(矩阵[i][k])
            子矩阵.append(子行)
        结果 += 符号 * 矩阵[0][j] * 行列式(子矩阵)
    
    return 结果


def 转置(矩阵: List[List[float]]) -> List[List[float]]:
    """矩阵转置"""
    行数 = len(矩阵)
    列数 = len(矩阵[0]) if 矩阵 else 0
    return [[矩阵[i][j] for i in range(行数)] for j in range(列数)]


def 矩阵乘法(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """矩阵乘法"""
    a_rows = len(a)
    a_cols = len(a[0]) if a else 0
    b_rows = len(b)
    b_cols = len(b[0]) if b else 0
    
    if a_cols != b_rows:
        raise ValueError(f'矩阵维度不匹配: {a_cols} != {b_rows}')
    
    结果 = [[0.0 for _ in range(b_cols)] for _ in range(a_rows)]
    for i in range(a_rows):
        for j in range(b_cols):
            for k in range(a_cols):
                结果[i][j] += a[i][k] * b[k][j]
    return 结果


def 矩阵加法(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """矩阵加法"""
    if len(a) != len(b) or (a and b and len(a[0]) != len(b[0])):
        raise ValueError('矩阵形状必须相同')
    
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def 矩阵减法(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """矩阵减法"""
    if len(a) != len(b) or (a and b and len(a[0]) != len(b[0])):
        raise ValueError('矩阵形状必须相同')
    
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def 标量乘法(矩阵: List[List[float]], 标量: float) -> List[List[float]]:
    """标量乘法"""
    return [[矩阵[i][j] * 标量 for j in range(len(矩阵[0]))] for i in range(len(矩阵))]


def 单位矩阵(n: int) -> List[List[float]]:
    """创建单位矩阵"""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def 零矩阵(行数: int, 列数: int) -> List[List[float]]:
    """创建零矩阵"""
    return [[0.0 for _ in range(列数)] for _ in range(行数)]


def 逆矩阵(矩阵: List[List[float]]) -> List[List[float]]:
    """计算逆矩阵（高斯-约当消元法）"""
    n = len(矩阵)
    if n == 0:
        raise ValueError('矩阵不能为空')
    if any(len(row) != n for row in 矩阵):
        raise ValueError('必须是方阵')
    
    增广矩阵 = []
    for i in range(n):
        行 = list(矩阵[i]) + [1.0 if j == i else 0.0 for j in range(n)]
        增广矩阵.append(行)
    
    for 主元列 in range(n):
        最大值 = abs(增广矩阵[主元列][主元列])
        主元行 = 主元列
        for i in range(主元列 + 1, n):
            if abs(增广矩阵[i][主元列]) > 最大值:
                最大值 = abs(增广矩阵[i][主元列])
                主元行 = i
        
        增广矩阵[主元列], 增广矩阵[主元行] = 增广矩阵[主元行], 增广矩阵[主元列]
        
        主元值 = 增广矩阵[主元列][主元列]
        if abs(主元值) < 1e-10:
            raise ValueError('矩阵不可逆')
        
        for j in range(2 * n):
            增广矩阵[主元列][j] /= 主元值
        
        for i in range(n):
            if i != 主元列:
                因子 = 增广矩阵[i][主元列]
                for j in range(2 * n):
                    增广矩阵[i][j] -= 因子 * 增广矩阵[主元列][j]
    
    逆矩阵 = [row[n:] for row in 增广矩阵]
    return 逆矩阵


def 高斯消元(系数矩阵: List[List[float]], 常数向量: List[float]) -> List[float]:
    """高斯消元法求解线性方程组 Ax = b"""
    n = len(系数矩阵)
    if len(常数向量) != n:
        raise ValueError('系数矩阵和常数向量长度不匹配')
    
    增广矩阵 = []
    for i in range(n):
        行 = list(系数矩阵[i]) + [常数向量[i]]
        增广矩阵.append(行)
    
    for 主元列 in range(n):
        最大值 = abs(增广矩阵[主元列][主元列])
        主元行 = 主元列
        for i in range(主元列 + 1, n):
            if abs(增广矩阵[i][主元列]) > 最大值:
                最大值 = abs(增广矩阵[i][主元列])
                主元行 = i
        
        增广矩阵[主元列], 增广矩阵[主元行] = 增广矩阵[主元行], 增广矩阵[主元列]
        
        主元值 = 增广矩阵[主元列][主元列]
        if abs(主元值) < 1e-10:
            raise ValueError('系数矩阵奇异，无法求解')
        
        for i in range(主元列 + 1, n):
            因子 = 增广矩阵[i][主元列] / 主元值
            for j in range(主元列, n + 1):
                增广矩阵[i][j] -= 因子 * 增广矩阵[主元列][j]
    
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = 增广矩阵[i][n]
        for j in range(i + 1, n):
            x[i] -= 增广矩阵[i][j] * x[j]
        x[i] /= 增广矩阵[i][i]
    
    return x


def 求解线性方程组(系数矩阵: List[List[float]], 常数向量: List[float]) -> List[float]:
    """求解线性方程组（封装高斯消元）"""
    return 高斯消元(系数矩阵, 常数向量)


def LU分解(矩阵: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """LU分解"""
    n = len(矩阵)
    L = 零矩阵(n, n)
    U = [list(row) for row in 矩阵]
    
    for i in range(n):
        L[i][i] = 1.0
    
    for 主元列 in range(n):
        for i in range(主元列 + 1, n):
            因子 = U[i][主元列] / U[主元列][主元列]
            L[i][主元列] = 因子
            for j in range(主元列, n):
                U[i][j] -= 因子 * U[主元列][j]
    
    return L, U


def QR分解(矩阵: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """QR分解（Gram-Schmidt正交化）"""
    n = len(矩阵)
    列数 = len(矩阵[0]) if 矩阵 else 0
    
    Q = 零矩阵(n, 列数)
    R = 零矩阵(列数, 列数)
    
    for j in range(列数):
        v = list(矩阵[i][j] for i in range(n))
        
        for i in range(j):
            投影 = sum(Q[k][i] * v[k] for k in range(n))
            R[i][j] = 投影
            for k in range(n):
                v[k] -= 投影 * Q[k][i]
        
        范数 = math.sqrt(sum(x ** 2 for x in v))
        R[j][j] = 范数
        
        for i in range(n):
            Q[i][j] = v[i] / 范数
    
    return Q, R


def 特征值(矩阵: List[List[float]], 迭代次数: int = 100) -> List[float]:
    """幂法计算主特征值（简化版）"""
    n = len(矩阵)
    
    x = [1.0] * n
    for _ in range(迭代次数):
        y = [0.0] * n
        for i in range(n):
            for j in range(n):
                y[i] += 矩阵[i][j] * x[j]
        
        范数 = math.sqrt(sum(v ** 2 for v in y))
        if 范数 < 1e-10:
            break
        x = [v / 范数 for v in y]
    
    特征值 = sum(sum(矩阵[i][j] * x[j] for j in range(n)) * x[i] for i in range(n))
    return [特征值]


def 向量范数(向量: List[float], 阶数: int = 2) -> float:
    """计算向量范数"""
    if 阶数 == float('inf'):
        return max(abs(x) for x in 向量)
    if 阶数 == 1:
        return sum(abs(x) for x in 向量)
    return math.pow(sum(abs(x) ** 阶数 for x in 向量), 1.0 / 阶数)


def 矩阵范数(矩阵: List[List[float]], 类型: str = 'Frobenius') -> float:
    """计算矩阵范数"""
    if 类型 == 'Frobenius':
        return math.sqrt(sum(sum(x ** 2 for x in row) for row in 矩阵))
    elif 类型 == '行和':
        return max(sum(abs(x) for x in row) for row in 矩阵)
    elif 类型 == '列和':
        列数 = len(矩阵[0]) if 矩阵 else 0
        return max(sum(abs(矩阵[i][j]) for i in range(len(矩阵))) for j in range(列数))
    else:
        raise ValueError(f'未知范数类型: {类型}')


def 向量内积(a: List[float], b: List[float]) -> float:
    """向量内积"""
    if len(a) != len(b):
        raise ValueError('向量长度必须相同')
    return sum(x * y for x, y in zip(a, b))


def 向量正交化(向量列表: List[List[float]]) -> List[List[float]]:
    """Gram-Schmidt正交化"""
    结果 = []
    for v in 向量列表:
        新向量 = list(v)
        for u in 结果:
            投影 = 向量内积(v, u) / 向量内积(u, u)
            for i in range(len(新向量)):
                新向量[i] -= 投影 * u[i]
        结果.append(新向量)
    return 结果


def 向量单位化(向量: List[float]) -> List[float]:
    """向量单位化"""
    范数 = 向量范数(向量)
    if 范数 < 1e-10:
        raise ValueError('零向量无法单位化')
    return [x / 范数 for x in 向量]


def 条件数(矩阵: List[List[float]]) -> float:
    """计算矩阵条件数（简化版）"""
    try:
        逆 = 逆矩阵(矩阵)
        return 矩阵范数(矩阵) * 矩阵范数(逆)
    except ValueError:
        return float('inf')


def 秩(矩阵: List[List[float]]) -> int:
    """计算矩阵秩（简化版）"""
    n = len(矩阵)
    m = len(矩阵[0]) if 矩阵 else 0
    
    副本 = [list(row) for row in 矩阵]
    秩 = 0
    
    for 主元列 in range(min(n, m)):
        最大值 = abs(副本[秩][主元列])
        主元行 = 秩
        for i in range(秩 + 1, n):
            if abs(副本[i][主元列]) > 最大值:
                最大值 = abs(副本[i][主元列])
                主元行 = i
        
        if abs(最大值) < 1e-10:
            continue
        
        副本[秩], 副本[主元行] = 副本[主元行], 副本[秩]
        
        for i in range(n):
            if i != 秩 and abs(副本[i][主元列]) > 1e-10:
                因子 = 副本[i][主元列] / 副本[秩][主元列]
                for j in range(m):
                    副本[i][j] -= 因子 * 副本[秩][j]
        
        秩 += 1
    
    return 秩


def 迹(矩阵: List[List[float]]) -> float:
    """计算矩阵迹"""
    n = len(矩阵)
    return sum(矩阵[i][i] for i in range(n))


def 对角化(矩阵: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """对角化（简化版，仅适用于可对角化矩阵）"""
    n = len(矩阵)
    对角矩阵 = 零矩阵(n, n)
    
    特征值列表 = []
    for _ in range(n):
        特征值列表.append(特征值(矩阵)[0])
    
    for i in range(n):
        对角矩阵[i][i] = 特征值列表[i]
    
    return 对角矩阵, 对角矩阵