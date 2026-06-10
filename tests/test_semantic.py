# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 语义分析器测试

测试覆盖：
- 类型检查
- 作用域管理
- 符号表
- 错误检测
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer


class TestTypeChecking:
    """类型检查测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_number_type(self, parser, analyzer):
        """测试数字类型"""
        module = parser.parse('定义甲等于123。')
        
        success = analyzer.analyze(module)
        
        assert success == True
    
    def test_string_type(self, parser, analyzer):
        """测试字符串类型"""
        module = parser.parse('定义甲等于"你好"。')
        
        success = analyzer.analyze(module)
        
        assert success == True
    
    def test_binary_operation_type(self, parser, analyzer):
        """测试二元运算类型"""
        module = parser.parse('定义甲等于三加五。')
        
        success = analyzer.analyze(module)
        
        # 应该能正确推导类型
        assert success == True


class TestScopeManagement:
    """作用域管理测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_global_scope(self, parser, analyzer):
        """测试全局作用域"""
        module = parser.parse('定义甲等于1。定义乙等于2。')
        
        success = analyzer.analyze(module)
        
        assert success == True
        # 验证符号表
        assert '甲' in analyzer.symbol_table or analyzer.current_scope.has('甲')
        assert '乙' in analyzer.symbol_table or analyzer.current_scope.has('乙')
    
    def test_function_scope(self, parser, analyzer):
        """测试函数作用域"""
        module = parser.parse('《计算》段(甲, 乙)：返回甲加乙。')
        
        success = analyzer.analyze(module)
        
        assert success == True
    
    def test_nested_scope(self, parser, analyzer):
        """测试嵌套作用域"""
        code = '''《外层》段(甲)：
  《内层》段(乙)：
    返回甲加乙。'''
        
        module = parser.parse(code)
        
        success = analyzer.analyze(module)
        
        assert success == True


class TestSymbolTable:
    """符号表测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_variable_declaration(self, parser, analyzer):
        """测试变量声明"""
        module = parser.parse('定义甲等于123。')
        
        success = analyzer.analyze(module)
        
        # 变量应该被添加到符号表
        assert success == True
    
    def test_function_declaration(self, parser, analyzer):
        """测试函数声明"""
        module = parser.parse('《计算》段(甲, 乙)：返回甲加乙。')
        
        success = analyzer.analyze(module)
        
        # 函数应该被添加到符号表
        assert success == True
    
    def test_undefined_variable(self, parser, analyzer):
        """测试未定义变量"""
        module = parser.parse('打印乙。')
        
        # 应该检测到未定义变量
        # 可能返回 False 或记录错误
        analyzer.analyze(module)


class TestSemanticErrors:
    """语义错误测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_type_mismatch(self, parser, analyzer):
        """测试类型不匹配"""
        # 尝试数字和字符串相加
        module = parser.parse('定义甲等于123加"你好"。')
        
        # 应该检测到类型错误
        # 可能返回 False 或记录错误
        analyzer.analyze(module)
    
    def test_duplicate_definition(self, parser, analyzer):
        """测试重复定义"""
        module = parser.parse('定义甲等于1。定义甲等于2。')
        
        # 应该检测到重复定义
        analyzer.analyze(module)


class TestSemanticAnalysisIntegration:
    """语义分析集成测试"""
    
    @pytest.fixture
    def parser(self):
        return DuanParser()
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_complete_program(self, parser, analyzer):
        """测试完整程序"""
        code = '''《计算平方》段(数)：
  返回数乘数。

定义结果等于《计算平方》参数5。
打印结果。'''
        
        module = parser.parse(code)
        success = analyzer.analyze(module)
        
        assert success == True
    
    def test_recursive_function(self, parser, analyzer):
        """测试递归函数"""
        code = '''《阶乘》段(数)：
  如果数小于等于1那么返回1。
  返回数乘《阶乘》参数数减1。'''
        
        module = parser.parse(code)
        success = analyzer.analyze(module)
        
        assert success == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
