# -*- coding: utf-8 -*-
"""
常量折叠优化器单元测试

测试 ConstantFoldingOptimizer 的各项功能。
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
    BinaryOp, Identifier, Module,
)
from optimizer.constant_fold import ConstantFoldingOptimizer


class TestConstantFolding(unittest.TestCase):
    """常量折叠优化器测试"""

    def setUp(self):
        """每个测试前创建优化器实例"""
        self.optimizer = ConstantFoldingOptimizer()

    def test_fold_arithmetic(self):
        # 测试算术运算常量折叠：1 + 2 * 3 应该折叠为 7
        # 构建表达式：1 + (2 * 3)
        expr = BinaryOp(
            left=NumberLiteral(value=1),
            operator='+',
            right=BinaryOp(
                left=NumberLiteral(value=2),
                operator='*',
                right=NumberLiteral(value=3)
            )
        )

        result = self.optimizer.optimize_expr(expr)

        # 验证结果是 NumberLiteral 且值为 7
        self.assertIsInstance(result, NumberLiteral)
        self.assertEqual(result.value, 7)

    def test_fold_string(self):
        # 测试字符串拼接折叠："a" + "b" 应该折叠为 "ab"
        expr = BinaryOp(
            left=StringLiteral(value="a"),
            operator='+',
            right=StringLiteral(value="b")
        )

        result = self.optimizer.optimize_expr(expr)

        # 验证结果是 StringLiteral 且值为 "ab"
        self.assertIsInstance(result, StringLiteral)
        self.assertEqual(result.value, "ab")

    def test_no_fold_variables(self):
        # 测试变量表达式不折叠：包含变量的表达式应保持原样
        expr = BinaryOp(
            left=Identifier(name="x"),
            operator='+',
            right=NumberLiteral(value=1)
        )

        result = self.optimizer.optimize_expr(expr)

        # 验证结果仍然是 BinaryOp，没有被折叠
        self.assertIsInstance(result, BinaryOp)
        self.assertIsInstance(result.left, Identifier)
        self.assertEqual(result.left.name, "x")

    def test_fold_nested(self):
        # 测试嵌套表达式正确折叠：(1 + 2) * (3 + 4) 应该折叠为 21
        expr = BinaryOp(
            left=BinaryOp(
                left=NumberLiteral(value=1),
                operator='+',
                right=NumberLiteral(value=2)
            ),
            operator='*',
            right=BinaryOp(
                left=NumberLiteral(value=3),
                operator='+',
                right=NumberLiteral(value=4)
            )
        )

        result = self.optimizer.optimize_expr(expr)

        # 验证结果是 NumberLiteral 且值为 21
        self.assertIsInstance(result, NumberLiteral)
        self.assertEqual(result.value, 21)

    def test_zero_division(self):
        # 测试除零保留到运行时：除零不应崩溃，应保持原样
        expr = BinaryOp(
            left=NumberLiteral(value=5),
            operator='/',
            right=NumberLiteral(value=0)
        )

        # 不应抛出异常
        result = self.optimizer.optimize_expr(expr)

        # 验证结果仍然是 BinaryOp（没有被折叠）
        self.assertIsInstance(result, BinaryOp)
        self.assertEqual(result.operator, '/')

    def test_fold_comparison(self):
        # 测试比较运算折叠
        # 大于
        expr = BinaryOp(
            left=NumberLiteral(value=5),
            operator='>',
            right=NumberLiteral(value=3)
        )
        result = self.optimizer.optimize_expr(expr)
        self.assertIsInstance(result, BooleanLiteral)
        self.assertEqual(result.value, True)

        # 小于等于
        expr2 = BinaryOp(
            left=NumberLiteral(value=2),
            operator='<=',
            right=NumberLiteral(value=2)
        )
        result2 = self.optimizer.optimize_expr(expr2)
        self.assertIsInstance(result2, BooleanLiteral)
        self.assertEqual(result2.value, True)

    def test_fold_boolean(self):
        # 测试布尔运算折叠
        # 且运算
        expr = BinaryOp(
            left=BooleanLiteral(value=True),
            operator='and',
            right=BooleanLiteral(value=False)
        )
        result = self.optimizer.optimize_expr(expr)
        self.assertIsInstance(result, BooleanLiteral)
        self.assertEqual(result.value, False)

        # 或运算
        expr2 = BinaryOp(
            left=BooleanLiteral(value=False),
            operator='or',
            right=BooleanLiteral(value=True)
        )
        result2 = self.optimizer.optimize_expr(expr2)
        self.assertIsInstance(result2, BooleanLiteral)
        self.assertEqual(result2.value, True)

    def test_fold_module(self):
        # 测试优化整个模块
        module = Module()
        module.statements = []

        # 在模块中添加一个含常量表达式的语句
        from ast_nodes import ExpressionStatement
        module.statements.append(ExpressionStatement(
            expression=BinaryOp(
                left=NumberLiteral(value=10),
                operator='+',
                right=NumberLiteral(value=20)
            )
        ))

        result = self.optimizer.optimize(module)

        # 验证模块中的表达式已被折叠
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt.expression, NumberLiteral)
        self.assertEqual(stmt.expression.value, 30)


if __name__ == '__main__':
    unittest.main()
