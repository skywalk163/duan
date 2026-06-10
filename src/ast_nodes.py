"""
段言（Duan）编程语言 AST 节点定义

抽象语法树节点类型
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Union


# =============================================================================
# 基础节点
# =============================================================================

@dataclass
class ASTNode:
    """AST 节点基类"""
    line: int
    column: int


# =============================================================================
# 字面量节点
# =============================================================================

@dataclass
class NumberLiteral(ASTNode):
    """数字字面量"""
    value: Union[int, float]


@dataclass
class StringLiteral(ASTNode):
    """字符串字面量"""
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    """布尔字面量"""
    value: bool


@dataclass
class NullLiteral(ASTNode):
    """空值字面量"""
    pass


# =============================================================================
# 标识符节点
# =============================================================================

@dataclass
class Identifier(ASTNode):
    """标识符（变量名）"""
    name: str


@dataclass
class SegmentName(ASTNode):
    """段落名"""
    name: str


@dataclass
class ModuleName(ASTNode):
    """模块名"""
    name: str


# =============================================================================
# 表达式节点
# =============================================================================

@dataclass
class BinaryOp(ASTNode):
    """二元运算"""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """一元运算"""
    operator: str
    operand: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """函数调用"""
    name: Union[SegmentName, Identifier]
    arguments: List[ASTNode]


@dataclass
class PipeExpression(ASTNode):
    """管道表达式"""
    expressions: List[ASTNode]


@dataclass
class PropertyAccess(ASTNode):
    """属性访问（之字结构）"""
    obj: ASTNode
    property_name: str


@dataclass
class IndexAccess(ASTNode):
    """索引访问"""
    obj: ASTNode
    index: ASTNode


@dataclass
class MethodCall(ASTNode):
    """方法调用（主谓结构）"""
    obj: ASTNode
    method: str
    arguments: List[ASTNode]


@dataclass
class SelfReference(ASTNode):
    """self 引用（己）"""
    pass


@dataclass
class ClassInstantiation(ASTNode):
    """类实例化（创建对象）"""
    class_name: str
    arguments: List[ASTNode]


# =============================================================================
# 语句节点
# =============================================================================

@dataclass
class VariableDeclaration(ASTNode):
    """变量声明"""
    name: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    """赋值语句"""
    target: ASTNode
    value: ASTNode


@dataclass
class IfStatement(ASTNode):
    """条件语句"""
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class ForeachStatement(ASTNode):
    """遍历循环"""
    variable: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class WhileStatement(ASTNode):
    """当循环"""
    condition: ASTNode
    body: List[ASTNode]


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
class ExpressionStatement(ASTNode):
    """表达式语句"""
    expression: ASTNode


# =============================================================================
# 段落定义节点
# =============================================================================

@dataclass
class Parameter(ASTNode):
    """参数定义"""
    name: str
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


@dataclass
class SegmentDefinition(ASTNode):
    """段落定义"""
    name: str
    parameters: List[Parameter]
    body: List[ASTNode]
    return_type: Optional[str] = None
    exports: bool = False


# =============================================================================
# 类定义节点（新增）
# =============================================================================

@dataclass
class AttributeDeclaration(ASTNode):
    """属性声明"""
    name: str
    type_annotation: Optional[str] = None
    default_value: Optional[ASTNode] = None


@dataclass
class MethodDefinition(ASTNode):
    """方法定义"""
    name: str
    parameters: List[Parameter]
    body: List[ASTNode]
    return_type: Optional[str] = None
    is_constructor: bool = False


@dataclass
class ClassDefinition(ASTNode):
    """类定义"""
    name: str
    attributes: List[AttributeDeclaration]
    methods: List[MethodDefinition]
    base_class: Optional[str] = None


# =============================================================================
# 模块节点
# =============================================================================

@dataclass
class ImportStatement(ASTNode):
    """导入语句"""
    module: str
    names: List[str]


@dataclass
class ExportStatement(ASTNode):
    """导出语句"""
    name: str


@dataclass
class Module(ASTNode):
    """模块（篇）"""
    name: Optional[str]
    imports: List[ImportStatement]
    exports: List[ExportStatement]
    segments: List[SegmentDefinition]
    statements: List[ASTNode]


# =============================================================================
# 类型定义节点
# =============================================================================

@dataclass
class TypeDefinition(ASTNode):
    """类型定义"""
    name: str
    fields: List[tuple]  # [(name, type), ...]


@dataclass
class TypeAnnotation(ASTNode):
    """类型注解"""
    type_name: str
    generic_args: Optional[List['TypeAnnotation']] = None


# =============================================================================
# 辅助函数
# =============================================================================

def ast_to_dict(node: ASTNode) -> dict:
    """将 AST 节点转换为字典（用于序列化）"""
    if isinstance(node, ASTNode):
        result = {'type': node.__class__.__name__}
        for field in node.__dataclass_fields__:
            value = getattr(node, field)
            if isinstance(value, list):
                result[field] = [ast_to_dict(item) for item in value]
            elif isinstance(value, ASTNode):
                result[field] = ast_to_dict(value)
            else:
                result[field] = value
        return result
    return node
