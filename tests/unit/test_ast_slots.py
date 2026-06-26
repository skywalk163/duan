# -*- coding: utf-8 -*-
"""
AST 节点 __slots__ 优化测试

验证所有 AST 节点类都使用了 __slots__，没有 __dict__，以节省内存。
"""

import sys
import os
import unittest

# 添加项目路径
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
sys.path.insert(0, _src_dir)


class TestAstSlots(unittest.TestCase):
    """AST 节点 __slots__ 测试"""

    @classmethod
    def setUpClass(cls):
        """导入所有 AST 节点类"""
        import ast_nodes
        cls.ast_module = ast_nodes
        
        # 收集所有 ASTNode 的子类
        cls.ast_classes = []
        for name in dir(cls.ast_module):
            obj = getattr(cls.ast_module, name)
            if isinstance(obj, type) and issubclass(obj, cls.ast_module.ASTNode) and obj is not cls.ast_module.ASTNode:
                cls.ast_classes.append(obj)
        cls.ast_classes.append(cls.ast_module.ASTNode)  # 也包含基类

    def test_ast_node_base_has_slots(self):
        """测试 ASTNode 基类使用了 __slots__"""
        node = self.ast_module.ASTNode()
        self.assertFalse(hasattr(node, '__dict__'), 
            "ASTNode 实例不应有 __dict__")
        self.assertTrue(hasattr(self.ast_module.ASTNode, '__slots__'),
            "ASTNode 类应定义 __slots__")

    def test_core_literals_no_dict(self):
        """测试核心字面量节点没有 __dict__"""
        # 数字字面量
        num = self.ast_module.NumberLiteral(value=42)
        self.assertFalse(hasattr(num, '__dict__'),
            "NumberLiteral 实例不应有 __dict__")
        
        # 字符串字面量
        s = self.ast_module.StringLiteral(value="hello")
        self.assertFalse(hasattr(s, '__dict__'),
            "StringLiteral 实例不应有 __dict__")
        
        # 布尔字面量
        b = self.ast_module.BooleanLiteral(value=True)
        self.assertFalse(hasattr(b, '__dict__'),
            "BooleanLiteral 实例不应有 __dict__")
        
        # 空值字面量
        n = self.ast_module.NullLiteral()
        self.assertFalse(hasattr(n, '__dict__'),
            "NullLiteral 实例不应有 __dict__")

    def test_core_expressions_no_dict(self):
        """测试核心表达式节点没有 __dict__"""
        # 标识符
        ident = self.ast_module.Identifier(name="x")
        self.assertFalse(hasattr(ident, '__dict__'),
            "Identifier 实例不应有 __dict__")
        
        # 二元运算
        binop = self.ast_module.BinaryOp(
            left=self.ast_module.NumberLiteral(value=1),
            operator="+",
            right=self.ast_module.NumberLiteral(value=2)
        )
        self.assertFalse(hasattr(binop, '__dict__'),
            "BinaryOp 实例不应有 __dict__")
        
        # 一元运算
        unary = self.ast_module.UnaryOp(
            operator="-",
            operand=self.ast_module.NumberLiteral(value=5)
        )
        self.assertFalse(hasattr(unary, '__dict__'),
            "UnaryOp 实例不应有 __dict__")

    def test_core_statements_no_dict(self):
        """测试核心语句节点没有 __dict__"""
        # 变量声明
        vardecl = self.ast_module.VariableDeclaration(
            name="x",
            value=self.ast_module.NumberLiteral(value=10)
        )
        self.assertFalse(hasattr(vardecl, '__dict__'),
            "VariableDeclaration 实例不应有 __dict__")
        
        # 赋值语句
        assign = self.ast_module.Assignment(
            target=self.ast_module.Identifier(name="x"),
            value=self.ast_module.NumberLiteral(value=20)
        )
        self.assertFalse(hasattr(assign, '__dict__'),
            "Assignment 实例不应有 __dict__")
        
        # 条件语句
        ifstmt = self.ast_module.IfStatement(
            condition=self.ast_module.Identifier(name="x"),
            then_body=[]
        )
        self.assertFalse(hasattr(ifstmt, '__dict__'),
            "IfStatement 实例不应有 __dict__")

    def test_module_node_no_dict(self):
        """测试 Module 顶层节点没有 __dict__"""
        module = self.ast_module.Module()
        self.assertFalse(hasattr(module, '__dict__'),
            "Module 实例不应有 __dict__")

    def test_all_ast_classes_have_slots(self):
        """测试所有 AST 节点类都使用了 __slots__"""
        no_slots_classes = []
        for cls in self.ast_classes:
            try:
                instance = cls()
                if hasattr(instance, '__dict__'):
                    no_slots_classes.append(cls.__name__)
            except Exception:
                # 如果构造需要参数，尝试其他方式检查
                if not hasattr(cls, '__slots__'):
                    no_slots_classes.append(cls.__name__)
        
        self.assertEqual(len(no_slots_classes), 0,
            f"以下类没有使用 __slots__: {no_slots_classes}")

    def test_field_access_works(self):
        """测试字段访问仍然正常工作"""
        node = self.ast_module.NumberLiteral(value=42, line=10, column=20)
        self.assertEqual(node.value, 42)
        self.assertEqual(node.line, 10)
        self.assertEqual(node.column, 20)
        
        # 测试修改字段
        node.value = 100
        self.assertEqual(node.value, 100)

    def test_dataclass_features_work(self):
        """测试 dataclass 特性仍然正常"""
        # 测试 __dataclass_fields__ 仍然可用
        self.assertTrue(hasattr(self.ast_module.NumberLiteral, '__dataclass_fields__'))
        
        # 测试 asdict 类似功能
        from ast_nodes import ast_to_dict
        node = self.ast_module.NumberLiteral(value=42, line=1, column=2)
        result = ast_to_dict(node)
        self.assertEqual(result['type'], 'NumberLiteral')
        self.assertEqual(result['value'], 42)
        self.assertEqual(result['line'], 1)
        self.assertEqual(result['column'], 2)


if __name__ == '__main__':
    unittest.main()
