"""
插件系统模块 - 动态加载、热更新

提供插件系统功能，包括：
- 插件动态加载
- 插件管理
- 热更新支持
- 插件生命周期管理
- 扩展点机制
"""
import importlib
import importlib.util
import inspect
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Type


class 插件异常(Exception):
    """插件异常"""
    pass


class 插件加载异常(插件异常):
    """插件加载异常"""
    pass


class 插件未找到异常(插件异常):
    """插件未找到异常"""
    pass


class 插件:
    """插件基类"""
    
    名称: str = ''
    版本: str = '1.0.0'
    描述: str = ''
    作者: str = ''
    
    def __init__(self):
        self._已启用 = False
    
    def 初始化(self):
        """插件初始化"""
        pass
    
    def 启动(self):
        """插件启动"""
        pass
    
    def 停止(self):
        """插件停止"""
        pass
    
    def 销毁(self):
        """插件销毁"""
        pass
    
    @property
    def 已启用(self) -> bool:
        """是否已启用"""
        return self._已启用


class 插件管理器:
    """插件管理器"""
    
    def __init__(self):
        self._插件字典: Dict[str, 插件] = {}
        self._插件类字典: Dict[str, Type[插件]] = {}
        self._插件路径列表: List[str] = []
        self._扩展点字典: Dict[str, List[Callable]] = {}
    
    def 添加插件路径(self, 路径: str):
        """添加插件路径"""
        if 路径 not in self._插件路径列表:
            self._插件路径列表.append(路径)
            if 路径 not in sys.path:
                sys.path.insert(0, 路径)
    
    def 加载插件(self, 插件名: str) -> 插件:
        """加载插件"""
        if 插件名 in self._插件字典:
            return self._插件字典[插件名]
        
        插件类 = self._查找插件类(插件名)
        if not 插件类:
            raise 插件未找到异常(f'插件 {插件名} 未找到')
        
        插件实例 = 插件类()
        插件实例.初始化()
        插件实例._已启用 = True
        插件实例.启动()
        
        self._插件字典[插件名] = 插件实例
        self._插件类字典[插件名] = 插件类
        
        return 插件实例
    
    def 卸载插件(self, 插件名: str):
        """卸载插件"""
        if 插件名 not in self._插件字典:
            raise 插件未找到异常(f'插件 {插件名} 未找到')
        
        插件实例 = self._插件字典[插件名]
        插件实例.停止()
        插件实例.销毁()
        插件实例._已启用 = False
        
        del self._插件字典[插件名]
    
    def 重新加载插件(self, 插件名: str) -> 插件:
        """重新加载插件（热更新）"""
        if 插件名 in self._插件字典:
            self.卸载插件(插件名)
        
        if 插件名 in sys.modules:
            模块 = sys.modules[插件名]
            importlib.reload(模块)
        
        return self.加载插件(插件名)
    
    def 获取插件(self, 插件名: str) -> Optional[插件]:
        """获取插件实例"""
        return self._插件字典.get(插件名)
    
    def 获取所有插件(self) -> Dict[str, 插件]:
        """获取所有已加载的插件"""
        return self._插件字典.copy()
    
    def 插件列表(self) -> List[str]:
        """获取插件名称列表"""
        return list(self._插件字典.keys())
    
    def 已加载(self, 插件名: str) -> bool:
        """检查插件是否已加载"""
        return 插件名 in self._插件字典
    
    def 启用插件(self, 插件名: str):
        """启用插件"""
        插件 = self.获取插件(插件名)
        if 插件 and not 插件.已启用:
            插件.启动()
            插件._已启用 = True
    
    def 禁用插件(self, 插件名: str):
        """禁用插件"""
        插件 = self.获取插件(插件名)
        if 插件 and 插件.已启用:
            插件.停止()
            插件._已启用 = False
    
    def 注册扩展点(self, 扩展点名: str, 回调函数: Callable):
        """注册扩展点"""
        if 扩展点名 not in self._扩展点字典:
            self._扩展点字典[扩展点名] = []
        self._扩展点字典[扩展点名].append(回调函数)
    
    def 触发扩展点(self, 扩展点名: str, *参数, **关键字参数) -> List[Any]:
        """触发扩展点"""
        结果列表 = []
        if 扩展点名 in self._扩展点字典:
            for 回调 in self._扩展点字典[扩展点名]:
                结果 = 回调(*参数, **关键字参数)
                结果列表.append(结果)
        return 结果列表
    
    def 加载目录(self, 目录路径: str) -> List[str]:
        """从目录加载所有插件"""
        已加载插件 = []
        if not os.path.isdir(目录路径):
            return 已加载插件
        
        self.添加插件路径(目录路径)
        
        for 文件名 in os.listdir(目录路径):
            if 文件名.endswith('.py') and not 文件名.startswith('_'):
                插件名 = 文件名[:-3]
                try:
                    self.加载插件(插件名)
                    已加载插件.append(插件名)
                except Exception:
                    pass
        
        return 已加载插件
    
    def _查找插件类(self, 插件名: str) -> Optional[Type[插件]]:
        """查找插件类"""
        try:
            模块 = importlib.import_module(插件名)
            
            for 名称 in dir(模块):
                对象 = getattr(模块, 名称)
                if (inspect.isclass(对象) and 
                    issubclass(对象, 插件) and 
                    对象 is not 插件):
                    return 对象
            
            return None
        except ImportError:
            return None
    
    def 销毁所有(self):
        """销毁所有插件"""
        for 插件名 in list(self._插件字典.keys()):
            try:
                self.卸载插件(插件名)
            except Exception:
                pass


class 扩展点:
    """扩展点装饰器"""
    
    def __init__(self, 名称: str):
        self.名称 = 名称
    
    def __call__(self, 函数):
        函数._扩展点 = self.名称
        return 函数


class 插件装饰器:
    """插件装饰器"""
    
    def __init__(self, 名称: str = '', 版本: str = '1.0.0', 描述: str = ''):
        self.名称 = 名称
        self.版本 = 版本
        self.描述 = 描述
    
    def __call__(self, 类):
        类.名称 = self.名称 or 类.__name__
        类.版本 = self.版本
        类.描述 = self.描述
        return 类


class 动态模块加载器:
    """动态模块加载器"""
    
    @staticmethod
    def 从文件加载(文件路径: str, 模块名: str = None) -> Any:
        """从文件加载模块"""
        if not os.path.exists(文件路径):
            raise 插件加载异常(f'文件不存在: {文件路径}')
        
        模块名 = 模块名 or os.path.splitext(os.path.basename(文件路径))[0]
        
        规范 = importlib.util.spec_from_file_location(模块名, 文件路径)
        if 规范 is None or 规范.loader is None:
            raise 插件加载异常(f'无法加载模块: {文件路径}')
        
        模块 = importlib.util.module_from_spec(规范)
        sys.modules[模块名] = 模块
        规范.loader.exec_module(模块)
        
        return 模块
    
    @staticmethod
    def 从字符串加载(代码: str, 模块名: str = '动态模块') -> Any:
        """从字符串加载模块"""
        模块 = type(sys)(模块名)
        sys.modules[模块名] = 模块
        
        exec(代码, 模块.__dict__)
        
        return 模块
    
    @staticmethod
    def 重新加载模块(模块名: str) -> Any:
        """重新加载模块"""
        if 模块名 in sys.modules:
            return importlib.reload(sys.modules[模块名])
        raise 插件未找到异常(f'模块 {模块名} 未加载')


class 热更新管理器:
    """热更新管理器"""
    
    def __init__(self):
        self._模块列表: List[str] = []
        self._文件时间戳: Dict[str, float] = {}
    
    def 监控模块(self, 模块名: str, 文件路径: str):
        """监控模块文件变化"""
        self._模块列表.append(模块名)
        self._文件时间戳[文件路径] = os.path.getmtime(文件路径)
    
    def 检查更新(self) -> List[str]:
        """检查更新"""
        更新列表 = []
        
        for 文件路径, 旧时间戳 in self._文件时间戳.items():
            try:
                新时间戳 = os.path.getmtime(文件路径)
                if 新时间戳 > 旧时间戳:
                    self._文件时间戳[文件路径] = 新时间戳
                    模块名 = os.path.splitext(os.path.basename(文件路径))[0]
                    更新列表.append(模块名)
            except OSError:
                pass
        
        return 更新列表
    
    def 自动更新(self) -> Dict[str, bool]:
        """自动更新"""
        结果 = {}
        更新的模块 = self.检查更新()
        
        for 模块名 in 更新的模块:
            try:
                动态模块加载器.重新加载模块(模块名)
                结果[模块名] = True
            except Exception:
                结果[模块名] = False
        
        return 结果


# 便捷函数
def 创建插件管理器() -> 插件管理器:
    """创建插件管理器"""
    return 插件管理器()


def 创建热更新管理器() -> 热更新管理器:
    """创建热更新管理器"""
    return 热更新管理器()


def 动态加载文件(文件路径: str, 模块名: str = None) -> Any:
    """从文件动态加载模块"""
    return 动态模块加载器.从文件加载(文件路径, 模块名)


def 动态加载代码(代码: str, 模块名: str = '动态模块') -> Any:
    """从代码动态加载模块"""
    return 动态模块加载器.从字符串加载(代码, 模块名)