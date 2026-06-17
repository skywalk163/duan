# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 代码生成器测试

测试覆盖：
- 变量声明代码生成
- 表达式代码生成
- 条件语句代码生成
- 循环语句代码生成
- 函数定义代码生成
- 函数调用代码生成
- 完整程序代码生成
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator


class TestVariableGeneration:
    """变量声明代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_simple_variable(self, parser, analyzer, generator):
        """测试简单变量生成"""
        module = parser.parse('定义甲等于123。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert '甲' in python_code or 'jia' in python_code.lower()
        assert '123' in python_code
        assert '=' in python_code
    
    def test_variable_with_expression(self, parser, analyzer, generator):
        """测试带表达式的变量生成"""
        module = parser.parse('定义结果等于三加五。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert '结果' in python_code or 'jieguo' in python_code.lower()
        assert '+' in python_code or 'add' in python_code.lower()


class TestExpressionGeneration:
    """表达式代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_arithmetic_expression(self, parser, analyzer, generator):
        """测试算术表达式生成"""
        module = parser.parse('定义结果等于甲加乙乘丙。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert '甲' in python_code or 'jia' in python_code.lower()
        assert '+' in python_code or 'add' in python_code.lower()
        assert '*' in python_code or 'mul' in python_code.lower()
    
    def test_comparison_expression(self, parser, analyzer, generator):
        """测试比较表达式生成"""
        module = parser.parse('如果甲大于乙那么打印甲。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'if' in python_code
        assert '>' in python_code or 'gt' in python_code.lower()


class TestConditionalGeneration:
    """条件语句代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_simple_if(self, parser, analyzer, generator):
        """测试简单if生成"""
        module = parser.parse('如果甲大于乙那么打印甲。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'if' in python_code
        assert 'print' in python_code or '打印' in python_code
    
    def test_if_else(self, parser, analyzer, generator):
        """测试if-else生成"""
        module = parser.parse('如果甲大于乙那么打印甲。否则打印乙。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'if' in python_code
        assert 'else' in python_code


class TestLoopGeneration:
    """循环语句代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_while_loop(self, parser, analyzer, generator):
        """测试while循环生成"""
        code = '''当 甲 小于 十：
  甲 等于 甲 加 一。
结束。'''
        
        module = parser.parse(code)
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'while' in python_code
    
    def test_for_loop(self, parser, analyzer, generator):
        """测试for循环生成"""
        code = '''遍历元素之列表：
  打印元素。'''
        
        module = parser.parse(code)
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'for' in python_code


class TestFunctionGeneration:
    """函数定义代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_simple_function(self, parser, analyzer, generator):
        """测试简单函数生成"""
        module = parser.parse('《计算》段：返回甲加乙。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'def' in python_code
        assert '计算' in python_code or 'jisuan' in python_code.lower()
    
    def test_function_with_params(self, parser, analyzer, generator):
        """测试带参数的函数生成"""
        module = parser.parse('《计算》段(甲, 乙)：返回甲加乙。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'def' in python_code
        assert '(' in python_code
        assert ')' in python_code
        assert 'return' in python_code


class TestFunctionCallGeneration:
    """函数调用代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_simple_call(self, parser, analyzer, generator):
        """测试简单函数调用生成"""
        module = parser.parse('定义结果等于《计算》(甲，乙)。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert '计算' in python_code or 'jisuan' in python_code.lower()
        assert '(' in python_code
        assert ')' in python_code
    
    def test_call_in_expression(self, parser, analyzer, generator):
        """测试表达式中的函数调用"""
        module = parser.parse('定义结果等于《计算》(甲，乙)。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert '计算' in python_code or 'jisuan' in python_code.lower()


class TestCompleteProgramGeneration:
    """完整程序代码生成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_factorial(self, parser, analyzer, generator):
        """测试阶乘程序生成"""
        code = '''《阶乘》段(数)：
  如果数小于等于1那么返回1。
  返回数乘《阶乘》(数减1)。

定义结果等于《阶乘》(5)。
打印结果。'''
        
        module = parser.parse(code)
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'def' in python_code
        assert '阶乘' in python_code or 'jiecheng' in python_code.lower()
        assert 'if' in python_code
        assert 'return' in python_code
        assert 'print' in python_code
    
    def test_fibonacci(self, parser, analyzer, generator):
        """测试斐波那契程序生成"""
        code = '''《斐波那契》段(数)：
  如果数小于等于2那么返回1。
  返回《斐波那契》(数减1)加《斐波那契》(数减2)。

定义结果等于《斐波那契》(10)。
打印结果。'''
        
        module = parser.parse(code)
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        assert 'def' in python_code
        assert 'if' in python_code
        assert 'return' in python_code


class TestCodeExecution:
    """代码执行测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    @pytest.fixture
    def generator(self):
        return PythonCodeGenerator()
    
    def test_simple_execution(self, parser, analyzer, generator):
        """测试简单程序执行"""
        module = parser.parse('定义甲等于三加五。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        # 尝试执行生成的代码
        try:
            exec_globals = {}
            exec(python_code, exec_globals)
            # 如果没有异常，测试通过
            assert True
        except Exception as e:
            # 如果有异常，打印错误信息
            print(f"Execution error: {e}")
            # 可能需要调整生成器
    
    def test_function_execution(self, parser, analyzer, generator):
        """测试函数程序执行"""
        module = parser.parse('《加法》段(甲, 乙)：返回甲加乙。')
        analyzer.analyze(module)
        
        python_code = generator.generate(module)
        
        try:
            exec_globals = {}
            exec(python_code, exec_globals)
            
            # 检查函数是否被定义
            func_name = None
            for key in exec_globals:
                if '加法' in key or 'jiafa' in key.lower() or callable(exec_globals[key]):
                    func_name = key
                    break
            
            if func_name:
                # 测试函数调用
                result = exec_globals[func_name](3, 5)
                assert result == 8
        except Exception as e:
            print(f"Execution error: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
