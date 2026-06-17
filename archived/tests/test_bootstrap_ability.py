# 段言自举能力测试
# 测试当前段言语法能支持的自举功能

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

# 测试1：基础字典操作
test1 = '''
定义字典等于字典创建。
字典设置参数字典，"类型"，"标识符"。
字典设置参数字典，"值"，"甲"。
打印字典。
'''

# 测试2：列表操作
test2 = '''
定义列表等于列表创建。
列表追加参数列表，"定义"。
列表追加参数列表，"等于"。
打印列表。
打印列表长度参数列表。
'''

# 测试3：字符串操作
test3 = '''
定义文本等于"Hello"。
定义长度等于字符串长度参数文本。
打印长度。

定义部分等于分割字符串参数文本，"l"。
打印部分。
'''

# 测试4：类型检查
test4 = '''
定义甲等于123。
如果是整数参数甲那么
  打印"甲是整数"。

定义乙等于"Hello"。
如果是字符串参数乙那么
  打印"乙是字符串"。
'''

# 测试5：函数定义和使用
test5 = '''
《创建令牌》段(类型, 值)：
  定义令牌等于字典创建。
  字典设置参数令牌，"类型"，类型。
  字典设置参数令牌，"值"，值。
  返回令牌。

定义tok等于《创建令牌》参数"标识符"，"甲"。
打印tok。
定义类型等于字典获取参数tok，"类型"。
打印类型。
'''

tests = [
    ("字典操作", test1),
    ("列表操作", test2),
    ("字符串操作", test3),
    ("类型检查", test4),
    ("函数定义", test5),
]

print("=" * 60)
print("段言自举能力测试")
print("=" * 60)

parser = DuanParser()
generator = PythonCodeGenerator()

for name, code in tests:
    print(f"\n测试：{name}")
    print("-" * 60)
    print("段言代码：")
    print(code.strip())
    print()
    
    try:
        module = parser.parse(code)
        python_code = generator.generate(module)
        
        print("生成的Python代码：")
        print(python_code)
        
        # 尝试执行
        print("\n执行结果：")
        try:
            exec(python_code)
            print("[OK] 执行成功")
        except Exception as e:
            print(f"[FAIL] 执行失败: {e}")
    
    except Exception as e:
        print(f"[FAIL] 编译失败: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
