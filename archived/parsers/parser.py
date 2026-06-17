"""
段言（Duan）编程语言语法解析器

核心特性：
- 缩进定义块（决策33）
- 元数驱动解析（决策28）
- 管道操作符（决策30）
- 主谓/谓宾语义区分（决策34）
"""

from typing import List, Optional, Union
from .tokens import Token, TokenType
from .ast_nodes import (
    ASTNode, NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Identifier, SegmentName, ModuleName, BinaryOp, UnaryOp, FunctionCall,
    PipeExpression, PropertyAccess, IndexAccess, MethodCall,
    VariableDeclaration, Assignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    ExpressionStatement, Parameter, SegmentDefinition, ImportStatement,
    ExportStatement, Module, TypeDefinition, TypeAnnotation
)
from .keywords import VERB_ARITY, get_arity


class ParseError(Exception):
    """语法解析错误"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"行 {token.line}, 列 {token.column}: {message}")


class Parser:
    """段言语法解析器"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.indent_level = 0
    
    def parse(self) -> Module:
        """解析为 AST"""
        imports = []
        exports = []
        segments = []
        statements = []
        module_name = None
        
        # 解析模块名（可选）
        if self.check(TokenType.MODULE_NAME):
            module_name = self.parse_module_name().name
        
        # 解析导入/导出/段落/语句
        while not self.is_at_end():
            if self.check(TokenType.KEYWORD_IMPORT):
                imports.append(self.parse_import())
            elif self.check(TokenType.KEYWORD_EXPORT):
                exports.append(self.parse_export())
            elif self.check(TokenType.SEGMENT_NAME):
                segments.append(self.parse_segment_definition())
            elif self.check(TokenType.KEYWORD_DEFINE):
                statements.append(self.parse_variable_declaration())
            elif self.check(TokenType.KEYWORD_TYPE):
                segments.append(self.parse_type_definition())
            elif self.check(TokenType.NEWLINE):
                self.advance()
            else:
                # 尝试解析语句
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return Module(
            line=1,
            column=1,
            name=module_name,
            imports=imports,
            exports=exports,
            segments=segments,
            statements=statements
        )
    
    def current_token(self) -> Token:
        """获取当前 Token"""
        if self.is_at_end():
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 0) -> Token:
        """查看指定位置的 Token"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def is_at_end(self) -> bool:
        """是否到达末尾"""
        return self.current_token().type == TokenType.EOF
    
    def check(self, *types: TokenType) -> bool:
        """检查当前 Token 类型"""
        return self.current_token().type in types
    
    def match(self, *types: TokenType) -> Optional[Token]:
        """匹配并消耗 Token"""
        if self.check(*types):
            return self.advance()
        return None
    
    def advance(self) -> Token:
        """前进一个 Token"""
        token = self.current_token()
        if not self.is_at_end():
            self.pos += 1
        return token
    
    def expect(self, type: TokenType, message: str) -> Token:
        """期望特定类型的 Token"""
        if self.check(type):
            return self.advance()
        raise ParseError(message, self.current_token())
    
    def skip_newlines(self):
        """跳过换行"""
        while self.match(TokenType.NEWLINE):
            pass
    
    def parse_module_name(self) -> ModuleName:
        """解析模块名"""
        token = self.expect(TokenType.MODULE_NAME, "期望模块名")
        return ModuleName(line=token.line, column=token.column, name=token.value)
    
    def parse_import(self) -> ImportStatement:
        """解析导入语句"""
        token = self.advance()  # 消耗 '导入'
        
        # 解析导入的名称列表
        names = []
        
        # 可能是 '从 模块 导入 名称'
        if self.check(TokenType.KEYWORD_FROM):
            self.advance()  # 消耗 '从'
            module = self.expect(TokenType.IDENTIFIER, "期望模块名").value
            self.expect(TokenType.KEYWORD_IMPORT, "期望 '导入'")
            
            if self.check(TokenType.SEGMENT_NAME):
                names.append(self.expect(TokenType.SEGMENT_NAME, "期望段落名").value)
                while self.match(TokenType.COMMA):
                    names.append(self.expect(TokenType.SEGMENT_NAME, "期望段落名").value)
            
            return ImportStatement(line=token.line, column=token.column, module=module, names=names)
        
        # 直接导入
        if self.check(TokenType.SEGMENT_NAME):
            names.append(self.expect(TokenType.SEGMENT_NAME, "期望段落名").value)
            while self.match(TokenType.COMMA):
                names.append(self.expect(TokenType.SEGMENT_NAME, "期望段落名").value)
        
        module = ''
        return ImportStatement(line=token.line, column=token.column, module=module, names=names)
    
    def parse_export(self) -> ExportStatement:
        """解析导出语句"""
        token = self.advance()  # 消耗 '导出'
        name = self.expect(TokenType.SEGMENT_NAME, "期望段落名").value
        return ExportStatement(line=token.line, column=token.column, name=name)
    
    def parse_segment_definition(self) -> SegmentDefinition:
        """解析段落定义"""
        name_token = self.expect(TokenType.SEGMENT_NAME, "期望段落名")
        self.expect(TokenType.KEYWORD_SEGMENT, "期望 '段'")
        
        # 解析参数列表
        parameters = []
        if self.match(TokenType.LPAREN):
            if not self.check(TokenType.RPAREN):
                parameters.append(self.parse_parameter())
                while self.match(TokenType.COMMA):
                    parameters.append(self.parse_parameter())
            self.expect(TokenType.RPAREN, "期望 ')'")
        
        # 解析返回类型（可选）
        return_type = None
        if self.match(TokenType.ARROW):
            return_type = self.parse_type_annotation()
        
        # 解析冒号或缩进
        if self.match(TokenType.COLON):
            pass
        else:
            self.skip_newlines()
            if self.match(TokenType.INDENT):
                pass
        
        # 解析段落体
        body = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            
            # 检查是否到达段落结束
            if self.check(TokenType.KEYWORD_RETURN):
                body.append(self.parse_return_statement())
                continue
            
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        # 消耗 DEDENT 或显式结束
        if self.check(TokenType.DEDENT):
            self.advance()
        
        return SegmentDefinition(
            line=name_token.line,
            column=name_token.column,
            name=name_token.value,
            parameters=parameters,
            body=body,
            return_type=return_type
        )
    
    def parse_parameter(self) -> Parameter:
        """解析参数定义"""
        name_token = self.expect(TokenType.IDENTIFIER, "期望参数名")
        
        # 类型注解（可选）
        type_annotation = None
        if self.match(TokenType.COLON):
            type_annotation = self.parse_type_annotation()
        
        # 默认值（可选）
        default_value = None
        if self.match(TokenType.KEYWORD_EQUAL):
            default_value = self.parse_expression()
        
        return Parameter(
            line=name_token.line,
            column=name_token.column,
            name=name_token.value,
            type_annotation=type_annotation,
            default_value=default_value
        )
    
    def parse_type_annotation(self) -> str:
        """解析类型注解"""
        tokens = []
        
        # 收集类型 Token
        if self.check(TokenType.TYPE_NUMBER, TokenType.TYPE_INT, TokenType.TYPE_FLOAT,
                      TokenType.TYPE_STRING, TokenType.TYPE_LIST, TokenType.TYPE_DICT,
                      TokenType.TYPE_SET, TokenType.TYPE_BOOL, TokenType.TYPE_NULL,
                      TokenType.TYPE_ANY):
            tokens.append(self.advance().value)
        elif self.check(TokenType.IDENTIFIER):
            tokens.append(self.advance().value)
        
        # 泛型参数（可选）
        if self.match(TokenType.LBRACKET):
            tokens.append('[')
            tokens.append(self.parse_type_annotation())
            while self.match(TokenType.COMMA):
                tokens.append(',')
                tokens.append(self.parse_type_annotation())
            self.expect(TokenType.RBRACKET, "期望 ']'")
            tokens.append(']')
        
        return ''.join(tokens)
    
    def parse_type_definition(self) -> TypeDefinition:
        """解析类型定义"""
        token = self.advance()  # 消耗 '类型'
        name = self.expect(TokenType.IDENTIFIER, "期望类型名").value
        
        fields = []
        if self.match(TokenType.COLON):
            # 缩进块
            self.skip_newlines()
            if self.match(TokenType.INDENT):
                while not self.check(TokenType.DEDENT) and not self.is_at_end():
                    if self.check(TokenType.NEWLINE):
                        self.advance()
                        continue
                    
                    field_name = self.expect(TokenType.IDENTIFIER, "期望字段名").value
                    self.expect(TokenType.COLON, "期望 ':'")
                    field_type = self.parse_type_annotation()
                    fields.append((field_name, field_type))
                
                self.expect(TokenType.DEDENT, "期望取消缩进")
        
        return TypeDefinition(
            line=token.line,
            column=token.column,
            name=name,
            fields=fields
        )
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """解析变量声明"""
        token = self.advance()  # 消耗 '定义'
        name = self.expect(TokenType.IDENTIFIER, "期望变量名").value
        self.expect(TokenType.KEYWORD_EQUAL, "期望 '等于'")
        value = self.parse_expression()
        
        return VariableDeclaration(
            line=token.line,
            column=token.column,
            name=name,
            value=value
        )
    
    def parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        self.skip_newlines()
        
        if self.check(TokenType.KEYWORD_DEFINE):
            return self.parse_variable_declaration()
        
        if self.check(TokenType.KEYWORD_IF):
            return self.parse_if_statement()
        
        if self.check(TokenType.KEYWORD_FOREACH):
            return self.parse_foreach_statement()
        
        if self.check(TokenType.KEYWORD_WHILE):
            return self.parse_while_statement()
        
        if self.check(TokenType.KEYWORD_BREAK):
            token = self.advance()
            return BreakStatement(line=token.line, column=token.column)
        
        if self.check(TokenType.KEYWORD_CONTINUE):
            token = self.advance()
            return ContinueStatement(line=token.line, column=token.column)
        
        if self.check(TokenType.KEYWORD_RETURN):
            return self.parse_return_statement()
        
        # 表达式语句
        expr = self.parse_expression()
        if expr:
            return ExpressionStatement(line=expr.line, column=expr.column, expression=expr)
        
        return None
    
    def parse_if_statement(self) -> IfStatement:
        """解析条件语句"""
        token = self.advance()  # 消耗 '如果'
        condition = self.parse_expression()
        self.expect(TokenType.KEYWORD_THEN, "期望 '那么'")
        
        # 冒号或缩进
        if self.match(TokenType.COLON):
            pass
        
        # then 体
        then_body = []
        self.skip_newlines()
        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT) and not self.check(TokenType.KEYWORD_ELSE, TokenType.KEYWORD_ELSEIF):
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.parse_statement()
                if stmt:
                    then_body.append(stmt)
        
        # else 体
        else_body = None
        if self.match(TokenType.KEYWORD_ELSE):
            if self.match(TokenType.COLON):
                pass
            self.skip_newlines()
            if self.match(TokenType.INDENT):
                else_body = []
                while not self.check(TokenType.DEDENT):
                    if self.check(TokenType.NEWLINE):
                        self.advance()
                        continue
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
        
        return IfStatement(
            line=token.line,
            column=token.column,
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
    
    def parse_foreach_statement(self) -> ForeachStatement:
        """解析遍历循环"""
        token = self.advance()  # 消耗 '遍历'
        
        variable = self.expect(TokenType.IDENTIFIER, "期望变量名").value
        
        # '在' 可选
        # self.match(TokenType.IDENTIFIER)  # 消耗 '在' 如果有
        
        iterable = self.parse_expression()
        
        if self.match(TokenType.COLON):
            pass
        
        # 循环体
        body = []
        self.skip_newlines()
        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT):
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
        
        return ForeachStatement(
            line=token.line,
            column=token.column,
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def parse_while_statement(self) -> WhileStatement:
        """解析当循环"""
        token = self.advance()  # 消耗 '当'
        condition = self.parse_expression()
        
        if self.match(TokenType.COLON):
            pass
        
        # 循环体
        body = []
        self.skip_newlines()
        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT):
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
        
        return WhileStatement(
            line=token.line,
            column=token.column,
            condition=condition,
            body=body
        )
    
    def parse_return_statement(self) -> ReturnStatement:
        """解析返回语句"""
        token = self.advance()  # 消耗 '返回'
        
        value = None
        if not self.check(TokenType.DOT, TokenType.NEWLINE, TokenType.DEDENT):
            value = self.parse_expression()
        
        return ReturnStatement(
            line=token.line,
            column=token.column,
            value=value
        )
    
    def parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self.parse_pipe_expression()
    
    def parse_pipe_expression(self) -> ASTNode:
        """解析管道表达式"""
        left = self.parse_comparison()
        
        # 管道操作符：-> 或 并
        while self.check(TokenType.ARROW, TokenType.AND_WORD, TokenType.COMMA):
            op = self.advance()
            right = self.parse_comparison()
            left = PipeExpression(
                line=left.line,
                column=left.column,
                expressions=[left, right]
            )
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """解析比较表达式"""
        left = self.parse_additive()
        
        while self.check(TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(
                line=left.line,
                column=left.column,
                left=left,
                operator=op,
                right=right
            )
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """解析加减表达式"""
        left = self.parse_multiplicative()
        
        while self.check(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(
                line=left.line,
                column=left.column,
                left=left,
                operator=op,
                right=right
            )
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """解析乘除表达式"""
        left = self.parse_unary()
        
        while self.check(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(
                line=left.line,
                column=left.column,
                left=left,
                operator=op,
                right=right
            )
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """解析一元表达式"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.current_token()
            operand = self.parse_unary()
            return UnaryOp(
                line=op.line,
                column=op.column,
                operator=op.value,
                operand=operand
            )
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """解析后缀表达式（函数调用、属性访问等）"""
        expr = self.parse_primary()
        
        while True:
            # 函数调用
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN, "期望 ')'")
                
                if isinstance(expr, SegmentName):
                    expr = FunctionCall(
                        line=expr.line,
                        column=expr.column,
                        name=expr,
                        arguments=args
                    )
                elif isinstance(expr, Identifier):
                    expr = FunctionCall(
                        line=expr.line,
                        column=expr.column,
                        name=expr,
                        arguments=args
                    )
            
            # 属性访问（之字结构）
            elif self.match(TokenType.OF):
                prop = self.expect(TokenType.IDENTIFIER, "期望属性名").value
                expr = PropertyAccess(
                    line=expr.line,
                    column=expr.column,
                    obj=expr,
                    property_name=prop
                )
            
            # 索引访问
            elif self.match(TokenType.LBRACKET):
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "期望 ']'")
                expr = IndexAccess(
                    line=expr.line,
                    column=expr.column,
                    obj=expr,
                    index=index
                )
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        token = self.current_token()
        
        # 数字
        if self.match(TokenType.NUMBER):
            value = token.value
            if '.' in value:
                return NumberLiteral(line=token.line, column=token.column, value=float(value))
            else:
                return NumberLiteral(line=token.line, column=token.column, value=int(value))
        
        # 字符串
        if self.match(TokenType.STRING):
            return StringLiteral(line=token.line, column=token.column, value=token.value)
        
        # 布尔值
        if self.match(TokenType.TRUE):
            return BooleanLiteral(line=token.line, column=token.column, value=True)
        
        if self.match(TokenType.FALSE):
            return BooleanLiteral(line=token.line, column=token.column, value=False)
        
        # 空值
        if self.match(TokenType.NULL):
            return NullLiteral(line=token.line, column=token.column)
        
        # 段落名
        if self.match(TokenType.SEGMENT_NAME):
            return SegmentName(line=token.line, column=token.column, name=token.value)
        
        # 标识符
        if self.match(TokenType.IDENTIFIER):
            return Identifier(line=token.line, column=token.column, name=token.value)
        
        # 括号表达式
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "期望 ')'")
            return expr
        
        # 列表字面量
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET, "期望 ']'")
            # 返回一个函数调用 '列'
            return FunctionCall(
                line=token.line,
                column=token.column,
                name=Identifier(line=token.line, column=token.column, name='列'),
                arguments=elements
            )
        
        raise ParseError(f"未预期的 Token: {token.type}", token)


def parse(tokens: List[Token]) -> Module:
    """将 Token 列表解析为 AST"""
    parser = Parser(tokens)
    return parser.parse()
