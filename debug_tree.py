#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')
sys.path.insert(0, 'antlrparser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser

# 测试代码
code = """返回 "你好，" 加 姓名 加 "！"。"""

print("=== 调试返回语句解析 ===")
print("源代码:", repr(code))

# 创建词法分析器
input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)

# 创建 token 流
token_stream = CommonTokenStream(lexer)

# 创建解析器
parser = DuanLangParser(token_stream)

print("\n--- 开始解析 ---")
tree = parser.returnStmt()
print("解析成功!")

# 打印解析树结构
def print_tree(node, indent=0):
    prefix = "  " * indent
    node_type = type(node).__name__
    if hasattr(node, 'getText'):
        text = node.getText()[:50]  # 限制文本长度
        print(f"{prefix}{node_type}: {repr(text)}")
    else:
        print(f"{prefix}{node_type}")
    
    if hasattr(node, 'getChildren'):
        for child in node.getChildren():
            print_tree(child, indent + 1)

print("\n--- 解析树结构 ---")
print_tree(tree)