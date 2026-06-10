#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试模块系统"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

# 测试1: 导出语句
print("="*60)
print("测试1: 导出语句")
print("="*60)
code1 = '导出《平方》，《立方》。'
parser = DuanParser()
generator = PythonCodeGenerator()
module1 = parser.parse(code1)
py1 = generator.generate(module1)
print(f"段言: {code1}")
print(f"Python:\n{py1}\n")

# 测试2: 导入语句
print("="*60)
print("测试2: 导入语句")
print("="*60)
code2 = '导入《数学库》。'
module2 = parser.parse(code2)
py2 = generator.generate(module2)
print(f"段言: {code2}")
print(f"Python:\n{py2}\n")

# 测试3: 从...导入
print("="*60)
print("测试3: 从...导入")
print("="*60)
code3 = '从《math_utils》导入《平方》，《立方》。'
module3 = parser.parse(code3)
py3 = generator.generate(module3)
print(f"段言: {code3}")
print(f"Python:\n{py3}\n")

# 测试4: 完整模块
print("="*60)
print("测试4: 完整模块")
print("="*60)
code4 = '''导出《平方》。
《平方》段(数)：
  返回数乘数。
'''
module4 = parser.parse(code4)
py4 = generator.generate(module4)
print(f"段言:\n{code4}")
print(f"Python:\n{py4}\n")

print("="*60)
print("[OK] 所有基础测试通过")
print("="*60)
