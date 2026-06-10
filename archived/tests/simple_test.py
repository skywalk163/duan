# -*- coding: utf-8 -*-
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from duan_parser_v3 import DuanParser

print("Starting parser test...")
sys.stdout.flush()

parser = DuanParser()

# Test 1: Variable declaration
print("\nTest 1: Variable Declaration")
sys.stdout.flush()
result = parser.parse('定义甲等于三。')
print(f"  Statements: {len(result.statements)}")
for stmt in result.statements:
    print(f"  Type: {type(stmt).__name__}")
sys.stdout.flush()

print("\nTest completed!")
