#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言自举能力验证测试
测试所有实现简化版词法分析器所需的核心功能
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator
from semantic_analyzer import SemanticAnalyzer

def compile_and_run(source: str, test_name: str):
    """编译并执行段言代码"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    print(f"源代码:\n{source}")

    try:
        # 1. 词法分析
        print("\n[1/5] 词法分析...")
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        print(f"      [OK] Tokens: {len(tokens)}")

        # 2. 语法分析
        print("[2/5] 语法分析...")
        parser = DuanParser()
        ast = parser.parse(source)
        print(f"      [OK] AST: {len(ast.statements)} statements")

        # 3. 语义分析
        print("[3/5] 语义分析...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("[OK] 语义分析通过")

        # 4. 代码生成
        print("[4/5] 代码生成...")
        generator = PythonCodeGenerator()
        code = generator.generate(ast)
        print("      [OK] 代码生成完成")

        # 5. 执行
        print("[5/5] 执行生成的代码...")
        print("-" * 60)
        exec(code, {'__name__': '__main__'})
        print("-" * 60)

        print(f"\n[OK] {test_name} 测试通过")
        return True

    except Exception as e:
        print(f"\n[FAIL] {test_name} 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有自举能力测试"""
    print("=" * 60)
    print("段言自举能力验证测试")
    print("=" * 60)

    tests = []

    # 测试1: 字符串索引
    tests.append((
        '''定义文本等于"测试文本"。
定义字符等于文本【零】。
打印字符。
打印文本【一】。
打印文本【二】。
打印文本【三】。
''',
        "字符串索引访问"
    ))

    # 测试2: 循环控制
    tests.append((
        '''定义计数等于零。
当计数小于五：
  打印计数。
  定义计数等于计数加一。
  如果计数等于三那么跳出。
打印"循环结束"。
''',
        "循环控制（跳出）"
    ))

    # 测试3: 跳过语句
    tests.append((
        '''定义计数等于零。
当计数小于五：
  定义计数等于计数加一。
  如果计数等于三那么跳过。
  打印计数。
''',
        "循环控制（跳过）"
    ))

    # 测试4: 列表操作
    tests.append((
        '''定义列表等于列表创建。
列表追加参数列表，"甲"。
列表追加参数列表，"乙"。
列表追加参数列表，"丙"。
打印列表。
打印列表长度参数列表。
''',
        "列表操作"
    ))

    # 测试5: 字典操作
    tests.append((
        '''定义字典等于字典创建。
字典设置参数字典，"名称"，"段言"。
字典设置参数字典，"版本"，"1.0"。
打印字典。
定义名称等于字典获取参数字典，"名称"。
打印名称。
''',
        "字典操作"
    ))

    # 测试6: 字符串操作
    tests.append((
        '''定义文本等于"你好世界"。
定义长度等于字符串长度参数文本。
打印长度。
定义子串等于字符串截取参数文本，零，二。
打印子串。
''',
        "字符串操作"
    ))

    # 运行所有测试
    results = []
    for source, name in tests:
        results.append(compile_and_run(source, name))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n[OK] 所有自举能力测试通过！")
        print("\n段言已具备实现简化版词法分析器的全部核心能力：")
        print("  [OK] 字符串索引访问")
        print("  [OK] 循环控制（跳出/跳过）")
        print("  [OK] 列表操作")
        print("  [OK] 字典操作")
        print("  [OK] 字符串操作")
        print("\n下一步：完善 lexer_mini.duan 并验证自举编译器工作")
        return 0
    else:
        print(f"\n[FAIL] 有 {total - passed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
