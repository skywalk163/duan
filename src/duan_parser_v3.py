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
# AST 节点定义
# =============================================================================

class ASTNode:
    """AST 节点基类"""
    pass


class Module(ASTNode):
    """模块"""
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
    
    def __repr__(self):
        return f"Module({len(self.statements)} statements)"


class VarDecl(ASTNode):
    """变量声明"""
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"VarDecl({self.name} = {self.value})"


class IfStmt(ASTNode):
    """条件语句"""
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"IfStmt({self.condition})"


class ForeachStmt(ASTNode):
    """遍历循环"""
    def __init__(self, variable: str, iterable: ASTNode, body: List[ASTNode]):
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForeachStmt({self.variable} in {self.iterable})"


class WhileStmt(ASTNode):
    """当循环"""
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStmt({self.condition})"


class Paragraph(ASTNode):
    """段落定义"""
    def __init__(self, name: str, params: List[Dict[str, str]], return_type: Optional[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
    
    def __repr__(self):
        return f"Paragraph({self.name})"


class ReturnStmt(ASTNode):
    """返回语句"""
    def __init__(self, value: Optional[ASTNode]):
        self.value = value
    
    def __repr__(self):
        return f"ReturnStmt({self.value})"


class BinaryOp(ASTNode):
    """二元运算"""
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


class NumberLiteral(ASTNode):
    """数字字面量"""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"


class StringLiteral(ASTNode):
    """字符串字面量"""
    def __init__(self, value: str):
        self.value = value
    
    def __repr__(self):
        return f'"{self.value}"'


class Identifier(ASTNode):
    """标识符"""
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name


class ParagraphCall(ASTNode):
    """段落调用"""
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"《{self.name}》({', '.join(map(str, self.args))})"


class IndexAccess(ASTNode):
    """索引访问（字符串/列表索引）"""
    def __init__(self, obj: ASTNode, index: ASTNode):
        self.obj = obj
        self.index = index
    
    def __repr__(self):
        return f"{self.obj}[{self.index}]"


class BreakStmt(ASTNode):
    """跳出语句"""
    def __repr__(self):
        return "跳出"


class ContinueStmt(ASTNode):
    """跳过语句"""
    def __repr__(self):
        return "跳过"


class Pipeline(ASTNode):
    """管道操作"""
    def __init__(self, stages: List[ASTNode]):
        self.stages = stages
    
    def __repr__(self):
        return ' -> '.join(map(str, self.stages))


class ImportStmt(ASTNode):
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
    """导出语句"""
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
    
    def __repr__(self):
        return f"ExportStmt({', '.join(self.symbols)})"


class Parameter(ASTNode):
    """参数定义"""
    def __init__(self, name: str, type_annotation: str = None, default_value: ASTNode = None):
        self.name = name
        self.type_annotation = type_annotation
        self.default_value = default_value
    
    def __repr__(self):
        return f"Parameter({self.name})"


class AttributeDeclaration(ASTNode):
    """属性声明"""
    def __init__(self, name: str, type_annotation: str = None, default_value: ASTNode = None):
        self.name = name
        self.type_annotation = type_annotation
        self.default_value = default_value
    
    def __repr__(self):
        return f"AttributeDeclaration({self.name})"


class MethodDefinition(ASTNode):
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
    """self赋值语句：己属性名 为 值"""
    def __init__(self, attr_name: str, value: ASTNode):
        self.attr_name = attr_name
        self.value = value
    
    def __repr__(self):
        return f"SelfAssignment(self.{self.attr_name})"


class ClassDefinition(ASTNode):
    """类定义"""
    def __init__(self, name: str, attributes: List[AttributeDeclaration], 
                 methods: List[MethodDefinition], base_class: str = None):
        self.name = name
        self.attributes = attributes
        self.methods = methods
        self.base_class = base_class
    
    def __repr__(self):
        return f"ClassDefinition({self.name})"


class ClassInstantiation(ASTNode):
    """类实例化（新建 类名 参数...）"""
    def __init__(self, class_name: str, args: List[ASTNode]):
        self.class_name = class_name
        self.args = args
    
    def __repr__(self):
        return f"ClassInstantiation({self.class_name})"


class MemberAccess(ASTNode):
    """成员访问（对象.属性 或 对象.方法()）"""
    def __init__(self, obj: ASTNode, member: str, is_method_call: bool = False, args: List[ASTNode] = None):
        self.obj = obj
        self.member = member
        self.is_method_call = is_method_call
        self.args = args or []
    
    def __repr__(self):
        return f"MemberAccess({self.obj}.{self.member})"


# =============================================================================
# 递归下降解析器
# =============================================================================

class DuanParser:
    """段言完整语法解析器"""
    
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
            raise SyntaxError(f"意外的输入结束")
        
        if expected_type and tok.type != expected_type:
            raise SyntaxError(f"期望 {expected_type}，得到 {tok.type} (位置: L{tok.line}:C{tok.col})")
        
        if expected_value and tok.value != expected_value:
            raise SyntaxError(f"期望 '{expected_value}'，得到 '{tok.value}' (位置: L{tok.line}:C{tok.col})")
        
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
        
        # 段落定义：《段名》段 或 "段落 段名 参数 参数名"
        if tok.type == TokenType.LBOOK:
            return self._parse_paragraph()
        
        # 段落定义：段落 段名 参数 参数名
        if tok.type == TokenType.KEYWORD and tok.value == '段落':
            return self._parse_paragraph_v2()
        
        # 类定义：类 类名
        if tok.type == TokenType.KEYWORD and tok.value == '类':
            return self._parse_class_definition()

        # 动词调用作为独立语句
        if tok.type == TokenType.KEYWORD and tok.value in VERB_ARITY:
            return self._parse_expr_stmt()
        
        # self赋值语句：己属性名 为 值
        if tok.type == TokenType.KEYWORD and tok.value == '己':
            return self._parse_self_assignment()
        
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
        if self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
        elif self._match(TokenType.KEYWORD, '等于'):
            self._consume(TokenType.KEYWORD, '等于')
        else:
            # 兼容其他赋值操作符
            raise SyntaxError(f"期望'为'或'等于'，但得到: {self._current()}")
        
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
        """解析导入语句：导入《模块名》。 或 导入《模块名》为别名。"""
        # 导入
        self._consume(TokenType.KEYWORD, '导入')
        
        # 《模块名》
        self._consume(TokenType.LBOOK)
        name_tok = self._consume(TokenType.IDENTIFIER)
        module_name = name_tok.value
        self._consume(TokenType.RBOOK)
        
        # 检查是否有别名：为
        alias = None
        if self._match(TokenType.KEYWORD, '为'):
            self._consume(TokenType.KEYWORD, '为')
            alias_tok = self._consume(TokenType.IDENTIFIER)
            alias = alias_tok.value
        
        # 句号
        self._consume(TokenType.DOT)
        
        return ImportStmt(module_name, symbols=None, alias=alias)
    
    def _parse_from_import_stmt(self) -> ImportStmt:
        """解析从...导入语句：从《模块名》导入《符号1》，《符号2》。"""
        # 从
        self._consume(TokenType.KEYWORD, '从')
        
        # 《模块名》
        self._consume(TokenType.LBOOK)
        name_tok = self._consume(TokenType.IDENTIFIER)
        module_name = name_tok.value
        self._consume(TokenType.RBOOK)
        
        # 导入
        self._consume(TokenType.KEYWORD, '导入')
        
        # 《符号1》，《符号2》，...
        symbols = []
        while True:
            self._consume(TokenType.LBOOK)
            symbol_tok = self._consume(TokenType.IDENTIFIER)
            symbols.append(symbol_tok.value)
            self._consume(TokenType.RBOOK)
            
            # 检查是否有逗号（继续导入）
            if self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                continue
            
            # 检查是否有别名：为
            if self._match(TokenType.KEYWORD, '为'):
                # 目前只支持单个别名，简化处理
                # TODO: 支持每个符号单独别名
                break
            
            break
        
        # 句号
        self._consume(TokenType.DOT)
        
        return ImportStmt(module_name, symbols=symbols)
    
    def _parse_set_stmt(self) -> VarDecl:
        """解析变量声明：设 变量名 为 值。"""
        # 设
        self._consume(TokenType.KEYWORD, '设')
        
        # 变量名
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 为
        self._consume(TokenType.KEYWORD, '为')
        
        # 值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return VarDecl(name, value)
    
    def _parse_export_stmt(self) -> ExportStmt:
        """解析导出语句：导出《符号1》，《符号2》。"""
        # 导出
        self._consume(TokenType.KEYWORD, '导出')
        
        # 检查是否是"全部"
        if self._match(TokenType.IDENTIFIER, '全部'):
            self._consume(TokenType.IDENTIFIER, '全部')
            self._consume(TokenType.DOT)
            return ExportStmt(['*'])  # 特殊标记：导出全部
        
        # 《符号1》，《符号2》，...
        symbols = []
        while True:
            self._consume(TokenType.LBOOK)
            symbol_tok = self._consume(TokenType.IDENTIFIER)
            symbols.append(symbol_tok.value)
            self._consume(TokenType.RBOOK)
            
            # 检查是否有逗号（继续导出）
            if self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                continue
            
            break
        
        # 句号
        self._consume(TokenType.DOT)
        
        return ExportStmt(symbols)
    
    def _parse_var_decl(self) -> VarDecl:
        """解析变量声明"""
        # 定义
        self._consume(TokenType.KEYWORD, '定义')

        # 标识符（允许 KEYWORD 作为变量名）
        name_tok = self._current()
        if name_tok is None:
            raise SyntaxError("期望标识符，但到达输入结束")

        # 允许 KEYWORD 或 IDENTIFIER 作为变量名
        if name_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._consume()
            name = name_tok.value
        else:
            raise SyntaxError(f"期望标识符，得到 {name_tok.type} (位置: L{name_tok.line}:C{name_tok.col})")

        # 等于
        self._consume(TokenType.KEYWORD, '等于')

        # 表达式
        value = self._parse_expr()

        # 句号
        self._consume(TokenType.DOT)

        return VarDecl(name, value)
    
    def _parse_if_stmt(self) -> IfStmt:
        """解析条件语句"""
        # 如果
        self._consume(TokenType.KEYWORD, '如果')
        
        # 条件
        condition = self._parse_expr()
        
        # 那么
        self._consume(TokenType.KEYWORD, '那么')
        
        # 冒号（可选）
        has_colon = self._match(TokenType.COLON)
        if has_colon:
            self._consume(TokenType.COLON)
        
        # 缩进块或单行语句
        then_body = self._parse_body()
        
        # 否则？
        else_body = None
        if self._match(TokenType.KEYWORD, '否则'):
            self._consume(TokenType.KEYWORD, '否则')
            
            # 冒号（可选）
            if self._match(TokenType.COLON):
                self._consume(TokenType.COLON)
            
            else_body = self._parse_body()
        
        return IfStmt(condition, then_body, else_body)
    
    def _parse_foreach_stmt(self) -> ForeachStmt:
        """解析遍历循环"""
        # 遍历
        self._consume(TokenType.KEYWORD, '遍历')
        
        # 变量名
        var_tok = self._consume(TokenType.IDENTIFIER)
        variable = var_tok.value
        
        # 在
        self._consume(TokenType.KEYWORD, '在')
        
        # 可迭代对象
        iterable = self._parse_expr()
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # 循环体
        body = self._parse_body()
        
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
                else:
                    raise SyntaxError(f"期望参数名，得到 {tok.type if tok else 'EOF'} (位置: L{tok.line if tok else '?'}:C{tok.col if tok else '?'})")
                
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
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # 段落体
        body = self._parse_body()
        
        return Paragraph(name, params, return_type, body)
    
    def _parse_paragraph_v2(self) -> Paragraph:
        """解析段落定义：段落 段名 参数 参数名。"""
        # 段落
        self._consume(TokenType.KEYWORD, '段落')
        
        # 段名
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 参数列表（可选）
        params = []
        if self._match(TokenType.KEYWORD, '参数'):
            self._consume(TokenType.KEYWORD, '参数')
            
            # 收集参数名，直到句号
            while self._current() and self._current().type != TokenType.DOT:
                tok = self._current()
                if tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                    params.append({'name': param_name, 'type': None})
                elif tok.type == TokenType.KEYWORD:
                    # 参数名可能是关键字
                    param_name = self._consume(TokenType.KEYWORD).value
                    params.append({'name': param_name, 'type': None})
                else:
                    break
        
        # 句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 段落体
        body = self._parse_body()
        
        return Paragraph(name, params, None, body)
    
    def _parse_body(self) -> List[ASTNode]:
        """解析代码块（简化版：不处理缩进）"""
        statements = []

        # 简化处理：最多解析100条语句
        max_statements = 100
        count = 0

        while self._current() and count < max_statements:
            tok = self._current()

            # 结束标记
            if tok.type == TokenType.KEYWORD and tok.value in ('否则', '结束'):
                # 消耗"结束"关键字
                if tok.value == '结束':
                    self._consume(TokenType.KEYWORD, '结束')
                    if self._current() and self._current().type == TokenType.DOT:
                        self._consume(TokenType.DOT)
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
        """解析表达式（支持管道操作符）"""
        left = self._parse_comparison()
        
        # 管道操作符
        stages = [left]
        
        while self._match(TokenType.ARROW) or self._match(TokenType.COMMA):
            if self._match(TokenType.ARROW):
                self._consume(TokenType.ARROW)
            else:
                self._consume(TokenType.COMMA)
            
            right = self._parse_comparison()
            stages.append(right)
        
        if len(stages) > 1:
            return Pipeline(stages)
        
        return left
    
    def _parse_comparison(self) -> ASTNode:
        """解析比较表达式"""
        left = self._parse_add_expr()
        
        while self._current():
            tok = self._current()
            # 遇到"那么"关键字，停止解析
            if tok.type == TokenType.KEYWORD and tok.value == '那么':
                break
            if tok.type == TokenType.KEYWORD and tok.value in ('大于', '小于', '等于', '不等于', '大于等于', '小于等于'):
                op = self._consume().value
                
                op_map = {
                    '大于': '>',
                    '小于': '<',
                    '等于': '==',
                    '不等于': '!=',
                    '大于等于': '>=',
                    '小于等于': '<=',
                }
                
                right = self._parse_add_expr()
                left = BinaryOp(op_map.get(op, op), left, right)
            else:
                break
        
        return left
    
    def _parse_add_expr(self) -> ASTNode:
        """解析加减表达式"""
        left = self._parse_mul_expr()
        
        while self._current():
            tok = self._current()
            # 支持：加、减、加上、减去
            if tok.type == TokenType.KEYWORD and tok.value in ('加', '减', '加上', '减去'):
                op = self._consume().value
                
                op_map = {'加': '+', '减': '-', '加上': '+', '减去': '-'}
                right = self._parse_mul_expr()
                left = BinaryOp(op_map.get(op, op), left, right)
            else:
                break
        
        return left
    
    def _parse_mul_expr(self) -> ASTNode:
        """解析乘除表达式"""
        left = self._parse_primary()
        
        while self._current():
            tok = self._current()
            # 支持：乘、除、乘以、除以
            if tok.type == TokenType.KEYWORD and tok.value in ('乘', '除', '乘以', '除以'):
                op = self._consume().value
                
                op_map = {'乘': '*', '除': '/', '乘以': '*', '除以': '/'}
                # 重要：右侧应该解析为完整的加减表达式，而非仅primary
                # 这样'数 乘以 计算阶乘 数 减一'会被正确解析为：数 * 计算阶乘(数 - 1)
                right = self._parse_add_expr()
                left = BinaryOp(op_map.get(op, op), left, right)
            else:
                # 遇到加减运算符或其他，返回让上层处理
                break
        
        return left
    
    def _parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        tok = self._current()
        
        if tok is None:
            raise SyntaxError(f"意外的输入结束")
        
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
            expr = NumberLiteral(tok.value)
            return self._parse_postfix(expr)

        # 字符串
        if tok.type == TokenType.STRING:
            self._consume()
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
        operator_verbs = {'加', '减', '乘', '除', '加上', '减去', '乘以', '除以', '大于', '小于', '等于', '不等于', '大于等于', '小于等于'}
        
        if tok.type == TokenType.KEYWORD and tok.value in VERB_ARITY and tok.value not in operator_verbs:
            verb_name = tok.value
            self._consume()
            
            # 特殊处理：新建（类实例化）
            if verb_name == '新建':
                # 新建 类名 参数...
                class_name_tok = self._current()
                if class_name_tok and class_name_tok.type == TokenType.IDENTIFIER:
                    class_name = class_name_tok.value
                    self._consume()
                    
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
                    # 收集单个primary参数（不进行段落调用检测）
                    arg = self._collect_primary_arg()
                    if arg:
                        args.append(arg)
                    else:
                        break
            else:
                # 固定参数数量
                for _ in range(arity):
                    if self._current() and self._current().type not in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN):
                        arg = self._collect_primary_arg()
                        if arg:
                            args.append(arg)

            expr = ParagraphCall(verb_name, args)
            return self._parse_postfix(expr)

        # 标识符：可能带参数（段落调用）
        if tok.type == TokenType.IDENTIFIER:
            return self._collect_single_arg()

        raise SyntaxError(f"意外的 Token: {tok.type} = {tok.value}")

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

        # 标识符（直接返回，不进行段落调用检测）
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            self._consume()
            expr = Identifier(name)
            return self._parse_postfix(expr)

        # 关键字作为标识符
        if tok.type == TokenType.KEYWORD:
            name = tok.value
            self._consume()
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
            operator_verbs = {'加', '减', '乘', '除', '加上', '减去', '乘以', '除以', '大于', '小于', '等于', '不等于', '大于等于', '小于等于'}
            
            # 检查下一个token是否是运算符动词
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value in operator_verbs:
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
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in operator_verbs:
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
            operator_verbs = {'加', '减', '乘', '除', '加上', '减去', '乘以', '除以', '大于', '小于', '等于', '不等于', '大于等于', '小于等于'}
            
            # 检查下一个token是否是运算符动词
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value in operator_verbs:
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
                    if next_tok.type == TokenType.KEYWORD and next_tok.value in operator_verbs:
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
    
    def _parse_postfix(self, expr: ASTNode) -> ASTNode:
        """解析后缀表达式（索引访问、成员访问等）"""
        while self._current():
            tok = self._current()
            
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
                    
                    is_method_call = len(args) > 0
                    expr = MemberAccess(expr, member_name, is_method_call, args)
                    continue
                else:
                    raise SyntaxError(f"期望成员名，但得到: {member_tok}")
            
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
        
        # 类名
        name_tok = self._consume(TokenType.IDENTIFIER)
        class_name = name_tok.value
        
        # 继承？（可选）
        base_class = None
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '继承':
            self._consume(TokenType.KEYWORD, '继承')
            base_tok = self._consume(TokenType.IDENTIFIER)
            base_class = base_tok.value
        
        # 句号
        self._consume(TokenType.DOT)
        
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
            
            # 属性声明
            if tok.type == TokenType.KEYWORD and tok.value == '属性':
                attr = self._parse_attribute_declaration()
                attributes.append(attr)
            
            # 构造函数
            elif tok.type == TokenType.KEYWORD and tok.value == '构造':
                method = self._parse_method_definition(is_constructor=True)
                methods.append(method)
            
            # 方法定义
            elif tok.type == TokenType.KEYWORD and tok.value == '段落':
                method = self._parse_method_definition(is_constructor=False)
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
            base_class=base_class
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
        构造 参数 参数名 参数名。
          方法体。
        结束。
        
        或：
        段落 方法名 参数 参数名。
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
            name_tok = self._consume(TokenType.IDENTIFIER)
            method_name = name_tok.value
        
        # 参数列表
        parameters = []
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '参数':
            self._consume(TokenType.KEYWORD, '参数')
            
            # 收集参数
            while self._current() and self._current().type == TokenType.IDENTIFIER:
                param_tok = self._consume(TokenType.IDENTIFIER)
                parameters.append(Parameter(name=param_tok.value))
        
        # 句号
        self._consume(TokenType.DOT)
        
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
            is_constructor=is_constructor
        )


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
