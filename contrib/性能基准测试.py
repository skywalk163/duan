"""
性能基准测试模块 - 计时、内存测量

提供性能基准测试功能，包括：
- 函数计时
- 内存测量
- 基准测试套件
- 性能报告
"""
import time
import tracemalloc
import gc
from typing import Callable, Dict, Any, List, Optional


class 计时结果:
    """计时结果类"""
    
    def __init__(self, 名称: str, 耗时: float, 调用次数: int = 1):
        self.名称 = 名称
        self.耗时 = 耗时
        self.调用次数 = 调用次数
        self.平均耗时 = 耗时 / 调用次数


class 内存测量结果:
    """内存测量结果类"""
    
    def __init__(self, 名称: str, 峰值内存: int, 当前内存: int, 分配数: int = 0):
        self.名称 = 名称
        self.峰值内存 = 峰值内存
        self.当前内存 = 当前内存
        self.分配数 = 分配数


class 基准测试结果:
    """基准测试结果类"""
    
    def __init__(self, 名称: str, 计时结果: 计时结果 = None, 内存结果: 内存测量结果 = None):
        self.名称 = 名称
        self.计时结果 = 计时结果
        self.内存结果 = 内存结果


def 计时(函数: Callable, *参数, **关键字参数) -> 计时结果:
    """计时函数执行"""
    开始时间 = time.perf_counter()
    函数(*参数, **关键字参数)
    结束时间 = time.perf_counter()
    耗时 = 结束时间 - 开始时间
    return 计时结果(函数.__name__, 耗时)


def 多次计时(函数: Callable, 次数: int = 1000, *参数, **关键字参数) -> 计时结果:
    """多次计时函数执行"""
    开始时间 = time.perf_counter()
    for _ in range(次数):
        函数(*参数, **关键字参数)
    结束时间 = time.perf_counter()
    耗时 = 结束时间 - 开始时间
    return 计时结果(函数.__name__, 耗时, 次数)


def 测量内存(函数: Callable, *参数, **关键字参数) -> 内存测量结果:
    """测量函数执行的内存使用"""
    tracemalloc.start()
    函数(*参数, **关键字参数)
    当前内存, 峰值内存 = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return 内存测量结果(函数.__name__, 峰值内存, 当前内存)


def 测量内存详细(函数: Callable, *参数, **关键字参数) -> 内存测量结果:
    """详细测量内存使用"""
    tracemalloc.start()
    快照1 = tracemalloc.take_snapshot()
    
    函数(*参数, **关键字参数)
    
    快照2 = tracemalloc.take_snapshot()
    当前内存, 峰值内存 = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    分配数 = len(快照2) - len(快照1)
    
    return 内存测量结果(函数.__name__, 峰值内存, 当前内存, 分配数)


def 基准测试(函数: Callable, 次数: int = 1000, 测量内存: bool = False, *参数, **关键字参数) -> 基准测试结果:
    """运行基准测试"""
    计时结果 = 多次计时(函数, 次数, *参数, **关键字参数)
    
    内存结果 = None
    if 测量内存:
        内存结果 = 测量内存详细(函数, *参数, **关键字参数)
    
    return 基准测试结果(函数.__name__, 计时结果, 内存结果)


class 基准测试套件:
    """基准测试套件"""
    
    def __init__(self, 名称: str = ''):
        self.名称 = 名称
        self._测试列表: List = []
        self._结果列表: List[基准测试结果] = []
    
    def 添加测试(self, 名称: str, 函数: Callable, 次数: int = 1000, 测量内存: bool = False):
        """添加测试"""
        self._测试列表.append({
            '名称': 名称,
            '函数': 函数,
            '次数': 次数,
            '测量内存': 测量内存
        })
    
    def 添加对比测试(self, 名称1: str, 函数1: Callable, 名称2: str, 函数2: Callable, 次数: int = 1000):
        """添加对比测试"""
        self.add测试(名称1, 函数1, 次数)
        self.add测试(名称2, 函数2, 次数)
    
    def 运行(self) -> List[基准测试结果]:
        """运行所有测试"""
        self._结果列表 = []
        
        for 测试 in self._测试列表:
            函数 = 测试['函数']
            次数 = 测试['次数']
            测量内存 = 测试['测量内存']
            
            开始时间 = time.perf_counter()
            for _ in range(次数):
                函数()
            耗时 = time.perf_counter() - 开始时间
            
            _计时结果 = 计时结果(测试['名称'], 耗时, 次数)
            
            内存结果 = None
            if 测量内存:
                tracemalloc.start()
                函数()
                当前内存, 峰值内存 = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                内存结果 = 内存测量结果(测试['名称'], 峰值内存, 当前内存)
            
            self._结果列表.append(基准测试结果(测试['名称'], _计时结果, 内存结果))
        
        return self._结果列表
    
    def 打印报告(self):
        """打印基准测试报告"""
        结果 = self.运行()
        
        print(f"\n{'='*60}")
        print(f"基准测试报告 - {self.名称}")
        print(f"{'='*60}")
        
        for 结果 in 结果:
            print(f"\n测试: {结果.名称}")
            if 结果.计时结果:
                计时 = 结果.计时结果
                print(f"  总耗时: {计时.耗时:.6f}秒")
                print(f"  调用次数: {计时.调用次数}")
                print(f"  平均耗时: {计时.平均耗时*1000000:.2f}微秒")
                print(f"  每秒调用: {1/计时.平均耗时:.0f}次/秒")
            
            if 结果.内存结果:
                内存 = 结果.内存结果
                print(f"  峰值内存: {内存.峰值内存/1024:.2f} KB")
                print(f"  当前内存: {内存.当前内存/1024:.2f} KB")
        
        print(f"\n{'='*60}")


class 性能计数器:
    """性能计数器"""
    
    def __init__(self):
        self._计数器: Dict[str, List[float]] = {}
        self._开始时间: Dict[str, float] = {}
    
    def 开始(self, 名称: str):
        """开始计时"""
        self._开始时间[名称] = time.perf_counter()
    
    def 结束(self, 名称: str) -> float:
        """结束计时并返回耗时"""
        if 名称 not in self._开始时间:
            return 0
        
        耗时 = time.perf_counter() - self._开始时间[名称]
        
        if 名称 not in self._计数器:
            self._计数器[名称] = []
        self._计数器[名称].append(耗时)
        
        return 耗时
    
    def 获取平均耗时(self, 名称: str) -> float:
        """获取平均耗时"""
        记录 = self._计数器.get(名称, [])
        if not 记录:
            return 0
        return sum(记录) / len(记录)
    
    def 获取最大耗时(self, 名称: str) -> float:
        """获取最大耗时"""
        记录 = self._计数器.get(名称, [])
        if not 记录:
            return 0
        return max(记录)
    
    def 获取最小耗时(self, 名称: str) -> float:
        """获取最小耗时"""
        记录 = self._计数器.get(名称, [])
        if not 记录:
            return 0
        return min(记录)
    
    def 获取调用次数(self, 名称: str) -> int:
        """获取调用次数"""
        return len(self._计数器.get(名称, []))
    
    def 打印统计(self):
        """打印统计信息"""
        print(f"\n{'='*60}")
        print(f"性能计数器统计")
        print(f"{'='*60}")
        
        for 名称, 记录 in self._计数器.items():
            平均 = sum(记录) / len(记录) if 记录 else 0
            最大 = max(记录) if 记录 else 0
            最小 = min(记录) if 记录 else 0
            
            print(f"\n{名称}:")
            print(f"  调用次数: {len(记录)}")
            print(f"  平均耗时: {平均*1000000:.2f}微秒")
            print(f"  最大耗时: {最大*1000000:.2f}微秒")
            print(f"  最小耗时: {最小*1000000:.2f}微秒")
    
    def 重置(self, 名称: str = None):
        """重置计数器"""
        if 名称:
            if 名称 in self._计数器:
                del self._计数器[名称]
            if 名称 in self._开始时间:
                del self._开始时间[名称]
        else:
            self._计数器 = {}
            self._开始时间 = {}


class 内存监控器:
    """内存监控器"""
    
    def __init__(self):
        self._快照列表: List = []
        self._启用 = False
    
    def 开始监控(self):
        """开始监控"""
        tracemalloc.start()
        self._启用 = True
    
    def 停止监控(self):
        """停止监控"""
        tracemalloc.stop()
        self._启用 = False
    
    def 拍摄快照(self, 标签: str = ''):
        """拍摄内存快照"""
        if not self._启用:
            return
        
        当前内存, 峰值内存 = tracemalloc.get_traced_memory()
        self._快照列表.append({
            '标签': 标签,
            '时间': time.time(),
            '当前内存': 当前内存,
            '峰值内存': 峰值内存
        })
    
    def 获取快照列表(self) -> List:
        """获取快照列表"""
        return self._快照列表
    
    def 打印快照(self):
        """打印快照信息"""
        print(f"\n{'='*60}")
        print(f"内存监控快照")
        print(f"{'='*60}")
        
        for 快照 in self._快照列表:
            print(f"\n标签: {快照['标签']}")
            print(f"  当前内存: {快照['当前内存']/1024:.2f} KB")
            print(f"  峰值内存: {快照['峰值内存']/1024:.2f} KB")
    
    def 生成对比报告(self, 快照1: int = 0, 快照2: int = -1) -> Dict[str, Any]:
        """生成对比报告"""
        if len(self._快照列表) < 2:
            return {}
        
        前快照 = self._快照列表[快照1]
        后快照 = self._快照列表[快照2]
        
        return {
            '内存增长': (后快照['当前内存'] - 前快照['当前内存']) / 1024,
            '峰值增长': (后快照['峰值内存'] - 前快照['峰值内存']) / 1024,
            '时间差': 后快照['时间'] - 前快照['时间']
        }


def 计算复杂度(函数: Callable, 输入大小列表: List[int], *参数) -> Dict[str, Any]:
    """计算算法复杂度"""
    结果 = []
    
    for 大小 in 输入大小列表:
        计时结果 = 多次计时(函数, 100, 大小, *参数)
        结果.append({
            '输入大小': 大小,
            '平均耗时': 计时结果.平均耗时,
            '总耗时': 计时结果.耗时
        })
    
    return 结果


def 对比性能(函数列表: List[Callable], 次数: int = 1000) -> List[Dict[str, Any]]:
    """对比多个函数的性能"""
    结果 = []
    
    for 函数 in 函数列表:
        计时结果 = 多次计时(函数, 次数)
        结果.append({
            '函数名': 函数.__name__,
            '总耗时': 计时结果.耗时,
            '平均耗时': 计时结果.平均耗时,
            '每秒调用': 1 / 计时结果.平均耗时
        })
    
    return sorted(结果, key=lambda x: x['平均耗时'])


def 性能装饰器(次数: int = 1000):
    """性能装饰器"""
    def 包装(函数):
        def 内部(*参数, **关键字参数):
            开始时间 = time.perf_counter()
            for _ in range(次数):
                结果 = 函数(*参数, **关键字参数)
            耗时 = time.perf_counter() - 开始时间
            
            print(f"性能测试 - {函数.__name__}:")
            print(f"  总耗时: {耗时:.6f}秒")
            print(f"  平均耗时: {(耗时/次数)*1000000:.2f}微秒")
            print(f"  每秒调用: {次数/耗时:.0f}次/秒")
            
            return 结果
        
        return 内部
    
    return 包装


def 内存使用() -> Dict[str, float]:
    """获取当前内存使用"""
    import psutil
    
    进程 = psutil.Process()
    内存信息 = 进程.memory_info()
    
    return {
        'rss': 内存信息.rss / 1024 / 1024,
        'vms': 内存信息.vms / 1024 / 1024,
        'shared': 内存信息.shared / 1024 / 1024,
        'text': 内存信息.text / 1024 / 1024,
        'lib': 内存信息.lib / 1024 / 1024,
        'data': 内存信息.data / 1024 / 1024,
        'dirty': 内存信息.dirty / 1024 / 1024
    }


def GC统计() -> Dict[str, Any]:
    """获取GC统计"""
    gc.collect()
    return {
        '对象数': len(gc.get_objects()),
        '垃圾回收次数': gc.get_stats(),
        '启用': gc.isenabled()
    }


def 打印系统性能信息():
    """打印系统性能信息"""
    import psutil
    
    print(f"\n{'='*60}")
    print(f"系统性能信息")
    print(f"{'='*60}")
    
    print(f"\nCPU信息:")
    print(f"  CPU核数: {psutil.cpu_count()}")
    print(f"  CPU使用率: {psutil.cpu_percent()}%")
    
    print(f"\n内存信息:")
    内存 = psutil.virtual_memory()
    print(f"  总内存: {内存.total/1024/1024/1024:.2f} GB")
    print(f"  可用内存: {内存.available/1024/1024/1024:.2f} GB")
    print(f"  已用内存: {内存.percent}%")
    
    print(f"\n进程内存:")
    进程 = psutil.Process()
    print(f"  RSS: {进程.memory_info().rss/1024/1024:.2f} MB")
    print(f"  VMS: {进程.memory_info().vms/1024/1024:.2f} MB")