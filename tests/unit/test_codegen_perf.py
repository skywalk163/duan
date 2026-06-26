# -*- coding: utf-8 -*-
"""
代码生成器性能测试

测试优化后的代码生成器性能，确保生成大量代码时性能良好
"""

import sys
import os
import time
import pytest

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
sys.path.insert(0, _src_dir)


class TestCodeGenPerformance:
    """代码生成器性能测试"""

    def test_generate_500_functions_python_code_generator(self):
        """测试 PythonCodeGenerator 生成 500 个函数定义在 2 秒内完成"""
        from code_generator import PythonCodeGenerator
        from ast_nodes_v3 import Module, Paragraph, NumberLiteral, ReturnStmt

        functions = []
        for i in range(500):
            body = [ReturnStmt(NumberLiteral(i))]
            func = Paragraph(f'func_{i}', [], None, body)
            functions.append(func)

        module = Module(functions)
        generator = PythonCodeGenerator()

        start_time = time.time()
        code = generator.generate(module)
        end_time = time.time()

        elapsed = end_time - start_time
        print(f"\nPythonCodeGenerator 生成 500 个函数耗时: {elapsed:.4f} 秒")

        assert code is not None
        assert len(code) > 0
        assert 'def func_0' in code
        assert 'def func_499' in code
        assert elapsed < 2.0, f"代码生成耗时 {elapsed:.4f} 秒，超过 2 秒限制"

    def test_generate_500_functions_unified_code_generator(self):
        """测试 UnifiedCodeGenerator 生成 500 个函数定义在 2 秒内完成"""
        from code_generator_unified import UnifiedCodeGenerator
        from ast_nodes_v3 import Module, Paragraph, NumberLiteral, ReturnStmt

        functions = []
        for i in range(500):
            body = [ReturnStmt(NumberLiteral(i))]
            func = Paragraph(f'func_{i}', [], None, body)
            functions.append(func)

        module = Module(functions)
        generator = UnifiedCodeGenerator()

        start_time = time.time()
        code = generator.generate(module)
        end_time = time.time()

        elapsed = end_time - start_time
        print(f"\nUnifiedCodeGenerator 生成 500 个函数耗时: {elapsed:.4f} 秒")

        assert code is not None
        assert len(code) > 0
        assert 'def func_0' in code
        assert 'def func_499' in code
        assert elapsed < 2.0, f"代码生成耗时 {elapsed:.4f} 秒，超过 2 秒限制"

    def test_indent_cache_works(self):
        """测试缩进缓存是否正常工作"""
        from code_generator import PythonCodeGenerator

        generator = PythonCodeGenerator()

        indent0 = generator._get_indent(0)
        indent1 = generator._get_indent(1)
        indent2 = generator._get_indent(2)
        indent4 = generator._get_indent(4)

        assert indent0 == ''
        assert indent1 == '    '
        assert indent2 == '        '
        assert indent4 == '                '

        assert 0 in generator._indent_cache
        assert 1 in generator._indent_cache
        assert 2 in generator._indent_cache
        assert 4 in generator._indent_cache

        indent1_cached = generator._get_indent(1)
        assert indent1_cached == indent1

    def test_build_output_works(self):
        """测试 _build_output 方法是否正常工作"""
        from code_generator import PythonCodeGenerator
        from ast_nodes_v3 import Module, VarDecl, NumberLiteral

        module = Module([VarDecl('x', NumberLiteral(42))])
        generator = PythonCodeGenerator()
        code = generator.generate(module)

        assert code is not None
        assert 'x = 42' in code
        assert '\n' in code

    def test_output_consistency(self):
        """测试优化后的输出与预期一致"""
        from code_generator import PythonCodeGenerator
        from ast_nodes_v3 import Module, Paragraph, NumberLiteral, ReturnStmt

        functions = []
        for i in range(10):
            body = [ReturnStmt(NumberLiteral(i))]
            func = Paragraph(f'func_{i}', [], None, body)
            functions.append(func)

        module = Module(functions)
        generator = PythonCodeGenerator()
        code = generator.generate(module)

        lines = code.split('\n')
        assert len(lines) > 0

        for i in range(10):
            assert f'def func_{i}():' in code
            assert f'return {i}' in code


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
