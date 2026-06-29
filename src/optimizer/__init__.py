from .base import Optimizer
from .constant_fold import ConstantFoldingOptimizer
from .dead_code import DeadCodeEliminationOptimizer
from .loop_invariant import LoopInvariantOptimizer
from .peephole import PeepholeOptimizer
from .cse import CommonSubexpressionEliminationOptimizer
from .inline import InlineOptimizer

__all__ = [
    "Optimizer",
    "ConstantFoldingOptimizer",
    "DeadCodeEliminationOptimizer",
    "LoopInvariantOptimizer",
    "PeepholeOptimizer",
    "CommonSubexpressionEliminationOptimizer",
    "InlineOptimizer",
]
