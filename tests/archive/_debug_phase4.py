"""Debug auto_close_blocks"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.join('.', 'src'))
from antlrparser.duan_visitor import DuanParser

p = DuanParser()

# Test 1: if without end
s1 = '设 甲 为 10。如果 甲 大于 5：打印 "大"。则 设 乙 为 20。打印 乙。'
print('Test 1 (if):')
print('  Before:', repr(s1[:60]))
r1 = p._auto_close_blocks(s1)
print('  After:', repr(r1[:80]))
print()

# Test 2: multiple stmts
s2 = '设 列表 为 [1, 2]。对 元素 中的 列表：打印 元素。设 和 为 0。遍历 数 中的 列表：设 和 为 和 加 数。打印 和。'
print('Test 2 (multi):')
print('  Before:', repr(s2[:80]))
r2 = p._auto_close_blocks(s2)
print('  After:', repr(r2[:120]))