# -*- coding: utf-8 -*-
"""
段言编译器核心模块
"""

from .interfaces import (
    ILexer, IParser, ISemanticAnalyzer, ICodeGenerator, ICompiler,
    Position, SourceLocation
)
from .errors import (
    DuanError, LexerError, ParserError, SemanticError, CodeGenError,
    TypeError, NameError, CompileError, error_context
)
from .config import DuanConfig, OutputFormat, OptimizationLevel, get_default_config

__all__ = [
    # 接口
    'ILexer', 'IParser', 'ISemanticAnalyzer', 'ICodeGenerator', 'ICompiler',
    'Position', 'SourceLocation',
    
    # 错误
    'DuanError', 'LexerError', 'ParserError', 'SemanticError', 'CodeGenError',
    'TypeError', 'NameError', 'CompileError', 'error_context',
    
    # 配置
    'DuanConfig', 'OutputFormat', 'OptimizationLevel', 'get_default_config',
]
