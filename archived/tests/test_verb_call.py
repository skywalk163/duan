#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试动词调用功能"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

def test_verb_call():
    """测试动词调用"""
    print("=== 测试动词调用 ===")

    # 测试1: 无参数动词
    print("\n[1] 无参数动词：字典创建")
    source1 = "定义字典等于字典创建。"

    lexer = Lexer()
    tokens1 = lexer.tokenize(source1)
    print(f"    Tokens: {len(tokens1)}")

    parser = DuanParser()
    ast1 = parser.parse(source1)
    print(f"    AST: {len(ast1.statements)} statements")

    generator = PythonCodeGenerator()
    code1 = generator.generate(ast1)
    print("    Generated code:")
    for line in code1.split('\n')[-5:]:
        print(f"      {line}")

    # 测试2: 单参数动词
    print("\n[2] 单参数动词：打印")
    source2 = "打印\"你好\"。"

    tokens2 = lexer.tokenize(source2)
    print(f"    Tokens: {len(tokens2)}")

    ast2 = parser.parse(source2)
    print(f"    AST: {len(ast2.statements)} statements")

    code2 = generator.generate(ast2)
    print("    Generated code:")
    for line in code2.split('\n')[-3:]:
        print(f"      {line}")

    print("\n[OK] 动词调用测试完成")

if __name__ == '__main__':
    test_verb_call()
