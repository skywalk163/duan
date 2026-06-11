#!/usr/bin/env python
# -*- coding: utf-8 -*-

from antlrparser.duan_visitor import parse_source
from antlrparser.duan_interpreter import run_source

print("=== 测试基本解析 ===")

# 测试基本语句
source = "定义 x 等于 10。打印(x)。"
module = parse_source(source)
if module:
    print("基本语句解析成功!")
    print(f'语句数: {len(module.statements)}')
else:
    print("基本语句解析失败!")

print("\n=== 测试解释器 ===")
result = run_source("定义 x 等于 5加3。打印(x)。")
print(f'输出: {result.get_output()}')

print("\n=== 测试列表 ===")
result2 = run_source("定义 lst 等于 [1,2,3]。打印(listLen(lst))。")
print(f'输出: {result2.get_output()}')

print("\n=== 测试完成 ===")