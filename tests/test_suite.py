#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
段言编程语言 - 统一测试套件

测试覆盖：
- 基本语法
- 变量和表达式
- 段落（函数）定义和调用
- 控制流（条件、循环）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'antlrparser'))

import unittest
from io import StringIO
from duan_compile import compile_to_python, parse_source


class TestDuanCompiler(unittest.TestCase):
    """段言编译器测试套件"""
    
    def run_duan_code(self, code):
        """运行段言代码并返回输出"""
        module = parse_source(code)
        python_code = compile_to_python(module)
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            exec(python_code)
        except Exception as e:
            sys.stdout = old_stdout
            raise AssertionError(f"代码执行失败: {e}\n生成的代码:\n{python_code}")
        
        sys.stdout = old_stdout
        return captured_output.getvalue()
    
    def test_variable_declaration(self):
        """测试变量声明"""
        code = """
设 甲 为 10。
设 乙 为 "测试"。
打印(甲)。
打印(乙)。
"""
        output = self.run_duan_code(code)
        self.assertIn("10", output)
        self.assertIn("测试", output)
    
    def test_arithmetic_operations(self):
        """测试算术运算"""
        code = """
设 结果 为 3 + 5 * 2。
打印(结果)。
"""
        output = self.run_duan_code(code)
        self.assertIn("13", output)
    
    def test_paragraph_definition(self):
        """测试段落（函数）定义"""
        code = """
段落 平方 接收 数值:
    返回 数值 * 数值。
结束。

打印(平方(5))。
"""
        output = self.run_duan_code(code)
        self.assertIn("25", output)
    
    def test_paragraph_with_multiple_params(self):
        """测试多参数段落"""
        code = """
段落 求和 接收 甲, 乙:
    返回 甲 + 乙。
结束。

打印(求和(3, 7))。
"""
        output = self.run_duan_code(code)
        self.assertIn("10", output)
    
    def test_conditional_statement(self):
        """测试条件语句"""
        code = """
设 年龄 为 18。
如果 年龄 > 18:
    打印("成年")。
否则:
    打印("未成年")。
结束。
"""
        output = self.run_duan_code(code)
        self.assertIn("未成年", output)
    
    def test_while_loop(self):
        """测试while循环"""
        code = """
设 计数 为 0。
当 计数 < 3:
    打印(计数)。
    设 计数 为 计数 + 1。
结束。
"""
        output = self.run_duan_code(code)
        self.assertIn("0", output)
        self.assertIn("1", output)
        self.assertIn("2", output)
    
    def test_string_concatenation(self):
        """测试字符串拼接"""
        code = """
设 问候 为 "你好，"。
设 名字 为 "世界"。
打印(问候 + 名字 + "！")。
"""
        output = self.run_duan_code(code)
        self.assertIn("你好，世界！", output)
    
    def test_list_literal(self):
        """测试列表字面量"""
        code = """
设 水果 为 ["苹果", "香蕉", "橙子"]。
打印(水果[0])。
"""
        output = self.run_duan_code(code)
        self.assertIn("苹果", output)


class TestDuanControlFlow(unittest.TestCase):
    """段言控制流测试"""
    
    def run_duan_code(self, code):
        """运行段言代码并返回输出"""
        module = parse_source(code)
        python_code = compile_to_python(module)
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            exec(python_code)
        except Exception as e:
            sys.stdout = old_stdout
            raise AssertionError(f"代码执行失败: {e}\n生成的代码:\n{python_code}")
        
        sys.stdout = old_stdout
        return captured_output.getvalue()
    
    def test_break_statement(self):
        """测试break语句"""
        code = """
设 计数 为 0。
当 计数 < 10:
    如果 计数 == 5:
        跳出。
    结束。
    设 计数 为 计数 + 1。
结束。
打印("循环结束于: " + str(计数))。
"""
        output = self.run_duan_code(code)
        self.assertIn("循环结束于: 5", output)
    
    def test_continue_statement(self):
        """测试continue语句"""
        code = """
设 计数 为 0。
设 总和 为 0。
当 计数 < 5:
    设 计数 为 计数 + 1。
    如果 计数 == 3:
        跳过。
    结束。
    设 总和 为 总和 + 计数。
结束。
打印("总和: " + str(总和))。
"""
        output = self.run_duan_code(code)
        self.assertIn("总和: 12", output)


def run_all_tests():
    """运行所有测试"""
    print("=== 段言编译器测试套件 ===")
    
    suite = unittest.TestSuite()
    
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDuanCompiler))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDuanControlFlow))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n=== 测试统计 ===")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
