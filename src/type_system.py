"""
段言（Duan）编程语言 - 类型系统定义（Phase 1 增强版）

定义所有类型类、符号表、类型推断错误，以及：
- 基本类型（数、串、布尔、空、任意、未知）
- 复合类型（列表、字典、元组、集合）
- 泛型类型（类型变量、泛型实例、泛型定义）
- 函数类型
- 类类型（含泛型）
- 接口类型
- 代数数据类型（枚举）
- 类型替换与合一
"""

from typing import Dict, List, Optional, Any, Set, Tuple, Union
from dataclasses import dataclass, field
from copy import deepcopy


# =============================================================================
# 类型基类（启用快速类型匹配：_type_id 整数 ID + slots + 单例基本类型）
# =============================================================================

# 类型 ID 常量（对应每个子类）
TYPE_ID_NUMBER = 1
TYPE_ID_STRING = 2
TYPE_ID_BOOLEAN = 3
TYPE_ID_NULL = 4
TYPE_ID_ANY = 5
TYPE_ID_UNKNOWN = 6
TYPE_ID_OPTIONAL = 7
TYPE_ID_LIST = 8
TYPE_ID_DICT = 9
TYPE_ID_TUPLE = 10
TYPE_ID_SET = 11
TYPE_ID_FUNCTION = 12
TYPE_ID_TVAR = 13
TYPE_ID_GENERIC_INSTANCE = 14
TYPE_ID_GENERIC_DEF = 15
TYPE_ID_CLASS = 16
TYPE_ID_INTERFACE = 17
TYPE_ID_ENUM = 18
TYPE_ID_FUTURE = 19


class Type:
    """类型基类 —— 所有类型的公共接口"""
    __slots__ = ()
    _type_id = 0

    def is_subtype_of(self, other: 'Type') -> bool:
        """检查当前类型是否为 other 的子类型"""
        if other._type_id == TYPE_ID_ANY:
            return True
        if type(self) == type(other):
            return self._same_type_check(other)
        return False

    def _same_type_check(self, other: 'Type') -> bool:
        """同类型时的检查"""
        return True

    def collect_type_vars(self) -> Set['TypeVar']:
        """收集类型中出现的所有类型变量（返回 TypeVar 名称集合以保证 hashable）。"""
        return set()

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        """应用类型变量替换"""
        return self

    def resolve_type_vars(self) -> 'Type':
        return self

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self.__repr__()

    # 默认 hash 与相等性（子类型可按需覆盖）
    def __hash__(self):
        return hash(type(self).__name__)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return True


# =============================================================================
# 基本类型（单例化 + type_id 快速匹配）
# =============================================================================

class _SingletonType(Type):
    """只存在一个实例的类型基类 —— 基本类型都用此实现"""
    _instance: 'Type' = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return self.__class__._display_name


class NumberType(_SingletonType):
    """数字类型（数）"""
    _type_id = TYPE_ID_NUMBER
    _display_name = "数"

    def _same_type_check(self, other: 'Type') -> bool:
        return other._type_id == TYPE_ID_NUMBER


class StringType(_SingletonType):
    """字符串类型（串）"""
    _type_id = TYPE_ID_STRING
    _display_name = "串"

    def _same_type_check(self, other: 'Type') -> bool:
        return other._type_id == TYPE_ID_STRING


class BooleanType(_SingletonType):
    """布尔类型（布尔）"""
    _type_id = TYPE_ID_BOOLEAN
    _display_name = "布尔"

    def _same_type_check(self, other: 'Type') -> bool:
        return other._type_id == TYPE_ID_BOOLEAN


class NullType(_SingletonType):
    """空值类型（空）"""
    _type_id = TYPE_ID_NULL
    _display_name = "空"

    def is_subtype_of(self, other: 'Type') -> bool:
        """空值可以赋值给可空类型或任意类型"""
        oid = other._type_id
        if oid == TYPE_ID_ANY or oid == TYPE_ID_OPTIONAL or oid == TYPE_ID_NULL:
            return True
        return False


class AnyType(_SingletonType):
    """任意类型（任意）—— 未给出类型注解时使用"""
    _type_id = TYPE_ID_ANY
    _display_name = "任意"


class UnknownType(_SingletonType):
    """未知类型（未知）—— 无法静态推断的类型"""
    _type_id = TYPE_ID_UNKNOWN
    _display_name = "未知"

    def is_subtype_of(self, other: 'Type') -> bool:
        # 未知类型与任意类型都兼容，便于渐进式类型推断
        return True


@dataclass(frozen=True)
class OptionalTypeWrapper(Type):
    """可空类型包装（对应 T|空）"""
    inner_type: Type = field(default_factory=lambda: AnyType())
    _type_id = TYPE_ID_OPTIONAL

    def __repr__(self):
        return f"{self.inner_type}|空"

    def is_subtype_of(self, other: 'Type') -> bool:
        if other._type_id == TYPE_ID_OPTIONAL:
            return self.inner_type.is_subtype_of(other.inner_type)
        if other._type_id == TYPE_ID_ANY:
            return True
        return False

    def unwrap(self) -> Type:
        """解包装获取内部类型"""
        return self.inner_type

    def collect_type_vars(self) -> Set['TypeVar']:
        return self.inner_type.collect_type_vars()

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return OptionalTypeWrapper(self.inner_type.apply_substitution(subs))

    def resolve_type_vars(self) -> 'Type':
        return OptionalTypeWrapper(self.inner_type.resolve_type_vars())


# =============================================================================
# 复合类型
# =============================================================================

@dataclass
class ListType(Type):
    """列表类型（带元素类型）"""
    element_type: Optional[Type] = None
    _type_id = TYPE_ID_LIST

    def __repr__(self):
        if self.element_type:
            return f"列表[{self.element_type}]"
        return "列表"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_LIST:
            return False
        if self.element_type is None or other.element_type is None:
            return True
        return self.element_type.is_subtype_of(other.element_type)

    def collect_type_vars(self) -> Set['TypeVar']:
        if self.element_type:
            return self.element_type.collect_type_vars()
        return set()

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        if self.element_type:
            return ListType(self.element_type.apply_substitution(subs))
        return ListType(self.element_type)

    def resolve_type_vars(self) -> 'Type':
        if self.element_type:
            return ListType(self.element_type.resolve_type_vars())
        return ListType(self.element_type)


@dataclass
class DictType(Type):
    """字典类型（带键值类型）"""
    key_type: Optional[Type] = None
    value_type: Optional[Type] = None
    _type_id = TYPE_ID_DICT

    def __repr__(self):
        if self.key_type and self.value_type:
            return f"字典[{self.key_type}: {self.value_type}]"
        return "字典"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_DICT:
            return False
        k_ok = (self.key_type is None) or (other.key_type is None) or self.key_type.is_subtype_of(other.key_type)
        v_ok = (self.value_type is None) or (other.value_type is None) or self.value_type.is_subtype_of(other.value_type)
        return k_ok and v_ok

    def collect_type_vars(self) -> Set['TypeVar']:
        result: Set[TypeVar] = set()
        if self.key_type:
            result.update(self.key_type.collect_type_vars())
        if self.value_type:
            result.update(self.value_type.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return DictType(
            self.key_type.apply_substitution(subs) if self.key_type else None,
            self.value_type.apply_substitution(subs) if self.value_type else None,
        )

    def resolve_type_vars(self) -> 'Type':
        return DictType(
            self.key_type.resolve_type_vars() if self.key_type else None,
            self.value_type.resolve_type_vars() if self.value_type else None,
        )


@dataclass
class TupleType(Type):
    """元组类型（固定元素类型列表）"""
    element_types: List[Type] = field(default_factory=list)
    _type_id = TYPE_ID_TUPLE

    def __repr__(self):
        if self.element_types:
            return "元组[" + ", ".join(str(t) for t in self.element_types) + "]"
        return "元组"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_TUPLE:
            return False
        if len(self.element_types) != len(other.element_types):
            return False
        return all(a.is_subtype_of(b) for a, b in zip(self.element_types, other.element_types))

    def collect_type_vars(self) -> Set['TypeVar']:
        result: Set[TypeVar] = set()
        for t in self.element_types:
            result.update(t.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return TupleType([t.apply_substitution(subs) for t in self.element_types])

    def resolve_type_vars(self) -> 'Type':
        return TupleType([t.resolve_type_vars() for t in self.element_types])


@dataclass
class SetType(Type):
    """集合类型（带元素类型）"""
    element_type: Optional[Type] = None
    _type_id = TYPE_ID_SET

    def __repr__(self):
        if self.element_type:
            return f"集合[{self.element_type}]"
        return "集合"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_SET:
            return False
        if self.element_type is None or other.element_type is None:
            return True
        return self.element_type.is_subtype_of(other.element_type)

    def collect_type_vars(self) -> Set['TypeVar']:
        if self.element_type:
            return self.element_type.collect_type_vars()
        return set()

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        if self.element_type:
            return SetType(self.element_type.apply_substitution(subs))
        return SetType(self.element_type)

    def resolve_type_vars(self) -> 'Type':
        if self.element_type:
            return SetType(self.element_type.resolve_type_vars())
        return SetType(self.element_type)


# =============================================================================
# 函数类型
# =============================================================================

@dataclass
class FunctionType(Type):
    """函数类型（参数类型列表 + 返回类型）"""
    param_types: List[Type] = field(default_factory=list)
    return_type: Type = field(default_factory=lambda: AnyType())
    _type_id = TYPE_ID_FUNCTION

    def __repr__(self):
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_FUNCTION:
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        return all(p.is_subtype_of(op) for p, op in zip(self.param_types, other.param_types))

    def collect_type_vars(self) -> Set['TypeVar']:
        result: Set[TypeVar] = set()
        for t in self.param_types:
            result.update(t.collect_type_vars())
        result.update(self.return_type.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return FunctionType(
            [t.apply_substitution(subs) for t in self.param_types],
            self.return_type.apply_substitution(subs),
        )

    def resolve_type_vars(self) -> 'Type':
        return FunctionType(
            [t.resolve_type_vars() for t in self.param_types],
            self.return_type.resolve_type_vars(),
        )


# =============================================================================
# 泛型：类型变量 / 泛型实例 / 泛型定义
# =============================================================================

@dataclass
class TypeVar(Type):
    """泛型类型变量（如 T、U）

    支持可选的上界约束（constraint）。
    """
    name: str = ""
    constraint: Optional[Type] = None  # 上界约束：该类型变量必须是 constraint 的子类型
    _type_id = TYPE_ID_TVAR

    def __repr__(self):
        if self.constraint:
            return f"{self.name}<:{self.constraint}"
        return self.name

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_TVAR:
            return False
        if self.name != other.name:
            return False
        if self.constraint and other.constraint:
            return self.constraint.is_subtype_of(other.constraint)
        return True

    def is_subtype_of(self, other: 'Type') -> bool:
        if other._type_id == TYPE_ID_ANY:
            return True
        if other._type_id == TYPE_ID_TVAR:
            return self.name == other.name
        if self.constraint:
            return self.constraint.is_subtype_of(other)
        return False

    def collect_type_vars(self) -> Set['TypeVar']:
        result = {self}
        if self.constraint:
            result.update(self.constraint.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        if self.name in subs:
            return subs[self.name]
        new_constraint = self.constraint.apply_substitution(subs) if self.constraint else None
        if new_constraint is self.constraint:
            return self
        return TypeVar(self.name, new_constraint)

    def resolve_type_vars(self) -> 'Type':
        return self

    # hash / equality 以名称为核心，便于集合操作
    def __hash__(self):
        return hash(("TypeVar", self.name))

    def __eq__(self, other):
        if hasattr(other, '_type_id') and other._type_id == TYPE_ID_TVAR:
            return self.name == other.name
        return False


@dataclass
class GenericTypeInstance(Type):
    """泛型类型实例化（如 列表[数]、映射[T, U]）"""
    base_name: str = ""
    type_args: List[Type] = field(default_factory=list)
    _type_id = TYPE_ID_GENERIC_INSTANCE

    def __repr__(self):
        if not self.type_args:
            return self.base_name
        args_str = ", ".join(str(a) for a in self.type_args)
        return f"{self.base_name}[{args_str}]"

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_GENERIC_INSTANCE:
            return False
        if self.base_name != other.base_name:
            return False
        if len(self.type_args) != len(other.type_args):
            return False
        return all(a.is_subtype_of(b) for a, b in zip(self.type_args, other.type_args))

    def collect_type_vars(self) -> Set['TypeVar']:
        result: Set[TypeVar] = set()
        for t in self.type_args:
            result.update(t.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return GenericTypeInstance(
            self.base_name,
            [t.apply_substitution(subs) for t in self.type_args],
        )

    def resolve_type_vars(self) -> 'Type':
        return GenericTypeInstance(
            self.base_name,
            [t.resolve_type_vars() for t in self.type_args],
        )


@dataclass
class GenericTypeDef(Type):
    """泛型类型定义（如 列表<T>）

    仅用于符号表中记录泛型类/接口的定义。
    """
    base_name: str = ""
    param_names: List[str] = field(default_factory=list)
    _type_id = TYPE_ID_GENERIC_DEF

    def __repr__(self):
        if self.param_names:
            return f"{self.base_name}<{', '.join(self.param_names)}>"
        return self.base_name

    def collect_type_vars(self) -> Set['TypeVar']:
        return {TypeVar(n) for n in self.param_names}

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        new_names = [subs[n].__repr__() if hasattr(subs.get(n), '_type_id') and subs.get(n) is not None and subs[n]._type_id != TYPE_ID_TVAR else n for n in self.param_names]
        # 简化：泛型定义通常不参与替换
        return GenericTypeDef(self.base_name, new_names)

    def resolve_type_vars(self) -> 'Type':
        return self


# =============================================================================
# 类类型 & 接口类型
# =============================================================================

class ClassType(Type):
    """类类型（支持泛型实例化 + 接口实现跟踪）"""
    _type_id = TYPE_ID_CLASS

    def __init__(self, class_name: str = "", type_args: Optional[List[Type]] = None,
                 implements_interfaces: Optional[List['InterfaceType']] = None):
        self.class_name = class_name
        self.type_args: List[Type] = type_args if type_args is not None else []
        self.implements_interfaces: List['InterfaceType'] = implements_interfaces if implements_interfaces is not None else []

    def __repr__(self):
        if self.type_args:
            args = ", ".join(str(t) for t in self.type_args)
            return f"{self.class_name}[{args}]"
        return self.class_name

    def is_subtype_of(self, other: 'Type') -> bool:
        if other._type_id == TYPE_ID_ANY:
            return True
        if other._type_id == TYPE_ID_INTERFACE:
            # 类实现了该接口 → 是子类型
            return any(iface.interface_name == other.interface_name
                       for iface in self.implements_interfaces)
        if type(self) == type(other):
            return self._same_type_check(other)
        return False

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_CLASS:
            return False
        if self.class_name != other.class_name:
            return False
        if self.type_args and other.type_args:
            if len(self.type_args) != len(other.type_args):
                return False
            return all(a.is_subtype_of(b) for a, b in zip(self.type_args, other.type_args))
        return True

    def collect_type_vars(self) -> Set['TypeVar']:
        if not self.type_args:
            return set()
        result: Set[TypeVar] = set()
        for t in self.type_args:
            result.update(t.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        if not self.type_args:
            return self
        return ClassType(
            self.class_name,
            [t.apply_substitution(subs) for t in self.type_args],
            [iface.apply_substitution(subs) if iface._type_id == TYPE_ID_INTERFACE else iface
             for iface in self.implements_interfaces] if self.implements_interfaces else [],
        )

    def resolve_type_vars(self) -> 'Type':
        if not self.type_args:
            return self
        return ClassType(
            self.class_name,
            [t.resolve_type_vars() for t in self.type_args],
            self.implements_interfaces,
        )


@dataclass
class InterfaceType(Type):
    """接口类型（Phase 1 基础设施）"""
    interface_name: str = ""
    methods: Dict[str, 'FunctionType'] = field(default_factory=dict)
    type_args: Optional[List[Type]] = None
    _type_id = TYPE_ID_INTERFACE

    def __repr__(self):
        if self.type_args:
            args = ", ".join(str(t) for t in self.type_args)
            return f"{self.interface_name}[{args}]"
        return self.interface_name

    def _same_type_check(self, other: 'Type') -> bool:
        if other._type_id != TYPE_ID_INTERFACE:
            return False
        return self.interface_name == other.interface_name

    def __hash__(self):
        return hash(("InterfaceType", self.interface_name))

    def __eq__(self, other):
        if hasattr(other, '_type_id') and other._type_id == TYPE_ID_INTERFACE:
            return self.interface_name == other.interface_name
        return False

    def collect_type_vars(self) -> Set['TypeVar']:
        result: Set[TypeVar] = set()
        for ft in self.methods.values():
            result.update(ft.collect_type_vars())
        return result

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'InterfaceType':
        new_methods = {}
        for name, ft in self.methods.items():
            new_methods[name] = ft.apply_substitution(subs)
        return InterfaceType(self.interface_name, new_methods, self.type_args)

    def method_signature_matches(self, name: str, actual_ft: 'FunctionType') -> Optional[str]:
        """检查接口方法的签名是否与实现匹配。返回 None 表示匹配，返回字符串表示错误描述。"""
        if name not in self.methods:
            return None  # 方法不在接口中
        required_ft = self.methods[name]
        if len(actual_ft.param_types) != len(required_ft.param_types):
            return (
                f"方法 '{name}' 参数数量不匹配: "
                f"期望 {len(required_ft.param_types)} 个，实际 {len(actual_ft.param_types)} 个"
            )
        # 检查参数类型兼容性
        subs = TypeSubstitution()
        for i, (actual_t, required_t) in enumerate(zip(actual_ft.param_types, required_ft.param_types)):
            try:
                subs = unify(actual_t, required_t, subs)
            except UnificationError:
                return f"方法 '{name}' 第 {i} 个参数类型不匹配接口签名"
        try:
            unify(actual_ft.return_type, required_ft.return_type, subs)
        except UnificationError:
            return f"方法 '{name}' 返回类型不匹配接口签名"
        return None


# =============================================================================
# 代数数据类型（枚举）
# =============================================================================

@dataclass
class EnumType(Type):
    """枚举/代数数据类型"""
    enum_name: str = ""
    variants: Dict[str, List[Type]] = field(default_factory=dict)  # 变体名 → 字段类型列表
    generic_params: List[str] = field(default_factory=list)
    _type_id = TYPE_ID_ENUM

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

    def collect_type_vars(self) -> Set['TypeVar']:
        return {TypeVar(n) for n in self.generic_params}


# =============================================================================
# 异步 / Future 类型
# =============================================================================

@dataclass
class FutureType(Type):
    """Future/异步类型（对应 async 函数的返回值包装）"""
    inner_type: Type = field(default_factory=lambda: AnyType())
    _type_id = TYPE_ID_FUTURE

    def __repr__(self):
        return f"未来[{self.inner_type}]"

    def is_subtype_of(self, other: 'Type') -> bool:
        if other._type_id == TYPE_ID_FUTURE:
            return self.inner_type.is_subtype_of(other.inner_type)
        if other._type_id == TYPE_ID_ANY:
            return True
        return False

    def collect_type_vars(self) -> Set['TypeVar']:
        return self.inner_type.collect_type_vars()

    def apply_substitution(self, subs: 'TypeSubstitution') -> 'Type':
        return FutureType(self.inner_type.apply_substitution(subs))

    def resolve_type_vars(self) -> 'Type':
        return FutureType(self.inner_type.resolve_type_vars())


# =============================================================================
# 类型替换与合一
# =============================================================================

class TypeSubstitution:
    """类型变量 → 类型 的替换映射"""

    def __init__(self, mapping: Optional[Dict[str, Type]] = None):
        self.mapping: Dict[str, Type] = dict(mapping) if mapping else {}

    def __contains__(self, name: str) -> bool:
        return name in self.mapping

    def __getitem__(self, name: str) -> Type:
        return self.mapping[name]

    def __setitem__(self, name: str, t: Type) -> None:
        self.mapping[name] = t

    def get(self, name: str, default: Optional[Type] = None) -> Optional[Type]:
        return self.mapping.get(name, default)

    def bind(self, name: str, t: Type) -> 'TypeSubstitution':
        """添加一个绑定，返回自身以支持链式调用"""
        self.mapping[name] = t
        return self

    def compose(self, other: 'TypeSubstitution') -> 'TypeSubstitution':
        """组合两个替换：先应用 other，再应用 self（但这里简化）。"""
        result = TypeSubstitution()
        # 将 self 中的值使用 other 应用
        for name, t in self.mapping.items():
            result.mapping[name] = t.apply_substitution(other)
        # 合并 other
        for name, t in other.mapping.items():
            if name not in result.mapping:
                result.mapping[name] = t
        return result

    def items(self):
        return self.mapping.items()

    def clone(self) -> 'TypeSubstitution':
        return TypeSubstitution(dict(self.mapping))

    def __repr__(self) -> str:
        return f"TypeSubstitution({self.mapping})"

    def __bool__(self) -> bool:
        return bool(self.mapping)


class UnificationError(Exception):
    """类型合一失败"""

    def __init__(self, message: str, t1: Optional[Type] = None, t2: Optional[Type] = None):
        self.message = message
        self.t1 = t1
        self.t2 = t2
        if t1 is not None and t2 is not None:
            super().__init__(f"类型合一失败: {message} ({t1} ~ {t2})")
        else:
            super().__init__(f"类型合一失败: {message}")


def unify(t1: Type, t2: Type, subs: Optional[TypeSubstitution] = None) -> TypeSubstitution:
    """类型合一：尝试找到使 t1 和 t2 等价的类型变量替换。
    使用 _type_id 快速分派替代 isinstance 链。
    """
    if subs is None:
        subs = TypeSubstitution()

    # 先应用已有的替换
    t1 = t1.apply_substitution(subs)
    t2 = t2.apply_substitution(subs)

    id1 = t1._type_id
    id2 = t2._type_id

    # 任意类型 / 未知类型 —— 视为通配
    if id1 == TYPE_ID_ANY or id1 == TYPE_ID_UNKNOWN or id2 == TYPE_ID_ANY or id2 == TYPE_ID_UNKNOWN:
        return subs

    # 空类型
    if id1 == TYPE_ID_NULL or id2 == TYPE_ID_NULL:
        return subs

    # 类型变量
    if id1 == TYPE_ID_TVAR:
        return _unify_type_var(t1, t2, subs)
    if id2 == TYPE_ID_TVAR:
        return _unify_type_var(t2, t1, subs)

    # 相同基本类型（数/串/布尔）
    if id1 == id2:
        # 同类型同 ID 直接通过 —— 进一步检查（类名称/泛型参数等）由每个分支负责
        # 列表
        if id1 == TYPE_ID_LIST:
            if t1.element_type is None or t2.element_type is None:
                return subs
            return unify(t1.element_type, t2.element_type, subs)
        # 集合
        if id1 == TYPE_ID_SET:
            if t1.element_type is None or t2.element_type is None:
                return subs
            return unify(t1.element_type, t2.element_type, subs)
        # 字典
        if id1 == TYPE_ID_DICT:
            s = subs
            if t1.key_type and t2.key_type:
                s = unify(t1.key_type, t2.key_type, s)
            if t1.value_type and t2.value_type:
                s = unify(t1.value_type, t2.value_type, s)
            return s
        # 元组
        if id1 == TYPE_ID_TUPLE:
            if len(t1.element_types) != len(t2.element_types):
                raise UnificationError("元组长度不一致", t1, t2)
            s = subs
            for a, b in zip(t1.element_types, t2.element_types):
                s = unify(a, b, s)
            return s
        # 可空
        if id1 == TYPE_ID_OPTIONAL:
            return unify(t1.inner_type, t2.inner_type, subs)
        # 未来类型
        if id1 == TYPE_ID_FUTURE:
            return unify(t1.inner_type, t2.inner_type, subs)
        # 函数类型
        if id1 == TYPE_ID_FUNCTION:
            if len(t1.param_types) != len(t2.param_types):
                raise UnificationError("参数数量不一致", t1, t2)
            s = subs
            for a, b in zip(t1.param_types, t2.param_types):
                s = unify(a, b, s)
            return unify(t1.return_type, t2.return_type, s)
        # 泛型实例
        if id1 == TYPE_ID_GENERIC_INSTANCE:
            if t1.base_name != t2.base_name:
                raise UnificationError("泛型基名称不一致", t1, t2)
            if len(t1.type_args) != len(t2.type_args):
                raise UnificationError("泛型参数数量不一致", t1, t2)
            s = subs
            for a, b in zip(t1.type_args, t2.type_args):
                s = unify(a, b, s)
            return s
        # 类类型
        if id1 == TYPE_ID_CLASS:
            if t1.class_name != t2.class_name:
                raise UnificationError("类名称不一致", t1, t2)
            if t1.type_args and t2.type_args:
                if len(t1.type_args) != len(t2.type_args):
                    raise UnificationError("类泛型参数数量不一致", t1, t2)
                s = subs
                for a, b in zip(t1.type_args, t2.type_args):
                    s = unify(a, b, s)
                return s
            return subs
        # 接口类型
        if id1 == TYPE_ID_INTERFACE:
            if t1.interface_name == t2.interface_name:
                return subs
        # 枚举类型
        if id1 == TYPE_ID_ENUM:
            if t1.enum_name == t2.enum_name:
                return subs
        # 基本类型 (数/串/布尔/空) —— 已经同 ID，直接通过
        return subs

    # 不同 ID —— 尝试兼容模式
    # 泛型实例 ↔ 类类型同名
    if id1 == TYPE_ID_GENERIC_INSTANCE and id2 == TYPE_ID_CLASS:
        if t1.base_name == t2.class_name and t2.type_args is None:
            return subs
    if id2 == TYPE_ID_GENERIC_INSTANCE and id1 == TYPE_ID_CLASS:
        if t2.base_name == t1.class_name and t1.type_args is None:
            return subs

    # 泛型实例 ↔ 列表/字典/集合
    if id1 == TYPE_ID_GENERIC_INSTANCE and id2 == TYPE_ID_LIST:
        if t1.base_name in ("列表", "List") and len(t1.type_args) == 1:
            if t2.element_type:
                return unify(t1.type_args[0], t2.element_type, subs)
            return subs
    if id2 == TYPE_ID_GENERIC_INSTANCE and id1 == TYPE_ID_LIST:
        if t2.base_name in ("列表", "List") and len(t2.type_args) == 1:
            if t1.element_type:
                return unify(t2.type_args[0], t1.element_type, subs)
            return subs
    if id1 == TYPE_ID_GENERIC_INSTANCE and id2 == TYPE_ID_DICT:
        if t1.base_name in ("字典", "Map") and len(t1.type_args) == 2:
            s = subs
            if t2.key_type:
                s = unify(t1.type_args[0], t2.key_type, s)
            if t2.value_type:
                s = unify(t1.type_args[1], t2.value_type, s)
            return s
    if id2 == TYPE_ID_GENERIC_INSTANCE and id1 == TYPE_ID_DICT:
        if t2.base_name in ("字典", "Map") and len(t2.type_args) == 2:
            s = subs
            if t1.key_type:
                s = unify(t2.type_args[0], t1.key_type, s)
            if t1.value_type:
                s = unify(t2.type_args[1], t1.value_type, s)
            return s

    raise UnificationError("无法合一的类型", t1, t2)


def _unify_type_var(tv: TypeVar, other: Type, subs: TypeSubstitution) -> TypeSubstitution:
    """将类型变量 tv 与 other 合一（HM 风格：严格发生检查）"""
    # 若 tv 已有绑定，则使用绑定后的值
    if tv.name in subs:
        return unify(subs[tv.name], other, subs)

    oid = other._type_id
    # 自身合一（tv == tv）
    if oid == TYPE_ID_TVAR and other.name == tv.name:
        return subs

    # 检查约束（如果有）
    if tv.constraint and oid != TYPE_ID_ANY and oid != TYPE_ID_UNKNOWN and oid != TYPE_ID_TVAR:
        if not other.is_subtype_of(tv.constraint):
            raise UnificationError(
                f"类型变量 {tv.name} 有约束 {tv.constraint}，但 {other} 不满足",
                tv, other,
            )

    # 严格发生检查：若 tv 出现在 other 中（非自身名称），拒绝
    # 例如 T = list[T] 这样的无限类型在 HM 中是不允许的
    if oid != TYPE_ID_TVAR:
        fvs = other.collect_type_vars()
        for fv in fvs:
            if fv.name == tv.name:
                # 发生检查失败：tv 出现在 other 内部（非平凡场景）
                raise UnificationError(
                    f"发生检查失败：类型变量 {tv.name} 出现在 {other} 内部，"
                    f"导致无限类型（发生检查失败）",
                    tv, other,
                )

    new_subs = subs.clone()
    new_subs[tv.name] = other
    return new_subs


def free_type_vars(t: Type) -> Set[TypeVar]:
    """收集类型 t 中的自由类型变量（去重）"""
    return t.collect_type_vars()


def apply_substitution_to_type(t: Type, subs: TypeSubstitution) -> Type:
    """对类型应用替换（等价 t.apply_substitution(subs) 的公开入口）"""
    return t.apply_substitution(subs)


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
# 符号表（增强：支持泛型参数绑定、作用域嵌套）
# =============================================================================

@dataclass
class TypedSymbol:
    """带类型信息的符号"""
    name: str
    symbol_type: str  # 'variable', 'function', 'class', 'parameter', 'enum', 'trait', 'type_param'
    data_type: Type
    scope_level: int
    is_mutable: bool = False
    is_nullable: bool = False


class TypeSymbolTable:
    """带类型信息的符号表（增强版）

    支持：
    - 作用域嵌套（enter_scope / exit_scope）
    - 泛型参数绑定（define_generic_param / resolve_type_param）
    - 按作用域查找（从内到外）
    """

    def __init__(self):
        self.scopes: List[Dict[str, TypedSymbol]] = [{}]
        self.current_level = 0
        # 泛型参数（名称 → TypeVar），单独维护以便快速查找
        self.generic_params: Dict[str, TypeVar] = {}

    # ---- 作用域 ----
    def enter_scope(self):
        """进入新作用域"""
        self.scopes.append({})
        self.current_level += 1

    def exit_scope(self):
        """退出作用域"""
        if self.current_level > 0:
            self.scopes.pop()
            self.current_level -= 1

    # ---- 符号定义 ----
    def define(self, name: str, symbol_type: str, data_type: Type,
               is_mutable: bool = False, is_nullable: bool = False) -> bool:
        """定义符号到当前作用域。若已在当前作用域存在则返回 False。"""
        if name in self.scopes[self.current_level]:
            return False
        symbol = TypedSymbol(name, symbol_type, data_type, self.current_level,
                             is_mutable, is_nullable)
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

    # ---- 泛型参数 ----
    def define_generic_param(self, name: str, constraint: Optional[Type] = None):
        """定义泛型参数到当前作用域"""
        tv = TypeVar(name, constraint)
        self.generic_params[name] = tv
        # 同时在符号表中记录为 'type_param'
        self.define(name, 'type_param', tv)

    def resolve_type_param(self, name: str) -> Optional[Type]:
        """解析类型参数"""
        # 优先从单独的 generic_params 字典查找
        if name in self.generic_params:
            return self.generic_params[name]
        # 再从符号表查找（支持上层作用域的泛型参数）
        symbol = self.lookup(name)
        if symbol and symbol.symbol_type == 'type_param':
            return symbol.data_type
        return None

    def clear_generic_params(self):
        """清除泛型参数（在退出泛型作用域时调用）"""
        self.generic_params.clear()

    def get_generic_param_names(self) -> List[str]:
        """获取当前所有泛型参数名称"""
        return list(self.generic_params.keys())


# =============================================================================
# 类型推断错误
# =============================================================================

class TypeErrorInference(Exception):
    """类型推断错误"""

    def __init__(self, message: str, node=None):
        self.message = message
        self.node = node
        super().__init__(f"类型错误: {message}")


# =============================================================================
# 类型解析辅助
# =============================================================================

class TypeParser:
    """从字符串解析段言类型表达式。

    支持的类型表达式示例：
        数
        串
        列表[数]
        字典[串: 数]
        T                   （类型变量）
        列表[T]             （泛型实例）
        (数, 串) -> 布尔     （函数类型）
        T|空                （可空类型）
    """
    _BASIC_MAP = {
        '数': TYPE_NUMBER, '整数': TYPE_NUMBER, '浮点': TYPE_NUMBER,
        '串': TYPE_STRING, '字符串': TYPE_STRING,
        '布尔': TYPE_BOOLEAN, '逻辑': TYPE_BOOLEAN,
        '空': TYPE_NULL,
        '任意': TYPE_ANY, 'Any': TYPE_ANY,
        '未知': TYPE_UNKNOWN,
        '列表': ListType(),
        '字典': DictType(),
        '集合': SetType(),
        '元组': TupleType(),
    }
    _COMPOUND_KEYS = frozenset(['列表', 'List', '字典', 'Map', '映射', '集合', 'Set', '元组', 'Tuple'])

    def __init__(self, symbol_table: Optional[TypeSymbolTable] = None):
        self.symbol_table = symbol_table

    def parse(self, expr: str) -> Type:
        expr = expr.strip()
        if not expr:
            return TYPE_UNKNOWN
        # 可空类型
        if expr.endswith('|空'):
            inner = expr[:-2].strip()
            return OptionalTypeWrapper(self.parse(inner))
        # 函数类型 (t1, t2) -> t_ret
        if '->' in expr:
            idx = expr.index('->')
            params_part = expr[:idx].strip()
            return_part = expr[idx + 2:].strip()
            params = self._split_top_level(params_part, ',')
            param_types = [self.parse(p) for p in params]
            return FunctionType(param_types, self.parse(return_part))
        # 泛型/复合：基名[参数列表]
        if '[' in expr and expr.endswith(']'):
            bracket = expr.index('[')
            base = expr[:bracket].strip()
            args_str = expr[bracket + 1:-1].strip()
            if args_str:
                # 字典特殊处理：键: 值
                if base in ('字典', 'Map', '映射') and ':' in args_str:
                    # 顶层 ':' 切分
                    key_part, _, val_part = args_str.partition(':')
                    return DictType(self.parse(key_part), self.parse(val_part))
                # 常规逗号切分
                parts = self._split_top_level(args_str, ',')
                type_args = [self.parse(p) for p in parts]
            else:
                type_args = []
            # 映射到已知类型
            if base in ('列表', 'List'):
                elem = type_args[0] if type_args else None
                return ListType(elem)
            if base in ('集合', 'Set'):
                elem = type_args[0] if type_args else None
                return SetType(elem)
            if base in ('字典', 'Map'):
                k = type_args[0] if len(type_args) > 0 else None
                v = type_args[1] if len(type_args) > 1 else None
                return DictType(k, v)
            if base in ('元组', 'Tuple'):
                return TupleType(type_args)
            # 其他：泛型实例
            return GenericTypeInstance(base, type_args)
        # 元组 notation: (T1, T2, ...)  （且不含 ->）
        if expr.startswith('(') and expr.endswith(')') and '->' not in expr:
            inner = expr[1:-1].strip()
            if inner:
                parts = self._split_top_level(inner, ',')
                type_args = [self.parse(p) for p in parts]
                return TupleType(type_args)
            return TupleType([])
        # 基本类型（预构建映射，避免每次创建 dict）
        if expr in TypeParser._BASIC_MAP:
            return TypeParser._BASIC_MAP[expr]
        # 类型变量（大写开头或单字母）
        if self._looks_like_type_var(expr):
            # 优先从符号表解析
            if self.symbol_table:
                resolved = self.symbol_table.resolve_type_param(expr)
                if resolved:
                    return resolved
            return TypeVar(expr)
        # 否则：类/接口/枚举名称
        return ClassType(expr)

    def _looks_like_type_var(self, name: str) -> bool:
        """判断是否看起来像类型变量（单字母大写，或全大写标识符）"""
        if not name:
            return False
        if len(name) == 1 and name.isascii() and name.isupper():
            return True
        if len(name) <= 3 and name[0].isascii() and name[0].isupper():
            # 像 T、U、T1、U2、Key、Val 这类单/双字母
            return all(c.isascii() and (c.isupper() or c.isdigit()) for c in name)
        return False

    def _split_top_level(self, expr: str, sep: str) -> List[str]:
        """按顶层分隔符切分（忽略嵌套 [] () {} 内的分隔符）"""
        parts = []
        depth = 0
        current = []
        for ch in expr:
            if ch in '[({':
                depth += 1
                current.append(ch)
            elif ch in '])}':
                depth -= 1
                current.append(ch)
            elif ch == sep[0] and depth == 0:
                part = ''.join(current).strip()
                if part:
                    parts.append(part)
                current = []
            else:
                current.append(ch)
        tail = ''.join(current).strip()
        if tail:
            parts.append(tail)
        return parts


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # 类型基类
    'Type',
    # 基本类型
    'NumberType', 'StringType', 'BooleanType', 'NullType',
    'AnyType', 'UnknownType', 'OptionalTypeWrapper',
    # 复合类型
    'ListType', 'DictType', 'TupleType', 'SetType',
    # 函数类型
    'FunctionType',
    # 泛型
    'TypeVar', 'GenericTypeInstance', 'GenericTypeDef',
    # 类与接口
    'ClassType', 'InterfaceType',
    # 枚举 / 代数数据类型
    'EnumType',
    # 未来类型
    'FutureType',
    # 合一与替换
    'TypeSubstitution', 'UnificationError', 'unify',
    # 类型解析
    'TypeParser',
    # 符号表
    'TypedSymbol', 'TypeSymbolTable',
    # 异常
    'TypeErrorInference',
    # 常量
    'TYPE_NUMBER', 'TYPE_STRING', 'TYPE_BOOLEAN', 'TYPE_NULL', 'TYPE_UNKNOWN', 'TYPE_ANY',
]
