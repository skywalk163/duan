"""
段言（Duan）编程语言 - 表达式解析混入类

提供所有表达式级别解析方法，包括：
- 算术表达式（加、减、乘、除）
- 比较表达式
- 逻辑表达式
- 基本表达式（数字、字符串、标识符、括号等）
- 后缀表达式（函数调用、成员访问、索引访问）
- 列表/字典字面量
- Lambda 表达式
- 字符串插值
"""

from typing import List, Any, Optional, Union
from tokens import Token, TokenType
from keywords import VERB_ARITY, KEYWORDS_DOUBLE, KEYWORDS_SPECIAL
from ast_nodes_v3 import *
from ast_nodes import UnwrapExpression
from parser_core import ParseError


class ParserExprMixin:
    """表达式解析混入类"""
    
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
            elif tok.type == TokenType.PLUS:
                # 处理 + 符号（字符串连接等）
                self._consume()
                right = self._parse_mul_expr()
                left = BinaryOp('+', left, right)
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
        
        # 一元运算符：非（逻辑非）
        if tok.type == TokenType.KEYWORD and tok.value == '非':
            self._consume(TokenType.KEYWORD, '非')
            operand = self._parse_primary()
            return UnaryOp('非', operand)
        
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
            
            # 检查是否为范围表达式：1至10 或 1到10 或 1到10步2
            next_tok = self._current()
            if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value in ('至', '到'):
                self._consume(TokenType.KEYWORD)  # 消耗「至」或「到」
                end_tok = self._current()
                if end_tok and end_tok.type == TokenType.NUMBER:
                    end_val = self._consume(TokenType.NUMBER).value
                    end_expr = NumberLiteral(end_val)
                    
                    # 检查是否有步长：步 数字
                    step_expr = None
                    step_tok = self._current()
                    if step_tok and step_tok.type == TokenType.KEYWORD and step_tok.value == '步':
                        self._consume(TokenType.KEYWORD, '步')
                        step_num_tok = self._current()
                        if step_num_tok and step_num_tok.type == TokenType.NUMBER:
                            step_val = self._consume(TokenType.NUMBER).value
                            step_expr = NumberLiteral(step_val)
                    
                    expr = RangeExpr(expr, end_expr, step_expr)
            
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
                
                # 收集参数（支持括号式和无括号式）
                args = []
                if self._current() and self._current().type == TokenType.LPAREN:
                    # 括号式参数：新建 类名(参数1, 参数2)
                    self._consume(TokenType.LPAREN)
                    while not self._match(TokenType.RPAREN):
                        arg = self._parse_comparison()
                        if arg is not None:
                            args.append(arg)
                        if self._match(TokenType.COMMA):
                            self._consume(TokenType.COMMA)
                    self._consume(TokenType.RPAREN)
                else:
                    # 无括号参数
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
                # 无参数函数：支持 "刷新输出" 或 "刷新输出()"
                if self._current() and self._current().type == TokenType.LPAREN:
                    self._consume(TokenType.LPAREN)
                    # 跳过可选的空格/内容直到右括号
                    while self._current() and self._current().type != TokenType.RPAREN:
                        self._consume()
                    if self._current() and self._current().type == TokenType.RPAREN:
                        self._consume(TokenType.RPAREN)
            elif arity == -1:
                # 可变参数：收集到阻断符为止
                # 检查是否使用了括号语法
                if self._current() and self._current().type == TokenType.LPAREN:
                    # 括号式参数：列(参数1, 参数2, 参数3)
                    self._consume(TokenType.LPAREN)
                    while not self._match(TokenType.RPAREN):
                        if self._current() and self._current().type == TokenType.COMMA:
                            self._consume(TokenType.COMMA)
                            continue
                        arg = self._parse_comparison()
                        if arg:
                            args.append(arg)
                        else:
                            break
                    if self._current() and self._current().type == TokenType.RPAREN:
                        self._consume(TokenType.RPAREN)
                else:
                    # 无括号式：列 参数1 参数2 参数3
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
                # 检查是否使用了括号语法：动词(参数1, 参数2)
                if self._current() and self._current().type == TokenType.LPAREN:
                    # 括号式参数：列表追加(成绩, 分数)
                    self._consume(TokenType.LPAREN)
                    collected = 0
                    while not self._match(TokenType.RPAREN) and collected < arity:
                        if self._current() and self._current().type == TokenType.COMMA:
                            self._consume(TokenType.COMMA)
                            continue
                        arg = self._parse_comparison()
                        if arg:
                            args.append(arg)
                            collected += 1
                        else:
                            break
                        if self._match(TokenType.COMMA):
                            self._consume(TokenType.COMMA)
                    # 跳过剩余的 token 直到右括号
                    while self._current() and self._current().type != TokenType.RPAREN:
                        self._consume()
                    if self._current() and self._current().type == TokenType.RPAREN:
                        self._consume(TokenType.RPAREN)
                else:
                    # 无括号式：列表追加 成绩 分数
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
            # 检测：如果后面是块关键字（那么、否则、结束、当）或标点（。，）
            # 且没有括号，则将此运算符关键字作为标识符（变量名）处理
            if not next_tok or next_tok.type == TokenType.LPAREN:
                pass  # 下面的正常分支处理括号
            elif (next_tok.type == TokenType.KEYWORD and next_tok.value in KEYWORDS_DOUBLE) or \
                 next_tok.type in (TokenType.DOT, TokenType.COMMA, TokenType.RPAREN,
                                    TokenType.RBRACKET, TokenType.COLON, TokenType.EOF):
                if next_tok.type != TokenType.LPAREN:
                    # 当作变量名处理，如 "如果操作等于加那么..." 中的 "加"
                    self._consume()
                    return self._parse_postfix(Identifier(name))
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
            
            # 合并连续的 IDENTIFIER 令牌（用于处理 tokenizer 将 "字典创建" 拆分为两个 IDENTIFIER 的情况）
            while self._current() and self._current().type == TokenType.IDENTIFIER:
                name += self._consume().value
            
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
            elif tok.type == TokenType.KEYWORD and tok.value not in ('返回', '匹配', '情况', '如果', '若', '否则', '遍历', '当', '设', '定义', '类', '构造', '段落', '函数', '尝试', '捕获', '抛出', '最终', '导入', '导出', '从'):
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
            if self._current() and self._current().type == TokenType.KEYWORD and self._current().value in ('若', '如果'):
                self._consume()
                condition = self._parse_expr()

            self._consume(TokenType.RBRACKET)
            return ListComprehension(first_expr, variable, iterable, condition)

        # 普通列表字面量：元素, 元素, ...
        elements = [first_expr]
        while self._match(TokenType.COMMA):
            self._consume(TokenType.COMMA)
            if self._match(TokenType.RBRACKET):
                break
            elem = self._parse_comparison()
            elements.append(elem)
        self._consume(TokenType.RBRACKET)
        return ListLiteral(elements)

    def _parse_postfix(self, expr: ASTNode) -> ASTNode:
        """解析后缀表达式（索引访问、成员访问、函数调用、解包）"""
        while self._current():
            tok = self._current()

            # 解包操作：值! 或 值！
            if tok.type == TokenType.BANG:
                self._consume(TokenType.BANG)
                expr = UnwrapExpression(value=expr)
                continue

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
            # 支持英文点号(.) 和 中文"的"两种属性访问语法
            # "obj.属性" / "obj.方法()" 或 "obj的属性" / "obj的方法()"
            is_dot_access = False
            if tok.type == TokenType.DOT:
                # 检查是否是英文点号（成员访问）还是中文句号（语句结束）        
                if tok.value == '.':
                    is_dot_access = True
                # 中文句号(。)是语句结束符，不进行成员访问

            # 「的」或「之」作为属性访问运算符
            if not is_dot_access and tok.type == TokenType.KEYWORD and tok.value in ('的', '之'):
                is_dot_access = True

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
                # 使用 _parse_comparison 而非 _parse_expr，
                # 避免逗号被误识别为管道操作符
                arg = self._parse_comparison()
                args.append(arg)

                # 逗号分隔
                if self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)

            self._consume(TokenType.RPAREN)

            return ParagraphCall(name, args)

        # 否则是字符串字面量
        return StringLiteral(name)