from abc import ABC, abstractmethod
from ast_nodes import ASTNode, Module


class Optimizer(ABC):
    """优化器基类"""

    @abstractmethod
    def optimize(self, module: Module) -> Module:
        """优化整个模块，返回优化后的模块"""
        pass

    def optimize_expr(self, expr: ASTNode) -> ASTNode:
        """优化单个表达式，默认返回原值，子类可重写"""
        return expr
