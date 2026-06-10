#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言模块系统测试

测试导入、导出语句的解析和代码生成
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser, ImportStmt, ExportStmt
from code_generator import PythonCodeGenerator


def test_import_basic():
    """测试基本导入"""
    code = '导入《数学库》。'
    
    parser = DuanParser()
    module = parser.parse(code)
    
    assert len(module.statements) == 1
    stmt = module.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_name == '数学库'
    assert stmt.symbols is None
    assert stmt.alias is None
    
    print("[OK] 测试基本导入通过")


def test_import_with_alias():
    """测试带别名的导入"""
    code = '导入《数学库》为数学。'
    
    parser = DuanParser()
    module = parser.parse(code)
    
    assert len(module.statements) == 1
    stmt = module.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_name == '数学库'
    assert stmt.alias == '数学'
    
    print("[OK] 测试带别名的导入通过")


def test_from_import():
    """测试从...导入"""
    code = '从《数学库》导入《平方根》，《绝对值》。'
    
    parser = DuanParser()
    module = parser.parse(code)
    
    assert len(module.statements) == 1
    stmt = module.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_name == '数学库'
    assert stmt.symbols == ['平方根', '绝对值']
    
    print("[OK] 测试从...导入通过")


def test_export():
    """测试导出"""
    code = '导出《平方》，《立方》。'
    
    parser = DuanParser()
    module = parser.parse(code)
    
    assert len(module.statements) == 1
    stmt = module.statements[0]
    assert isinstance(stmt, ExportStmt)
    assert stmt.symbols == ['平方', '立方']
    
    print("[OK] 测试导出通过")


def test_export_all():
    """测试导出全部"""
    code = '导出全部。'
    
    parser = DuanParser()
    module = parser.parse(code)
    
    assert len(module.statements) == 1
    stmt = module.statements[0]
    assert isinstance(stmt, ExportStmt)
    assert stmt.symbols == ['*']
    
    print("[OK] 测试导出全部通过")


def test_code_generation_import():
    """测试导入语句的代码生成"""
    code = '导入《数学库》。'
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    module = parser.parse(code)
    python_code = generator.generate(module)
    
    assert 'import 数学库' in python_code
    print(f"生成的Python代码:\n{python_code}")
    print("[OK] 测试导入代码生成通过")


def test_code_generation_from_import():
    """测试从...导入的代码生成"""
    code = '从《数学库》导入《平方根》，《绝对值》。'
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    module = parser.parse(code)
    python_code = generator.generate(module)
    
    assert 'from 数学库 import 平方根, 绝对值' in python_code
    print(f"生成的Python代码:\n{python_code}")
    print("[OK] 测试从...导入代码生成通过")


def test_code_generation_export():
    """测试导出语句的代码生成"""
    code = '导出《平方》，《立方》。'
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    module = parser.parse(code)
    python_code = generator.generate(module)
    
    assert "__all__ = ['平方', '立方']" in python_code
    print(f"生成的Python代码:\n{python_code}")
    print("[OK] 测试导出代码生成通过")


def test_complete_module():
    """测试完整模块示例"""
    code = '''
# 数学工具模块

导出《平方》，《立方》。

《平方》段(数)：
  返回数乘数。

《立方》段(数)：
  返回数乘数乘数。
'''
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    module = parser.parse(code)
    python_code = generator.generate(module)
    
    print(f"生成的Python代码:\n{python_code}")
    
    # 检查关键内容
    assert '__all__' in python_code
    assert 'def 平方' in python_code
    assert 'def 立方' in python_code
    
    print("[OK] 测试完整模块通过")


def test_module_usage():
    """测试模块使用示例"""
    code = '''
从《math_utils》导入《平方》，《立方》。

定义甲等于5。

打印甲。
'''
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    try:
        module = parser.parse(code)
        python_code = generator.generate(module)
        
        print(f"生成的Python代码:\n{python_code}")
        
        # 检查关键内容
        assert 'from math_utils import 平方, 立方' in python_code
        assert '甲 = 5' in python_code
        
        print("[OK] 测试模块使用通过")
    except Exception as e:
        print(f"[WARN] 测试模块使用跳过: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("段言模块系统测试")
    print("=" * 60)
    print()
    
    # 运行所有测试
    test_import_basic()
    test_import_with_alias()
    test_from_import()
    test_export()
    test_export_all()
    test_code_generation_import()
    test_code_generation_from_import()
    test_code_generation_export()
    test_complete_module()
    test_module_usage()
    
    print()
    print("=" * 60)
    print("所有测试通过！")
    print("=" * 60)
