# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - pytest 配置
"""

import sys
import io
import pytest

# 设置输出编码（Windows 兼容）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加 src 目录到路径
sys.path.insert(0, 'src')


@pytest.fixture
def parser():
    """提供解析器实例"""
    from duan_parser_v3 import DuanParser
    return DuanParser()


@pytest.fixture
def analyzer():
    """提供语义分析器实例"""
    from semantic_analyzer import SemanticAnalyzer
    return SemanticAnalyzer()


@pytest.fixture
def generator():
    """提供代码生成器实例"""
    from code_generator import PythonCodeGenerator
    return PythonCodeGenerator()
