#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')
sys.path.insert(0, 'antlrparser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder

# 测试代码
code = """段落 问候 接收 姓名:
    返回 "你好，" 加 姓名 加 "！"。
结束。"""

print("=== 调试段落定义解析 ===")
print("源代码:\n", code)

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
    tree = parser.methodDef()
    print("解析成功!")
    
    # 使用 Visitor 转换为 AST
    visitor = DuanLangASTBuilder()
    ast = visitor.visitMethodDef(tree)
    print("\n--- AST ---")
    print(f"方法名: {ast.name}")
    print(f"参数: {ast.parameters}")
    print(f"返回类型: {ast.return_type}")
    print(f"方法体: {ast.body}")
    
except Exception as e:
    print(f"解析失败: {e}")