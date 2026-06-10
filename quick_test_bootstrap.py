#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试自举核心功能"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

def test(source, name):
    print(f"\n=== {name} ===")
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    parser = DuanParser()
    ast = parser.parse(source)
    generator = PythonCodeGenerator()
    code = generator.generate(ast)
    print("Generated code:")
    print(code)
    print("Executing...")
    exec(code, {'__name__': '__main__'})
    print("[OK]")

# 测试1: 字符串索引
test('定义文本等于"测试"。定义字符等于文本【零】。打印字符。', "字符串索引")

# 测试2: 循环控制
test('定义甲等于零。当甲小于三：打印甲。定义甲等于甲加一。', "循环")

print("\n=== 所有测试通过 ===")
