#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
段言编程语言 - 类实例化和方法调用测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'antlrparser'))

from duan_visitor import parse_source
from duan_interpreter import run_source

print("=== 类实例化和方法调用测试 ===")

# 测试1: 基本类实例化
print("\n1. 基本类实例化测试")
source1 = """
【测试模块】
《人》类:
  定义 姓名 等于 ""。
  《说话》方法():
    打印(姓名)。
  结束。
结束。

定义 某人 等于 新 人()。
某人之姓名 等于 "张三"。
某人之说话()。
"""
result = run_source(source1)
print(f"   输出: {result.get_output().strip()}")

# 测试2: 带构造函数的类
print("\n2. 带构造函数的类测试")
source2 = """
【测试模块】
《人》类:
  《人》构造(名):
    姓名 等于 名。
  结束。
  定义 姓名 等于 ""。
  《说话》方法():
    打印(姓名)。
  结束。
结束。

定义 某人 等于 新 人("李四")。
某人之说话()。
"""
result = run_source(source2)
print(f"   输出: {result.get_output().strip()}")

# 测试3: 方法参数
print("\n3. 方法参数测试")
source3 = """
【测试模块】
《计算器》类:
  《加法》方法(数1, 数2):
    返回 数1加 数2。
  结束。
结束。

定义 calc 等于 新 计算器()。
定义 结果 等于 calc之加法(10, 20)。
打印(结果)。
"""
result = run_source(source3)
print(f"   输出: {result.get_output().strip()}")

# 测试4: 字段访问和修改
print("\n4. 字段访问和修改测试")
source4 = """
【测试模块】
《计数器》类:
  定义 值 等于 0。
  《增加》方法():
    值 等于 值加 1。
  结束。
  《获取》方法():
    返回 值。
  结束。
结束。

定义 cnt 等于 新 计数器()。
cnt之增加()。
cnt之增加()。
打印(cnt之获取())。
"""
result = run_source(source4)
print(f"   输出: {result.get_output().strip()}")

print("\n=== 所有测试完成 ===")