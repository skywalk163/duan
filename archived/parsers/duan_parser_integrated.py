"""
段言（Duan）编程语言 - 集成解析器

集成自定义词法分析器到 Lark 语法解析器，实现：
- 无空格分词（决策29）
- 双字关键字优先匹配
- 类型切换自动分词

基于：
- src/lexer.py - 自定义词法分析器
- src/duan_parser_v2.py - Lark 语法框架
"""

from lark import Lark, Token, Tree, Transformer
from typing import List, Any, Optional
from lexer import Lexer, LexerError
from tokens import TokenType


# =============================================================================
# Lark 兼容的词法分析器包装器
# =============================================================================

class DuanLexerAdapter:
    """将自定义词法分析器适配为 Lark 兼容接口"""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens: List[Token] = []
        self.pos = 0
    
    def lex(self, source: str) -> List[Token]:
        """执行词法分析，返回 Lark Token 列表"""
        # 使用自定义词法分析器获取 Token
        duan_tokens = self.lexer.tokenize(source)
        
        # 转换为 Lark Token
        lark_tokens = []
        for tok in duan_tokens:
            lark_token = self._convert_token(tok)
            if lark_token:
                lark_tokens.append(lark_token)
        
        return lark_tokens
    
    def _convert_token(self, tok) -> Optional[Token]:
        """将段言 Token 转换为 Lark Token"""
        from tokens import Token as DuanToken
        
        token_type_map = {
            TokenType.NUMBER: 'NUMBER',
            TokenType.STRING: 'STRING',
            TokenType.CHINESE_NUM: 'CHINESE_NUM',
            TokenType.IDENTIFIER: 'IDENTIFIER',
            TokenType.KEYWORD: None,  # 关键字需要特殊处理
            TokenType.DOT: 'DOT',
            TokenType.COMMA: 'COMMA',
            TokenType.SEMICOLON: 'SEMICOLON',
            TokenType.COLON: 'COLON',
            TokenType.LPAREN: 'LPAREN',
            TokenType.RPAREN: 'RPAREN',
            TokenType.LBRACKET: 'LBRACKET',
            TokenType.RBRACKET: 'RBRACKET',
            TokenType.EQUALS: 'EQUALS',
            TokenType.INDENT: '_INDENT',
            TokenType.DEDENT: '_DEDENT',
            TokenType.NEWLINE: '_NL',
            TokenType.EOF: 'EOF',
            TokenType.PIPE: 'PIPE',
        }
        
        if tok.type == TokenType.KEYWORD:
            # 关键字直接使用其值作为 Token 类型
            return Token(tok.value.upper(), tok.value, line=tok.line, column=tok.col)
        elif tok.type == TokenType.OPERATOR:
            # 运算符直接使用其值作为 Token 类型
            op_map = {
                '加': 'ADD',
                '减': 'SUB',
                '乘': 'MUL',
                '除': 'DIV',
                '大于': 'GT',
                '小于': 'LT',
                '等于': 'EQ',
                '不等于': 'NE',
                '大于等于': 'GE',
                '小于等于': 'LE',
            }
            token_type = op_map.get(tok.value, 'OPERATOR')
            return Token(token_type, tok.value, line=tok.line, column=tok.col)
        elif tok.type in token_type_map:
            token_type = token_type_map[tok.type]
            if token_type:
                return Token(token_type, tok.value, line=tok.line, column=tok.col)
        
        return None


# =============================================================================
# 段言语法（集成版 EBNF）
# =============================================================================

DUAN_GRAMMAR_INTEGRATED = r"""
// 起始规则
start: statement*

// 语句
statement: var_decl
         | if_stmt
         | foreach_stmt
         | while_stmt
         | return_stmt
         | expr_stmt

// 变量声明：定义甲等于三。
var_decl: "定义" IDENTIFIER "等于" expr DOT

// 条件语句
if_stmt: "如果" expr "那么" COLON _NL _INDENT body _DEDENT else_clause?

else_clause: "否则" COLON _NL _INDENT body _DEDENT

// 遍历循环
foreach_stmt: "遍历" IDENTIFIER "在" expr COLON _NL _INDENT body _DEDENT

// 当循环
while_stmt: "当" expr COLON _NL _INDENT body _DEDENT

// 返回语句
return_stmt: "返回" expr DOT

// 代码块
body: statement*

// 表达式语句
expr_stmt: expr DOT

// 表达式
expr: comparison

comparison: add_expr (comp_op add_expr)*

add_expr: mul_expr ((ADD | SUB) mul_expr)*

mul_expr: unary ((MUL | DIV) unary)*

unary: SUB unary | primary

primary: NUMBER
       | STRING
       | CHINESE_NUM
       | "真"
       | "假"
       | "空"
       | IDENTIFIER
       | LPAREN expr RPAREN

// 比较运算符
comp_op: GT | LT | EQ | NE | GE | LE

// =============================================================================
// 终结符（由外部词法分析器提供）
// =============================================================================

// 字面量
NUMBER: /-?\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'/
CHINESE_NUM: /[一二三四五六七八九十]+/

// 标识符
IDENTIFIER: /[^\s\-\+\*\/\%\=\!\>\<\(\)\[\]\{\}\,\.\;\:\'\"\《\》\【\】\u3002\uFF0C\uFF1A]+/

// 运算符
ADD: "加"
SUB: "减"
MUL: "乘"
DIV: "除"

// 比较运算符
GT: "大于"
LT: "小于"
EQ: "等于"
NE: "不等于"
GE: "大于等于"
LE: "小于等于"

// 符号
DOT: "。"
COMMA: "，"
SEMICOLON: "；"
COLON: "："
LPAREN: "（"
RPAREN: "）"
LBRACKET: "【"
RBRACKET: "】"
EQUALS: "="
PIPE: "->"

// 结构
_NL: /\n+/
_INDENT: /__INDENT__/
_DEDENT: /__DEDENT__/

// 文件结束
EOF: /__EOF__/

// 忽略空白
%ignore /[ \t\r]+/
"""


# =============================================================================
# AST 转换器
# =============================================================================

class DuanTransformer(Transformer):
    """将解析树转换为 AST"""
    
    def start(self, items):
        """起始规则"""
        items = [item for item in items if item is not None]
        return {'type': 'Module', 'statements': list(items)}
    
    def var_decl(self, items):
        """变量声明"""
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else str(name_item)
        
        return {
            'type': 'VarDecl',
            'name': name,
            'value': items[1]
        }
    
    def if_stmt(self, items):
        """条件语句"""
        condition = items[0]
        then_body = items[1] if len(items) > 1 else []
        else_body = items[2] if len(items) > 2 else None
        
        return {
            'type': 'IfStmt',
            'condition': condition,
            'then_body': then_body,
            'else_body': else_body
        }
    
    def else_clause(self, items):
        """else 子句"""
        return items[0] if items else []
    
    def foreach_stmt(self, items):
        """遍历循环"""
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else str(name_item)
        
        return {
            'type': 'ForeachStmt',
            'variable': name,
            'iterable': items[1],
            'body': items[2]
        }
    
    def while_stmt(self, items):
        """当循环"""
        return {
            'type': 'WhileStmt',
            'condition': items[0],
            'body': items[1]
        }
    
    def return_stmt(self, items):
        """返回语句"""
        return {
            'type': 'ReturnStmt',
            'value': items[0] if items else None
        }
    
    def body(self, items):
        """代码块"""
        statements = [item for item in items if item is not None]
        return {'type': 'Body', 'statements': statements}
    
    def expr_stmt(self, items):
        """表达式语句"""
        return {
            'type': 'ExprStmt',
            'expression': items[0]
        }
    
    def expr(self, items):
        """表达式"""
        if len(items) == 1:
            return items[0]
        return {'type': 'Expr', 'children': items}
    
    def comparison(self, items):
        """比较表达式"""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        i = 1
        while i < len(items):
            if i + 1 < len(items):
                result = {
                    'type': 'BinaryOp',
                    'operator': items[i],
                    'left': result,
                    'right': items[i + 1]
                }
            i += 2
        return result
    
    def comp_op(self, items):
        """比较运算符"""
        op = items[0]
        op_val = str(op)
        
        op_map = {
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '大于等于': '>=',
            '小于等于': '<=',
        }
        
        return op_map.get(op_val, op_val)
    
    def add_expr(self, items):
        """加减表达式"""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        i = 1
        while i < len(items):
            if i + 1 < len(items):
                op = items[i]
                op_val = str(op)
                
                op_map = {'加': '+', '减': '-'}
                op_val = op_map.get(op_val, op_val)
                
                result = {
                    'type': 'BinaryOp',
                    'operator': op_val,
                    'left': result,
                    'right': items[i + 1]
                }
            i += 2
        return result
    
    def mul_expr(self, items):
        """乘除表达式"""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        i = 1
        while i < len(items):
            if i + 1 < len(items):
                op = items[i]
                op_val = str(op)
                
                op_map = {'乘': '*', '除': '/'}
                op_val = op_map.get(op_val, op_val)
                
                result = {
                    'type': 'BinaryOp',
                    'operator': op_val,
                    'left': result,
                    'right': items[i + 1]
                }
            i += 2
        return result
    
    def unary(self, items):
        """一元表达式"""
        if len(items) == 1:
            return items[0]
        return {
            'type': 'UnaryOp',
            'operator': '-',
            'operand': items[0]
        }
    
    def primary(self, items):
        """基本表达式"""
        return items[0]
    
    def NUMBER(self, token):
        """数字"""
        value = token.value
        return {
            'type': 'NumberLiteral',
            'value': float(value) if '.' in value else int(value)
        }
    
    def STRING(self, token):
        """字符串"""
        value = token.value
        return {
            'type': 'StringLiteral',
            'value': value[1:-1]  # 移除引号
        }
    
    def CHINESE_NUM(self, token):
        """中文数字"""
        chinese_to_arabic = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        }
        
        value = token.value
        
        # 简单处理：一到十
        if len(value) == 1:
            num = chinese_to_arabic.get(value, 0)
        else:
            # 复杂中文数字处理（简化版）
            num = 0
            for ch in value:
                if ch in chinese_to_arabic:
                    num = chinese_to_arabic[ch]
                    break
        
        return {
            'type': 'NumberLiteral',
            'value': num
        }
    
    def IDENTIFIER(self, token):
        """标识符"""
        return {
            'type': 'Identifier',
            'name': token.value
        }


# =============================================================================
# 解析器创建
# =============================================================================

def create_integrated_parser():
    """创建集成解析器"""
    lexer = Lexer()
    
    parser = Lark(
        DUAN_GRAMMAR_INTEGRATED,
        parser='lalr',
        transformer=DuanTransformer()
    )
    
    return parser, lexer


def parse(source: str) -> dict:
    """解析段言代码（无空格）"""
    parser, lexer = create_integrated_parser()
    
    # 使用自定义词法分析器
    tokens = lexer.tokenize(source)
    
    # 转换为 Lark Token
    adapter = DuanLexerAdapter(lexer)
    lark_tokens = adapter.lex(source)
    
    # 打印 Token 流（调试）
    print("\n=== Token 流 ===")
    for tok in lark_tokens:
        print(f"  {tok.type}: {tok.value!r}")
    
    # 使用 Lark 解析
    # 注意：这里需要将 Token 流传递给 Lark
    # 由于 Lark 的限制，我们暂时使用字符串解析
    # 后续需要实现完整的 Token 流解析
    
    return parser.parse(source)


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言集成解析器测试（无空格分词）")
    print("=" * 60)
    
    test_cases = [
        # 无空格变量声明
        ('无空格变量声明', '定义甲等于三。'),
        
        # 无空格运算
        ('无空格运算', '定义丙等于三加五。'),
        
        # 带空格的传统语法
        ('带空格语法', '定义 甲 等于 三。'),
        
        # 复杂表达式
        ('复杂表达式', '定义戊等于甲大于乙。'),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_code in test_cases:
        print(f"\n--- 测试: {name} ---")
        print(f"代码: {test_code}")
        
        try:
            result = parse(test_code)
            print(f"[OK] 解析成功")
            print(f"  类型: {result.get('type')}")
            if result.get('statements'):
                print(f"  语句数: {len(result['statements'])}")
                for i, stmt in enumerate(result['statements']):
                    print(f"  语句{i+1}: {stmt.get('type')}")
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
