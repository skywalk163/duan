"""
类型系统增强模块 - 泛型、类型校验

提供增强的类型系统功能，包括：
- 运行时类型检查
- 泛型支持
- 类型校验装饰器
- 类型推断
- 接口/协议
"""
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from functools import wraps


class 类型校验失败异常(TypeError):
    """类型校验失败异常"""
    
    def __init__(self, 消息: str = '', 期望类型: type = None, 实际类型: type = None, 参数名: str = ''):
        super().__init__(消息)
        self.期望类型 = 期望类型
        self.实际类型 = 实际类型
        self.参数名 = 参数名


def 类型检查(值: Any, 期望类型: type, 参数名: str = '') -> bool:
    """检查值是否为指定类型"""
    if 期望类型 is Any:
        return True
    
    if isinstance(期望类型, type):
        if not isinstance(值, 期望类型):
            raise 类型校验失败异常(
                f'参数 "{参数名}" 类型错误: 期望 {期望类型.__name__}, 实际 {type(值).__name__}',
                期望类型, type(值), 参数名
            )
    elif hasattr(期望类型, '__origin__'):
        原始类型 = 期望类型.__origin__
        if not isinstance(值, 原始类型):
            raise 类型校验失败异常(
                f'参数 "{参数名}" 类型错误: 期望 {期望类型}, 实际 {type(值).__name__}',
                期望类型, type(值), 参数名
            )
    return True


def 类型校验(*参数类型, **关键字参数类型):
    """类型校验装饰器"""
    def 装饰器(函数):
        @wraps(函数)
        def 包装(*参数, **关键字参数):
            import inspect
            参数名列表 = inspect.signature(函数).parameters.keys()
            参数名列表 = list(参数名列表)
            
            for i, (参数值, 期望类型) in enumerate(zip(参数, 参数类型)):
                参数名 = 参数名列表[i] if i < len(参数名列表) else f'位置参数{i}'
                类型检查(参数值, 期望类型, 参数名)
            
            for 参数名, 期望类型 in 关键字参数类型.items():
                if 参数名 in 关键字参数:
                    类型检查(关键字参数[参数名], 期望类型, 参数名)
            
            return 函数(*参数, **关键字参数)
        return 包装
    return 装饰器


def 返回值类型检查(期望返回类型: type):
    """返回值类型检查装饰器"""
    def 装饰器(函数):
        @wraps(函数)
        def 包装(*参数, **关键字参数):
            结果 = 函数(*参数, **关键字参数)
            类型检查(结果, 期望返回类型, '返回值')
            return 结果
        return 包装
    return 装饰器


class 泛型类:
    """泛型类基类"""
    
    _类型参数 = None
    
    @classmethod
    def 指定类型(cls, *类型参数):
        """指定类型参数"""
        class 特化类(cls):
            _类型参数 = 类型参数
        
        特化类.__name__ = f'{cls.__name__}[{", ".join(t.__name__ for t in 类型参数)}]'
        return 特化类
    
    @classmethod
    def 获取类型参数(cls):
        """获取类型参数"""
        return cls._类型参数


class 泛型列表(泛型类):
    """泛型列表"""
    
    def __init__(self):
        self._列表: List[Any] = []
    
    def 添加(self, 元素):
        """添加元素（带类型检查）"""
        if self._类型参数:
            元素类型 = self._类型参数[0]
            if not isinstance(元素, 元素类型):
                raise 类型校验失败异常(
                    f'元素类型错误: 期望 {元素类型.__name__}, 实际 {type(元素).__name__}'
                )
        self._列表.append(元素)
    
    def 获取(self, 索引: int):
        """获取元素"""
        return self._列表[索引]
    
    def 长度(self) -> int:
        """获取长度"""
        return len(self._列表)
    
    def 列表(self) -> list:
        """获取原始列表"""
        return self._列表.copy()


class 泛型字典(泛型类):
    """泛型字典"""
    
    def __init__(self):
        self._字典: Dict[Any, Any] = {}
    
    def 设置(self, 键, 值):
        """设置键值对（带类型检查）"""
        if self._类型参数:
            键类型, 值类型 = self._类型参数
            if not isinstance(键, 键类型):
                raise 类型校验失败异常(
                    f'键类型错误: 期望 {键类型.__name__}, 实际 {type(键).__name__}'
                )
            if not isinstance(值, 值类型):
                raise 类型校验失败异常(
                    f'值类型错误: 期望 {值类型.__name__}, 实际 {type(值).__name__}'
                )
        self._字典[键] = 值
    
    def 获取(self, 键, 默认值=None):
        """获取值"""
        return self._字典.get(键, 默认值)
    
    def 包含键(self, 键) -> bool:
        """检查是否包含键"""
        return 键 in self._字典
    
    def 长度(self) -> int:
        """获取长度"""
        return len(self._字典)
    
    def 字典(self) -> dict:
        """获取原始字典"""
        return self._字典.copy()


class 可选类型:
    """可选类型"""
    
    def __init__(self, 值类型: type):
        self.值类型 = 值类型
    
    def 检查(self, 值) -> bool:
        """检查值是否符合类型"""
        if 值 is None:
            return True
        return isinstance(值, self.值类型)


class 联合类型:
    """联合类型"""
    
    def __init__(self, *类型列表: type):
        self.类型列表 = 类型列表
    
    def 检查(self, 值) -> bool:
        """检查值是否符合类型"""
        return any(isinstance(值, t) for t in self.类型列表)


class 接口:
    """接口基类"""
    
    @classmethod
    def 实现(cls, 接口):
        """检查是否实现了接口"""
        for 方法名 in dir(接口):
            if not 方法名.startswith('_'):
                if not hasattr(cls, 方法名):
                    return False
        return True


def 定义接口(接口名: str, 方法列表: List[str]) -> type:
    """定义接口"""
    接口类 = type(接口名, (), {
        '__接口__': True,
        '__方法列表__': 方法列表
    })
    return 接口类


def 实现接口(接口: type):
    """实现接口装饰器"""
    def 装饰器(类):
        方法列表 = getattr(接口, '__方法列表__', [])
        for 方法名 in 方法列表:
            if not hasattr(类, 方法名):
                raise NotImplementedError(f'类 {类.__name__} 未实现接口方法 {方法名}')
        类.__接口__ = getattr(类, '__接口__', []) + [接口.__name__]
        return 类
    return 装饰器


class 类型推断器:
    """类型推断器"""
    
    @staticmethod
    def 推断(值: Any) -> type:
        """推断值的类型"""
        return type(值)
    
    @staticmethod
    def 推断函数返回类型(函数: Callable) -> Optional[type]:
        """推断函数返回类型"""
        import inspect
        签名 = inspect.signature(函数)
        if 签名.return_annotation is not inspect.Parameter.empty:
            return 签名.return_annotation
        return None
    
    @staticmethod
    def 推断函数参数类型(函数: Callable) -> Dict[str, Optional[type]]:
        """推断函数参数类型"""
        import inspect
        签名 = inspect.signature(函数)
        类型字典 = {}
        for 参数名, 参数 in 签名.parameters.items():
            if 参数.annotation is not inspect.Parameter.empty:
                类型字典[参数名] = 参数.annotation
            else:
                类型字典[参数名] = None
        return 类型字典


class 数据类:
    """数据类基类"""
    
    def __init__(self, **字段):
        for 字段名, 字段值 in 字段.items():
            setattr(self, 字段名, 字段值)
    
    def __repr__(self) -> str:
        字段列表 = []
        for 字段名, 字段值 in self.__dict__.items():
            字段列表.append(f'{字段名}={repr(字段值)}')
        return f'{type(self).__name__}({", ".join(字段列表)})'
    
    def __eq__(self, 其他) -> bool:
        if not isinstance(其他, type(self)):
            return False
        return self.__dict__ == 其他.__dict__
    
    def 到字典(self) -> dict:
        """转换为字典"""
        return self.__dict__.copy()
    
    @classmethod
    def 从字典(cls, 数据: dict):
        """从字典创建"""
        return cls(**数据)


def 数据类装饰器(类):
    """数据类装饰器"""
    原始初始化 = 类.__init__
    
    @wraps(原始初始化)
    def 新初始化(self, **kwargs):
        for 字段名, 字段值 in kwargs.items():
            setattr(self, 字段名, 字段值)
    
    类.__init__ = 新初始化
    
    def 表示(self):
        字段列表 = []
        for 字段名, 字段值 in self.__dict__.items():
            字段列表.append(f'{字段名}={repr(字段值)}')
        return f'{type(self).__name__}({", ".join(字段列表)})'
    
    类.__repr__ = 表示
    
    def 等于(self, 其他):
        if not isinstance(其他, type(self)):
            return False
        return self.__dict__ == 其他.__dict__
    
    类.__eq__ = 等于
    
    return 类


class 枚举:
    """枚举基类"""
    
    @classmethod
    def 值列表(cls):
        """获取所有值"""
        结果 = []
        for 名称, 值 in cls.__dict__.items():
            if not 名称.startswith('_'):
                结果.append(值)
        return 结果
    
    @classmethod
    def 名称列表(cls):
        """获取所有名称"""
        结果 = []
        for 名称, 值 in cls.__dict__.items():
            if not 名称.startswith('_'):
                结果.append(名称)
        return 结果
    
    @classmethod
    def 包含值(cls, 值):
        """检查是否包含值"""
        return 值 in cls.值列表()
    
    @classmethod
    def 获取名称(cls, 值):
        """根据值获取名称"""
        for 名称, v in cls.__dict__.items():
            if v == 值 and not 名称.startswith('_'):
                return 名称
        return None


class 验证器:
    """验证器基类"""
    
    @staticmethod
    def 非空(值, 字段名: str = ''):
        """验证非空"""
        if 值 is None or (isinstance(值, str) and 值.strip() == ''):
            raise ValueError(f'{字段名} 不能为空')
    
    @staticmethod
    def 长度范围(值: str, 最小长度: int, 最大长度: int, 字段名: str = ''):
        """验证长度范围"""
        长度 = len(值)
        if 长度 < 最小长度 or 长度 > 最大长度:
            raise ValueError(f'{字段名} 长度必须在 {最小长度}-{最大长度} 之间')
    
    @staticmethod
    def 数值范围(值: float, 最小值: float, 最大值: float, 字段名: str = ''):
        """验证数值范围"""
        if 值 < 最小值 or 值 > 最大值:
            raise ValueError(f'{字段名} 必须在 {最小值}-{最大值} 之间')
    
    @staticmethod
    def 匹配正则(值: str, 模式: str, 字段名: str = ''):
        """验证正则匹配"""
        import re
        if not re.match(模式, 值):
            raise ValueError(f'{字段名} 格式不正确')
    
    @staticmethod
    def 电子邮箱(值: str, 字段名: str = '邮箱'):
        """验证邮箱格式"""
        模式 = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        验证器.匹配正则(值, 模式, 字段名)
    
    @staticmethod
    def 自定义(验证函数: Callable[[Any], bool], 错误消息: str = ''):
        """自定义验证"""
        def 验证(值, 字段名: str = ''):
            if not 验证函数(值):
                raise ValueError(错误消息 or f'{字段名} 验证失败')
        return 验证


# 便捷函数
def 检查类型(值: Any, 期望类型: type) -> bool:
    """检查类型"""
    try:
        类型检查(值, 期望类型)
        return True
    except 类型校验失败异常:
        return False


def 断言类型(值: Any, 期望类型: type, 消息: str = ''):
    """断言类型"""
    try:
        类型检查(值, 期望类型)
    except 类型校验失败异常 as e:
        raise AssertionError(消息 or str(e))


def 创建泛型列表(元素类型: type) -> 泛型列表:
    """创建泛型列表"""
    return 泛型列表.指定类型(元素类型)()


def 创建泛型字典(键类型: type, 值类型: type) -> 泛型字典:
    """创建泛型字典"""
    return 泛型字典.指定类型(键类型, 值类型)()