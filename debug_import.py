#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')
sys.path.insert(0, 'antlrparser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser

# 导入 duan_visitor 中的 DuanLangParser
from duan_visitor import DuanLangParser as VisitorDuanLangParser

print("=== 检查 DuanLangParser 导入 ===")
print(f"直接导入的 DuanLangParser: {DuanLangParser}")
print(f"从 duan_visitor 导入的 DuanLangParser: {VisitorDuanLangParser}")
print(f"两者是否相同: {DuanLangParser == VisitorDuanLangParser}")

# 检查 OrExprContext
print(f"\n直接导入的 DuanLangParser.OrExprContext: {DuanLangParser.OrExprContext}")
print(f"从 duan_visitor 导入的 DuanLangParser.OrExprContext: {VisitorDuanLangParser.OrExprContext}")
print(f"两者是否相同: {DuanLangParser.OrExprContext == VisitorDuanLangParser.OrExprContext}")