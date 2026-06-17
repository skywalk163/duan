"""
段言（Duan）编程语言 - 增强类型推断器

类型定义从 type_system 模块导入。
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import sys
import os

from type_system import *


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
    TypeAlias, OptionalType,
)
# =============================================================================
# 类型推断器
# =============================================================================

class TypeInferencer:
    """段言增强类型推断器"""

    def __init__(self):
        self.symbol_table = TypeSymbolTable()
        self.type_cache: Dict[int, Type] = {}  # AST节点ID → 类型
        self.errors: List[str] = []

        # 注册内置类型
        self._init_builtin_types()

        # 当前正在推断的函数返回类型
        self._current_return_type: Optional[Type] = None

        # 是否在异步函数中
        self._in_async_function: bool = False

        # 已知的枚举定义（名称 → EnumType）
        self.enum_defs: Dict[str, EnumType] = {}

        # 已知的 trait 定义（名称 → TraitType）
        self.trait_defs: Dict[str, TraitType] = {}

        # trait 实现（(trait名, 类型名) → 方法名 → FunctionType）
        self.trait_impls: Dict[Tuple[str, str], Dict[str, FunctionType]] = {}

    def _init_builtin_types(self):
        """初始化内置类型"""
        # 内置类型名
        self._builtin_type_names = {'数', '串', '布尔', '空', '列表', '字典', '任意'}

    def _parse_type_string(self, type_str: str) -> Type:
        """将类型字符串解析为 Type 对象"""
        if not type_str:
            return TYPE_UNKNOWN

        # 检查是否为可空类型（如 "数|空"）
        if '|空' in type_str:
            inner = type_str.replace('|空', '').strip()
            return OptionalTypeWrapper(self._parse_type_string(inner))

        # 检查是否为泛型类型（如 "列表[数]"）
        if '[' in type_str and type_str.endswith(']'):
            bracket_idx = type_str.index('[')
            base_name = type_str[:bracket_idx]
            args_str = type_str[bracket_idx + 1:-1]
            # 解析逗号分隔的参数（处理嵌套括号）
            args = self._split_type_args(args_str)
            type_args = [self._parse_type_string(a.strip()) for a in args]
            return GenericTypeInstance(base_name, type_args)

        # 检查是否为泛型参数
        if type_str[0].isupper() or type_str.startswith('T'):
            param = self.symbol_table.resolve_type_param(type_str)
            if param:
                return param

        # 基本类型映射
        type_map = {
            '数': TYPE_NUMBER,
            '串': TYPE_STRING,
            '布尔': TYPE_BOOLEAN,
            '空': TYPE_NULL,
            '列表': ListType(),
            '字典': DictType(),
            '任意': TYPE_ANY,
        }
        return type_map.get(type_str, TYPE_UNKNOWN)

    def _split_type_args(self, args_str: str) -> List[str]:
        """分割类型参数（处理嵌套括号）"""
        args = []
        depth = 0
        current = []
        for ch in args_str:
            if ch in '[(':
                depth += 1
                current.append(ch)
            elif ch in '])':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                args.append(''.join(current).strip())
                current = []
            else:
                current.append(ch)
        if current:
            args.append(''.join(current).strip())
        return args

    def register_enum(self, enum_def: EnumDefinition):
        """注册枚举类型"""
        variants = {}
        for variant in enum_def.variants:
            field_types = []
            for field in variant.fields:
                field_types.append(self._parse_type_string(field.type_annotation))
            variants[variant.name] = field_types

        enum_type = EnumType(
            enum_name=enum_def.name,
            variants=variants,
            generic_params=enum_def.generic_params
        )
        self.enum_defs[enum_def.name] = enum_type
        self.symbol_table.define(enum_def.name, 'enum', enum_type)

    def register_trait(self, trait_def: TraitDefinition):
        """注册 trait 定义"""
        methods = {}
        for method in trait_def.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            methods[method.name] = FunctionType(param_types, return_type)

        trait_type = TraitType(trait_name=trait_def.name, methods=methods)
        self.trait_defs[trait_def.name] = trait_type

    def register_trait_impl(self, impl: TraitImplementation):
        """注册 trait 实现"""
        key = (impl.trait_name, impl.type_name)
        methods = {}
        for method in impl.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            methods[method.name] = FunctionType(param_types, return_type)
        self.trait_impls[key] = methods

        # 类型实现 trait 检查
        if impl.trait_name in self.trait_defs:
            required = self.trait_defs[impl.trait_name]
            for method_name, func_type in required.methods.items():
                if method_name not in methods:
                    self.errors.append(
                        f"类型 '{impl.type_name}' 未实现 trait '{impl.trait_name}' "
                        f"的必需方法 '{method_name}'"
                    )

    def infer(self, module: Module) -> Dict[int, Type]:
        """对整个模块进行类型推断"""
        self.type_cache = {}
        self.symbol_table = TypeSymbolTable()
        self.errors = []
        self.enum_defs = {}
        self.trait_defs = {}
        self.trait_impls = {}

        # 第一阶段：注册所有类型定义（枚举、trait、类）
        self._scan_type_definitions(module)

        # 第二阶段：注册 trait 实现
        for impl in getattr(module, 'trait_impls', []):
            self.register_trait_impl(impl)

        # 第三阶段：推断所有定义和语句
        self._infer_module(module)

        return self.type_cache

    def _scan_type_definitions(self, module: Module):
        """扫描所有类型定义（建立符号表）"""
        # 注册枚举
        for enum_def in getattr(module, 'enums', []):
            self.register_enum(enum_def)

        # 注册 trait
        for trait_def in getattr(module, 'trait_defs', []):
            self.register_trait(trait_def)

        # 注册类
        if hasattr(module, 'classes'):
            for cls in module.classes:
                self.symbol_table.define(cls.name, 'class', ClassType(cls.name))

        # 注册段落/函数
        if hasattr(module, 'segments'):
            for segment in module.segments:
                self.symbol_table.define(segment.name, 'function', TYPE_UNKNOWN)

    def _infer_module(self, module: Module):
        """推断模块"""
        # 处理枚举定义（创建类型）
        for enum_def in getattr(module, 'enums', []):
            self._infer_enum_def(enum_def)

        # 处理 trait 定义
        for trait_def in getattr(module, 'trait_defs', []):
            self._infer_trait_def(trait_def)

        # 处理类定义
        if hasattr(module, 'classes'):
            for cls in module.classes:
                self._infer_class(cls)

        # 处理段落定义
        if hasattr(module, 'segments'):
            for segment in module.segments:
                self._infer_segment(segment)

        # 处理语句
        if hasattr(module, 'statements'):
            for stmt in module.statements:
                self._infer_statement(stmt)

    def _infer_enum_def(self, enum_def: EnumDefinition):
        """推断枚举定义"""
        self.symbol_table.enter_scope()

        # 注册泛型参数
        for gp in enum_def.generic_params:
            self.symbol_table.define_generic_param(gp)

        # 注册变体（每个变体名可当作构造函数）
        for variant in enum_def.variants:
            field_types = [self._parse_type_string(f.type_annotation) for f in variant.fields]
            if field_types:
                func_type = FunctionType(field_types, self.enum_defs.get(enum_def.name, EnumType(enum_name=enum_def.name)))
            else:
                func_type = FunctionType([], self.enum_defs.get(enum_def.name, EnumType(enum_name=enum_def.name)))
            self.symbol_table.define(variant.name, 'function', func_type)

        self.symbol_table.exit_scope()

    def _infer_trait_def(self, trait_def: TraitDefinition):
        """推断 trait 定义"""
        # 注册方法签名
        for method in trait_def.methods:
            param_types = [self._parse_type_string(p.type_annotation) for p in method.parameters]
            return_type = self._parse_type_string(method.return_type)
            func_type = FunctionType(param_types, return_type)
            # 将 trait 方法注册到符号表
            self.symbol_table.define(method.name, 'function', func_type)

    def _infer_class(self, cls: ClassDefinition):
        """推断类"""
        self.symbol_table.enter_scope()

        # 注册泛型参数
        for gp in cls.generic_params:
            self.symbol_table.define_generic_param(gp)

        # 处理构造函数
        if cls.constructor:
            self._infer_constructor(cls.constructor)

        # 处理方法
        for method in cls.methods:
            self._infer_method(method)

        self.symbol_table.exit_scope()

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

        # 定义 self 参数
        self.symbol_table.define('己', 'parameter', TYPE_ANY)

        for param in method.parameters:
            param_type = self._parse_type_string(param.type_annotation)
            self.symbol_table.define(param.name, 'parameter', param_type)

        # 设置返回类型
        if method.return_type:
            self._current_return_type = self._parse_type_string(method.return_type)
        else:
            self._current_return_type = None

        for stmt in method.body:
            self._infer_statement(stmt)

        self._current_return_type = None
        self.symbol_table.exit_scope()

    def _infer_segment(self, segment: SegmentDefinition):
        """推断段落（函数）"""
        self.symbol_table.enter_scope()

        # 检查是否为异步函数
        is_async = '异步' in segment.modifiers
        if is_async:
            self._in_async_function = True

        # 注册泛型参数
        if hasattr(segment, 'generic_params'):
            for gp in segment.generic_params:
                self.symbol_table.define_generic_param(gp)

        for param in segment.parameters:
            param_type = self._parse_type_string(param.type_annotation)
            self.symbol_table.define(param.name, 'parameter', param_type)

        # 设置返回类型
        if segment.return_type:
            raw_type = self._parse_type_string(segment.return_type)
            self._current_return_type = raw_type
            # 异步函数返回类型包装为 FutureType
            if is_async:
                self._current_return_type = FutureType(raw_type)

        for stmt in segment.body:
            self._infer_statement(stmt)

        self._current_return_type = None
        if is_async:
            self._in_async_function = False
        self.symbol_table.exit_scope()

    def _infer_defer_stmt(self, stmt: DeferStatement):
        """推断推迟语句"""
        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
        self.type_cache[id(stmt)] = TYPE_NULL

    def _infer_async_scope(self, stmt: AsyncScope):
        """推断并行作用域（结构化并发）"""
        for task in stmt.tasks:
            self._infer_expr(task)
        self.type_cache[id(stmt)] = ListType()

    def _infer_statement(self, stmt):
        """推断语句类型"""
        if stmt is None:
            return

        node_type = type(stmt).__name__

        # 变量声明
        if is_instance(stmt, 'VariableDeclaration'):
            self._infer_var_decl(stmt)

        # 赋值语句
        elif is_instance(stmt, 'Assignment'):
            self._infer_assignment(stmt)

        # 条件语句
        elif is_instance(stmt, 'IfStatement'):
            self._infer_if_stmt(stmt)

        # 循环语句
        elif is_instance(stmt, 'ForeachStatement'):
            self._infer_foreach_stmt(stmt)

        elif is_instance(stmt, 'WhileStatement'):
            self._infer_while_stmt(stmt)

        # 返回语句
        elif is_instance(stmt, 'ReturnStatement'):
            self._infer_return_stmt(stmt)

        # Match 语句（模式匹配）
        elif is_instance(stmt, 'MatchStatement'):
            self._infer_match_stmt(stmt)

        # 表达式语句
        elif is_instance(stmt, 'ExpressionStatement'):
            self._infer_expr(stmt.expression)

        # 打印语句
        elif is_instance(stmt, 'PrintStatement'):
            if hasattr(stmt, 'value'):
                self._infer_expr(stmt.value)

        # 抛出语句
        elif is_instance(stmt, 'ThrowStatement'):
            if hasattr(stmt, 'value'):
                self._infer_expr(stmt.value)

        # 函数调用作为语句
        elif is_instance(stmt, 'FunctionCall'):
            self._infer_expr(stmt)

        # 段落定义（内嵌）
        elif is_instance(stmt, 'SegmentDefinition'):
            self._infer_segment(stmt)

        # 推迟语句（defer）
        elif is_instance(stmt, 'DeferStatement'):
            self._infer_defer_stmt(stmt)

        # 并行作用域（结构化并发）
        elif is_instance(stmt, 'AsyncScope'):
            self._infer_async_scope(stmt)

        # 空语句
        elif is_instance(stmt, 'BreakStatement') or is_instance(stmt, 'ContinueStatement'):
            pass

    def _infer_var_decl(self, stmt):
        """推断变量声明"""
        expr_type = self._infer_expr(stmt.value)

        # 检查类型注解
        type_annotation = getattr(stmt, 'type_annotation', None)
        if type_annotation:
            anno_type = self._parse_type_string(type_annotation)
            if not expr_type.is_subtype_of(anno_type):
                self.errors.append(
                    f"类型不匹配: 变量 '{stmt.name}' 声明为 {anno_type}，"
                    f"但初始值类型为 {expr_type}"
                )
            expr_type = anno_type

        # 可空性检查
        if isinstance(expr_type, NullType):
            # 变量被赋值为空，检查是否有类型注解且不可空
            if type_annotation and '|空' not in type_annotation:
                self.errors.append(
                    f"空安全错误: 变量 '{stmt.name}' 声明为不可空类型 {type_annotation}，"
                    f"但不能赋值为空"
                )

        is_mutable = getattr(stmt, 'is_mutable', False)
        self.symbol_table.define(stmt.name, 'variable', expr_type, is_mutable)
        self.type_cache[id(stmt)] = expr_type

    def _infer_assignment(self, stmt):
        """推断赋值语句"""
        value_type = self._infer_expr(stmt.value)

        if is_instance(stmt.target, 'Identifier'):
            target_name = stmt.target.name
            symbol = self.symbol_table.lookup(target_name)
            if symbol:
                # 检查不可变变量赋值
                if not symbol.is_mutable:
                    self.errors.append(
                        f"不可变变量 '{target_name}' 不能重新赋值"
                    )
                # 类型兼容检查
                if not value_type.is_subtype_of(symbol.data_type):
                    self.errors.append(
                        f"类型不匹配: 变量 '{target_name}' 类型为 {symbol.data_type}，"
                        f"不能赋值为 {value_type}"
                    )
                self.symbol_table.update_type(target_name, value_type)
            self.type_cache[id(stmt)] = value_type

        elif is_instance(stmt.target, 'PropertyAccess'):
            self._infer_expr(stmt.target)
            self.type_cache[id(stmt)] = value_type

    def _infer_if_stmt(self, stmt):
        """推断条件语句"""
        cond_type = self._infer_expr(stmt.condition)

        # 条件必须是布尔类型
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

        # 处理 elseif 分支
        for elseif_body in getattr(stmt, 'elseif_bodies', []):
            self.symbol_table.enter_scope()
            for s in elseif_body:
                self._infer_statement(s)
            self.symbol_table.exit_scope()

    def _infer_foreach_stmt(self, stmt):
        """推断遍历循环"""
        iter_type = self._infer_expr(stmt.iterable)

        self.symbol_table.enter_scope()

        # 推断循环变量类型
        if isinstance(iter_type, ListType):
            var_type = iter_type.element_type or TYPE_UNKNOWN
        elif isinstance(iter_type, StringType):
            var_type = TYPE_STRING
        else:
            var_type = TYPE_UNKNOWN
        self.symbol_table.define(stmt.variable, 'variable', var_type)

        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()

    def _infer_while_stmt(self, stmt):
        """推断当循环"""
        cond_type = self._infer_expr(stmt.condition)

        if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
            self.errors.append(
                f"循环条件类型应为布尔，实际为 {cond_type}"
            )

        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()

    def _infer_return_stmt(self, stmt):
        """推断返回语句"""
        if stmt.value:
            return_type = self._infer_expr(stmt.value)

            # 检查返回类型是否匹配
            if self._current_return_type and not return_type.is_subtype_of(self._current_return_type):
                self.errors.append(
                    f"返回类型不匹配: 期望 {self._current_return_type}，"
                    f"实际为 {return_type}"
                )
            self.type_cache[id(stmt)] = return_type
        else:
            if self._current_return_type and not isinstance(self._current_return_type, NullType):
                self.errors.append(
                    f"返回类型不匹配: 期望 {self._current_return_type}，"
                    f"但无返回值"
                )

    def _infer_match_stmt(self, stmt):
        """推断模式匹配语句"""
        subject_type = self._infer_expr(stmt.subject)
        self.type_cache[id(stmt)] = TYPE_UNKNOWN

        # 检查枚举穷尽性
        if isinstance(subject_type, EnumType):
            matched_variants = set()
            for case in stmt.cases:
                pattern = case.pattern
                variant_name = self._get_pattern_variant_name(pattern)
                if variant_name:
                    matched_variants.add(variant_name)

                # 推断分支体
                self.symbol_table.enter_scope()

                # 如果模式有绑定，在作用域中添加
                if pattern and pattern.binding:
                    binding_type = self._get_binding_type(subject_type, pattern)
                    self.symbol_table.define(pattern.binding, 'variable', binding_type)

                # 如果有守卫条件，推断它
                if case.guard:
                    guard_type = self._infer_expr(case.guard)
                    if not isinstance(guard_type, (BooleanType, AnyType, UnknownType)):
                        self.errors.append(
                            f"匹配守卫条件类型应为布尔，实际为 {guard_type}"
                        )

                for s in case.body:
                    self._infer_statement(s)
                self.symbol_table.exit_scope()

            # 检查是否匹配了所有变体
            # 检查最后是否有通配符 _
            has_wildcard = any(
                self._is_wildcard_pattern(c.pattern) for c in stmt.cases
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
            # 非枚举类型，正常推断所有分支
            for case in stmt.cases:
                self.symbol_table.enter_scope()
                for s in case.body:
                    self._infer_statement(s)
                self.symbol_table.exit_scope()

    def _get_pattern_variant_name(self, pattern) -> Optional[str]:
        """获取模式中的变体名"""
        if pattern is None:
            return None
        if hasattr(pattern, 'kind') and pattern.kind == 'variable':
            # 可能是变体名（大写开头）
            if hasattr(pattern, 'value') and isinstance(pattern.value, str) and pattern.value[0].isupper():
                return pattern.value
        if hasattr(pattern, 'kind') and pattern.kind == 'type_check':
            return pattern.type_name
        return None

    def _is_wildcard_pattern(self, pattern) -> bool:
        """检查是否为通配符模式"""
        if pattern is None:
            return False
        return getattr(pattern, 'kind', '') == 'wildcard'

    def _get_binding_type(self, enum_type: EnumType, pattern) -> Type:
        """获取模式绑定的类型"""
        return TYPE_UNKNOWN

    def _infer_expr(self, expr) -> Type:
        """推断表达式类型"""
        if expr is None:
            return TYPE_NULL

        # 检查缓存
        if id(expr) in self.type_cache:
            return self.type_cache[id(expr)]

        node_type = type(expr).__name__
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

        # 标识符
        elif is_instance(expr, 'Identifier'):
            symbol = self.symbol_table.lookup(expr.name)
            if symbol:
                result_type = symbol.data_type
            else:
                # 检查是否枚举变体
                if expr.name in self.enum_defs:
                    result_type = EnumType(enum_name=expr.name)
                else:
                    result_type = TYPE_UNKNOWN

        # 二元运算
        elif is_instance(expr, 'BinaryOp'):
            left_type = self._infer_expr(expr.left)
            right_type = self._infer_expr(expr.right)

            op = expr.operator

            # 加法/连接
            if op in ['+', '加']:
                if isinstance(left_type, StringType) and isinstance(right_type, StringType):
                    result_type = TYPE_STRING
                elif isinstance(left_type, NumberType) and isinstance(right_type, NumberType):
                    result_type = TYPE_NUMBER
                elif isinstance(left_type, StringType) or isinstance(right_type, StringType):
                    # 混合类型：一个字符串一个数字 -> 结果是字符串
                    result_type = TYPE_STRING
                elif isinstance(left_type, UnknownType) or isinstance(right_type, UnknownType):
                    # 未知类型时保持为未知，不强制推断
                    result_type = TYPE_UNKNOWN
                else:
                    # 其他情况默认为数字
                    result_type = TYPE_NUMBER

            # 算术运算
            elif op in ['-', '减', '*', '乘', '/', '除', '%', '模', '^', '幂']:
                if isinstance(left_type, NumberType) and isinstance(right_type, NumberType):
                    result_type = TYPE_NUMBER
                else:
                    self.errors.append(f"算术运算 '{op}' 需要数字类型，但得到 {left_type} 和 {right_type}")
                    result_type = TYPE_NUMBER

            # 比较运算
            elif op in ['>', '<', '>=', '<=', '==', '!=', '等于', '不等于', '大于', '小于', '大于等于', '小于等于']:
                result_type = TYPE_BOOLEAN

            # 逻辑运算
            elif op in ['且', '与', '或']:
                result_type = TYPE_BOOLEAN

            else:
                result_type = TYPE_UNKNOWN

        # 一元运算
        elif is_instance(expr, 'UnaryOp'):
            operand_type = self._infer_expr(expr.operand)

            if expr.operator in ['-', '非', 'not']:
                result_type = TYPE_BOOLEAN if isinstance(operand_type, BooleanType) else TYPE_NUMBER
            else:
                result_type = TYPE_UNKNOWN

        # 函数调用
        elif is_instance(expr, 'FunctionCall'):
            result_type = self._infer_function_call(expr)

        # 属性访问
        elif is_instance(expr, 'PropertyAccess'):
            obj_type = self._infer_expr(expr.obj)
            result_type = TYPE_UNKNOWN

        # 索引访问
        elif is_instance(expr, 'IndexAccess'):
            obj_type = self._infer_expr(expr.obj)
            index_type = self._infer_expr(expr.index)

            if isinstance(obj_type, ListType):
                result_type = obj_type.element_type or TYPE_UNKNOWN
            elif isinstance(obj_type, StringType):
                result_type = TYPE_STRING
            elif isinstance(obj_type, DictType):
                result_type = obj_type.value_type or TYPE_UNKNOWN
            else:
                result_type = TYPE_UNKNOWN

        # 列表字面量
        elif is_instance(expr, 'ListLiteral'):
            element_types = [self._infer_expr(e) for e in expr.elements]
            if element_types:
                first_type = element_types[0]
                if all(t == first_type for t in element_types):
                    result_type = ListType(first_type)
                else:
                    result_type = ListType()
            else:
                result_type = ListType()

        # 字典字面量
        elif is_instance(expr, 'DictLiteral'):
            for entry in expr.entries:
                self._infer_expr(entry.key)
                self._infer_expr(entry.value)
            result_type = DictType()

        # 类实例化
        elif is_instance(expr, 'NewExpression'):
            for arg in expr.arguments:
                self._infer_expr(arg)
            result_type = ClassType(expr.class_name)

        # Self引用
        elif is_instance(expr, 'SelfReference'):
            result_type = TYPE_ANY

        # 列表推导
        elif is_instance(expr, 'ListComprehension'):
            iter_type = self._infer_expr(expr.iterable)
            self.symbol_table.enter_scope()
            if isinstance(iter_type, ListType):
                self.symbol_table.define(expr.variable, 'variable', iter_type.element_type or TYPE_UNKNOWN)
            else:
                self.symbol_table.define(expr.variable, 'variable', TYPE_UNKNOWN)
            if expr.condition:
                cond_type = self._infer_expr(expr.condition)
                if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
                    self.errors.append(f"列表推导过滤条件类型应为布尔，实际为 {cond_type}")
            elem_type = self._infer_expr(expr.expression)
            self.symbol_table.exit_scope()
            result_type = ListType(elem_type)

        # Lambda 表达式
        elif is_instance(expr, 'LambdaExpression'):
            self.symbol_table.enter_scope()
            param_types = []
            for param in expr.parameters:
                ptype = self._parse_type_string(param.type_annotation)
                self.symbol_table.define(param.name, 'parameter', ptype)
                param_types.append(ptype)
            body_type = self._infer_expr(expr.body)
            self.symbol_table.exit_scope()
            result_type = FunctionType(param_types, body_type)

        # 字符串插值
        elif is_instance(expr, 'StringInterpolation'):
            for part in expr.parts:
                if not isinstance(part, str):
                    self._infer_expr(part)
            result_type = TYPE_STRING

        # 条件表达式（三元）
        elif is_instance(expr, 'ConditionalExpression'):
            cond_type = self._infer_expr(expr.condition)
            if not isinstance(cond_type, (BooleanType, AnyType, UnknownType)):
                self.errors.append(f"条件表达式类型应为布尔，实际为 {cond_type}")
            then_type = self._infer_expr(expr.then_expr)
            if expr.else_expr:
                else_type = self._infer_expr(expr.else_expr)
                result_type = then_type  # 简化：使用 then 分支类型
            else:
                result_type = then_type

        # 管道表达式
        elif is_instance(expr, 'PipeExpression'):
            for sub_expr in expr.expressions:
                self._infer_expr(sub_expr)
            result_type = TYPE_UNKNOWN

        # 异步等待表达式
        elif is_instance(expr, 'AwaitExpression'):
            inner_type = self._infer_expr(expr.expression)
            # await 等待一个 Future，解包出内部类型
            if isinstance(inner_type, FutureType):
                result_type = inner_type.inner_type
            else:
                result_type = inner_type

        else:
            result_type = TYPE_UNKNOWN

        # 缓存结果
        self.type_cache[id(expr)] = result_type
        return result_type

    def _infer_function_call(self, expr) -> Type:
        """推断函数调用"""
        # 分析参数
        arg_types = []
        for arg in expr.arguments:
            arg_type = self._infer_expr(arg)
            arg_types.append(arg_type)

        # 获取函数名
        func_name = None
        if is_instance(expr.name, 'Identifier'):
            func_name = expr.name.name
        elif hasattr(expr.name, 'name'):
            func_name = expr.name.name

        if not func_name:
            return TYPE_UNKNOWN

        # 检查是否是枚举变体构造函数
        if func_name in self.enum_defs:
            return self.enum_defs[func_name]

        # 检查是否在枚举变体中（变体名作为构造函数）
        for enum_name, enum_type in self.enum_defs.items():
            if func_name in enum_type.variants:
                return enum_type

        # 查找函数定义
        symbol = self.symbol_table.lookup(func_name)
        if symbol and isinstance(symbol.data_type, FunctionType):
            func_type = symbol.data_type
            # 检查参数数量
            if len(arg_types) != len(func_type.param_types):
                self.errors.append(
                    f"函数 '{func_name}' 需要 {len(func_type.param_types)} 个参数，"
                    f"但提供了 {len(arg_types)} 个"
                )
            return func_type.return_type

        # 检查是否在符号表中（简化处理）
        if symbol:
            return symbol.data_type or TYPE_UNKNOWN

        # 内置函数类型推断
        result_type = self._infer_builtin_return(func_name, arg_types)
        return result_type

    def _infer_builtin_return(self, func_name: str, arg_types: List[Type]) -> Type:
        """推断内置函数返回类型"""
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

        # 泛化处理：尝试从参数类型推断
        if arg_types:
            # 类似 列表获取、列表追加 等操作
            if func_name.startswith('列表'):
                if arg_types and isinstance(arg_types[0], ListType):
                    return arg_types[0]
                return TYPE_UNKNOWN

            if func_name.startswith('字典'):
                return TYPE_UNKNOWN

        return TYPE_UNKNOWN

    def get_errors(self) -> List[str]:
        """获取收集到的类型错误"""
        return self.errors

    def get_type_cache(self) -> Dict[int, Type]:
        """获取类型缓存"""
        return self.type_cache


# =============================================================================
# 辅助函数
# =============================================================================

def is_instance(node, class_name):
    """检查节点类型（通过名称检查，支持多个模块）"""
    if node is None:
        return False
    return type(node).__name__ == class_name


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言增强类型推断器测试")
    print("=" * 60)

    # 测试基本类型
    print("\n--- 基本类型推断 ---")
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

    # 测试枚举
    print("\n--- 枚举类型 ---")
    test_enum = EnumDefinition(
        name='选项',
        variants=[
            EnumVariant(name='是', fields=[]),
            EnumVariant(name='否', fields=[]),
            EnumVariant(name='未知', fields=[]),
        ]
    )

    # 测试类型错误
    print("\n--- 类型错误检查 ---")
    test_module2 = Module(
        statements=[
            VariableDeclaration(
                name='数值',
                value=NumberLiteral(value=42)
            ),
            ExpressionStatement(
                expression=BinaryOp(
                    left=Identifier(name='数值'),
                    operator='加',
                    right=StringLiteral(value='hello')
                )
            )
        ]
    )
    inferencer2 = TypeInferencer()
    inferencer2.infer(test_module2)
    if inferencer2.get_errors():
        print("发现的类型错误:")
        for err in inferencer2.get_errors():
            print(f"  - {err}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)