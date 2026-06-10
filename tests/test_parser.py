# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 语法解析器测试

测试覆盖：
- 变量声明
- 表达式解析
- 条件语句
- 循环语句
- 段落定义
- 管道操作
- 错误处理
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duan_parser_v3 import DuanParser
from ast_nodes import *


class TestVariableDeclaration:
    """变量声明测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_simple_variable(self, parser):
        """测试简单变量声明"""
        module = parser.parse('定义甲等于3。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)
        assert stmt.name == '甲'
    
    def test_variable_with_expression(self, parser):
        """测试带表达式的变量声明"""
        module = parser.parse('定义结果等于三加五。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)
        assert stmt.name == '结果'
    
    def test_multiple_variables(self, parser):
        """测试多变量声明"""
        module = parser.parse('定义甲等于1。定义乙等于2。定义丙等于3。')
        
        assert len(module.statements) == 3
        for stmt in module.statements:
            assert isinstance(stmt, VariableDecl)


class TestExpressions:
    """表达式测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_arithmetic_expression(self, parser):
        """测试算术表达式"""
        module = parser.parse('定义结果等于甲加乙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)
        assert stmt.initializer is not None
    
    def test_nested_expression(self, parser):
        """测试嵌套表达式"""
        module = parser.parse('定义结果等于甲加乙乘丙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)
    
    def test_comparison_expression(self, parser):
        """测试比较表达式"""
        module = parser.parse('如果甲大于乙那么打印甲。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, IfStatement)


class TestConditionals:
    """条件语句测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_simple_if(self, parser):
        """测试简单if语句"""
        module = parser.parse('如果甲大于十那么打印甲。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.condition is not None
    
    def test_if_else(self, parser):
        """测试if-else语句"""
        module = parser.parse('如果甲大于乙那么打印甲。否则打印乙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.else_branch is not None


class TestLoops:
    """循环语句测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_while_loop(self, parser):
        """测试while循环"""
        code = '''当甲小于十：
  甲等于甲加一。'''
        
        module = parser.parse(code)
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, WhileStatement)
    
    def test_for_loop(self, parser):
        """测试for循环"""
        code = '''遍历列表中的元素：
  打印元素。'''
        
        module = parser.parse(code)
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, ForStatement)


class TestFunctionDefinition:
    """函数定义测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_simple_function(self, parser):
        """测试简单函数定义"""
        module = parser.parse('《计算》段返回甲加乙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, FunctionDef)
        assert stmt.name == '计算'
    
    def test_function_with_params(self, parser):
        """测试带参数的函数定义"""
        module = parser.parse('《计算》段(甲, 乙)：返回甲加乙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, FunctionDef)
        assert len(stmt.params) == 2
    
    def test_function_with_body(self, parser):
        """测试带函数体的函数定义"""
        code = '''《计算》段(甲, 乙)：
  定义结果等于甲加乙。
  返回结果。'''
        
        module = parser.parse(code)
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, FunctionDef)
        assert len(stmt.body) >= 1


class TestPipeline:
    """管道操作测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_arrow_pipeline(self, parser):
        """测试箭头管道"""
        module = parser.parse('数据 -> 过滤 -> 排序。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        # 管道操作应该被正确解析
    
    def test_comma_pipeline(self, parser):
        """测试逗号管道"""
        module = parser.parse('数据，过滤，排序。')
        
        assert len(module.statements) == 1


class TestFunctionCall:
    """函数调用测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_simple_call(self, parser):
        """测试简单函数调用"""
        module = parser.parse('《计算》参数甲乙。')
        
        assert len(module.statements) >= 1
    
    def test_call_in_expression(self, parser):
        """测试表达式中的函数调用"""
        module = parser.parse('定义结果等于《计算》参数甲乙。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)


class TestComplexPrograms:
    """复杂程序测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_factorial(self, parser):
        """测试阶乘程序"""
        code = '''《阶乘》段(数)：
  如果数小于等于1那么返回1。
  返回数乘《阶乘》参数数减1。

定义结果等于《阶乘》参数5。
打印结果。'''
        
        module = parser.parse(code)
        
        assert len(module.statements) >= 2
    
    def test_fibonacci(self, parser):
        """测试斐波那契程序"""
        code = '''《斐波那契》段(数)：
  如果数小于等于2那么返回1。
  返回《斐波那契》参数数减1加《斐波那契》参数数减2。

定义结果等于《斐波那契》参数10。
打印结果。'''
        
        module = parser.parse(code)
        
        assert len(module.statements) >= 2


class TestErrorHandling:
    """错误处理测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_incomplete_statement(self, parser):
        """测试不完整语句"""
        # 不完整语句应该能优雅处理
        try:
            module = parser.parse('定义甲等于')
            # 可能返回部分结果或抛出异常
        except Exception as e:
            # 应该是有意义的错误信息
            assert str(e) != ''
    
    def test_invalid_syntax(self, parser):
        """测试无效语法"""
        try:
            module = parser.parse('如果那么否则')
            # 可能返回结果或抛出异常
        except Exception as e:
            # 应该能优雅处理
            assert str(e) != ''


class TestNoSpaceCode:
    """无空格代码测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    def test_no_space_variable(self, parser):
        """测试无空格变量声明"""
        module = parser.parse('定义甲等于三加五。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, VariableDecl)
    
    def test_no_space_condition(self, parser):
        """测试无空格条件语句"""
        module = parser.parse('如果甲大于乙那么打印甲。')
        
        assert len(module.statements) == 1
        stmt = module.statements[0]
        assert isinstance(stmt, IfStatement)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
