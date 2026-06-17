#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer

# 测试代码
code = "类 狗:"

print("=== 测试词法分析器 ===")
print("输入:", repr(code))

# 创建词法分析器
input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)

# 获取所有 tokens
tokens = []
while True:
    token = lexer.nextToken()
    if token.type == Token.EOF:
        break
    tokens.append((token.type, token.text, lexer.symbolicNames[token.type]))

print("\nTokens:")
for t in tokens:
    print(f"  类型={t[2]} (ID={t[0]}), 值={repr(t[1])}")

# 打印所有 token 类型定义
print("\nToken 类型定义:")
for name in dir(lexer):
    if name.isupper() and not name.startswith('_'):
        val = getattr(lexer, name)
        if isinstance(val, int):
            print(f"  {name} = {val}")
