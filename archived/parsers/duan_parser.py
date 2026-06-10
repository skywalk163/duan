"""
段言（Duan）编程语言 - 完整解析器（渐进式实现）

基于 Lark 实现，支持：
- 缩进定义块（决策33）
- 双字关键字（决策27）
- 中文运算符（决策27）
- 管道操作符（决策30）
"""

from lark import Lark, Token, Tree, Transformer
from lark.indenter import Indenter
from typing import Any, List, Optional


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
# 段言语法（渐进式 EBNF）
# =============================================================================

DUAN_GRAMMAR = r"""
// 起始规则
start: _NL* statement*

// 语句
statement: var_decl _NL
         | if_stmt
         | foreach_stmt
         | while_stmt
         | return_stmt
         | expr_stmt _NL

// 变量声明：定义 甲 等于 三。
var_decl: "定义" name "等于" expr

// 条件语句
if_stmt: "如果" expr "那么" ":" _NL _INDENT body _DEDENT else_clause?

else_clause: "否则" ":" _NL _INDENT body _DEDENT

// 循环语句
foreach_stmt: "遍历" name "在" expr ":" _NL _INDENT body _DEDENT

while_stmt: "当" expr ":" _NL _INDENT body _DEDENT

// 返回语句
return_stmt: "返回" expr? _NL

// 代码块
body: statement*

// 表达式语句
expr_stmt: expr

// 名称
name: IDENTIFIER

// 表达式（运算符优先级从低到高）
expr: or_expr

or_expr: and_expr ("或" and_expr)*

and_expr: not_expr ("且" not_expr)*

not_expr: "非" not_expr | comparison

comparison: add_expr (comp_op add_expr)*

add_expr: mul_expr (("加" | "减") mul_expr)*

mul_expr: postfix (("乘" | "除") postfix)*

postfix: primary (call | property_access | index_access)*

// 函数调用
call: "(" args? ")"

args: expr ("," expr)*

// 属性访问（之字结构）
property_access: "之" name

// 索引访问
index_access: "[" expr "]"

primary: NUMBER
       | STRING
       | "真"
       | "假"
       | "空"
       | name
       | "(" expr ")"

// =============================================================================
// 终结符
// =============================================================================

// 换行和缩进
_NL: /(\r?\n[ \t]*)+/

// 比较运算符（必须定义在 IDENTIFIER 之前）
"大于": "大于"
"小于": "小于"
"不等于": "不等于"
"大于等于": "大于等于"
"小于等于": "小于等于"

// 比较运算符规则
comp_op: "大于" | "小于" | "不等于" | "大于等于" | "小于等于" | ">" | "<" | "=" | "≠" | "≥" | "≤"

// 标识符（排除所有关键字）
IDENTIFIER: /[^\s\-\+\*\/\%\=\!\>\<\(\)\[\]\{\}\,\.\;\:\'\"\《\》\【\】\u3002\uFF0C\uFF1A]+/

// 字面量
NUMBER: /-?\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'|「[^」]*」|『[^』]*』/

// 缩进标记
%declare _INDENT _DEDENT

// 忽略注释和空白
%ignore /#[^\n]*/
%ignore /[ \t]+/
"""


# =============================================================================
# AST 转换器
# =============================================================================

class DuanTransformer(Transformer):
    """将解析树转换为 AST"""
    
    def start(self, items):
        """起始规则"""
        items = [item for item in items if item is not None and item != '\n']
        
        return {
            'type': 'Module',
            'statements': items
        }
    
    def var_decl(self, items):
        """变量声明"""
        return {
            'type': 'VarDecl',
            'name': items[0],
            'value': items[1]
        }
    
    def name(self, items):
        """名称"""
        return items[0]
    
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
        return {
            'type': 'ForeachStmt',
            'variable': items[0],
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
    
    def or_expr(self, items):
        """或表达式"""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        for i in range(1, len(items)):
            result = {
                'type': 'BinaryOp',
                'operator': '或',
                'left': result,
                'right': items[i]
            }
        return result
    
    def and_expr(self, items):
        """且表达式"""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        for i in range(1, len(items)):
            result = {
                'type': 'BinaryOp',
                'operator': '且',
                'left': result,
                'right': items[i]
            }
        return result
    
    def not_expr(self, items):
        """非表达式"""
        if len(items) == 1:
            return items[0]
        return {
            'type': 'UnaryOp',
            'operator': '非',
            'operand': items[0]
        }
    
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
    
    def postfix(self, items):
        """后缀表达式"""
        result = items[0]
        
        for item in items[1:]:
            if isinstance(item, dict):
                if item.get('type') == 'Call':
                    result = {
                        'type': 'Call',
                        'function': result,
                        'arguments': item['arguments']
                    }
                elif item.get('type') == 'PropertyAccess':
                    result = {
                        'type': 'PropertyAccess',
                        'object': result,
                        'property': item['property']
                    }
                elif item.get('type') == 'IndexAccess':
                    result = {
                        'type': 'IndexAccess',
                        'object': result,
                        'index': item['index']
                    }
        
        return result
    
    def call(self, items):
        """函数调用"""
        return {
            'type': 'Call',
            'arguments': items[0] if items else []
        }
    
    def args(self, items):
        """参数列表"""
        return list(items)
    
    def property_access(self, items):
        """属性访问"""
        return {
            'type': 'PropertyAccess',
            'property': items[0]
        }
    
    def index_access(self, items):
        """索引访问"""
        return {
            'type': 'IndexAccess',
            'index': items[0]
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
        if value.startswith('"') or value.startswith("'"):
            value = value[1:-1]
        elif value.startswith('「'):
            value = value[1:-1]
        elif value.startswith('『'):
            value = value[1:-1]
        
        return {
            'type': 'StringLiteral',
            'value': value
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
        
        # 循环语句
        ('遍历循环', '''遍历 项 在 列表：
  打印 项。
'''),
        
        # 属性访问
        ('属性访问', '''定义 首 等于 列表 之首。
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
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
