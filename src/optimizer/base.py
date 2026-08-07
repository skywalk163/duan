"""优化器基类"""

import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ast_nodes import ASTNode, Module


class OptimizerStats:
    """优化器统计信息

    记录优化耗时、优化前后对比、优化效果等指标。
    """

    def __init__(self, name: str):
        self.name = name
        self.start_time = 0.0
        self.end_time = 0.0
        self.initial_stmt_count = 0
        self.final_stmt_count = 0
        self.initial_expr_count = 0
        self.final_expr_count = 0
        self.optimizations_applied = 0
        self.status = 'pending'  # pending | running | done | skipped

    @property
    def elapsed(self) -> float:
        if self.end_time > 0:
            return self.end_time - self.start_time
        return 0.0

    @property
    def stmt_reduction(self) -> int:
        return self.initial_stmt_count - self.final_stmt_count

    @property
    def stmt_reduction_pct(self) -> float:
        if self.initial_stmt_count > 0:
            return (self.stmt_reduction / self.initial_stmt_count) * 100
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'elapsed': self.elapsed,
            'initial_stmt_count': self.initial_stmt_count,
            'final_stmt_count': self.final_stmt_count,
            'stmt_reduction': self.stmt_reduction,
            'stmt_reduction_pct': self.stmt_reduction_pct,
            'optimizations_applied': self.optimizations_applied,
            'status': self.status,
        }

    def __repr__(self) -> str:
        return (f"  {self.name}: {self.elapsed:.3f}s, 语句 {self.initial_stmt_count}->{self.final_stmt_count}"
                f" ({self.stmt_reduction_pct:+.1f}%), 优化 {self.optimizations_applied} 次 [{self.status}]")


class Optimizer(ABC):
    """优化器基类"""

    def __init__(self):
        self.stats: Optional[OptimizerStats] = None
        self._optimizations_applied = 0

    @abstractmethod
    def optimize(self, module: Module) -> Module:
        """优化整个模块，返回优化后的模块"""
        pass

    def optimize_expr(self, expr: ASTNode) -> ASTNode:
        """优化单个表达式，默认返回原值，子类可重写"""
        return expr

    def optimize_with_stats(self, module: Module) -> Module:
        """运行优化并收集统计信息

        Args:
            module: 输入的模块

        Returns:
            优化后的模块
        """
        # 创建统计信息
        name = self.__class__.__name__
        self.stats = OptimizerStats(name)
        self._optimizations_applied = 0

        # 统计优化前状态
        self.stats.initial_stmt_count = self._count_statements(module)
        self.stats.initial_expr_count = self._count_expressions(module)

        # 运行优化
        self.stats.start_time = time.time()
        self.stats.status = 'running'

        try:
            result = self.optimize(module)
            self.stats.status = 'done'
        except Exception as e:
            self.stats.status = 'skipped'
            result = module

        self.stats.end_time = time.time()

        # 统计优化后状态
        self.stats.final_stmt_count = self._count_statements(result)
        self.stats.final_expr_count = self._count_expressions(result)
        self.stats.optimizations_applied = self._optimizations_applied

        return result

    def _record_optimization(self, count: int = 1):
        """记录一次优化应用"""
        self._optimizations_applied += count

    def _compare_before_after(self, before: ASTNode, after: ASTNode) -> Dict[str, Any]:
        """比较优化前后表达式差异

        Args:
            before: 优化前的表达式
            after: 优化后的表达式

        Returns:
            差异信息字典
        """
        return {
            'before_type': type(before).__name__,
            'after_type': type(after).__name__,
            'changed': before is not after,
        }

    @staticmethod
    def _count_statements(module: Module) -> int:
        """统计模块中的语句数量"""
        count = len(module.statements) if hasattr(module, 'statements') else 0
        for seg in (module.segments if hasattr(module, 'segments') else []):
            if hasattr(seg, 'body'):
                count += len(seg.body)
        for cls_def in (module.classes if hasattr(module, 'classes') else []):
            if hasattr(cls_def, 'methods'):
                for method in cls_def.methods:
                    if hasattr(method, 'body'):
                        count += len(method.body)
            if hasattr(cls_def, 'constructor') and cls_def.constructor:
                if hasattr(cls_def.constructor, 'body'):
                    count += len(cls_def.constructor.body)
        return count

    @staticmethod
    def _count_expressions(module: Module) -> int:
        """统计模块中的表达式数量（粗略估算）"""
        # 简化实现：只统计顶层语句中的表达式
        count = 0
        for seg in (module.segments if hasattr(module, 'segments') else []):
            if hasattr(seg, 'body'):
                for stmt in seg.body:
                    count += Optimizer._stmt_expr_count(stmt)
        return count

    @staticmethod
    def _stmt_expr_count(stmt) -> int:
        """统计语句中的表达式数量"""
        if stmt is None:
            return 0
        # 基本统计
        if hasattr(stmt, 'value') and stmt.value is not None:
            return 1
        if hasattr(stmt, 'condition') and stmt.condition is not None:
            return 1
        if hasattr(stmt, 'expression') and stmt.expression is not None:
            return 1
        return 0