"""
Mock工具模块 - 模拟对象、打桩

提供Mock和Stub功能，包括：
- Mock对象创建
- 方法打桩
- 调用记录
- 属性模拟
- 依赖隔离
"""
from typing import Any, Callable, Dict, List, Optional


class Mock调用记录:
    """Mock调用记录类"""
    
    def __init__(self, 方法名: str, 参数: tuple, 关键字参数: dict, 返回值: Any = None, 异常: Exception = None):
        self.方法名 = 方法名
        self.参数 = 参数
        self.关键字参数 = 关键字参数
        self.返回值 = 返回值
        self.异常 = 异常
        self.调用次数 = 1


class Mock对象:
    """Mock对象类"""
    
    def __init__(self, 目标类型: type = None):
        self._目标类型 = 目标类型
        self._调用记录: List[Mock调用记录] = []
        self._返回值映射: Dict[str, Any] = {}
        self._副作用映射: Dict[str, Callable] = {}
        self._属性映射: Dict[str, Any] = {}
        self._方法存根: Dict[str, Callable] = {}
    
    def 设置返回值(self, 方法名: str, 返回值: Any):
        """设置方法返回值"""
        self._返回值映射[方法名] = 返回值
    
    def 设置副作用(self, 方法名: str, 函数: Callable):
        """设置方法副作用"""
        self._副作用映射[方法名] = 函数
    
    def 设置属性(self, 名称: str, 值: Any):
        """设置属性值"""
        self._属性映射[名称] = 值
    
    def 设置方法存根(self, 方法名: str, 函数: Callable):
        """设置方法存根"""
        self._方法存根[方法名] = 函数
    
    def 获取调用记录(self, 方法名: str = None) -> List[Mock调用记录]:
        """获取调用记录"""
        if 方法名:
            return [r for r in self._调用记录 if r.方法名 == 方法名]
        return self._调用记录
    
    def 获取调用次数(self, 方法名: str = None) -> int:
        """获取调用次数"""
        if 方法名:
            return len(self.获取调用记录(方法名))
        return len(self._调用记录)
    
    def 重置调用记录(self):
        """重置调用记录"""
        self._调用记录 = []
    
    def 断言被调用(self, 方法名: str = None, 最少次数: int = 1):
        """断言方法被调用"""
        次数 = self.获取调用次数(方法名)
        if 次数 < 最少次数:
            方法描述 = f"'{方法名}' " if 方法名 else ''
            raise AssertionError(f"断言失败: 方法{方法描述}调用次数 {次数} < {最少次数}")
    
    def 断言未被调用(self, 方法名: str = None):
        """断言方法未被调用"""
        次数 = self.获取调用次数(方法名)
        if 次数 > 0:
            方法描述 = f"'{方法名}' " if 方法名 else ''
            raise AssertionError(f"断言失败: 方法{方法描述}被调用了 {次数} 次")
    
    def 断言被调用次数(self, 方法名: str = None, 期望次数: int = 1):
        """断言方法被调用指定次数"""
        次数 = self.获取调用次数(方法名)
        if 次数 != 期望次数:
            方法描述 = f"'{方法名}' " if 方法名 else ''
            raise AssertionError(f"断言失败: 方法{方法描述}调用次数 {次数} != {期望次数}")
    
    def 断言以参数调用(self, 方法名: str, *期望参数, **期望关键字参数):
        """断言方法以指定参数被调用"""
        记录 = self.获取调用记录(方法名)
        for r in 记录:
            if r.参数 == 期望参数 and r.关键字参数 == 期望关键字参数:
                return
        raise AssertionError(f"断言失败: 方法'{方法名}'未以指定参数调用")
    
    def __getattr__(self, 名称: str):
        """获取属性或方法"""
        if 名称 in self._属性映射:
            return self._属性映射[名称]
        
        if 名称 in self._方法存根:
            def 包装(*参数, **关键字参数):
                记录 = Mock调用记录(名称, 参数, 关键字参数)
                
                try:
                    返回值 = self._方法存根[名称](*参数, **关键字参数)
                    记录.返回值 = 返回值
                    self._调用记录.append(记录)
                    return 返回值
                except Exception as e:
                    记录.异常 = e
                    self._调用记录.append(记录)
                    raise
            
            return 包装
        
        def 模拟方法(*参数, **关键字参数):
            记录 = Mock调用记录(名称, 参数, 关键字参数)
            
            if 名称 in self._副作用映射:
                self._副作用映射[名称](*参数, **关键字参数)
            
            if 名称 in self._返回值映射:
                返回值 = self._返回值映射[名称]
                if callable(返回值):
                    返回值 = 返回值(*参数, **关键字参数)
                记录.返回值 = 返回值
            else:
                返回值 = Mock对象()
                记录.返回值 = 返回值
            
            self._调用记录.append(记录)
            return 返回值
        
        return 模拟方法


class Stub对象:
    """Stub对象类"""
    
    def __init__(self):
        self._方法存根: Dict[str, Callable] = {}
        self._属性值: Dict[str, Any] = {}
    
    def 设置方法(self, 方法名: str, 函数: Callable):
        """设置方法"""
        self._方法存根[方法名] = 函数
    
    def 设置属性(self, 名称: str, 值: Any):
        """设置属性"""
        self._属性值[名称] = 值
    
    def __getattr__(self, 名称: str):
        """获取属性或方法"""
        if 名称 in self._属性值:
            return self._属性值[名称]
        
        if 名称 in self._方法存根:
            return self._方法存根[名称]
        
        return Stub对象()


class 打桩器:
    """打桩器类"""
    
    def __init__(self):
        self._原始对象 = {}
        self._原始方法 = {}
    
    def 打桩对象(self, 模块, 对象名: str, 替代对象):
        """打桩对象"""
        self._原始对象[(模块, 对象名)] = getattr(模块, 对象名)
        setattr(模块, 对象名, 替代对象)
    
    def 打桩方法(self, 对象, 方法名: str, 替代方法):
        """打桩方法"""
        self._原始方法[(对象, 方法名)] = getattr(对象, 方法名)
        setattr(对象, 方法名, 替代方法)
    
    def 打桩属性(self, 对象, 属性名: str, 替代值):
        """打桩属性"""
        self._原始方法[(对象, 属性名)] = getattr(对象, 属性名)
        setattr(对象, 属性名, 替代值)
    
    def 恢复所有(self):
        """恢复所有打桩"""
        for (模块, 对象名), 原始对象 in self._原始对象.items():
            setattr(模块, 对象名, 原始对象)
        
        for (对象, 方法名), 原始方法 in self._原始方法.items():
            setattr(对象, 方法名, 原始方法)


# 便捷函数
def 创建Mock(目标类型: type = None) -> Mock对象:
    """创建Mock对象"""
    return Mock对象(目标类型)


def 创建Stub() -> Stub对象:
    """创建Stub对象"""
    return Stub对象()


def 创建打桩器() -> 打桩器:
    """创建打桩器"""
    return 打桩器()


def Mock(目标类型: type = None) -> Mock对象:
    """创建Mock对象（便捷函数）"""
    return Mock对象(目标类型)


def Stub() -> Stub对象:
    """创建Stub对象（便捷函数）"""
    return Stub对象()


def 打桩(模块, 对象名: str, 替代对象):
    """打桩对象（便捷函数）"""
    打桩器 = 创建打桩器()
    打桩器.打桩对象(模块, 对象名, 替代对象)
    return 打桩器


def 模拟返回(对象, 方法名: str, 返回值: Any):
    """模拟方法返回值"""
    if isinstance(对象, Mock对象):
        对象.设置返回值(方法名, 返回值)
    else:
        原始方法 = getattr(对象, 方法名)
        
        def 包装(*参数, **关键字参数):
            return 返回值
        
        setattr(对象, 方法名, 包装)
        return 原始方法


def 模拟异常(对象, 方法名: str, 异常: Exception):
    """模拟方法抛出异常"""
    if isinstance(对象, Mock对象):
        def 抛出异常(*参数, **关键字参数):
            raise 异常
        
        对象.设置返回值(方法名, 抛出异常)
    else:
        原始方法 = getattr(对象, 方法名)
        
        def 包装(*参数, **关键字参数):
            raise 异常
        
        setattr(对象, 方法名, 包装)
        return 原始方法


def 模拟副作用(对象, 方法名: str, 函数: Callable):
    """模拟方法副作用"""
    if isinstance(对象, Mock对象):
        对象.设置副作用(方法名, 函数)
    else:
        原始方法 = getattr(对象, 方法名)
        
        def 包装(*参数, **关键字参数):
            函数(*参数, **关键字参数)
            return 原始方法(*参数, **关键字参数)
        
        setattr(对象, 方法名, 包装)
        return 原始方法


def 验证调用(对象, 方法名: str, 期望次数: int = 1):
    """验证方法调用次数"""
    if isinstance(对象, Mock对象):
        对象.断言被调用次数(方法名, 期望次数)
    else:
        raise ValueError('对象必须是Mock对象')


def 验证未调用(对象, 方法名: str = None):
    """验证方法未被调用"""
    if isinstance(对象, Mock对象):
        对象.断言未被调用(方法名)
    else:
        raise ValueError('对象必须是Mock对象')


class Mock上下文管理器:
    """Mock上下文管理器"""
    
    def __init__(self, 模块, 对象名: str, 替代对象):
        self._模块 = 模块
        self._对象名 = 对象名
        self._替代对象 = 替代对象
        self._原始对象 = None
    
    def __enter__(self):
        """进入上下文"""
        self._原始对象 = getattr(self._模块, self._对象名)
        setattr(self._模块, self._对象名, self._替代对象)
        return self._替代对象
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        setattr(self._模块, self._对象名, self._原始对象)


def Mock上下文(模块, 对象名: str, 替代对象) -> Mock上下文管理器:
    """创建Mock上下文管理器"""
    return Mock上下文管理器(模块, 对象名, 替代对象)


class 属性Mock:
    """属性Mock"""
    
    def __init__(self, 值: Any = None, 可设置: bool = True):
        self._值 = 值
        self._可设置 = 可设置
        self._获取次数 = 0
        self._设置次数 = 0
    
    @property
    def 值(self):
        """获取值"""
        self._获取次数 += 1
        return self._值
    
    @值.setter
    def 值(self, 新值):
        """设置值"""
        if not self._可设置:
            raise AttributeError('属性不可设置')
        self._设置次数 += 1
        self._值 = 新值
    
    def 获取获取次数(self) -> int:
        """获取获取次数"""
        return self._获取次数
    
    def 获取设置次数(self) -> int:
        """获取设置次数"""
        return self._设置次数
    
    def 重置计数(self):
        """重置计数"""
        self._获取次数 = 0
        self._设置次数 = 0