# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 测试运行器

运行所有测试并生成测试报告
"""

import sys
import io
import os
import subprocess

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_pytest():
    """运行pytest测试"""
    print("=" * 70)
    print("段言编译器测试套件")
    print("=" * 70)
    print()
    
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    print(f"项目目录: {project_dir}")
    print(f"Python版本: {sys.version}")
    print()
    
    # 运行pytest
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short', '--color=yes'],
        cwd=project_dir,
        capture_output=False,
        text=True
    )
    
    print()
    print("=" * 70)
    if result.returncode == 0:
        print("[OK] 所有测试通过！")
    else:
        print(f"[FAIL] 测试失败，退出码: {result.returncode}")
    print("=" * 70)
    
    return result.returncode


def run_quick_tests():
    """运行快速测试（不使用pytest）"""
    print("=" * 70)
    print("段言编译器快速测试")
    print("=" * 70)
    print()
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    tests_passed = 0
    tests_failed = 0
    
    # 测试1：词法分析器
    print("\n--- 测试1: 词法分析器 ---")
    try:
        from lexer import Lexer
        lexer = Lexer()
        tokens = lexer.tokenize('定义甲等于三。')
        print(f"[OK] 词法分析器工作正常，生成 {len(tokens)} 个token")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 词法分析器错误: {e}")
        tests_failed += 1
    
    # 测试2：语法解析器
    print("\n--- 测试2: 语法解析器 ---")
    try:
        from duan_parser_v3 import DuanParser
        parser = DuanParser()
        module = parser.parse('定义甲等于123。')
        print(f"[OK] 语法解析器工作正常，解析 {len(module.statements)} 条语句")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 语法解析器错误: {e}")
        tests_failed += 1
    
    # 测试3：语义分析器
    print("\n--- 测试3: 语义分析器 ---")
    try:
        from semantic_analyzer import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        print(f"[OK] 语义分析器初始化成功")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 语义分析器错误: {e}")
        tests_failed += 1
    
    # 测试4：代码生成器
    print("\n--- 测试4: 代码生成器 ---")
    try:
        from code_generator import PythonCodeGenerator
        generator = PythonCodeGenerator()
        print(f"[OK] 代码生成器初始化成功")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 代码生成器错误: {e}")
        tests_failed += 1
    
    # 测试5：完整编译流程
    print("\n--- 测试5: 完整编译流程 ---")
    try:
        from duan_parser_v3 import DuanParser
        from semantic_analyzer import SemanticAnalyzer
        from code_generator import PythonCodeGenerator
        
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        code = '定义甲等于三加五。'
        module = parser.parse(code)
        analyzer.analyze(module)
        python_code = generator.generate(module)
        
        print(f"[OK] 完整编译流程工作正常")
        print(f"  段言: {code}")
        print(f"  Python: {python_code.strip()}")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 完整编译流程错误: {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # 测试6：动词信息模块
    print("\n--- 测试6: 动词信息模块 ---")
    try:
        from verb_info import get_verb_info
        info = get_verb_info('加')
        print(f"[OK] 动词信息模块工作正常")
        if info:
            print(f"  动词'加' - 元数: {info.arity}, 模式: {info.mode}")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 动词信息模块错误: {e}")
        tests_failed += 1
    
    # 测试7：语义识别器
    print("\n--- 测试7: 语义识别器 ---")
    try:
        from semantic_identifier import SemanticIdentifier
        identifier = SemanticIdentifier({})
        print(f"[OK] 语义识别器初始化成功")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] 语义识别器错误: {e}")
        tests_failed += 1
    
    # 总结
    print()
    print("=" * 70)
    print(f"测试结果: {tests_passed} 通过, {tests_failed} 失败")
    print("=" * 70)
    
    return tests_failed


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='段言编译器测试')
    parser.add_argument('--quick', action='store_true', help='运行快速测试')
    parser.add_argument('--pytest', action='store_true', help='运行pytest测试')
    
    args = parser.parse_args()
    
    if args.quick:
        exit_code = run_quick_tests()
        sys.exit(0 if exit_code == 0 else 1)
    elif args.pytest:
        exit_code = run_pytest()
        sys.exit(exit_code)
    else:
        # 默认运行快速测试
        exit_code = run_quick_tests()
        sys.exit(0 if exit_code == 0 else 1)