#!/usr/bin/env python
# -*- coding: utf-8 -*-

from antlrparser.duan_visitor import parse_source
from antlrparser.duan_interpreter import run_source

print("=== 测试类和接口解析 ===")

source = """
【测试模块】
《人》类:
  定义 姓名 等于 ""。
  《说话》方法():
    打印(姓名)。
  结束。
结束。

《可飞行》接口:
  《飞》方法() -> 空。
结束。
"""

module = parse_source(source)
print(f'模块名: {module.name}')
print(f'类数量: {len(module.classes)}')
print(f'接口数量: {len(module.interfaces)}')

if module.classes:
    cls = module.classes[0]
    print(f'类名: {cls.name}')
    print(f'字段数: {len(cls.fields)}')
    print(f'方法数: {len(cls.methods)}')
    if cls.methods:
        print(f'方法名: {cls.methods[0].name}')

if module.interfaces:
    iface = module.interfaces[0]
    print(f'接口名: {iface.name}')
    print(f'方法签名数: {len(iface.methods)}')

print("\n=== 测试解释器执行 ===")

result = run_source("""
定义 x 等于 10。
定义 y 等于 20。
打印(x加y)。

定义 列表 等于 [1, 2, 3]。
打印(listLen(列表))。
""")

print(f'输出:\n{result.get_output()}')

print("\n=== 所有测试通过 ===")
