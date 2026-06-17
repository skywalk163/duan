#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder

# 测试代码
code = "新建 狗(\"旺财\")"

print("=== 测试新建表达式解析 ===")

input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = DuanLangParser(token_stream)

# 打印token流
print("Token 流:")
token_stream.fill()
for i, token in enumerate(token_stream.tokens):
    if token.type == -1:
        continue
    token_type = DuanLangParser.symbolicNames[token.type]
    print(f"{i}: '{token.text}' -> {token_type}")

# 解析
tree = parser.primary()
print(f"\n解析树: {tree.toStringTree(recog=parser)}")

# 使用Visitor
visitor = DuanLangASTBuilder()
result = visitor.visitPrimary(tree)
print(f"\nAST节点类型: {type(result).__name__}")
print(f"AST节点: {result}")

# 检查是否有K_NEW子节点
print("\n检查子节点:")
for child in tree.getChildren():
    if hasattr(child, 'symbol'):
        token_type = DuanLangParser.symbolicNames[child.symbol.type]
        print(f"  子节点: '{child.getText()}' -> {token_type}")
    else:
        print(f"  子节点: {type(child).__name__}")

# 检查ctx.K_NEW()是否存在
print(f"\nctx.K_NEW(): {tree.K_NEW()}")
print(f"ctx.ID(): {tree.ID()}")
