from .base import Optimizer
from ast_nodes import (
    ASTNode, Module,
    NumberLiteral, BooleanLiteral, NullLiteral, StringLiteral,
    IfStatement, WhileStatement, ForeachStatement,
    ReturnStatement, ThrowStatement, BreakStatement, ContinueStatement,
    VariableDeclaration, Assignment, ExpressionStatement, PrintStatement,
    SegmentDefinition, ClassDefinition, MethodDefinition,
    TryStatement, WithStatement, MatchStatement,
)


TERMINAL_STATEMENTS = (
    ReturnStatement,
    ThrowStatement,
    BreakStatement,
    ContinueStatement,
)


class DeadCodeEliminationOptimizer(Optimizer):
    """死代码消除优化器

    消除不可达的死代码，包括：
    - if 条件恒假：删除整个 if（无 else 时）或只保留 else 分支
    - if 条件恒真：只保留 then 分支
    - while 条件恒假：删除整个循环
    - return/throw/break/continue 后的语句删除
    - 递归处理嵌套块
    """

    def optimize(self, module: Module) -> Module:
        """优化整个模块"""
        module.statements = self._optimize_block(module.statements)
        module.segments = [self._optimize_segment(seg) for seg in module.segments]
        module.classes = [self._optimize_class(cls) for cls in module.classes]
        return module

    def _is_constant_false(self, expr: ASTNode) -> bool:
        """判断表达式是否为常量假值"""
        if isinstance(expr, BooleanLiteral):
            return not expr.value
        if isinstance(expr, NumberLiteral):
            return expr.value == 0
        if isinstance(expr, NullLiteral):
            return True
        if isinstance(expr, StringLiteral):
            return expr.value == ""
        return False

    def _is_constant_true(self, expr: ASTNode) -> bool:
        """判断表达式是否为常量真值"""
        if isinstance(expr, BooleanLiteral):
            return expr.value
        if isinstance(expr, NumberLiteral):
            return expr.value != 0
        if isinstance(expr, StringLiteral):
            return expr.value != ""
        return False

    def _optimize_block(self, stmts: list) -> list:
        """优化语句块，消除终止语句后的死代码"""
        result = []
        for stmt in stmts:
            optimized = self._optimize_stmt(stmt)
            if isinstance(optimized, list):
                has_terminal = False
                for s in optimized:
                    result.append(s)
                    if isinstance(s, TERMINAL_STATEMENTS):
                        has_terminal = True
                        break
                if has_terminal:
                    break
            else:
                result.append(optimized)
                if isinstance(optimized, TERMINAL_STATEMENTS):
                    break
        return result

    def _optimize_stmt(self, stmt: ASTNode):
        """优化单个语句，可能返回语句列表（用于 if 展开）"""
        if isinstance(stmt, IfStatement):
            return self._optimize_if(stmt)
        if isinstance(stmt, WhileStatement):
            return self._optimize_while(stmt)
        if isinstance(stmt, ForeachStatement):
            stmt.body = self._optimize_block(stmt.body)
            return stmt
        if isinstance(stmt, TryStatement):
            stmt.try_body = self._optimize_block(stmt.try_body)
            stmt.catch_body = self._optimize_block(stmt.catch_body)
            if stmt.finally_body:
                stmt.finally_body = self._optimize_block(stmt.finally_body)
            return stmt
        if isinstance(stmt, WithStatement):
            stmt.body = self._optimize_block(stmt.body)
            return stmt
        if isinstance(stmt, MatchStatement):
            for case in stmt.cases:
                case.body = self._optimize_block(case.body)
            return stmt
        if isinstance(stmt, VariableDeclaration):
            return stmt
        if isinstance(stmt, Assignment):
            return stmt
        if isinstance(stmt, ExpressionStatement):
            return stmt
        if isinstance(stmt, PrintStatement):
            return stmt
        if isinstance(stmt, ReturnStatement):
            return stmt
        if isinstance(stmt, ThrowStatement):
            return stmt
        if isinstance(stmt, BreakStatement):
            return stmt
        if isinstance(stmt, ContinueStatement):
            return stmt
        return stmt

    def _optimize_if(self, stmt: IfStatement):
        """优化 if 语句"""
        stmt.then_body = self._optimize_block(stmt.then_body)
        if stmt.else_body:
            stmt.else_body = self._optimize_block(stmt.else_body)

        if self._is_constant_true(stmt.condition):
            return stmt.then_body
        if self._is_constant_false(stmt.condition):
            if stmt.else_body is not None:
                return stmt.else_body
            return []

        return stmt

    def _optimize_while(self, stmt: WhileStatement):
        """优化 while 语句"""
        stmt.body = self._optimize_block(stmt.body)

        if self._is_constant_false(stmt.condition):
            return []

        return stmt

    def _optimize_segment(self, seg: SegmentDefinition) -> SegmentDefinition:
        """优化段落定义"""
        seg.body = self._optimize_block(seg.body)
        return seg

    def _optimize_class(self, cls: ClassDefinition) -> ClassDefinition:
        """优化类定义"""
        for method in cls.methods:
            method.body = self._optimize_block(method.body)
        if cls.constructor:
            cls.constructor.body = self._optimize_block(cls.constructor.body)
        return cls
