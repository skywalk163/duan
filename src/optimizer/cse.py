from .base import Optimizer
from ast_nodes import (
    ASTNode, Module, BinaryOp, UnaryOp,
    NumberLiteral, BooleanLiteral, StringLiteral, NullLiteral,
    VariableDeclaration, Assignment, IfStatement,
    ExpressionStatement, PrintStatement, ReturnStatement,
    WhileStatement, FunctionCall, Identifier, PropertyAccess,
)


class CommonSubexpressionEliminationOptimizer(Optimizer):
    """公共子表达式消除优化器 (CSE)

    在基本块（无分支的语句序列）内，如果同一个表达式被计算多次，
    将第一次计算的结果存到临时变量，后续使用直接引用临时变量。

    示例：
        a = x + y
        b = x + y
        print(a + b)
    优化为：
        tmp1 = x + y
        a = tmp1
        b = tmp1
        print(a + b)
    """

    def __init__(self):
        super().__init__()
        # 缓存：表达式字符串 -> 临时变量名
        self.expr_cache = {}
        # 临时变量计数器
        self.temp_counter = 0
        # 基本块内的语句累积
        self.block_stmts = []
        # 当前块中已定义的变量
        self.killed_vars = set()

    def optimize(self, module: Module) -> Module:
        """优化整个模块"""
        self.expr_cache = {}
        self.temp_counter = 0
        self.killed_vars = set()
        module.statements = self._process_block(module.statements)
        # 处理段落（函数）
        new_segments = []
        for seg in module.segments:
            new_segments.append(self._optimize_segment(seg))
        module.segments = new_segments
        return module

    def _optimize_segment(self, seg) -> ASTNode:
        """优化段落：函数体作为独立作用域"""
        # 段落内表达式缓存独立
        old_cache = self.expr_cache
        old_counter = self.temp_counter
        old_killed = self.killed_vars
        self.expr_cache = {}
        self.temp_counter = 0
        self.killed_vars = set()
        if hasattr(seg, 'body'):
            seg.body = self._process_block(seg.body)
        self.expr_cache = old_cache
        self.temp_counter = old_counter
        self.killed_vars = old_killed
        return seg

    def _process_block(self, stmts: list) -> list:
        """处理基本块内的语句序列"""
        result = []
        for stmt in stmts:
            processed = self._process_stmt(stmt, result)
            if processed:
                if isinstance(processed, list):
                    result.extend(processed)
                else:
                    result.append(processed)
        return result

    def _process_stmt(self, stmt: ASTNode, current_block: list) -> object:
        """处理单条语句"""
        if stmt is None:
            return None

        # 控制流语句会结束基本块
        if isinstance(stmt, IfStatement):
            return self._process_if(stmt, current_block)
        if isinstance(stmt, WhileStatement):
            return self._process_while(stmt, current_block)
        if isinstance(stmt, ReturnStatement):
            # return 前优化表达式
            if stmt.value:
                stmt.value = self._try_cse_expr(stmt.value, current_block)
            self._invalidate_cache()
            return stmt

        # 变量声明 / 赋值
        if isinstance(stmt, VariableDeclaration):
            if stmt.value:
                stmt.value = self._try_cse_expr(stmt.value, current_block)
            # 失效与该变量相关的缓存
            if hasattr(stmt, 'name'):
                self._invalidate_for_var(stmt.name)
            return stmt

        if isinstance(stmt, Assignment):
            stmt.value = self._try_cse_expr(stmt.value, current_block)
            if hasattr(stmt, 'target') and hasattr(stmt.target, 'name'):
                self._invalidate_for_var(stmt.target.name)
            return stmt

        # 表达式语句
        if isinstance(stmt, ExpressionStatement):
            stmt.expression = self._try_cse_expr(stmt.expression, current_block)
            return stmt

        if isinstance(stmt, PrintStatement):
            if hasattr(stmt, 'value') and stmt.value:
                stmt.value = self._try_cse_expr(stmt.value, current_block)
            if hasattr(stmt, 'arguments') and stmt.arguments:
                stmt.arguments = [self._try_cse_expr(a, current_block) for a in stmt.arguments]
            return stmt

        return stmt

    def _process_if(self, stmt: IfStatement, current_block: list) -> IfStatement:
        """处理 if 语句（条件、then、else 分别处理）"""
        stmt.condition = self._try_cse_expr(stmt.condition, current_block)
        # then 分支独立处理
        old_cache = self.expr_cache
        old_counter = self.temp_counter
        old_killed = self.killed_vars
        self.expr_cache = {}
        self.temp_counter = 0
        self.killed_vars = set()
        stmt.then_body = self._process_block(stmt.then_body)
        self.expr_cache = old_cache
        self.temp_counter = old_counter
        self.killed_vars = old_killed

        if stmt.else_body is not None:
            old_cache = self.expr_cache
            old_counter = self.temp_counter
            old_killed = self.killed_vars
            self.expr_cache = {}
            self.temp_counter = 0
            self.killed_vars = set()
            stmt.else_body = self._process_block(stmt.else_body)
            self.expr_cache = old_cache
            self.temp_counter = old_counter
            self.killed_vars = old_killed

        return stmt

    def _process_while(self, stmt: WhileStatement, current_block: list) -> WhileStatement:
        """处理 while 语句"""
        # 循环体结束基本块
        stmt.condition = self._try_cse_expr(stmt.condition, current_block)
        old_cache = self.expr_cache
        old_counter = self.temp_counter
        old_killed = self.killed_vars
        self.expr_cache = {}
        self.temp_counter = 0
        self.killed_vars = set()
        stmt.body = self._process_block(stmt.body)
        self.expr_cache = old_cache
        self.temp_counter = old_counter
        self.killed_vars = old_killed
        return stmt

    def _try_cse_expr(self, expr: ASTNode, current_block: list) -> ASTNode:
        """尝试对表达式做 CSE"""
        if expr is None:
            return expr

        # 字面量不参与 CSE
        if isinstance(expr, (NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral)):
            return expr

        # 简单标识符不参与 CSE
        if isinstance(expr, Identifier):
            return expr

        # 计算表达式的规范字符串表示
        key = self._expr_key(expr)
        if key is None:
            # 含有不确定部分（函数调用等），不参与 CSE
            return self._walk_and_no_cse(expr, current_block)

        if key in self.expr_cache:
            # 找到重复表达式，复用临时变量
            temp_var = self.expr_cache[key]
            return Identifier(name=temp_var, line=expr.line, column=expr.column)
        else:
            # 首次出现，记录到缓存
            temp_var = f'__cse_tmp_{self.temp_counter}'
            self.temp_counter += 1
            self.expr_cache[key] = temp_var
            # 仍然递归处理子表达式（不缓存它们）
            return self._walk_no_cse(expr, current_block)

    def _walk_no_cse(self, expr: ASTNode, current_block: list) -> ASTNode:
        """仅做表达式处理，不参与 CSE"""
        if isinstance(expr, BinaryOp):
            expr.left = self._try_cse_expr(expr.left, current_block)
            expr.right = self._try_cse_expr(expr.right, current_block)
        elif isinstance(expr, UnaryOp):
            expr.operand = self._try_cse_expr(expr.operand, current_block)
        elif isinstance(expr, FunctionCall):
            # 函数调用：内部参数可能参与 CSE，但调用本身不参与
            expr.arguments = [self._try_cse_expr(a, current_block) for a in expr.arguments]
        elif isinstance(expr, PropertyAccess):
            expr.obj = self._try_cse_expr(expr.obj, current_block)
        return expr

    def _walk_and_no_cse(self, expr: ASTNode, current_block: list) -> ASTNode:
        """对整个表达式递归处理但不参与 CSE"""
        return self._walk_no_cse(expr, current_block)

    def _expr_key(self, expr: ASTNode) -> str:
        """生成表达式的规范键（用于识别相同子表达式）"""
        if isinstance(expr, NumberLiteral):
            return f'num({expr.value})'
        if isinstance(expr, StringLiteral):
            return f'str({expr.value!r})'
        if isinstance(expr, BooleanLiteral):
            return f'bool({expr.value})'
        if isinstance(expr, NullLiteral):
            return 'null'
        if isinstance(expr, Identifier):
            return f'id({expr.name})'
        if isinstance(expr, BinaryOp):
            l = self._expr_key(expr.left)
            r = self._expr_key(expr.right)
            if l is None or r is None:
                return None
            return f'({l}{expr.operator}{r})'
        if isinstance(expr, UnaryOp):
            o = self._expr_key(expr.operand)
            if o is None:
                return None
            return f'({expr.operator}{o})'
        # 函数调用、成员访问等不参与 CSE
        return None

    def _invalidate_for_var(self, var_name: str):
        """使与某变量相关的缓存失效"""
        # 简化处理：所有缓存都失效（保守策略）
        self.expr_cache = {}
        self.killed_vars.add(var_name)

    def _invalidate_cache(self):
        """完全清空缓存"""
        self.expr_cache = {}
        self.killed_vars = set()
