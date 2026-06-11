#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser

source = "定义 某人 等于 新 人()。"

# 使用标准 ANTLR 解析器
input_stream = InputStream(source)
lexer = DuanLangLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = DuanLangParser(token_stream)

# 解析
tree = parser.program()

# 打印解析树
print("解析树:")
print(tree.toStringTree(recog=parser))