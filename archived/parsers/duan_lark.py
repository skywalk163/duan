"""
段言（Duan）编程语言 - 基于 Lark 的解析器

使用 Lark 解析器实现词法分析和语法解析
"""

from lark import Lark, Token, Tree, Transformer
from lark.indenter import Indenter
from typing import Any


# =============================================================================
# 段言语法（EBNF）
# =============================================================================

DUAN_GRAMMAR = r"""
// 起始规则
start: _NL* (import_stmt | export_stmt | segment_def | type_def | statement)*

// 导入导出
import_stmt: "导入" (segment_name ("," segment_name)* | "从" module_name "导入" segment_name ("," segment_name)*) _END
export_stmt: "导出" segment_name _END

// 段落定义
segment_def: segment_name "段" parameters? ("->" type_name)? ":" _NL _INDENT body _DEDENT

parameters: "(" [parameter ("," parameter)*] ")"
parameter: IDENTIFIER (":" type_name)? ("等于" expr)?

type_def: "类型" IDENTIFIER ":" _NL _INDENT field* _DEDENT
field: IDENTIFIER ":" type_name _NL

type_name: "数" | "整数" | "浮数" | "串" | "列" | "典" | "集" | "布尔" | "空" | "任意" | IDENTIFIER

// 语句
statement: var_decl _END
         | if_stmt
         | foreach_stmt
         | while_stmt
         | "跳出" _END
         | "跳过" _END
         | return_stmt _END
         | expr_stmt _END

var_decl: "定义" IDENTIFIER "等于" expr
if_stmt: "如果" expr "那么" ":" _NL _INDENT body _DEDENT else_clause?
else_clause: "否则" ":" _NL _INDENT body _DEDENT
foreach_stmt: "遍历" IDENTIFIER "在" expr ":" _NL _INDENT body _DEDENT
while_stmt: "当" expr ":" _NL _INDENT body _DEDENT
return_stmt: "返回" expr?

body: statement*

expr_stmt: expr

// 表达式（优先级从低到高）
expr: pipe_expr

pipe_expr: or_expr ("->" or_expr | "并" or_expr)*
         | or_expr ("," or_expr)+  // 中文逗号管道

or_expr: and_expr ("或" and_expr)*
and_expr: not_expr ("且" not_expr)*
not_expr: "非" not_expr | comparison

comparison: add_expr (comp_op add_expr)*
comp_op: "=" | "≠" | "<" | ">" | "≤" | "≥" | "==" | "!=" | "<=" | ">="

add_expr: mul_expr (("+" | "-") mul_expr)*
mul_expr: unary (("*" | "×" | "/" | "÷" | "%") unary)*
unary: "-" unary | postfix

postfix: primary (call | property_access | index_access)*
call: "(" [expr ("," expr)*] ")"
property_access: "之" IDENTIFIER
index_access: "[" expr "]"

primary: NUMBER
       | STRING
       | "真"
       | "假"
       | "空"
       | segment_name
       | list_literal
       | IDENTIFIER
       | "(" expr ")"

list_literal: "[" [expr ("," expr)*] "]"

// 名称
segment_name: "《" IDENTIFIER "》"
module_name: "【" IDENTIFIER "】"

// 终结符
IDENTIFIER: /[^\s\-\+\*\/\%\=\!\>\<\(\)\[\]\{\}\,\.\;\:\'\"\《\》\【\】]+/
NUMBER: /-?\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'|「[^」]*」|『[^』]*』/

_END: /。|\./  // 句号作为语句结束

// 忽略空白（由 Indenter 处理）
%ignore /[ \t]+/

// 注释
_COMMENT: /#.*/

// 换行和缩进（由 Indenter 处理）
_NL: /(\r?\n)+/
_INDENT: "INDENT"
_DEDENT: "DEDENT"
"""


class DuanIndenter(Indenter):
    """段言缩进处理器"""
    
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


class DuanTransformer(Transformer):
    """将解析树转换为 AST"""
    
    def start(self, items):
        return {
            'type': 'Module',
            'imports': [item for item in items if item.get('type') == 'Import'],
            'exports': [item for item in items if item.get('type') == 'Export'],
            'segments': [item for item in items if item.get('type') == 'SegmentDef'],
            'types': [item for item in items if item.get('type') == 'TypeDef'],
            'statements': [item for item in items if item.get('type') not in 
                          {'Import', 'Export', 'SegmentDef', 'TypeDef'}]
        }
    
    def import_stmt(self, items):
        if len(items) == 1:
            # 导入 段名
            return {'type': 'Import', 'module': '', 'names': [items[0]]}
        else:
            # 导入 从 模块 段名
            return {'type': 'Import', 'module': items[0], 'names': items[1:]}
    
    def export_stmt(self, items):
        return {'type': 'Export', 'name': items[0]}
    
    def segment_def(self, items):
        name = items[0]
        params = items[1] if len(items) > 1 and isinstance(items[1], list) else []
        return_type = None
        body = []
        
        for item in items[1:]:
            if isinstance(item, dict):
                if item.get('type') == 'ReturnType':
                    return_type = item['value']
                elif item.get('type') == 'Body':
                    body = item['statements']
        
        return {
            'type': 'SegmentDef',
            'name': name,
            'parameters': params,
            'return_type': return_type,
            'body': body
        }
    
    def parameters(self, items):
        return list(items)
    
    def parameter(self, items):
        name = items[0]
        type_name = None
        default = None
        
        for item in items[1:]:
            if isinstance(item, str):
                type_name = item
            else:
                default = item
        
        return {
            'type': 'Parameter',
            'name': name,
            'type': type_name,
            'default': default
        }
    
    def type_name(self, items):
        return items[0]
    
    def type_def(self, items):
        name = items[0]
        fields = items[1:]
        return {
            'type': 'TypeDef',
            'name': name,
            'fields': fields
        }
    
    def field(self, items):
        return {'name': items[0], 'type': items[1]}
    
    def var_decl(self, items):
        return {
            'type': 'VarDecl',
            'name': items[0],
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
        return items[0]
    
    def foreach_stmt(self, items):
        return {
            'type': 'ForeachStmt',
            'variable': items[0],
            'iterable': items[1],
            'body': items[2]
        }
    
    def while_stmt(self, items):
        return {
            'type': 'WhileStmt',
            'condition': items[0],
            'body': items[1]
        }
    
    def return_stmt(self, items):
        return {
            'type': 'ReturnStmt',
            'value': items[0] if items else None
        }
    
    def body(self, items):
        return {'type': 'Body', 'statements': list(items)}
    
    def expr_stmt(self, items):
        return {
            'type': 'ExprStmt',
            'expression': items[0]
        }
    
    def pipe_expr(self, items):
        if len(items) == 1:
            return items[0]
        
        return {
            'type': 'PipeExpr',
            'expressions': list(items)
        }
    
    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        for i in range(1, len(items), 2):
            result = {
                'type': 'BinaryOp',
                'operator': '或',
                'left': result,
                'right': items[i + 1]
            }
        return result
    
    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        for i in range(1, len(items), 2):
            result = {
                'type': 'BinaryOp',
                'operator': '且',
                'left': result,
                'right': items[i + 1]
            }
        return result
    
    def not_expr(self, items):
        if len(items) == 1:
            return items[0]
        return {
            'type': 'UnaryOp',
            'operator': '非',
            'operand': items[0]
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
        return items[0]
    
    def add_expr(self, items):
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
    
    def mul_expr(self, items):
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
    
    def unary(self, items):
        if len(items) == 1:
            return items[0]
        return {
            'type': 'UnaryOp',
            'operator': '-',
            'operand': items[0]
        }
    
    def postfix(self, items):
        result = items[0]
        for item in items[1:]:
            result = {
                'type': item['type'],
                'object': result,
                **{k: v for k, v in item.items() if k != 'type'}
            }
        return result
    
    def call(self, items):
        return {
            'type': 'Call',
            'arguments': list(items)
        }
    
    def property_access(self, items):
        return {
            'type': 'PropertyAccess',
            'property': items[0]
        }
    
    def index_access(self, items):
        return {
            'type': 'IndexAccess',
            'index': items[0]
        }
    
    def primary(self, items):
        return items[0]
    
    def segment_name(self, items):
        return {
            'type': 'SegmentName',
            'name': items[0]
        }
    
    def module_name(self, items):
        return {
            'type': 'ModuleName',
            'name': items[0]
        }
    
    def list_literal(self, items):
        return {
            'type': 'ListLiteral',
            'elements': list(items)
        }
    
    def NUMBER(self, token):
        value = token.value
        return {
            'type': 'NumberLiteral',
            'value': float(value) if '.' in value else int(value)
        }
    
    def STRING(self, token):
        value = token.value
        # 移除引号
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
        return token.value


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
    # 测试代码 - 简化版
    test_code = '''
定义 甲 等于 三。
定义 乙 等于 五。

《加法》段(甲: 数, 乙: 数) -> 数:
  返回 甲。

如果 甲 大于 乙 那么:
  打印 甲。
'''
    
    try:
        parser = create_parser()
        tree = parser.parse(test_code)
        import json
        print(json.dumps(tree, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"解析错误: {e}")
