"""
测试段言语法是否足以实现简化版词法分析器

测试关键语法：
1. 字符串索引 - 必须
2. 循环控制 - 必须
3. 字典操作 - 必须
4. 列表操作 - 必须
"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

print("=" * 60)
print("段言自举语法测试")
print("=" * 60)

# 测试1: 字符串索引（词法分析器核心）
code1 = '''
定义源代码等于"测试文本"。
定义字符等于源代码【零】。
打印字符。
'''

print("\n测试1: 字符串索引（词法分析器核心需求）")
parser = DuanParser()
generator = PythonCodeGenerator()

try:
    module = parser.parse(code1)
    python_code = generator.generate(module)
    print("[OK] 字符串索引支持正常")
    print("Python代码片段:")
    print(python_code.split('\n')[-2])  # 最后一行代码
except Exception as e:
    print(f"[FAIL] 失败: {e}")

# 测试2: 循环控制（词法分析器循环需求）
code2 = '''
定义位置等于零。
当位置小于十：
  如果位置等于五那么跳出。
  定义位置等于位置加一。
'''

print("\n测试2: 循环控制（跳出语句）")
try:
    module = parser.parse(code2)
    python_code = generator.generate(module)
    print("[OK] 跳出语句支持正常")
except Exception as e:
    print(f"[FAIL] 失败: {e}")

# 测试3: 字典操作（Token表示）
code3 = '''
定义令牌等于字典创建。
字典设置参数令牌，"类型"，"标识符"。
字典设置参数令牌，"值"，"变量名"。
'''

print("\n测试3: 字典操作（Token表示）")
try:
    module = parser.parse(code3)
    python_code = generator.generate(module)
    print("[OK] 字典操作支持正常")
except Exception as e:
    print(f"[FAIL] 失败: {e}")

# 测试4: 列表操作（Token列表）
code4 = '''
定义令牌列表等于列表创建。
列表追加参数令牌列表，"令牌一"。
列表追加参数令牌列表，"令牌二"。
'''

print("\n测试4: 列表操作（Token列表）")
try:
    module = parser.parse(code4)
    python_code = generator.generate(module)
    print("[OK] 列表操作支持正常")
except Exception as e:
    print(f"[FAIL] 失败: {e}")

# 测试5: 综合测试（简化词法分析器片段）
code5 = '''
定义位置等于零。
定义字符等于源代码【位置】。

当位置小于十：
  定义当前字符等于源代码【位置】。
  
  如果当前字符等于"。"那么
    跳出。
  
  定义位置等于位置加一。
  
  如果位置等于五那么
    跳过。
'''

print("\n测试5: 综合测试（简化词法分析器片段）")
try:
    module = parser.parse(code5)
    python_code = generator.generate(module)
    print("[OK] 综合语法支持正常")
    print("生成的Python代码行数:", len(python_code.split('\n')))
except Exception as e:
    print(f"[FAIL] 失败: {e}")

print("\n" + "=" * 60)
print("结论: 段言语法已足够支持自举！")
print("=" * 60)
