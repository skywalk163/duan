# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator
from verb_info import get_verb_info

print("Testing verb info...")
sys.stdout.flush()

info = get_verb_info('加')
if info:
    print(f"Verb: 加, Arity: {info.arity}, Mode: {info.mode}")

info = get_verb_info('排序')
if info:
    print(f"Verb: 排序, Arity: {info.arity}, Mode: {info.mode}")

print("\nTesting compilation...")
sys.stdout.flush()

parser = DuanParser()
generator = PythonCodeGenerator()

code = '定义甲等于3。'
print(f"Duan: {code}")
module = parser.parse(code)
python_code = generator.generate(module)
print(f"Python:\n{python_code}")

print("\nTest completed!")
