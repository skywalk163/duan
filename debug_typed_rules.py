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

print("=== 调试 getTypedRuleContexts ===")

# 创建词法分析器
input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)

# 创建 token 流
token_stream = CommonTokenStream(lexer)

# 创建解析器
parser = DuanLangParser(token_stream)

# 解析
tree = parser.returnStmt()
expr_ctx = tree.expr()
pipeline_ctx = expr_ctx.getChild(0)
and_ctx = pipeline_ctx.getChild(0)

print(f"and_ctx 类型: {type(and_ctx).__name__}")

# 检查不同的引用方式
print(f"\n使用 parser.OrExprContext: {and_ctx.getTypedRuleContexts(parser.OrExprContext)}")
print(f"使用 DuanLangParser.OrExprContext: {and_ctx.getTypedRuleContexts(DuanLangParser.OrExprContext)}")

# 检查子节点
print(f"\nand_ctx.getChildren():")
for child in and_ctx.getChildren():
    print(f"  {type(child).__name__}: {child.getText()[:30]}")