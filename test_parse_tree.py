#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser/duan_parser')

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from antlr4.tree.Trees import Trees

# 测试代码
code = """类 狗:
    属性 名字。
    
    构造(名字):
        己.名字 = 名字。
    结束。
    
    段落 叫:
        打印(己.名字)。
    结束。
结束。

设 旺财 为 新建 狗("旺财")。
旺财.叫()。
"""

print("=== 测试解析树 ===")
print("源代码:")
print(code)

# 创建解析器
input_stream = InputStream(code)
lexer = DuanLangLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = DuanLangParser(token_stream)

# 获取解析树
tree = parser.program()

# 打印解析树
print("\n解析树:")
print(Trees.toStringTree(tree, None, parser))

# 打印子节点类型
print("\n子节点类型:")
for i, child in enumerate(tree.getChildren()):
    print(f"  {i}: {type(child).__name__}")
    if hasattr(child, 'getText'):
        text = child.getText()
        print(f"      text: {text[:50] if len(text) > 50 else text}")
