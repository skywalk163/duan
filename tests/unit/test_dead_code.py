# -*- coding: utf-8 -*-
"""
死代码消除优化器单元测试

测试 DeadCodeEliminationOptimizer 的各项功能。
"""

import sys
import os
import unittest

# 添加项目路径
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
sys.path.insert(0, _src_dir)

from ast_nodes import (
    Module, NumberLiteral, BooleanLiteral, StringLiteral,
    IfStatement, WhileStatement,
    ReturnStatement, BreakStatement, ContinueStatement, ThrowStatement,
    VariableDeclaration, PrintStatement, ExpressionStatement, Identifier,
    SegmentDefinition,
)
from optimizer.dead_code import DeadCodeEliminationOptimizer


class TestDeadCodeElimination(unittest.TestCase):
    """死代码消除优化器测试"""

    def setUp(self):
        """每个测试前创建优化器实例"""
        self.optimizer = DeadCodeEliminationOptimizer()

    def test_eliminate_if_false(self):
        # 测试 if 假条件删除整个 if 语句
        # 构建：if (0) { x = 1; }
        module = Module()
        module.statements = [
            IfStatement(
                condition=NumberLiteral(value=0),
                then_body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                ],
                else_body=None,
            )
        ]

        result = self.optimizer.optimize(module)

        # if 0 应该被完全删除，语句块为空
        self.assertEqual(len(result.statements), 0)

    def test_eliminate_if_false_with_else(self):
        # 测试 if 假条件且有 else 时，只保留 else 分支
        # 构建：if (0) { x = 1; } else { x = 2; }
        module = Module()
        module.statements = [
            IfStatement(
                condition=NumberLiteral(value=0),
                then_body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                ],
                else_body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=2)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # 应该只保留 else 分支的语句
        self.assertEqual(len(result.statements), 1)
        self.assertIsInstance(result.statements[0], VariableDeclaration)
        self.assertEqual(result.statements[0].name, "x")
        self.assertEqual(result.statements[0].value.value, 2)

    def test_keep_if_true(self):
        # 测试 if 真条件只保留 then 分支
        # 构建：if (1) { x = 1; } else { x = 2; }
        module = Module()
        module.statements = [
            IfStatement(
                condition=NumberLiteral(value=1),
                then_body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                ],
                else_body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=2)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # 应该只保留 then 分支的语句
        self.assertEqual(len(result.statements), 1)
        self.assertIsInstance(result.statements[0], VariableDeclaration)
        self.assertEqual(result.statements[0].name, "x")
        self.assertEqual(result.statements[0].value.value, 1)

    def test_keep_if_true_no_else(self):
        # 测试 if 真条件无 else 时，保留 then 分支内容
        # 构建：if (true) { print(1); }
        module = Module()
        module.statements = [
            IfStatement(
                condition=BooleanLiteral(value=True),
                then_body=[
                    PrintStatement(value=NumberLiteral(value=1)),
                ],
                else_body=None,
            )
        ]

        result = self.optimizer.optimize(module)

        # 应该展开为 then 体中的语句
        self.assertEqual(len(result.statements), 1)
        self.assertIsInstance(result.statements[0], PrintStatement)

    def test_eliminate_after_return(self):
        # 测试 return 后的语句被删除
        # 构建：{ return 1; x = 2; print(3); }
        module = Module()
        module.segments = [
            SegmentDefinition(
                name="test",
                body=[
                    ReturnStatement(value=NumberLiteral(value=1)),
                    VariableDeclaration(name="x", value=NumberLiteral(value=2)),
                    PrintStatement(value=NumberLiteral(value=3)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # return 之后的语句应该被删除
        seg = result.segments[0]
        self.assertEqual(len(seg.body), 1)
        self.assertIsInstance(seg.body[0], ReturnStatement)

    def test_eliminate_after_throw(self):
        # 测试 throw 后的语句被删除
        module = Module()
        module.segments = [
            SegmentDefinition(
                name="test",
                body=[
                    ThrowStatement(value=StringLiteral(value="error")),
                    PrintStatement(value=NumberLiteral(value=1)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        seg = result.segments[0]
        self.assertEqual(len(seg.body), 1)
        self.assertIsInstance(seg.body[0], ThrowStatement)

    def test_eliminate_after_break(self):
        # 测试 break 后的语句被删除
        module = Module()
        module.statements = [
            WhileStatement(
                condition=Identifier(name="cond"),
                body=[
                    BreakStatement(),
                    PrintStatement(value=NumberLiteral(value=1)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        while_stmt = result.statements[0]
        self.assertEqual(len(while_stmt.body), 1)
        self.assertIsInstance(while_stmt.body[0], BreakStatement)

    def test_eliminate_after_continue(self):
        # 测试 continue 后的语句被删除
        module = Module()
        module.statements = [
            WhileStatement(
                condition=Identifier(name="cond"),
                body=[
                    ContinueStatement(),
                    PrintStatement(value=NumberLiteral(value=1)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        while_stmt = result.statements[0]
        self.assertEqual(len(while_stmt.body), 1)
        self.assertIsInstance(while_stmt.body[0], ContinueStatement)

    def test_eliminate_while_false(self):
        # 测试 while 假条件删除整个循环
        # 构建：while (0) { x = 1; }
        module = Module()
        module.statements = [
            WhileStatement(
                condition=NumberLiteral(value=0),
                body=[
                    VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # while 0 应该被完全删除
        self.assertEqual(len(result.statements), 0)

    def test_keep_while_true(self):
        # 测试 while 真条件保留循环体
        module = Module()
        module.statements = [
            WhileStatement(
                condition=BooleanLiteral(value=True),
                body=[
                    PrintStatement(value=NumberLiteral(value=1)),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # while true 应该保留
        self.assertEqual(len(result.statements), 1)
        self.assertIsInstance(result.statements[0], WhileStatement)
        self.assertEqual(len(result.statements[0].body), 1)

    def test_nested_blocks(self):
        # 测试嵌套块正确处理
        # 构建：
        # if (1) {
        #   if (0) {
        #     x = 1;
        #   } else {
        #     return 2;
        #     y = 3;  // 死代码
        #   }
        #   z = 4;  // 死代码（在 return 后）
        # }
        module = Module()
        module.statements = [
            IfStatement(
                condition=NumberLiteral(value=1),
                then_body=[
                    IfStatement(
                        condition=NumberLiteral(value=0),
                        then_body=[
                            VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                        ],
                        else_body=[
                            ReturnStatement(value=NumberLiteral(value=2)),
                            VariableDeclaration(name="y", value=NumberLiteral(value=3)),
                        ],
                    ),
                    VariableDeclaration(name="z", value=NumberLiteral(value=4)),
                ],
                else_body=None,
            )
        ]

        result = self.optimizer.optimize(module)

        # 外层 if true 展开，内层 if false 走 else，return 后删除死代码
        # 最终只有 return 2
        self.assertEqual(len(result.statements), 1)
        self.assertIsInstance(result.statements[0], ReturnStatement)
        self.assertEqual(result.statements[0].value.value, 2)

    def test_nested_while_in_if(self):
        # 测试嵌套 while 在 if 中
        # if (0) { while(1) { break; x=1; } } else { while(0) { y=2; } }
        module = Module()
        module.statements = [
            IfStatement(
                condition=NumberLiteral(value=0),
                then_body=[
                    WhileStatement(
                        condition=NumberLiteral(value=1),
                        body=[
                            BreakStatement(),
                            VariableDeclaration(name="x", value=NumberLiteral(value=1)),
                        ],
                    ),
                ],
                else_body=[
                    WhileStatement(
                        condition=NumberLiteral(value=0),
                        body=[
                            VariableDeclaration(name="y", value=NumberLiteral(value=2)),
                        ],
                    ),
                ],
            )
        ]

        result = self.optimizer.optimize(module)

        # if false 走 else，else 中的 while false 被删除，所以语句块为空
        self.assertEqual(len(result.statements), 0)

    def test_no_dead_code(self):
        # 测试没有死代码的情况保持不变
        module = Module()
        module.statements = [
            VariableDeclaration(name="x", value=NumberLiteral(value=1)),
            PrintStatement(value=Identifier(name="x")),
        ]

        result = self.optimizer.optimize(module)

        self.assertEqual(len(result.statements), 2)
        self.assertIsInstance(result.statements[0], VariableDeclaration)
        self.assertIsInstance(result.statements[1], PrintStatement)


if __name__ == '__main__':
    unittest.main()
