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

print("=== 调试 visitExpr ===")

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

print(f"expr_ctx 类型: {type(expr_ctx).__name__}")
print(f"expr_ctx.getChild(0) 类型: {type(expr_ctx.getChild(0)).__name__}")

# 创建 Visitor
visitor = DuanLangASTBuilder()

# 测试 visitExpr
print("\n--- 测试 visitExpr ---")
try:
    result = visitor.visitExpr(expr_ctx)
    print(f"visitExpr 结果: {result}")
    print(f"结果类型: {type(result).__name__}")
except Exception as e:
    print(f"visitExpr 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 visitPipelineExpr
print("\n--- 测试 visitPipelineExpr ---")
pipeline_ctx = expr_ctx.getChild(0)
try:
    result = visitor.visitPipelineExpr(pipeline_ctx)
    print(f"visitPipelineExpr 结果: {result}")
    print(f"结果类型: {type(result).__name__}")
except Exception as e:
    print(f"visitPipelineExpr 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 visitAndExpr
print("\n--- 测试 visitAndExpr ---")
and_ctx = pipeline_ctx.getChild(0)
try:
    result = visitor.visitAndExpr(and_ctx)
    print(f"visitAndExpr 结果: {result}")
    print(f"结果类型: {type(result).__name__}")
except Exception as e:
    print(f"visitAndExpr 失败: {e}")
    import traceback
    traceback.print_exc()