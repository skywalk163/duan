#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试模块解析器"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from module_resolver import ModuleResolver

print("="*60)
print("模块解析器快速测试")
print("="*60)

# 创建解析器
resolver = ModuleResolver(search_paths=['examples/modules'])

# 测试1: 查找模块
print("\n1. 测试查找模块")
try:
    path = resolver.find_module('math_utils')
    print(f"   [OK] 找到: {path}")
except Exception as e:
    print(f"   [FAIL] {e}")
    sys.exit(1)

# 测试2: 解析单个模块
print("\n2. 测试解析模块")
try:
    module = resolver.parse_module(path)
    print(f"   [OK] 模块名: {module.name}")
    print(f"        依赖: {module.dependencies}")
    print(f"        导出: {module.exports}")
except Exception as e:
    print(f"   [FAIL] {e}")
    sys.exit(1)

# 测试3: 构建依赖图
print("\n3. 测试构建依赖图")
try:
    graph = resolver.build_dependency_graph('main', 'examples/modules')
    print(f"   [OK] 节点数: {len(graph.nodes)}")
    for name in sorted(graph.nodes.keys()):
        info = graph.nodes[name]
        print(f"        - {name} (依赖: {info.dependencies})")
except Exception as e:
    print(f"   [FAIL] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4: 拓扑排序
print("\n4. 测试拓扑排序")
try:
    order = resolver.topological_sort(graph)
    print(f"   [OK] 编译顺序: {' -> '.join(order)}")
except Exception as e:
    print(f"   [FAIL] {e}")
    sys.exit(1)

print("\n" + "="*60)
print("[OK] 所有测试通过")
print("="*60)
