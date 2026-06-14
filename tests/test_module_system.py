"""
段言 - 模块系统和标准库综合测试
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator
from semantic_analyzer import SemanticAnalyzer


class TestStdlib(unittest.TestCase):
    """标准库模块测试"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = DuanParser()
        self.analyzer = SemanticAnalyzer()
        self.generator = PythonCodeGenerator()
    
    def compile_and_run(self, code: str, timeout: float = 5) -> str:
        """编译并运行段言代码，返回标准输出"""
        import io
        import contextlib
        
        # 编译
        module = self.parser.parse(code)
        self.analyzer.analyze(module)
        python_code = self.generator.generate(module)
        
        # 运行
        output = io.StringIO()
        _duan_builtin = None
        
        try:
            with contextlib.redirect_stdout(output):
                exec_globals = {
                    'sys': sys,
                    'os': os,
                }
                exec(python_code, exec_globals)
                _duan_builtin = exec_globals.get('_duan_builtin')
        except Exception as e:
            raise RuntimeError(
                f"执行错误: {e}\n"
                f"生成的Python代码:\n{python_code}"
            ) from e
        
        return output.getvalue().strip()
    
    def test_import_math_abs(self):
        """从《数学》导入《绝对值》"""
        code = """
从《数学》导入《绝对值》。
设 甲 为 绝对值 -5。
打印 甲。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, '5')
    
    def test_import_math_sqrt(self):
        """从《数学》导入《平方根》"""
        code = """
从《数学》导入《平方根》。
设 甲 为 平方根 九。
打印 甲。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, '3.0')
    
    def test_import_math_pow(self):
        """从《数学》导入《幂》"""
        code = """
从《数学》导入《幂》。
设 甲 为 幂 二 十。
打印 甲。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, '1024')
    
    def test_import_math_random(self):
        """从《数学》导入《随机整数》"""
        code = """
从《数学》导入《随机整数》。
设 甲 为 随机整数 一 一百。
打印 甲 大于 零 与 甲 小于 一百零一。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, 'True')
    
    def test_import_math_round(self):
        """从《数学》导入《四舍五入》"""
        code = """
从《数学》导入《四舍五入》。
设 甲 为 四舍五入 三点一四一五九 二。
打印 甲。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, '3.14')
    
    def test_import_time_sleep(self):
        """从《时间》导入《暂停》《计时开始》《计时结束》"""
        code = """
从《时间》导入《计时开始》，《计时结束》，《暂停》。
设 开始 为 计时开始。
暂停 零点一。
设 耗时 为 计时结束 开始。
打印 耗时 大于 零点零五。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, 'True')
    
    def test_import_time_format(self):
        """从《时间》导入《当前日期》"""
        code = """
从《时间》导入《当前日期》。
设 日期 为 当前日期。
打印 字符串长度 日期。
"""
        output = self.compile_and_run(code)
        self.assertEqual(output, '10')  # YYYY-MM-DD
    
    def test_mixed_stdlib_builtins(self):
        """混合使用内置函数和标准库"""
        code = """
从《数学》导入《平方根》，《幂》。
设 甲 为 幂 三 四。
设 乙 为 平方根 十六。
打印 甲。
打印 乙。
"""
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[0], '81')
        self.assertEqual(lines[1], '4.0')
    
    def test_import_with_multiple_symbols(self):
        """从同一模块导入多个符号"""
        code = """
从《数学》导入《绝对值》，《最大值》，《最小值》。
设 甲 为 绝对值 -10。
设 乙 为 最大值 五 八。
设 丙 为 最小值 三 七。
打印 甲。
打印 乙。
打印 丙。
"""
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[0], '10')
        self.assertEqual(lines[1], '8')
        self.assertEqual(lines[2], '3')
    
    def test_module_resolver_find(self):
        """测试模块解析器能找到stdlib模块"""
        from module_resolver import ModuleResolver, ModuleNotFoundError
        
        resolver = ModuleResolver()
        
        # 应该能找到 数学 模块
        math_path = resolver.find_module('数学')
        self.assertTrue(math_path.exists())
        self.assertIn('数学', str(math_path))
        
        # 应该能找到 时间 模块
        time_path = resolver.find_module('时间')
        self.assertTrue(time_path.exists())
        self.assertIn('时间', str(time_path))
        
        # 不存在模块应抛出异常
        with self.assertRaises(ModuleNotFoundError):
            resolver.find_module('不存在的模块')


class TestModuleSystem(unittest.TestCase):
    """模块系统解析器测试"""
    
    def test_resolver_basic(self):
        """测试模块解析器基本功能"""
        from module_resolver import ModuleResolver
        
        resolver = ModuleResolver()
        
        # 解析 数学 模块
        math_info = resolver.parse_module(resolver.find_module('数学'))
        self.assertEqual(math_info.name, '数学')
        self.assertTrue(len(math_info.exports) > 0)
    
    def test_resolver_build_graph(self):
        """测试依赖图构建"""
        from module_resolver import ModuleResolver
        
        resolver = ModuleResolver()
        resolver.parse_module(resolver.find_module('数学'))
        
        graph = resolver.build_dependency_graph('数学')
        self.assertIn('数学', graph.nodes)
    
    def test_topological_sort(self):
        """测试拓扑排序"""
        from module_resolver import ModuleResolver
        
        resolver = ModuleResolver()
        resolver.parse_module(resolver.find_module('数学'))
        resolver.parse_module(resolver.find_module('时间'))
        
        # 独立模块，排序无顺序要求
        graph = resolver.build_dependency_graph('数学')
        order = resolver.topological_sort(graph)
        self.assertIn('数学', order)


if __name__ == '__main__':
    unittest.main(verbosity=2)