"""
第六阶段标准库测试
测试：矩阵运算、随机数、统计函数、线性代数、日期时间
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'stdlib'))


class Test矩阵运算(unittest.TestCase):
    """测试矩阵运算模块"""
    
    def test_创建数组(self):
        """测试创建数组"""
        from 矩阵运算 import 创建数组
        
        arr = 创建数组([1, 2, 3, 4])
        self.assertEqual(arr.形状(), (4,))
        self.assertEqual(arr.维度(), 1)
        self.assertEqual(arr.大小(), 4)
    
    def test_二维数组(self):
        """测试二维数组"""
        from 矩阵运算 import 创建数组
        
        arr = 创建数组([[1, 2], [3, 4]])
        self.assertEqual(arr.形状(), (2, 2))
        self.assertEqual(arr[0, 1], 2)
        self.assertEqual(arr[1, 0], 3)
    
    def test_数组运算(self):
        """测试数组运算"""
        from 矩阵运算 import 创建数组
        
        a = 创建数组([1, 2, 3])
        b = 创建数组([4, 5, 6])
        
        c = a + b
        self.assertEqual(c.扁平化(), [5, 7, 9])
        
        c = a * 2
        self.assertEqual(c.扁平化(), [2, 4, 6])
        
        c = a - b
        self.assertEqual(c.扁平化(), [-3, -3, -3])
    
    def test_转置(self):
        """测试转置"""
        from 矩阵运算 import 创建数组
        
        arr = 创建数组([[1, 2], [3, 4]])
        转置 = arr.转置()
        self.assertEqual(转置[0, 0], 1)
        self.assertEqual(转置[0, 1], 3)
        self.assertEqual(转置[1, 0], 2)
        self.assertEqual(转置[1, 1], 4)
    
    def test_矩阵乘法(self):
        """测试矩阵乘法"""
        from 矩阵运算 import 创建数组, 矩阵乘法
        
        a = 创建数组([[1, 2], [3, 4]])
        b = 创建数组([[5, 6], [7, 8]])
        
        result = 矩阵乘法(a, b)
        self.assertEqual(result[0, 0], 19)
        self.assertEqual(result[0, 1], 22)
        self.assertEqual(result[1, 0], 43)
        self.assertEqual(result[1, 1], 50)
    
    def test_点积(self):
        """测试点积"""
        from 矩阵运算 import 创建数组, 点积
        
        a = 创建数组([1, 2, 3])
        b = 创建数组([4, 5, 6])
        
        result = 点积(a, b)
        self.assertEqual(result, 32)
    
    def test_全零全一(self):
        """测试全零全一"""
        from 矩阵运算 import 全零, 全一
        
        zeros = 全零((2, 3))
        self.assertEqual(zeros.形状(), (2, 3))
        self.assertEqual(zeros.扁平化(), [0, 0, 0, 0, 0, 0])
        
        ones = 全一((2, 3))
        self.assertEqual(ones.形状(), (2, 3))
        self.assertEqual(ones.扁平化(), [1, 1, 1, 1, 1, 1])
    
    def test_统计聚合(self):
        """测试统计聚合"""
        from 矩阵运算 import 创建数组
        
        arr = 创建数组([[1, 2], [3, 4]])
        self.assertEqual(arr.求和(), 10)
        self.assertEqual(arr.均值(), 2.5)
        self.assertEqual(arr.最大值(), 4)
        self.assertEqual(arr.最小值(), 1)


class Test随机数(unittest.TestCase):
    """测试随机数模块"""
    
    def test_设置种子(self):
        """测试设置种子"""
        from 随机数 import 设置种子, 获取种子, 随机
        
        设置种子(42)
        seed = 获取种子()
        self.assertEqual(seed, 42)
        
        r1 = 随机()
        设置种子(42)
        r2 = 随机()
        self.assertEqual(r1, r2)
    
    def test_随机整数(self):
        """测试随机整数"""
        from 随机数 import 设置种子, 随机整数
        
        设置种子(42)
        for _ in range(100):
            r = 随机整数(0, 100)
            self.assertGreaterEqual(r, 0)
            self.assertLessEqual(r, 100)
    
    def test_随机浮点数(self):
        """测试随机浮点数"""
        from 随机数 import 设置种子, 随机浮点数
        
        设置种子(42)
        for _ in range(100):
            r = 随机浮点数(0, 1)
            self.assertGreaterEqual(r, 0)
            self.assertLess(r, 1)
    
    def test_正态分布(self):
        """测试正态分布"""
        from 随机数 import 设置种子, 正态分布
        
        设置种子(42)
        values = [正态分布(0, 1) for _ in range(1000)]
        mean = sum(values) / len(values)
        self.assertAlmostEqual(mean, 0, places=1)
    
    def test_随机选择(self):
        """测试随机选择"""
        from 随机数 import 设置种子, 随机选择, 随机选择多个
        
        设置种子(42)
        seq = [1, 2, 3, 4, 5]
        result = 随机选择(seq)
        self.assertIn(result, seq)
        
        results = 随机选择多个(seq, 3)
        self.assertEqual(len(results), 3)
    
    def test_随机洗牌(self):
        """测试随机洗牌"""
        from 随机数 import 设置种子, 随机洗牌
        
        设置种子(42)
        seq = [1, 2, 3, 4, 5]
        shuffled = 随机洗牌(seq)
        self.assertEqual(sorted(shuffled), [1, 2, 3, 4, 5])
    
    def test_随机字符串(self):
        """测试随机字符串"""
        from 随机数 import 设置种子, 随机字符串
        
        设置种子(42)
        s = 随机字符串(10)
        self.assertEqual(len(s), 10)


class Test统计函数(unittest.TestCase):
    """测试统计函数模块"""
    
    def test_均值(self):
        """测试均值"""
        from 统计函数 import 均值
        
        data = [1, 2, 3, 4, 5]
        self.assertEqual(均值(data), 3.0)
    
    def test_中位数(self):
        """测试中位数"""
        from 统计函数 import 中位数
        
        data_odd = [1, 2, 3, 4, 5]
        self.assertEqual(中位数(data_odd), 3)
        
        data_even = [1, 2, 3, 4]
        self.assertEqual(中位数(data_even), 2.5)
    
    def test_众数(self):
        """测试众数"""
        from 统计函数 import 众数
        
        data = [1, 2, 2, 3, 3, 3]
        self.assertEqual(众数(data), [3])
    
    def test_方差标准差(self):
        """测试方差标准差"""
        from 统计函数 import 方差, 标准差
        
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(方差(data), 2.0)
        self.assertAlmostEqual(标准差(data), 1.4142, places=3)
    
    def test_皮尔逊相关系数(self):
        """测试皮尔逊相关系数"""
        from 统计函数 import 皮尔逊相关系数
        
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(皮尔逊相关系数(x, y), 1.0)
    
    def test_协方差(self):
        """测试协方差"""
        from 统计函数 import 协方差
        
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(协方差(x, y), 4.0)
    
    def test_分位数(self):
        """测试分位数"""
        from 统计函数 import 分位数
        
        data = [1, 2, 3, 4, 5]
        self.assertEqual(分位数(data, 0.5), 3)
    
    def test_归一化(self):
        """测试归一化"""
        from 统计函数 import 归一化
        
        data = [1, 2, 3, 4, 5]
        normalized = 归一化(data, 'minmax')
        self.assertEqual(normalized[0], 0.0)
        self.assertEqual(normalized[-1], 1.0)


class Test线性代数(unittest.TestCase):
    """测试线性代数模块"""
    
    def test_行列式(self):
        """测试行列式"""
        from 线性代数 import 行列式
        
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(行列式(matrix), -2)
    
    def test_转置(self):
        """测试转置"""
        from 线性代数 import 转置
        
        matrix = [[1, 2], [3, 4]]
        result = 转置(matrix)
        self.assertEqual(result[0], [1, 3])
        self.assertEqual(result[1], [2, 4])
    
    def test_矩阵乘法(self):
        """测试矩阵乘法"""
        from 线性代数 import 矩阵乘法
        
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = 矩阵乘法(a, b)
        self.assertEqual(result[0][0], 19)
        self.assertEqual(result[1][1], 50)
    
    def test_逆矩阵(self):
        """测试逆矩阵"""
        from 线性代数 import 逆矩阵, 矩阵乘法, 单位矩阵
        
        matrix = [[1, 2], [3, 4]]
        inv = 逆矩阵(matrix)
        
        result = 矩阵乘法(matrix, inv)
        expected = [[1, 0], [0, 1]]
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result[i][j], expected[i][j], places=10)
    
    def test_高斯消元(self):
        """测试高斯消元"""
        from 线性代数 import 高斯消元
        
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        b = [8, -11, -3]
        x = 高斯消元(A, b)
        
        self.assertAlmostEqual(x[0], 2)
        self.assertAlmostEqual(x[1], 3)
        self.assertAlmostEqual(x[2], -1)
    
    def test_LU分解(self):
        """测试LU分解"""
        from 线性代数 import LU分解, 矩阵乘法
        
        A = [[4, 3], [6, 3]]
        L, U = LU分解(A)
        
        result = 矩阵乘法(L, U)
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result[i][j], A[i][j], places=10)
    
    def test_向量范数(self):
        """测试向量范数"""
        from 线性代数 import 向量范数
        
        v = [3, 4]
        self.assertEqual(向量范数(v, 2), 5)
    
    def test_秩(self):
        """测试秩"""
        from 线性代数 import 秩
        
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(秩(matrix), 2)


class Test日期时间(unittest.TestCase):
    """测试日期时间模块"""
    
    def test_日期时间创建(self):
        """测试日期时间创建"""
        from 日期时间 import 日期时间
        
        dt = 日期时间(2024, 1, 15, 10, 30, 45)
        self.assertEqual(dt.年(), 2024)
        self.assertEqual(dt.月(), 1)
        self.assertEqual(dt.日(), 15)
        self.assertEqual(dt.时(), 10)
        self.assertEqual(dt.分(), 30)
        self.assertEqual(dt.秒(), 45)
    
    def test_日期时间运算(self):
        """测试日期时间运算"""
        from 日期时间 import 日期时间, 时间差
        
        dt1 = 日期时间(2024, 1, 1, 0, 0, 0)
        dt2 = 日期时间(2024, 1, 2, 0, 0, 0)
        
        delta = dt2 - dt1
        self.assertAlmostEqual(delta.天数(), 1.0)
        
        dt3 = dt1 + 时间差(天数=1)
        self.assertEqual(dt3.日(), 2)
    
    def test_格式化(self):
        """测试格式化"""
        from 日期时间 import 日期时间
        
        dt = 日期时间(2024, 6, 15, 14, 30, 45)
        formatted = dt.格式化('%Y-%m-%d %H:%M:%S')
        self.assertEqual(formatted, '2024-06-15 14:30:45')
    
    def test_从字符串解析(self):
        """测试从字符串解析"""
        from 日期时间 import 从字符串
        
        dt = 从字符串('2024-06-15 14:30:45')
        self.assertEqual(dt.年(), 2024)
        self.assertEqual(dt.月(), 6)
        self.assertEqual(dt.日(), 15)
    
    def test_时区转换(self):
        """测试时区转换"""
        from 日期时间 import 日期时间, 北京时间, 纽约时间
        
        dt = 日期时间(2024, 6, 15, 12, 0, 0, 时区=北京时间())
        ny_dt = dt.转换时区(纽约时间())
        self.assertEqual(ny_dt.时(), 23)
    
    def test_时间差(self):
        """测试时间差"""
        from 日期时间 import 时间差
        
        td = 时间差(天数=2, 秒数=3600)
        self.assertAlmostEqual(td.天数(), 2.0416666666666665)
        self.assertEqual(td.小时数(), 1)
    
    def test_工作日判断(self):
        """测试工作日判断"""
        from 日期时间 import 日期时间
        
        workday = 日期时间(2024, 6, 17, 0, 0, 0)
        self.assertTrue(workday.是否工作日())
        
        weekend = 日期时间(2024, 6, 15, 0, 0, 0)
        self.assertFalse(weekend.是否工作日())
    
    def test_闰年判断(self):
        """测试闰年判断"""
        from 日期时间 import 判断闰年
        
        self.assertTrue(判断闰年(2024))
        self.assertFalse(判断闰年(2023))
        self.assertTrue(判断闰年(2000))
        self.assertFalse(判断闰年(1900))
    
    def test_相对时间解析(self):
        """测试相对时间解析"""
        from 日期时间 import 解析相对时间, 当前时间, 减天数
        
        result = 解析相对时间('1天前')
        expected = 减天数(当前时间(), 1)
        self.assertEqual(result.年(), expected.年())
        self.assertEqual(result.月(), expected.月())
        self.assertEqual(result.日(), expected.日())


if __name__ == '__main__':
    unittest.main()