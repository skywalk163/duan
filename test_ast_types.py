#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'antlrparser')

from duan_visitor import parse_source
from duan_ast import NewExpression, PropertyAccess, SelfReference

# 测试代码
code = """设 旺财 为 新建 狗("旺财")。
旺财.叫()。
"""

print("=== 检查AST节点类型 ===")
module = parse_source(code)

if module:
    for stmt in module.statements:
        print(f"语句类型: {type(stmt).__name__}")
        if hasattr(stmt, 'value'):
            print(f"  值类型: {type(stmt.value).__name__}")
            if hasattr(stmt.value, 'obj'):
                print(f"    对象类型: {type(stmt.value.obj).__name__}")
                if hasattr(stmt.value.obj, 'obj'):
                    print(f"      内层对象类型: {type(stmt.value.obj.obj).__name__}")
                    print(f"      类名: {stmt.value.obj.obj.class_name}")

# 检查定义的类型
print("\n=== 检查定义的类型 ===")
print(f"NewExpression: {NewExpression}")
print(f"PropertyAccess: {PropertyAccess}")
print(f"SelfReference: {SelfReference}")
