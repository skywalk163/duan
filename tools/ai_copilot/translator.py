# -*- coding: utf-8 -*-
"""
段言 ↔ Python 双向翻译器

提供 Python 代码与段言（DuanLang）代码之间的双向翻译功能。

用法:
    from translator import PythonToDuanTranslator, DuanToPythonTranslator

    # Python → 段言
    translator = PythonToDuanTranslator()
    duan_code = translator.translate("print('hello')")

    # 段言 → Python
    translator = DuanToPythonTranslator()
    python_code = translator.translate('打印("hello")')
"""

import os
import sys
import ast
from typing import Optional, List

# 路径设置
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(os.path.dirname(_TOOL_DIR))
sys.path.insert(0, _TOOL_DIR)
sys.path.insert(0, os.path.join(_PROJECT_DIR, 'src'))


# =============================================================================
# Python → 段言 翻译器
# =============================================================================

class PythonToDuanTranslator:
    """Python 代码 → 段言 翻译器

    将 Python 源码通过 AST 分析，逐节点映射为段言 v6.2 代码。
    支持 Python 基本语法：import, def, class, if/elif/else, for, while,
    try/except, with, return, yield, async/await, 赋值, 表达式等。
    Python 关键字被映射为对应的段言中文关键字。
    """

    def __init__(self):
        """初始化翻译器"""
        self._transpiler = None

    def _get_transpiler(self):
        """延迟加载 Py2DuanTranspiler"""
        if self._transpiler is None:
            from py2duan_transpiler import Py2DuanTranspiler
            self._transpiler = Py2DuanTranspiler()
        return self._transpiler

    def translate(self, python_code: str) -> str:
        """将 Python 源码翻译为段言代码

        Args:
            python_code: Python 源码字符串

        Returns:
            翻译后的段言代码字符串

        Raises:
            SyntaxError: 如果 Python 代码有语法错误
            ImportError: 如果无法加载翻译器
        """
        # 先验证 Python 代码语法
        try:
            ast.parse(python_code)
        except SyntaxError as e:
            raise SyntaxError(f"Python 语法错误: {e}") from e

        transpiler = self._get_transpiler()
        try:
            result = transpiler.transpile(python_code)
            return result
        except Exception as e:
            raise RuntimeError(f"翻译失败: {e}") from e

    def translate_file(self, file_path: str) -> str:
        """将 Python 文件翻译为段言代码

        Args:
            file_path: Python 文件路径

        Returns:
            翻译后的段言代码字符串
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            python_code = f.read()
        return self.translate(python_code)


# =============================================================================
# 段言 → Python 翻译器
# =============================================================================

class DuanToPythonTranslator:
    """段言代码 → Python 翻译器

    将段言代码通过解析器生成 AST，再通过 PythonCodeGenerator 生成 Python 代码。
    段言的中文关键字被映射为对应的 Python 英文关键字。
    """

    def __init__(self):
        """初始化翻译器"""
        self._generator = None

    def _get_generator(self):
        """延迟加载 PythonCodeGenerator"""
        if self._generator is None:
            from code_generator import PythonCodeGenerator
            self._generator = PythonCodeGenerator()
        return self._generator

    def translate(self, duan_code: str) -> str:
        """将段言代码翻译为 Python 代码

        Args:
            duan_code: 段言源码字符串

        Returns:
            翻译后的 Python 代码字符串

        Raises:
            ValueError: 如果段言代码有语法错误
            ImportError: 如果无法加载生成器
        """
        try:
            from duan_parser_v3 import DuanParser, ParseError
            parser = DuanParser()
            ast_tree = parser.parse(duan_code)
        except ParseError as e:
            raise ValueError(f"段言语法错误: {e}") from e
        except Exception as e:
            raise ValueError(f"段言解析失败: {e}") from e

        generator = self._get_generator()
        try:
            result = generator.generate(ast_tree)
            return result
        except Exception as e:
            raise RuntimeError(f"Python 代码生成失败: {e}") from e

    def translate_file(self, file_path: str) -> str:
        """将段言文件翻译为 Python 代码

        Args:
            file_path: 段言文件路径 (.duan)

        Returns:
            翻译后的 Python 代码字符串
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            duan_code = f.read()
        return self.translate(duan_code)


# =============================================================================
# 便捷函数
# =============================================================================

def python_to_duan(python_code: str, file_path: Optional[str] = None) -> str:
    """将 Python 代码翻译为段言代码（便捷函数）

    Args:
        python_code: Python 源码字符串，如果不为空则直接翻译
        file_path: Python 文件路径，如果 python_code 为空则读取文件

    Returns:
        翻译后的段言代码
    """
    translator = PythonToDuanTranslator()
    if file_path and not python_code:
        return translator.translate_file(file_path)
    return translator.translate(python_code)


def duan_to_python(duan_code: str, file_path: Optional[str] = None) -> str:
    """将段言代码翻译为 Python 代码（便捷函数）

    Args:
        duan_code: 段言源码字符串，如果不为空则直接翻译
        file_path: 段言文件路径，如果 duan_code 为空则读取文件

    Returns:
        翻译后的 Python 代码
    """
    translator = DuanToPythonTranslator()
    if file_path and not duan_code:
        return translator.translate_file(file_path)
    return translator.translate(duan_code)


# =============================================================================
# CLI 入口
# =============================================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        prog='duan-translator',
        description='段言 ↔ Python 双向翻译器',
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--to-duan', metavar='FILE',
                       help='将 Python 文件翻译为段言')
    group.add_argument('--to-python', metavar='FILE',
                       help='将段言文件翻译为 Python')
    parser.add_argument('--output', '-o', metavar='FILE',
                        help='输出到文件（默认输出到终端）')

    args = parser.parse_args()

    try:
        if args.to_duan:
            result = python_to_duan('', file_path=args.to_duan)
            source_label = f"Python 文件 {args.to_duan}"
        elif args.to_python:
            result = duan_to_python('', file_path=args.to_python)
            source_label = f"段言文件 {args.to_python}"
        else:
            parser.print_help()
            return

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"翻译完成，输出到: {args.output}")
        else:
            print(result)

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except (SyntaxError, ValueError) as e:
        print(f"翻译错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()