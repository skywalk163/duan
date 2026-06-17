#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')
sys.path.insert(0, 'antlrparser')

from tests.test_suite import TestDuanCompiler
t = TestDuanCompiler()
try:
    output = t.run_duan_code('''
设 甲 为 10。
设 乙 为 "测试"。
打印(甲)。
打印(乙)。
''')
    print('Output:', repr(output))
except Exception as e:
    print('Error:', e)