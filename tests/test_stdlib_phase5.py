"""
第五阶段标准库测试
测试：装饰器、上下文管理器
"""
import unittest
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'stdlib'))


class Test装饰器(unittest.TestCase):
    """测试装饰器模块"""
    
    def test_缓存(self):
        """测试缓存装饰器"""
        from 装饰器 import 缓存
        
        调用次数 = [0]
        
        @缓存(最大缓存数=10)
        def 计算(x):
            调用次数[0] += 1
            return x * x
        
        结果1 = 计算(5)
        结果2 = 计算(5)
        结果3 = 计算(6)
        
        self.assertEqual(结果1, 25)
        self.assertEqual(结果2, 25)
        self.assertEqual(结果3, 36)
        self.assertEqual(调用次数[0], 2)
        
        缓存信息 = 计算.获取缓存信息()
        self.assertEqual(缓存信息['大小'], 2)
        self.assertGreaterEqual(缓存信息['命中率'], 0.3)
        
        计算.清除缓存()
        self.assertEqual(计算.获取缓存信息()['大小'], 0)
    
    def test_缓存带过期(self):
        """测试带过期时间的缓存"""
        from 装饰器 import 缓存带过期
        
        @缓存带过期(过期秒数=0.1)
        def 获取时间():
            return time.time()
        
        t1 = 获取时间()
        t2 = 获取时间()
        self.assertEqual(t1, t2)
        
        time.sleep(0.15)
        t3 = 获取时间()
        self.assertNotEqual(t1, t3)
    
    def test_缓存LRU(self):
        """测试LRU缓存"""
        from 装饰器 import 缓存LRU
        
        @缓存LRU(最大缓存数=3)
        def 函数(x):
            return x
        
        for i in range(5):
            函数(i)
        
        info = 函数.获取缓存信息()
        self.assertEqual(info['大小'], 3)
    
    def test_重试(self):
        """测试重试装饰器"""
        from 装饰器 import 重试
        
        尝试次数 = [0]
        
        @重试(最大次数=3, 间隔秒数=0.01)
        def 可能失败(should_fail):
            尝试次数[0] += 1
            if should_fail:
                raise ValueError("测试失败")
            return "成功"
        
        result = 可能失败(False)
        self.assertEqual(result, "成功")
        self.assertEqual(尝试次数[0], 1)
        
        尝试次数[0] = 0
        with self.assertRaises(ValueError):
            可能失败(True)
        self.assertEqual(尝试次数[0], 3)
    
    def test_计时(self):
        """测试计时装饰器"""
        from 装饰器 import 计时
        
        结果列表 = []
        
        @计时(日志函数=lambda x: 结果列表.append(x))
        def 耗时操作():
            time.sleep(0.01)
            return 42
        
        result = 耗时操作()
        self.assertEqual(result, 42)
        self.assertTrue(len(结果列表) > 0)
        self.assertIn('执行时间', 结果列表[0])
    
    def test_异常处理(self):
        """测试异常处理装饰器"""
        from 装饰器 import 异常处理
        
        @异常处理(捕获异常=(ValueError,), 返回值='错误')
        def 会出错():
            raise ValueError("测试")
        
        result = 会出错()
        self.assertEqual(result, '错误')
    
    def test_类型检查(self):
        """测试类型检查装饰器"""
        from 装饰器 import 类型检查
        
        @类型检查(int, str)
        def 函数(a, b):
            return f'{a}-{b}'
        
        result = 函数(1, 'hello')
        self.assertEqual(result, '1-hello')
        
        with self.assertRaises(TypeError):
            函数('not int', 'hello')
    
    def test_权限检查(self):
        """测试权限检查装饰器"""
        from 装饰器 import 权限检查
        
        def 检查权限(user):
            return user == 'admin'
        
        @权限检查(检查权限, 未授权返回值='未授权')
        def 敏感操作(user):
            return f'欢迎 {user}'
        
        result1 = 敏感操作('admin')
        self.assertEqual(result1, '欢迎 admin')
        
        result2 = 敏感操作('guest')
        self.assertEqual(result2, '未授权')
    
    def test_单例(self):
        """测试单例装饰器"""
        from 装饰器 import 单例
        
        @单例
        class 计数器:
            def __init__(self):
                self.value = 0
            
            def 增加(self):
                self.value += 1
        
        c1 = 计数器()
        c2 = 计数器()
        
        self.assertIs(c1, c2)
        c1.增加()
        self.assertEqual(c2.value, 1)
    
    def test_同步(self):
        """测试同步装饰器"""
        from 装饰器 import 同步
        from 线程 import 创建线程
        
        计数器 = [0]
        
        @同步()
        def 增加():
            计数器[0] += 1
        
        threads = [创建线程(增加) for _ in range(100)]
        for t in threads:
            t.join()
        
        self.assertEqual(计数器[0], 100)
    
    def test_限流(self):
        """测试限流装饰器"""
        from 装饰器 import 限流
        
        @限流(最大调用次数=3, 时间窗口秒数=1)
        def 受限函数():
            return 'ok'
        
        for _ in range(3):
            受限函数()
        
        with self.assertRaises(ValueError):
            受限函数()
        
        受限函数.重置限制()
        受限函数()
    
    def test_统计(self):
        """测试统计装饰器"""
        from 装饰器 import 统计
        
        @统计()
        def 函数(x):
            time.sleep(0.001)
            return x * 2
        
        for i in range(5):
            函数(i)
        
        统计数据 = 函数.获取统计数据()
        self.assertEqual(统计数据['调用次数'], 5)
        self.assertGreater(统计数据['总耗时'], 0)
        self.assertGreaterEqual(统计数据['平均耗时'], 0)


class Test上下文管理器(unittest.TestCase):
    """测试上下文管理器模块"""
    
    def test_临时文件(self):
        """测试临时文件"""
        from 上下文管理器 import 临时文件
        
        with 临时文件() as 文件路径:
            self.assertTrue(os.path.exists(文件路径))
            with open(文件路径, 'w') as f:
                f.write('test content')
        
        self.assertFalse(os.path.exists(文件路径))
    
    def test_临时文件不删除(self):
        """测试临时文件不删除"""
        from 上下文管理器 import 临时文件
        
        文件路径 = None
        with 临时文件(删除=False) as fp:
            文件路径 = fp
            self.assertTrue(os.path.exists(fp))
        
        self.assertTrue(os.path.exists(文件路径))
        os.remove(文件路径)
    
    def test_临时目录(self):
        """测试临时目录"""
        from 上下文管理器 import 临时目录
        
        with 临时目录() as 目录路径:
            self.assertTrue(os.path.isdir(目录路径))
            文件路径 = os.path.join(目录路径, 'test.txt')
            with open(文件路径, 'w') as f:
                f.write('test')
        
        self.assertFalse(os.path.exists(目录路径))
    
    def test_临时目录不删除(self):
        """测试临时目录不删除"""
        from 上下文管理器 import 临时目录
        
        目录路径 = None
        with 临时目录(删除=False) as dp:
            目录路径 = dp
            self.assertTrue(os.path.isdir(dp))
        
        self.assertTrue(os.path.exists(目录路径))
        import shutil
        shutil.rmtree(目录路径)
    
    def test_自动关闭(self):
        """测试自动关闭"""
        from 上下文管理器 import 自动关闭
        
        class 模拟资源:
            def __init__(self):
                self.已关闭 = False
            
            def close(self):
                self.已关闭 = True
        
        资源 = 模拟资源()
        with 自动关闭(资源):
            pass
        
        self.assertTrue(资源.已关闭)
    
    def test_计时器上下文(self):
        """测试计时器上下文"""
        from 上下文管理器 import 计时器上下文
        
        日志 = []
        with 计时器上下文(日志函数=lambda x: 日志.append(x), 名称='测试'):
            time.sleep(0.01)
        
        self.assertTrue(len(日志) > 0)
        self.assertIn('测试', 日志[0])
        self.assertIn('耗时', 日志[0])
    
    def test_锁上下文(self):
        """测试锁上下文"""
        from 上下文管理器 import 锁上下文
        from 线程 import 创建线程
        
        计数器 = [0]
        锁 = __import__('threading').Lock()
        
        def 增加():
            with 锁上下文(锁):
                计数器[0] += 1
        
        threads = [创建线程(增加) for _ in range(50)]
        for t in threads:
            t.join()
        
        self.assertEqual(计数器[0], 50)
    
    def test_事务(self):
        """测试事务"""
        from 上下文管理器 import 事务
        
        状态 = []
        
        def 提交():
            状态.append('已提交')
        
        def 回滚():
            状态.append('已回滚')
        
        with 事务(提交, 回滚):
            pass
        
        self.assertEqual(状态, ['已提交'])
        
        状态.clear()
        try:
            with 事务(提交, 回滚):
                raise ValueError("测试")
        except:
            pass
        
        self.assertEqual(状态, ['已回滚'])
    
    def test_变更恢复(self):
        """测试变更恢复"""
        from 上下文管理器 import 变更恢复
        
        class 对象:
            def __init__(self):
                self.value = 10
        
        obj = 对象()
        self.assertEqual(obj.value, 10)
        
        with 变更恢复(obj, 'value', 20):
            self.assertEqual(obj.value, 20)
        
        self.assertEqual(obj.value, 10)
    
    def test_环境变量上下文(self):
        """测试环境变量上下文"""
        from 上下文管理器 import 环境变量上下文
        
        旧值 = os.environ.get('TEST_VAR')
        
        with 环境变量上下文(TEST_VAR='test_value'):
            self.assertEqual(os.environ.get('TEST_VAR'), 'test_value')
        
        if 旧值 is None:
            self.assertNotIn('TEST_VAR', os.environ)
        else:
            self.assertEqual(os.environ.get('TEST_VAR'), 旧值)
    
    def test_工作目录(self):
        """测试工作目录"""
        from 上下文管理器 import 工作目录
        
        旧目录 = os.getcwd()
        
        with 工作目录('.') as 新目录:
            self.assertEqual(os.getcwd(), os.path.abspath('.'))
        
        self.assertEqual(os.getcwd(), 旧目录)
    
    def test_静默异常(self):
        """测试静默异常"""
        from 上下文管理器 import 静默异常
        
        日志 = []
        
        with 静默异常(日志函数=lambda x: 日志.append(x)):
            raise ValueError("测试异常")
        
        self.assertTrue(len(日志) > 0)
    
    def test_创建删除临时文件目录(self):
        """测试创建删除临时文件目录"""
        from 上下文管理器 import 创建临时文件, 创建临时目录, 删除临时文件, 删除临时目录
        
        文件路径 = 创建临时文件()
        self.assertTrue(os.path.exists(文件路径))
        删除临时文件(文件路径)
        self.assertFalse(os.path.exists(文件路径))
        
        目录路径 = 创建临时目录()
        self.assertTrue(os.path.isdir(目录路径))
        删除临时目录(目录路径)
        self.assertFalse(os.path.exists(目录路径))


if __name__ == '__main__':
    unittest.main()
