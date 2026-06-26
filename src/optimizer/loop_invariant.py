from .base import Optimizer
from ast_nodes import (
    ASTNode, Module,
    NumberLiteral, StringLiteral, BooleanLiteral,
    VariableDeclaration, Assignment, Identifier,
    WhileStatement, ForeachStatement,
    IfStatement, ExpressionStatement, PrintStatement, ReturnStatement,
    SegmentDefinition, ClassDefinition,
)


class LoopInvariantOptimizer(Optimizer):
    """循环不变量外提优化器（保守策略）

    只外提确定安全的语句：
    - 变量赋值为纯字面量（数字、字符串、布尔）
    - 变量声明初始化为纯字面量

    保守策略：不确定就不外提。
    """

    def optimize(self, module: Module) -> Module:
        """优化整个模块"""
        module.statements = self._optimize_stmt_list(module.statements)
        module.segments = [self._optimize_segment(seg) for seg in module.segments]
        module.classes = [self._optimize_class(cls) for cls in module.classes]
        return module

    def _is_pure_literal(self, expr: ASTNode) -> bool:
        """判断表达式是否为纯字面量（数字、字符串、布尔）"""
        return isinstance(expr, (NumberLiteral, StringLiteral, BooleanLiteral))

    def _is_loop_invariant_stmt(self, stmt: ASTNode, loop_vars: set) -> bool:
        """判断语句是否为循环不变量（可安全外提）

        保守策略：只外提纯字面量的赋值和声明。
        """
        if isinstance(stmt, VariableDeclaration):
            if stmt.value and self._is_pure_literal(stmt.value):
                return True
            return False

        if isinstance(stmt, Assignment):
            if isinstance(stmt.target, Identifier):
                if self._is_pure_literal(stmt.value):
                    return True
            return False

        return False

    def _extract_loop_invariants(self, body: list, loop_vars: set) -> tuple:
        """从循环体中提取不变量语句

        返回 (不变量列表, 剩余语句列表)
        """
        invariants = []
        remaining = []

        for stmt in body:
            if self._is_loop_invariant_stmt(stmt, loop_vars):
                invariants.append(stmt)
            else:
                remaining.append(stmt)

        return invariants, remaining

    def _optimize_stmt_list(self, stmts: list) -> list:
        """优化语句列表，处理其中的循环"""
        result = []
        for stmt in stmts:
            optimized = self._optimize_stmt(stmt)
            if isinstance(optimized, list):
                result.extend(optimized)
            else:
                result.append(optimized)
        return result

    def _optimize_stmt(self, stmt: ASTNode):
        """优化单个语句，返回优化后的语句或语句列表"""
        if isinstance(stmt, WhileStatement):
            return self._optimize_while_loop(stmt)
        elif isinstance(stmt, ForeachStatement):
            return self._optimize_foreach_loop(stmt)
        elif isinstance(stmt, IfStatement):
            return self._optimize_if_stmt(stmt)
        elif isinstance(stmt, VariableDeclaration):
            return stmt
        elif isinstance(stmt, Assignment):
            return stmt
        else:
            return stmt

    def _optimize_while_loop(self, loop: WhileStatement):
        """优化 while 循环，外提不变量"""
        loop.body = self._optimize_stmt_list(loop.body)

        loop_vars = self._collect_loop_vars(loop)
        invariants, remaining = self._extract_loop_invariants(loop.body, loop_vars)

        if not invariants:
            return loop

        loop.body = remaining
        return invariants + [loop]

    def _optimize_foreach_loop(self, loop: ForeachStatement):
        """优化 foreach 循环，外提不变量"""
        loop.body = self._optimize_stmt_list(loop.body)

        loop_vars = self._collect_loop_vars(loop)
        invariants, remaining = self._extract_loop_invariants(loop.body, loop_vars)

        if not invariants:
            return loop

        loop.body = remaining
        return invariants + [loop]

    def _optimize_if_stmt(self, stmt: IfStatement) -> IfStatement:
        """优化 if 语句中的循环"""
        stmt.then_body = self._optimize_stmt_list(stmt.then_body)
        if stmt.else_body:
            stmt.else_body = self._optimize_stmt_list(stmt.else_body)
        return stmt

    def _collect_loop_vars(self, loop) -> set:
        """收集循环中定义的变量集合

        保守策略：只收集最明显的循环变量。
        """
        loop_vars = set()

        if isinstance(loop, ForeachStatement):
            loop_vars.add(loop.variable)

        return loop_vars

    def _optimize_segment(self, seg: SegmentDefinition) -> SegmentDefinition:
        """优化段落定义"""
        seg.body = self._optimize_stmt_list(seg.body)
        return seg

    def _optimize_class(self, cls: ClassDefinition) -> ClassDefinition:
        """优化类定义"""
        return cls
