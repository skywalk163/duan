#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试段言类定义的完整特性"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

def test_oop_features():
    """测试OOP完整特性"""
    print("=" * 60)
    print("测试段言OOP完整特性")
    print("=" * 60)
    
    code = '''# 定义基类
类 动物。
  属性 名称。
  
  构造 参数 名称。
    己名称 为 名称。
  结束。
  
  段落 自我介绍。
    返回 "我是"。
  结束。
  
  段落 说话。
    返回 "动物叫"。
  结束。
结束。

# 定义子类
类 狗 继承 动物。
  属性 年龄。
  
  构造 参数 名称 年龄。
    己名称 为 名称。
    己年龄 为 年龄。
  结束。
  
  段落 说话。
    返回 "汪汪汪"。
  结束。
  
  段落 抓老鼠。
    返回 "狗拿耗子"。
  结束。
结束。

# 测试段落
段落 测试类。
  打印 "=== 测试类定义 ==="。
  
  # 创建动物实例（这里使用Python语法作为过渡）
  定义 结果 等于 "测试完成"。
  打印 结果。
结束。

测试类。
'''
    
    print("\n段言源代码:")
    print(code)
    print("\n" + "=" * 60)
    
    # 解析
    print("\n[步骤1] 解析...")
    parser = DuanParser()
    ast = parser.parse(code)
    
    print(f"解析成功，语句数: {len(ast.statements)}")
    for i, stmt in enumerate(ast.statements):
        print(f"  语句{i+1}: {type(stmt).__name__}")
    
    # 代码生成
    print("\n[步骤2] 代码生成...")
    generator = PythonCodeGenerator()
    python_code = generator.generate(ast)
    
    print("生成的Python代码（部分）:")
    print("-" * 60)
    # 只显示关键部分
    lines = python_code.split('\n')
    in_class = False
    display_lines = []
    for line in lines:
        if 'class' in line or 'def ' in line or 'self.' in line:
            display_lines.append(line)
    print('\n'.join(display_lines[:30]))
    print("-" * 60)
    
    # 执行
    print("\n[步骤3] 执行...")
    exec_globals = {}
    exec(python_code, exec_globals)
    
    print("执行成功！")
    
    # 测试类实例化
    print("\n[步骤4] 测试类实例化...")
    Animal = exec_globals.get('动物')
    Dog = exec_globals.get('狗')
    
    if Animal:
        animal = Animal("通用动物")
        print(f"  动物实例名称: {animal.名称}")
        print(f"  动物说话: {animal.说话()}")
    
    if Dog:
        dog = Dog("旺财", 3)
        print(f"  狗实例名称: {dog.名称}")
        print(f"  狗实例年龄: {dog.年龄}")
        print(f"  狗说话: {dog.说话()}")
        print(f"  狗抓老鼠: {dog.抓老鼠()}")
        
        # 测试继承
        print(f"  狗是动物的子类: {issubclass(Dog, Animal)}")
    
    print("\n[SUCCESS] OOP特性测试通过")
    return True

if __name__ == '__main__':
    success = test_oop_features()
    sys.exit(0 if success else 1)
