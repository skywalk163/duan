#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')
sys.path.insert(0, 'antlrparser')

from antlrparser.duan_visitor import parse_source

code = '''
段落 平方 接收 数值:
    返回 数值 * 数值。
结束。
'''

module = parse_source(code)
print('Module:', module)
if module:
    print('Segments:', module.segments if hasattr(module, 'segments') else 'N/A')