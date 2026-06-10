#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

code = '定义甲等于三。打印甲。'

print("测试段言编译和运行...")
print("源代码:", code)

parser = DuanParser()
module = parser.parse(code)
print("解析成功")

generator = PythonCodeGenerator()
python_code = generator.generate(module)
print("生成Python代码成功")
print("\nPython代码:")
print(python_code)

print("\n执行:")
exec(python_code)

print("\n测试完成")
