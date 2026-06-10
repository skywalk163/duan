# -*- coding: utf-8 -*-
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

print("Testing Python code generator...")
sys.stdout.flush()

# Test 1: Variable declaration
print("\n=== Test 1: Variable Declaration ===")
parser = DuanParser()
generator = PythonCodeGenerator()

code = '定义甲等于三。'
print(f"Duan code: {code}")
module = parser.parse(code)
python_code = generator.generate(module)
print(f"Python code:\n{python_code}")
sys.stdout.flush()

# Test 2: Binary operation
print("\n=== Test 2: Binary Operation ===")
code = '定义丙等于三加五。'
print(f"Duan code: {code}")
module = parser.parse(code)
python_code = generator.generate(module)
print(f"Python code:\n{python_code}")
sys.stdout.flush()

# Test 3: Function definition
print("\n=== Test 3: Function Definition ===")
code = '《计算》段(甲, 乙)：返回甲加乙。'
print(f"Duan code: {code}")
module = parser.parse(code)
python_code = generator.generate(module)
print(f"Python code:\n{python_code}")
sys.stdout.flush()

print("\nAll tests completed!")
