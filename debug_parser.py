#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser

# 测试代码
code = "类 狗:"

print("=== 调试解析器 ===")
print("源代码:", repr(code))

# 创建词法分析器
input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)

# 打印 token 流
print("\n--- Token 流 ---")
lexer2 = DuanLangLexer(InputStream(code))
while True:
    token = lexer2.nextToken()
    if token.type == Token.EOF:
        break
    print(f"Token: {lexer.symbolicNames[token.type]} ({token.type}) = {repr(token.text)}")

# 创建 token 流
token_stream = CommonTokenStream(lexer)

# 创建解析器
parser = DuanLangParser(token_stream)

print("\n--- 开始解析 ---")
try:
    tree = parser.classDef()
    print("解析成功!")
except Exception as e:
    print(f"解析失败: {e}")
    
# 打印 Parser 和 Lexer 的 token 定义对比
print("\n--- Token 定义对比 ---")
print(f"Lexer COLON = {lexer.COLON}")
print(f"Parser COLON = {parser.COLON}")
print(f"Lexer ID = {lexer.ID}")
print(f"Parser ID = {parser.ID}")
print(f"Lexer K_CLASS = {lexer.K_CLASS}")
print(f"Parser K_CLASS = {parser.K_CLASS}")
