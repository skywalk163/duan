"""
段言（Duan）编程语言 - 完整解析器（基于已验证版本）

基于 duan_lark_simple.py，添加：
- 缩进定义块（决策33）
- 条件语句（如果...那么...否则...）
- 循环语句（遍历、当）
"""

from lark import Lark, Token, Tree, Transformer
from lark.indenter import Indenter
from typing import Any


# =============================================================================
# 缩进处理器
# =============================================================================

class DuanIndenter(Indenter):
    """段言缩进处理器"""
    
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


# =============================================================================
# 段言语法（完整版 EBNF）
# =============================================================================

DUAN_GRAMMAR = r"""
// 起始规则
start: _NL* statement*

// 语句（每行一句，以句号结尾）
statement: var_decl
         | if_stmt
         | foreach_stmt
         | while_stmt
         | return_stmt
         | expr_stmt

// 变量声明：定义 甲 等于 三。
var_decl: "定义" IDENTIFIER "等于" expr "。"

// 条件语句：如果 甲 大于 乙 那么：...否则：...
if_stmt: "如果" expr "那么" ":" _NL _INDENT body _DEDENT else_clause?

else_clause: "否则" ":" _NL _INDENT body _DEDENT

// 遍历循环
foreach_stmt: "遍历" IDENTIFIER "在" expr ":" _NL _INDENT body _DEDENT

// 当循环
while_stmt: "当" expr ":" _NL _INDENT body _DEDENT

// 返回语句
return_stmt: "返回" expr "。"

// 代码块
body: statement*

// 表达式语句
expr_stmt: expr "。"

// 表达式（运算符优先级从低到高）
expr: comparison

comparison: add_expr (comp_op add_expr)*

add_expr: mul_expr ((ADD | SUB) mul_expr)*

mul_expr: unary ((MUL | DIV) unary)*

unary: "-" unary | primary

primary: NUMBER
       | STRING
       | "真"
       | "假"
       | "空"
       | IDENTIFIER
       | "(" expr ")"

// =============================================================================
// 终结符
// =============================================================================

// 换行和缩进
_NL: /(\r?\n[ \t]*)+/

// 算术运算符（必须定义在 IDENTIFIER 之前）
ADD: "加"
SUB: "减"
MUL: "乘"
DIV: "除"

// 比较运算符
GT: "大于"
LT: "小于"
EQ_COMP: "等于比较"
NE: "不等于"
GE: "大于等于"
LE: "小于等于"

// 比较运算符规则
comp_op: ">" | "<" | "=" | "≠" | "≥" | "≤" | GT | LT | NE | GE | LE

// 标识符（排除所有关键字和运算符）
IDENTIFIER: /[^\s\-\+\*\/\%\=\!\>\<\(\)\[\]\{\}\,\.\;\:\'\"\《\》\【\】\u3002\uFF0C\uFF1A]+/

// 字面量
NUMBER: /-?\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'/

// 缩进标记（由 Indenter 自动生成）
%declare _INDENT _DEDENT

// 忽略空白
%ignore /[ \t]+/
%ignore /#.*/
"""


# =============================================================================
# AST 转换器
# =============================================================================

class DuanTransformer(Transformer):
    """将解析树转换为 AST"""
    
    def start(self, items):
        """起始规则"""
        items = [item for item in items if item is not None and item != '\n']
        return {'type': 'Module', 'statements': list(items)}
    
    def var_decl(self, items):
        """变量声明"""
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else name_item.value
        
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
        name = name_item['name'] if isinstance(name_item, dict) else name_item.value
        
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
        op_val = op.value if hasattr(op, 'value') else str(op)
        
        op_map = {
            '大于': '>',
            '小于': '<',
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
                op_val = op.value if hasattr(op, 'value') else str(op)
                
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
                op_val = op.value if hasattr(op, 'value') else str(op)
                
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
    
    def IDENTIFIER(self, token):
        """标识符"""
        return {
            'type': 'Identifier',
            'name': token.value
        }
    
    def _NL(self, token):
        """换行"""
        return '\n'


# =============================================================================
# 解析器创建
# =============================================================================

def create_parser():
    """创建段言解析器"""
    return Lark(
        DUAN_GRAMMAR,
        parser='lalr',
        postlex=DuanIndenter(),
        transformer=DuanTransformer()
    )


def parse(source: str) -> dict:
    """解析段言代码"""
    parser = create_parser()
    return parser.parse(source)


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    # 测试代码
    test_cases = [
        # 基本变量声明
        ('变量声明', '''定义 甲 等于 三。
定义 乙 等于 五。
定义 丙 等于 三 加 五。
'''),
        
        # 条件语句
        ('条件语句', '''如果 甲 大于 乙 那么：
  打印 甲。
否则：
  打印 乙。
'''),
        
        # 遍历循环
        ('遍历循环', '''遍历 项 在 列表：
  打印 项。
'''),
        
        # 当循环
        ('当循环', '''当 甲 大于 零：
  打印 甲。
  定义 甲 等于 甲 减 一。
'''),
    ]
    
    print("=" * 60)
    print("段言完整解析器测试")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, test_code in test_cases:
        try:
            result = parse(test_code)
            print(f"\n[OK] {name}")
            print(f"  类型: {result.get('type')}")
            
            stats = []
            if result.get('statements'):
                stats.append(f"{len(result['statements'])} 条语句")
            
            if stats:
                print(f"  统计: {', '.join(stats)}")
            
            passed += 1
        except Exception as e:
            print(f"\n[FAIL] {name}")
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
