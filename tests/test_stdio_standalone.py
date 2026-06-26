import sys
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from code_generator import PythonCodeGenerator
from duan_parser_v3 import DuanParser

parser = DuanParser()
gen = PythonCodeGenerator()

source = """段落 主():
    定义 消息 等于 "段言IO测试-开始"。
    打印输出(消息)。
    打印输出("等待输入...")。
    定义 用户行 等于 读取行()。
    打印输出(用户行)。
"""

raw_ast = parser.parse(source)
python_code = gen.generate(raw_ast)

# 打印全部生成的代码
print("=== 生成的Python代码 ===")
print(python_code)
print("=== 结束 ===\n")

# 检查是否调用了 主()
if "主()" in python_code:
    print("✓ 主() 被调用了")
else:
    print("✗ 主() 未被调用！")

# 手动在生成的代码末尾添加主()调用，然后执行
code_to_run = python_code + "\n\n主()\n"
print("\n=== 带主()调用的执行测试 (输入='你好段言') ===")

import subprocess
result = subprocess.run(
    [sys.executable, '-c', code_to_run],
    input='你好段言\n',
    capture_output=True,
    text=True,
    timeout=10
)
print("STDOUT:", repr(result.stdout))
print("STDERR:", repr(result.stderr))
print("RETURN CODE:", result.returncode)
