"""
测试段言新语法：
1. 字符串索引
2. 循环控制（跳过/跳出）
"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

print("=" * 60)
print("段言新语法测试")
print("=" * 60)

# 测试用例
test_cases = [
    # 1. 字符串索引
    ('字符串索引', '定义甲等于文本【零】。'),
    
    # 2. 列表索引
    ('列表索引', '定义项等于数据【位置】。'),
    
    # 3. 循环控制 - 跳过
    ('跳过语句', '''遍历项在范围：
  如果项等于零那么跳过。
  打印项。
结束。'''),
    
    # 4. 循环控制 - 跳出
    ('跳出语句', '''遍历项在范围：
  如果项等于五那么跳出。
  打印项。
结束。'''),
]

parser = DuanParser()
generator = PythonCodeGenerator()

passed = 0
failed = 0

for name, code in test_cases:
    print(f"\n--- 测试: {name} ---")
    print(f"段言代码: {code[:50]}...")
    
    try:
        # 解析
        module = parser.parse(code)
        print(f"[OK] 解析成功")
        
        # 生成Python代码
        python_code = generator.generate(module)
        print(f"\nPython代码:")
        print(python_code)
        passed += 1
    except Exception as e:
        print(f"[FAIL] 失败")
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()
        failed += 1

print("\n" + "=" * 60)
print(f"测试完成: {passed} 通过, {failed} 失败")
print("=" * 60)
