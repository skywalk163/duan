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
code = """返回 "你好，" 加 姓名 加 "！"。"""

print("=== 调试 visitAndExpr 内部 ===")

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

# 检查 getTypedRuleContexts
print(f"\n使用 DuanLangParser.OrExprContext:")
result = and_ctx.getTypedRuleContexts(DuanLangParser.OrExprContext)
print(f"  结果: {result}")
print(f"  结果长度: {len(result)}")

# 检查 DuanLangParser 模块
print(f"\nDuanLangParser 模块: {DuanLangParser}")
print(f"DuanLangParser.OrExprContext: {DuanLangParser.OrExprContext}")

# 检查 parser 实例
print(f"\nparser 实例: {parser}")
print(f"parser.OrExprContext: {parser.OrExprContext}")

# 比较
print(f"\nDuanLangParser.OrExprContext == parser.OrExprContext: {DuanLangParser.OrExprContext == parser.OrExprContext}")