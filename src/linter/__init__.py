# -*- coding: utf-8 -*-
"""
段言代码检查器 (Duan Linter)

提供段言代码的静态分析功能，包括语法检查、风格检查、废弃模式检测等。
"""

from src.linter.duan_linter import DuanLinter, LintResult, LintRule, Severity, RULES

__version__ = '1.1.0'