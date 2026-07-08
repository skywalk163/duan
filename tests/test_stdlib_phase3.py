"""
第三阶段标准库测试
测试：时间管理、线程、进程、网络请求
"""
import unittest
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'stdlib'))


def _进程测试函数(a, b):
    """进程测试用函数（模块级别，可被pickle）"""
    return a + b


class Test时间管理(unittest.TestCase):
    """测试时间管理模块"""
    
    def test_睡眠(self):
        """测试睡眠函数"""
        from 时间管理 import 睡眠, 睡眠毫秒
        
        开始 = time.perf_counter()
        睡眠(0.05)
        经过 = time.perf_counter() - 开始
        self.assertGreaterEqual(经过, 0.04)
        
        开始 = time.perf_counter()
        睡眠毫秒(50)
        经过 = time.perf_counter() - 开始
        self.assertGreaterEqual(经过, 0.04)
    
    def test_计时器(self):
        """测试计时器"""
        from 时间管理 import 计时器
        
        t = 计时器()
        t.开始()
        time.sleep(0.05)
        耗时 = t.结束()
        self.assertGreaterEqual(耗时, 0.04)
        
        t2 = 计时器()
        t2.开始()
        time.sleep(0.02)
        t2.打点('点1')
        time.sleep(0.02)
        t2.打点('点2')
        记录 = t2.获取记录()
        self.assertEqual(len(记录), 2)
        self.assertEqual(记录[0][0], '点1')
        self.assertEqual(记录[1][0], '点2')
    
    def test_计时器上下文(self):
        """测试计时器上下文管理器"""
        from 时间管理 import 计时器
        
        with 计时器() as t:
            time.sleep(0.02)
        self.assertGreater(t.经过时间(), 0.01)
    
    def test_计时函数(self):
        """测试计时函数"""
        from 时间管理 import 计时函数
        
        def 测试函数():
            time.sleep(0.02)
            return 42
        
        结果, 耗时 = 计时函数(测试函数)
        self.assertEqual(结果, 42)
        self.assertGreater(耗时, 0.01)
    
    def test_多次计时(self):
        """测试多次计时"""
        from 时间管理 import 多次计时
        
        def 测试函数():
            return sum(range(100))
        
        统计 = 多次计时(测试函数, 次数=5)
        self.assertEqual(统计['次数'], 5)
        self.assertIn('总时间', 统计)
        self.assertIn('平均时间', 统计)
        self.assertIn('最快', 统计)
        self.assertIn('最慢', 统计)
        self.assertEqual(统计['最后结果'], sum(range(100)))
    
    def test_倒计时(self):
        """测试倒计时"""
        from 时间管理 import 倒计时
        
        cd = 倒计时(0.1)
        self.assertFalse(cd.是否运行中())
        self.assertFalse(cd.是否结束())
        
        cd.开始()
        self.assertTrue(cd.是否运行中())
        self.assertGreater(cd.剩余时间(), 0)
        
        cd.等待结束()
        self.assertTrue(cd.是否结束())
        self.assertEqual(cd.剩余时间(), 0)
    
    def test_倒计时暂停继续(self):
        """测试倒计时暂停/继续"""
        from 时间管理 import 倒计时
        
        cd = 倒计时(0.2)
        cd.开始()
        time.sleep(0.05)
        cd.暂停()
        
        暂停时剩余 = cd.剩余时间()
        self.assertFalse(cd.是否运行中())
        self.assertGreater(暂停时剩余, 0)
        
        time.sleep(0.05)
        self.assertEqual(cd.剩余时间(), 暂停时剩余)
        
        cd.继续()
        self.assertTrue(cd.是否运行中())
        cd.等待结束()
        self.assertTrue(cd.是否结束())
    
    def test_定时器(self):
        """测试定时器"""
        from 时间管理 import 定时器
        
        结果 = []
        
        def 回调():
            结果.append('触发')
        
        t = 定时器(0.05, 回调)
        t.开始()
        self.assertTrue(t.是否运行中())
        
        time.sleep(0.15)
        self.assertEqual(结果, ['触发'])
        self.assertFalse(t.是否运行中())
    
    def test_定时器取消(self):
        """测试定时器取消"""
        from 时间管理 import 定时器
        
        结果 = []
        
        def 回调():
            结果.append('触发')
        
        t = 定时器(0.2, 回调)
        t.开始()
        t.取消()
        
        time.sleep(0.3)
        self.assertEqual(结果, [])
    
    def test_时间戳(self):
        """测试时间戳函数"""
        from 时间管理 import 时间戳, 时间戳毫秒, 性能计数器
        
        ts = 时间戳()
        self.assertIsInstance(ts, float)
        self.assertGreater(ts, 1700000000)
        
        tsm = 时间戳毫秒()
        self.assertIsInstance(tsm, int)
        self.assertGreater(tsm, 1700000000000)
        
        pc = 性能计数器()
        self.assertIsInstance(pc, float)
    
    def test_格式化耗时(self):
        """测试格式化耗时"""
        from 时间管理 import 格式化耗时
        
        self.assertIn('微秒', 格式化耗时(0.0005))
        self.assertIn('毫秒', 格式化耗时(0.5))
        self.assertIn('秒', 格式化耗时(10))
        self.assertIn('分', 格式化耗时(120))
        self.assertIn('时', 格式化耗时(3600 + 120))


class Test线程(unittest.TestCase):
    """测试线程模块"""
    
    def test_创建线程(self):
        """测试创建线程"""
        from 线程 import 创建线程, 当前线程标识
        
        结果 = []
        
        def 任务():
            结果.append(当前线程标识())
        
        t = 创建线程(任务)
        t.join()
        
        self.assertEqual(len(结果), 1)
        self.assertNotEqual(结果[0], 当前线程标识())
    
    def test_线程类(self):
        """测试线程类"""
        from 线程 import 线程
        
        def 任务(a, b):
            return a + b
        
        t = 线程(任务, 1, 2)
        t.开始()
        结果 = t.获取结果()
        self.assertEqual(结果, 3)
        self.assertTrue(t.是否完成())
    
    def test_线程异常(self):
        """测试线程异常处理"""
        from 线程 import 线程
        
        def 任务():
            raise ValueError("测试错误")
        
        t = 线程(任务)
        t.开始()
        t.等待()
        
        self.assertTrue(t.是否完成())
        self.assertIsNotNone(t.获取异常())
        with self.assertRaises(ValueError):
            t.获取结果()
    
    def test_互斥锁(self):
        """测试互斥锁"""
        from 线程 import 互斥锁, 创建线程
        
        锁 = 互斥锁()
        计数器 = 0
        
        def 任务():
            nonlocal 计数器
            for _ in range(1000):
                锁.加锁()
                计数器 += 1
                锁.解锁()
        
        线程列表 = [创建线程(任务) for _ in range(5)]
        for t in 线程列表:
            t.join()
        
        self.assertEqual(计数器, 5000)
    
    def test_互斥锁上下文(self):
        """测试互斥锁上下文管理器"""
        from 线程 import 互斥锁
        
        锁 = 互斥锁()
        with 锁:
            self.assertTrue(锁.已锁定())
        self.assertFalse(锁.已锁定())
    
    def test_信号量(self):
        """测试信号量"""
        from 线程 import 信号量
        
        sem = 信号量(3)
        sem.获取()
        sem.获取()
        sem.获取()
        self.assertFalse(sem.获取(阻塞=False))
        sem.释放()
        self.assertTrue(sem.获取(阻塞=False))
        sem.释放()
        sem.释放()
        sem.释放()
    
    def test_事件(self):
        """测试事件"""
        from 线程 import 事件, 创建线程
        
        ev = 事件()
        结果 = []
        
        def 等待任务():
            ev.等待()
            结果.append('触发')
        
        创建线程(等待任务)
        time.sleep(0.02)
        self.assertEqual(结果, [])
        
        ev.设置()
        time.sleep(0.02)
        self.assertEqual(结果, ['触发'])
        self.assertTrue(ev.是否已设置())
        
        ev.清除()
        self.assertFalse(ev.是否已设置())
    
    def test_线程安全队列(self):
        """测试线程安全队列"""
        from 线程 import 线程安全队列, 创建线程
        
        q = 线程安全队列(10)
        self.assertTrue(q.空())
        
        def 生产者():
            for i in range(10):
                q.入队(i)
        
        结果 = []
        def 消费者():
            for i in range(10):
                结果.append(q.出队())
        
        t1 = 创建线程(生产者)
        t2 = 创建线程(消费者)
        t1.join()
        t2.join()
        
        self.assertEqual(len(结果), 10)
        self.assertEqual(set(结果), set(range(10)))
        self.assertTrue(q.空())
    
    def test_线程池(self):
        """测试线程池"""
        from 线程 import 线程池
        
        池 = 线程池(最大线程数=4)
        池.启动()
        
        结果列表 = []
        锁 = []
        
        def 任务(x):
            return x * x
        
        for i in range(10):
            池.提交(任务, i, 结果回调=lambda r, e, idx=i: 结果列表.append((idx, r)))
        
        池.等待完成()
        池.关闭()
        
        self.assertEqual(len(结果列表), 10)
        结果列表.sort()
        for i in range(10):
            self.assertEqual(结果列表[i][1], i * i)
    
    def test_并发执行(self):
        """测试并发执行"""
        from 线程 import 并发执行
        
        任务列表 = [
            lambda: 1 * 1,
            lambda: 2 * 2,
            lambda: 3 * 3,
        ]
        
        结果 = 并发执行(任务列表, 最大线程数=3)
        self.assertEqual(结果, [1, 4, 9])
    
    def test_并发执行带参数(self):
        """测试并发执行带参数"""
        from 线程 import 并发执行带参数
        
        def 任务(a, b):
            return a + b
        
        参数列表 = [(1, 2), (3, 4), (5, 6)]
        结果 = 并发执行带参数(任务, 参数列表, 最大线程数=3)
        self.assertEqual(结果, [3, 7, 11])


class Test进程(unittest.TestCase):
    """测试进程模块"""
    
    def test_当前进程标识(self):
        """测试进程ID"""
        from 进程 import 当前进程标识, 父进程标识, CPU核心数
        
        pid = 当前进程标识()
        self.assertIsInstance(pid, int)
        self.assertGreater(pid, 0)
        
        ppid = 父进程标识()
        self.assertIsInstance(ppid, int)
        self.assertGreater(ppid, 0)
        
        cores = CPU核心数()
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)
    
    def test_执行系统命令(self):
        """测试执行系统命令"""
        from 进程 import 执行系统命令
        
        结果 = 执行系统命令('echo hello')
        self.assertEqual(结果['返回码'], 0)
        self.assertFalse(结果['超时'])
        self.assertIn('hello', 结果['标准输出'])
    
    def test_进程类(self):
        """测试进程类"""
        from 进程 import 进程
        
        p = 进程(_进程测试函数, 10, 20)
        p.开始()
        结果 = p.获取结果(超时=5)
        self.assertEqual(结果, 30)
    
    def test_进程队列(self):
        """测试进程队列"""
        from 进程 import 进程队列
        
        q = 进程队列()
        self.assertTrue(q.空())
        
        q.入队('test')
        q.入队(123)
        q.入队({'a': 1})
        
        self.assertEqual(q.出队(), 'test')
        self.assertEqual(q.出队(), 123)
        self.assertEqual(q.出队(), {'a': 1})
    
    def test_共享值(self):
        """测试共享值"""
        from 进程 import 共享值
        
        sv = 共享值('i', 0)
        self.assertEqual(sv.获取(), 0)
        
        sv.设置(42)
        self.assertEqual(sv.获取(), 42)
    
    def test_共享数组(self):
        """测试共享数组"""
        from 进程 import 共享数组
        
        sa = 共享数组('i', 5)
        self.assertEqual(sa.长度(), 5)
        
        sa.设置(0, 10)
        sa.设置(1, 20)
        self.assertEqual(sa.获取(0), 10)
        self.assertEqual(sa.获取(1), 20)
    
    def test_进程锁(self):
        """测试进程锁"""
        from 进程 import 进程锁
        
        锁 = 进程锁()
        with 锁:
            pass
    
    def test_管道(self):
        """测试管道"""
        from 进程 import 管道
        
        pipe = 管道()
        pipe.标记父端()
        pipe.关闭本端()
        pipe.关闭对端()


class Test网络请求(unittest.TestCase):
    """测试网络请求模块"""
    
    def test_URL编码解码(self):
        """测试URL编码解码"""
        from 网络请求 import 编码URL, 解码URL
        
        原始 = '你好 world'
        编码 = 编码URL(原始)
        解码 = 解码URL(编码)
        self.assertEqual(解码, 原始)
    
    def test_解析URL(self):
        """测试URL解析"""
        from 网络请求 import 解析URL
        
        结果 = 解析URL('https://example.com:8080/path/to/page?a=1&b=2#frag')
        self.assertEqual(结果['协议'], 'https')
        self.assertEqual(结果['主机'], 'example.com')
        self.assertEqual(结果['端口'], 8080)
        self.assertEqual(结果['路径'], '/path/to/page')
        self.assertEqual(结果['查询'], 'a=1&b=2')
        self.assertEqual(结果['片段'], 'frag')
    
    def test_拼接URL(self):
        """测试URL拼接"""
        from 网络请求 import 拼接URL
        
        结果 = 拼接URL('https://example.com/', 'path', 'to', 'page')
        self.assertIn('path/to/page', 结果)
    
    def test_解析查询串(self):
        """测试查询串解析"""
        from 网络请求 import 解析查询串
        
        结果 = 解析查询串('a=1&b=2&c=3')
        self.assertEqual(结果['a'], '1')
        self.assertEqual(结果['b'], '2')
        self.assertEqual(结果['c'], '3')
    
    def test_响应对象(self):
        """测试响应对象"""
        from 网络请求 import 响应
        
        r = 响应(
            状态码=200,
            响应头={'content-type': 'application/json'},
            内容=b'{"key": "value"}',
            请求地址='http://example.com'
        )
        
        self.assertEqual(r.状态码, 200)
        self.assertTrue(r.是否成功)
        self.assertIn('application/json', r.获取头('content-type'))
        self.assertEqual(r.文本, '{"key": "value"}')
        self.assertEqual(r.JSON(), {'key': 'value'})
    
    def test_HTTP错误响应(self):
        """测试HTTP错误响应"""
        from 网络请求 import 响应, HTTP错误
        
        r = 响应(
            状态码=404,
            响应头={},
            内容=b'Not Found',
            请求地址='http://example.com/nonexistent'
        )
        
        self.assertEqual(r.状态码, 404)
        self.assertFalse(r.是否成功)
    
    def test_请求错误类(self):
        """测试错误类"""
        from 网络请求 import 请求错误, 超时错误, 连接错误, HTTP错误
        
        e1 = 请求错误('测试')
        self.assertIsInstance(e1, Exception)
        
        e2 = 超时错误('超时')
        self.assertIsInstance(e2, 请求错误)
        
        e3 = 连接错误('连接失败')
        self.assertIsInstance(e3, 请求错误)


if __name__ == '__main__':
    unittest.main()
