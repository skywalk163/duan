"""
段言（Duan）编程语言 - 基于 Lark 的解析器（简化版）

使用 Lark 解析器实现词法分析和语法解析
"""

from lark import Lark, Token, Tree, Transformer
from typing import Any


def unwrap_tree(item):
    """递归展开 Tree 对象"""
    if isinstance(item, Tree):
        # 递归处理 Tree 的子节点
        children = [unwrap_tree(child) for child in item.children]
        # 如果只有一个子节点且是 dict，直接返回它
        if len(children) == 1 and isinstance(children[0], dict):
            return children[0]
        # 否则返回带有规则名的结构
        return {'rule': item.data, 'children': children}
    elif isinstance(item, list):
        return [unwrap_tree(i) for i in item]
    else:
        return item


# =============================================================================
# 段言语法（简化版 EBNF）
# =============================================================================

DUAN_GRAMMAR = r"""
// 起始规则
start: statement*

// 语句（每行一句，以句号结尾）
statement: var_decl
         | if_stmt
         | segment_def
         | expr_stmt

// 变量声明：定义 甲 等于 三。
var_decl: "定义" IDENTIFIER "等于" expr "。"

// 条件语句：如果 甲 大于 乙 那么：...否则：...
if_stmt: "如果" expr "那么" ":" block else_clause?

else_clause: "否则" ":" block

// 代码块（缩进）
block: INDENT statement* DEDENT

// 段落定义：《函数名》段(参数): ...
segment_def: "《" IDENTIFIER "》" "段" "(" params? ")" ":" block

params: param ("," param)*
param: IDENTIFIER (":" IDENTIFIER)?

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

// 终结符：中文运算符（必须定义在 IDENTIFIER 之前）
ADD: "加"
SUB: "减"
MUL: "乘"
DIV: "除"

GT: "大于"
LT: "小于"
EQ: "等于"
NE: "不等于"

// 其他符号
comp_op: ">" | "<" | "=" | "≥" | "≤" | "≠" | GT | LT | EQ | NE

// 标识符（排除所有关键字和运算符）
IDENTIFIER: /[^\s\-\+\*\/\%\=\!\>\<\(\)\[\]\{\}\,\.\;\:\'\"\《\》\【\】\u3002\uFF0C\uFF1A]+/

// 字面量
NUMBER: /-?\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'/

// 缩进标记（由 Lark 的 Indenter 自动生成）
%declare INDENT DEDENT

// 忽略空白
%ignore /[ \t]+/
%ignore /\#.*/

// 换行
%ignore /\r?\n/
"""


class DuanTransformer(Transformer):
    """将解析树转换为 AST"""
    
    def start(self, items):
        return {'type': 'Module', 'statements': list(items)}
    
    def statement(self, items):
        """将 statement 规则展开"""
        if len(items) == 1:
            return items[0]
        return {'type': 'Statement', 'children': items}
    
    def expr(self, items):
        """将 expr 规则展开"""
        if len(items) == 1:
            return items[0]
        return {'type': 'Expr', 'children': items}
    
    def var_decl(self, items):
        # items[0] 是 IDENTIFIER，已经被 IDENTIFIER 方法转换成 dict
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else name_item.value
        
        return {
            'type': 'VarDecl',
            'name': name,
            'value': items[1]
        }
    
    def if_stmt(self, items):
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
        return items[0] if items else []
    
    def block(self, items):
        return list(items)
    
    def segment_def(self, items):
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else name_item.value
        
        return {
            'type': 'SegmentDef',
            'name': name,
            'parameters': items[1] if len(items) > 1 and isinstance(items[1], list) else [],
            'body': items[-1] if items else []
        }
    
    def params(self, items):
        return list(items)
    
    def param(self, items):
        name_item = items[0]
        name = name_item['name'] if isinstance(name_item, dict) else name_item.value
        
        type_item = items[1] if len(items) > 1 else None
        type_name = type_item['name'] if isinstance(type_item, dict) else (type_item.value if type_item else None)
        
        return {
            'name': name,
            'type': type_name
        }
    
    def expr_stmt(self, items):
        return {
            'type': 'ExprStmt',
            'expression': items[0]
        }
    
    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        for i in range(1, len(items), 2):
            result = {
                'type': 'BinaryOp',
                'operator': items[i],
                'left': result,
                'right': items[i + 1]
            }
        return result
    
    def comp_op(self, items):
        op = items[0]
        op_val = op.value if hasattr(op, 'value') else op
        
        # 中文比较运算符映射
        op_map = {
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
        }
        
        return op_map.get(op_val, op_val)
    
    def add_expr(self, items):
        if len(items) == 1:
            return items[0]
        
        # items 结构：[左操作数, ADD/SUB, 右操作数, ...]
        result = items[0]
        i = 1
        while i < len(items):
            if i + 1 >= len(items):
                break
            
            op = items[i]
            op_val = op.value if hasattr(op, 'value') else str(op)
            
            # 中文运算符映射
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
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        i = 1
        while i < len(items):
            if i + 1 >= len(items):
                break
            
            op = items[i]
            op_val = op.value if hasattr(op, 'value') else str(op)
            
            # 中文运算符映射
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
        if len(items) == 1:
            return items[0]
        return {
            'type': 'UnaryOp',
            'operator': '-',
            'operand': items[0]
        }
    
    def primary(self, items):
        return items[0]
    
    def NUMBER(self, token):
        value = token.value
        return {
            'type': 'NumberLiteral',
            'value': float(value) if '.' in value else int(value)
        }
    
    def STRING(self, token):
        value = token.value
        return {
            'type': 'StringLiteral',
            'value': value[1:-1]  # 移除引号
        }
    
    def IDENTIFIER(self, token):
        return {
            'type': 'Identifier',
            'name': token.value
        }


def create_parser():
    """创建段言解析器"""
    return Lark(
        DUAN_GRAMMAR,
        parser='lalr',
        transformer=DuanTransformer(),
        # 使用 Indenter 处理缩进
        postlex=None  # 简化版暂时不用 Indenter
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
        '定义 甲 等于 三。',
        '定义 乙 等于 五。',
        '定义 丙 等于 三 加 五。',
        '定义 丁 等于 十 减 二。',
        '定义 戊 等于 甲 大于 乙。',
        '定义 己 等于 三 乘 四。',
        '定义 庚 等于 十二 除 三。',
    ]
    
    print("=" * 60)
    print("段言 Lark 解析器测试")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test_code in enumerate(test_cases, 1):
        try:
            parser = create_parser()
            result = parser.parse(test_code)
            
            print(f"\n[OK] 测试 {i} 成功: {test_code}")
            
            # 简化输出：只打印关键信息
            if result['statements']:
                stmt = result['statements'][0]
                if isinstance(stmt, dict):
                    print(f"  类型: {stmt.get('type')}")
                    if stmt.get('type') == 'VarDecl':
                        print(f"  变量名: {stmt.get('name')}")
                        value = stmt.get('value')
                        if isinstance(value, dict):
                            print(f"  值类型: {value.get('type')}")
                            if value.get('type') == 'BinaryOp':
                                print(f"  运算符: {value.get('operator')}")
                            elif value.get('type') == 'Identifier':
                                print(f"  值: {value.get('name')}")
            
            passed += 1
        except Exception as e:
            print(f"\n[FAIL] 测试 {i} 失败: {test_code}")
            print(f"  错误: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
