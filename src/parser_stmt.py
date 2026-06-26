"""
段言（Duan）编程语言 - 语句解析混入类

提供所有语句级别解析方法，包括：
- 模块解析
- 变量声明、赋值、条件、循环
- 导入/导出
- 段落定义
- 类/接口定义
- 模式匹配
- 异常处理
"""

from typing import List, Any, Optional
from tokens import Token, TokenType
from keywords import VERB_ARITY, KEYWORDS_DOUBLE, KEYWORDS_SPECIAL, BUILTIN_TYPES
from ast_nodes_v3 import *
from parser_core import ParseError


class ParserStmtMixin:
    """语句解析混入类"""
    
    # =========================================================================
    # 语法规则
    # =========================================================================
    
    def _parse_module(self) -> Module:
        """解析模块"""
        statements = []
        
        while self._current():
            tok = self._current()
            
            # 跳过外层的DEDENT（level=0）
            if tok.type == TokenType.DEDENT:
                dedent_level = getattr(tok, 'value', None)
                # 如果level是None或level == 0，表示这是外层结构的结束
                # 消耗这个DEDENT并继续
                if dedent_level is None or dedent_level == 0:
                    self._consume(TokenType.DEDENT)
                    continue
            
            # 跳过空行（NEWLINE）
            if tok.type == TokenType.NEWLINE:
                self._consume(TokenType.NEWLINE)
                continue
            
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
        
        # 条件语句：如果 / 若
        if tok.type == TokenType.KEYWORD and tok.value in ('如果', '若'):
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
        
        # 段落定义或类定义：《段名》段 或 《类名》类
        # 或段落调用：《段名》(参数)
        if tok.type == TokenType.LBOOK:
            # 先不消耗，peek看是否是类定义
            if self._peek_bracket_class():
                return self._parse_bracket_class()
            # 检查是否是段落调用（非定义）：《段名》(参数)
            # 《段名》段 是定义，《段名》(参数) 是调用
            if self._peek(1) and self._peek(1).type == TokenType.IDENTIFIER:
                if self._peek(2) and self._peek(2).type == TokenType.RBOOK:
                    if self._peek(3) and self._peek(3).type == TokenType.LPAREN:
                        return self._parse_expr_stmt()
            return self._parse_paragraph()
        
        # 段落定义：段落/函数 段名 参数 参数名
        if tok.type == TokenType.KEYWORD and tok.value in ('段落', '函数'):
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
            elif tok.type == TokenType.KEYWORD and tok.value not in ('为',):
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
        """解析赋值语句：标识符 等于 值。或 标识符 加上/减去/乘以/除以 值。"""
        # 复合赋值运算符映射
        compound_ops = {
            '加上': '加',
            '减去': '减',
            '乘以': '乘',
            '除以': '除',
            '模以': '模',
            '幂以': '幂',
        }
        
        # 标识符
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 检查索引赋值：甲[丁] 为/等于 值。
        if self._current() and self._current().type == TokenType.LBRACKET:
            self._consume(TokenType.LBRACKET)
            index = self._parse_expr()
            self._consume(TokenType.RBRACKET)
            
            # 检查索引复合赋值：甲[丁] 加上 值。
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value in compound_ops:
                op_text = self._current().value
                operator = compound_ops[op_text]
                self._consume(TokenType.KEYWORD, op_text)
                value = self._parse_expr()
                if self._current() and self._current().type == TokenType.DOT:
                    self._consume(TokenType.DOT)
                # 暂不支持复合赋值
                raise ParseError(f"暂不支持索引复合赋值", name_tok.line, name_tok.col, name_tok.value)
            
            # 检查等于/为
            if not self._match(TokenType.KEYWORD, '等于') and not self._match(TokenType.KEYWORD, '为'):
                self.pos -= 1  # 回退
                return self._parse_expr_stmt()
            
            # 消耗等于/为
            self._consume()
            
            value = self._parse_expr()
            
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            
            return IndexedAssignment(name, index, value)
        
        # 检查复合赋值：甲 加上 1。
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value in compound_ops:
            op_text = self._current().value
            operator = compound_ops[op_text]
            self._consume(TokenType.KEYWORD, op_text)
            
            # 值
            value = self._parse_expr()
            
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            
            return CompoundAssignment(name, operator, value)
        
        # 等于或为
        if not self._match(TokenType.KEYWORD, '等于') and not self._match(TokenType.KEYWORD, '为'):
            # 不是赋值语句，可能是表达式
            self.pos -= 1  # 回退标识符
            return self._parse_expr_stmt()
        
        # 消耗等于/为
        self._consume()
        
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
        
        # 检查是否为解构赋值：设 (甲, 乙) 为 元组 或 设 [首, 余] 为 列表
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
            return DestructuringAssignment(variables, value, style='tuple')
        
        # 检查是否为列表解构赋值：设 [首, 余] 为 列表
        if self._current() and self._current().type == TokenType.LBRACKET:
            self._consume(TokenType.LBRACKET)
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
            self._consume(TokenType.RBRACKET)
            # 为
            self._consume(TokenType.KEYWORD, '为')
            # 值
            value = self._parse_expr()
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            return DestructuringAssignment(variables, value, style='list')
        
        # 普通变量声明：变量名（支持标识符和关键字）
        name_tok = self._current()
        if name_tok and name_tok.type == TokenType.IDENTIFIER:
            name = self._consume(TokenType.IDENTIFIER).value
        elif name_tok and name_tok.type == TokenType.KEYWORD:
            name = self._consume(TokenType.KEYWORD).value
        else:
            raise ParseError(f"期望标识符，但得到 {name_tok.type if name_tok else '输入结束'}",
                             name_tok.line if name_tok else 0, name_tok.col if name_tok else 0)
        
        # 类型注解（可选）：设 变量: 类型 为 值
        type_annotation = None
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
            type_tok = self._current()
            if type_tok and type_tok.type == TokenType.IDENTIFIER:
                type_annotation = self._consume(TokenType.IDENTIFIER).value
            elif type_tok and type_tok.type == TokenType.KEYWORD:
                type_annotation = self._consume(TokenType.KEYWORD).value
        
        # 为
        self._consume(TokenType.KEYWORD, '为')
        
        # 值
        value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return VarDecl(name, value, type_annotation=type_annotation)
    
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

        # 类型注解（可选）：定义 变量: 类型 等于 值
        type_annotation = None
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
            type_tok = self._current()
            if type_tok and type_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                type_annotation = self._consume().value

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

        return VarDecl(name, value, type_annotation=type_annotation)
    
    def _parse_if_stmt(self) -> IfStmt:
        """解析条件语句
        
        语法：
        1. 如果 条件。
            语句。
        2. 如果 条件 那么
            语句。
        3. 如果 条件 那么
            语句。
          否则
            语句。
        """
        # 如果 / 若
        if self._match(TokenType.KEYWORD, '若'):
            self._consume(TokenType.KEYWORD, '若')
        elif self._match(TokenType.KEYWORD, '如果'):
            self._consume(TokenType.KEYWORD, '如果')
        else:
            tok = self._current()
            raise ParseError(f"期望'如果'或'若'，但得到'{tok.value if tok else '输入结束'}'",
                             tok.line if tok else 0, tok.col if tok else 0)
        
        # 条件
        condition = self._parse_expr()
        
        # 那么 / 则（可选）
        if self._match(TokenType.KEYWORD, '则'):
            self._consume(TokenType.KEYWORD, '则')
        elif self._match(TokenType.KEYWORD, '那么'):
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
            # 消耗 NEWLINE 和 INDENT
            if self._current() and self._current().type == TokenType.NEWLINE:
                self._consume(TokenType.NEWLINE)
            if self._current() and self._current().type == TokenType.INDENT:
                self._consume(TokenType.INDENT)
            
            then_body = self._parse_body()
            
        # 消耗 DEDENT（then块结束）
            if self._current() and self._current().type == TokenType.DEDENT:
                self._consume(TokenType.DEDENT)
            
            # 消耗"结束"关键字（可选，if块后的结束标记）
            # 但注意：如果"结束"后面紧跟"否则"，则"结束"属于整个if-else，不应在此消耗
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
                # Check if next is 否则 - if so, this 结束 belongs to if-else structure, don't consume
                next_tok = self._peek(1)
                if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value == '否则':
                    pass  # Don't consume, leave for 否则 handling
                else:
                    self._consume(TokenType.KEYWORD, '结束')
                    if self._current() and self._current().type == TokenType.DOT:
                        self._consume(TokenType.DOT)
            elif self._current() and self._current().type == TokenType.IDENTIFIER and self._current().value == '结束':
                next_tok = self._peek(1)
                if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value == '否则':
                    pass  # Don't consume
                else:
                    self._consume(TokenType.IDENTIFIER)
                    if self._current() and self._current().type == TokenType.DOT:
                        self._consume(TokenType.DOT)
        else:
            stmt = self._parse_statement()
            then_body = [stmt] if stmt else []
        
        # 否则？
        else_body = None
        
        if self._match(TokenType.KEYWORD, '否则'):
            self._consume(TokenType.KEYWORD, '否则')
            
            # 检查是否是"否则如果"
            if self._match(TokenType.KEYWORD, '如果'):
                self._consume(TokenType.KEYWORD, '如果')
                # 递归解析"否则如果"分支
                condition2 = self._parse_expr()
                
                # 那么 / 则（可选）
                if self._match(TokenType.KEYWORD, '则'):
                    self._consume(TokenType.KEYWORD, '则')
                elif self._match(TokenType.KEYWORD, '那么'):
                    self._consume(TokenType.KEYWORD, '那么')
                
                # 冒号（可选）
                if self._current() and self._current().type == TokenType.COLON:
                    self._consume(TokenType.COLON)
                
                if has_colon:
                    # 消耗 NEWLINE 和 INDENT
                    if self._current() and self._current().type == TokenType.NEWLINE:
                        self._consume(TokenType.NEWLINE)
                    if self._current() and self._current().type == TokenType.INDENT:
                        self._consume(TokenType.INDENT)
                    
                    elif_body = self._parse_body()
                    
                    # 消耗 DEDENT
                    if self._current() and self._current().type == TokenType.DEDENT:
                        self._consume(TokenType.DEDENT)
                else:
                    stmt = self._parse_statement()
                    elif_body = [stmt] if stmt else []
                
                # 递归处理后续的"否则如果"或"否则"分支
                # 检查是否还有"否则"
                nested_else_body = None
                if self._current() and self._match(TokenType.KEYWORD, '否则'):
                    self._consume(TokenType.KEYWORD, '否则')
                    
                    if self._match(TokenType.KEYWORD, '如果'):
                        self._consume(TokenType.KEYWORD, '如果')
                        condition3 = self._parse_expr()
                        
                        if self._match(TokenType.KEYWORD, '则'):
                            self._consume(TokenType.KEYWORD, '则')
                        elif self._match(TokenType.KEYWORD, '那么'):
                            self._consume(TokenType.KEYWORD, '那么')
                        
                        if self._current() and self._current().type == TokenType.COLON:
                            self._consume(TokenType.COLON)
                        
                        if has_colon:
                            if self._current() and self._current().type == TokenType.NEWLINE:
                                self._consume(TokenType.NEWLINE)
                            if self._current() and self._current().type == TokenType.INDENT:
                                self._consume(TokenType.INDENT)
                            
                            elif_body2 = self._parse_body()
                            
                            if self._current() and self._current().type == TokenType.DEDENT:
                                self._consume(TokenType.DEDENT)
                        else:
                            stmt = self._parse_statement()
                            elif_body2 = [stmt] if stmt else []
                        
                        # 继续递归检查
                        # 简化处理：最多三层嵌套
                        inner_else_body = None
                        if self._current() and self._match(TokenType.KEYWORD, '否则'):
                            self._consume(TokenType.KEYWORD, '否则')
                            
                            if self._match(TokenType.KEYWORD, '如果'):
                                # 更多嵌套，简化处理：返回None
                                pass
                            else:
                                if self._current() and self._current().type == TokenType.DOT:
                                    self._consume(TokenType.DOT)
                                if self._current() and self._current().type == TokenType.COLON:
                                    self._consume(TokenType.COLON)
                                
                                if has_colon:
                                    if self._current() and self._current().type == TokenType.NEWLINE:
                                        self._consume(TokenType.NEWLINE)
                                    if self._current() and self._current().type == TokenType.INDENT:
                                        self._consume(TokenType.INDENT)
                                    
                                    inner_else_body = self._parse_body()
                                    
                                    if self._current() and self._current().type == TokenType.DEDENT:
                                        self._consume(TokenType.DEDENT)
                                else:
                                    stmt = self._parse_statement()
                                    inner_else_body = [stmt] if stmt else []
                        
                        # 返回多层嵌套的IfStmt
                        return IfStmt(condition, then_body, 
                                     IfStmt(condition2, elif_body, 
                                            IfStmt(condition3, elif_body2, inner_else_body)))
                    else:
                        # 纯否则分支
                        if self._current() and self._current().type == TokenType.DOT:
                            self._consume(TokenType.DOT)
                        if self._current() and self._current().type == TokenType.COLON:
                            self._consume(TokenType.COLON)
                        
                        if has_colon:
                            if self._current() and self._current().type == TokenType.NEWLINE:
                                self._consume(TokenType.NEWLINE)
                            if self._current() and self._current().type == TokenType.INDENT:
                                self._consume(TokenType.INDENT)
                            
                            nested_else_body = self._parse_body()
                            
                            if self._current() and self._current().type == TokenType.DEDENT:
                                self._consume(TokenType.DEDENT)
                        else:
                            stmt = self._parse_statement()
                            nested_else_body = [stmt] if stmt else []
                
                # 返回嵌套的IfStmt
                return IfStmt(condition, then_body, IfStmt(condition2, elif_body, nested_else_body))
            
            # 句号（可选）
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
            
            # 冒号（可选）
            if self._current() and self._current().type == TokenType.COLON:
                self._consume(TokenType.COLON)
            
            if has_colon:
                # 消耗 NEWLINE 和 INDENT
                if self._current() and self._current().type == TokenType.NEWLINE:
                    self._consume(TokenType.NEWLINE)
                if self._current() and self._current().type == TokenType.INDENT:
                    self._consume(TokenType.INDENT)
                
                else_body = self._parse_body()
                
                # 消耗 DEDENT（else块结束）
                if self._current() and self._current().type == TokenType.DEDENT:
                    self._consume(TokenType.DEDENT)
                
                # 消耗"结束"关键字（可选，if-else整体后的结束标记）
                if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
                    self._consume(TokenType.KEYWORD, '结束')
                    if self._current() and self._current().type == TokenType.DOT:
                        self._consume(TokenType.DOT)
                elif self._current() and self._current().type == TokenType.IDENTIFIER and self._current().value == '结束':
                    self._consume(TokenType.IDENTIFIER)
                    if self._current() and self._current().type == TokenType.DOT:
                        self._consume(TokenType.DOT)
            else:
                stmt = self._parse_statement()
                else_body = [stmt] if stmt else []
        
        return IfStmt(condition, then_body, else_body)
    
    def _parse_foreach_stmt(self) -> ForeachStmt:
        """解析遍历循环"""
        # 跳过 NEWLINE
        if self._current() and self._current().type == TokenType.NEWLINE:
            self._consume(TokenType.NEWLINE)
        
        # 遍历 / 对
        if self._match(TokenType.KEYWORD, '对'):
            self._consume(TokenType.KEYWORD, '对')
        else:
            self._consume(TokenType.KEYWORD, '遍历')
        
        # 变量名
        var_tok = self._consume(TokenType.IDENTIFIER)
        variable = var_tok.value
        
        # 在 / 之 / 中的
        tok = self._current()
        if self._match(TokenType.KEYWORD, '在'):
            self._consume(TokenType.KEYWORD, '在')
        elif self._match(TokenType.KEYWORD, '之'):
            self._consume(TokenType.KEYWORD, '之')
        elif self._match(TokenType.KEYWORD, '中的'):
            self._consume(TokenType.KEYWORD, '中的')
        else:
            raise ParseError(f"遍历循环期望'在'、'之'或'中的'，但得到 {tok.type} = '{tok.value}'", tok.line, tok.col)
        
        # 可迭代对象
        iterable = self._parse_expr()
        
        # 冒号
        self._consume(TokenType.COLON)
        
        # 消耗 NEWLINE 和 INDENT
        if self._current() and self._current().type == TokenType.NEWLINE:
            self._consume(TokenType.NEWLINE)
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)
        
        # 循环体
        body = self._parse_body()
        
        # 消耗 DEDENT（循环体结束）
        if self._current() and self._current().type == TokenType.DEDENT:
            self._consume(TokenType.DEDENT)
        
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
        
        # 消耗 NEWLINE 和 INDENT
        if self._current() and self._current().type == TokenType.NEWLINE:
            self._consume(TokenType.NEWLINE)
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)
        
        # 循环体 - 使用_parse_body
        body = self._parse_body()
        
        # 消耗 DEDENT（循环体结束）
        # _parse_body 遇到 DEDENT 时会 break，这里需要消耗它
        if self._current() and self._current().type == TokenType.DEDENT:
            self._consume(TokenType.DEDENT)
        
        # 消耗"结束"关键字（可选）
        # "结束"可能被词法分析器识别为 IDENTIFIER（非关键字），两种情况都要处理
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        elif self._current() and self._current().type == TokenType.IDENTIFIER and self._current().value == '结束':
            self._consume(TokenType.IDENTIFIER)
            if self._current() and self._current().type == TokenType.DOT:
                self._consume(TokenType.DOT)
        
        return WhileStmt(condition, body)
    
    def _parse_return_stmt(self) -> ReturnStmt:
        """解析返回语句"""
        # 返回
        self._consume(TokenType.KEYWORD, '返回')
        
        # 表达式（可选）
        value = None
        # 检查是否有表达式：如果下一个token不是句号、不是DEDENT、不是语句关键字，则解析表达式
        if self._current():
            tok = self._current()
            if tok.type != TokenType.DOT and tok.type != TokenType.DEDENT:
                # 不是语句关键字的情况下才解析表达式
                is_stmt_keyword = (tok.type == TokenType.KEYWORD and 
                                    tok.value in ('设', '定义', '当', '如果', '若', '遍历', 
                                                  '打印', '导入', '导出', '跳出', '跳过', 
                                                  '尝试', '抛出', '匹配', '返回', '属性', 
                                                  '构造', '段落', '函数', '类', '接口'))
                if not is_stmt_keyword:
                    value = self._parse_expr()
        
        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
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
        
        或带类型过滤：
        尝试：
          语句...
        捕获 值错误：
          语句...
        
        或带类型和变量：
        尝试：
          语句...
        捕获 值错误 异常变量：
          语句...
        
        或带最终块：
        尝试：
          语句...
        捕获 异常变量：
          语句...
        最终：
          语句...
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
            # 消耗 NEWLINE 和 INDENT
            if self._current() and self._current().type == TokenType.NEWLINE:
                self._consume(TokenType.NEWLINE)
            if self._current() and self._current().type == TokenType.INDENT:
                self._consume(TokenType.INDENT)
            
            body = self._parse_body()
            
            # 消耗 DEDENT（段落体结束）
            if self._current() and self._current().type == TokenType.DEDENT:
                self._consume(TokenType.DEDENT)
            
            # 如果DEDENT的level不是0，还需要继续消耗缩进
            # 直到遇到level=0的DEDENT或非DEDENT token
            while self._current() and self._current().type == TokenType.DEDENT:
                dedent_tok = self._current()
                # 检查DEDENT的level
                if hasattr(dedent_tok, 'value') and dedent_tok.value == 0:
                    # level=0表示回到0级缩进，段落定义结束
                    # 消耗这个DEDENT
                    self._consume(TokenType.DEDENT)
                    break
                # 否则继续消耗
                self._consume(TokenType.DEDENT)
            
            # 注意：不消耗"结束"关键字和DOT，让外层结构处理（_parse_module）
            
        else:
            stmt = self._parse_statement()
            body = [stmt] if stmt else []
        
        return Paragraph(name, params, return_type, body)
    
    def _parse_paragraph_v2(self) -> Paragraph:
        """解析段落定义：段落/函数 段名 参数/接收/输入 参数名。"""
        # 段落 或 函数 或 段
        if self._match(TokenType.KEYWORD, '段落'):
            self._consume(TokenType.KEYWORD, '段落')
        elif self._match(TokenType.KEYWORD, '函数'):
            self._consume(TokenType.KEYWORD, '函数')
        elif self._match(TokenType.KEYWORD, '段'):
            self._consume(TokenType.KEYWORD, '段')
        else:
            tok = self._current()
            raise ParseError(f"期望'段落'、'函数'或'段'，但得到 {tok.type if tok else '输入结束'} = '{tok.value if tok else ''}'",
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
            elif next_tok.type == TokenType.KEYWORD and next_tok.value not in ('参数', '接收', '输入', '返回'):
                name_parts.append(self._consume(TokenType.KEYWORD).value)
            else:
                break
        
        name = ''.join(name_parts)
        
        # 参数列表（可选）- 支持"参数"、"接收"和"输入"三种写法，也支持括号 (a, b) 形式
        params = []
        has_params = False
        if self._match(TokenType.KEYWORD, '参数'):
            self._consume(TokenType.KEYWORD, '参数')
            has_params = True
        elif self._match(TokenType.KEYWORD, '接收'):
            self._consume(TokenType.KEYWORD, '接收')
            has_params = True
        elif self._match(TokenType.KEYWORD, '输入'):
            self._consume(TokenType.KEYWORD, '输入')
            has_params = True
        elif self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            has_params = True
            # 括号形式：(甲, 乙) 或 (甲: 数, 乙: 数)
            while self._current() and self._current().type != TokenType.RPAREN:
                if self._current().type == TokenType.COMMA:
                    self._consume(TokenType.COMMA)
                    continue
                tok = self._current()
                param_name = None
                param_type = None
                if tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                elif tok.type == TokenType.KEYWORD:
                    param_name = self._consume(TokenType.KEYWORD).value
                elif tok.type == TokenType.CHINESE_NUM:
                    param_name = str(self._consume(TokenType.CHINESE_NUM).value)
                else:
                    break
                if param_name is not None:
                    # 可选类型注解：甲: 数
                    if self._current() and self._current().type == TokenType.COLON:
                        self._consume(TokenType.COLON)
                        type_tok = self._current()
                        if type_tok and type_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                            param_type = self._consume().value
                    params.append({'name': param_name, 'type': param_type})
            if self._current() and self._current().type == TokenType.RPAREN:
                self._consume(TokenType.RPAREN)
        
        if has_params:
            
            # 收集参数名，直到句号、冒号或语句关键字
            _stmt_keywords = {'设', '定义', '当', '如果', '若', '遍历', '返回', '打印', '导入', '导出', '跳出', '跳过', '尝试', '抛出', '匹配'}
            while self._current() and self._current().type != TokenType.DOT and self._current().type != TokenType.COLON:
                tok = self._current()
                # 遇到语句关键字结束参数收集
                if tok.type == TokenType.KEYWORD and (tok.value == '返回' or tok.value in _stmt_keywords):
                    break
                # 跳过逗号分隔符
                if tok.type == TokenType.COMMA:
                    self._consume(TokenType.COMMA)
                    continue
                if tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                    # 类型注解（可选）：甲: 数 — 只有冒号后紧跟标识符/关键字才是类型注解
                    param_type = None
                    if self._current() and self._current().type == TokenType.COLON:
                        # 检查冒号后是不是类型名（标识符或关键字），如果是则为类型注解
                        next_tok = self._peek(1)
                        if next_tok and next_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.CHINESE_NUM):
                            self._consume(TokenType.COLON)
                            type_tok = self._current()
                            if type_tok and type_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.CHINESE_NUM):
                                param_type = self._consume().value
                        else:
                            # 冒号后不是类型名，说明是参数列表结束的冒号，先添加参数再跳出
                            params.append({'name': param_name, 'type': param_type})
                            break
                    if param_type is not None or not (self._current() and self._current().type == TokenType.COLON):
                        params.append({'name': param_name, 'type': param_type})
                elif tok.type == TokenType.KEYWORD:
                    # 参数名可能是关键字（如数学运算符），但排除语句关键字
                    param_name = self._consume(TokenType.KEYWORD).value
                    # 类型注解（可选）
                    param_type = None
                    if self._current() and self._current().type == TokenType.COLON:
                        next_tok = self._peek(1)
                        if next_tok and next_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.CHINESE_NUM):
                            self._consume(TokenType.COLON)
                            type_tok = self._current()
                            if type_tok and type_tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.CHINESE_NUM):
                                param_type = self._consume().value
                        else:
                            # 冒号后不是类型名，说明是参数列表结束的冒号，先添加参数再跳出
                            params.append({'name': param_name, 'type': param_type})
                            break
                    if param_type is not None or not (self._current() and self._current().type == TokenType.COLON):
                        params.append({'name': param_name, 'type': param_type})
                else:
                    break
        
        # 返回类型（可选）— 仅当后跟内置类型名时才当作返回类型标注
        return_type = None
        if (self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '返回'
            and self._peek(1) and self._peek(1).value in BUILTIN_TYPES):
            self._consume(TokenType.KEYWORD, '返回')
            return_type = self._consume().value  # 消耗类型名
        
        # 句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 冒号（支持：或：）
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)

        # 消耗 NEWLINE 和 INDENT（段落体的缩进块）
        if self._current() and self._current().type == TokenType.NEWLINE:
            self._consume(TokenType.NEWLINE)
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)

        # 段落体
        body = self._parse_body()

        # 消耗 DEDENT（段落体结束）
        if self._current() and self._current().type == TokenType.DEDENT:
            self._consume(TokenType.DEDENT)
        
        # 消耗"结束"关键字（可选，但推荐使用）
        # "结束"可能被词法分析器识别为 IDENTIFIER（非关键字），两种情况都要处理
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '结束':
            self._consume(TokenType.KEYWORD, '结束')
        elif self._current() and self._current().type == TokenType.IDENTIFIER and self._current().value == '结束':
            self._consume(TokenType.IDENTIFIER)
        
        # 消耗句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return Paragraph(name, params, return_type, body)
    
    def _parse_body(self) -> List[ASTNode]:
        """解析代码块
        
        正确处理嵌套的 INDENT/DEDENT：
        - 调用者已消耗当前块的 INDENT
        - 内部嵌套结构（if/while/for 等）会产生额外的 INDENT/DEDENT
        - 用 depth 计数器跟踪嵌套深度
        - 当 depth 回到 -1 时，表示遇到了调用者那个 INDENT 对应的 DEDENT，停止解析
        """
        statements = []
        depth = 0

        max_statements = 100
        count = 0

        while self._current() and count < max_statements:
            tok = self._current()

            # 跳过 NEWLINE token
            if tok.type == TokenType.NEWLINE:
                self._consume(TokenType.NEWLINE)
                continue

            # INDENT：嵌套深度增加
            if tok.type == TokenType.INDENT:
                self._consume(TokenType.INDENT)
                depth += 1
                continue

            # DEDENT：嵌套深度减少
            if tok.type == TokenType.DEDENT:
                if depth == 0:
                    # 检查是否是空行导致的假 DEDENT（后面跟着 INDENT）
                    next_tok = self._peek(1)
                    if next_tok and next_tok.type == TokenType.INDENT:
                        # 跳过这对 DEDENT+INDENT，继续解析
                        self._consume(TokenType.DEDENT)
                        self._consume(TokenType.INDENT)
                        continue
                    # 深度为 0 时遇到 DEDENT，说明当前块结束
                    # 不消耗这个 DEDENT，留给调用者处理
                    break
                else:
                    # 嵌套结构结束，消耗 DEDENT 并减少深度
                    self._consume(TokenType.DEDENT)
                    depth -= 1
                    continue

            # 否则标记（if语句的else分支）- 在块模式下，_parse_body遇到"否则"应该停止
            # 让调用者（如_parse_if_stmt）来处理
            if tok.type == TokenType.KEYWORD and tok.value == '否则':
                break

            # 异常处理的特殊标记（捕获、最终）
            if tok.type == TokenType.KEYWORD and tok.value in ('捕获', '最终'):
                break

            # 类/接口定义（在body中遇到的，作为嵌套处理）
            if tok.type == TokenType.KEYWORD and tok.value in ('段落', '函数', '段', '类', '接口'):
                break

            # 段落定义：《段名》段(...) - 嵌套段落定义也结束当前body
            if tok.type == TokenType.LBOOK:
                next_tok = self._peek(1)
                if next_tok and next_tok.type == TokenType.IDENTIFIER:
                    third_tok = self._peek(2)
                    fourth_tok = self._peek(3)
                    if (third_tok and third_tok.type == TokenType.RBOOK and 
                        fourth_tok and fourth_tok.type == TokenType.KEYWORD and fourth_tok.value == '段'):
                        break

            # 解析语句
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
                count += 1
            else:
                break

        return statements
    
    # =============================================================================
    # 类定义解析
    # =============================================================================

    def _peek_bracket_class(self) -> bool:
        """检查是否是《类名》类: 语法"""
        # 当前应该是 LBOOK，检查后跟 IDENTIFIER RBOOK KEYWORD('类')
        if self._peek(1) and self._peek(1).type == TokenType.IDENTIFIER:
            if self._peek(2) and self._peek(2).type == TokenType.RBOOK:
                if self._peek(3) and self._peek(3).type == TokenType.KEYWORD and self._peek(3).value == '类':
                    return True
        return False

    def _parse_bracket_class(self) -> ClassDefinition:
        """解析《类名》类: 语法
        
        示例：
        《计算器》类:
            定义 结果 等于 0。
            《加》方法(x):
                结果 等于 结果 加 x。
        """
        # 《
        self._consume(TokenType.LBOOK)
        # 类名
        name = self._consume(TokenType.IDENTIFIER).value
        # 》
        self._consume(TokenType.RBOOK)
        # 类
        self._consume(TokenType.KEYWORD, '类')
        # 冒号
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
        elif self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 类体
        attributes = []
        methods = []
        
        while self._current():
            tok = self._current()
            
            # DEDENT 结束类体
            if tok.type == TokenType.DEDENT:
                break
            
            # 属性定义：定义 属性名 等于 值。
            if tok.type == TokenType.KEYWORD and tok.value == '定义':
                attr = self._parse_bracket_class_attribute()
                if attr:
                    attributes.append(attr)
                continue
            
            # 方法定义：《方法名》方法(参数)
            if tok.type == TokenType.LBOOK:
                method = self._parse_bracket_class_method()
                if method:
                    methods.append(method)
                continue
            
            # 跳过空行等
            self._consume()
        
        return ClassDefinition(
            name=name,
            attributes=attributes,
            methods=methods,
            base_classes=[]
        )

    def _parse_bracket_class_attribute(self) -> Optional[AttributeDeclaration]:
        """解析《类名》类中的属性定义：定义 属性名 等于 值。"""
        # 定义
        self._consume(TokenType.KEYWORD, '定义')
        
        # 属性名
        name_tok = self._consume(TokenType.IDENTIFIER)
        attr_name = name_tok.value
        
        # 初始值（可选）
        default_value = None
        # 等于
        if self._current() and self._current().type == TokenType.KEYWORD and self._current().value == '等于':
            self._consume(TokenType.KEYWORD, '等于')
            # 初始值
            default_value = self._parse_expr()
        
        # 句号
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        return AttributeDeclaration(name=attr_name, default_value=default_value)

    def _parse_bracket_class_method(self) -> Optional[MethodDefinition]:
        """解析《类名》类中的方法定义：《方法名》方法(参数)"""
        # 《
        self._consume(TokenType.LBOOK)
        
        # 方法名
        name_tok = self._consume(TokenType.IDENTIFIER)
        method_name = name_tok.value
        
        # 》
        self._consume(TokenType.RBOOK)
        
        # 方法
        kw_tok = self._current()
        if kw_tok and kw_tok.type in (TokenType.KEYWORD, TokenType.IDENTIFIER) and kw_tok.value == '方法':
            self._consume()
        else:
            raise ParseError(f"期望'方法'，但得到 {kw_tok.type if kw_tok else '输入结束'}（附近: '{kw_tok.value if kw_tok else ''}'）", kw_tok.line if kw_tok else 0, kw_tok.col if kw_tok else 0)
        
        # 参数列表 (params)
        params = []
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            while not self._match(TokenType.RPAREN):
                tok = self._current()
                if tok and tok.type == TokenType.IDENTIFIER:
                    param_name = self._consume(TokenType.IDENTIFIER).value
                    params.append(Parameter(name=param_name))
                elif tok and tok.type == TokenType.KEYWORD:
                    param_name = self._consume(TokenType.KEYWORD).value
                    params.append(Parameter(name=param_name))
                # 逗号
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                elif self._match(TokenType.RPAREN):
                    break
                else:
                    break
            self._consume(TokenType.RPAREN)
        
        # 冒号
        if self._current() and self._current().type == TokenType.COLON:
            self._consume(TokenType.COLON)
        elif self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)
        
        # 方法体
        body = []
        while self._current():
            tok = self._current()
            
            # DEDENT 结束方法体
            if tok.type == TokenType.DEDENT:
                break
            
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        return MethodDefinition(
            name=method_name,
            parameters=params,
            body=body,
            is_constructor=(method_name == '初始化' or method_name == '构造')
        )

    def _parse_class_definition(self) -> ClassDefinition:
        """解析类定义

        语法：
        类 类名。
          属性 属性名。
          属性 属性名。

          构造 参数 参数名 参数名。
            己属性名 为 参数名。

          段落 方法名 参数 参数名。
            方法体。

        或带继承：
        类 类名 继承 父类名。
          ...
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

        # 解析类体（依赖 INDENT/DEDENT 结构）
        # 首先检查是否有 INDENT（表示有类体）
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)  # 消耗 INDENT
            
            while self._current():
                tok = self._current()

                # DEDENT 处理
                if tok.type == TokenType.DEDENT:
                    if tok.value == 0:
                        # 完全结束类体
                        self._consume(TokenType.DEDENT)
                        break
                    else:
                        # 中间级别的 DEDENT（方法体结束等），消耗后继续
                        self._consume(TokenType.DEDENT)
                        continue

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
                elif tok.type == TokenType.KEYWORD and tok.value in ('段落', '段', '函数'):
                    method = self._parse_method_definition(is_constructor=False)    
                    methods.append(method)
                elif tok.type == TokenType.KEYWORD and tok.value == '私段落':       
                    method = self._parse_method_definition(is_constructor=False)    
                    method.is_private = True  # 标记为私有
                    methods.append(method)

                # 其他情况（不应该发生）
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

        语法：属性 属性名[。]
        """
        # 属性
        self._consume(TokenType.KEYWORD, '属性')

        # 属性名
        name_tok = self._consume(TokenType.IDENTIFIER)
        attr_name = name_tok.value

        # 句号（可选）
        if self._current() and self._current().type == TokenType.DOT:
            self._consume(TokenType.DOT)

        return AttributeDeclaration(name=attr_name)

    def _parse_method_definition(self, is_constructor=False) -> MethodDefinition:
        """解析方法定义

        语法：
        构造 接收 参数名 参数名：
          方法体

        或：
        段落 方法名 接收 参数名 参数名：
          方法体

        或：
        段 方法名 接收 参数名 参数名：
          方法体

        或：
        函数 方法名 接收 参数名 参数名：
          方法体
        """
        method_name = None

        if is_constructor:
            # 构造
            self._consume(TokenType.KEYWORD, '构造')
            method_name = '__init__'
        else:
            # 段落 / 段 / 函数
            tok = self._current()
            if tok and tok.type == TokenType.KEYWORD and tok.value in ('段落', '段', '函数'):
                self._consume(TokenType.KEYWORD)
            else:
                raise ParseError(f"期望'段落'、'段'或'函数'，但得到'{tok.value if tok else '输入结束'}'", 
                                tok.line if tok else 0, tok.col if tok else 0, tok.value if tok else None)
            
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
        
        # 消耗方法体的 INDENT（如果有）
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)
        
        while self._current():
            tok = self._current()

            # DEDENT 结束方法体
            if tok.type == TokenType.DEDENT:
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

        或带继承：
        接口 名称 继承 父接口1, 父接口2：
          ...
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
                    # 遇到逗号、冒号、句号时停止
                    if self._current().type in (TokenType.COLON, TokenType.DOT):
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
        
        # 解析接口体（依赖 INDENT/DEDENT 结构）
        # 首先检查是否有 INDENT（表示有接口体）
        if self._current() and self._current().type == TokenType.INDENT:
            self._consume(TokenType.INDENT)  # 消耗 INDENT
            
            while self._current():
                tok = self._current()

                # DEDENT 结束接口体
                if tok.type == TokenType.DEDENT:
                    self._consume(TokenType.DEDENT)  # 消耗这个 DEDENT
                    break

                # 方法签名：段落/函数 方法名 参数 参数名 返回 类型
                if tok.type == TokenType.KEYWORD and tok.value in ('段落', '函数'): 
                    sig = self._parse_method_signature()
                    methods.append(sig)

                # 属性声明：属性 名称（可选类型）
                elif tok.type == TokenType.KEYWORD and tok.value == '属性':
                    attr = self._parse_attribute_declaration()
                    properties.append(attr)

                # 其他情况（不应该发生）
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

            # DEDENT 结束匹配
            if tok.type == TokenType.DEDENT:
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
        """解析上下文管理器：使用 表达式 为 变量：...（依赖缩进）

        语法：
        使用 表达式 为 变量：
            语句。
        （缩进结束）
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

            # 遇到下一个"情况"或 DEDENT，停止
            if tok.type == TokenType.KEYWORD and tok.value == '情况':
                break
            if tok.type == TokenType.DEDENT:
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