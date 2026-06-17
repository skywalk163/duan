"""
测试循环控制语句：跳过/跳出
"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

print("=" * 60)
print("循环控制语句测试")
print("=" * 60)

# 测试1: 简单的跳出语句
code1 = '跳出。'

print(f"\n段言代码: {code1}")

parser = DuanParser()
generator = PythonCodeGenerator()

try:
    module = parser.parse(code1)
    print(f"[OK] 解析成功")
    print(f"AST: {module.statements[0]}")
    
    python_code = generator.generate(module)
    print(f"\nPython代码:")
    print(python_code)
except Exception as e:
    print(f"[FAIL] 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: 简单的跳过语句
code2 = '跳过。'

print(f"\n\n段言代码: {code2}")

try:
    module = parser.parse(code2)
    print(f"[OK] 解析成功")
    print(f"AST: {module.statements[0]}")
    
    python_code = generator.generate(module)
    print(f"\nPython代码:")
    print(python_code)
except Exception as e:
    print(f"[FAIL] 失败: {e}")
    import traceback
    traceback.print_exc()
