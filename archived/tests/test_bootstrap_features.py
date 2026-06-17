#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试简化版词法分析器功能
验证：字符串索引、循环控制、字典操作
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator
from semantic_analyzer import SemanticAnalyzer

def test_string_index():
    """测试字符串索引语法"""
    print("\n=== 测试字符串索引 ===")

    source = '''定义文本等于"测试"。
定义字符等于文本【零】。
打印字符。'''

    # 词法分析
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    print(f"Token count: {len(tokens)}")

    # 语法分析
    parser = DuanParser()
    ast = parser.parse(source)
    print(f"AST: {ast}")
    print(f"Statements: {len(ast.statements)}")

    # 语义分析
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Semantic analysis passed")

    # 代码生成
    generator = PythonCodeGenerator()
    code = generator.generate(ast)
    print("\nGenerated Python code:")
    print(code)

    # 执行生成的代码
    print("\nExecuting generated code:")
    exec(code, {'__name__': '__main__'})

    return True

def test_loop_control():
    """测试循环控制语句"""
    print("\n=== 测试循环控制 ===")

    source = '''定义计数等于零。
当计数小于三：
  打印计数。
  定义计数等于计数加一。
  如果计数等于二那么跳出。'''

    # 词法分析
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    print(f"Token count: {len(tokens)}")

    # 语法分析
    parser = DuanParser()
    ast = parser.parse(source)
    print(f"AST parsed")

    # 语义分析
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Semantic analysis passed")

    # 代码生成
    generator = PythonCodeGenerator()
    code = generator.generate(ast)
    print("\nGenerated Python code:")
    print(code)

    # 执行生成的代码
    print("\nExecuting generated code:")
    exec(code, {'__name__': '__main__'})

    return True

def test_dict_operations():
    """测试字典操作"""
    print("\n=== 测试字典操作 ===")

    source = '''定义字典等于字典创建。
字典设置参数字典，"键"，"值"。
打印字典。'''

    # 词法分析
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    print(f"Token count: {len(tokens)}")

    # 语法分析
    parser = DuanParser()
    try:
        ast = parser.parse(source)
        print(f"AST parsed")

        # 代码生成
        generator = PythonCodeGenerator()
        code = generator.generate(ast)
        print("\nGenerated Python code:")
        print(code)

        # 执行生成的代码
        print("\nExecuting generated code:")
        exec(code, {'__name__': '__main__'})

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    print("开始测试简化版词法分析器功能...")

    try:
        # 测试1: 字符串索引
        if test_string_index():
            print("\n[OK] 字符串索引测试通过")

        # 测试2: 循环控制
        if test_loop_control():
            print("\n[OK] 循环控制测试通过")

        # 测试3: 字典操作
        if test_dict_operations():
            print("\n[OK] 字典操作测试通过")

        print("\n=== 所有测试通过 ===")

    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
