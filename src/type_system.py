"""
段言（Duan）编程语言 - 类型系统定义

定义所有类型类、符号表和类型推断错误。
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field


# =============================================================================
# 增强类型系统定义
# =============================================================================

class Type:
    """类型基类"""
    pass

    def is_subtype_of(self, other: 'Type') -> bool:
        """检查当前类型是否为 other 的子类型"""
        if isinstance(other, AnyType):
            return True
        if type(self) == type(other):
            return self._same_type_check(other)
        return False

    def _same_type_check(self, other: 'Type') -> bool:
        """同类型时的检查"""
        return True


class NumberType(Type):
    """数字类型"""
    def __repr__(self):
        return "数"

    def _same_type_check(self, other: 'Type') -> bool:
        return isinstance(other, NumberType)


class StringType(Type):
    """字符串类型"""
    def __repr__(self):
        return "串"

    def _same_type_check(self, other: 'Type') -> bool:
        return isinstance(other, StringType)


class BooleanType(Type):
    """布尔类型"""
    def __repr__(self):
        return "布尔"

    def _same_type_check(self, other: 'Type') -> bool:
        return isinstance(other, BooleanType)


class NullType(Type):
    """空值类型"""
    def __repr__(self):
        return "空"

    def is_subtype_of(self, other: 'Type') -> bool:
        """空值可以赋值给可空类型或任意类型"""
        if isinstance(other, AnyType):
            return True
        if isinstance(other, OptionalTypeWrapper):
            return True
        return super().is_subtype_of(other)


class AnyType(Type):
    """任意类型（用于未推断出的类型）"""
    def __repr__(self):
        return "任意"

    def is_subtype_of(self, other: 'Type') -> bool:
        return True


class UnknownType(Type):
    """未知类型"""
    def __repr__(self):
        return "未知"

    def is_subtype_of(self, other: 'Type') -> bool:
        return True


@dataclass
class ListType(Type):
    """列表类型（带元素类型）"""
    element_type: Optional['Type'] = None

    def __repr__(self):
        return f"列表[{self.element_type}]" if self.element_type else "列表"

    def _same_type_check(self, other: 'Type') -> bool:
        if not isinstance(other, ListType):
            return False
        if self.element_type and other.element_type:
            return self.element_type.is_subtype_of(other.element_type)
        return True


@dataclass
class DictType(Type):
    """字典类型（带键值类型）"""
    key_type: Optional['Type'] = None
    value_type: Optional['Type'] = None

    def __repr__(self):
        if self.key_type and self.value_type:
            return f"字典[{self.key_type}: {self.value_type}]"
        return "字典"

    def _same_type_check(self, other: 'Type') -> bool:
        if not isinstance(other, DictType):
            return False
        k_ok = (not self.key_type) or (not other.key_type) or self.key_type.is_subtype_of(other.key_type)
        v_ok = (not self.value_type) or (not other.value_type) or self.value_type.is_subtype_of(other.value_type)
        return k_ok and v_ok


@dataclass
class ClassType(Type):
    """类类型"""
    class_name: str = ""

    def __repr__(self):
        return self.class_name

    def _same_type_check(self, other: 'Type') -> bool:
        return isinstance(other, ClassType) and self.class_name == other.class_name


@dataclass
class TypeParam(Type):
    """泛型类型参数"""
    name: str = ""
    constraint: Optional[Type] = None  # 上界约束

    def __repr__(self):
        return self.name

    def is_subtype_of(self, other: 'Type') -> bool:
        if isinstance(other, AnyType):
            return True
        if isinstance(other, TypeParam):
            return self.name == other.name
        if self.constraint:
            return self.constraint.is_subtype_of(other)
        return False


@dataclass
class GenericTypeInstance(Type):
    """泛型类型实例化（如 列表[数]）"""
    base_name: str = ""
    type_args: List[Type] = field(default_factory=list)

    def __repr__(self):
        args_str = ", ".join(str(a) for a in self.type_args)
        return f"{self.base_name}[{args_str}]"

    def _same_type_check(self, other: 'Type') -> bool:
        if not isinstance(other, GenericTypeInstance):
            return False
        if self.base_name != other.base_name:
            return False
        if len(self.type_args) != len(other.type_args):
            return False
        return all(sa.is_subtype_of(oa) for sa, oa in zip(self.type_args, other.type_args))


@dataclass
class EnumType(Type):
    """枚举/代数数据类型"""
    enum_name: str = ""
    variants: Dict[str, List[Type]] = field(default_factory=dict)  # 变体名 → 字段类型列表
    generic_params: List[str] = field(default_factory=list)

    def __repr__(self):
        return self.enum_name

    def get_variant_types(self, variant_name: str) -> Optional[List[Type]]:
        """获取变体的字段类型"""
        return self.variants.get(variant_name)

    def has_variant(self, variant_name: str) -> bool:
        return variant_name in self.variants

    def _enum_exhaustive_variants(self, matched_variants: Set[str]) -> Optional[str]:
        """检查枚举匹配是否穷尽，返回第一个未匹配的变体名"""
        for v in self.variants:
            if v not in matched_variants:
                return v
        return None


@dataclass
class OptionalTypeWrapper(Type):
    """可空类型包装（对应 T|空）"""
    inner_type: Type = field(default_factory=lambda: AnyType())

    def __repr__(self):
        return f"{self.inner_type}|空"

    def is_subtype_of(self, other: 'Type') -> bool:
        if isinstance(other, OptionalTypeWrapper):
            return self.inner_type.is_subtype_of(other.inner_type)
        if isinstance(other, AnyType):
            return True
        return False

    def unwrap(self) -> Type:
        """解包装获取内部类型"""
        return self.inner_type


@dataclass
class FunctionType(Type):
    """函数类型"""
    param_types: List[Type] = field(default_factory=list)
    return_type: Type = field(default_factory=lambda: AnyType())

    def __repr__(self):
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"

    def _same_type_check(self, other: 'Type') -> bool:
        if not isinstance(other, FunctionType):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        return all(p.is_subtype_of(op) for p, op in zip(self.param_types, other.param_types))


@dataclass
class TraitType(Type):
    """Trait 类型"""
    trait_name: str = ""
    methods: Dict[str, FunctionType] = field(default_factory=dict)

    def __repr__(self):
        return self.trait_name


@dataclass
class FutureType(Type):
    """Future/异步类型（对应 async 函数的返回值包装）"""
    inner_type: Type = field(default_factory=lambda: AnyType())

    def __repr__(self):
        return f"未来[{self.inner_type}]"

    def is_subtype_of(self, other: 'Type') -> bool:
        if isinstance(other, FutureType):
            return self.inner_type.is_subtype_of(other.inner_type)
        if isinstance(other, AnyType):
            return True
        return False


# =============================================================================
# 类型常量
# =============================================================================

TYPE_NUMBER = NumberType()
TYPE_STRING = StringType()
TYPE_BOOLEAN = BooleanType()
TYPE_NULL = NullType()
TYPE_UNKNOWN = UnknownType()
TYPE_ANY = AnyType()


# =============================================================================
# 符号表（带增强类型信息）
# =============================================================================

@dataclass
class TypedSymbol:
    """带类型信息的符号"""
    name: str
    symbol_type: str  # 'variable', 'function', 'class', 'parameter', 'enum', 'trait'
    data_type: Type
    scope_level: int
    is_mutable: bool = False  # 是否为可变变量
    is_nullable: bool = False  # 是否可空


class TypeSymbolTable:
    """带类型信息的符号表"""

    def __init__(self):
        self.scopes: List[Dict[str, TypedSymbol]] = [{}]
        self.current_level = 0
        # 泛型参数作用域（仅当前函数/类有效）
        self.generic_params: Dict[str, TypeParam] = {}

    def enter_scope(self):
        """进入新作用域"""
        self.scopes.append({})
        self.current_level += 1

    def exit_scope(self):
        """退出作用域"""
        if self.current_level > 0:
            self.scopes.pop()
            self.current_level -= 1

    def define(self, name: str, symbol_type: str, data_type: Type, is_mutable: bool = False) -> bool:
        """定义符号"""
        if name in self.scopes[self.current_level]:
            return False

        symbol = TypedSymbol(name, symbol_type, data_type, self.current_level, is_mutable)
        self.scopes[self.current_level][name] = symbol
        return True

    def lookup(self, name: str) -> Optional[TypedSymbol]:
        """查找符号（从当前作用域向外查找）"""
        for level in range(self.current_level, -1, -1):
            if name in self.scopes[level]:
                return self.scopes[level][name]
        return None

    def update_type(self, name: str, data_type: Type):
        """更新符号类型"""
        symbol = self.lookup(name)
        if symbol:
            symbol.data_type = data_type

    def define_generic_param(self, name: str, constraint: Optional[Type] = None):
        """定义泛型参数"""
        self.generic_params[name] = TypeParam(name, constraint)

    def resolve_type_param(self, name: str) -> Optional[Type]:
        """解析类型参数（优先从泛型参数中查找）"""
        return self.generic_params.get(name)

    def clear_generic_params(self):
        """清除泛型参数"""
        self.generic_params.clear()


# =============================================================================
# 类型推断错误
# =============================================================================

class TypeErrorInference(Exception):
    """类型推断错误"""
    def __init__(self, message: str, node=None):
        self.message = message
        self.node = node
        super().__init__(f"类型错误: {message}")


__all__ = [
    'Type', 'NumberType', 'StringType', 'BooleanType', 'NullType', 
    'AnyType', 'UnknownType', 'ListType', 'DictType', 'ClassType',
    'TypeParam', 'GenericTypeInstance', 'EnumType', 'OptionalTypeWrapper',
    'FunctionType', 'TraitType', 'FutureType',
    'TypedSymbol', 'TypeSymbolTable', 'TypeErrorInference',
    'TYPE_NUMBER', 'TYPE_STRING', 'TYPE_BOOLEAN', 'TYPE_NULL', 'TYPE_UNKNOWN', 'TYPE_ANY',
]