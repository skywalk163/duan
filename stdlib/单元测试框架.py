"""
单元测试框架模块 - 断言、测试套件、夹具

提供轻量级单元测试框架，包括：
- 测试用例定义
- 测试套件管理
- 断言方法
- 夹具机制
- 测试报告生成
"""
import sys
import traceback
import time
from typing import Callable, List, Dict, Any, Optional


class 测试结果:
    """测试结果类"""
    
    def __init__(self, 名称: str, 通过: bool, 耗时: float = 0, 错误: str = ''):
        self.名称 = 名称
        self.通过 = 通过
        self.耗时 = 耗时
        self.错误 = 错误


class 测试用例:
    """测试用例类"""
    
    def __init__(self, 名称: str, 函数: Callable):
        self.名称 = 名称
        self.函数 = 函数
    
    def 运行(self) -> 测试结果:
        """运行测试用例"""
        开始时间 = time.time()
        try:
            self.函数()
            耗时 = time.time() - 开始时间
            return 测试结果(self.名称, True, 耗时)
        except AssertionError as e:
            耗时 = time.time() - 开始时间
            return 测试结果(self.名称, False, 耗时, str(e))
        except Exception as e:
            耗时 = time.time() - 开始时间
            return 测试结果(self.名称, False, 耗时, traceback.format_exc())


class 测试套件:
    """测试套件类"""
    
    def __init__(self, 名称: str = ''):
        self.名称 = 名称
        self._测试用例列表: List[测试用例] = []
        self._前置夹具 = None
        self._后置夹具 = None
        self._测试类列表: List = []
    
    def 添加测试(self, 名称: str, 函数: Callable):
        """添加测试用例"""
        self._测试用例列表.append(测试用例(名称, 函数))
    
    def 添加测试类(self, 测试类):
        """添加测试类"""
        self._测试类列表.append(测试类)
    
    def 设置前置夹具(self, 函数: Callable):
        """设置前置夹具"""
        self._前置夹具 = 函数
    
    def 设置后置夹具(self, 函数: Callable):
        """设置后置夹具"""
        self._后置夹具 = 函数
    
    def 运行(self) -> List[测试结果]:
        """运行测试套件"""
        结果列表 = []
        
        if self._前置夹具:
            self._前置夹具()
        
        for 测试类 in self._测试类列表:
            实例 = 测试类()
            if hasattr(实例, '设置'):
                实例.设置()
            
            for 方法名 in dir(实例):
                if 方法名.startswith('测试_'):
                    方法 = getattr(实例, 方法名)
                    开始时间 = time.time()
                    try:
                        if hasattr(实例, '设置每测试'):
                            实例.设置每测试()
                        方法()
                        耗时 = time.time() - 开始时间
                        结果列表.append(测试结果(f'{测试类.__name__}.{方法名}', True, 耗时))
                    except AssertionError as e:
                        耗时 = time.time() - 开始时间
                        结果列表.append(测试结果(f'{测试类.__name__}.{方法名}', False, 耗时, str(e)))
                    except Exception as e:
                        耗时 = time.time() - 开始时间
                        结果列表.append(测试结果(f'{测试类.__name__}.{方法名}', False, 耗时, traceback.format_exc()))
            
            if hasattr(实例, '清理'):
                实例.清理()
        
        for 测试 in self._测试用例列表:
            结果列表.append(测试.运行())
        
        if self._后置夹具:
            self._后置夹具()
        
        return 结果列表


class 测试运行器:
    """测试运行器类"""
    
    def __init__(self):
        self._套件列表: List[测试套件] = []
    
    def 添加套件(self, 套件: 测试套件):
        """添加测试套件"""
        self._套件列表.append(套件)
    
    def 运行(self) -> Dict[str, Any]:
        """运行所有测试"""
        开始时间 = time.time()
        所有结果: List[测试结果] = []
        
        for 套件 in self._套件列表:
            所有结果.extend(套件.运行())
        
        总耗时 = time.time() - 开始时间
        通过数 = sum(1 for r in 所有结果 if r.通过)
        失败数 = len(所有结果) - 通过数
        
        return {
            '总测试数': len(所有结果),
            '通过数': 通过数,
            '失败数': 失败数,
            '总耗时': 总耗时,
            '结果列表': 所有结果,
            '通过率': 通过数 / len(所有结果) if 所有结果 else 0
        }
    
    def 打印报告(self):
        """打印测试报告"""
        结果 = self.运行()
        
        print(f"\n{'='*60}")
        print(f"测试报告")
        print(f"{'='*60}")
        print(f"总测试数: {结果['总测试数']}")
        print(f"通过: {结果['通过数']}")
        print(f"失败: {结果['失败数']}")
        print(f"通过率: {结果['通过率']:.2%}")
        print(f"总耗时: {结果['总耗时']:.3f}秒")
        print(f"{'='*60}")
        
        for 测试结果 in 结果['结果列表']:
            状态 = '✓' if 测试结果.通过 else '✗'
            耗时 = f' ({测试结果.耗时:.3f}秒)' if 测试结果.耗时 > 0.01 else ''
            print(f"{状态} {测试结果.名称}{耗时}")
            if not 测试结果.通过:
                print(f"   错误: {测试结果.错误}")
        
        print(f"{'='*60}")
        
        return 结果['失败数'] == 0


# 断言函数
def 断言为真(条件: bool, 消息: str = ''):
    """断言条件为真"""
    if not 条件:
        raise AssertionError(消息 or '断言失败: 条件不为真')


def 断言为假(条件: bool, 消息: str = ''):
    """断言条件为假"""
    if 条件:
        raise AssertionError(消息 or '断言失败: 条件不为假')


def 断言相等(实际值, 期望值, 消息: str = ''):
    """断言两个值相等"""
    if 实际值 != 期望值:
        raise AssertionError(消息 or f'断言失败: {实际值} != {期望值}')


def 断言不相等(实际值, 期望值, 消息: str = ''):
    """断言两个值不相等"""
    if 实际值 == 期望值:
        raise AssertionError(消息 or f'断言失败: {实际值} == {期望值}')


def 断言接近(实际值: float, 期望值: float, 公差: float = 0.0001, 消息: str = ''):
    """断言两个浮点数接近"""
    if abs(实际值 - 期望值) > 公差:
        raise AssertionError(消息 or f'断言失败: {实际值} 与 {期望值} 的差超过 {公差}')


def 断言包含(容器, 元素, 消息: str = ''):
    """断言容器包含元素"""
    if 元素 not in 容器:
        raise AssertionError(消息 or f'断言失败: {容器} 不包含 {元素}')


def 断言不包含(容器, 元素, 消息: str = ''):
    """断言容器不包含元素"""
    if 元素 in 容器:
        raise AssertionError(消息 or f'断言失败: {容器} 包含 {元素}')


def 断言为无(值, 消息: str = ''):
    """断言值为None"""
    if 值 is not None:
        raise AssertionError(消息 or f'断言失败: {值} 不为 None')


def 断言不为无(值, 消息: str = ''):
    """断言值不为None"""
    if 值 is None:
        raise AssertionError(消息 or '断言失败: 值为 None')


def 断言抛出异常(函数: Callable, 异常类型: type = Exception, 消息: str = ''):
    """断言函数抛出异常"""
    try:
        函数()
        raise AssertionError(消息 or '断言失败: 未抛出预期异常')
    except 异常类型:
        pass
    except Exception as e:
        raise AssertionError(消息 or f'断言失败: 抛出了错误的异常类型: {type(e).__name__}')


def 断言不抛出异常(函数: Callable, 消息: str = ''):
    """断言函数不抛出异常"""
    try:
        函数()
    except Exception as e:
        raise AssertionError(消息 or f'断言失败: 意外抛出异常: {e}')


def 断言实例(对象, 类型: type, 消息: str = ''):
    """断言对象是指定类型的实例"""
    if not isinstance(对象, 类型):
        raise AssertionError(消息 or f'断言失败: {type(对象).__name__} 不是 {类型.__name__} 的实例')


def 断言长度(序列, 期望长度: int, 消息: str = ''):
    """断言序列长度"""
    if len(序列) != 期望长度:
        raise AssertionError(消息 or f'断言失败: 长度 {len(序列)} != {期望长度}')


def 断言为空(序列, 消息: str = ''):
    """断言序列为空"""
    if len(序列) != 0:
        raise AssertionError(消息 or f'断言失败: 序列不为空')


def 断言不为空(序列, 消息: str = ''):
    """断言序列不为空"""
    if len(序列) == 0:
        raise AssertionError(消息 or '断言失败: 序列为空')


# 装饰器
def 测试(名称: str = ''):
    """测试装饰器"""
    def 包装(函数):
        函数._测试名称 = 名称 or function.__name__
        return 函数
    return 包装


def 夹具(类型: str = '前置'):
    """夹具装饰器"""
    def 包装(函数):
        函数._夹具类型 = 类型
        return 函数
    return 包装


# 便捷函数
def 创建测试套件(名称: str = '') -> 测试套件:
    """创建测试套件"""
    return 测试套件(名称)


def 创建测试运行器() -> 测试运行器:
    """创建测试运行器"""
    return 测试运行器()


def 运行测试(套件: 测试套件):
    """运行测试套件并打印报告"""
    运行器 = 创建测试运行器()
    运行器.添加套件(套件)
    return 运行器.打印报告()


def 主():
    """主函数"""
    运行器 = 创建测试运行器()
    
    for 模块 in sys.modules.values():
        for 名称 in dir(模块):
            对象 = getattr(模块, 名称)
            if isinstance(对象, type) and 对象.__name__.startswith('测试'):
                套件 = 创建测试套件(对象.__name__)
                套件.添加测试类(对象)
                运行器.添加套件(套件)
    
    运行器.打印报告()


if __name__ == '__main__':
    主()