import sys
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

parser = DuanParser()

# 测试: 不带括号的 arity=0 函数
tests = [
    ("字典创建(无括号)", """段落 主():
    定义 d 等于 字典创建。
    字典设置(d, "key", "value")。
    打印输出(字典获取(d, "key"))。
结束。
"""),
    ("列表创建(无括号)", """段落 主():
    定义 lst 等于 列表创建。
    列表追加(lst, "a")。
    列表追加(lst, "b")。
    打印输出(列表长度(lst))。
结束。
"""),
    ("JSON 测试", """段落 主():
    定义 数据 等于 解析JSON("{\"name\": \"段言\"}")。
    打印输出(字典获取(数据, "name"))。
结束。
"""),
]

for name, source in tests:
    print(f"\n=== {name} ===")
    gen = PythonCodeGenerator()
    try:
        ast = parser.parse(source) if name.split('(')[0] != tests[-1][0].split('(')[0] else DuanParser().parse(source)
        if name == "JSON 测试":
            ast = DuanParser().parse(source)
        code = gen.generate(ast)
        code_to_run = code + "\n\n主()\n"
        result = __import__('subprocess').run(
            [sys.executable, '-c', code_to_run],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout:
            print("STDOUT:", result.stdout.strip())
        if result.stderr:
            print("STDERR:", result.stderr.strip())
        if not result.stdout and not result.stderr:
            print("(无输出)")
    except Exception as e:
        print(f"错误: {e}")
