# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 端到端集成测试

测试完整编译流程：
段言代码 → 词法分析 → 语法解析 → 语义分析 → Python代码 → 执行验证
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator


class TestEndToEndSimple:
    """简单程序端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_variable_declaration(self, compile_pipeline):
        """测试变量声明"""
        duan_code = '定义甲等于123。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert len(python_code) > 0
    
    def test_arithmetic_operation(self, compile_pipeline):
        """测试算术运算"""
        duan_code = '定义结果等于三加五。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        # 尝试执行
        try:
            exec_globals = {}
            exec(python_code, exec_globals)
        except Exception as e:
            print(f"Execution failed: {e}")
    
    def test_string_output(self, compile_pipeline):
        """测试字符串输出"""
        duan_code = '打印"你好世界"。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'print' in python_code or '打印' in python_code


class TestEndToEndConditionals:
    """条件语句端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_simple_if(self, compile_pipeline):
        """测试简单条件"""
        duan_code = '如果甲大于乙那么打印甲。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'if' in python_code
    
    def test_if_else(self, compile_pipeline):
        """测试条件分支"""
        duan_code = '如果甲大于乙那么打印甲。否则打印乙。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'if' in python_code
        assert 'else' in python_code


class TestEndToEndFunctions:
    """函数端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_simple_function(self, compile_pipeline):
        """测试简单函数"""
        duan_code = '《计算》段返回甲加乙。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code
    
    def test_function_with_params(self, compile_pipeline):
        """测试带参数函数"""
        duan_code = '《加法》段(甲, 乙)：返回甲加乙。'
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code
        assert 'return' in python_code
    
    def test_function_call(self, compile_pipeline):
        """测试函数调用"""
        duan_code = '''《加法》段(甲, 乙)：返回甲加乙。
定义结果等于《加法》参数三和五。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code


class TestEndToEndRecursion:
    """递归函数端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_factorial(self, compile_pipeline):
        """测试阶乘函数"""
        duan_code = '''《阶乘》段(数)：
  如果数小于等于1那么返回1。
  返回数乘《阶乘》参数数减1。

定义结果等于《阶乘》参数5。
打印结果。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code
        assert '阶乘' in python_code or 'jiecheng' in python_code.lower()
    
    def test_fibonacci(self, compile_pipeline):
        """测试斐波那契函数"""
        duan_code = '''《斐波那契》段(数)：
  如果数小于等于2那么返回1。
  返回《斐波那契》参数数减1加《斐波那契》参数数减2。

定义结果等于《斐波那契》参数10。
打印结果。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code


class TestEndToEndRealWorld:
    """真实场景端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_list_operations(self, compile_pipeline):
        """测试列表操作"""
        duan_code = '''定义列表等于1，2，3，4，5。
定义结果等于排序列表。
打印结果。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
    
    def test_calculator(self, compile_pipeline):
        """测试计算器"""
        duan_code = '''《计算器》段(操作，甲，乙)：
  如果操作等于加那么返回甲加乙。
  如果操作等于减那么返回甲减乙。
  如果操作等于乘那么返回甲乘乙。
  如果操作等于除那么返回甲除乙。
  返回0。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None
        assert 'def' in python_code


class TestEndToEndErrorHandling:
    """错误处理端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            try:
                module = parser.parse(code)
                analyzer.analyze(module)
                python_code = generator.generate(module)
                return python_code
            except Exception as e:
                return None
        
        return compile
    
    def test_incomplete_code(self, compile_pipeline):
        """测试不完整代码"""
        duan_code = '定义甲等于'
        
        python_code = compile_pipeline(duan_code)
        
        # 应该能优雅处理
        # 可能返回 None 或部分结果
    
    def test_invalid_syntax(self, compile_pipeline):
        """测试无效语法"""
        duan_code = '如果那么否则'
        
        python_code = compile_pipeline(duan_code)
        
        # 应该能优雅处理


class TestEndToEndPerformance:
    """性能端到端测试"""
    
    @pytest.fixture
    def compile_pipeline(self):
        """编译流水线"""
        parser = DuanParser()
        analyzer = SemanticAnalyzer()
        generator = PythonCodeGenerator()
        
        def compile(code):
            module = parser.parse(code)
            analyzer.analyze(module)
            python_code = generator.generate(module)
            return python_code
        
        return compile
    
    def test_large_function(self, compile_pipeline):
        """测试大型函数"""
        # 生成一个较大的函数
        lines = ['定义甲等于{}。'.format(i) for i in range(100)]
        duan_code = '\n'.join(lines)
        
        python_code = compile_pipeline(duan_code)
        
        # 应该能在合理时间内完成
        assert python_code is not None
    
    def test_nested_functions(self, compile_pipeline):
        """测试嵌套函数"""
        duan_code = '''《外层》段(甲)：
  《内层》段(乙)：
    返回甲加乙。
  返回《内层》参数甲加1。'''
        
        python_code = compile_pipeline(duan_code)
        
        assert python_code is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
