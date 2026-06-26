"""
段言（Duan）编程语言 - Python 后端 AST 节点定义

从 duan_parser_v3.py 提取，作为独立模块供代码生成器/语义分析器使用。
"""

from typing import List, Any, Optional, Dict


# =============================================================================
# AST 节点定义
# =============================================================================

class ASTNode:
    """AST 节点基类"""
    __slots__ = ()


class Module(ASTNode):
    __slots__ = ('statements',)
    """模块"""
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
    
    def __repr__(self):
        return f"Module({len(self.statements)} statements)"


class ParameterList(ASTNode):
    __slots__ = ('params',)
    """参数列表（用于参数声明语句）"""
    def __init__(self, params: List[str]):
        self.params = params
    
    def __repr__(self):
        return f"ParameterList({self.params})"


class VarDecl(ASTNode):
    __slots__ = ('name', 'value', 'type_annotation')
    """变量声明"""
    def __init__(self, name: str, value: ASTNode, type_annotation: Optional[str] = None):
        self.name = name
        self.value = value
        self.type_annotation = type_annotation
    
    def __repr__(self):
        if self.type_annotation:
            return f"VarDecl({self.name}: {self.type_annotation} = {self.value})"
        return f"VarDecl({self.name} = {self.value})"


class IfStmt(ASTNode):
    __slots__ = ('condition', 'then_body', 'else_body')
    """条件语句"""
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"IfStmt({self.condition})"


class ForeachStmt(ASTNode):
    __slots__ = ('variable', 'iterable', 'body')
    """遍历循环"""
    def __init__(self, variable: str, iterable: ASTNode, body: List[ASTNode]):
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForeachStmt({self.variable} in {self.iterable})"


class WhileStmt(ASTNode):
    __slots__ = ('condition', 'body')
    """当循环"""
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStmt({self.condition})"


class Paragraph(ASTNode):
    __slots__ = ('name', 'params', 'return_type', 'body', 'generic_params')
    """段落定义"""
    def __init__(self, name: str, params: List[Dict[str, str]], return_type: Optional[str], body: List[ASTNode],
                 generic_params: List[str] = None):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.generic_params = generic_params or []
    
    def __repr__(self):
        return f"Paragraph({self.name})"


class ReturnStmt(ASTNode):
    __slots__ = ('value',)
    """返回语句"""
    def __init__(self, value: Optional[ASTNode]):
        self.value = value
    
    def __repr__(self):
        return f"ReturnStmt({self.value})"


class BinaryOp(ASTNode):
    __slots__ = ('operator', 'left', 'right')
    """二元运算"""
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


class UnaryOp(ASTNode):
    __slots__ = ('operator', 'operand')
    """一元运算
    
    支持的运算符：
    - '非'：逻辑非
    - '-'：负号
    """
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"({self.operator} {self.operand})"


class NumberLiteral(ASTNode):
    __slots__ = ('value',)
    """数字字面量"""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"


class StringLiteral(ASTNode):
    __slots__ = ('value',)
    """字符串字面量"""
    def __init__(self, value: str):
        self.value = value
    
    def __repr__(self):
        return f'"{self.value}"'


class Identifier(ASTNode):
    __slots__ = ('name',)
    """标识符"""
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name


class ParagraphCall(ASTNode):
    __slots__ = ('name', 'args')
    """段落调用"""
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"《{self.name}》({', '.join(map(str, self.args))})"


class IndexAccess(ASTNode):
    __slots__ = ('obj', 'index')
    """索引访问（字符串/列表索引）"""
    def __init__(self, obj: ASTNode, index: ASTNode):
        self.obj = obj
        self.index = index
    
    def __repr__(self):
        return f"{self.obj}[{self.index}]"


class BreakStmt(ASTNode):
    __slots__ = ()
    """跳出语句"""
    def __repr__(self):
        return "跳出"


class ContinueStmt(ASTNode):
    __slots__ = ()
    """跳过语句"""
    def __repr__(self):
        return "跳过"


class TryStmt(ASTNode):
    __slots__ = ('try_body', 'catch_type', 'catch_var', 'catch_body', 'finally_body')
    """异常捕获语句"""
    def __init__(self, try_body: List[ASTNode], catch_type: str = None, catch_var: str = None,
                 catch_body: List[ASTNode] = None, finally_body: List[ASTNode] = None):
        self.try_body = try_body
        self.catch_type = catch_type
        self.catch_var = catch_var
        self.catch_body = catch_body or []
        self.finally_body = finally_body or []
    
    def __repr__(self):
        return f"TryStmt(catch: {self.catch_var})"


class ThrowStmt(ASTNode):
    __slots__ = ('value',)
    """抛出异常语句"""
    def __init__(self, value: ASTNode):
        self.value = value
    
    def __repr__(self):
        return f"ThrowStmt({self.value})"


class Pipeline(ASTNode):
    __slots__ = ('stages',)
    """管道操作"""
    def __init__(self, stages: List[ASTNode]):
        self.stages = stages
    
    def __repr__(self):
        return ' -> '.join(map(str, self.stages))


class ImportStmt(ASTNode):
    __slots__ = ('module_name', 'symbols', 'alias')
    """导入语句"""
    def __init__(self, module_name: str, symbols: List[str] = None, alias: str = None):
        self.module_name = module_name
        self.symbols = symbols
        self.alias = alias
    
    def __repr__(self):
        if self.symbols:
            symbols_str = ', '.join(self.symbols)
            if self.alias:
                return f"ImportStmt(from {self.module_name} import {symbols_str} as {self.alias})"
            return f"ImportStmt(from {self.module_name} import {symbols_str})"
        else:
            if self.alias:
                return f"ImportStmt(import {self.module_name} as {self.alias})"
            return f"ImportStmt(import {self.module_name})"


class ExportStmt(ASTNode):
    __slots__ = ('symbols',)
    """导出语句"""
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
    
    def __repr__(self):
        return f"ExportStmt({', '.join(self.symbols)})"


class Parameter(ASTNode):
    __slots__ = ('name', 'type_annotation', 'default_value')
    """参数定义"""
    def __init__(self, name: str, type_annotation: str = None, default_value: ASTNode = None):
        self.name = name
        self.type_annotation = type_annotation
        self.default_value = default_value
    
    def __repr__(self):
        return f"Parameter({self.name})"


class AttributeDeclaration(ASTNode):
    __slots__ = ('name', 'type_annotation', 'default_value')
    """属性声明"""
    def __init__(self, name: str, type_annotation: str = None, default_value: ASTNode = None):
        self.name = name
        self.type_annotation = type_annotation
        self.default_value = default_value
    
    def __repr__(self):
        return f"AttributeDeclaration({self.name})"


class MethodDefinition(ASTNode):
    __slots__ = ('name', 'parameters', 'body', 'return_type', 'is_constructor', 'generic_params')
    """方法定义"""
    def __init__(self, name: str, parameters: List[Parameter], body: List[ASTNode], 
                 return_type: str = None, is_constructor: bool = False,
                 generic_params: List[str] = None):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
        self.is_constructor = is_constructor
        self.generic_params = generic_params or []
    
    def __repr__(self):
        return f"MethodDefinition({self.name})"


class CompoundAssignment(ASTNode):
    __slots__ = ('target', 'operator', 'value')
    """复合赋值（甲 加上 1 → 甲 += 1）"""
    def __init__(self, target: str, operator: str, value: ASTNode):
        self.target = target
        self.operator = operator  # '加', '减', '乘', '除', '模', '幂'
        self.value = value
    
    def __repr__(self):
        return f"CompoundAssignment({self.target} {self.operator}= {self.value})"


class IndexedAssignment(ASTNode):
    __slots__ = ('target', 'index', 'value')
    """索引赋值（甲[丁] 为 值 → 甲[丁] = 值）"""
    def __init__(self, target: str, index: ASTNode, value: ASTNode):
        self.target = target
        self.index = index
        self.value = value
    
    def __repr__(self):
        return f"IndexedAssignment({self.target}[{self.index}] = {self.value})"


class SelfAssignment(ASTNode):
    __slots__ = ('attr_name', 'value')
    """self赋值语句"""
    def __init__(self, attr_name: str, value: ASTNode):
        self.attr_name = attr_name
        self.value = value
    
    def __repr__(self):
        return f"SelfAssignment(self.{self.attr_name})"


class ClassDefinition(ASTNode):
    __slots__ = ('name', 'attributes', 'methods', 'base_classes', 'generic_params')
    """类定义"""
    def __init__(self, name: str, attributes: List[AttributeDeclaration], 
                 methods: List[MethodDefinition], base_classes: List[str] = None,
                 generic_params: List[str] = None):
        self.name = name
        self.attributes = attributes
        self.methods = methods
        self.base_classes = base_classes or []
        self.generic_params = generic_params or []
    
    def __repr__(self):
        return f"ClassDefinition({self.name})"


class ClassInstantiation(ASTNode):
    __slots__ = ('class_name', 'args')
    """类实例化"""
    def __init__(self, class_name: str, args: List[ASTNode]):
        self.class_name = class_name
        self.args = args
    
    def __repr__(self):
        return f"ClassInstantiation({self.class_name})"


class ConditionalExpression(ASTNode):
    __slots__ = ('condition', 'then_expr', 'else_expr')
    """三元条件表达式"""
    def __init__(self, condition: ASTNode, then_expr: ASTNode, else_expr: Optional[ASTNode] = None):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
    
    def __repr__(self):
        return f"ConditionalExpression({self.condition}, {self.then_expr}, {self.else_expr})"


class MemberAccess(ASTNode):
    __slots__ = ('obj', 'member', 'is_method_call', 'args')
    """成员访问"""
    def __init__(self, obj: ASTNode, member: str, is_method_call: bool = False, args: List[ASTNode] = None):
        self.obj = obj
        self.member = member
        self.is_method_call = is_method_call
        self.args = args or []
    
    def __repr__(self):
        return f"MemberAccess({self.obj}.{self.member})"


class ListLiteral(ASTNode):
    __slots__ = ('elements',)
    """列表字面量"""
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements
    
    def __repr__(self):
        return f"[{', '.join(map(str, self.elements))}]"


class StringInterpolation(ASTNode):
    __slots__ = ('parts',)
    """字符串插值"""
    def __init__(self, parts: List):
        self.parts = parts  # 交替的 str 和 ASTNode
    
    def __repr__(self):
        return f"StringInterpolation({len(self.parts)} parts)"


class ListComprehension(ASTNode):
    __slots__ = ('expression', 'variable', 'iterable', 'condition')
    """列表推导"""
    def __init__(self, expression: ASTNode, variable: str, iterable: ASTNode, condition: ASTNode = None):
        self.expression = expression
        self.variable = variable
        self.iterable = iterable
        self.condition = condition
    
    def __repr__(self):
        return f"ListComprehension([{self.expression} for {self.variable} in {self.iterable}])"


class LambdaExpression(ASTNode):
    __slots__ = ('params', 'body')
    """匿名函数"""
    def __init__(self, params: List[str], body: ASTNode):
        self.params = params
        self.body = body
    
    def __repr__(self):
        return f"Lambda({', '.join(self.params)}: {self.body})"


class MatchStmt(ASTNode):
    __slots__ = ('subject', 'cases')
    """模式匹配"""
    def __init__(self, subject: ASTNode, cases: List):
        self.subject = subject
        self.cases = cases
    
    def __repr__(self):
        return f"MatchStmt({len(self.cases)} cases)"


class MatchCase(ASTNode):
    __slots__ = ('pattern', 'guard', 'body')
    """匹配分支"""
    def __init__(self, pattern, guard: ASTNode = None, body: List[ASTNode] = None):
        self.pattern = pattern
        self.guard = guard
        self.body = body or []
    
    def __repr__(self):
        return f"MatchCase({self.pattern})"


class MatchPattern(ASTNode):
    __slots__ = ('kind', 'value', 'elements', 'type_name', 'binding')
    """匹配模式"""
    def __init__(self, kind: str, value=None, elements: List = None, type_name: str = '', binding: str = ''):
        self.kind = kind
        self.value = value
        self.elements = elements or []
        self.type_name = type_name
        self.binding = binding
    
    def __repr__(self):
        if self.kind == 'wildcard':
            return '_'
        if self.kind == 'variable':
            return self.binding
        if self.kind == 'number':
            return str(self.value)
        if self.kind == 'string':
            return f'"{self.value}"'
        return f"MatchPattern({self.kind})"


class DictComprehension(ASTNode):
    __slots__ = ('key_expr', 'value_expr', 'variable', 'iterable', 'condition')
    """字典推导"""
    def __init__(self, key_expr: ASTNode, value_expr: ASTNode, variable: str,
                 iterable: ASTNode, condition: ASTNode = None):
        self.key_expr = key_expr
        self.value_expr = value_expr
        self.variable = variable
        self.iterable = iterable
        self.condition = condition
    
    def __repr__(self):
        return f"DictComprehension({{{self.key_expr}: {self.value_expr} for {self.variable} in {self.iterable}}})"


class DecoratorDefinition(ASTNode):
    __slots__ = ('decorator_name', 'paragraph')
    """装饰器定义"""
    def __init__(self, decorator_name: str, paragraph):
        self.decorator_name = decorator_name
        self.paragraph = paragraph
    
    def __repr__(self):
        return f"DecoratorDefinition(@{self.decorator_name})"


class MethodSignature(ASTNode):
    __slots__ = ('name', 'parameters', 'return_type')
    """接口方法签名"""
    def __init__(self, name: str, parameters: List[Parameter] = None, return_type: str = None):
        self.name = name
        self.parameters = parameters or []
        self.return_type = return_type
    
    def __repr__(self):
        return f"MethodSignature({self.name})"


class InterfaceDefinition(ASTNode):
    __slots__ = ('name', 'methods', 'properties', 'super_interfaces')
    """接口定义"""
    def __init__(self, name: str, methods: List[MethodSignature], 
                 properties: List[AttributeDeclaration] = None,
                 super_interfaces: List[str] = None):
        self.name = name
        self.methods = methods
        self.properties = properties or []
        self.super_interfaces = super_interfaces or []
    
    def __repr__(self):
        return f"InterfaceDefinition({self.name})"


class DestructuringAssignment(ASTNode):
    __slots__ = ('variables', 'value', 'style')
    """解构赋值
    
    style: 'tuple' 或 'list'，区分元组解构和列表解构
    """
    def __init__(self, variables: List[str], value: ASTNode, style: str = 'tuple'):
        self.variables = variables
        self.value = value
        self.style = style  # 'tuple' 或 'list'
    
    def __repr__(self):
        bracket = '(' if self.style == 'tuple' else '['
        end_bracket = ')' if self.style == 'tuple' else ']'
        return f"DestructuringAssignment({bracket}{', '.join(self.variables)}{end_bracket} = {self.value})"


class WithStmt(ASTNode):
    __slots__ = ('context_expr', 'variable', 'body')
    """上下文管理器"""
    def __init__(self, context_expr: ASTNode, variable: str = None, body: List[ASTNode] = None):
        self.context_expr = context_expr
        self.variable = variable
        self.body = body or []
    
    def __repr__(self):
        var = f" as {self.variable}" if self.variable else ""
        return f"WithStmt({self.context_expr}{var})"


class DictLiteral(ASTNode):
    __slots__ = ('entries',)
    """字典字面量"""
    def __init__(self, entries: List):
        self.entries = entries
    
    def __repr__(self):
        items = [f"{k}: {v}" for k, v in self.entries]
        return f"DictLiteral({{{', '.join(items)}}})"


class RangeExpr(ASTNode):
    __slots__ = ('start', 'end', 'step')
    """范围表达式
    
    语法：
    - 1至10       # 从1到10（包含10）
    - 1到10       # 从1到10（包含10）
    - 1到10步2    # 从1到10，步长为2
    
    生成 Python: range(start, end+1) 或 range(start, end+1, step)
    """
    def __init__(self, start: ASTNode, end: ASTNode, step: ASTNode = None):
        self.start = start
        self.end = end
        self.step = step
    
    def __repr__(self):
        step_str = f"步{self.step}" if self.step else ""
        return f"RangeExpr({self.start}至{self.end}{step_str})"