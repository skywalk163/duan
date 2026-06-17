"""段言解释器 - 运算操作混入模块"""

from interpreter_core import InterpreterCore, DuanValue, DuanError, Signal, ReturnSignal, BreakSignal, ContinueSignal
from duan_ast import BinaryOp, UnaryOp


class OperationsMixin:
    """运算操作混入类"""

    def _eval_binary_op(self, node: BinaryOp) -> DuanValue:
        """求值二元运算 - 优化版"""
        op = node.operator
        
        # 逻辑运算 - 需要短路求值
        if op in self._OP_AND:
            left = self._eval(node.left)
            if not left.is_truthy():
                return DuanValue(False, '布尔')
            return DuanValue(self._eval(node.right).is_truthy(), '布尔')
        
        if op in self._OP_OR:
            left = self._eval(node.left)
            if left.is_truthy():
                return DuanValue(True, '布尔')
            return DuanValue(self._eval(node.right).is_truthy(), '布尔')
        
        # 非短路运算：先求值左右操作数
        left = self._eval(node.left)
        right = self._eval(node.right)
        
        # 优化：直接访问 type_name 避免属性查找
        left_type = left.type_name
        right_type = right.type_name
        
        # 算术运算
        if op in self._OP_PLUS:
            # 列表拼接
            if left_type == '列' and right_type == '列':
                return DuanValue(left.value + right.value, '列')
            # 字符串拼接
            if left_type == '串' or right_type == '串':
                return DuanValue(str(left) + str(right), '串')
            return DuanValue(self._to_number(left) + self._to_number(right), '数')
        
        if op in self._OP_MINUS:
            return DuanValue(self._to_number(left) - self._to_number(right), '数')
        
        if op in self._OP_MULT:
            return DuanValue(self._to_number(left) * self._to_number(right), '数')
        
        if op in self._OP_DIV:
            r = self._to_number(right)
            if r == 0:
                raise RuntimeError("除以零")
            return DuanValue(self._to_number(left) / r, '数')
        
        if op in self._OP_MOD:
            return DuanValue(self._to_number(left) % self._to_number(right), '数')
        
        if op in self._OP_POW:
            return DuanValue(self._to_number(left) ** self._to_number(right), '数')
        
        # 比较运算
        if op in self._OP_GT:
            return DuanValue(self._to_number(left) > self._to_number(right), '布尔')
        
        if op in self._OP_LT:
            return DuanValue(self._to_number(left) < self._to_number(right), '布尔')
        
        if op in self._OP_EQ:
            return DuanValue(self._equals(left, right), '布尔')
        
        if op in self._OP_NE:
            return DuanValue(not self._equals(left, right), '布尔')
        
        if op in self._OP_GE:
            return DuanValue(self._to_number(left) >= self._to_number(right), '布尔')
        
        if op in self._OP_LE:
            return DuanValue(self._to_number(left) <= self._to_number(right), '布尔')
        
        raise RuntimeError(f"不支持的二元运算符: '{op}'")
    
    def _eval_unary_op(self, node: UnaryOp) -> DuanValue:
        """求值一元运算 - 优化版"""
        op = node.operator
        operand = self._eval(node.operand)
        
        if op in self._OP_NOT:
            return DuanValue(not operand.is_truthy(), '布尔')
        
        if op in self._OP_MINUS:
            val = self._to_number(operand)
            return DuanValue(-val, '数')
        
        raise RuntimeError(f"不支持的一元运算符: '{op}'")