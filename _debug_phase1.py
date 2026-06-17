"""调试 Python 后端解析 - 详细"""
import sys, os
sys.path.insert(0, 'src')
sys.path.insert(0, '.')

from lexer import Lexer
from duan_parser_v3 import DuanParser

# 调试1: 函数定义
src = '函数 平方 输入 数值：返回 数值 乘 数值'
print('=== 测试: 函数 平方 输入 数值 ===')
print(f'源码: {src}')
print(f'长度: {len(src)} chars')

lexer = Lexer(src)
tokens = lexer.tokenize()
print('Tokens:')
for t in tokens:
    print(f'  {t.type.name:15s} {repr(t.value):20s} L{t.line}:C{t.col}')

parser = DuanParser()
try:
    module = parser.parse(src)
    if module:
        print(f'解析成功! {len(module.statements)} statements')
        for s in module.statements:
            print(f'  {type(s).__name__}: {s}')
            if hasattr(s, 'body') and s.body:
                for b in s.body:
                    print(f'    body: {type(b).__name__}: {b}')
    else:
        print('解析返回 None')
except Exception as e:
    print(f'解析失败: {e}')
    import traceback
    traceback.print_exc()

# 调试2: 用句号结尾
print()
src2 = '函数 平方 输入 数值：返回 数值 乘 数值。'
print('=== 测试: 加句号 ===')
lexer2 = Lexer(src2)
tokens2 = lexer2.tokenize()
for t in tokens2:
    print(f'  {t.type.name:15s} {repr(t.value):20s} L{t.line}:C{t.col}')

parser2 = DuanParser()
try:
    module2 = parser2.parse(src2)
    if module2:
        print(f'解析成功! {len(module2.statements)} statements')
        for s in module2.statements:
            print(f'  {type(s).__name__}: {s}')
    else:
        print('解析返回 None')
except Exception as e:
    print(f'解析失败: {e}')