#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'antlrparser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder

# 测试1：单行
code1 = '设 甲 为 10。'
print("=== 测试1：单行 ===")
input_stream = InputStream(code1)
lexer = DuanLangLexer(input_stream)
tokens = CommonTokenStream(lexer)
parser = DuanLangParser(tokens)
tree = parser.program()
print(f"Parse tree: {tree.toStringTree(recog=parser)[:100]}")

# 测试2：多行（换行符）
code2 = '''设 甲 为 10。
打印 甲。'''
print("\n=== 测试2：多行 ===")
input_stream = InputStream(code2)
lexer = DuanLangLexer(input_stream)
tokens = CommonTokenStream(lexer)
parser = DuanLangParser(tokens)
tree = parser.program()
print(f"Parse tree: {tree.toStringTree(recog=parser)[:100]}")

# 测试3：从parse_source
print("\n=== 测试3：parse_source ===")
from duan_visitor import parse_source
module = parse_source(code2)
if module:
    print(f"成功，语句数: {len(module.statements)}")
else:
    print("失败")
