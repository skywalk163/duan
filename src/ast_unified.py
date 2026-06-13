"""
段言（Duan）编程语言 - 统一 AST 节点定义

合并自：
- src/ast_nodes.py（手写解析器）
- antlrparser/duan_ast.py（ANTLR解析器）

用于支持双后端：Python后端和LLVM后端
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Any


# =============================================================================
# 基础节点
# =============================================================================

@dataclass
class ASTNode:
    """AST 节点基类"""
    line: int = 0
    column: int = 0


# =============================================================================
# 字面量节点
# =============================================================================

@dataclass
class NumberLiteral(ASTNode):
    """数字字面量"""
    value: Union[int, float] = 0


@dataclass
class StringLiteral(ASTNode):
    """字符串字面量"""
    value: str = ""


@dataclass
class BooleanLiteral(ASTNode):
    """布尔字面量"""
    value: bool = False


@dataclass
class NullLiteral(ASTNode):
    """空值字面量"""
    pass


@dataclass
class ListLiteral(ASTNode):
    """列表字面量"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class DictEntry(ASTNode):
    """典条目（键值对）"""
    key: ASTNode = None
    value: ASTNode = None


@dataclass
class DictLiteral(ASTNode):
    """典字面量（字典）"""
    entries: List[DictEntry] = field(default_factory=list)


# =============================================================================
# 标识符节点
# =============================================================================

@dataclass
class Identifier(ASTNode):
    """标识符（变量名、段落名引用等）"""
    name: str = ""


@dataclass
class SegmentName(ASTNode):
    """段落名（《名称》）"""
    name: str = ""


@dataclass
class ModuleName(ASTNode):
    """模块/篇名（【名称】）"""
    name: str = ""


# =============================================================================
# 表达式节点
# =============================================================================

@dataclass
class BinaryOp(ASTNode):
    """二元运算"""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None


@dataclass
class UnaryOp(ASTNode):
    """一元运算"""
    operator: str = ""
    operand: ASTNode = None


@dataclass
class FunctionCall(ASTNode):
    """函数/段落调用"""
    name: Union[SegmentName, Identifier] = None
    arguments: List[ASTNode] = field(default_factory=list)


@dataclass
class PipeExpression(ASTNode):
    """管道表达式（-> 或 并 连接）"""
    expressions: List[ASTNode] = field(default_factory=list)


@dataclass
class PropertyAccess(ASTNode):
    """属性访问（之字结构：对象之属性）"""
    obj: ASTNode = None
    property_name: str = ""


@dataclass
class IndexAccess(ASTNode):
    """索引访问（对象[索引]）"""
    obj: ASTNode = None
    index: ASTNode = None


@dataclass
class MethodCall(ASTNode):
    """方法调用（主谓结构：对象.方法()）"""
    obj: ASTNode = None
    method: str = ""
    arguments: List[ASTNode] = field(default_factory=list)


@dataclass
class SelfReference(ASTNode):
    """self 引用（己）"""
    pass


@dataclass
class NewExpression(ASTNode):
    """类实例化表达式（新建 类名()）"""
    class_name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)


# 别名：ClassInstantiation = NewExpression（兼容src）
ClassInstantiation = NewExpression


# =============================================================================
# 语句节点
# =============================================================================

@dataclass
class VariableDeclaration(ASTNode):
    """变量声明"""
    name: str = ""
    value: ASTNode = None


@dataclass
class Assignment(ASTNode):
    """赋值语句"""
    target: ASTNode = None
    value: ASTNode = None


@dataclass
class IfStatement(ASTNode):
    """条件语句"""
    condition: ASTNode = None
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: Optional[List[ASTNode]] = None
    elseif_conditions: List[ASTNode] = field(default_factory=list)
    elseif_bodies: List[List[ASTNode]] = field(default_factory=list)


@dataclass
class ForeachStatement(ASTNode):
    """遍历循环"""
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileStatement(ASTNode):
    """当循环"""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class BreakStatement(ASTNode):
    """跳出语句"""
    pass


@dataclass
class ContinueStatement(ASTNode):
    """跳过语句"""
    pass


@dataclass
class ReturnStatement(ASTNode):
    """返回语句"""
    value: Optional[ASTNode] = None


@dataclass
class TryStatement(ASTNode):
    """异常捕获"""
    try_body: List[ASTNode] = field(default_factory=list)
    catch_var: str = ""
    catch_body: List[ASTNode] = field(default_factory=list)
    finally_body: Optional[List[ASTNode]] = None


@dataclass
class ThrowStatement(ASTNode):
    """抛出异常"""
    value: ASTNode = None


@dataclass
class PrintStatement(ASTNode):
    """打印/输出语句"""
    value: ASTNode = None


@dataclass
class ExpressionStatement(ASTNode):
    """表达式语句"""
    expression: ASTNode = None


# =============================================================================
# 段落定义节点
# =============================================================================

@dataclass
class Parameter(ASTNode):
    """参数定义"""
    name: str = ""
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


@dataclass
class ParameterList(ASTNode):
    """参数列表（段落体内的参数声明）"""
    parameters: List[str] = field(default_factory=list)


@dataclass
class SegmentDefinition(ASTNode):
    """段落定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    modifiers: List[str] = field(default_factory=list)


# =============================================================================
# 类和接口定义
# =============================================================================

@dataclass
class AttributeDeclaration(ASTNode):
    """属性声明"""
    name: str = ""
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


@dataclass
class MethodDefinition(ASTNode):
    """方法定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    is_static: bool = False
    is_constructor: bool = False


@dataclass
class ConstructorDefinition(ASTNode):
    """构造函数定义"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ClassDefinition(ASTNode):
    """类定义"""
    name: str = ""
    generic_params: List[str] = field(default_factory=list)
    superclasses: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    attributes: List[AttributeDeclaration] = field(default_factory=list)
    methods: List[MethodDefinition] = field(default_factory=list)
    constructor: Optional[ConstructorDefinition] = None


@dataclass
class InterfaceMethod(ASTNode):
    """接口方法签名"""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    return_type: str = ""


@dataclass
class InterfaceProperty(ASTNode):
    """接口属性签名"""
    name: str = ""
    type_annotation: str = ""


@dataclass
class InterfaceDefinition(ASTNode):
    """接口定义"""
    name: str = ""
    superinterfaces: List[str] = field(default_factory=list)
    methods: List[InterfaceMethod] = field(default_factory=list)
    properties: List[InterfaceProperty] = field(default_factory=list)


# =============================================================================
# 数据/错误类型定义
# =============================================================================

@dataclass
class DataTypeField(ASTNode):
    """数据类型字段"""
    name: str = ""
    type_annotation: str = ""


@dataclass
class DataTypeDefinition(ASTNode):
    """数据类型定义"""
    name: str = ""
    fields: List[DataTypeField] = field(default_factory=list)


@dataclass
class ErrorTypeDefinition(ASTNode):
    """错误类型定义"""
    name: str = ""
    fields: List[DataTypeField] = field(default_factory=list)


# =============================================================================
# 类型注解节点（泛型支持）
# =============================================================================

@dataclass
class TypeAnnotation(ASTNode):
    """类型注解"""
    type_name: str = ""
    generic_args: Optional[List['TypeAnnotation']] = None


@dataclass
class GenericType(ASTNode):
    """泛型类型"""
    base_type: str = ""
    type_arguments: List[str] = field(default_factory=list)


# =============================================================================
# 模块节点
# =============================================================================

@dataclass
class ImportStatement(ASTNode):
    """导入语句"""
    module: str = ""
    names: List[str] = field(default_factory=list)
    alias: Optional[str] = None  # 导入别名


@dataclass
class ExportStatement(ASTNode):
    """导出语句"""
    names: List[str] = field(default_factory=list)  # 支持多个导出


@dataclass
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
