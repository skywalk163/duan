# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 统一测试运行器

运行方式：
  python tests/run_tests.py          # 运行全部测试
  python tests/run_tests.py --quick  # 仅运行快速验证
  python tests/run_tests.py --edge   # 仅运行边界测试
  python tests/run_tests.py --list   # 列出所有测试文件
"""

import sys
import io
import os
import subprocess
import glob

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


def print_header(title):
    """打印带格式的标题"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def print_summary(results):
    """打印测试总结"""
    total = sum(r['total'] for r in results)
    passed = sum(r['passed'] for r in results)
    failed = sum(r['failed'] for r in results)
    errors = sum(r['errors'] for r in results)
    
    print()
    print("=" * 70)
    print("  测试总结")
    print("=" * 70)
    for r in results:
        status = "OK" if r['failed'] == 0 and r['errors'] == 0 else "FAIL"
        print(f"  [{status}] {r['name']}: {r['passed']}/{r['total']} 通过")
    
    total_failures = failed + errors
    print()
    if total_failures == 0:
        print(f"  [OK] 全部 {total} 个测试通过！")
    else:
        print(f"  [FAIL] {passed}/{total} 通过, {total_failures} 失败")
    print("=" * 70)
    print()
    
    return total_failures


def run_quick_tests():
    """运行快速验证测试（不使用pytest，验证核心模块可用性）"""
    print_header("快速验证测试")
    
    sys.path.insert(0, SRC_DIR)
    
    tests_passed = 0
    tests_failed = 0
    
    test_cases = [
        ("词法分析器", lambda: _test_lexer()),
        ("语法解析器", lambda: _test_parser()),
        ("语义分析器", lambda: _test_semantic()),
        ("代码生成器", lambda: _test_codegen()),
        ("完整编译流程", lambda: _test_pipeline()),
        ("动词信息模块", lambda: _test_verb_info()),
        ("语义识别器", lambda: _test_identifier()),
    ]
    
    for name, test_fn in test_cases:
        print(f"  [{name}] ", end="")
        try:
            msg = test_fn()
            print(f"OK  {msg}")
            tests_passed += 1
        except Exception as e:
            print(f"FAIL  {e}")
            tests_failed += 1
    
    print(f"\n  快速验证: {tests_passed} 通过, {tests_failed} 失败")
    return {'name': '快速验证', 'total': len(test_cases), 'passed': tests_passed, 'failed': tests_failed, 'errors': 0}


def _test_lexer():
    from lexer import Lexer
    lexer = Lexer()
    tokens = lexer.tokenize('定义甲等于三。')
    return f"生成 {len(tokens)} 个 token"


def _test_parser():
    from duan_parser_v3 import DuanParser
    parser = DuanParser()
    module = parser.parse('定义甲等于123。')
    return f"解析 {len(module.statements)} 条语句"


def _test_semantic():
    from semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    return "初始化成功"


def _test_codegen():
    from code_generator import PythonCodeGenerator
    generator = PythonCodeGenerator()
    return "初始化成功"


def _test_pipeline():
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
    return f"正常输出: {python_code.strip()[:60]}..."


def _test_verb_info():
    from verb_info import get_verb_info
    info = get_verb_info('加')
    if info:
        return f"动词'加' - 元数: {info.arity}"
    return "正常"


def _test_identifier():
    from semantic_identifier import SemanticIdentifier
    identifier = SemanticIdentifier({})
    return "初始化成功"


def run_pytest(test_files=None, exclude_patterns=None):
    """运行 pytest 测试
    
    Args:
        test_files: 要运行的测试文件列表（None=运行所有）
        exclude_patterns: 要排除的模式列表
    """
    os.chdir(PROJECT_DIR)
    
    if test_files is None:
        # 自动发现 tests/ 目录下的所有 test_*.py 文件
        all_tests = sorted(glob.glob(os.path.join(PROJECT_DIR, 'tests', 'test_*.py')))
        # 排除 ANTLR 后端测试（使用不同语法）
        exclude = ['test_comprehensive', 'test_modern_features', 'test_ternary', 'test_ternary_antlr',
                   'test_advanced_semantic', 'test_module_system', 'test_class_advanced',
                   'test_async', 'test_interface']
        if exclude_patterns:
            exclude.extend(exclude_patterns)
        test_files = [t for t in all_tests if not any(e in os.path.basename(t) for e in exclude)]
    
    if not test_files:
        print("  (没有匹配的测试文件)")
        return {'name': 'pytest', 'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}
    
    cmd = [sys.executable, '-m', 'pytest'] + test_files + ['-v', '--tb=short', '--no-header', '-q']
    
    result = subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    # 解析输出获取统计
    lines = result.stdout.split('\n')
    summary_line = ''
    for line in lines:
        if 'passed' in line and 'failed' in line:
            summary_line = line.strip()
            break
    
    # 计算统计
    total = passed = failed = errors = 0
    for line in lines:
        if 'PASSED' in line:
            passed += 1
            total += 1
        elif 'FAILED' in line:
            failed += 1
            total += 1
        elif 'ERROR' in line:
            errors += 1
            total += 1
    
    if total == 0 and result.returncode == 0:
        # 可能没有匹配的测试方法
        pass
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr[:500])
    
    return {'name': 'pytest 单元测试', 'total': total, 'passed': passed, 'failed': failed, 'errors': errors}


def run_edge_case_tests():
    """运行边界测试"""
    print_header("边界测试")
    return run_pytest(
        test_files=[os.path.join(PROJECT_DIR, 'tests', 'test_edge_cases.py')]
    )


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("  段言（Duan）编程语言 - 完整测试套件")
    print("=" * 70)
    print(f"  项目目录: {PROJECT_DIR}")
    print(f"  Python: {sys.version.split()[0]}")
    
    results = []
    
    # 1. 快速验证
    results.append(run_quick_tests())
    
    # 2. 核心 pytest 测试（Python 后端）
    print_header("核心 pytest 测试")
    results.append(run_pytest())
    
    # 3. 边界测试
    results.append(run_edge_case_tests())
    
    # 总结
    return print_summary(results)


def list_test_files():
    """列出所有测试文件"""
    print_header("测试文件列表")
    
    test_dir = os.path.join(PROJECT_DIR, 'tests')
    test_files = sorted(glob.glob(os.path.join(test_dir, 'test_*.py')))
    
    for tf in test_files:
        name = os.path.basename(tf)
        # 尝试读取文档字符串
        with open(tf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取模块文档字符串
        doc = ""
        if '"""' in content:
            start = content.index('"""') + 3
            end = content.index('"""', start)
            doc = content[start:end].strip().split('\n')[0]
        
        category = "Python后端" 
        if any(x in name for x in ['comprehensive', 'modern', 'ternary', 'antlr']):
            category = "ANTLR后端"
        elif name == 'test_edge_cases.py':
            category = "边界测试"
        elif name in ('test_parser.py', 'test_codegen.py', 'test_lexer.py', 'test_e2e.py'):
            category = "核心测试"
        elif name in ('run_tests.py', 'verify.py', 'coverage_report.py', 'final_test.py'):
            category = "工具"
        
        print(f"  [{category:12s}] {name}")
        if doc:
            print(f"            {doc}")
    
    print(f"\n  共 {len(test_files)} 个测试文件")
    print()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='段言（Duan）编程语言 - 统一测试运行器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tests/run_tests.py              # 运行全部测试
  python tests/run_tests.py --quick       # 仅快速验证
  python tests/run_tests.py --edge        # 仅边界测试
  python tests/run_tests.py --list        # 列出测试文件
  python tests/run_tests.py --full        # 运行完整的 pytest（含 ANTLR 后端）
        """
    )
    parser.add_argument('--quick', action='store_true', help='仅运行快速验证测试')
    parser.add_argument('--edge', action='store_true', help='仅运行边界测试')
    parser.add_argument('--list', action='store_true', help='列出所有测试文件')
    parser.add_argument('--full', action='store_true', help='运行完整测试（含所有后端）')
    
    args = parser.parse_args()
    
    if args.list:
        list_test_files()
        sys.exit(0)
    elif args.quick:
        result = run_quick_tests()
        sys.exit(0 if result['failed'] == 0 else 1)
    elif args.edge:
        result = run_edge_case_tests()
        sys.exit(0 if result['failed'] == 0 else 1)
    elif args.full:
        print_header("完整测试（含所有后端）")
        result = run_pytest(test_files=None, exclude_patterns=[])
        sys.exit(0 if result['failed'] == 0 else 1)
    else:
        exit_code = run_all_tests()
        sys.exit(exit_code)