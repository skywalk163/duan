#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
段言编程语言 - 完整功能测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'antlrparser'))

from duan_visitor import parse_source
from duan_interpreter import run_source

print("=== 段言语言完整功能测试 ===")

# 1. 测试基本解析
print("\n1. 基本解析测试")
source1 = "定义 x 等于 10。打印(x)。"
module = parse_source(source1)
print(f"   ✓ 基本语句解析成功 (语句数: {len(module.statements)})")

# 2. 测试解释器
print("\n2. 解释器测试")
result = run_source("定义 x 等于 5加3。打印(x)。")
print(f"   ✓ 解释器执行成功 (输出: {result.get_output().strip()})")

# 3. 测试列表操作
print("\n3. 列表操作测试")
result2 = run_source("定义 lst 等于 [1,2,3]。打印(listLen(lst))。")
print(f"   ✓ 列表操作成功 (输出: {result2.get_output().strip()})")

# 4. 测试类定义
print("\n4. 类定义解析测试")
source4 = """
【测试】
《人》类:
  定义 姓名 等于 ""。
  《说话》方法():
    打印(姓名)。
  结束。
结束。
"""
module4 = parse_source(source4)
print(f"   ✓ 类定义解析成功 (类名: {module4.classes[0].name}, 字段: {[f.name for f in module4.classes[0].fields]})")

# 5. 测试接口定义
print("\n5. 接口定义解析测试")
source5 = """
【测试】
《可飞行》接口:
  《飞》方法() -> 空。
结束。
"""
module5 = parse_source(source5)
print(f"   ✓ 接口定义解析成功 (接口名: {module5.interfaces[0].name}, 方法: {[m.name for m in module5.interfaces[0].methods]})")

# 6. 测试类实现接口
print("\n6. 类实现接口测试")
source6 = """
【测试】
《人》类 使用 可飞行:
  定义 姓名 等于 ""。
  《飞》方法():
    打印(姓名 + "正在飞")。
  结束。
结束。
"""
module6 = parse_source(source6)
print(f"   ✓ 类实现接口成功 (类名: {module6.classes[0].name}, 实现接口: {module6.classes[0].interfaces})")

print("\n=== 所有测试通过 ===")