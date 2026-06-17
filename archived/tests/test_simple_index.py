"""
简单测试字符串索引语法
"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

print("=" * 60)
print("字符串索引语法测试")
print("=" * 60)

# 测试1: 字符串索引
code1 = '定义甲等于文本【零】。'

print(f"\n段言代码: {code1}")

parser = DuanParser()
generator = PythonCodeGenerator()

try:
    # 解析
    module = parser.parse(code1)
    print(f"[OK] 解析成功")
    
    # 生成Python代码
    python_code = generator.generate(module)
    print(f"\nPython代码:")
    print(python_code)
except Exception as e:
    print(f"[FAIL] 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: 列表索引
code2 = '定义项等于数据【位置】。'

print(f"\n\n段言代码: {code2}")

try:
    module = parser.parse(code2)
    print(f"[OK] 解析成功")
    
    python_code = generator.generate(module)
    print(f"\nPython代码:")
    print(python_code)
except Exception as e:
    print(f"[FAIL] 失败: {e}")
    import traceback
    traceback.print_exc()
