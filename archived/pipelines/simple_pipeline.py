# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator

print("Testing complete pipeline...")
sys.stdout.flush()

# Test: Variable declaration
print("\n=== Test: Variable Declaration ===")
duan_code = '定义甲等于3。'
print(f"Duan: {duan_code}")

parser = DuanParser()
module = parser.parse(duan_code)
print(f"Parsed: {len(module.statements)} statements")

analyzer = SemanticAnalyzer()
success = analyzer.analyze(module)
print(f"Semantic analysis: {'OK' if success else 'FAIL'}")

generator = PythonCodeGenerator()
python_code = generator.generate(module)
print(f"Python:\n{python_code}")

sys.stdout.flush()

# Test: Function definition
print("\n=== Test: Function Definition ===")
duan_code = '《计算》段(甲, 乙)：返回甲加乙。'
print(f"Duan: {duan_code}")

module = parser.parse(duan_code)
print(f"Parsed: {len(module.statements)} statements")

analyzer = SemanticAnalyzer()
success = analyzer.analyze(module)
print(f"Semantic analysis: {'OK' if success else 'FAIL'}")

python_code = generator.generate(module)
print(f"Python:\n{python_code}")

sys.stdout.flush()

print("\nPipeline test completed!")
