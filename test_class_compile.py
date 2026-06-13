#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser')
sys.path.insert(0, 'src')

from antlr4 import InputStream, CommonTokenStream
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder
from code_generator_unified import UnifiedCodeGenerator

# 测试类定义
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

print("=== 测试类定义编译 ===")
print("源代码:")
print(code)

try:
    # 创建词法分析器和解析器
    input_stream = InputStream(code)
    lexer = DuanLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = DuanLangParser(token_stream)
    
    # 解析
    tree = parser.program()
    
    if parser.getNumberOfSyntaxErrors() > 0:
        print("\n解析失败!")
        sys.exit(1)
    
    # 构建AST
    builder = DuanLangASTBuilder()
    module = builder.visitProgram(tree)
    
    # 生成代码
    generator = UnifiedCodeGenerator()
    python_code = generator.generate(module)
    
    print("\n生成的Python代码:")
    print(python_code)
    
    # 执行代码
    print("\n执行结果:")
    exec(python_code)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
