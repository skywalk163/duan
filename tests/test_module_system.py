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


class TestStdlibExpansion(unittest.TestCase):
    """标准库扩充测试"""
    
    def setUp(self):
        self.lexer = Lexer()
        self.parser = DuanParser()
        self.analyzer = SemanticAnalyzer()
        self.generator = PythonCodeGenerator()
    
    def compile_and_run(self, code: str) -> str:
        """编译并运行段言代码，返回标准输出"""
        import io
        import contextlib
        module = self.parser.parse(code)
        self.analyzer.analyze(module)
        python_code = self.generator.generate(module)
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec_globals = {'sys': sys, 'os': os}
                exec(python_code, exec_globals)
        except Exception as e:
            raise RuntimeError(
                f"执行错误: {e}\n"
                f"生成的Python代码:\n{python_code}"
            ) from e
        return output.getvalue().strip()
    
    # ===== 正则表达式模块 =====
    
    def test_regex_match(self):
        """从《正则》导入《匹配》"""
        code = r'从《正则》导入《匹配》。设 甲 为 匹配 "hello" "hello world"。打印 甲["匹配"]。'
        output = self.compile_and_run(code)
        self.assertEqual(output, 'hello')
    
    def test_regex_search(self):
        """从《正则》导入《搜索》"""
        code = r'从《正则》导入《搜索》。设 甲 为 搜索 "world" "hello world"。打印 甲["匹配"]。'
        output = self.compile_and_run(code)
        self.assertEqual(output, 'world')
    
    def test_regex_findall(self):
        """从《正则》导入《全部匹配》"""
        code = r'从《正则》导入《全部匹配》。设 甲 为 全部匹配 "a" "banana"。打印 字符串长度 甲。打印 甲[0] 加 甲[1] 加 甲[2]。'
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[0], '3')
        self.assertEqual(lines[1], 'aaa')
    
    def test_regex_replace(self):
        """从《正则》导入《替换》"""
        code = r'从《正则》导入《替换》。设 甲 为 替换 "na" "XY" "banana"。打印 甲。'
        output = self.compile_and_run(code)
        self.assertEqual(output, 'baXYXY')
    
    def test_regex_escape(self):
        """从《正则》导入《转义》"""
        code = r'从《正则》导入《转义》。设 甲 为 转义 "a.b" 。打印 甲。'
        output = self.compile_and_run(code)
        self.assertIn(r'a\.b', output)
    
    def test_regex_is_match(self):
        """从《正则》导入《是否匹配》"""
        code = r'从《正则》导入《是否匹配》。打印 是否匹配 "abc" "abc"。打印 是否匹配 "abc" "ab"。'
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[0], 'True')
        self.assertEqual(lines[1], 'False')
    
    # ===== 编码模块 =====
    
    def test_base64_encode_decode(self):
        """从《编码》导入《Base64编码》《Base64解码》"""
        code = '''
从《编码》导入《Base64编码》，《Base64解码》。
设 甲 为 Base64编码 "你好"。
设 乙 为 Base64解码 甲。
打印 甲。
打印 乙。
'''
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[1], '你好')
    
    def test_md5_hash(self):
        """从《编码》导入《MD5哈希》"""
        code = '''
从《编码》导入《MD5哈希》。
设 甲 为 MD5哈希 "hello"。
打印 字符串长度 甲。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, '32')
    
    def test_hex_encode_decode(self):
        """从《编码》导入《Hex编码》《Hex解码》"""
        code = '''
从《编码》导入《Hex编码》，《Hex解码》。
设 甲 为 Hex编码 "AB"。
设 乙 为 Hex解码 甲。
打印 甲。
打印 乙。
'''
        output = self.compile_and_run(code)
        lines = output.split('\n')
        self.assertEqual(lines[0], '4142')
        self.assertEqual(lines[1], 'AB')
    
    # ===== 数学统计函数 =====
    
    def test_stat_mean(self):
        """从《数学》导入《平均数》"""
        code = '''
从《数学》导入《平均数》。
设 数据 为 列 1 2 3 4 5。
设 甲 为 平均数 数据。
打印 甲。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, '3')
    
    def test_stat_median(self):
        """从《数学》导入《中位数》"""
        code = '''
从《数学》导入《中位数》。
设 数据 为 列 1 3 5 7 9。
设 甲 为 中位数 数据。
打印 甲。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, '5')
    
    def test_stat_sum(self):
        """从《数学》导入《求和》"""
        code = '''
从《数学》导入《求和》。
设 数据 为 列 10 20 30。
设 甲 为 求和 数据。
打印 甲。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, '60')
    
    def test_stat_stdev(self):
        """从《数学》导入《标准差》"""
        code = '''
从《数学》导入《标准差》。
设 数据 为 列 1 1 1 1。
设 甲 为 标准差 数据。
打印 甲。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, '0.0')
    
    # ===== 时间新函数 =====
    
    def test_time_weekday(self):
        """从《时间》导入《星期几》"""
        code = '''
从《时间》导入《星期几》。
设 甲 为 星期几。
打印 甲 大于等于 0 与 甲 小于等于 6。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, 'True')
    
    def test_time_day_name(self):
        """从《时间》导入《星期名称》"""
        code = '''
从《时间》导入《星期名称》。
设 甲 为 星期名称。
打印 甲。
'''
        output = self.compile_and_run(code)
        self.assertIn(output, ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
    
    def test_time_days_after(self):
        """从《时间》导入《N天后》《星期几》"""
        code = '''
从《时间》导入《N天后》，《星期几》。
设 今天为 星期几。
设 七天后为 星期几 N天后 7。
打印 七天后 等于 今天。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, 'True')
    
    def test_time_is_weekday(self):
        """从《时间》导入《是否工作日》"""
        code = '''
从《时间》导入《是否工作日》，《是否周末》。
设 今天工作 为 是否工作日。
设 今天周末 为 是否周末。
打印 今天工作 不等于 今天周末。
'''
        output = self.compile_and_run(code)
        self.assertEqual(output, 'True')


if __name__ == '__main__':
    unittest.main(verbosity=2)