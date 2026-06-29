from .base import Optimizer
from ast_nodes import (
    ASTNode, Module, BinaryOp, UnaryOp,
    NumberLiteral, BooleanLiteral, StringLiteral, NullLiteral,
    VariableDeclaration, Assignment, IfStatement,
    ExpressionStatement, PrintStatement, ReturnStatement,
    WhileStatement, FunctionCall, Identifier, PropertyAccess,
)


class PeepholeOptimizer(Optimizer):
    """窥孔优化器

    在小范围代码窗口（peephole）内做局部优化：
    - 代数恒等式：x + 0 → x, x * 1 → x, x * 0 → 0, x - x → 0, x / 1 → x
    - 布尔简化：!True → False, True && x → x
    - 数值比较：x == x → True, x != x → False
    - 条件反转：if True -> 替换为 if 分支；if False -> 替换为 else 分支
    """

    def optimize(self, module: Module) -> Module:
        """优化整个模块"""
        module.statements = [self._optimize_stmt(s) for s in module.statements]
        module.segments = [self._optimize_segment(seg) for seg in module.segments]
        return module

    def optimize_expr(self, expr: ASTNode) -> ASTNode:
        """优化单个表达式"""
        return self._optimize_expr(expr)

    def _optimize_expr(self, expr: ASTNode) -> ASTNode:
        """优化表达式"""
        if expr is None:
            return expr

        # 后序遍历
        if isinstance(expr, BinaryOp):
            expr.left = self._optimize_expr(expr.left)
            expr.right = self._optimize_expr(expr.right)
            return self._simplify_binary(expr)

        if isinstance(expr, UnaryOp):
            expr.operand = self._optimize_expr(expr.operand)
            return self._simplify_unary(expr)

        if isinstance(expr, FunctionCall):
            expr.arguments = [self._optimize_expr(a) for a in expr.arguments]
            return expr

        return expr

    def _simplify_binary(self, node: BinaryOp) -> ASTNode:
        """简化二元运算"""
        op = node.operator
        left = node.left
        right = node.right

        # 加法：x + 0 = x, 0 + x = x
        if op == '+':
            if self._is_zero(right):
                return left
            if self._is_zero(left):
                return right

        # 减法：x - 0 = x
        if op == '-':
            if self._is_zero(right):
                return left

        # 乘法：x * 1 = x, 1 * x = x, x * 0 = 0
        if op == '*':
            if self._is_one(right):
                return left
            if self._is_one(left):
                return right
            if self._is_zero(left) or self._is_zero(right):
                return self._make_number(0, node.line, node.column)

        # 除法：x / 1 = x
        if op == '/':
            if self._is_one(right):
                return left

        # 减法自销：x - x = 0 (需要结构等价)
        if op == '-' and self._is_same_expr(left, right):
            return self._make_number(0, node.line, node.column)

        # 加法自销：x + (-x) = 0 (简化为 x - x = 0 通过结构等价)
        if op == '+' and isinstance(right, UnaryOp) and right.operator == '-':
            if self._is_same_expr(left, right.operand):
                return self._make_number(0, node.line, node.column)

        # 比较：x == x = True
        if op == '==':
            if self._is_same_expr(left, right):
                return BooleanLiteral(value=True, line=node.line, column=node.column)
        if op == '!=':
            if self._is_same_expr(left, right):
                return BooleanLiteral(value=False, line=node.line, column=node.column)

        return node

    def _simplify_unary(self, node: UnaryOp) -> ASTNode:
        """简化一元运算"""
        if node.operator == 'not':
            if isinstance(node.operand, BooleanLiteral):
                return BooleanLiteral(value=not node.operand.value,
                                      line=node.line, column=node.column)
        if node.operator == '-':
            if isinstance(node.operand, NumberLiteral):
                return NumberLiteral(value=-node.operand.value,
                                     line=node.line, column=node.column)
        return node

    def _is_zero(self, node: ASTNode) -> bool:
        """判断是否为 0"""
        return isinstance(node, NumberLiteral) and node.value == 0

    def _is_one(self, node: ASTNode) -> bool:
        """判断是否为 1"""
        return isinstance(node, NumberLiteral) and node.value == 1

    def _is_same_expr(self, a: ASTNode, b: ASTNode) -> bool:
        """判断两个表达式是否结构等价（简单比较）"""
        if type(a) != type(b):
            return False
        if isinstance(a, NumberLiteral):
            return a.value == b.value
        if isinstance(a, StringLiteral):
            return a.value == b.value
        if isinstance(a, BooleanLiteral):
            return a.value == b.value
        if isinstance(a, Identifier):
            return a.name == b.name
        return False

    def _make_number(self, value, line=0, col=0) -> NumberLiteral:
        """创建数字字面量"""
        return NumberLiteral(value=value, line=line, column=col)

    def _optimize_stmt(self, stmt: ASTNode) -> ASTNode:
        """优化语句"""
        if stmt is None:
            return stmt
        if isinstance(stmt, VariableDeclaration):
            if stmt.value:
                stmt.value = self._optimize_expr(stmt.value)
        elif isinstance(stmt, Assignment):
            stmt.value = self._optimize_expr(stmt.value)
        elif isinstance(stmt, ExpressionStatement):
            stmt.expression = self._optimize_expr(stmt.expression)
        elif isinstance(stmt, PrintStatement):
            if hasattr(stmt, 'value') and stmt.value:
                stmt.value = self._optimize_expr(stmt.value)
            if hasattr(stmt, 'arguments') and stmt.arguments:
                stmt.arguments = [self._optimize_expr(a) for a in stmt.arguments]
        elif isinstance(stmt, ReturnStatement):
            if stmt.value:
                stmt.value = self._optimize_expr(stmt.value)
        elif isinstance(stmt, IfStatement):
            stmt.condition = self._optimize_expr(stmt.condition)
            stmt.then_body = [self._optimize_stmt(s) for s in stmt.then_body]
            if stmt.else_body:
                stmt.else_body = [self._optimize_stmt(s) for s in stmt.else_body]
        elif isinstance(stmt, WhileStatement):
            stmt.condition = self._optimize_expr(stmt.condition)
            stmt.body = [self._optimize_stmt(s) for s in stmt.body]
        return stmt

    def _optimize_segment(self, seg) -> ASTNode:
        """优化段落"""
        if hasattr(seg, 'body'):
            seg.body = [self._optimize_stmt(s) for s in seg.body]
        return seg
