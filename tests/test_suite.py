# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 独立测试套件

不依赖 pytest，直接运行所有测试
"""

import sys
import io
import os
import traceback

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def run_test(self, test_name, test_func):
        """运行单个测试"""
        try:
            test_func()
            print(f"  [OK] {test_name}")
            self.passed += 1
            return True
        except AssertionError as e:
            print(f"  [FAIL] {test_name}")
            print(f"    AssertionError: {e}")
            self.failed += 1
            self.errors.append((test_name, str(e)))
            return False
        except Exception as e:
            print(f"  [ERROR] {test_name}")
            print(f"    {type(e).__name__}: {e}")
            self.failed += 1
            self.errors.append((test_name, f"{type(e).__name__}: {e}"))
            return False
    
    def print_summary(self):
        """打印测试总结"""
        print()
        print("=" * 70)
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败")
        
        if self.errors:
            print()
            print("失败详情:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        print("=" * 70)
        
        return self.failed == 0


def test_lexer_basic():
    """测试词法分析器基础功能"""
    from lexer import Lexer
    
    lexer = Lexer()
    
    # 测试1：空输入
    tokens = lexer.tokenize('')
    assert tokens == [], "空输入应该返回空列表"
    
    # 测试2：简单标识符
    tokens = lexer.tokenize('甲')
    assert len(tokens) >= 1, "应该至少生成一个token"
    
    # 测试3：关键字识别
    tokens = lexer.tokenize('定义')
    keywords = [t for t in tokens if hasattr(t, 'type') and str(t.type) == 'TokenType.KEYWORD']
    assert len(keywords) >= 1, "应该识别到关键字"
    
    # 测试4：数字识别
    tokens = lexer.tokenize('123')
    numbers = [t for t in tokens if hasattr(t, 'type') and str(t.type) == 'TokenType.NUMBER']
    assert len(numbers) >= 1, "应该识别到数字"
    
    # 测试5：无空格分词
    tokens = lexer.tokenize('定义甲等于三。')
    assert len(tokens) >= 4, "应该正确分词：定义、甲、等于、三"


def test_parser_basic():
    """测试语法解析器基础功能"""
    from duan_parser_v3 import DuanParser
    
    parser = DuanParser()
    
    # 测试1：简单变量声明
    module = parser.parse('定义甲等于123。')
    assert len(module.statements) == 1, "应该解析出1条语句"
    
    # 测试2：多条语句
    module = parser.parse('定义甲等于1。定义乙等于2。')
    assert len(module.statements) == 2, "应该解析出2条语句"
    
    # 测试3：条件语句
    module = parser.parse('如果甲大于乙那么打印甲。')
    assert len(module.statements) >= 1, "应该解析出语句"
    
    # 测试4：函数定义
    module = parser.parse('《计算》段返回甲加乙。')
    assert len(module.statements) >= 1, "应该解析出函数定义"


def test_semantic_analyzer():
    """测试语义分析器"""
    from semantic_analyzer import SemanticAnalyzer
    
    analyzer = SemanticAnalyzer()
    
    # 测试初始化
    assert analyzer is not None, "语义分析器应该能初始化"


def test_code_generator():
    """测试代码生成器"""
    from code_generator import PythonCodeGenerator
    
    generator = PythonCodeGenerator()
    
    # 测试初始化
    assert generator is not None, "代码生成器应该能初始化"


def test_verb_info():
    """测试动词信息模块"""
    from verb_info import get_verb_info
    
    # 测试已知动词
    info = get_verb_info('加')
    assert info is not None, "应该能获取'加'的动词信息"
    assert info.arity == 2, "'加'应该是二元动词"
    
    # 测试另一个动词
    info = get_verb_info('打印')
    assert info is not None, "应该能获取'打印'的动词信息"


def test_semantic_identifier():
    """测试语义识别器"""
    from semantic_identifier import SemanticIdentifier
    
    identifier = SemanticIdentifier({})
    
    # 测试初始化
    assert identifier is not None, "语义识别器应该能初始化"


def test_complete_compilation():
    """测试完整编译流程"""
    from duan_parser_v3 import DuanParser
    from semantic_analyzer import SemanticAnalyzer
    from code_generator import PythonCodeGenerator
    
    parser = DuanParser()
    analyzer = SemanticAnalyzer()
    generator = PythonCodeGenerator()
    
    # 测试1：简单变量
    code = '定义甲等于123。'
    module = parser.parse(code)
    analyzer.analyze(module)
    python_code = generator.generate(module)
    
    assert python_code is not None, "应该生成Python代码"
    assert '甲' in python_code or 'jia' in python_code.lower(), "应该包含变量名"
    assert '123' in python_code, "应该包含数字"
    
    # 测试2：算术表达式
    code = '定义结果等于三加五。'
    module = parser.parse(code)
    analyzer.analyze(module)
    python_code = generator.generate(module)
    
    assert python_code is not None, "应该生成Python代码"
    assert '+' in python_code or 'add' in python_code.lower(), "应该包含加法运算"


def test_no_space_tokenization():
    """测试无空格分词"""
    from lexer import Lexer
    
    lexer = Lexer()
    
    # 测试无空格代码
    test_cases = [
        '定义甲等于三。',
        '甲加乙。',
        '如果甲大于乙那么打印甲。',
    ]
    
    for code in test_cases:
        tokens = lexer.tokenize(code)
        assert len(tokens) >= 2, f"'{code}' 应该分出至少2个token"


def test_chinese_numbers():
    """测试中文数字"""
    from lexer import Lexer
    
    lexer = Lexer()
    
    # 测试中文数字
    tokens = lexer.tokenize('三')
    assert len(tokens) >= 1, "应该识别中文数字"
    
    # 测试混合数字
    tokens = lexer.tokenize('三加5')
    assert len(tokens) >= 3, "应该正确分词：三、加、5"


def test_function_compilation():
    """测试函数编译"""
    from duan_parser_v3 import DuanParser
    from semantic_analyzer import SemanticAnalyzer
    from code_generator import PythonCodeGenerator
    
    parser = DuanParser()
    analyzer = SemanticAnalyzer()
    generator = PythonCodeGenerator()
    
    code = '《加法》段(甲, 乙)：返回甲加乙。'
    module = parser.parse(code)
    analyzer.analyze(module)
    python_code = generator.generate(module)
    
    assert python_code is not None, "应该生成Python代码"
    assert 'def' in python_code, "应该包含函数定义"
    assert 'return' in python_code, "应该包含返回语句"


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("段言编译器测试套件")
    print("=" * 70)
    print()
    
    runner = TestRunner()
    
    # 词法分析器测试
    print("--- 词法分析器测试 ---")
    runner.run_test("词法分析器基础功能", test_lexer_basic)
    runner.run_test("无空格分词", test_no_space_tokenization)
    runner.run_test("中文数字识别", test_chinese_numbers)
    
    # 语法解析器测试
    print()
    print("--- 语法解析器测试 ---")
    runner.run_test("语法解析器基础功能", test_parser_basic)
    
    # 语义分析器测试
    print()
    print("--- 语义分析器测试 ---")
    runner.run_test("语义分析器", test_semantic_analyzer)
    
    # 代码生成器测试
    print()
    print("--- 代码生成器测试 ---")
    runner.run_test("代码生成器", test_code_generator)
    
    # 高级语义测试
    print()
    print("--- 高级语义测试 ---")
    runner.run_test("动词信息模块", test_verb_info)
    runner.run_test("语义识别器", test_semantic_identifier)
    
    # 集成测试
    print()
    print("--- 集成测试 ---")
    runner.run_test("完整编译流程", test_complete_compilation)
    runner.run_test("函数编译", test_function_compilation)
    
    # 打印总结
    success = runner.print_summary()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
