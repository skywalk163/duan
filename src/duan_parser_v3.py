"""
段言（Duan）编程语言 - 完整语法解析器（v3.0）

支持完整语法：
- 变量声明：定义甲等于三。
- 条件语句：如果...那么...否则...
- 循环语句：遍历...当...
- 段落定义：《段名》段(参数):
- 管道操作符：-> 和 ，

基于：
- 自定义词法分析器（无空格分词）
- 递归下降解析器
"""

from typing import List, Any, Optional, Dict
from lexer import Lexer, LexerError
from tokens import Token, TokenType
from keywords import VERB_ARITY, KEYWORDS_DOUBLE, KEYWORDS_SPECIAL
import sys


# =============================================================================
# 解析错误类
# =============================================================================

class ParseError(Exception):
    """语法解析错误"""
    def __init__(self, message: str, line: int = 0, col: int = 0, token_value: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.token_value = token_value
        parts = [f"语法错误"]
        if line:
            parts.append(f"(行{line}")
            if col:
                parts[-1] += f", 列{col}"
            parts[-1] += ")"
        parts.append(f": {message}")
        if token_value:
            parts.append(f" (附近: '{token_value}')")
        super().__init__(''.join(parts))


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
    __slots__ = ('name', 'value')
    """变量声明"""
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value
    
    def __repr__(self):
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
    __slots__ = ('name', 'params', 'return_type', 'body')
    """段落定义"""
    def __init__(self, name: str, params: List[Dict[str, str]], return_type: Optional[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
    
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
        self.catch_type = catch_type  # 捕获的异常类型（如'值错误'），None表示捕获所有异常
        self.catch_var = catch_var    # 捕获的异常变量名
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
        """
        module_name: 模块名
        symbols: 导入的符号列表（None表示导入整个模块）
        alias: 模块或符号别名
        """
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
    __slots__ = ('name', 'parameters', 'body', 'return_type', 'is_constructor')
    """方法定义"""
    def __init__(self, name: str, parameters: List[Parameter], body: List[ASTNode], 
                 return_type: str = None, is_constructor: bool = False):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
        self.is_constructor = is_constructor
    
    def __repr__(self):
        return f"MethodDefinition({self.name})"


class SelfAssignment(ASTNode):
    __slots__ = ('attr_name', 'value')
    """self赋值语句：己属性名 为 值"""
    def __init__(self, attr_name: str, value: ASTNode):
        self.attr_name = attr_name
        self.value = value
    
    def __repr__(self):
        return f"SelfAssignment(self.{self.attr_name})"


class ClassDefinition(ASTNode):
    __slots__ = ('name', 'attributes', 'methods', 'base_classes')
    """类定义"""
    def __init__(self, name: str, attributes: List[AttributeDeclaration], 
                 methods: List[MethodDefinition], base_classes: List[str] = None):
        self.name = name
        self.attributes = attributes
        self.methods = methods
        self.base_classes = base_classes or []  # 父类列表
    
    def __repr__(self):
        return f"ClassDefinition({self.name})"


class ClassInstantiation(ASTNode):
    __slots__ = ('class_name', 'args')
    """类实例化（新建 类名 参数...）"""
    def __init__(self, class_name: str, args: List[ASTNode]):
        self.class_name = class_name
        self.args = args
    
    def __repr__(self):
        return f"ClassInstantiation({self.class_name})"


class ConditionalExpression(ASTNode):
    __slots__ = ('condition', 'then_expr', 'else_expr')
    """三元条件表达式：如果 条件 那么 值1 否则 值2"""
    def __init__(self, condition: ASTNode, then_expr: ASTNode, else_expr: Optional[ASTNode] = None):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
    
    def __repr__(self):
        return f"ConditionalExpression({self.condition}, {self.then_expr}, {self.else_expr})"


class MemberAccess(ASTNode):
    __slots__ = ('obj', 'member', 'is_method_call', 'args')
    """成员访问（对象.属性 或 对象.方法()）"""
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
    """字符串插值：\"你好，{名字}\" -> f-string"""
    def __init__(self, parts: List):
        self.parts = parts  # 交替的 str 和 ASTNode
    
    def __repr__(self):
        return f"StringInterpolation({len(self.parts)} parts)"


class ListComprehension(ASTNode):
    __slots__ = ('expression', 'variable', 'iterable', 'condition')
    """列表推导：[表达式 遍历 变量 之 列表]"""
    def __init__(self, expression: ASTNode, variable: str, iterable: ASTNode, condition: ASTNode = None):
        self.expression = expression
        self.variable = variable
        self.iterable = iterable
        self.condition = condition
    
    def __repr__(self):
        return f"ListComprehension([{self.expression} for {self.variable} in {self.iterable}])"


class LambdaExpression(ASTNode):
    __slots__ = ('params', 'body')
    """匿名函数：接收 甲：返回 甲 乘 甲。"""
    def __init__(self, params: List[str], body: ASTNode):
        self.params = params
        self.body = body
    
    def __repr__(self):
        return f"Lambda({', '.join(self.params)}: {self.body})"


class MatchStmt(ASTNode):
    __slots__ = ('subject', 'cases')
    """模式匹配：匹配 值：情况 ... 结束。"""
    def __init__(self, subject: ASTNode, cases: List):
        self.subject = subject
        self.cases = cases  # List[MatchCase]
    
    def __repr__(self):
        return f"MatchStmt({len(self.cases)} cases)"


class MatchCase(ASTNode):
    __slots__ = ('pattern', 'guard', 'body')
    """匹配分支"""
    def __init__(self, pattern, guard: ASTNode = None, body: List[ASTNode] = None):
        self.pattern = pattern  # MatchPattern
        self.guard = guard
        self.body = body or []
    
    def __repr__(self):
        return f"MatchCase({self.pattern})"


class MatchPattern(ASTNode):
    __slots__ = ('kind', 'value', 'elements', 'type_name', 'binding')
    """匹配模式"""
    def __init__(self, kind: str, value=None, elements: List = None, type_name: str = '', binding: str = ''):
        self.kind = kind  # 'number', 'string', 'bool', 'null', 'variable', 'wildcard', 'list', 'type_check'
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
    """字典推导：【键: 值 遍历 变量 之 列表】"""
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
    """装饰器定义：@段落名 标注 段落 ..."""
    def __init__(self, decorator_name: str, paragraph):
        self.decorator_name = decorator_name
        self.paragraph = paragraph  # Paragraph node
    
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
        self.methods = methods        # List[MethodSignature]
        self.properties = properties or []
        self.super_interfaces = super_interfaces or []
    
    def __repr__(self):
        return f"InterfaceDefinition({self.name})"


class DestructuringAssignment(ASTNode):
    __slots__ = ('variables', 'value')
    """解构赋值：设（甲，乙）为 元组"""
    def __init__(self, variables: List[str], value: ASTNode):
        self.variables = variables
        self.value = value
    
    def __repr__(self):
        return f"DestructuringAssignment({', '.join(self.variables)} = {self.value})"


class WithStmt(ASTNode):
    __slots__ = ('context_expr', 'variable', 'body')
    """上下文管理器：使用 表达式 为 变量：...结束。"""
    def __init__(self, context_expr: ASTNode, variable: str = None, body: List[ASTNode] = None):
        self.context_expr = context_expr
        self.variable = variable
        self.body = body or []
    
    def __repr__(self):
        var = f" as {self.variable}" if self.variable else ""
        return f"WithStmt({self.context_expr}{var})"


class DictLiteral(ASTNode):
    __slots__ = ('entries',)
    """字典字面量：【键1: 值1, 键2: 值2, ...】"""
    def __init__(self, entries: List):
        self.entries = entries  # List[Tuple[ASTNode, ASTNode]]
    
    def __repr__(self):
        items = [f"{k}: {v}" for k, v in self.entries]
        return f"DictLiteral({{{', '.join(items)}}})"


# =============================================================================
# 递归下降解析器
# =============================================================================

class DuanParser:
    """段言完整语法解析器"""
    
    # 运算符动词集合（类常量，避免重复创建）
    OPERATOR_VERBS = frozenset({'加', '减', '乘', '除', '加上', '减去', '乘以', '除以', 
                                '大于', '小于', '等于', '不等于', '大于等于', '小于等于',
                                '模', '幂'})
    
    # 操作符映射表（类常量）
    COMPARISON_OP_MAP = {
        '大于': '>', '小于': '<', '等于': '==',
        '不等于': '!=', '大于等于': '>=', '小于等于': '<=',
    }
    ADD_OP_MAP = {'加': '+', '减': '-', '加上': '+', '减去': '-'}
    MUL_OP_MAP = {'乘': '*', '除': '/', '乘以': '*', '除以': '/', '模': '%', '幂': '**'}
    LOGICAL_OP_MAP = {'且': 'and', '与': 'and', '或': 'or'}
    
    def __init__(self):
        self.lexer = Lexer()
        self.tokens: List[Token] = []
        self.pos = 0
    
    def parse(self, source: str) -> Module:
        """解析段言代码"""
        # 词法分析
        tokens = self.lexer.tokenize(source)
        
        # 过滤掉 NEWLINE/INDENT/DEDENT（简化版）
        self.tokens = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT, TokenType.EOF)]
        self.pos = 0
        
        # 解析模块
        return self._parse_module()
    
    def _current(self) -> Optional[Token]:
        """获取当前 Token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _peek(self, offset: int = 0) -> Optional[Token]:
        """查看指定位置的 Token"""
        idx = self.pos + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def _consume(self, expected_type=None, expected_value=None) -> Token:
        """消耗并返回当前 Token"""
        tok = self._current()
        if tok is None:
            last_tok = self.tokens[-1] if self.tokens else None
            line = last_tok.line if last_tok else 0
            col = last_tok.col if last_tok else 0
            hint = ""
            if expected_type:
                hint = f" (期望 {expected_type}"
                if expected_value:
                    hint += f" = '{expected_value}'"
                hint += ")"
            raise ParseError(f"输入意外结束{hint}（建议检查是否缺少表达式或语句）", line, col)
        
        if expected_type and tok.type != expected_type:
            raise ParseError(f"期望 {expected_type}，但得到 {tok.type}（附近: '{tok.value}'）", tok.line, tok.col, tok.value)
        
        if expected_value and tok.value != expected_value:
            raise ParseError(f"期望'{expected_value}'，但得到'{tok.value}'（附近: '{tok.value}'）", tok.line, tok.col)
        
        self.pos += 1
        return tok
    
    def _match(self, token_type, value=None) -> bool:
        """检查当前 Token 是否匹配"""
        tok = self._current()
        if tok is None:
            return False
        if tok.type != token_type:
            return False
        if value is not None and tok.value != value:
            return False
        return True
    
    # =========================================================================
    # 语法规则
    # =========================================================================
    
    def _parse_module(self) -> Module:
        """解析模块"""
        statements = []
        
        while self._current():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                # 无法解析，跳出循环避免无限循环
                break
        
        return Module(statements)
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        tok = self._current()
        
        if tok is None:
            return None
        
        # 结束标记（提前检查）
        if tok.type == TokenType.KEYWORD and tok.value == '结束':
            return None  # 返回None，让_parse_body处理结束
        
        # 导入语句：导入
        if tok.type == TokenType.KEYWORD and tok.value == '导入':
            return self._parse_import_stmt()
        
        # 从...导入语句：从
        if tok.type == TokenType.KEYWORD and tok.value == '从':
            return self._parse_from_import_stmt()
        
        # 导出语句：导出
        if tok.type == TokenType.KEYWORD and tok.value == '导出':
            return self._parse_export_stmt()
        
        # 变量声明：定义
        if tok.type == TokenType.KEYWORD and tok.value == '定义':
            return self._parse_var_decl()
        
        # 变量声明：设...为...
        if tok.type == TokenType.KEYWORD and tok.value == '设':
            return self._parse_set_stmt()
        
        # 条件语句：如果
        if tok.type == TokenType.KEYWORD and tok.value == '如果':
            return self._parse_if_stmt()
        
        # 遍历循环：遍历
        if tok.type == TokenType.KEYWORD and tok.value == '遍历':
            return self._parse_foreach_stmt()
        
        # 当循环：当
        if tok.type == TokenType.KEYWORD and tok.value == '当':
            return self._parse_while_stmt()
        
        # 返回语句：返回
        if tok.type == TokenType.KEYWORD and tok.value == '返回':
            return self._parse_return_stmt()
        
        # 跳出语句：跳出
        if tok.type == TokenType.KEYWORD and tok.value == '跳出':
            self._consume(TokenType.KEYWORD, '跳出')
            self._consume(TokenType.DOT)
            return BreakStmt()
        
        # 跳过语句：跳过
        if tok.type == TokenType.KEYWORD and tok.value == '跳过':
            self._consume(TokenType.KEYWORD, '跳过')
            self._consume(TokenType.DOT)
            return ContinueStmt()
        
        # 参数声明：参数
        if tok.type == TokenType.KEYWORD and tok.value == '参数':
            return self._parse_parameter_stmt()
        
        # 异常捕获：尝试
        if tok.type == TokenType.KEYWORD and tok.value == '尝试':
            return self._parse_try_stmt()
        
        # 抛出异常：抛出
        if tok.type == TokenType.KEYWORD and tok.value == '抛出':
            return self._parse_throw_stmt()
        
        # 段落定义：《段名》段 或 "段落 段名 参数 参数名"
        if tok.type == TokenType.LBOOK:
            return self._parse_paragraph()
        
        # 段落定义：段落 段名 参数 参数名
        if tok.type == TokenType.KEYWORD and tok.value == '段落':
            return self._parse_paragraph_v2()
        
        # 段落定义：段 段名 接收 参数
        if tok.type == TokenType.KEYWORD and tok.value == '段':
            return self._parse_paragraph_v2()
        
        # 类定义：类 类名
        if tok.type == TokenType.KEYWORD and tok.value == '类':
            return self._parse_class_definition()

        # 接口定义：接口 接口名
        if tok.type == TokenType.KEYWORD and tok.value == '接口':
            return self._parse_interface_definition()

        # 模式匹配：匹配
        if tok.type == TokenType.KEYWORD and tok.value == '匹配':
            return self._parse_match_stmt()

        # 上下文管理器：使用
        if tok.type == TokenType.KEYWORD and tok.value == '使用':
            return self._parse_with_stmt()

        # 动词调用作为独立语句
        if tok.type == TokenType.KEYWORD and tok.value in VERB_ARITY:
            return self._parse_expr_stmt()
        
        # self赋值语句：己属性名 为 值
        if tok.type == TokenType.KEYWORD and tok.value == '己':
            return self._parse_self_assignment()

        # 装饰器：@段落名 标注 段落 ...
        if tok.type == TokenType.AT:
            return self._parse_decorator()
        
        # 赋值语句：标识符 等于 值。
        if tok.type == TokenType.IDENTIFIER:
            return self._parse_assignment_stmt()

        return None

    def _parse_expr_stmt(self) -> ASTNode:
        """解析表达式语句（动词调用等）"""
        expr = self._parse_expr()
        # 消耗句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        return expr
    
    def _parse_self_assignment(self) -> ASTNode:
        """解析self赋值语句：己属性名 为 值。
        
        语法：己属性名 为 值。
        生成：self.属性名 = 值
        """
        # 己
        self._consume(TokenType.KEYWORD, '己')
        
        # 属性名（可能以"己"开头，但已经被消费了）
        # 这里属性名可能是单个标识符，也可能带类型等
        attr_name_tokens = []
        
        # 收集属性名，直到遇到"为"关键字
        while self._current():
            tok = self._current()
            
            if tok.type == TokenType.KEYWORD and tok.value == '为':
                break
            
            if tok.type == TokenType.IDENTIFIER:
                attr_name_tokens.append(tok.value)
                self._consume(TokenType.IDENTIFIER)
            elif tok.type == TokenType.KEYWORD and tok.value not in ('为', '结束'):
                # 属性名可能包含关键字
                attr_name_tokens.append(tok.value)
                self._consume(TokenType.KEYWORD)
            else:
                break
        
        # 拼接属性名（处理"己名称"这种"己"+"名称"的情况）
        attr_name = ''.join(attr_name_tokens)
        
        # 为
        tok = self._current()
        if self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
        elif self._match(TokenType.KEYWORD, '等于'):
            self._consume(TokenType.KEYWORD, '等于')
        else:
            # 兼容其他赋值操作符
            raise ParseError(f"期望'为'或'等于'，但得到 {tok.type} = '{tok.value}'", tok.line, tok.col)
        
        # 值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 创建赋值节点（self.attr_name = value）
        return SelfAssignment(attr_name, value)
    
    def _parse_assignment_stmt(self) -> ASTNode:
        """解析赋值语句：标识符 等于 值。"""
        # 标识符
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 等于
        if not self._match(TokenType.KEYWORD, '等于'):
            # 不是赋值语句，可能是表达式
            self.pos -= 1  # 回退标识符
            return self._parse_expr_stmt()
        
        self._consume(TokenType.KEYWORD, '等于')
        
        # 值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return VarDecl(name, value)
    
    def _parse_import_stmt(self) -> ImportStmt:
        """解析导入语句
        
        语法：
        1. 导入 模块名。
        2. 导入《模块名》。
        3. 导入 模块名 为 别名。
        4. 导入《模块名》为 别名。
        """
        # 导入
        self._consume(TokenType.KEYWORD, '导入')
        
        # 模块名（可以是标识符、关键字或书名号包裹）
        module_name = None
        if self._match(TokenType.LBOOK):
            # 书名号语法：《模块名》
            self._consume(TokenType.LBOOK)
            name_tok = self._consume(TokenType.IDENTIFIER)
            module_name = name_tok.value
            self._consume(TokenType.RBOOK)
        else:
            # 简单语法：模块名（可以是标识符或关键字）
            tok = self._current()
            if tok.type == TokenType.IDENTIFIER:
                module_name = self._consume(TokenType.IDENTIFIER).value
            elif tok.type == TokenType.KEYWORD:
                module_name = self._consume(TokenType.KEYWORD).value
            else:
                raise ParseError(f"期望模块名，但得到 {tok.type} = '{tok.value}'（建议：使用「从 模块名 导入 名称。」语法）", tok.line, tok.col)
        
        # 检查是否有别名：为
        alias = None
        if self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
            alias_tok = self._consume(TokenType.IDENTIFIER)
            alias = alias_tok.value
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return ImportStmt(module_name, symbols=None, alias=alias)
    
    def _parse_from_import_stmt(self) -> ImportStmt:
        """解析从...导入语句
        
        语法：
        1. 从 模块名 导入 符号一 符号二。
        2. 从《模块名》导入《符号一》，《符号二》。
        3. 从 模块名 导入《符号一》《符号二》。
        """
        # 从
        self._consume(TokenType.KEYWORD, '从')
        
        # 模块名（可以是标识符、关键字或书名号包裹）
        module_name = None
        if self._match(TokenType.LBOOK):
            # 书名号语法：《模块名》
            self._consume(TokenType.LBOOK)
            name_tok = self._consume(TokenType.IDENTIFIER)
            module_name = name_tok.value
            self._consume(TokenType.RBOOK)
        else:
            # 简单语法：模块名（可以是标识符或关键字）
            tok = self._current()
            if tok.type == TokenType.IDENTIFIER:
                module_name = self._consume(TokenType.IDENTIFIER).value
            elif tok.type == TokenType.KEYWORD:
                module_name = self._consume(TokenType.KEYWORD).value
            else:
                raise ParseError(f"期望模块名，但得到 {tok.type} = '{tok.value}'（建议：使用「从 模块名 导入 名称。」语法）", tok.line, tok.col)
        
        # 导入
        self._consume(TokenType.KEYWORD, '导入')
        
        # 符号列表（可以是书名号包裹、标识符或关键字）
        symbols = []
        while True:
            # 读取符号
            if self._match(TokenType.LBOOK):
                # 书名号语法：《符号》
                self._consume(TokenType.LBOOK)
                symbol_tok = self._consume(TokenType.IDENTIFIER)
                symbols.append(symbol_tok.value)
                self._consume(TokenType.RBOOK)
            elif self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                # 简单语法：符号名（可以是标识符或关键字）
                tok = self._consume()
                symbols.append(tok.value)
            else:
                break
            
            # 检查是否有逗号（继续导入）
            if self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                continue
            
            # 检查是否还有更多符号（空格分隔）
            if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                continue
            
            # 检查是否结束（句号）
            if self._current() and self._current().type == TokenType.DOT:
                break
            
            # 如果不是标识符/关键字或句号，结束
            break
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 别名（可选）：从 模块 导入 符号 为 别名
        alias = None
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '为':
            self._consume(TokenType.KEYWORD, '为')
            if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                alias = self._consume().value
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        
        return ImportStmt(module_name, symbols=symbols, alias=alias)
    
    def _parse_set_stmt(self) -> ASTNode:
        """解析变量声明：设 变量名 为 值。或 解构赋值：设（甲，乙）为 元组。"""
        # 设
        self._consume(TokenType.KEYWORD, '设')
        
        # 检查是否为解构赋值：设 (甲, 乙) 为 元组
        if self._current() and self._current().type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            variables = []
            # 收集变量名
            while self._current():
                tok = self._current()
                if tok.type == TokenType.IDENTIFIER:
                    variables.append(self._consume(TokenType.IDENTIFIER).value)
                elif tok.type == TokenType.KEYWORD:
                    variables.append(self._consume(TokenType.KEYWORD).value)
                else:
                    break
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                else:
                    break
            self._consume(TokenType.RPAREN)
            # 为
            self._consume(TokenType.KEYWORD, '为')
            # 值
            value = self._parse_expr()
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            return DestructuringAssignment(variables, value)
        
        # 普通变量声明：变量名（支持标识符和关键字）
        name_tok = self._current()
        if name_tok and name_tok.type == TokenType.IDENTIFIER:
            name = self._consume(TokenType.IDENTIFIER).value
        elif name_tok and name_tok.type == TokenType.KEYWORD:
            name = self._consume(TokenType.KEYWORD).value
        else:
            raise ParseError(f"期望标识符，但得到 {name_tok.type if name_tok else '输入结束'}",
                             name_tok.line if name_tok else 0, name_tok.col if name_tok else 0)
        
        # 为
        self._consume(TokenType.KEYWORD, '为')
        
        # 值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return VarDecl(name, value)
    
    def _parse_export_stmt(self) -> ExportStmt:
        """解析导出语句
        
        语法：
        1. 导出 符号一 符号二。
        2. 导出《符号一》，《符号二》。
        3. 导出 全部。
        """
        # 导出
        self._consume(TokenType.KEYWORD, '导出')
        
        # 检查是否是"全部"
        if self._match(TokenType.IDENTIFIER, '全部'):
            self._consume(TokenType.IDENTIFIER, '全部')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            return ExportStmt(['*'])  # 特殊标记：导出全部
        
        # 符号列表（可以是书名号包裹或简单标识符/关键字）
        symbols = []
        while True:
            # 读取符号
            if self._match(TokenType.LBOOK):
                # 书名号语法：《符号》
                self._consume(TokenType.LBOOK)
                symbol_tok = self._consume(TokenType.IDENTIFIER)
                symbols.append(symbol_tok.value)
                self._consume(TokenType.RBOOK)
            else:
                # 简单语法：符号名（支持IDENTIFIER和KEYWORD）
                tok = self._current()
                if tok and tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    self._consume()
                    symbols.append(tok.value)
                else:
                    break
            
            # 检查是否有逗号（继续导出）
            if self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                continue
            
            # 检查是否还有更多符号（空格分隔）
            if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                continue
            
            # 检查是否结束（句号）
            if self._current() and self._current().type == TokenType.DOT:
                break
            
            # 如果不是标识符/关键字或句号，结束
            tok = self._current()
            if not tok or tok.type not in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                break
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return ExportStmt(symbols)
    
    def _parse_var_decl(self) -> VarDecl:
        """解析变量声明"""
        # 定义
        self._consume(TokenType.KEYWORD, '定义')

        # 标识符（允许 KEYWORD 作为变量名）
        name_tok = self._current()
        if name_tok is None:
            raise ParseError("期望标识符，但到达输入结束")

        # 允许 KEYWORD 或 IDENTIFIER 作为变量名
        if name_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._consume()
            name = name_tok.value
        else:
            raise ParseError(f"期望标识符，得到 {name_tok.type}", name_tok.line, name_tok.col, name_tok.value)

        # 等于/为（支持两种赋值关键字）
        if self._match(TokenType.KEYWORD, '等于'):
            self._consume(TokenType.KEYWORD, '等于')
        elif self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
        else:
            tok = self._current()
            raise ParseError(f"期望'等于'或'为'，但得到 {tok.type if tok else '输入结束'} = '{tok.value if tok else ''}'",
                             tok.line if tok else 0, tok.col if tok else 0, tok.value if tok else None)

        # 表达式
        value = self._parse_expr()

        # 句号
        self._consume(TokenType.DOT)

        return VarDecl(name, value)
    
    def _parse_if_stmt(self) -> IfStmt:
        """解析条件语句
        
        语法：
        1. 如果 条件。
            语句。
          结束。
        2. 如果 条件 那么
            语句。
          结束。
        3. 如果 条件 那么
            语句。
          否则
            语句。
          结束。
        """
        # 如果
        self._consume(TokenType.KEYWORD, '如果')
        
        # 条件
        condition = self._parse_expr()
        
        # 那么（可选）
        if self._match(TokenType.KEYWORD, '那么'):
            self._consume(TokenType.KEYWORD, '那么')
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 冒号（可选）- 检查是否是块模式
        has_colon = False
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
            has_colon = True
        
        # then块：块模式下用 _parse_body，否则只解析单个语句
        if has_colon:
            then_body = self._parse_body()
        else:
            stmt = self._parse_statement()
            then_body = [stmt] if stmt else []
        
        # 否则？
        else_body = None
        
        if self._match(TokenType.KEYWORD, '否则'):
            self._consume(TokenType.KEYWORD, '否则')
            
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            
            # 冒号（可选）
            if self._current() and self._current().type == TokenType.COLON:
                self._consume(TokenType.COLON)
            
            if has_colon:
                else_body = self._parse_body()
            else:
                stmt = self._parse_statement()
                else_body = [stmt] if stmt else []
        
        # 结束（仅块模式消耗）
        if has_colon and self._match(TokenType.KEYWORD, '结束'):
            self._consume(TokenType.KEYWORD, '结束')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        
        return IfStmt(condition, then_body, else_body)
    
    def _parse_foreach_stmt(self) -> ForeachStmt:
        """解析遍历循环"""
        # 遍历
        self._consume(TokenType.KEYWORD, '遍历')
        
        # 变量名
        var_tok = self._consume(TokenType.IDENTIFIER)
        variable = var_tok.value
        
        # 在 / 之
        tok = self._current()
        if self._match(TokenType.KEYWORD, '在'):
            self._consume(TokenType.KEYWORD, '在')
        elif self._match(TokenType.KEYWORD, '之'):
            self._consume(TokenType.KEYWORD, '之')
        else:
            raise ParseError(f"遍历循环期望'在'或'之'，但得到 {tok.type} = '{tok.value}'", tok.line, tok.col)
        
        # 可迭代对象
        iterable = self._parse_expr()
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # 循环体
        body = self._parse_body()
        
        # 结束
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        
        return ForeachStmt(variable, iterable, body)
    
    def _parse_while_stmt(self) -> WhileStmt:
        """解析当循环"""
        # 当
        self._consume(TokenType.KEYWORD, '当')
        
        # 条件
        condition = self._parse_expr()
        
        # 那么（可选）
        if self._match(TokenType.KEYWORD, '那么'):
            self._consume(TokenType.KEYWORD, '那么')
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # 循环体
        body = self._parse_body()
        
        # 结束
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        
        return WhileStmt(condition, body)
    
    def _parse_return_stmt(self) -> ReturnStmt:
        """解析返回语句"""
        # 返回
        self._consume(TokenType.KEYWORD, '返回')
        
        # 表达式（可选）
        value = None
        if not self._match(TokenType.DOT):
            value = self._parse_expr()
        
        # 句号
        self._consume(TokenType.DOT)
        
        return ReturnStmt(value)
    
    def _parse_parameter_stmt(self) -> ParameterList:
        """解析参数声明语句
        
        语法：参数 参数名1 参数名2 ...。
        """
        # 参数
        self._consume(TokenType.KEYWORD, '参数')
        
        # 收集参数名（支持多个参数）
        params = []
        while self._current() and self._current().type != TokenType.DOT:
            tok = self._current()
            if tok.type == TokenType.IDENTIFIER:
                params.append(self._consume(TokenType.IDENTIFIER).value)
            elif tok.type == TokenType.KEYWORD:
                # 参数名可能是关键字
                params.append(self._consume(TokenType.KEYWORD).value)
            else:
                break
        
        # 句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return ParameterList(params)
    
    def _parse_try_stmt(self) -> TryStmt:
        """解析异常捕获语句
        
        语法：
        尝试：
          语句...
        捕获 异常变量：
          语句...
        结束。
        
        或带类型过滤：
        尝试：
          语句...
        捕获 值错误：
          语句...
        结束。
        
        或带类型和变量：
        尝试：
          语句...
        捕获 值错误 异常变量：
          语句...
        结束。
        
        或带最终块：
        尝试：
          语句...
        捕获 异常变量：
          语句...
        最终：
          语句...
        结束。
        """
        # 尝试
        self._consume(TokenType.KEYWORD, '尝试')
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # try块
        try_body = self._parse_body()
        
        # 捕获（可选）
        catch_type = None
        catch_var = None
        catch_body = []
        if self._match(TokenType.KEYWORD, '捕获'):
            self._consume(TokenType.KEYWORD, '捕获')
            
            # 读取类型/变量名
            # 可能的情况：
            # 1. 标识符 -> :           => 变量名（向后兼容）
            # 2. 标识符 -> 标识符 -> :  => 类型 + 变量名
            # 3. 关键字 -> :           => 类型
            # 4. 关键字 -> 标识符 -> :  => 类型 + 变量名
            tok = self._current()
            if tok and tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                # 先读取第一个标识符/关键字
                first = self._consume().value
                
                # 检查下一个 token
                next_tok = self._current()
                if next_tok and next_tok.type == TokenType.COLON:
                    # 情况1或3：只有一个标识符/关键字，后面是冒号
                    # 启发式判断：以大写字母开头视为类型名，否则视为变量名
                    if first and first[0].isupper():
                        catch_type = first
                    else:
                        catch_var = first
                elif next_tok and next_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    # 情况2或4：有类型和变量名
                    catch_type = first
                    catch_var = self._consume().value
                else:
                    # 只有一个标识符，视为变量名
                    catch_var = first
            
            # 冒号
            self._consume(TokenType.COLON)
            
            # catch块
            catch_body = self._parse_body()
        
        # 最终（可选）
        finally_body = []
        if self._match(TokenType.KEYWORD, '最终'):
            self._consume(TokenType.KEYWORD, '最终')
            
            # 冒号
            self._consume(TokenType.COLON)
            
            # finally块
            finally_body = self._parse_body()
        
        return TryStmt(try_body, catch_type, catch_var, catch_body, finally_body)
    
    def _parse_throw_stmt(self) -> ThrowStmt:
        """解析抛出异常语句
        
        语法：抛出 表达式。
        """
        # 抛出
        self._consume(TokenType.KEYWORD, '抛出')
        
        # 异常值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return ThrowStmt(value)
    
    def _parse_paragraph(self) -> Paragraph:
        """解析段落定义：《段名》段"""
        # 《
        self._consume(TokenType.LBOOK)
        
        # 段名
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 》
        self._consume(TokenType.RBOOK)
        
        # 段
        self._consume(TokenType.KEYWORD, '段')
        
        # 参数列表
        params = []
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            
            while not self._match(TokenType.RPAREN):
                # 参数名（允许KEYWORD或IDENTIFIER）
                tok = self._peek()
                if tok and tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                elif tok and tok.type == TokenType.KEYWORD:
                    param_name = self._consume(TokenType.KEYWORD).value
                elif tok and tok.type == TokenType.CHINESE_NUM:
                    param_name = str(self._consume(TokenType.CHINESE_NUM).value)
                elif tok and tok.type == TokenType.NUMBER:
                    param_name = str(self._consume(TokenType.NUMBER).value)
                else:
                    raise ParseError(f"期望参数名，但得到 {tok.type if tok else '输入结束'}（位置: L{tok.line if tok else '?'}:C{tok.col if tok else '?'}）")
                
                # 类型注解（可选）
                param_type = None
                if self._match(TokenType.COLON):
                    self._consume(TokenType.COLON)
                    param_type = self._consume(TokenType.IDENTIFIER).value
                
                params.append({'name': param_name, 'type': param_type})
                
                # 逗号分隔
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
            
            self._consume(TokenType.RPAREN)
        
        # 返回类型（可选）
        return_type = None
        if self._match(TokenType.ARROW):
            self._consume(TokenType.ARROW)
            return_type = self._consume(TokenType.IDENTIFIER).value
        
        # 冒号（可选）
        has_colon = False
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
            has_colon = True
        
        # 段落体
        if has_colon:
            body = self._parse_body()
            
            # 消耗"结束"关键字（块模式需要）
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
                self._consume(TokenType.KEYWORD, '结束')
                # 消耗可选的句号
                if self._current() and self._current().type == TokenType.DOT:
                    self._consume(TokenType.DOT)
            else:
                tok = self._current()
                if tok:
                    raise ParseError(f"块模式段落定义需要'结束'关键字，但得到 '{tok.value}'", tok.line, tok.col, tok.value)
        else:
            stmt = self._parse_statement()
            body = [stmt] if stmt else []
        
        return Paragraph(name, params, return_type, body)
    
    def _parse_paragraph_v2(self) -> Paragraph:
        """解析段落定义：段落/段 段名 参数/接收 参数名。"""
        # 段落 或 段
        if self._match(TokenType.KEYWORD, '段落'):
            self._consume(TokenType.KEYWORD, '段落')
        elif self._match(TokenType.KEYWORD, '段'):
            self._consume(TokenType.KEYWORD, '段')
        else:
            tok = self._current()
            raise ParseError(f"期望'段落'或'段'，但得到 {tok.type if tok else '输入结束'} = '{tok.value if tok else ''}'",
                             tok.line if tok else 0, tok.col if tok else 0, tok.value if tok else None)
        
        # 段名（支持IDENTIFIER, CHINESE_NUM, KEYWORD）
        name_tok = self._current()
        name_parts = []
        if name_tok and name_tok.type == TokenType.IDENTIFIER:
            name_parts.append(self._consume(TokenType.IDENTIFIER).value)
        elif name_tok and name_tok.type == TokenType.CHINESE_NUM:
            name_parts.append(str(self._consume(TokenType.CHINESE_NUM).value))
        elif name_tok and name_tok.type == TokenType.KEYWORD:
            name_parts.append(self._consume(TokenType.KEYWORD).value)
        else:
            raise ParseError(f"期望标识符或中文数字作为段名，但得到 {name_tok.type if name_tok else '输入结束'}", name_tok.line if name_tok else 0, name_tok.col if name_tok else 0, name_tok.value if name_tok else None)
        
        # 继续收集连续的中文数字或标识符/关键字作为段名（例如"三倍"）
        while self._current():
            next_tok = self._current()
            if next_tok.type == TokenType.IDENTIFIER:
                name_parts.append(self._consume(TokenType.IDENTIFIER).value)
            elif next_tok.type == TokenType.CHINESE_NUM:
                name_parts.append(str(self._consume(TokenType.CHINESE_NUM).value))
            elif next_tok.type == TokenType.KEYWORD and next_tok.value not in ('参数', '接收', '返回', '结束'):
                name_parts.append(self._consume(TokenType.KEYWORD).value)
            else:
                break
        
        name = ''.join(name_parts)
        
        # 参数列表（可选）- 支持"参数"和"接收"两种写法
        params = []
        has_params = False
        if self._match(TokenType.KEYWORD, '参数'):
            self._consume(TokenType.KEYWORD, '参数')
            has_params = True
        elif self._match(TokenType.KEYWORD, '接收'):
            self._consume(TokenType.KEYWORD, '接收')
            has_params = True
        
        if has_params:
            
            # 收集参数名，直到句号或"返回"
            while self._current() and self._current().type != TokenType.DOT:
                tok = self._current()
                # 遇到"返回"结束参数收集
                if tok.type == TokenType.KEYWORD and tok.value == '返回':
                    break
                # 跳过逗号分隔符
                if tok.type == TokenType.COMMA:
                    self._consume(TokenType.COMMA)
                    continue
                if tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                    params.append({'name': param_name, 'type': None})
                elif tok.type == TokenType.KEYWORD:
                    # 参数名可能是关键字
                    param_name = self._consume(TokenType.KEYWORD).value
                    params.append({'name': param_name, 'type': None})
                else:
                    break
        
        # 返回类型（可选）
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '返回':
            self._consume(TokenType.KEYWORD, '返回')
        
        # 句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 冒号（支持：或：）
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
        
        # 段落体
        body = self._parse_body()
        
        # 消耗"结束"关键字（如果有）
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
        
        # 消耗句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return Paragraph(name, params, None, body)
    
    def _parse_body(self) -> List[ASTNode]:
        """解析代码块（简化版：不处理缩进）"""
        statements = []

        # 简化处理：最多解析100条语句
        max_statements = 100
        count = 0

        while self._current() and count < max_statements:
            tok = self._current()

            # 结束标记（但不消耗，让上层决定）
            if tok.type == TokenType.KEYWORD and tok.value in ('否则', '结束'):
                break
            
            # 异常处理的特殊标记（捕获、最终）
            if tok.type == TokenType.KEYWORD and tok.value in ('捕获', '最终'):
                break

            # DEDENT标记（缩进结束）
            if tok.type == TokenType.DEDENT:
                break

            # 解析语句
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
                count += 1
            else:
                break

        return statements
    
    def _parse_expr(self) -> ASTNode:
        """解析表达式（支持管道操作符和逻辑运算符）"""
        left = self._parse_logical_expr()
        
        # 管道操作符
        stages = [left]
        
        while self._match(TokenType.ARROW) or self._match(TokenType.COMMA):
            if self._match(TokenType.ARROW):
                self._consume(TokenType.ARROW)
            else:
                self._consume(TokenType.COMMA)
            
            right = self._parse_logical_expr()
            stages.append(right)
        
        if len(stages) > 1:
            return Pipeline(stages)
        
        return left
    
    def _parse_logical_expr(self) -> ASTNode:
        """解析逻辑表达式（且/与, 或）"""
        left = self._parse_comparison()
        
        while self._current():
            tok = self._current()
            if tok.type == TokenType.KEYWORD and tok.value in self.LOGICAL_OP_MAP:
                op = self._consume().value
                right = self._parse_comparison()
                left = BinaryOp(self.LOGICAL_OP_MAP[op], left, right)
            else:
                break
        
        return left
    
    def _parse_comparison(self) -> ASTNode:
        """解析比较表达式"""
        left = self._parse_add_expr()
        
        while self._current():
            tok = self._current()
            # 遇到"那么"关键字，停止解析
            if tok.type == TokenType.KEYWORD and tok.value == '那么':
                break
            if tok.type == TokenType.KEYWORD and tok.value in self.OPERATOR_VERBS:
                op = self._consume().value
                right = self._parse_add_expr()
                left = BinaryOp(self.COMPARISON_OP_MAP.get(op, op), left, right)
            else:
                break
        
        return left
    
    def _parse_add_expr(self) -> ASTNode:
        """解析加减表达式"""
        left = self._parse_mul_expr()
        
        while self._current():
            tok = self._current()
            # 支持：加、减、加上、减去
            if tok.type == TokenType.KEYWORD and tok.value in self.ADD_OP_MAP:
                op = self._consume().value
                right = self._parse_mul_expr()
                left = BinaryOp(self.ADD_OP_MAP[op], left, right)
            else:
                break
        
        return left
    
    def _parse_mul_expr(self) -> ASTNode:
        """解析乘除表达式"""
        left = self._parse_primary()
        
        while self._current():
            tok = self._current()
            # 支持：乘、除、乘以、除以
            if tok.type == TokenType.KEYWORD and tok.value in self.MUL_OP_MAP:
                op = self._consume().value
                # 重要：右侧应该解析为完整的加减表达式，而非仅primary
                # 这样'数 乘以 计算阶乘 数 减一'会被正确解析为：数 * 计算阶乘(数 - 1)
                right = self._parse_add_expr()
                left = BinaryOp(self.MUL_OP_MAP[op], left, right)
            else:
                # 遇到加减运算符或其他，返回让上层处理
                break
        
        return left
    
    def _parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        tok = self._current()
        
        if tok is None:
            raise ParseError(f"意外的输入结束")
        
        # 三元条件表达式：如果 条件 那么 值1 否则 值2
        if tok.type == TokenType.KEYWORD and tok.value == '如果':
            self._consume(TokenType.KEYWORD, '如果')
            condition = self._parse_expr()
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '那么':
                self._consume(TokenType.KEYWORD, '那么')
            then_expr = self._parse_expr()
            else_expr = None
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '否则':
                self._consume(TokenType.KEYWORD, '否则')
                else_expr = self._parse_expr()
            return ConditionalExpression(condition, then_expr, else_expr)
        
        # 括号表达式
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return self._parse_postfix(expr)
        
        # 数字
        if tok.type == TokenType.NUMBER:
            self._consume()
            expr = NumberLiteral(tok.value)
            return self._parse_postfix(expr)

        # 中文数字
        if tok.type == TokenType.CHINESE_NUM:
            self._consume()
            
            # 检查中文数字后是否紧接标识符（如"三倍"作为函数名）
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.IDENTIFIER:
                id_name = self._consume(TokenType.IDENTIFIER).value
                expr = Identifier(f"{tok.value}{id_name}")
                return self._parse_postfix(expr)
            
            expr = NumberLiteral(tok.value)
            return self._parse_postfix(expr)

        # 匿名函数：接收 参数：返回 表达式。
        if tok.type == TokenType.KEYWORD and tok.value == '接收':
            return self._parse_lambda()

        # 字符串（支持插值检测）
        if tok.type == TokenType.STRING:
            self._consume()
            # 检测插值表达式 {xxx}
            interpolated = self._parse_string_interpolation(tok.value, tok.line, tok.col)
            if interpolated is not None:
                return self._parse_postfix(interpolated)
            expr = StringLiteral(tok.value)
            return self._parse_postfix(expr)

        # 特殊值（真、假、空）
        if tok.type == TokenType.KEYWORD and tok.value in KEYWORDS_SPECIAL:
            self._consume()
            # 转换为对应的Python值
            if tok.value == '真':
                expr = Identifier('True')
            elif tok.value == '假':
                expr = Identifier('False')
            else:  # '空'
                expr = Identifier('None')
            return self._parse_postfix(expr)

        # 段落调用：《段名》(参数)
        if tok.type == TokenType.LBOOK:
            expr = self._parse_paragraph_call()
            return self._parse_postfix(expr)

        # 动词调用（KEYWORD token 且值为动词，但排除运算符动词）
        # 运算符动词由 _parse_add_expr 等方法处理
        if tok.type == TokenType.KEYWORD and tok.value in VERB_ARITY and tok.value not in self.OPERATOR_VERBS:
            verb_name = tok.value
            self._consume()
            
            # 特殊处理：新建（类实例化）
            if verb_name == '新建':
                # 新建 类名 参数...
                # 类名可能由多个token组成（如"空类"中"空"是KEYWORD，"类"是KEYWORD）
                class_name_parts = []
                while self._current():
                    ct = self._current()
                    if ct.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                        class_name_parts.append(ct.value)
                        self._consume()
                    else:
                        break
                class_name = ''.join(class_name_parts)
                
                if not class_name:
                    raise ParseError("期望类名")
                
                # 收集参数（直到遇到阻断符）
                args = []
                while self._current():
                    next_tok = self._current()
                    if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                        break
                    arg = self._collect_primary_arg()
                    if arg:
                        args.append(arg)
                    else:
                        break
                
                expr = ClassInstantiation(class_name, args)
                return self._parse_postfix(expr)
            
            # 收集参数（元数驱动）
            arity = VERB_ARITY[verb_name]
            args = []

            if arity == 0:
                # 无参数函数
                pass
            elif arity == -1:
                # 可变参数：收集到阻断符为止
                while self._current():
                    next_tok = self._current()
                    if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                        break
                    # 收集完整表达式（支持嵌套函数调用和运算符）
                    arg = self._parse_comparison()
                    if arg:
                        args.append(arg)
                    else:
                        break
            else:
                # 固定参数数量（使用完整表达式解析，支持嵌套函数调用和比较运算符）
                for _ in range(arity):
                    if self._current() and self._current().type not in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN):
                        arg = self._parse_comparison()
                        if arg:
                            args.append(arg)

            expr = ParagraphCall(verb_name, args)
            return self._parse_postfix(expr)

        # 标识符：可能带参数（段落调用）
        if tok.type == TokenType.IDENTIFIER:
            return self._collect_single_arg()

        # 运算符动词作为函数调用（如"除(10, 0)"或"幂 二 十"）
        if tok.type == TokenType.KEYWORD and tok.value in self.OPERATOR_VERBS:
            name = tok.value
            next_tok = self._peek(1)
            if next_tok and next_tok.type == TokenType.LPAREN:
                # 函数调用 with parentheses
                self._consume()
                self._consume(TokenType.LPAREN)
                args = []
                while self._current() and self._current().type != TokenType.RPAREN:
                    if self._current().type == TokenType.COMMA:
                        self._consume(TokenType.COMMA)
                        continue
                    arg = self._parse_comparison()
                    if arg:
                        args.append(arg)
                    else:
                        break
                self._consume(TokenType.RPAREN)
                expr = ParagraphCall(name, args)
                return self._parse_postfix(expr)
            else:
                # 无括号：动词 参数1 参数2（如"幂 二 十"）
                # 使用元数驱动参数收集
                self._consume()
                arity = VERB_ARITY.get(name, 2)
                args = []
                if arity == -1:
                    # 可变参数
                    while self._current():
                        next_tok = self._current()
                        if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                            break
                        if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                            break
                        arg = self._parse_comparison()
                        if arg:
                            args.append(arg)
                        else:
                            break
                else:
                    # 固定参数
                    for _ in range(arity):
                        if self._current() and self._current().type not in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN):
                            arg = self._parse_comparison()
                            if arg:
                                args.append(arg)
                expr = ParagraphCall(name, args)
                return self._parse_postfix(expr)

        # 列表字面量 [元素1, 元素2, ...]
        if tok.type == TokenType.LBRACKET:
            return self._parse_list_literal()

        # Self引用：己属性名
        if tok.type == TokenType.KEYWORD and tok.value == '己':
            self._consume()
            # 收集属性名（可能多字）
            name_parts = []
            while self._current() and self._current().type == TokenType.IDENTIFIER:
                name_parts.append(self._consume().value)
            if name_parts:
                attr_name = ''.join(name_parts)
                expr = Identifier(f"self.{attr_name}")
                return self._parse_postfix(expr)
            else:
                raise ParseError("己引用后应跟属性名", tok.line, tok.col)

        # Super引用：父.方法名() → super().方法名()
        if tok.type == TokenType.KEYWORD and tok.value == '父':
            self._consume()
            expr = Identifier("super()")
            return self._parse_postfix(expr)

        raise ParseError(f"意外的标记: {tok.type} = '{tok.value}'（附近: '{tok.value}'）", tok.line, tok.col)

    def _collect_primary_arg(self) -> Optional[ASTNode]:
        """收集单个primary参数（不进行段落调用检测）"""
        tok = self._current()
        if tok is None:
            return None

        # 数字
        if tok.type == TokenType.NUMBER:
            self._consume()
            return NumberLiteral(tok.value)

        # 中文数字
        if tok.type == TokenType.CHINESE_NUM:
            self._consume()
            return NumberLiteral(tok.value)

        # 字符串
        if tok.type == TokenType.STRING:
            self._consume()
            return StringLiteral(tok.value)

        # 标识符（检查是否为函数调用，如"字符串长度 日期"）
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            self._consume()
            
            # 检查下一个token是否是参数（嵌套函数调用模式）
            next_tok = self._current()
            if next_tok and next_tok.type in (TokenType.NUMBER, TokenType.CHINESE_NUM, TokenType.STRING,
                                               TokenType.IDENTIFIER, TokenType.LBOOK):
                # 可能是函数调用，尝试收集后续参数
                args = []
                while self._current():
                    nt = self._current()
                    # 停止条件
                    if nt.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    # 遇到动词运算符停止（如加、减、大于等）
                    if nt.type == TokenType.KEYWORD and nt.value in self.OPERATOR_VERBS:
                        break
                    # 遇到其他关键字停止
                    if nt.type == TokenType.KEYWORD and nt.value in KEYWORDS_DOUBLE:
                        break
                    
                    # 收集参数
                    if nt.type == TokenType.NUMBER:
                        args.append(NumberLiteral(self._consume().value))
                    elif nt.type == TokenType.CHINESE_NUM:
                        args.append(NumberLiteral(self._consume().value))
                    elif nt.type == TokenType.STRING:
                        args.append(StringLiteral(self._consume().value))
                    elif nt.type == TokenType.IDENTIFIER:
                        args.append(Identifier(self._consume().value))
                    elif nt.type == TokenType.LBOOK:
                        args.append(self._parse_paragraph_call())
                    else:
                        break
                
                if args:
                    expr = ParagraphCall(name, args)
                    return self._parse_postfix(expr)
            
            # 简单标识符
            expr = Identifier(name)
            return self._parse_postfix(expr)

        # 关键字作为标识符（检查是否为函数调用）
        if tok.type == TokenType.KEYWORD:
            name = tok.value
            self._consume()
            
            # 检查下一个token是否构成函数调用
            next_tok = self._current()
            if next_tok and next_tok.type in (TokenType.NUMBER, TokenType.CHINESE_NUM, TokenType.STRING,
                                               TokenType.IDENTIFIER):
                # 可能是函数调用，尝试收集后续参数
                args = []
                while self._current():
                    nt = self._current()
                    # 停止条件
                    if nt.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    # 遇到动词运算符停止
                    if nt.type == TokenType.KEYWORD and nt.value in self.OPERATOR_VERBS:
                        break
                    # 遇到其他关键字停止（双字关键字通常是语句结构）
                    if nt.type == TokenType.KEYWORD and nt.value in KEYWORDS_DOUBLE:
                        break
                    
                    if nt.type == TokenType.NUMBER:
                        args.append(NumberLiteral(self._consume().value))
                    elif nt.type == TokenType.CHINESE_NUM:
                        args.append(NumberLiteral(self._consume().value))
                    elif nt.type == TokenType.STRING:
                        args.append(StringLiteral(self._consume().value))
                    elif nt.type == TokenType.IDENTIFIER:
                        args.append(Identifier(self._consume().value))
                    else:
                        break
                
                if args:
                    expr = ParagraphCall(name, args)
                    return self._parse_postfix(expr)
            
            # 简单标识符
            expr = Identifier(name)
            return self._parse_postfix(expr)

        # 特殊值
        if tok.type == TokenType.KEYWORD and tok.value in KEYWORDS_SPECIAL:
            self._consume()
            if tok.value == '真':
                return Identifier('True')
            elif tok.value == '假':
                return Identifier('False')
            else:  # '空'
                return Identifier('None')

        # 书名号段落调用
        if tok.type == TokenType.LBOOK:
            return self._parse_paragraph_call()

        # 括号表达式
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return expr

        # 列表字面量
        if tok.type == TokenType.LBRACKET:
            return self._parse_list_literal()

        return None

    def _collect_single_arg(self) -> Optional[ASTNode]:
        """收集单个参数（可能包含段落调用）"""
        tok = self._current()
        if tok is None:
            return None

        # 数字
        if tok.type == TokenType.NUMBER:
            self._consume()
            return NumberLiteral(tok.value)

        # 中文数字
        if tok.type == TokenType.CHINESE_NUM:
            self._consume()
            return NumberLiteral(tok.value)

        # 字符串
        if tok.type == TokenType.STRING:
            self._consume()
            return StringLiteral(tok.value)

        # 标识符
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            self._consume()
            
            # 运算符动词（不应收集为参数）
            
            # 检查下一个token是否是运算符动词
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value in self.OPERATOR_VERBS:
                # 下一个是运算符，不收集参数，直接返回标识符
                expr = Identifier(name)
            else:
                # 检查是否是段落调用（标识符后跟参数）
                args = []
                while self._current():
                    next_tok = self._current()
                    # 停止条件：句号、逗号、右括号
                    if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    # 遇到运算符动词停止
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in self.OPERATOR_VERBS:
                        break
                    # 遇到其他关键字（除运算符动词外）停止
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                        break
                    
                    # 收集单个参数（只收集primary，不包含运算）
                    if next_tok.type == TokenType.NUMBER:
                        args.append(NumberLiteral(self._consume().value))
                    elif next_tok.type == TokenType.CHINESE_NUM:
                        args.append(NumberLiteral(self._consume().value))
                    elif next_tok.type == TokenType.STRING:
                        args.append(StringLiteral(self._consume().value))
                    elif next_tok.type == TokenType.IDENTIFIER:
                        # 收集标识符作为独立参数（不嵌套）
                        args.append(Identifier(self._consume().value))
                    else:
                        break
                
                # 如果有参数，作为段落调用
                if args:
                    expr = ParagraphCall(name, args)
                else:
                    expr = Identifier(name)
            
            return self._parse_postfix(expr)
        
        # 关键字作为标识符（如参数名）
        if tok.type == TokenType.KEYWORD:
            name = tok.value
            self._consume()
            
            # 同样检查是否是段落调用
            args = []
            while self._current():
                next_tok = self._current()
                if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                    break
                if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                    break
                
                arg = self._collect_primary_arg()
                if arg:
                    args.append(arg)
                else:
                    break
            
            if args:
                expr = ParagraphCall(name, args)
            else:
                expr = Identifier(name)
            
            return self._parse_postfix(expr)
        
        # 特殊值
        if tok.type == TokenType.KEYWORD and tok.value in KEYWORDS_SPECIAL:
            self._consume()
            if tok.value == '真':
                return Identifier('True')
            elif tok.value == '假':
                return Identifier('False')
            else:  # '空'
                return Identifier('None')

        # 段落调用
        if tok.type == TokenType.LBOOK:
            return self._parse_paragraph_call()

        # 括号表达式
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return expr

        # 列表字面量
        if tok.type == TokenType.LBRACKET:
            return self._parse_list_literal()

        # 注意：不再递归处理动词，避免无限循环
        # 动词作为独立语句处理，不作为参数
        return None

        # 数字
        if tok.type == TokenType.NUMBER:
            self._consume()
            return NumberLiteral(tok.value)

        # 中文数字
        if tok.type == TokenType.CHINESE_NUM:
            self._consume()
            return NumberLiteral(tok.value)

        # 字符串
        if tok.type == TokenType.STRING:
            self._consume()
            return StringLiteral(tok.value)

        # 标识符
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            self._consume()
            
            # 运算符动词（不应收集为参数）
            
            # 检查下一个token是否是运算符动词
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value in self.OPERATOR_VERBS:
                # 下一个是运算符，不收集参数，直接返回标识符
                expr = Identifier(name)
            else:
                # 检查是否是段落调用（标识符后跟参数）
                args = []
                while self._current():
                    next_tok = self._current()
                    # 停止条件：句号、逗号、右括号
                    if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                        break
                    # 遇到运算符动词停止
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in self.OPERATOR_VERBS:
                        break
                    # 遇到其他关键字（除运算符动词外）停止
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                        break
                    
                    # 收集单个参数（只收集primary，不包含运算）
                    if next_tok.type == TokenType.NUMBER:
                        args.append(NumberLiteral(self._consume().value))
                    elif next_tok.type == TokenType.CHINESE_NUM:
                        args.append(NumberLiteral(self._consume().value))
                    elif next_tok.type == TokenType.STRING:
                        args.append(StringLiteral(self._consume().value))
                    elif next_tok.type == TokenType.IDENTIFIER:
                        # 收集标识符作为独立参数（不嵌套）
                        args.append(Identifier(self._consume().value))
                    else:
                        break
                
                # 如果有参数，作为段落调用
                if args:
                    expr = ParagraphCall(name, args)
                else:
                    expr = Identifier(name)
            
            return self._parse_postfix(expr)
        
        # 关键字作为标识符（如参数名）
        if tok.type == TokenType.KEYWORD:
            name = tok.value
            self._consume()
            
            # 同样检查是否是段落调用
            args = []
            while self._current():
                next_tok = self._current()
                if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                    break
                if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                    break
                
                arg = self._collect_single_arg()
                if arg:
                    args.append(arg)
                else:
                    break
            
            if args:
                expr = ParagraphCall(name, args)
            else:
                expr = Identifier(name)
            
            return self._parse_postfix(expr)
        
        # 特殊值
        if tok.type == TokenType.KEYWORD and tok.value in KEYWORDS_SPECIAL:
            self._consume()
            if tok.value == '真':
                return Identifier('True')
            elif tok.value == '假':
                return Identifier('False')
            else:  # '空'
                return Identifier('None')

        # 段落调用
        if tok.type == TokenType.LBOOK:
            return self._parse_paragraph_call()

        # 括号表达式
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return expr

        # 注意：不再递归处理动词，避免无限循环
        # 动词作为独立语句处理，不作为参数

        return None
    
    def _parse_string_interpolation(self, value: str, line: int = 0, col: int = 0):
        """检测字符串插值：如果字符串包含 {xxx}，返回 StringInterpolation 节点，否则返回 None"""
        if '{' not in value:
            return None

        import re
        parts = []
        last_end = 0
        for m in re.finditer(r'\{([^}]+)\}', value):
            # 插值前的普通文本
            if m.start() > last_end:
                parts.append(value[last_end:m.start()])
            # 插值表达式（作为标识符）
            expr_text = m.group(1).strip()
            parts.append(Identifier(expr_text))
            last_end = m.end()

        # 尾部普通文本
        if last_end < len(value):
            parts.append(value[last_end:])

        # 如果只有普通文本（没有真正的插值），返回 None
        has_expr = any(isinstance(p, Identifier) for p in parts)
        if not has_expr:
            return None

        return StringInterpolation(parts)

    def _parse_lambda(self) -> LambdaExpression:
        """解析匿名函数：接收 参数1 参数2：返回 表达式。 或 接收 参数1 参数2：表达式。"""
        # 接收
        self._consume(TokenType.KEYWORD, '接收')
        
        # 收集参数名（支持标识符和大部分关键字作为参数名）
        params = []
        while self._current():
            tok = self._current()
            if tok.type == TokenType.IDENTIFIER:
                params.append(self._consume(TokenType.IDENTIFIER).value)
            elif tok.type == TokenType.KEYWORD and tok.value not in ('返回', '结束', '匹配', '情况', '如果', '否则', '遍历', '当', '设', '定义', '类', '构造', '段落', '尝试', '捕获', '抛出', '最终', '导入', '导出', '从'):
                # 允许非语句关键字作为参数名
                params.append(self._consume(TokenType.KEYWORD).value)
            else:
                break
        
        # 冒号
        if self._match(TokenType.COLON):
            self._consume(TokenType.COLON)
        
        # 可选的"返回"关键字
        if self._match(TokenType.KEYWORD, '返回'):
            self._consume(TokenType.KEYWORD, '返回')
        
        # 表达式（函数体）
        body = self._parse_comparison()
        
        # 可选的句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return LambdaExpression(params, body)

    def _parse_list_literal(self) -> ASTNode:
        """解析列表字面量或列表推导
        
        普通列表：[元素1, 元素2, ...]
        列表推导：[表达式 遍历 变量 之 可迭代对象] 或 [表达式 遍历 变量 之 可迭代对象 若 条件]
        """
        self._consume(TokenType.LBRACKET)
        
        # 空列表
        if self._match(TokenType.RBRACKET):
            self._consume(TokenType.RBRACKET)
            return ListLiteral([])
        
        # 解析第一个元素/表达式
        first_expr = self._parse_comparison()
        
        # 检查是否是字典推导：键: 值 遍历 变量 之 ...
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
            value_expr = self._parse_comparison()
            
            # 检查后面是否有"遍历"
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '遍历':
                self._consume(TokenType.KEYWORD, '遍历')
                
                # 变量名
                var_tok = self._current()
                if var_tok and var_tok.type == TokenType.IDENTIFIER:
                    variable = self._consume(TokenType.IDENTIFIER).value
                elif var_tok and var_tok.type == TokenType.KEYWORD:
                    variable = self._consume(TokenType.KEYWORD).value
                else:
                    raise ParseError(f"字典推导期望变量名", 
                                     var_tok.line if var_tok else 0, var_tok.col if var_tok else 0)
                
                # 之
                if self._match(TokenType.KEYWORD, '之'):
                    self._consume(TokenType.KEYWORD, '之')
                elif self._match(TokenType.KEYWORD, '在'):
                    self._consume(TokenType.KEYWORD, '在')
                else:
                    tok = self._current()
                    raise ParseError(f"字典推导期望'之'或'在'",
                                     tok.line if tok else 0, tok.col if tok else 0)
                
                # 可迭代对象
                iterable = self._parse_comparison()
                
                # 可选条件
                condition = None
                tok = self._current()
                if tok and tok.type == TokenType.KEYWORD and tok.value in ('若', '如果'):
                    self._consume()
                    condition = self._parse_expr()
                
                self._consume(TokenType.RBRACKET)
                return DictComprehension(first_expr, value_expr, variable, iterable, condition)
            
            # 普通字典字面量：键: 值, 键: 值, ...
            entries = [(first_expr, value_expr)]
            while self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                key = self._parse_comparison()
                self._consume(TokenType.COLON)
                val = self._parse_comparison()
                entries.append((key, val))
            self._consume(TokenType.RBRACKET)
            return DictLiteral(entries)
        
        # 检查是否是列表推导（后面跟着"遍历"关键字）
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '遍历':
            # 列表推导模式
            self._consume(TokenType.KEYWORD, '遍历')
            
            # 变量名
            var_tok = self._current()
            if var_tok and var_tok.type == TokenType.IDENTIFIER:
                variable = self._consume(TokenType.IDENTIFIER).value
            elif var_tok and var_tok.type == TokenType.KEYWORD:
                variable = self._consume(TokenType.KEYWORD).value
            else:
                raise ParseError(f"列表推导期望变量名，但得到 {var_tok.type if var_tok else '输入结束'}",
                                 var_tok.line if var_tok else 0, var_tok.col if var_tok else 0)
            
            # 之 / 在
            if self._match(TokenType.KEYWORD, '之'):
                self._consume(TokenType.KEYWORD, '之')
            elif self._match(TokenType.KEYWORD, '在'):
                self._consume(TokenType.KEYWORD, '在')
            else:
                tok = self._current()
                raise ParseError(f"列表推导期望'之'或'在'，但得到 {tok.type if tok else '输入结束'}",
                                 tok.line if tok else 0, tok.col if tok else 0)
            
            # 可迭代对象
            iterable = self._parse_comparison()
            
            # 可选条件：若 条件 或 如果 条件
            condition = None
            tok = self._current()
            if tok and ((tok.type == TokenType.KEYWORD and tok.value in ('若', '如果')) or
                        (tok.type == TokenType.IDENTIFIER and tok.value == '若')):
                self._consume()
                condition = self._parse_expr()
            
            self._consume(TokenType.RBRACKET)
            return ListComprehension(first_expr, variable, iterable, condition)
        
        # 普通列表
        elements = [first_expr]
        while self._match(TokenType.COMMA):
            self._consume(TokenType.COMMA)
            elem = self._parse_comparison()
            if elem:
                elements.append(elem)
            else:
                break
        
        self._consume(TokenType.RBRACKET)
        return ListLiteral(elements)
    
    def _parse_postfix(self, expr: ASTNode) -> ASTNode:
        """解析后缀表达式（索引访问、成员访问、函数调用）"""
        while self._current():
            tok = self._current()
            
            # 函数调用：(参数1, 参数2, ...)
            # 例如：累计(数值 减 1)  或  三倍(甲)
            if tok.type == TokenType.LPAREN:
                self._consume(TokenType.LPAREN)
                
                # 获取函数名
                if isinstance(expr, Identifier):
                    func_name = expr.name
                elif isinstance(expr, str):
                    func_name = expr
                else:
                    raise ParseError(f"不支持在复杂表达式后进行括号调用: {type(expr).__name__}（可将'()'改为'。'或去掉括号）")
                
                # 收集参数（直到右括号）- 使用比较表达式而非完整表达式
                # 以避免逗号被当作管道操作符处理
                args = []
                while not self._match(TokenType.RPAREN):
                    arg = self._parse_comparison()
                    if arg is not None:
                        args.append(arg)
                    else:
                        break
                    # 逗号分隔
                    if self._match(TokenType.COMMA):
                        self._consume(TokenType.COMMA)
                
                self._consume(TokenType.RPAREN)
                expr = ParagraphCall(func_name, args)
                continue
            
            # 成员访问：obj.member 或 obj.method()
            # 注意：需要区分英文点号(.)和中文句号(。)
            is_dot_access = False
            if tok.type == TokenType.DOT:
                # 检查是否是英文点号（成员访问）还是中文句号（语句结束）
                if tok.value == '.':
                    is_dot_access = True
                # 中文句号(。)是语句结束符，不进行成员访问
            
            if is_dot_access:
                self._consume()  # 消耗点号
                
                # 获取成员名
                member_tok = self._current()
                if member_tok and member_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    member_name = member_tok.value
                    self._consume()
                    
                    # 检查是否是方法调用（后面跟着参数）
                    args = []
                    has_parens = False
                    
                    # 检查是否是括号括起来的参数列表
                    if self._current() and self._current().type == TokenType.LPAREN:
                        has_parens = True
                        self._consume(TokenType.LPAREN)
                        # 收集参数直到右括号
                        while not self._match(TokenType.RPAREN):
                            arg = self._parse_comparison()
                            if arg is not None:
                                args.append(arg)
                            else:
                                break
                            if self._match(TokenType.COMMA):
                                self._consume(TokenType.COMMA)
                        self._consume(TokenType.RPAREN)
                    else:
                        # 无括号模式：收集参数直到阻断符
                        while self._current():
                            next_tok = self._current()
                            # 阻断符：句号、逗号、右括号、右中括号、关键字
                            if next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET):
                                break
                            if next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE:
                                break
                            
                            # 收集参数
                            arg = self._collect_primary_arg()
                            if arg:
                                args.append(arg)
                            else:
                                break
                    
                    # 有括号一定是方法调用，无括号根据参数数量判断
                    is_method_call = has_parens or len(args) > 0
                    expr = MemberAccess(expr, member_name, is_method_call, args)
                    continue
                else:
                    raise ParseError(f"期望成员名，但得到 {member_tok.type} = '{member_tok.value}'", member_tok.line, member_tok.col)
            
            # 索引访问：[index] 或 【index】
            if tok.type == TokenType.LBRACKET:
                self._consume(TokenType.LBRACKET)
                index = self._parse_expr()
                self._consume(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            else:
                break
        
        return expr
    
    def _parse_paragraph_call(self) -> ASTNode:
        """解析书名号内容：可能是字符串字面量或段落调用"""
        # 《
        self._consume(TokenType.LBOOK)
        
        # 段名或字符串内容
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 》
        self._consume(TokenType.RBOOK)
        
        # 如果后面跟着 LPAREN，则是段落调用
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            
            args = []
            while not self._match(TokenType.RPAREN):
                arg = self._parse_expr()
                args.append(arg)
                
                # 逗号分隔
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
            
            self._consume(TokenType.RPAREN)
            
            return ParagraphCall(name, args)
        
        # 否则是字符串字面量
        return StringLiteral(name)
    
    # =============================================================================
    # 类定义解析
    # =============================================================================
    
    def _parse_class_definition(self) -> ClassDefinition:
        """解析类定义
        
        语法：
        类 类名。
          属性 属性名。
          属性 属性名。
          
          构造 参数 参数名 参数名。
            己属性名 为 参数名。
          结束。
          
          段落 方法名 参数 参数名。
            方法体。
          结束。
        结束。
        
        或带继承：
        类 类名 继承 父类名。
          ...
        结束。
        """
        # 类
        self._consume(TokenType.KEYWORD, '类')
        
        # 类名（支持IDENTIFIER和KEYWORD，可能由多个token组成如"空类"）
        name_parts = []
        name_tok = self._current()
        if name_tok and name_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                # 检查是否遇到"继承"或"实现"关键字
                if self._current().type == TokenType.KEYWORD and self._current().value in ('继承', '实现'):
                    break
                # 检查是否遇到句号或冒号
                if self._current().type in (TokenType.DOT, TokenType.COLON):
                    break
                name_parts.append(self._consume().value)
        else:
            raise ParseError(f"期望类名，但得到 {name_tok.type if name_tok else '输入结束'}")
        class_name = ''.join(name_parts)
        
        # 继承？（可选）
        base_classes = []
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '继承':
            self._consume(TokenType.KEYWORD, '继承')
            base_tok = self._current()
            if base_tok and base_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                base_classes = [base_tok.value]
                self._consume()
            else:
                raise ParseError(f"期望父类名，但得到 {base_tok.type if base_tok else '输入结束'}")
        
        # 实现接口（可选）
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '实现':
            self._consume(TokenType.KEYWORD, '实现')
            impl_interfaces = []
            while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                # 收集多 token 名称（如"可打印"被拆为"可"+"打印"）
                parts = []
                while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    if self._current().type in (TokenType.COLON, TokenType.DOT):
                        break
                    if self._current().type == TokenType.KEYWORD and self._current().value in ('结束',):
                        break
                    parts.append(self._consume().value)
                if parts:
                    impl_interfaces.append(''.join(parts))
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                else:
                    break
            # 合并到 base_classes
            if not base_classes:
                base_classes = []
            base_classes.extend(impl_interfaces)
        
        # 句号或冒号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        elif self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
        else:
            raise ParseError(f"期望句号或冒号，但得到 {self._current()}")
        
        # 类体
        attributes = []
        methods = []
        
        # 解析类体（直到遇到"结束"）
        while self._current():
            tok = self._current()
            
            # 结束关键字
            if tok.type == TokenType.KEYWORD and tok.value == '结束':
                self._consume(TokenType.KEYWORD, '结束')
                self._consume(TokenType.DOT)
                break
            
            # 属性声明（支持公有和私有）
            if tok.type == TokenType.KEYWORD and tok.value == '属性':
                attr = self._parse_attribute_declaration()
                attributes.append(attr)
            elif tok.type == TokenType.KEYWORD and tok.value == '私属性':
                attr = self._parse_attribute_declaration()
                attr.is_private = True  # 标记为私有
                attributes.append(attr)
            
            # 构造函数
            elif tok.type == TokenType.KEYWORD and tok.value == '构造':
                method = self._parse_method_definition(is_constructor=True)
                methods.append(method)
            
            # 方法定义（支持公有和私有）
            elif tok.type == TokenType.KEYWORD and tok.value == '段落':
                method = self._parse_method_definition(is_constructor=False)
                methods.append(method)
            elif tok.type == TokenType.KEYWORD and tok.value == '私段落':
                method = self._parse_method_definition(is_constructor=False)
                method.is_private = True  # 标记为私有
                methods.append(method)
            
            # 空行或其他情况
            else:
                # 跳过当前token继续
                if tok.type == TokenType.DOT:
                    self._consume(TokenType.DOT)
                else:
                    break
        
        return ClassDefinition(
            name=class_name,
            attributes=attributes,
            methods=methods,
            base_classes=base_classes
        )
    
    def _parse_attribute_declaration(self) -> AttributeDeclaration:
        """解析属性声明
        
        语法：属性 属性名。
        """
        # 属性
        self._consume(TokenType.KEYWORD, '属性')
        
        # 属性名
        name_tok = self._consume(TokenType.IDENTIFIER)
        attr_name = name_tok.value
        
        # 句号
        self._consume(TokenType.DOT)
        
        return AttributeDeclaration(name=attr_name)
    
    def _parse_method_definition(self, is_constructor=False) -> MethodDefinition:
        """解析方法定义
        
        语法：
        构造 接收 参数名 参数名：
          方法体。
        结束。
        
        或：
        段落 方法名 接收 参数名 参数名：
          方法体。
        结束。
        """
        method_name = None
        
        if is_constructor:
            # 构造
            self._consume(TokenType.KEYWORD, '构造')
            method_name = '__init__'
        else:
            # 段落
            self._consume(TokenType.KEYWORD, '段落')
            # 方法名可能是IDENTIFIER或KEYWORD（如"加""减""乘"）
            name_tok = self._current()
            if name_tok and name_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                method_name = name_tok.value
                self._consume()
            else:
                raise ParseError(f"期望方法名，但得到 {name_tok.type if name_tok else '输入结束'}", name_tok.line if name_tok else 0, name_tok.col if name_tok else 0, name_tok.value if name_tok else None)
        
        # 参数列表（支持"参数"和"接收"两种写法）
        parameters = []
        if self._current() and self._current().type == TokenType.KEYWORD:
            kw = self._current().value
            if kw == '参数' or kw == '接收':
                self._consume(TokenType.KEYWORD)
                
                # 收集参数（支持逗号分隔）
                while self._current():
                    ptok = self._current()
                    if ptok.type == TokenType.IDENTIFIER:
                        self._consume(TokenType.IDENTIFIER)
                        parameters.append(Parameter(name=ptok.value))
                        # 跳过逗号
                        if self._match(TokenType.COMMA):
                            self._consume(TokenType.COMMA)
                    else:
                        break
        
        # 返回类型（可选）：返回 类型
        return_type = None
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '返回':
            self._consume(TokenType.KEYWORD, '返回')
            if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                return_type = self._consume().value
        
        # 句号或冒号
        tok_colon = self._current()
        if tok_colon and tok_colon.type == TokenType.DOT:
            self._consume(TokenType.DOT)
        elif tok_colon and tok_colon.type == TokenType.COLON:
            self._consume(TokenType.COLON)
        else:
            raise ParseError(f"期望句号或冒号，但得到 {tok_colon.type if tok_colon else '输入结束'}", tok_colon.line if tok_colon else 0, tok_colon.col if tok_colon else 0, tok_colon.value if tok_colon else None)
        
        # 方法体
        body = []
        while self._current():
            tok = self._current()
            
            # 结束关键字
            if tok.type == TokenType.KEYWORD and tok.value == '结束':
                self._consume(TokenType.KEYWORD, '结束')
                self._consume(TokenType.DOT)
                break
            
            # 解析语句
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        return MethodDefinition(
            name=method_name,
            parameters=parameters,
            body=body,
            return_type=return_type,
            is_constructor=is_constructor
        )

    def _parse_interface_definition(self) -> InterfaceDefinition:
        """解析接口定义
        
        语法：
        接口 名称：
          段落 方法名 参数 参数名 返回 类型。
          段落 方法名(参数) 返回 类型。
        结束。
        
        或带继承：
        接口 名称 继承 父接口1, 父接口2：
          ...
        结束。
        """
        # 接口
        self._consume(TokenType.KEYWORD, '接口')
        
        # 接口名（可能由多个token组成，与类名类似）
        name_parts = []
        while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            # 检查是否遇到"继承"关键字或冒号/句号
            if self._current().type == TokenType.KEYWORD and self._current().value == '继承':
                break
            if self._current().type in (TokenType.COLON, TokenType.DOT):
                break
            name_parts.append(self._consume().value)
        name = ''.join(name_parts)
        if not name:
            raise ParseError(f"期望接口名，但得到 {self._current().type if self._current() else '输入结束'}")
        
        # 继承（可选）
        super_interfaces = []
        if self._match(TokenType.KEYWORD, '继承'):
            self._consume(TokenType.KEYWORD, '继承')
            while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                # 收集多 token 名称（如"可打印"被拆为"可"+"打印"）
                parts = []
                while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    # 遇到逗号、冒号、句号、结束关键字的token时停止
                    if self._current().type in (TokenType.COLON, TokenType.DOT):
                        break
                    if self._current().type == TokenType.KEYWORD and self._current().value in ('结束',):
                        break
                    parts.append(self._consume().value)
                if parts:
                    super_interfaces.append(''.join(parts))
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                else:
                    break
        
        # 冒号或句号
        if self._match(TokenType.COLON):
            self._consume(TokenType.COLON)
        elif self._match(TokenType.DOT):
            self._consume(TokenType.DOT)
        
        # 接口体
        methods = []
        properties = []
        while self._current():
            tok = self._current()
            
            # 结束
            if tok.type == TokenType.KEYWORD and tok.value == '结束':
                self._consume(TokenType.KEYWORD, '结束')
                if self._current() and self._current().type == TokenType.DOT:
                    self._consume(TokenType.DOT)
                break
            
            # 方法签名：段落 方法名 参数 参数名 返回 类型
            if tok.type == TokenType.KEYWORD and tok.value == '段落':
                sig = self._parse_method_signature()
                methods.append(sig)
            
            # 属性声明：属性 名称（可选类型）
            elif tok.type == TokenType.KEYWORD and tok.value == '属性':
                attr = self._parse_attribute_declaration()
                properties.append(attr)
            
            else:
                # 跳过无法识别的 token
                if tok.type == TokenType.DOT:
                    self._consume(TokenType.DOT)
                else:
                    break
        
        return InterfaceDefinition(name, methods, properties, super_interfaces)
    
    def _parse_method_signature(self) -> MethodSignature:
        """解析接口方法签名
        
        语法：
        段落 方法名 参数 参数名 返回 类型。
        段落 方法名(参数) 返回 类型。
        段落 方法名 返回 类型。
        段落 方法名。
        """
        self._consume(TokenType.KEYWORD, '段落')
        
        # 方法名
        name_tok = self._current()
        if name_tok and name_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            name = self._consume().value
        else:
            raise ParseError(f"期望方法名")
        
        # 参数
        params = []
        
        # 括号参数：(参数1, 参数2, ...)
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            while self._current() and self._current().type != TokenType.RPAREN:
                if self._current().type == TokenType.COMMA:
                    self._consume(TokenType.COMMA)
                    continue
                param_tok = self._current()
                if param_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                    param_name = self._consume().value
                    # 可选类型注解
                    param_type = None
                    if self._match(TokenType.COLON):
                        self._consume(TokenType.COLON)
                        if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                            param_type = self._consume().value
                    params.append(Parameter(param_name, param_type))
                else:
                    break
            self._consume(TokenType.RPAREN)
        
        # 无括号参数：参数 参数名（段落风格）
        elif self._match(TokenType.KEYWORD, '参数'):
            self._consume(TokenType.KEYWORD, '参数')
            while self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                param_name = self._consume().value
                params.append(Parameter(param_name))
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                else:
                    break
        
        # 返回类型（可选）
        return_type = None
        if self._match(TokenType.KEYWORD, '返回'):
            self._consume(TokenType.KEYWORD, '返回')
            if self._current() and self._current().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                return_type = self._consume().value
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return MethodSignature(name, params, return_type)

    def _parse_match_stmt(self) -> MatchStmt:
        """解析模式匹配语句
        
        语法：
        匹配 值：
          情况 模式1：
            语句。
          情况 模式2：
            语句。
          情况 _：
            语句。
        结束。
        """
        # 匹配
        self._consume(TokenType.KEYWORD, '匹配')
        
        # 匹配的值（表达式）
        subject = self._parse_expr()
        
        # 冒号
        if self._match(TokenType.COLON):
            self._consume(TokenType.COLON)
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 解析各个情况
        cases = []
        while self._current():
            tok = self._current()
            
            # 结束关键字
            if tok.type == TokenType.KEYWORD and tok.value == '结束':
                self._consume(TokenType.KEYWORD, '结束')
                if self._current() and self._current().type == TokenType.DOT:
                    self._consume(TokenType.DOT)
                break
            
            # 情况分支
            if tok.type == TokenType.KEYWORD and tok.value == '情况':
                case = self._parse_match_case()
                cases.append(case)
            else:
                # 跳过无法识别的token
                break
        
        return MatchStmt(subject, cases)

    def _parse_with_stmt(self) -> WithStmt:
        """解析上下文管理器：使用 表达式 为 变量：...结束。
        
        语法：
        使用 表达式 为 变量：
            语句。
        结束。
        """
        # 使用
        self._consume(TokenType.KEYWORD, '使用')
        
        # 上下文表达式
        context_expr = self._parse_expr()
        
        # 为 变量（可选）
        variable = None
        if self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
            var_tok = self._current()
            if var_tok and var_tok.type == TokenType.IDENTIFIER:
                variable = self._consume(TokenType.IDENTIFIER).value
            elif var_tok and var_tok.type == TokenType.KEYWORD:
                variable = self._consume(TokenType.KEYWORD).value
            else:
                raise ParseError(f"期望变量名，但得到 {var_tok.type if var_tok else '输入结束'}")

        # 冒号（可选）
        if self._match(TokenType.COLON):
            self._consume(TokenType.COLON)

        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)

        # 体
        body = self._parse_body()

        # 结束
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)

        return WithStmt(context_expr, variable, body)

    def _parse_decorator(self) -> DecoratorDefinition:
        """解析装饰器定义
        
        语法：
        @自定义装饰器 标注 段落 ...
        @静态方法 / @类方法 / @特性（后跟段落或构造定义）
        """
        # @
        self._consume(TokenType.AT)
        
        # 装饰器名
        decorator_name = None
        tok = self._current()
        if tok and tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            decorator_name = self._consume().value
        else:
            raise ParseError(f"期望装饰器名，但得到 {tok.type if tok else '输入结束'}")
        
        # 内置装饰器处理（@静态方法、@类方法、@特性、@抽象）
        if decorator_name in ('静态方法', '类方法', '特性', '抽象'):
            paragraph = None
            if self._match(TokenType.LBOOK):
                paragraph = self._parse_paragraph()
            elif self._match(TokenType.KEYWORD, '段落'):
                paragraph = self._parse_paragraph_v2()
            elif self._match(TokenType.KEYWORD, '构造'):
                paragraph = self._parse_method_definition(is_constructor=True)
            else:
                raise ParseError("装饰器后必须跟段落定义或构造定义")
            return DecoratorDefinition(decorator_name, paragraph)
        
        # 标注（可选关键字）— 仅自定义装饰器
        if self._match(TokenType.KEYWORD, '标注'):
            self._consume(TokenType.KEYWORD, '标注')
        
        # 解析被装饰的段落
        paragraph = None
        if self._match(TokenType.LBOOK):
            # 《段名》段形式
            paragraph = self._parse_paragraph()
        elif self._match(TokenType.KEYWORD, '段落'):
            # 段落 段名 参数形式
            paragraph = self._parse_paragraph_v2()
        else:
            raise ParseError("装饰器后必须跟段落定义（'《段名》段' 或 '段落 段名'）")
        
        return DecoratorDefinition(decorator_name, paragraph)

    def _parse_match_case(self) -> MatchCase:
        """解析匹配分支：情况 模式：语句..."""
        # 情况
        self._consume(TokenType.KEYWORD, '情况')
        
        # 解析模式
        pattern = self._parse_match_pattern()
        
        # 可选的守卫条件：若 条件
        guard = None
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value in ('若', '如果'):
            self._consume(TokenType.KEYWORD)
            guard = self._parse_comparison()
        
        # 冒号
        if self._match(TokenType.COLON):
            self._consume(TokenType.COLON)
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 分支体
        body = []
        while self._current():
            tok = self._current()
            
            # 遇到下一个"情况"或"结束"，停止
            if tok.type == TokenType.KEYWORD and tok.value in ('情况', '结束'):
                break
            
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        return MatchCase(pattern, guard, body)
    
    def _parse_match_pattern(self) -> MatchPattern:
        """解析匹配模式"""
        tok = self._current()
        
        if tok is None:
            return MatchPattern('wildcard')
        
        # 通配符：_（下划线）
        if tok.type == TokenType.IDENTIFIER and tok.value == '_':
            self._consume()
            return MatchPattern('wildcard')
        
        # 数字模式
        if tok.type == TokenType.NUMBER:
            self._consume()
            return MatchPattern('number', value=tok.value)
        
        if tok.type == TokenType.CHINESE_NUM:
            self._consume()
            return MatchPattern('number', value=tok.value)
        
        # 字符串模式
        if tok.type == TokenType.STRING:
            self._consume()
            return MatchPattern('string', value=tok.value)
        
        # 布尔模式
        if tok.type == TokenType.KEYWORD and tok.value == '真':
            self._consume()
            return MatchPattern('bool', value=True)
        if tok.type == TokenType.KEYWORD and tok.value == '假':
            self._consume()
            return MatchPattern('bool', value=False)
        
        # 空模式
        if tok.type == TokenType.KEYWORD and tok.value == '空':
            self._consume()
            return MatchPattern('null')
        
        # 列表模式：[模式1, 模式2, ...]
        if tok.type == TokenType.LBRACKET:
            self._consume(TokenType.LBRACKET)
            elements = []
            while not self._match(TokenType.RBRACKET):
                elem_pattern = self._parse_match_pattern()
                elements.append(elem_pattern)
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
            self._consume(TokenType.RBRACKET)
            return MatchPattern('list', elements=elements)
        
        # 类型检查或变量绑定：标识符
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            self._consume()
            # 检查是否是类型检查模式（标识符后跟另一个标识符，如"整数 甲"表示甲是整数类型）
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.IDENTIFIER and next_tok.value != '_':
                binding = self._consume(TokenType.IDENTIFIER).value
                return MatchPattern('type_check', type_name=name, binding=binding)
            return MatchPattern('variable', binding=name)
        
        # 关键字作为模式
        if tok.type == TokenType.KEYWORD:
            name = tok.value
            self._consume()
            return MatchPattern('variable', binding=name)
        
        return MatchPattern('wildcard')


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言完整语法解析器测试（v3.0）")
    print("=" * 60)
    
    test_cases = [
        # 变量声明
        ('变量声明', '定义甲等于三。'),
        ('变量声明+运算', '定义丙等于三加五。'),
        
        # 条件语句
        ('条件语句', '''如果甲大于十那么：
  打印甲。
结束。'''),
        
        # 遍历循环
        ('遍历循环', '''遍历项在列表：
  打印项。
结束。'''),
        
        # 段落定义
        ('段落定义', '''《计算》段(甲: 数, 乙: 数) -> 数：
  返回甲加乙。
结束。'''),
        
        # 管道操作
        ('管道操作', '数据 -> 过滤 -> 排序。'),
    ]
    
    parser = DuanParser()
    
    passed = 0
    failed = 0
    
    for name, test_code in test_cases:
        print(f"\n--- 测试: {name} ---")
        print(f"代码: {test_code[:50]}...")
        
        try:
            result = parser.parse(test_code)
            print(f"[OK] 解析成功")
            print(f"  类型: {type(result).__name__}")
            print(f"  语句数: {len(result.statements)}")
            for i, stmt in enumerate(result.statements):
                print(f"  语句{i+1}: {type(stmt).__name__}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 解析失败")
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
