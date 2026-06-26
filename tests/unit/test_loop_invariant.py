# -*- coding: utf-8 -*-
"""
循环不变量外提优化器单元测试

测试 LoopInvariantOptimizer 的各项功能。
"""

import sys
import os
import unittest

# 添加项目路径
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
sys.path.insert(0, _src_dir)

from ast_nodes import (
    NumberLiteral, StringLiteral, BooleanLiteral,
    Identifier, Module, VariableDeclaration, Assignment,
    WhileStatement, ForeachStatement,
)
from optimizer.loop_invariant import LoopInvariantOptimizer


class TestLoopInvariantOptimizer(unittest.TestCase):
    """循环不变量外提优化器测试"""

    def setUp(self):
        """每个测试前创建优化器实例"""
        self.optimizer = LoopInvariantOptimizer()

    def test_move_literal_assignment_out(self):
        # 测试字面量赋值被外提
        # 构建一个 while 循环，循环体内有纯字面量赋值
        loop = WhileStatement(
            condition=Identifier(name="cond"),
            body=[
                Assignment(
                    target=Identifier(name="x"),
                    value=NumberLiteral(value=42)
                ),
                Assignment(
                    target=Identifier(name="y"),
                    value=StringLiteral(value="hello")
                ),
                Assignment(
                    target=Identifier(name="z"),
                    value=BooleanLiteral(value=True)
                ),
            ]
        )

        module = Module()
        module.statements = [loop]

        result = self.optimizer.optimize(module)

        # 验证：循环前面应该有3个不变量赋值语句
        self.assertEqual(len(result.statements), 4)  # 3个不变量 + 1个循环

        # 前三个应该是赋值语句
        self.assertIsInstance(result.statements[0], Assignment)
        self.assertEqual(result.statements[0].target.name, "x")
        self.assertIsInstance(result.statements[0].value, NumberLiteral)
        self.assertEqual(result.statements[0].value.value, 42)

        self.assertIsInstance(result.statements[1], Assignment)
        self.assertEqual(result.statements[1].target.name, "y")
        self.assertIsInstance(result.statements[1].value, StringLiteral)
        self.assertEqual(result.statements[1].value.value, "hello")

        self.assertIsInstance(result.statements[2], Assignment)
        self.assertEqual(result.statements[2].target.name, "z")
        self.assertIsInstance(result.statements[2].value, BooleanLiteral)
        self.assertEqual(result.statements[2].value.value, True)

        # 第四个是循环，且循环体应该为空（因为所有语句都被外提了）
        self.assertIsInstance(result.statements[3], WhileStatement)
        self.assertEqual(len(result.statements[3].body), 0)

    def test_no_move_variable_dep(self):
        # 测试依赖变量的赋值不外提
        # 构建一个 while 循环，循环体内有依赖其他变量的赋值
        loop = WhileStatement(
            condition=Identifier(name="cond"),
            body=[
                # 这个赋值依赖变量 a，不能外提
                Assignment(
                    target=Identifier(name="x"),
                    value=Identifier(name="a")
                ),
                # 这个是纯字面量，可以外提
                Assignment(
                    target=Identifier(name="y"),
                    value=NumberLiteral(value=100)
                ),
            ]
        )

        module = Module()
        module.statements = [loop]

        result = self.optimizer.optimize(module)

        # 验证：只有 y=100 被外提，x=a 保留在循环内
        self.assertEqual(len(result.statements), 2)  # 1个不变量 + 1个循环

        # 第一个是不变量 y=100
        self.assertIsInstance(result.statements[0], Assignment)
        self.assertEqual(result.statements[0].target.name, "y")
        self.assertIsInstance(result.statements[0].value, NumberLiteral)
        self.assertEqual(result.statements[0].value.value, 100)

        # 第二个是循环，循环体内应该还有 x=a
        self.assertIsInstance(result.statements[1], WhileStatement)
        self.assertEqual(len(result.statements[1].body), 1)
        self.assertIsInstance(result.statements[1].body[0], Assignment)
        self.assertEqual(result.statements[1].body[0].target.name, "x")
        self.assertIsInstance(result.statements[1].body[0].value, Identifier)

    def test_nested_loops(self):
        # 测试嵌套循环正确处理
        # 构建嵌套循环：外层 while 循环内有一个内层 foreach 循环
        inner_loop = ForeachStatement(
            variable="item",
            iterable=Identifier(name="list"),
            body=[
                # 内层循环的不变量（纯字面量，对于外层也是不变的）
                Assignment(
                    target=Identifier(name="inner_val"),
                    value=NumberLiteral(value=10)
                ),
            ]
        )

        outer_loop = WhileStatement(
            condition=Identifier(name="cond"),
            body=[
                # 外层循环的不变量
                Assignment(
                    target=Identifier(name="outer_val"),
                    value=StringLiteral(value="outer")
                ),
                inner_loop,
            ]
        )

        module = Module()
        module.statements = [outer_loop]

        result = self.optimizer.optimize(module)

        # 验证：两层循环的不变量都被外提到最外层
        # 因为纯字面量对于所有外层循环也是不变的
        # 结构应该是：[outer_val赋值, inner_val赋值, 外层循环(包含 内层循环)]
        self.assertEqual(len(result.statements), 3)

        # 第一个是外层不变量
        self.assertIsInstance(result.statements[0], Assignment)
        self.assertEqual(result.statements[0].target.name, "outer_val")
        self.assertIsInstance(result.statements[0].value, StringLiteral)
        self.assertEqual(result.statements[0].value.value, "outer")

        # 第二个是内层不变量（也被外提到最外层，因为纯字面量是全局不变的）
        self.assertIsInstance(result.statements[1], Assignment)
        self.assertEqual(result.statements[1].target.name, "inner_val")
        self.assertIsInstance(result.statements[1].value, NumberLiteral)
        self.assertEqual(result.statements[1].value.value, 10)

        # 第三个是外层循环
        self.assertIsInstance(result.statements[2], WhileStatement)
        outer_body = result.statements[2].body

        # 外层循环体内：只有内层循环
        self.assertEqual(len(outer_body), 1)

        # 内层循环，其body应该为空
        self.assertIsInstance(outer_body[0], ForeachStatement)
        self.assertEqual(len(outer_body[0].body), 0)

    def test_variable_declaration_invariant(self):
        # 测试变量声明初始化为纯字面量也能被外提
        loop = WhileStatement(
            condition=Identifier(name="cond"),
            body=[
                VariableDeclaration(
                    name="x",
                    value=NumberLiteral(value=123),
                    is_mutable=True
                ),
                VariableDeclaration(
                    name="msg",
                    value=StringLiteral(value="test"),
                    is_mutable=False
                ),
            ]
        )

        module = Module()
        module.statements = [loop]

        result = self.optimizer.optimize(module)

        # 验证：两个变量声明都被外提
        self.assertEqual(len(result.statements), 3)  # 2个声明 + 1个循环

        self.assertIsInstance(result.statements[0], VariableDeclaration)
        self.assertEqual(result.statements[0].name, "x")
        self.assertIsInstance(result.statements[0].value, NumberLiteral)
        self.assertEqual(result.statements[0].value.value, 123)

        self.assertIsInstance(result.statements[1], VariableDeclaration)
        self.assertEqual(result.statements[1].name, "msg")
        self.assertIsInstance(result.statements[1].value, StringLiteral)
        self.assertEqual(result.statements[1].value.value, "test")

        self.assertIsInstance(result.statements[2], WhileStatement)
        self.assertEqual(len(result.statements[2].body), 0)

    def test_foreach_loop_invariant(self):
        # 测试 foreach 循环的不变量外提
        loop = ForeachStatement(
            variable="item",
            iterable=Identifier(name="items"),
            body=[
                Assignment(
                    target=Identifier(name="factor"),
                    value=NumberLiteral(value=2.5)
                ),
                Assignment(
                    target=Identifier(name="result"),
                    value=Identifier(name="item")
                ),
            ]
        )

        module = Module()
        module.statements = [loop]

        result = self.optimizer.optimize(module)

        # 验证：factor=2.5 被外提，result=item 保留
        self.assertEqual(len(result.statements), 2)

        self.assertIsInstance(result.statements[0], Assignment)
        self.assertEqual(result.statements[0].target.name, "factor")
        self.assertIsInstance(result.statements[0].value, NumberLiteral)
        self.assertEqual(result.statements[0].value.value, 2.5)

        self.assertIsInstance(result.statements[1], ForeachStatement)
        self.assertEqual(len(result.statements[1].body), 1)
        self.assertEqual(result.statements[1].body[0].target.name, "result")


if __name__ == '__main__':
    unittest.main()
