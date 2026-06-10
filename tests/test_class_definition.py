# -*- coding: utf-8 -*-
"""
段言编译器 - 类定义功能测试

测试类定义的解析和代码生成
"""

import sys
import os
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ast_nodes import (
    ClassDefinition, AttributeDeclaration, MethodDefinition,
    Parameter, Module, Identifier
)
from code_generator import PythonCodeGenerator


def test_class_definition_generation():
    """测试类定义代码生成"""
    print("=" * 60)
    print("段言编译器 - 类定义功能测试")
    print("=" * 60)
    
    # 创建一个简单的学生类AST
    student_class = ClassDefinition(
        line=1,
        column=1,
        name='学生',
        base_class=None,
        attributes=[
            AttributeDeclaration(
                line=2,
                column=3,
                name='姓名',
                type_annotation='str',  # 使用Python类型
                default_value=None
            ),
            AttributeDeclaration(
                line=3,
                column=3,
                name='年龄',
                type_annotation='int',  # 使用Python类型
                default_value=None
            ),
        ],
        methods=[
            MethodDefinition(
                line=5,
                column=3,
                name='构造',
                parameters=[
                    Parameter(line=5, column=6, name='姓名'),
                    Parameter(line=5, column=9, name='年龄'),
                ],
                body=[
                    ('var', 'self.姓名', Identifier(line=6, column=5, name='姓名')),
                    ('var', 'self.年龄', Identifier(line=7, column=5, name='年龄')),
                ],
                is_constructor=True
            ),
            MethodDefinition(
                line=9,
                column=3,
                name='介绍',
                parameters=[],
                body=[
                    ('return', None),
                ],
                is_constructor=False
            ),
        ]
    )
    
    # 创建模块
    module = Module(
        line=1,
        column=1,
        name=None,
        imports=[],
        exports=[],
        segments=[],
        statements=[student_class]
    )
    
    # 生成Python代码
    generator = PythonCodeGenerator()
    python_code = generator.generate(module)
    
    print("\n生成的Python代码：")
    print("-" * 60)
    print(python_code)
    print("-" * 60)
    
    # 验证生成的代码
    assert 'class 学生:' in python_code, "应该包含类定义"
    assert 'def __init__(self, 姓名, 年龄):' in python_code, "应该包含构造函数"
    assert 'def 介绍(self):' in python_code, "应该包含方法定义"
    
    print("\n✅ 测试通过！")
    
    # 尝试执行生成的代码
    print("\n尝试执行生成的代码：")
    print("-" * 60)
    try:
        exec_globals = {}
        exec(python_code, exec_globals)
        print("✅ 代码执行成功！")
        
        # 创建实例
        if '学生' in exec_globals:
            student = exec_globals['学生']('张三', 20)
            print(f"✅ 成功创建实例：{student}")
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_class_definition_generation()
