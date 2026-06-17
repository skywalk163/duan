#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser')
sys.path.insert(0, 'src')

from duan_visitor import parse_source

# 测试类定义
code = """类 狗:
    属性 名字。
    
    构造(名字):
        己.名字 = 名字。
    结束。
    
    段落 叫:
        打印(己.名字)。
    结束。
结束。

设 旺财 为 新建 狗("旺财")。
旺财.叫()。
"""

print("=== 测试 AST 解析 ===")
print("源代码:")
print(code)

# 解析
module = parse_source(code)
if not module:
    print("\n解析失败!")
    sys.exit(1)

# 打印模块结构
print("\n模块结构:")
print(f"类定义数量: {len(module.classes)}")
print(f"语句数量: {len(module.statements)}")

# 打印类定义
for cls in module.classes:
    print(f"\n类: {cls.name}")
    print(f"  字段: {[f.name for f in cls.fields]}")
    print(f"  方法: {[m.name for m in cls.methods]}")
    if cls.constructor:
        print(f"  构造函数参数: {[p.name for p in cls.constructor.parameters]}")

# 打印语句
print("\n语句:")
for i, stmt in enumerate(module.statements):
    print(f"  {i}: {type(stmt).__name__}")
    if hasattr(stmt, 'name'):
        print(f"      name: {stmt.name}")
    if hasattr(stmt, 'value'):
        print(f"      value: {type(stmt.value).__name__}")
        if hasattr(stmt.value, 'class_name'):
            print(f"          class_name: {stmt.value.class_name}")
        if hasattr(stmt.value, 'arguments'):
            print(f"          arguments: {[type(arg).__name__ for arg in stmt.value.arguments]}")
    if hasattr(stmt, 'expression'):
        print(f"      expression: {type(stmt.expression).__name__}")
        expr = stmt.expression
        if hasattr(expr, 'obj'):
            print(f"          obj: {type(expr.obj).__name__}")
            if hasattr(expr.obj, 'name'):
                print(f"              obj.name: {expr.obj.name}")
        if hasattr(expr, 'property_name'):
            print(f"          property_name: {expr.property_name}")
        if hasattr(expr, 'method'):
            print(f"          method: {expr.method}")
        if hasattr(expr, 'name'):
            print(f"          name: {type(expr.name).__name__}")
            if hasattr(expr.name, 'property_name'):
                print(f"              name.property_name: {expr.name.property_name}")
            if hasattr(expr.name, 'obj'):
                print(f"              name.obj: {type(expr.name.obj).__name__}")
                if hasattr(expr.name.obj, 'name'):
                    print(f"                  name.obj.name: {expr.name.obj.name}")
        if hasattr(expr, 'arguments'):
            print(f"          arguments: {[type(arg).__name__ for arg in expr.arguments]}")
