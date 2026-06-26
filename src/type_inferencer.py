"""
段言（Duan）编程语言 - 增强类型推断器（Phase 1 版本）

特点：
- 完整的类型系统：基本类型、复合类型、泛型类型、类类型、接口类型
- 基于合一（unification）的类型变量解析
- 泛型段落（函数）的类型参数推断
- 泛型类实例化
- 局部变量类型推断
- 函数返回类型推断
"""

import sys
import os
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field

# 统一类型系统（Phase 1 增强版）
from type_system import (
    Type, NumberType, StringType, BooleanType, NullType,
    AnyType, UnknownType, OptionalTypeWrapper,
    ListType, DictType, TupleType, SetType,
    FunctionType, TypeVar, GenericTypeInstance, GenericTypeDef,
    ClassType, InterfaceType, EnumType, FutureType,
    TypeSubstitution, UnificationError, unify, TypeParser,
    TypedSymbol, TypeSymbolTable, TypeErrorInference,
    TYPE_NUMBER, TYPE_STRING, TYPE_BOOLEAN, TYPE_NULL, TYPE_UNKNOWN, TYPE_ANY,
)

# 导入统一 AST 节点定义
from ast_nodes import (
    VariableDeclaration, Assignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    TryStatement, ThrowStatement, PrintStatement, ExpressionStatement,
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Identifier, SegmentName, BinaryOp, UnaryOp, FunctionCall,
    PropertyAccess, IndexAccess, ListLiteral, DictLiteral, DictEntry,
    NewExpression, SelfReference, SegmentDefinition, ClassDefinition,
    MethodDefinition, ConstructorDefinition, Parameter,
    Module, ListComprehension, LambdaExpression, StringInterpolation,
    ConditionalExpression, PipeExpression, MatchStatement, MatchCase, MatchPattern,
    AwaitExpression, DeferStatement, AsyncScope,
    EnumDefinition, EnumVariant, DataTypeField,
    TraitDefinition, TraitMethodSignature, TraitImplementation,
    TypeAlias, OptionalType as ASTOptionalType, UnwrapExpression,
)


# =============================================================================
# 辅助：检查节点实例
# =============================================================================

def is_instance(node, class_name: str) -> bool:
    """检查节点类型（通过名称检查，支持多个模块）"""
    if node is None:
        return False
    return type(node).__name__ == class_name


# =============================================================================
# 类型推断器
# =============================================================================

@dataclass
class InferenceResult:
    """单个表达式的推断结果（类型 + 相关的替换）"""
    inferred_type: Type
    substitution: TypeSubstitution = field(default_factory=TypeSubstitution)


class TypeInferencer:
    """段言增强类型推断器（Phase 1 版本）"""

    def __init__(self):
        self.symbol_table = TypeSymbolTable()
        self.type_cache: Dict[int, Type] = {}
        self.errors: List[str] = []

        # 注册内置类型
        self._init_builtin_types()

        # 当前正在推断的函数返回类型
        self._current_return_type: Optional[Type] = None

        # 是否在异步函数中
        self._in_async_function: bool = False

        # 已知的枚举定义（名称 → EnumType）
        self.enum_defs: Dict[str, EnumType] = {}

        # 已知的 trait/接口定义（名称 → InterfaceType/TraitType）
        self.trait_defs: Dict[str, InterfaceType] = {}

        # 泛型类定义：名称 → 泛型参数名列表
        self.generic_class_defs: Dict[str, List[str]] = {}

        # 泛型段落定义：名称 → 泛型参数名列表
        self.generic_segment_defs: Dict[str, List[str]] = {}

        # 泛型类实例化记录（名称 → 类型参数列表）—— 用于辅助测试
        self.generic_class_instances: Dict[str, List[Type]] = {}

        # 方法预扫描缓存：(类名, 方法名) → FunctionType
        self._method_pre_scan_cache: Dict[Tuple[str, str], FunctionType] = {}

        # HM 推断阶段：在段体推断期间累积的替换（用于反馈到段签名）
        self._hm_subs: Optional[TypeSubstitution] = None

        # trait 实现（(trait名, 类型名) → 方法名 → FunctionType）
        self.trait_impls: Dict[Tuple[str, str], Dict[str, FunctionType]] = {}

        # 类型字符串解析器
        self.type_parser = TypeParser(self.symbol_table)

        # 当前正在处理的 module（用于类定义查找）
        self.module = None

        # 收集函数体中的返回语句类型（用于推断未声明的返回类型）
        self._collected_return_types: List[Type] = []

        # 解构赋值跟踪（解构 (x, y) = expr）
        self._destructure_target: Optional[Tuple[str, ...]] = None

    # ---- 内置类型初始化 ----
    def _init_builtin_types(self):
        """初始化内置类型"""
        self._builtin_type_names = {'数', '串', '布尔', '空', '列表', '字典', '任意', '元组', '集合'}

    # ---- 类型字符串解析 ----
    def _parse_type_string(self, type_str) -> Type:
        """将类型字符串解析为 Type 对象"""
        if type_str is None:
            return TYPE_ANY
        return self.type_parser.parse(type_str)

    # ---- 注册枚举 ----
    def register_enum(self, enum_def: EnumDefinition):
        """注册枚举类型"""
        variants = {}
        for variant in enum_def.variants:
            field_types = [self._parse_type_string(f.type_annotation) for f in variant.fields]
            variants[variant.name] = field_types

        enum_type = EnumType(
            enum_name=enum_def.name,
            variants=variants,
            generic_params=list(getattr(enum_def, 'generic_params', []) or []),
        )
        self.enum_defs[enum_def.name] = enum_type
        self.symbol_table.define(enum_def.name, 'enum', enum_type)

    # ---- 注册 Trait/接口 ----
    def register_trait(self, trait_def: TraitDefinition):
        """注册 trait 定义"""
        methods = {}
        for method in trait_def.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            methods[method.name] = FunctionType(param_types, return_type)

        iface = InterfaceType(interface_name=trait_def.name, methods=methods)
        self.trait_defs[trait_def.name] = iface

    # ---- 注册 InterfaceDefinition（中文命名） ----
    def register_interface(self, iface_def):
        """注册接口定义（InterfaceDefinition 节点）"""
        methods = {}
        for method in iface_def.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            methods[method.name] = FunctionType(param_types, return_type)

        iface = InterfaceType(interface_name=iface_def.name, methods=methods)
        self.trait_defs[iface_def.name] = iface

    # ---- 注册 Trait/接口 实现 ----
    def register_trait_impl(self, impl: TraitImplementation):
        """注册 trait 实现并检查方法是否完整且签名匹配"""
        key = (impl.trait_name, impl.type_name)
        methods = {}
        for method in impl.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            methods[method.name] = FunctionType(param_types, return_type)
        self.trait_impls[key] = methods

        # 类型实现 trait 检查（方法存在性 + 签名匹配）
        if impl.trait_name in self.trait_defs:
            required = self.trait_defs[impl.trait_name]
            for method_name, func_type in required.methods.items():
                if method_name not in methods:
                    self.errors.append(
                        f"类型 '{impl.type_name}' 未实现接口 '{impl.trait_name}' "
                        f"的必需方法 '{method_name}'"
                    )
                else:
                    # 签名匹配检查
                    actual_ft = methods[method_name]
                    err = required.method_signature_matches(method_name, actual_ft)
                    if err:
                        self.errors.append(f"类型 '{impl.type_name}' 实现接口 '{impl.trait_name}': {err}")

    # ---- 主推断入口（HM 两阶段） ----
    def infer(self, module: Module) -> Dict[int, Type]:
        """对整个模块进行类型推断（HM 风格两阶段：预扫描 + 推断 + 泛化）"""
        self.type_cache = {}
        self.symbol_table = TypeSymbolTable()
        self.type_parser = TypeParser(self.symbol_table)
        self.errors = []
        self.enum_defs = {}
        self.trait_defs = {}
        self.trait_impls = {}
        self.generic_class_defs = {}
        self.generic_segment_defs = {}
        self.generic_class_instances = {}
        self._method_pre_scan_cache = {}
        self._hm_subs = None
        self.module = module

        # 阶段 0：注册所有类型定义（枚举、trait、类）
        self._scan_type_definitions(module)

        # 阶段 1：注册 trait 实现
        for impl in getattr(module, 'trait_impls', []):
            self.register_trait_impl(impl)

        # 阶段 2：预扫描所有段/方法定义（用 TypeVar 填充未知类型）
        self._pre_scan_definitions(module)

        # 阶段 3：HM 风格推断所有函数体（合一 + 泛化）
        self._hm_infer_module(module)

        # 阶段 4：推断顶层语句（独立的 HM 上下文，不污染段签名）
        self._hm_subs = None
        if hasattr(module, 'statements'):
            for stmt in module.statements:
                self._infer_statement(stmt)

        return self.type_cache

    # ---- 工具：根据类名查找类定义 ----
    def _lookup_class_def(self, name: str) -> Optional['ClassDefinition']:
        """在当前 module 中查找指定名称的类定义"""
        if self.module is None:
            return None
        for cls in getattr(self.module, 'classes', []) or []:
            if getattr(cls, 'name', None) == name:
                return cls
        return None

    # ---- 扫描阶段 ----
    def _scan_type_definitions(self, module: Module):
        """扫描所有类型定义（建立符号表）"""
        # 注册枚举
        for enum_def in getattr(module, 'enums', []):
            self.register_enum(enum_def)

        # 注册 trait/接口（包括 InterfaceDefinition 中文命名）
        for trait_def in getattr(module, 'trait_defs', []):
            self.register_trait(trait_def)
        for iface_def in getattr(module, 'interfaces', []):
            self.register_interface(iface_def)

        # 注册类（包括泛型类）
        if hasattr(module, 'classes'):
            for cls in module.classes:
                class_type = ClassType(cls.name)
                self.symbol_table.define(cls.name, 'class', class_type)
                # 记录泛型参数
                generic_params = getattr(cls, 'generic_params', None) or []
                if generic_params:
                    self.generic_class_defs[cls.name] = list(generic_params)

        # 注册段落/函数（包括泛型段落）
        if hasattr(module, 'segments'):
            for segment in module.segments:
                generic_params = getattr(segment, 'generic_params', None) or []
                if generic_params:
                    self.generic_segment_defs[segment.name] = list(generic_params)
                # 占位：等待进入推断阶段后再填入具体类型
                self.symbol_table.define(segment.name, 'function', TYPE_UNKNOWN)

    # ---- HM 阶段 1：预扫描所有定义，注册类型签名 ----
    def _pre_scan_definitions(self, module: Module):
        """第一阶段：扫描所有顶层段/类/方法定义，为每个注册初始类型签名。

        未标注的参数/返回类型使用 TypeVar 填充，便于后续通过合一推断。
        顶层语句中的段定义也一并扫描，确保相互调用能找到签名。
        """
        # 统一收集所有需要预扫描的段：module.segments + statements 中的段
        def _iter_segments():
            for seg in getattr(module, 'segments', []) or []:
                yield seg
            for stmt in getattr(module, 'statements', []) or []:
                if isinstance(stmt, SegmentDefinition):
                    yield stmt

        for segment in _iter_segments():
            # 显式的泛型参数名
            explicit_generics = list(getattr(segment, 'generic_params', None) or [])

            param_types: List[Type] = []
            tv_counter = [0]

            def _new_tvar(suggest: Optional[str] = None) -> TypeVar:
                if suggest and suggest not in [t.name for t in param_types if isinstance(t, TypeVar)]:
                    return TypeVar(suggest)
                name = f"T{tv_counter[0]}"
                tv_counter[0] += 1
                return TypeVar(name)

            for i, param in enumerate(segment.parameters):
                if param.type_annotation:
                    try:
                        param_types.append(self._parse_type_string(param.type_annotation))
                    except Exception:
                        param_types.append(_new_tvar())
                else:
                    # 尝试使用显式泛型参数名（按顺序）
                    if i < len(explicit_generics):
                        param_types.append(TypeVar(explicit_generics[i]))
                    else:
                        param_types.append(_new_tvar())

            # 返回类型：有标注用标注，否则用 TypeVar('R')
            if segment.return_type:
                try:
                    ret_type = self._parse_type_string(segment.return_type)
                except Exception:
                    ret_type = TypeVar('R')
            else:
                ret_type = TypeVar('R')

            func_type = FunctionType(param_types, ret_type)
            # 注册或覆盖符号
            existing = self.symbol_table.lookup(segment.name)
            if existing and existing.data_type is TYPE_UNKNOWN:
                existing.data_type = func_type
            else:
                self.symbol_table.define(segment.name, 'function', func_type)

        # 扫描类中的方法（用于类内部的方法调用推断）
        for cls in getattr(module, 'classes', []) or []:
            for method in getattr(cls, 'methods', []) or []:
                m_param_types: List[Type] = []
                for i, mp in enumerate(method.parameters):
                    if mp.type_annotation:
                        try:
                            m_param_types.append(self._parse_type_string(mp.type_annotation))
                            continue
                        except Exception:
                            pass
                    m_param_types.append(TypeVar(f"a{i}"))
                if method.return_type:
                    try:
                        m_ret = self._parse_type_string(method.return_type)
                    except Exception:
                        m_ret = TypeVar('R')
                else:
                    m_ret = TypeVar('R')
                # 记录在一个简单字典中，供 PropertyAccess 查找（可选）
                self._method_pre_scan_cache[(cls.name, method.name)] = FunctionType(m_param_types, m_ret)

    # ---- HM 阶段 2：推断函数体并泛化 ----
    def _hm_infer_module(self, module: Module):
        """第二阶段：HM 风格推断所有段体并进行 let-polymorphism 泛化。

        关键设计：
          * 预扫描阶段给每个段注册了「泛型占位」签名。
          * 段之间可能存在相互调用，因此需要多次迭代：
              迭代 1：先推断所有段体（此时调用者可能看到的是被调用者的 pre 类型）
              迭代 2：重新推断调用者的段体（此时调用者能看到被调用者已推断的具体类型）
          * 在写入符号表时，保留最泛化的版本，以便后续 FunctionCall 实例化。
          * ⭐ type_cache 在段体推断期间必须独立管理，避免旧结果污染。
          * 同时处理所有类定义（包括接口实现验证）。
        """
        def _iter_segments():
            for seg in getattr(module, 'segments', []):
                yield seg
            for stmt in getattr(module, 'statements', []):
                if isinstance(stmt, SegmentDefinition):
                    yield stmt

        # ---- 先推断枚举、trait 定义（内部一致性检查）----
        for enum_def in getattr(module, 'enums', []) or []:
            self._infer_enum_def(enum_def)

        for trait_def in getattr(module, 'trait_defs', []) or []:
            self._infer_trait_def(trait_def)

        # ---- 处理类定义（包括接口实现验证）----
        for cls in getattr(module, 'classes', []) or []:
            self._infer_class(cls)

        # ---- 处理段定义 ----
        all_segs = list(_iter_segments())

        for _ in range(2):
            for segment in all_segs:
                sym = self.symbol_table.lookup(segment.name)
                if sym is None or not isinstance(sym.data_type, FunctionType):
                    continue

                pre_func_type = sym.data_type

                # ⭐ 保存并重置 type_cache，避免上一轮段体推断污染本论推断
                saved_cache = self.type_cache
                self.type_cache = {}

                self.symbol_table.enter_scope()
                self._hm_subs = TypeSubstitution()

                for param, ptype in zip(segment.parameters, pre_func_type.param_types):
                    self.symbol_table.define(param.name, 'parameter', ptype)

                self._current_return_type = pre_func_type.return_type
                self._collected_return_types = []
                try:
                    for body_stmt in segment.body:
                        self._infer_statement(body_stmt)
                except Exception as e:
                    self.errors.append(f"段 '{segment.name}' 推断异常: {e}")

                # 应用累积的替换
                local_subs = self._hm_subs.clone()
                if self._collected_return_types:
                    try:
                        for rt in self._collected_return_types:
                            new_subs = unify(
                                pre_func_type.return_type.apply_substitution(local_subs),
                                rt.apply_substitution(local_subs),
                                local_subs,
                            )
                            local_subs = new_subs
                    except UnificationError:
                        pass

                resolved_params = [pt.apply_substitution(local_subs)
                                   for pt in pre_func_type.param_types]
                resolved_return = pre_func_type.return_type.apply_substitution(local_subs)

                # 无 return 且未显式声明返回 → 视为空
                if not self._collected_return_types and not segment.return_type \
                        and isinstance(resolved_return, TypeVar) \
                        and resolved_return.name not in local_subs.mapping:
                    resolved_return = TYPE_NULL

                final_func_type = FunctionType(resolved_params, resolved_return)
                generalized = self._generalize(segment.name, final_func_type)
                sym.data_type = generalized

                self._current_return_type = None
                self._hm_subs = TypeSubstitution()

                # 恢复 type_cache（但保留本轮已推断结果，以让后续段体查询能看到新的推断）：
                # 因为段体推断期间 type_cache 中保存了本论对 body 中调用的推断结果，
                # 为避免泄漏，我们只合并顶层/符号表而不在 type_cache 中保留段体内容。
                self.type_cache = saved_cache
                self.symbol_table.exit_scope()

    # ---- Let-polymorphism：泛化与实例化 ----
    def _generalize(self, name: str, t: Type) -> Type:
        """将具体类型中的自由类型变量提升为泛型参数（let-generalization）。

        返回的类型仍保留 TypeVar 形式，但会被记录为泛型段，供调用处实例化。
        这里实现为：将 t 中的自由 TypeVar 名称收集并登记到 generic_segment_defs。
        """
        fvs = list(t.collect_type_vars())
        if fvs:
            # 按名称排序获得确定性结果
            fv_names = sorted({tv.name for tv in fvs})
            # 记录为泛型段（用于调试/测试）
            self.generic_segment_defs[name] = fv_names
        return t

    def _instantiate(self, func_type: FunctionType) -> FunctionType:
        """将泛型类型实例化为调用点的具体类型（生成新鲜的 TypeVar）。

        对 func_type 中的所有 TypeVar（即自由类型变量）替换为全新的 TypeVar，
        避免不同调用点之间污染。这是 HM 的核心机制之一。
        """
        if not isinstance(func_type, FunctionType):
            return func_type

        fvs = list(func_type.collect_type_vars())
        if not fvs:
            return func_type

        # 建立 旧名称 → 新鲜 TypeVar 的替换
        subs = TypeSubstitution()
        seen = set()
        counter = [0]
        for tv in fvs:
            if tv.name in seen:
                continue
            seen.add(tv.name)
            # 生成一个全新的、唯一的 TypeVar 名称
            fresh_name = f"{tv.name}'{counter[0]}"
            counter[0] += 1
            subs.bind(tv.name, TypeVar(fresh_name))

        new_params = [p.apply_substitution(subs) for p in func_type.param_types]
        new_return = func_type.return_type.apply_substitution(subs)
        return FunctionType(new_params, new_return)

    # ---- 主推断阶段 ----
    def _infer_module(self, module: Module):
        """推断模块内容"""
        for enum_def in getattr(module, 'enums', []):
            self._infer_enum_def(enum_def)

        for trait_def in getattr(module, 'trait_defs', []):
            self._infer_trait_def(trait_def)

        if hasattr(module, 'classes'):
            for cls in module.classes:
                self._infer_class(cls)

        if hasattr(module, 'segments'):
            for segment in module.segments:
                self._infer_segment(segment)

        if hasattr(module, 'statements'):
            for stmt in module.statements:
                self._infer_statement(stmt)

    def _infer_enum_def(self, enum_def: EnumDefinition):
        """推断枚举定义"""
        self.symbol_table.enter_scope()

        generic_params = getattr(enum_def, 'generic_params', None) or []
        for gp in generic_params:
            self.symbol_table.define_generic_param(gp)

        for variant in enum_def.variants:
            field_types = [self._parse_type_string(f.type_annotation) for f in variant.fields]
            if field_types:
                func_type = FunctionType(field_types, self.enum_defs.get(enum_def.name, EnumType(enum_name=enum_def.name)))
            else:
                func_type = FunctionType([], self.enum_defs.get(enum_def.name, EnumType(enum_name=enum_def.name)))
            self.symbol_table.define(variant.name, 'function', func_type)

        self.symbol_table.exit_scope()

    def _infer_trait_def(self, trait_def: TraitDefinition):
        """推断 trait 定义 —— 验证方法签名内部一致性"""
        seen_methods = set()
        for method in trait_def.methods:
            if method.name in seen_methods:
                self.errors.append(
                    f"接口 '{trait_def.name}' 中存在重复方法 '{method.name}'"
                )
            seen_methods.add(method.name)

    # ---- 类推断（包括泛型类 + 接口实现验证） ----
    def _infer_class(self, cls: ClassDefinition):
        """推断类（支持泛型类 + 接口实现验证）"""
        self.symbol_table.enter_scope()

        # 注册泛型参数
        generic_params = getattr(cls, 'generic_params', None) or []
        for gp in generic_params:
            self.symbol_table.define_generic_param(gp)

        # 处理构造函数
        if cls.constructor:
            self._infer_constructor(cls.constructor)

        # 处理方法并构建方法签名索引
        class_method_sigs: Dict[str, FunctionType] = {}
        for method in cls.methods:
            self._infer_method(method)
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type) if method.return_type else TYPE_UNKNOWN
            class_method_sigs[method.name] = FunctionType(param_types, return_type)

        # 验证类实现的接口
        declared_interfaces = getattr(cls, 'interfaces', None) or []
        resolved_interfaces: List[InterfaceType] = []
        for iface_name in declared_interfaces:
            if iface_name in self.trait_defs:
                iface = self.trait_defs[iface_name]
                resolved_interfaces.append(iface)
                # 逐个检查接口方法是否被实现
                self._check_class_implements_interface(cls.name, iface, class_method_sigs)
            else:
                self.errors.append(f"类 '{cls.name}' 声明的接口 '{iface_name}' 未定义")

        # 更新符号表中该类的 ClassType，记录实现的接口
        sym = self.symbol_table.lookup(cls.name)
        if sym and isinstance(sym.data_type, ClassType):
            sym.data_type.implements_interfaces = resolved_interfaces

        self.symbol_table.exit_scope()

    def _check_class_implements_interface(self, class_name: str, iface: InterfaceType,
                                           class_methods: Dict[str, FunctionType]):
        """检查类是否完整实现了接口的所有方法（存在性 + 签名匹配）"""
        for method_name, required_ft in iface.methods.items():
            if method_name not in class_methods:
                self.errors.append(
                    f"类 '{class_name}' 未实现接口 '{iface.interface_name}' "
                    f"的必需方法 '{method_name}'"
                )
                continue
            actual_ft = class_methods[method_name]
            err = iface.method_signature_matches(method_name, actual_ft)
            if err:
                self.errors.append(
                    f"类 '{class_name}' 实现接口 '{iface.interface_name}': {err}"
                )

    def _infer_constructor(self, constructor: ConstructorDefinition):
        """推断构造函数"""
        self.symbol_table.enter_scope()

        for param in constructor.parameters:
            param_type = self._parse_type_string(param.type_annotation)
            self.symbol_table.define(param.name, 'parameter', param_type)

        for stmt in constructor.body:
            self._infer_statement(stmt)

        self.symbol_table.exit_scope()

    def _infer_method(self, method: MethodDefinition):
        """推断方法"""
        self.symbol_table.enter_scope()

        self.symbol_table.define('己', 'parameter', TYPE_ANY)

        for param in method.parameters:
            param_type = self._parse_type_string(param.type_annotation)
            self.symbol_table.define(param.name, 'parameter', param_type)

        if method.return_type:
            self._current_return_type = self._parse_type_string(method.return_type)
        else:
            self._current_return_type = None

        for stmt in method.body:
            self._infer_statement(stmt)

        self._current_return_type = None
        self.symbol_table.exit_scope()

    # ---- 段落/函数（含泛型）推断 ----
    def _infer_segment(self, segment: SegmentDefinition):
        """推断段落（函数）—— 支持泛型参数"""
        self.symbol_table.enter_scope()

        # 检查是否为异步函数
        is_async = '异步' in (getattr(segment, 'modifiers', []) or [])
        if is_async:
            self._in_async_function = True

        # 注册泛型参数到当前作用域
        generic_params = getattr(segment, 'generic_params', None) or []
        for gp in generic_params:
            self.symbol_table.define_generic_param(gp)

        # 注册参数类型（含 TypeVar）
        param_types: List[Type] = []
        for param in segment.parameters:
            if param.type_annotation:
                ptype = self._parse_type_string(param.type_annotation)
            else:
                ptype = TYPE_UNKNOWN
            param_types.append(ptype)
            self.symbol_table.define(param.name, 'parameter', ptype)

        # 设置返回类型（含 TypeVar）
        declared_return: Optional[Type] = None
        if segment.return_type:
            declared_return = self._parse_type_string(segment.return_type)
            self._current_return_type = declared_return
            if is_async:
                self._current_return_type = FutureType(declared_return)
        else:
            self._current_return_type = None

        # 推断函数体
        self._collected_return_types = []
        for stmt in segment.body:
            self._infer_statement(stmt)

        # 构建函数类型签名
        return_type_for_sig: Type
        if declared_return is not None:
            return_type_for_sig = declared_return
        elif self._collected_return_types:
            # 从返回语句推断返回类型
            inferred = self._collected_return_types[0]
            for t in self._collected_return_types[1:]:
                try:
                    subs = unify(inferred, t)
                    inferred = inferred.apply_substitution(subs)
                except UnificationError:
                    # 返回类型不一致，使用 Unknown
                    inferred = TYPE_UNKNOWN
                    break
            return_type_for_sig = inferred
        elif generic_params:
            return_type_for_sig = TYPE_UNKNOWN
        else:
            # 无返回语句 → 返回空
            return_type_for_sig = TYPE_NULL

        if is_async and not isinstance(return_type_for_sig, FutureType):
            return_type_for_sig = FutureType(return_type_for_sig)

        function_type = FunctionType(param_types, return_type_for_sig)

        # 更新符号表中该函数的类型
        sym = self.symbol_table.lookup(segment.name)
        if sym:
            sym.data_type = function_type

        self._current_return_type = None
        if is_async:
            self._in_async_function = False
        self.symbol_table.exit_scope()

    # ---- 语句推断 ----
    def _infer_defer_stmt(self, stmt: DeferStatement):
        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
        self.type_cache[id(stmt)] = TYPE_NULL
        return TYPE_NULL

    def _infer_async_scope(self, stmt: AsyncScope):
        elem_types = []
        for task in stmt.tasks:
            t = self._infer_expr(task)
            elem_types.append(t)
        result = ListType()
        self.type_cache[id(stmt)] = result
        return result

    def _infer_statement(self, stmt) -> Type:
        """推断语句类型，返回语句的整体类型（通常是返回语句的返回类型）"""
        if stmt is None:
            return TYPE_NULL

        if is_instance(stmt, 'VariableDeclaration'):
            return self._infer_var_decl(stmt)

        elif is_instance(stmt, 'Assignment'):
            return self._infer_assignment(stmt)

        elif is_instance(stmt, 'IfStatement'):
            return self._infer_if_stmt(stmt)

        elif is_instance(stmt, 'ForeachStatement'):
            return self._infer_foreach_stmt(stmt)

        elif is_instance(stmt, 'WhileStatement'):
            return self._infer_while_stmt(stmt)

        elif is_instance(stmt, 'ReturnStatement'):
            return self._infer_return_stmt(stmt)

        elif is_instance(stmt, 'MatchStatement'):
            return self._infer_match_stmt(stmt)

        elif is_instance(stmt, 'ExpressionStatement'):
            return self._infer_expr(stmt.expression)

        elif is_instance(stmt, 'PrintStatement'):
            if hasattr(stmt, 'value') and stmt.value is not None:
                self._infer_expr(stmt.value)
            return TYPE_NULL

        elif is_instance(stmt, 'ThrowStatement'):
            if hasattr(stmt, 'value') and stmt.value is not None:
                self._infer_expr(stmt.value)
            return TYPE_NULL

        elif is_instance(stmt, 'FunctionCall'):
            return self._infer_expr(stmt)

        elif is_instance(stmt, 'SegmentDefinition'):
            self._infer_segment(stmt)
            return TYPE_NULL

        elif is_instance(stmt, 'DeferStatement'):
            return self._infer_defer_stmt(stmt)

        elif is_instance(stmt, 'AsyncScope'):
            return self._infer_async_scope(stmt)

        return TYPE_NULL

    # ---- 变量声明推断 ----
    def _infer_var_decl(self, stmt) -> Type:
        """推断变量声明（支持解构赋值）"""

        # 检查是否解构赋值：解构 (x, y) = 表达式
        destructure_names = getattr(stmt, 'destructure_names', None)
        if destructure_names:
            return self._infer_destructure_decl(stmt, destructure_names)

        expr_type = self._infer_expr(stmt.value)

        # 检查类型注解
        type_annotation = getattr(stmt, 'type_annotation', None)
        final_type = expr_type

        if type_annotation:
            anno_type = self._parse_type_string(type_annotation)
            # 尝试合一（允许类型变量绑定）
            try:
                subs = unify(anno_type, expr_type)
                final_type = anno_type.apply_substitution(subs)
            except UnificationError:
                # 合一失败：类型不匹配
                if not expr_type.is_subtype_of(anno_type):
                    self.errors.append(
                        f"类型不匹配: 变量 '{stmt.name}' 声明为 {anno_type}，"
                        f"但初始值类型为 {expr_type}"
                    )
                final_type = anno_type

        # 可空性检查
        if isinstance(expr_type, NullType) and type_annotation and '|空' not in type_annotation:
            self.errors.append(
                f"空安全错误: 变量 '{stmt.name}' 声明为不可空类型 {type_annotation}，"
                f"但不能赋值为空"
            )

        is_mutable = getattr(stmt, 'is_mutable', False)
        self.symbol_table.define(stmt.name, 'variable', final_type, is_mutable)
        self.type_cache[id(stmt)] = final_type
        return final_type

    def _infer_destructure_decl(self, stmt, destructure_names: List[str]) -> Type:
        """推断解构变量声明：解构 (x, y) = 表达式"""
        expr_type = self._infer_expr(stmt.value)

        # 期望表达式返回 TupleType
        if isinstance(expr_type, TupleType):
            element_types = expr_type.element_types
            for i, name in enumerate(destructure_names):
                if i < len(element_types):
                    var_type = element_types[i]
                else:
                    var_type = TYPE_UNKNOWN
                is_mutable = getattr(stmt, 'is_mutable', False)
                self.symbol_table.define(name, 'variable', var_type, is_mutable)
        elif isinstance(expr_type, ListType):
            # 列表解构：所有变量获取元素类型
            elem_type = expr_type.element_type or TYPE_UNKNOWN
            for name in destructure_names:
                is_mutable = getattr(stmt, 'is_mutable', False)
                self.symbol_table.define(name, 'variable', elem_type, is_mutable)
        else:
            # 未知类型，全部标记为 Unknown
            for name in destructure_names:
                is_mutable = getattr(stmt, 'is_mutable', False)
                self.symbol_table.define(name, 'variable', TYPE_UNKNOWN, is_mutable)
            self.errors.append(
                f"解构赋值期望元组或列表类型，实际为 {expr_type}"
            )

        result_type = expr_type  # 整个解构表达式的类型
        self.type_cache[id(stmt)] = result_type
        return result_type

    def _infer_assignment(self, stmt) -> Type:
        """推断赋值语句"""
        value_type = self._infer_expr(stmt.value)

        if is_instance(stmt.target, 'Identifier'):
            target_name = stmt.target.name
            symbol = self.symbol_table.lookup(target_name)
            if symbol:
                if not symbol.is_mutable:
                    self.errors.append(
                        f"不可变变量 '{target_name}' 不能重新赋值"
                    )
                # 类型兼容检查（使用合一）
                try:
                    subs = unify(symbol.data_type, value_type)
                    updated = symbol.data_type.apply_substitution(subs)
                    self.symbol_table.update_type(target_name, updated)
                except UnificationError as e:
                    if not value_type.is_subtype_of(symbol.data_type):
                        self.errors.append(
                            f"类型不匹配: 变量 '{target_name}' 类型为 {symbol.data_type}，"
                            f"不能赋值为 {value_type} ({e.message})"
                        )
            self.type_cache[id(stmt)] = value_type
            return value_type

        elif is_instance(stmt.target, 'PropertyAccess'):
            self._infer_expr(stmt.target)
            self.type_cache[id(stmt)] = value_type
            return value_type

        self.type_cache[id(stmt)] = value_type
        return value_type

    def _infer_if_stmt(self, stmt) -> Type:
        cond_type = self._infer_expr(stmt.condition)
        if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
            self.errors.append(
                f"条件表达式类型应为布尔，实际为 {cond_type}"
            )

        self.symbol_table.enter_scope()
        for s in stmt.then_body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()

        if stmt.else_body:
            self.symbol_table.enter_scope()
            for s in stmt.else_body:
                self._infer_statement(s)
            self.symbol_table.exit_scope()

        for elseif_body in getattr(stmt, 'elseif_bodies', []) or []:
            self.symbol_table.enter_scope()
            for s in elseif_body:
                self._infer_statement(s)
            self.symbol_table.exit_scope()
        return TYPE_NULL

    def _infer_foreach_stmt(self, stmt) -> Type:
        iter_type = self._infer_expr(stmt.iterable)

        self.symbol_table.enter_scope()

        # 推断循环变量类型
        if isinstance(iter_type, ListType):
            var_type = iter_type.element_type or TYPE_UNKNOWN
        elif isinstance(iter_type, GenericTypeInstance) and iter_type.base_name in ('列表', 'List'):
            var_type = iter_type.type_args[0] if iter_type.type_args else TYPE_UNKNOWN
        elif isinstance(iter_type, StringType):
            var_type = TYPE_STRING
        else:
            var_type = TYPE_UNKNOWN
        self.symbol_table.define(stmt.variable, 'variable', var_type)

        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
        return TYPE_NULL

    def _infer_while_stmt(self, stmt) -> Type:
        cond_type = self._infer_expr(stmt.condition)
        if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
            self.errors.append(
                f"循环条件类型应为布尔，实际为 {cond_type}"
            )

        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
        return TYPE_NULL

    def _infer_return_stmt(self, stmt) -> Type:
        if stmt.value:
            return_type = self._infer_expr(stmt.value)
            # 收集返回类型以便在无显式声明时推断
            if return_type is not None:
                self._collected_return_types.append(return_type)
            if self._current_return_type:
                try:
                    subs = unify(self._current_return_type, return_type)
                    # ⭐ 累积到当前段的 HM 上下文中
                    hm_subs = getattr(self, '_hm_subs', None)
                    if hm_subs is not None:
                        for k, v in subs.mapping.items():
                            if k not in hm_subs.mapping:
                                hm_subs.mapping[k] = v
                            else:
                                hm_subs.mapping[k] = hm_subs.mapping[k].apply_substitution(subs)
                    resolved = self._current_return_type.apply_substitution(subs)
                    self._current_return_type = resolved
                except UnificationError:
                    if not return_type.is_subtype_of(self._current_return_type):
                        self.errors.append(
                            f"返回类型不匹配: 期望 {self._current_return_type}，实际为 {return_type}"
                        )
            self.type_cache[id(stmt)] = return_type
            return return_type
        else:
            if self._current_return_type and not isinstance(self._current_return_type, (NullType, UnknownType, AnyType)):
                self.errors.append(
                    f"返回类型不匹配: 期望 {self._current_return_type}，但无返回值"
                )
            return TYPE_NULL

    def _infer_match_stmt(self, stmt) -> Type:
        subject_type = self._infer_expr(stmt.subject)
        self.type_cache[id(stmt)] = TYPE_UNKNOWN

        if isinstance(subject_type, EnumType):
            matched_variants = set()
            for case in stmt.cases:
                pattern = case.pattern
                variant_name = self._get_pattern_variant_name(pattern)
                if variant_name:
                    matched_variants.add(variant_name)

                self.symbol_table.enter_scope()
                if pattern and getattr(pattern, 'binding', None):
                    binding_type = self._get_binding_type(subject_type, pattern)
                    self.symbol_table.define(pattern.binding, 'variable', binding_type)

                if case.guard:
                    guard_type = self._infer_expr(case.guard)
                    if not isinstance(guard_type, (BooleanType, AnyType, UnknownType)):
                        self.errors.append(
                            f"匹配守卫条件类型应为布尔，实际为 {guard_type}"
                        )

                for s in case.body:
                    self._infer_statement(s)
                self.symbol_table.exit_scope()

            has_wildcard = any(
                getattr(c.pattern, 'kind', '') == 'wildcard' for c in stmt.cases
            )

            if not has_wildcard and subject_type.enum_name in self.enum_defs:
                enum_def = self.enum_defs[subject_type.enum_name]
                unmatched = []
                for v in enum_def.variants:
                    if v not in matched_variants:
                        unmatched.append(v)
                if unmatched:
                    self.errors.append(
                        f"非穷尽匹配: 枚举 '{subject_type.enum_name}' 的以下变体未处理: "
                        + ", ".join(unmatched)
                    )
        else:
            for case in stmt.cases:
                self.symbol_table.enter_scope()
                for s in case.body:
                    self._infer_statement(s)
                self.symbol_table.exit_scope()
        return TYPE_NULL

    def _get_pattern_variant_name(self, pattern) -> Optional[str]:
        if pattern is None:
            return None
        if hasattr(pattern, 'kind') and pattern.kind == 'variable':
            if hasattr(pattern, 'value') and isinstance(pattern.value, str) and pattern.value and pattern.value[0].isascii() and pattern.value[0].isupper():
                return pattern.value
        if hasattr(pattern, 'kind') and pattern.kind == 'type_check':
            return pattern.type_name
        return None

    def _get_binding_type(self, enum_type: EnumType, pattern) -> Type:
        return TYPE_UNKNOWN

    # ---- 表达式推断 ----
    def _infer_expr(self, expr) -> Type:
        """推断表达式类型"""
        if expr is None:
            return TYPE_NULL

        if id(expr) in self.type_cache:
            return self.type_cache[id(expr)]

        result_type: Type = TYPE_UNKNOWN

        # 字面量
        if is_instance(expr, 'NumberLiteral'):
            result_type = TYPE_NUMBER
        elif is_instance(expr, 'StringLiteral'):
            result_type = TYPE_STRING
        elif is_instance(expr, 'BooleanLiteral'):
            result_type = TYPE_BOOLEAN
        elif is_instance(expr, 'NullLiteral'):
            result_type = TYPE_NULL

        # 解包表达式：值! 或 unwrap(值)
        elif is_instance(expr, 'UnwrapExpression'):
            inner_type = self._infer_expr(expr.value)
            if isinstance(inner_type, OptionalTypeWrapper):
                result_type = inner_type.inner_type
            elif isinstance(inner_type, NullType):
                result_type = TYPE_UNKNOWN  # 空值! → 运行时失败
            else:
                # 非可空类型但 unwrap 了：警告但允许
                result_type = inner_type
            return result_type

        # 标识符
        elif is_instance(expr, 'Identifier'):
            # 特殊处理：'空'、'None' 等是「可空的底类型」，被推断为 NullType
            if expr.name in ('None', '空', 'null', 'NULL'):
                result_type = TYPE_NULL
            else:
                symbol = self.symbol_table.lookup(expr.name)
                if symbol:
                    result_type = symbol.data_type
                elif expr.name in self.enum_defs:
                    result_type = EnumType(enum_name=expr.name)
                elif expr.name in self.trait_defs:
                    result_type = self.trait_defs[expr.name]
                elif expr.name in self.generic_class_defs:
                    result_type = ClassType(expr.name)
                else:
                    result_type = TYPE_UNKNOWN

        # 二元运算
        elif is_instance(expr, 'BinaryOp'):
            left_type = self._infer_expr(expr.left)
            right_type = self._infer_expr(expr.right)
            op = expr.operator

            # ⭐ 可空类型强制检查：可空类型不能直接参与运算，必须先 unwrap
            def _is_nullable(t):
                return isinstance(t, (OptionalTypeWrapper, NullType))

            if _is_nullable(left_type) and not isinstance(right_type, (AnyType, UnknownType, TypeVar)):
                self.errors.append(
                    f"可空类型不能直接参与运算 '{op}': 左侧类型为 {left_type}，"
                    f"需要先使用 '!' 或 'unwrap()' 解包"
                )
            if _is_nullable(right_type) and not isinstance(left_type, (AnyType, UnknownType, TypeVar)):
                self.errors.append(
                    f"可空类型不能直接参与运算 '{op}': 右侧类型为 {right_type}，"
                    f"需要先使用 '!' 或 'unwrap()' 解包"
                )

            # 小工具：HM 风格双向合一，把 TypeVar 约束为具体类型
            # 同时把产生的替换累积到 self._hm_subs（若在段体推断上下文）
            def _try_unify_both_as(target: Type) -> bool:
                try:
                    subs1 = unify(left_type, target)
                    subs2 = unify(right_type, target)
                    # 累积到当前段的 HM 上下文中
                    hm_subs = getattr(self, '_hm_subs', None)
                    if hm_subs is not None:
                        for k, v in subs1.mapping.items():
                            if k not in hm_subs.mapping:
                                hm_subs.mapping[k] = v
                        for k, v in subs2.mapping.items():
                            if k not in hm_subs.mapping:
                                hm_subs.mapping[k] = v
                    return True
                except UnificationError:
                    return False

            if op in ('+', '加'):
                if isinstance(left_type, StringType) and isinstance(right_type, StringType):
                    result_type = TYPE_STRING
                elif isinstance(left_type, NumberType) and isinstance(right_type, NumberType):
                    result_type = TYPE_NUMBER
                elif isinstance(left_type, StringType) or isinstance(right_type, StringType):
                    # 其中一边是字符串，尝试把另一边合一为字符串（宽松）
                    _try_unify_both_as(TYPE_STRING)
                    result_type = TYPE_STRING
                elif isinstance(left_type, TypeVar) and isinstance(right_type, TypeVar) and left_type.name == right_type.name:
                    # 同名 TypeVar：T + T → T（保持多态）
                    result_type = left_type
                elif isinstance(left_type, NumberType) or isinstance(right_type, NumberType):
                    # 一边是 数，另一边可能是 TypeVar/UNKNOWN，HM 合一
                    _try_unify_both_as(TYPE_NUMBER)
                    result_type = TYPE_NUMBER
                elif isinstance(left_type, (TypeVar, UnknownType)) or isinstance(right_type, (TypeVar, UnknownType)):
                    # 至少一边是 TypeVar/UNKNOWN —— 按 HM 规则推断为 数
                    # 但如果失败则回退为 UNKNOWN
                    if _try_unify_both_as(TYPE_NUMBER):
                        result_type = TYPE_NUMBER
                    else:
                        result_type = TYPE_UNKNOWN
                else:
                    # 完全具体但不一致
                    try:
                        unify(left_type, TYPE_NUMBER)
                        unify(right_type, TYPE_NUMBER)
                        result_type = TYPE_NUMBER
                    except UnificationError:
                        result_type = TYPE_UNKNOWN
            elif op in ('-', '减', '*', '乘', '/', '除', '%', '模', '^', '幂'):
                # 算术：HM 风格 —— 若是 TypeVar 则合一为 数
                try:
                    unify(left_type, TYPE_NUMBER)
                    unify(right_type, TYPE_NUMBER)
                except UnificationError:
                    self.errors.append(f"算术运算 '{op}' 需要数字类型，但得到 {left_type} 和 {right_type}")
                result_type = TYPE_NUMBER
            elif op in ('>', '<', '>=', '<=', '==', '!=', '等于', '不等于', '大于', '小于', '大于等于', '小于等于'):
                result_type = TYPE_BOOLEAN
            elif op in ('且', '与', '或', 'and', 'or'):
                result_type = TYPE_BOOLEAN
            else:
                result_type = TYPE_UNKNOWN

        # 一元运算
        elif is_instance(expr, 'UnaryOp'):
            operand_type = self._infer_expr(expr.operand)
            if expr.operator in ('非', 'not', '!'):
                result_type = TYPE_BOOLEAN if isinstance(operand_type, BooleanType) else TYPE_UNKNOWN
            elif expr.operator in ('-',):
                result_type = TYPE_NUMBER if isinstance(operand_type, NumberType) else TYPE_UNKNOWN
            else:
                result_type = operand_type

        # 函数调用 / 段落调用
        elif is_instance(expr, 'FunctionCall'):
            result_type = self._infer_function_call(expr)

        # 属性访问（支持泛型类实例方法查找）
        elif is_instance(expr, 'PropertyAccess'):
            obj_type = self._infer_expr(expr.obj)
            property_name = expr.property_name

            # 通用：先按 obj_type 的类定义查找方法
            if isinstance(obj_type, ClassType):
                cls_def = self._lookup_class_def(obj_type.class_name)
                if cls_def is not None:
                    # 构建从泛型参数名 → 实际类型的替换
                    param_names = list(self.generic_class_defs.get(obj_type.class_name, []))
                    subs = TypeSubstitution()
                    if param_names and obj_type.type_args:
                        for i, pn in enumerate(param_names):
                            if i < len(obj_type.type_args):
                                subs.bind(pn, obj_type.type_args[i])

                    # 在方法列表中查找
                    for method in getattr(cls_def, 'methods', []) or []:
                        if method.name == property_name:
                            # 构建 FunctionType 并应用替换
                            m_params = []
                            for mp in method.parameters:
                                if mp.type_annotation:
                                    m_params.append(self._parse_type_string(mp.type_annotation))
                                else:
                                    m_params.append(TYPE_UNKNOWN)
                            m_return = self._parse_type_string(method.return_type) if method.return_type else TYPE_UNKNOWN
                            ft = FunctionType(m_params, m_return)
                            if param_names:
                                ft = ft.apply_substitution(subs)
                            result_type = ft
                            self.type_cache[id(expr)] = result_type
                            return result_type

            # 在对象类型中按属性名查找（简单的 Any）
            result_type = TYPE_UNKNOWN

        # 索引访问
        elif is_instance(expr, 'IndexAccess'):
            obj_type = self._infer_expr(expr.obj)
            index_type = self._infer_expr(expr.index)

            if isinstance(obj_type, ListType):
                result_type = obj_type.element_type or TYPE_UNKNOWN
            elif isinstance(obj_type, GenericTypeInstance) and obj_type.base_name in ('列表', 'List'):
                result_type = obj_type.type_args[0] if obj_type.type_args else TYPE_UNKNOWN
            elif isinstance(obj_type, StringType):
                result_type = TYPE_STRING
            elif isinstance(obj_type, DictType):
                result_type = obj_type.value_type or TYPE_UNKNOWN
            elif isinstance(obj_type, GenericTypeInstance) and obj_type.base_name in ('字典', 'Map'):
                result_type = obj_type.type_args[1] if len(obj_type.type_args) > 1 else TYPE_UNKNOWN
            else:
                result_type = TYPE_UNKNOWN

        # 列表字面量（支持泛型元素类型推断）
        elif is_instance(expr, 'ListLiteral'):
            element_types = [self._infer_expr(e) for e in expr.elements]
            if element_types:
                # 尝试合一所有元素类型
                common_type: Type = element_types[0]
                all_matched = True
                for t in element_types[1:]:
                    try:
                        subs = unify(common_type, t)
                        common_type = common_type.apply_substitution(subs)
                    except UnificationError:
                        all_matched = False
                        break
                if all_matched:
                    result_type = ListType(common_type)
                else:
                    result_type = ListType(TYPE_ANY)
            else:
                result_type = ListType(TYPE_UNKNOWN)

        # 字典字面量
        elif is_instance(expr, 'DictLiteral'):
            key_types = []
            val_types = []
            for entry in expr.entries:
                if hasattr(entry, 'key'):
                    kt = self._infer_expr(entry.key)
                    key_types.append(kt)
                if hasattr(entry, 'value'):
                    vt = self._infer_expr(entry.value)
                    val_types.append(vt)
            # 统一键类型
            key_type: Type
            if key_types:
                key_type = key_types[0]
                for t in key_types[1:]:
                    try:
                        subs = unify(key_type, t)
                        key_type = key_type.apply_substitution(subs)
                    except UnificationError:
                        key_type = TYPE_ANY
                        break
            else:
                key_type = TYPE_UNKNOWN
            # 统一值类型
            val_type: Type
            if val_types:
                val_type = val_types[0]
                for t in val_types[1:]:
                    try:
                        subs = unify(val_type, t)
                        val_type = val_type.apply_substitution(subs)
                    except UnificationError:
                        val_type = TYPE_ANY
                        break
            else:
                val_type = TYPE_UNKNOWN
            result_type = DictType(key_type, val_type)

        # 类实例化（支持泛型类 + 类型参数推断）
        elif is_instance(expr, 'NewExpression'):
            arg_types = [self._infer_expr(a) for a in expr.arguments]
            class_name = expr.class_name

            if class_name in self.generic_class_defs:
                # 泛型类：根据显式类型参数 + 构造函数参数推断类型参数
                param_names = self.generic_class_defs[class_name]
                type_args: List[Type] = [TYPE_UNKNOWN for _ in param_names]

                # 1) 处理显式类型参数（如 数组[数](3)）
                explicit_args = getattr(expr, 'type_args', None) or []
                subs = TypeSubstitution()
                for i, ta_str in enumerate(explicit_args):
                    if i < len(param_names):
                        parsed = self._parse_type_string(ta_str) if isinstance(ta_str, str) else TYPE_UNKNOWN
                        subs.bind(param_names[i], parsed)
                        type_args[i] = parsed

                # 2) 若有构造函数参数，尝试从参数类型进行合一推断剩余类型参数
                cls_def = self._lookup_class_def(class_name)
                if cls_def is not None and cls_def.constructor:
                    ctor = cls_def.constructor
                    ctor_param_types: List[Type] = []
                    # 临时作用域：注册泛型参数以允许解析类型变量
                    self.symbol_table.enter_scope()
                    for gp in param_names:
                        self.symbol_table.define_generic_param(gp)
                    try:
                        for param in ctor.parameters:
                            if param.type_annotation:
                                ctor_param_types.append(self._parse_type_string(param.type_annotation))
                            else:
                                ctor_param_types.append(TYPE_UNKNOWN)
                    finally:
                        self.symbol_table.exit_scope()

                    # 合一推断：对每个形参和实参进行合一
                    for formal, actual in zip(ctor_param_types, arg_types):
                        try:
                            new_subs = unify(formal, actual, subs)
                            subs = new_subs
                        except UnificationError:
                            # 若合一失败，跳过该参数（保持 UNKNOWN）
                            pass

                    # 应用替换到所有类型参数位置
                    for i, name in enumerate(param_names):
                        if i < len(type_args) and isinstance(type_args[i], UnknownType):
                            tv = TypeVar(name)
                            resolved = tv.apply_substitution(subs)
                            if not isinstance(resolved, TypeVar) or resolved.name != name:
                                type_args[i] = resolved

                result_type = ClassType(class_name, type_args)
                # 记录实例化（便于测试/调试）
                self.generic_class_instances[class_name] = type_args
            else:
                # 内置泛型名称检查（如 "列表"）
                if class_name in ('列表', 'List'):
                    elem = arg_types[0] if arg_types else TYPE_UNKNOWN
                    result_type = ListType(elem)
                elif class_name in ('字典', 'Map'):
                    k = arg_types[0] if len(arg_types) > 0 else TYPE_UNKNOWN
                    v = arg_types[1] if len(arg_types) > 1 else TYPE_UNKNOWN
                    result_type = DictType(k, v)
                else:
                    result_type = ClassType(class_name)

        elif is_instance(expr, 'SelfReference'):
            result_type = TYPE_ANY

        elif is_instance(expr, 'ListComprehension'):
            iter_type = self._infer_expr(expr.iterable)
            self.symbol_table.enter_scope()
            if isinstance(iter_type, ListType):
                self.symbol_table.define(expr.variable, 'variable', iter_type.element_type or TYPE_UNKNOWN)
            elif isinstance(iter_type, GenericTypeInstance) and iter_type.base_name in ('列表', 'List'):
                self.symbol_table.define(expr.variable, 'variable',
                                         iter_type.type_args[0] if iter_type.type_args else TYPE_UNKNOWN)
            else:
                self.symbol_table.define(expr.variable, 'variable', TYPE_UNKNOWN)
            if expr.condition:
                cond_type = self._infer_expr(expr.condition)
                if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
                    self.errors.append(f"列表推导过滤条件类型应为布尔，实际为 {cond_type}")
            elem_type = self._infer_expr(expr.expression)
            self.symbol_table.exit_scope()
            result_type = ListType(elem_type)

        elif is_instance(expr, 'LambdaExpression'):
            result_type = self._infer_lambda(expr)

        elif is_instance(expr, 'StringInterpolation'):
            for part in expr.parts:
                if not isinstance(part, str):
                    self._infer_expr(part)
            result_type = TYPE_STRING

        elif is_instance(expr, 'ConditionalExpression'):
            cond_type = self._infer_expr(expr.condition)
            if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
                self.errors.append(f"条件表达式类型应为布尔，实际为 {cond_type}")
            then_type = self._infer_expr(expr.then_expr)
            if expr.else_expr:
                else_type = self._infer_expr(expr.else_expr)
                try:
                    subs = unify(then_type, else_type)
                    result_type = then_type.apply_substitution(subs)
                except UnificationError:
                    result_type = then_type
            else:
                result_type = then_type

        elif is_instance(expr, 'PipeExpression'):
            cur_type = TYPE_UNKNOWN
            for sub_expr in expr.expressions:
                cur_type = self._infer_expr(sub_expr)
            result_type = cur_type

        elif is_instance(expr, 'AwaitExpression'):
            inner_type = self._infer_expr(expr.expression)
            if isinstance(inner_type, FutureType):
                result_type = inner_type.inner_type
            else:
                result_type = inner_type

        else:
            result_type = TYPE_UNKNOWN

        self.type_cache[id(expr)] = result_type
        return result_type

    # ---- Lambda 表达式推断（HM 风格，含 TypeVar 参数） ----
    def _infer_lambda(self, expr) -> FunctionType:
        """推断 lambda 表达式：
        - 未标注的参数用 TypeVar 填充（支持合一推断）
        - 推断 body 类型作为返回类型
        """
        self.symbol_table.enter_scope()
        param_types: List[Type] = []
        for i, param in enumerate(expr.parameters):
            if getattr(param, 'type_annotation', None):
                try:
                    ptype = self._parse_type_string(param.type_annotation)
                except Exception:
                    ptype = TypeVar(f"lam{i}")
            else:
                ptype = TypeVar(f"lam{i}")
            param_types.append(ptype)
            self.symbol_table.define(param.name, 'parameter', ptype)

        # 推断 body
        body_type = self._infer_expr(expr.body)

        # 应用可能从外部合一所产生的替换（当前作用域内的参数 TypeVar 被合一后的值替换）
        # 这里简单处理：对 param_types 和 body_type 应用全局 TypeSubstitution 是不实际的，
        # 因为我们在 unify 时产生的替换仅用于推断，不持久化到一个全局环境。
        # 但在 _infer_function_call 中对每个调用会重新实例化，因此是安全的。

        self.symbol_table.exit_scope()
        return FunctionType(param_types, body_type)

    # ---- 函数/段落调用推断（核心：泛型参数推断） ----
    def _infer_function_call(self, expr) -> Type:
        """推断函数调用类型，支持 HM 风格泛型实例化。

        步骤：
        1. 推断实参类型
        2. 查找函数符号
        3. 实例化（将泛型类型变量替换为新鲜 TypeVar）
        4. 用实参与形参合一，得到替换
        5. 将替换应用到返回类型，得到具体返回类型
        6. 若在段体推断上下文中（self._hm_subs 存在），累积替换以便
           将参数 TypeVar 的约束反馈回段签名
        """
        # 分析参数
        arg_types = [self._infer_expr(a) for a in expr.arguments]

        # 获取函数名
        func_name = None
        if is_instance(expr.name, 'Identifier'):
            func_name = expr.name.name
        elif hasattr(expr.name, 'name'):
            func_name = expr.name.name

        if not func_name:
            return TYPE_UNKNOWN

        # 检查是否枚举变体构造函数
        if func_name in self.enum_defs:
            return self.enum_defs[func_name]
        for enum_name, enum_type in self.enum_defs.items():
            if func_name in getattr(enum_type, 'variants', {}):
                return enum_type

        # 查找符号（可能是泛型段/函数）
        symbol = self.symbol_table.lookup(func_name)

        # 显式类型参数（如 映射[T=数](...) 或 映射[数](...)）
        explicit_type_args = getattr(expr, 'type_args', None) or []

        if symbol and isinstance(symbol.data_type, FunctionType):
            func_type = symbol.data_type

            # --- HM 关键步骤：实例化泛型类型 ---
            instantiated = self._instantiate(func_type)

            # 检查参数数量
            if len(arg_types) != len(instantiated.param_types):
                self.errors.append(
                    f"函数 '{func_name}' 需要 {len(instantiated.param_types)} 个参数，"
                    f"但提供了 {len(arg_types)} 个"
                )
                return instantiated.return_type

            # ⭐ 可空类型强制检查：形参非可空时，实参不可为可空类型
            for i, (formal, actual) in enumerate(zip(instantiated.param_types, arg_types)):
                # 显式声明为可空的形参允许传入可空
                if isinstance(formal, OptionalTypeWrapper):
                    continue
                # 其他任意情况下，只要实参是可空的，就报告解包问题
                if isinstance(actual, (OptionalTypeWrapper, NullType)):
                    self.errors.append(
                        f"函数 '{func_name}' 第 {i + 1} 个参数类型不可空，"
                        f"但传入可空类型 {actual}，需要先使用 '!' 或 'unwrap()' 解包"
                    )

            # 若在段体推断上下文中，从 self._hm_subs 继承当前已知约束
            subs = getattr(self, '_hm_subs', None)
            if subs is not None:
                subs = subs.clone()
            else:
                subs = TypeSubstitution()

            # 处理显式类型参数
            if explicit_type_args:
                tvars_ordered = _collect_type_vars_ordered(instantiated)
                for i, expr_arg in enumerate(explicit_type_args):
                    if i < len(tvars_ordered):
                        tv_name = tvars_ordered[i]
                        concrete = self._parse_type_string(expr_arg) if isinstance(expr_arg, str) else TYPE_UNKNOWN
                        subs.bind(tv_name, concrete)

            # 通过参数与形参合一推断剩余类型变量
            for formal, actual in zip(instantiated.param_types, arg_types):
                try:
                    formal_applied = formal.apply_substitution(subs)
                    new_subs = unify(formal_applied, actual, subs)
                    subs = new_subs
                except UnificationError:
                    if not actual.is_subtype_of(formal):
                        self.errors.append(
                            f"函数 '{func_name}' 参数类型不匹配: "
                            f"期望 {formal}，实际 {actual}"
                        )

            # 将替换应用到返回类型得到具体返回类型
            resolved_return = instantiated.return_type.apply_substitution(subs)

            # ⭐ 累积约束到当前段的 HM 上下文（若存在）
            hm_subs = getattr(self, '_hm_subs', None)
            if hm_subs is not None:
                # 把 subs 中的新映射合并进 hm_subs
                for k, v in subs.mapping.items():
                    if k not in hm_subs.mapping:
                        hm_subs.mapping[k] = v
                    else:
                        # 已有映射：应用新替换后得到最具体类型
                        hm_subs.mapping[k] = hm_subs.mapping[k].apply_substitution(subs)

            return resolved_return

        # 符号存在但类型未知（如仅声明的段落）
        if symbol:
            return symbol.data_type or TYPE_UNKNOWN

        # 内置函数类型推断
        return self._infer_builtin_return(func_name, arg_types)

    def _infer_builtin_return(self, func_name: str, arg_types: List[Type]) -> Type:
        """推断内置函数返回类型"""
        # 普通内置函数
        builtin_returns = {
            '打印': TYPE_NULL,
            '显示': TYPE_NULL,
            '读取': TYPE_STRING,
            '长': TYPE_NUMBER,
            '长度': TYPE_NUMBER,
            '字符串长度': TYPE_NUMBER,
            '列表长度': TYPE_NUMBER,
            '转整数': TYPE_NUMBER,
            '转为整数': TYPE_NUMBER,
            '转浮点': TYPE_NUMBER,
            '转为浮点': TYPE_NUMBER,
            '转字符串': TYPE_STRING,
            '转为字符串': TYPE_STRING,
            '是整数': TYPE_BOOLEAN,
            '是浮点': TYPE_BOOLEAN,
            '是字符串': TYPE_BOOLEAN,
            '是列表': TYPE_BOOLEAN,
            '是字典': TYPE_BOOLEAN,
            '是空': TYPE_BOOLEAN,
            '文件存在': TYPE_BOOLEAN,
            '目录存在': TYPE_BOOLEAN,
            '排序': ListType(),
            '反转': ListType(),
            '求和': TYPE_NUMBER,
            '求最大': TYPE_NUMBER,
            '求最小': TYPE_NUMBER,
        }

        if func_name in builtin_returns:
            return builtin_returns[func_name]

        # 泛化处理：支持泛型的内置操作
        if arg_types:
            if func_name in ('列表追加', '列表添加'):
                if isinstance(arg_types[0], ListType):
                    return arg_types[0]
                if isinstance(arg_types[0], GenericTypeInstance) and arg_types[0].base_name in ('列表', 'List'):
                    return arg_types[0]
                return ListType()
            if func_name in ('映射',):
                # 映射[T](列表[T], T->T) -> 列表[T]（泛型）
                if len(arg_types) >= 1:
                    if isinstance(arg_types[0], ListType) and arg_types[0].element_type:
                        return ListType(arg_types[0].element_type)
                    if isinstance(arg_types[0], GenericTypeInstance) and arg_types[0].base_name in ('列表', 'List'):
                        if arg_types[0].type_args:
                            return ListType(arg_types[0].type_args[0])
                return ListType()
            if func_name.startswith('列表'):
                if isinstance(arg_types[0], ListType):
                    return arg_types[0]
                return ListType()
            if func_name.startswith('字典'):
                return DictType()

        return TYPE_UNKNOWN

    # ---- 公共辅助 ----
    def get_errors(self) -> List[str]:
        return self.errors

    def get_type_cache(self) -> Dict[int, Type]:
        return self.type_cache


# =============================================================================
# 辅助：按顺序收集函数签名中的类型变量
# =============================================================================

def _collect_type_vars_ordered(t: Type) -> List[str]:
    """按首次出现顺序收集类型变量名"""
    result: List[str] = []
    seen: Set[str] = set()

    def walk(node: Type):
        if isinstance(node, TypeVar):
            if node.name not in seen:
                seen.add(node.name)
                result.append(node.name)
        elif isinstance(node, FunctionType):
            for p in node.param_types:
                walk(p)
            walk(node.return_type)
        elif isinstance(node, ListType) and node.element_type:
            walk(node.element_type)
        elif isinstance(node, DictType):
            if node.key_type:
                walk(node.key_type)
            if node.value_type:
                walk(node.value_type)
        elif isinstance(node, GenericTypeInstance):
            for a in node.type_args:
                walk(a)
        elif isinstance(node, ClassType) and node.type_args:
            for a in node.type_args:
                walk(a)
        elif isinstance(node, FutureType):
            walk(node.inner_type)
        elif isinstance(node, OptionalTypeWrapper):
            walk(node.inner_type)
        elif isinstance(node, TupleType):
            for a in node.element_types:
                walk(a)
        elif isinstance(node, SetType) and node.element_type:
            walk(node.element_type)

    walk(t)
    return result


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言增强类型推断器测试 (Phase 1)")
    print("=" * 60)

    # 测试基本类型
    test_module = Module(
        statements=[
            VariableDeclaration(
                name='结果',
                value=BinaryOp(
                    left=NumberLiteral(value=3),
                    operator='+',
                    right=NumberLiteral(value=5)
                )
            ),
            ExpressionStatement(
                expression=BinaryOp(
                    left=StringLiteral(value='3 + 5 = '),
                    operator='+',
                    right=Identifier(name='结果')
                )
            )
        ]
    )

    inferencer = TypeInferencer()
    types = inferencer.infer(test_module)

    print("推断结果:")
    for stmt in test_module.statements:
        stmt_type = types.get(id(stmt), "?")
        print(f"  {type(stmt).__name__}: {stmt_type}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
