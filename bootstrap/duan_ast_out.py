# 由段言编译器生成
# 源文件: 段言代码

# 导入段言标准库
import sys
import os
import asyncio

try:
    import importlib.util
except ImportError:
    importlib = None

try:
    _duan_stdlib = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdlib')
except NameError:
    _duan_stdlib = os.path.join(os.getcwd(), 'stdlib')
    if not os.path.isdir(_duan_stdlib):
        parent_stdlib = os.path.normpath(os.path.join(os.getcwd(), '..', 'stdlib'))
        if os.path.isdir(parent_stdlib):
            _duan_stdlib = parent_stdlib

if os.path.isdir(_duan_stdlib) and _duan_stdlib not in sys.path:
    sys.path.insert(0, _duan_stdlib)

if importlib:
    try:
        _duan_builtin_path = os.path.join(_duan_stdlib, 'builtins.py')
        if os.path.isfile(_duan_builtin_path):
            spec = importlib.util.spec_from_file_location('duan_builtins', _duan_builtin_path)
            _duan_builtin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_duan_builtin)
        else:
            raise ImportError()
    except:
        import types
        _duan_builtin = types.ModuleType('_duan_builtin')
        _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()
        _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None
        _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)
        _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)
        _duan_builtin.打印 = print
        _duan_builtin.列表创建 = list
        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
        _duan_builtin.列表包含 = lambda lst, item: item in lst
        _duan_builtin.字符串长度 = len
        _duan_builtin.字典创建 = dict
        _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
        _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)
else:
    import types
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.打印 = print

def make_program(stmt_list):
    列追加(node, 'program')
    列追加(node, stmt_list)
    return node

def make_paragraph_def(name, params, body):
    列追加(node, 'paragraph_def')
    列追加(node, name)
    列追加(node, params)
    列追加(node, body)
    return node

def make_var_decl(var_name, value):
    列追加(node, 'var_decl')
    列追加(node, var_name)
    列追加(node, value)
    return node

def make_assign(var_name, value):
    列追加(node, 'assign')
    列追加(node, var_name)
    列追加(node, value)
    return node

def make_compound_assign(var_name, op, value):
    列追加(node, 'compound_assign')
    列追加(node, var_name)
    列追加(node, op)
    列追加(node, value)
    return node

def make_if_stmt(cond, body, elif_branches, else_body):
    列追加(node, 'if_stmt')
    列追加(node, cond)
    列追加(node, body)
    列追加(node, elif_branches)
    列追加(node, else_body)
    return node

def make_while_loop(cond, body):
    列追加(node, 'while_loop')
    列追加(node, cond)
    列追加(node, body)
    return node

def make_for_each(var_name, collection, body):
    列追加(node, 'for_each')
    列追加(node, var_name)
    列追加(node, collection)
    列追加(node, body)
    return node

def make_return(value):
    列追加(node, 'return')
    列追加(node, value)
    return node

def make_break():
    列追加(node, 'break')
    return node

def make_continue():
    列追加(node, 'continue')
    return node

def make_print(value):
    列追加(node, 'print')
    列追加(node, value)
    return node

def make_expr_stmt(expr):
    列追加(node, 'expr_stmt')
    列追加(node, expr)
    return node

def make_identifier(name):
    列追加(node, 'identifier')
    列追加(node, name)
    return node

def make_number(value):
    列追加(node, 'number')
    列追加(node, value)
    return node

def make_string(value):
    列追加(node, 'string')
    列追加(node, value)
    return node

def make_boolean(value):
    列追加(node, 'boolean')
    列追加(node, value)
    return node

def make_null():
    列追加(node, 'null')
    return node

def make_binary_op(op, left, right):
    列追加(node, 'binary_op')
    列追加(node, op)
    列追加(node, left)
    列追加(node, right)
    return node

def make_unary_op(op, operand):
    列追加(node, 'unary_op')
    列追加(node, op)
    列追加(node, operand)
    return node

def make_func_call(func_name, args):
    列追加(node, 'func_call')
    列追加(node, func_name)
    列追加(node, args)
    return node

def make_member_access(object, prop_name):
    列追加(node, 'member_access')
    列追加(node, object)
    列追加(node, prop_name)
    return node

def node_type(node):
    return 列获取(node, 0)

def node_data(node, index):
    return 列获取(node, index)
