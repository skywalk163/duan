"""
段言（Duan）编程语言 AST 节点定义

与 src/ast_nodes.py 保持兼容的 AST 节点结构
供 ANTLR 解析器生成 AST 使用
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union, Any


# =============================================================================
# 基础节点
# =============================================================================

@dataclass(slots=True)
class ASTNode:
    """AST 节点基类"""
    line: int = 0
    column: int = 0


# =============================================================================
# 字面量节点
# =============================================================================

@dataclass(slots=True)
class NumberLiteral(ASTNode):
    """数字字面量"""
    value: Union[int, float] = 0


@dataclass(slots=True)
class StringLiteral(ASTNode):
    """字符串字面量"""
    value: str = ""


@dataclass(slots=True)
class BooleanLiteral(ASTNode):
    """布尔字面量"""
    value: bool = False


@dataclass(slots=True)
class NullLiteral(ASTNode):
    """空值字面量"""
    pass


@dataclass(slots=True)
class SelfReference(ASTNode):
    """self引用（己）"""
    pass


# =============================================================================
# 标识符与名称节点
# =============================================================================

@dataclass(slots=True)
class Identifier(ASTNode):
    """标识符（变量名、段落名引用等）"""
    name: str = ""


@dataclass(slots=True)
class SegmentName(ASTNode):
    """段落名（《名称》）"""
    name: str = ""


@dataclass(slots=True)
class ModuleName(ASTNode):
    """模块/篇名（【名称】）"""
    name: str = ""


# =============================================================================
# 表达式节点
# =============================================================================

@dataclass(slots=True)
class BinaryOp(ASTNode):
    """二元运算"""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None


@dataclass(slots=True)
class UnaryOp(ASTNode):
    """一元运算"""
    operator: str = ""
    operand: ASTNode = None


@dataclass(slots=True)
class FunctionCall(ASTNode):
    """函数/段落调用"""
    name: Union[SegmentName, Identifier] = None
    arguments: List[ASTNode] = field(default_factory=list)
    type_args: List[str] = field(default_factory=list)  # 显式类型参数（如 映射[数](...)）


@dataclass(slots=True)
class PipeExpression(ASTNode):
    """管道表达式（-> 或 并 连接）"""
    expressions: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class PropertyAccess(ASTNode):
    """属性访问（之字结构：对象之属性）"""
    obj: ASTNode = None
    property_name: str = ""


@dataclass(slots=True)
class IndexAccess(ASTNode):
    """索引访问（对象[索引]）"""
    obj: ASTNode = None
    index: ASTNode = None


@dataclass(slots=True)
class ListLiteral(ASTNode):
    """列表字面量"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class DictEntry(ASTNode):
    """典条目（键值对）"""
    key: ASTNode = None
    value: ASTNode = None


@dataclass(slots=True)
class DictLiteral(ASTNode):
    """典字面量（字典）"""
    entries: List[DictEntry] = field(default_factory=list)


@dataclass(slots=True)
class NewExpression(ASTNode):
    """类实例化表达式（新类名()）"""
    class_name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)
    type_args: List[str] = field(default_factory=list)  # 显式类型参数（如 数组[数](3)）


@dataclass(slots=True)
class ConditionalExpression(ASTNode):
    """三元条件表达式：如果 条件 那么 值1 否则 值2"""
    condition: ASTNode = None
    then_expr: ASTNode = None
    else_expr: Optional[ASTNode] = None


@dataclass(slots=True)
class StringInterpolation(ASTNode):
    """字符串插值："你好，{名字}" -> f-string"""
    parts: List[Union[str, ASTNode]] = field(default_factory=list)  # 交替的字符串和表达式


@dataclass(slots=True)
class ListComprehension(ASTNode):
    """列表推导：[表达式 遍历 变量 之 列表]"""
    expression: ASTNode = None          # 输出表达式
    variable: str = ""                   # 遍历变量
    iterable: ASTNode = None            # 可迭代对象
    condition: Optional[ASTNode] = None # 可选过滤条件


@dataclass(slots=True)
class LambdaExpression(ASTNode):
    """匿名函数：接收 甲：返回 甲 乘 甲。"""
    parameters: List[Parameter] = field(default_factory=list)
    body: ASTNode = None                # 表达式体


@dataclass(slots=True)
class MatchStatement(ASTNode):
    """模式匹配：匹配 值：情况 ... 结束。"""
    subject: ASTNode = None             # 被匹配的值
    cases: List['MatchCase'] = field(default_factory=list)


@dataclass(slots=True)
class MatchCase(ASTNode):
    """匹配分支"""
    pattern: 'MatchPattern' = None      # 匹配模式
    guard: Optional[ASTNode] = None     # 守卫条件（情况 模式 如果 条件）
    body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class MatchPattern(ASTNode):
    """匹配模式"""
    kind: str = ""                      # 'number', 'string', 'bool', 'null', 'variable', 'wildcard', 'list', 'type_check'
    value: Optional[ASTNode] = None     # 字面量值或变量名
    elements: List['MatchPattern'] = field(default_factory=list)  # 列表模式元素
    type_name: str = ""                 # 类型检查模式中的类型名
    binding: str = ""                   # 变量绑定名


@dataclass(slots=True)
class DictComprehension(ASTNode):
    """字典推导：{键: 值 遍历 变量 之 列表}"""
    key_expr: ASTNode = None            # 键表达式
    value_expr: ASTNode = None          # 值表达式
    variable: str = ""                   # 遍历变量
    iterable: ASTNode = None            # 可迭代对象
    condition: Optional[ASTNode] = None # 可选过滤条件


@dataclass(slots=True)
class DecoratorDefinition(ASTNode):
    """装饰器定义：@段落名 标注 段落 ..."""
    decorator_name: str = ""            # 装饰器段落名
    paragraph: 'SegmentDefinition' = None  # 被装饰的段落


@dataclass(slots=True)
class DestructuringAssignment(ASTNode):
    """解构赋值：设 (甲, 乙) 为 元组"""
    variables: List[str] = field(default_factory=list)  # 解构变量列表
    value: ASTNode = None               # 被解构的值


@dataclass(slots=True)
class WithStatement(ASTNode):
    """上下文管理器：使用 表达式 作为 变量：...结束。"""
    context_expr: ASTNode = None        # 上下文表达式
    variable: Optional[str] = None      # 可选的 as 变量
    body: List[ASTNode] = field(default_factory=list)


# =============================================================================
# 语句节点
# =============================================================================

@dataclass(slots=True)
class VariableDeclaration(ASTNode):
    """变量声明"""
    name: str = ""
    value: ASTNode = None
    type_annotation: Optional[str] = None
    is_mutable: bool = False
    destructure_names: List[str] = field(default_factory=list)  # 解构赋值变量名列表


@dataclass(slots=True)
class Assignment(ASTNode):
    """赋值语句"""
    target: ASTNode = None
    value: ASTNode = None


@dataclass(slots=True)
class CompoundAssignment(ASTNode):
    """复合赋值（甲 加上 1 → 甲 += 1）"""
    target: str = ""        # 变量名
    operator: str = ""      # '加', '减', '乘', '除', '模', '幂'
    value: ASTNode = None


@dataclass(slots=True)
class IfStatement(ASTNode):
    """条件语句"""
    condition: ASTNode = None
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: Optional[List[ASTNode]] = None
    elseif_conditions: List[ASTNode] = field(default_factory=list)
    elseif_bodies: List[List[ASTNode]] = field(default_factory=list)


@dataclass(slots=True)
class ForeachStatement(ASTNode):
    """遍历循环"""
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class WhileStatement(ASTNode):
    """当循环"""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class BreakStatement(ASTNode):
    """跳出语句"""
    pass


@dataclass(slots=True)
class ContinueStatement(ASTNode):
    """跳过语句"""
    pass


@dataclass(slots=True)
class ReturnStatement(ASTNode):
    """返回语句"""
    value: Optional[ASTNode] = None


@dataclass(slots=True)
class CatchClause(ASTNode):
    """捕获子句"""
    catch_type: str = ""
    catch_var: str = ""
    catch_body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class TryStatement(ASTNode):
    """异常捕获"""
    try_body: List[ASTNode] = field(default_factory=list)
    catch_clauses: List[CatchClause] = field(default_factory=list)
    catch_type: str = ""       # 异常类型（如 "ValueError"）- 向后兼容
    catch_var: str = ""         # 异常变量名 - 向后兼容
    catch_body: List[ASTNode] = field(default_factory=list)  # 向后兼容
    finally_body: List[ASTNode] = field(default_factory=list)  # finally 块


@dataclass(slots=True)
class ThrowStatement(ASTNode):
    """抛出异常"""
    value: ASTNode = None


@dataclass(slots=True)
class PrintStatement(ASTNode):
    """打印/输出语句"""
    value: ASTNode = None


@dataclass(slots=True)
class ExpressionStatement(ASTNode):
    """表达式语句"""
    expression: ASTNode = None


# =============================================================================
# 段落定义节点
# =============================================================================

@dataclass(slots=True)
class Parameter(ASTNode):
    """参数定义"""
    name: str = ""
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


# =============================================================================
# 异步/并发节点
# =============================================================================

@dataclass(slots=True)
class AwaitExpression(ASTNode):
    """等待表达式（等待 异步操作）"""
    expression: ASTNode = None


@dataclass(slots=True)
class DeferStatement(ASTNode):
    """推迟语句（推迟 语句 — 在作用域退出时执行）"""
    body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class AsyncScope(ASTNode):
    """并行作用域（结构化并发）：并行 { 任务1 任务2 }"""
    tasks: List[ASTNode] = field(default_factory=list)
    result_vars: List[str] = field(default_factory=list)  # 可选的返回结果变量
    timeout: Optional[ASTNode] = None  # 可选超时


@dataclass(slots=True)
class SegmentDefinition(ASTNode):
    """段落定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    modifiers: List[str] = field(default_factory=list)
    generic_params: List[str] = field(default_factory=list)  # 泛型参数列表（如 ["T", "U"]）


# =============================================================================
# 数据/错误类型定义
# =============================================================================

@dataclass(slots=True)
class DataTypeField(ASTNode):
    """数据类型字段"""
    name: str = ""
    type_annotation: str = ""


@dataclass(slots=True)
class AttributeDeclaration(ASTNode):
    """属性声明（类定义中使用）"""
    name: str = ""
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


@dataclass(slots=True)
class DataTypeDefinition(ASTNode):
    """数据类型定义"""
    name: str = ""
    fields: List[DataTypeField] = field(default_factory=list)


@dataclass(slots=True)
class ErrorTypeDefinition(ASTNode):
    """错误类型定义"""
    name: str = ""
    fields: List[DataTypeField] = field(default_factory=list)


# =============================================================================
# 类和接口定义
# =============================================================================

@dataclass(slots=True)
class MethodDefinition(ASTNode):
    """方法定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    is_static: bool = False
    generic_params: List[str] = field(default_factory=list)


@dataclass(slots=True)
class ConstructorDefinition(ASTNode):
    """构造函数定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class ClassDefinition(ASTNode):
    """类定义"""
    name: str = ""
    generic_params: List[str] = field(default_factory=list)  # 泛型参数列表
    superclasses: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    fields: List[ASTNode] = field(default_factory=list)  # 包含 varDecl
    methods: List[MethodDefinition] = field(default_factory=list)
    constructor: Optional[ConstructorDefinition] = None


@dataclass(slots=True)
class InterfaceMethod(ASTNode):
    """接口方法签名"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    return_type: str = ""


@dataclass(slots=True)
class InterfaceProperty(ASTNode):
    """接口属性签名"""
    name: str = ""
    type_annotation: str = ""


@dataclass(slots=True)
class InterfaceDefinition(ASTNode):
    """接口定义"""
    name: str = ""
    superinterfaces: List[str] = field(default_factory=list)
    methods: List[InterfaceMethod] = field(default_factory=list)
    properties: List[InterfaceProperty] = field(default_factory=list)


# =============================================================================
# 类型注解节点（泛型支持）
# =============================================================================

@dataclass(slots=True)
class GenericType(ASTNode):
    """泛型类型（如 列表[数]、字典[串, 数]）"""
    base_type: str = ""
    type_arguments: List[str] = field(default_factory=list)


@dataclass(slots=True)
class GenericParameterDecl(ASTNode):
    """泛型参数声明"""
    name: str = ""
    constraint: Optional[str] = None  # 可选的上界约束


# =============================================================================
# 枚举/代数数据类型（ADT）
# =============================================================================

@dataclass(slots=True)
class EnumVariant(ASTNode):
    """枚举变体"""
    name: str = ""
    fields: List[DataTypeField] = field(default_factory=list)  # 携带的数据字段


@dataclass(slots=True)
class EnumDefinition(ASTNode):
    """枚举/代数数据类型定义"""
    name: str = ""
    generic_params: List[str] = field(default_factory=list)
    variants: List[EnumVariant] = field(default_factory=list)
    derives: List[str] = field(default_factory=list)  # 派生 trait（如 相等, 比较）


# =============================================================================
# Trait/接口系统增强
# =============================================================================

@dataclass(slots=True)
class TraitMethodSignature(ASTNode):
    """Trait 方法签名"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    return_type: str = ""
    has_default: bool = False  # 是否有默认实现


@dataclass(slots=True)
class TraitDefinition(ASTNode):
    """Trait 定义"""
    name: str = ""
    generic_params: List[str] = field(default_factory=list)
    methods: List[TraitMethodSignature] = field(default_factory=list)
    super_traits: List[str] = field(default_factory=list)


@dataclass(slots=True)
class TraitImplementation(ASTNode):
    """Trait 实现"""
    trait_name: str = ""
    type_name: str = ""
    methods: List[MethodDefinition] = field(default_factory=list)
    generic_args: List[str] = field(default_factory=list)  # 泛型实参


# =============================================================================
# 空安全类型
# =============================================================================

@dataclass(slots=True)
class UnwrapExpression(ASTNode):
    """解包表达式（值! 或 unwrap(值)）"""
    value: Any = None


@dataclass(slots=True)
class OptionalType(ASTNode):
    """可空类型（如 数|空）"""
    inner_type: str = ""


# =============================================================================
# 类型别名
# =============================================================================

@dataclass(slots=True)
class TypeAlias(ASTNode):
    """类型别名定义"""
    name: str = ""
    target_type: str = ""
    generic_params: List[str] = field(default_factory=list)


# =============================================================================
# 模块节点
# =============================================================================

@dataclass(slots=True)
class ImportStatement(ASTNode):
    """导入语句"""
    module: str = ""
    names: List[str] = field(default_factory=list)


@dataclass(slots=True)
class ExportStatement(ASTNode):
    """导出语句"""
    name: str = ""


@dataclass(slots=True)
class Module(ASTNode):
    """模块（篇）- 顶层节点"""
    name: Optional[str] = None
    imports: List[ImportStatement] = field(default_factory=list)
    exports: List[ExportStatement] = field(default_factory=list)
    segments: List[SegmentDefinition] = field(default_factory=list)
    classes: List[ClassDefinition] = field(default_factory=list)
    interfaces: List[InterfaceDefinition] = field(default_factory=list)
    data_types: List[DataTypeDefinition] = field(default_factory=list)
    error_types: List[ErrorTypeDefinition] = field(default_factory=list)
    statements: List[ASTNode] = field(default_factory=list)
    # 新类型定义
    enums: List[EnumDefinition] = field(default_factory=list)
    trait_defs: List[TraitDefinition] = field(default_factory=list)
    trait_impls: List[TraitImplementation] = field(default_factory=list)
    type_aliases: List[TypeAlias] = field(default_factory=list)


# =============================================================================
# 辅助函数
# =============================================================================

def ast_to_dict(node: ASTNode) -> dict:
    """将 AST 节点转换为字典（用于序列化）"""
    if isinstance(node, ASTNode):
        result = {'type': node.__class__.__name__}
        for field_name in node.__dataclass_fields__:
            value = getattr(node, field_name)
            if isinstance(value, list):
                result[field_name] = [ast_to_dict(item) for item in value]
            elif isinstance(value, ASTNode):
                result[field_name] = ast_to_dict(value)
            else:
                result[field_name] = value
        return result
    return node