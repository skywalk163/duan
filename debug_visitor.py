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

print("=== 调试 visitAndExpr ===")

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

print(f"expr_ctx 类型: {type(expr_ctx).__name__}")
print(f"pipeline_ctx 类型: {type(pipeline_ctx).__name__}")
print(f"and_ctx 类型: {type(and_ctx).__name__}")

# 检查 getTypedRuleContexts
print(f"\npipeline_ctx.getTypedRuleContexts(AndExprContext): {pipeline_ctx.getTypedRuleContexts(parser.AndExprContext)}")
print(f"and_ctx.getTypedRuleContexts(OrExprContext): {and_ctx.getTypedRuleContexts(parser.OrExprContext)}")

# 获取 or_ctx
or_ctx = and_ctx.getChild(0)
print(f"\nor_ctx 类型: {type(or_ctx).__name__}")
print(f"or_ctx.getTypedRuleContexts(ComparisonExprContext): {or_ctx.getTypedRuleContexts(parser.ComparisonExprContext)}")

# 获取 comparison_ctx
comparison_ctx = or_ctx.getChild(0)
print(f"\ncomparison_ctx 类型: {type(comparison_ctx).__name__}")
print(f"comparison_ctx.getTypedRuleContexts(AdditiveExprContext): {comparison_ctx.getTypedRuleContexts(parser.AdditiveExprContext)}")

# 获取 additive_ctx
additive_ctx = comparison_ctx.getChild(0)
print(f"\nadditive_ctx 类型: {type(additive_ctx).__name__}")
print(f"additive_ctx.getTypedRuleContexts(MultiplicativeExprContext): {additive_ctx.getTypedRuleContexts(parser.MultiplicativeExprContext)}")
print(f"additive_ctx.addOp(): {additive_ctx.addOp()}")