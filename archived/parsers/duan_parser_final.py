"""
段言（Duan）编程语言 - 最终集成解析器

策略：两阶段解析
1. 词法分析器生成 Token 流
2. Lark 解析 Token 流生成 AST

支持：
- 无空格分词（决策29）
- 双字关键字优先匹配
- 类型切换自动分词
"""

from lark import Lark, Token, Tree, Transformer, Visitor
from typing import List, Any, Optional, Iterator
from lexer import Lexer, LexerError
from tokens import TokenType
import sys


# =============================================================================
# Lark 兼容的 Token 流生成器
# =============================================================================

class DuanLexerWrapper:
    """将自定义词法分析器包装为 Lark 可用的外部 lexer"""
    
    def __init__(self):
        self.lexer = Lexer()
    
    def lex(self, source: str) -> Iterator[Token]:
        """生成 Lark Token 流"""
        tokens = self.lexer.tokenize(source)
        
        for tok in tokens:
            lark_token = self._convert_token(tok)
            if lark_token:
                yield lark_token
    
    def _convert_token(self, tok) -> Optional[Token]:
        """将段言 Token 转换为 Lark Token"""
        # 关键字映射
        keyword_map = {
            '定义': 'DEFINE',
            '等于': 'EQUALS_KW',
            '如果': 'IF',
            '那么': 'THEN',
            '否则': 'ELSE',
            '遍历': 'FOREACH',
            '当': 'WHILE',
            '返回': 'RETURN',
            '加': 'ADD',
            '减': 'SUB',
            '乘': 'MUL',
            '除': 'DIV',
            '大于': 'GT',
            '小于': 'LT',
            '不等于': 'NE',
            '大于等于': 'GE',
            '小于等于': 'LE',
            '打印': 'PRINT',
        }
        
        if tok.type == TokenType.KEYWORD:
            token_type = keyword_map.get(tok.value, 'KEYWORD')
            return Token(token_type, tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.CHINESE_NUM:
            return Token('CHINESE_NUM', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.IDENTIFIER:
            return Token('IDENTIFIER', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.NUMBER:
            return Token('NUMBER', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.STRING:
            return Token('STRING', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.DOT:
            return Token('DOT', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.COLON:
            return Token('COLON', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.NEWLINE:
            return Token('_NL', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.INDENT:
            return Token('_INDENT', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.DEDENT:
            return Token('_DEDENT', tok.value, line=tok.line, column=tok.col)
        
        elif tok.type == TokenType.EOF:
            return None  # Lark 自动处理 EOF
        
        return None


# =============================================================================
# 段言语法（简化的 LALR 语法）
# =============================================================================

DUAN_GRAMMAR = r"""
start: statement*

statement: var_decl

var_decl: "定义" IDENTIFIER "等于" expr DOT

expr: term ((ADD | SUB) term)*

term: primary ((MUL | DIV) primary)*

primary: NUMBER
       | CHINESE_NUM
       | IDENTIFIER
       | STRING

// 终结符
DEFINE: "定义"
EQUALS_KW: "等于"
ADD: "加"
SUB: "减"
MUL: "乘"
DIV: "除"
DOT: "。"

IDENTIFIER: /__IDENTIFIER__/
NUMBER: /__NUMBER__/
CHINESE_NUM: /__CHINESE_NUM__/
STRING: /__STRING__/

%ignore /\s+/
"""


# =============================================================================
# 简化的解析器（直接使用 Token 流）
# =============================================================================

class DuanParser:
    """段言解析器：使用自定义词法分析器"""
    
    def __init__(self):
        self.lexer = Lexer()
    
    def parse(self, source: str) -> dict:
        """解析段言代码"""
        # 词法分析
        tokens = self.lexer.tokenize(source)
        
        # 转换为列表以便调试
        token_list = list(tokens)
        
        # 打印 Token 流
        print("\n=== Token 流 ===")
        for tok in token_list:
            print(f"  {tok.type.name}: {tok.value!r}")
        
        # 递归下降解析
        self.tokens = [t for t in token_list if t.type not in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT, TokenType.EOF)]
        self.pos = 0
        
        return self._parse_module()
    
    def _current(self) -> Optional[Any]:
        """获取当前 Token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _peek(self, offset: int = 0) -> Optional[Any]:
        """查看指定位置的 Token"""
        idx = self.pos + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def _consume(self, expected_type=None, expected_value=None) -> Any:
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
    
    def _parse_module(self) -> dict:
        """解析模块"""
        statements = []
        
        while self._current():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return {
            'type': 'Module',
            'statements': statements
        }
    
    def _parse_statement(self) -> Optional[dict]:
        """解析语句"""
        tok = self._current()
        
        if tok and tok.type == TokenType.KEYWORD:
            if tok.value == '定义':
                return self._parse_var_decl()
        
        return None
    
    def _parse_var_decl(self) -> dict:
        """解析变量声明"""
        # 定义
        self._consume(TokenType.KEYWORD, '定义')
        
        # 标识符
        name_tok = self._consume(TokenType.IDENTIFIER)
        name = name_tok.value
        
        # 等于
        self._consume(TokenType.KEYWORD, '等于')
        
        # 表达式
        value = self._parse_expr()
        
        # 句号
        self._consume(TokenType.DOT)
        
        return {
            'type': 'VarDecl',
            'name': name,
            'value': value
        }
    
    def _parse_expr(self) -> dict:
        """解析表达式"""
        left = self._parse_term()
        
        while self._current():
            tok = self._current()
            if tok.type == TokenType.KEYWORD and tok.value in ('加', '减'):
                op = self._consume().value
                right = self._parse_term()
                
                op_map = {'加': '+', '减': '-'}
                left = {
                    'type': 'BinaryOp',
                    'operator': op_map.get(op, op),
                    'left': left,
                    'right': right
                }
            else:
                break
        
        return left
    
    def _parse_term(self) -> dict:
        """解析项"""
        left = self._parse_primary()
        
        while self._current():
            tok = self._current()
            if tok.type == TokenType.KEYWORD and tok.value in ('乘', '除'):
                op = self._consume().value
                right = self._parse_primary()
                
                op_map = {'乘': '*', '除': '/'}
                left = {
                    'type': 'BinaryOp',
                    'operator': op_map.get(op, op),
                    'left': left,
                    'right': right
                }
            else:
                break
        
        return left
    
    def _parse_primary(self) -> dict:
        """解析基本表达式"""
        tok = self._current()
        
        if tok is None:
            raise SyntaxError("意外的输入结束")
        
        if tok.type == TokenType.NUMBER:
            self._consume()
            return {
                'type': 'NumberLiteral',
                'value': tok.value
            }
        
        elif tok.type == TokenType.CHINESE_NUM:
            self._consume()
            return {
                'type': 'NumberLiteral',
                'value': tok.value
            }
        
        elif tok.type == TokenType.IDENTIFIER:
            self._consume()
            return {
                'type': 'Identifier',
                'name': tok.value
            }
        
        elif tok.type == TokenType.STRING:
            self._consume()
            return {
                'type': 'StringLiteral',
                'value': tok.value
            }
        
        else:
            raise SyntaxError(f"意外的 Token: {tok.type} = {tok.value}")


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言最终集成解析器测试（无空格分词）")
    print("=" * 60)
    
    test_cases = [
        # 无空格变量声明
        ('无空格变量声明', '定义甲等于三。'),
        
        # 无空格运算
        ('无空格运算', '定义丙等于三加五。'),
        
        # 带空格的传统语法
        ('带空格语法', '定义 甲 等于 三。'),
        
        # 复杂表达式
        ('复杂表达式', '定义戊等于甲加乙乘丙。'),
    ]
    
    parser = DuanParser()
    
    passed = 0
    failed = 0
    
    for name, test_code in test_cases:
        print(f"\n--- 测试: {name} ---")
        print(f"代码: {test_code}")
        
        try:
            result = parser.parse(test_code)
            print(f"[OK] 解析成功")
            print(f"  类型: {result.get('type')}")
            if result.get('statements'):
                print(f"  语句数: {len(result['statements'])}")
                for i, stmt in enumerate(result['statements']):
                    print(f"  语句{i+1}: {stmt.get('type')} - {stmt.get('name')}")
                    if stmt.get('value'):
                        val = stmt['value']
                        print(f"    值类型: {val.get('type')}")
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
