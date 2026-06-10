"""
段言（Duan）编程语言 解释执行器

将 AST 节点解释执行为实际的运行结果。
支持：变量环境、表达式求值、语句执行、段落调用。
"""

import sys
import os
from typing import List, Optional, Union, Any, Dict, Tuple
from dataclasses import dataclass, field

# 导入 AST 节点
from duan_ast import (
    ASTNode, Module, NumberLiteral, StringLiteral, BooleanLiteral,
    NullLiteral, ListLiteral, DictLiteral, DictEntry,
    Identifier, SegmentName, ModuleName,
    BinaryOp, UnaryOp, FunctionCall, PipeExpression,
    PropertyAccess, IndexAccess,
    VariableDeclaration, Assignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    TryStatement, ThrowStatement, PrintStatement, ExpressionStatement,
    Parameter, SegmentDefinition, DataTypeDefinition, ErrorTypeDefinition,
    ImportStatement, ExportStatement,
)

# 导入模块解析器
from duan_module import ModuleResolver, ModuleError

# =============================================================================
# 运行时值类型
# =============================================================================

class DuanValue:
    """段言运行时值的包装"""
    
    def __init__(self, value: Any, type_name: str = None):
        self.value = value
        self.type_name = type_name or self._infer_type(value)
    
    def _infer_type(self, value: Any) -> str:
        if value is None:
            return '空'
        if isinstance(value, bool):
            return '布尔'
        if isinstance(value, (int, float)):
            return '数'
        if isinstance(value, str):
            return '串'
        if isinstance(value, list):
            return '列'
        if isinstance(value, dict):
            return '典'
        if isinstance(value, DuanFunction):
            return '段'
        return type(value).__name__
    
    def is_truthy(self) -> bool:
        """判断是否为真值"""
        if self.value is None:
            return False
        if isinstance(self.value, bool):
            return self.value
        if isinstance(self.value, (int, float)):
            return self.value != 0
        if isinstance(self.value, str):
            return len(self.value) > 0
        if isinstance(self.value, list):
            return len(self.value) > 0
        if isinstance(self.value, dict):
            return len(self.value) > 0
        return True
    
    def __repr__(self):
        return f"{self.type_name}({repr(self.value)})"
    
    def __str__(self):
        if self.value is None:
            return '空'
        if isinstance(self.value, bool):
            return '真' if self.value else '假'
        if isinstance(self.value, dict):
            items = ', '.join(f'{k}: {v}' for k, v in self.value.items())
            return f'【{items}】'
        return str(self.value)


class DuanFunction:
    """段言段落（函数）的运行时表示"""
    
    def __init__(self, definition: SegmentDefinition, closure: 'Environment'):
        self.definition = definition
        self.name = definition.name
        self.closure = closure  # 定义时的环境（闭包）
    
    def __repr__(self):
        return f"段({self.name})"


class DuanBuiltinFunction:
    """内置函数的运行时表示"""
    
    def __init__(self, name: str, func: callable, min_args: int = 0, max_args: int = None):
        self.name = name
        self.func = func
        self.min_args = min_args
        self.max_args = max_args
    
    def __repr__(self):
        return f"内置({self.name})"


# =============================================================================
# 环境管理
# =============================================================================

class Signal(BaseException):
    """控制流信号的基类"""
    pass


class ReturnSignal(Signal):
    """返回信号"""
    def __init__(self, value: DuanValue = None):
        self.value = value or DuanValue(None)


class BreakSignal(Signal):
    """跳出信号"""
    pass


class ContinueSignal(Signal):
    """跳过信号"""
    pass


class DuanError(Signal):
    """段言运行时错误（对应 抛出/捕获）"""
    def __init__(self, message: str, value: DuanValue = None):
        self.message = message
        self.value = value or DuanValue(message, '串')


class Environment:
    """变量环境（作用域链）"""
    
    def __init__(self, parent: Optional['Environment'] = None, name: str = "全局"):
        self.variables: Dict[str, DuanValue] = {}
        self.parent = parent
        self.name = name
    
    def define(self, name: str, value: DuanValue):
        """定义新变量（当前作用域）"""
        self.variables[name] = value
    
    def get(self, name: str) -> DuanValue:
        """获取变量值（沿作用域链查找）"""
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"未定义的变量: '{name}'")
    
    def set(self, name: str, value: DuanValue):
        """设置变量值（沿作用域链查找并修改）"""
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        raise NameError(f"未定义的变量: '{name}'")
    
    def has(self, name: str) -> bool:
        """检查变量是否存在"""
        if name in self.variables:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False
    
    def create_child(self, name: str = "局部") -> 'Environment':
        """创建子作用域"""
        return Environment(parent=self, name=name)
    
    def __repr__(self):
        return f"环境({self.name}, vars={len(self.variables)})"


# =============================================================================
# 解释器
# =============================================================================

class Interpreter:
    """段言解释器 - 将 AST 解释执行为结果"""

    def __init__(self, search_paths: List[str] = None):
        self.global_env = Environment(name="全局")
        self.env = self.global_env
        self.output_lines: List[str] = []  # 打印/输出捕获
        self._break_encountered = False  # 标记是否遇到跳出
        self._register_builtins()
        # 模块系统
        self.module_resolver = ModuleResolver(search_paths=search_paths or ['.'])
        self.current_filepath: Optional[str] = None  # 当前执行的文件路径
        self._imported_modules: Set[str] = set()  # 已完全处理的模块（防循环）
    
    def _register_builtins(self):
        """注册内置函数"""
        builtins = [
            # 典操作
            DuanBuiltinFunction('_典', self._builtin_dict, min_args=0),
            # 类型转换
            DuanBuiltinFunction('_串化', self._builtin_to_string, min_args=1, max_args=1),
            DuanBuiltinFunction('_数化', self._builtin_to_number, min_args=1, max_args=1),
            # 字符分类
            DuanBuiltinFunction('_是中文', self._builtin_is_cjk, min_args=1, max_args=1),
            DuanBuiltinFunction('_是字母', self._builtin_is_letter, min_args=1, max_args=1),
            DuanBuiltinFunction('_是数字', self._builtin_is_digit, min_args=1, max_args=1),
            # 文件IO
            DuanBuiltinFunction('_读文件', self._builtin_read_file, min_args=1, max_args=1),
            DuanBuiltinFunction('_写文件', self._builtin_write_file, min_args=2, max_args=2),
        ]
        for b in builtins:
            self.global_env.define(b.name, DuanValue(b, '内置段'))
    
    # ----- 内置函数实现 -----
    
    def _builtin_dict(self, args: List[DuanValue]) -> DuanValue:
        """创建典：_典(键1, 值1, 键2, 值2, ...)"""
        result = {}
        for i in range(0, len(args), 2):
            if i + 1 >= len(args):
                raise RuntimeError("_典 需要偶数个参数（键值对）")
            key = args[i]
            if key.type_name not in ('串', '数', '布尔'):
                raise RuntimeError(f"典键不支持类型: '{key.type_name}'")
            result[key.value] = args[i + 1]
        return DuanValue(result, '典')
    
    def _builtin_to_string(self, args: List[DuanValue]) -> DuanValue:
        """转换为字符串"""
        return DuanValue(str(args[0]), '串')
    
    def _builtin_to_number(self, args: List[DuanValue]) -> DuanValue:
        """转换为数字"""
        try:
            val = args[0].value
            if isinstance(val, str):
                if '.' in val:
                    return DuanValue(float(val), '数')
                return DuanValue(int(val), '数')
            if isinstance(val, bool):
                return DuanValue(1 if val else 0, '数')
            if isinstance(val, (int, float)):
                return DuanValue(val, '数')
            raise ValueError()
        except (ValueError, TypeError):
            raise RuntimeError(f"无法转换为数字: '{args[0].value}'")
    
    def _builtin_is_cjk(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为中文字符"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        cp = ord(s)
        return DuanValue(
            0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0xF900 <= cp <= 0xFAFF,
            '布尔'
        )
    
    def _builtin_is_letter(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为英文字母"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        return DuanValue(('a' <= s <= 'z') or ('A' <= s <= 'Z') or s == '_', '布尔')
    
    def _builtin_is_digit(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为数字字符"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        return DuanValue('0' <= s <= '9', '布尔')
    
    def _builtin_read_file(self, args: List[DuanValue]) -> DuanValue:
        """读取文件内容"""
        path = str(args[0])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return DuanValue(content, '串')
        except Exception as e:
            raise RuntimeError(f"读取文件失败: {e}")
    
    def _builtin_write_file(self, args: List[DuanValue]) -> DuanValue:
        """写入文件内容"""
        path = str(args[0])
        content = str(args[1])
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return DuanValue(None, '空')
        except Exception as e:
            raise RuntimeError(f"写入文件失败: {e}")
    
    # ----- 顶层接口 -----
    
    def interpret(self, node: ASTNode) -> Optional[DuanValue]:
        """解释执行任意 AST 节点"""
        if isinstance(node, Module):
            return self._interpret_module(node)
        return self._execute(node)
    
    def interpret_module(self, module: Module, module_name: str = None) -> Optional[DuanValue]:
        """解释执行模块"""
        return self._interpret_module(module, module_name=module_name)
    
    def _interpret_module(self, module: Module, module_name: str = None) -> Optional[DuanValue]:
        # 记录本模块为已处理（防止循环导入时重复执行）
        if module_name:
            self._imported_modules.add(module_name)

        # 先处理导入（导入的段落优先注册到环境）
        for imp in module.imports:
            self._exec_import(imp)

        # 再注册当前模块的所有段落定义
        for seg in module.segments:
            func = DuanFunction(seg, self.env)
            self.env.define(seg.name, DuanValue(func, '段'))

        # 然后顺序执行顶层语句
        result = None
        for stmt in module.statements:
            try:
                result = self._execute(stmt)
            except ReturnSignal as rs:
                result = rs.value
                break
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return result
    
    def reset(self):
        """重置解释器状态"""
        self.global_env = Environment(name="全局")
        self.env = self.global_env
        self.output_lines = []
        self._break_encountered = False
        self._register_builtins()
        self.module_resolver.clear_cache()
        self.current_filepath = None
        self._imported_modules.clear()
    
    def get_output(self) -> str:
        """获取所有输出"""
        return '\n'.join(self.output_lines)
    
    # ----- 表达式求值 -----
    
    def _eval(self, node: ASTNode) -> DuanValue:
        """求值表达式"""
        if isinstance(node, NumberLiteral):
            return DuanValue(node.value, '数')
        
        if isinstance(node, StringLiteral):
            return DuanValue(node.value, '串')
        
        if isinstance(node, BooleanLiteral):
            return DuanValue(node.value, '布尔')
        
        if isinstance(node, NullLiteral):
            return DuanValue(None, '空')
        
        if isinstance(node, Identifier):
            return self.env.get(node.name)
        
        if isinstance(node, BinaryOp):
            return self._eval_binary_op(node)
        
        if isinstance(node, UnaryOp):
            return self._eval_unary_op(node)
        
        if isinstance(node, ListLiteral):
            return self._eval_list_literal(node)
        
        if isinstance(node, DictLiteral):
            return self._eval_dict_literal(node)
        
        if isinstance(node, IndexAccess):
            return self._eval_index_access(node)
        
        if isinstance(node, PropertyAccess):
            return self._eval_property_access(node)
        
        if isinstance(node, FunctionCall):
            return self._eval_function_call(node)
        
        if isinstance(node, PipeExpression):
            return self._eval_pipe(node)
        
        raise RuntimeError(f"不支持的表达式类型: {type(node).__name__}")
    
    def _eval_binary_op(self, node: BinaryOp) -> DuanValue:
        """求值二元运算"""
        op = node.operator
        
        # 逻辑运算 - 需要短路求值
        if op in ('且', 'AND', '&&'):
            left = self._eval(node.left)
            if not left.is_truthy():
                return DuanValue(False, '布尔')
            return DuanValue(self._eval(node.right).is_truthy(), '布尔')
        
        if op in ('或', 'OR', '||'):
            left = self._eval(node.left)
            if left.is_truthy():
                return DuanValue(True, '布尔')
            return DuanValue(self._eval(node.right).is_truthy(), '布尔')
        
        # 非短路运算：先求值左右操作数
        left = self._eval(node.left)
        right = self._eval(node.right)
        
        # 算术运算
        if op in ('加', 'PLUS', '+'):
            # 列表拼接
            if left.type_name == '列' and right.type_name == '列':
                return DuanValue(left.value + right.value, '列')
            # 字符串拼接
            if left.type_name == '串' or right.type_name == '串':
                return DuanValue(str(left) + str(right), '串')
            return DuanValue(self._to_number(left) + self._to_number(right), '数')
        
        if op in ('减', 'MINUS', '-', 'K_MINUS'):
            return DuanValue(self._to_number(left) - self._to_number(right), '数')
        
        if op in ('乘', 'MULTIPLY', '*'):
            return DuanValue(self._to_number(left) * self._to_number(right), '数')
        
        if op in ('除', 'DIVIDE', '/'):
            r = self._to_number(right)
            if r == 0:
                raise RuntimeError("除以零")
            return DuanValue(self._to_number(left) / r, '数')
        
        if op in ('模', 'MOD', '%'):
            return DuanValue(self._to_number(left) % self._to_number(right), '数')
        
        if op in ('幂', 'POW', '^'):
            return DuanValue(self._to_number(left) ** self._to_number(right), '数')
        
        # 比较运算
        if op in ('大于', 'GT', '>'):
            return DuanValue(self._to_number(left) > self._to_number(right), '布尔')
        
        if op in ('小于', 'LT', '<'):
            return DuanValue(self._to_number(left) < self._to_number(right), '布尔')
        
        if op in ('等于', 'EQ', '=='):
            return DuanValue(self._equals(left, right), '布尔')
        
        if op in ('不等于', 'NE', '!='):
            return DuanValue(not self._equals(left, right), '布尔')
        
        if op in ('大于等于', 'GE', '>='):
            return DuanValue(self._to_number(left) >= self._to_number(right), '布尔')
        
        if op in ('小于等于', 'LE', '<='):
            return DuanValue(self._to_number(left) <= self._to_number(right), '布尔')
        
        # 逻辑运算
        if op in ('且', 'AND', '&&'):
            return DuanValue(left.is_truthy() and right.is_truthy(), '布尔')
        
        if op in ('或', 'OR', '||'):
            return DuanValue(left.is_truthy() or right.is_truthy(), '布尔')
        
        raise RuntimeError(f"不支持的二元运算符: '{op}'")
    
    def _eval_unary_op(self, node: UnaryOp) -> DuanValue:
        """求值一元运算"""
        op = node.operator
        operand = self._eval(node.operand)
        
        if op in ('非', 'NOT', '!'):
            return DuanValue(not operand.is_truthy(), '布尔')
        
        if op in ('-', '减', 'K_MINUS'):
            val = self._to_number(operand)
            return DuanValue(-val, '数')
        
        raise RuntimeError(f"不支持的一元运算符: '{op}'")
    
    def _eval_list_literal(self, node: ListLiteral) -> DuanValue:
        """求值列表字面量"""
        elements = [self._eval(e) for e in node.elements]
        return DuanValue(elements, '列')
    
    def _eval_dict_literal(self, node: DictLiteral) -> DuanValue:
        """求值典字面量"""
        result = {}
        for entry in node.entries:
            key_val = self._eval(entry.key)
            val_val = self._eval(entry.value)
            # 键必须是可哈希的：串、数、布尔
            if key_val.type_name in ('串', '数', '布尔'):
                result[key_val.value] = val_val
            else:
                raise RuntimeError(f"典键不支持类型: '{key_val.type_name}'")
        return DuanValue(result, '典')
    
    def _eval_index_access(self, node: IndexAccess) -> DuanValue:
        """求值索引访问：对象[索引]"""
        obj = self._eval(node.obj)
        idx = self._eval(node.index)
        
        if obj.type_name == '典':
            key = idx.value
            if key not in obj.value:
                raise RuntimeError(f"典中不存在键: '{key}'")
            return obj.value[key]
        
        if obj.type_name == '串':
            # 字符串索引
            s = obj.value
            i = self._to_number(idx)
            if not isinstance(i, int):
                i = int(i)
            if i < 0 or i >= len(s):
                raise RuntimeError(f"字符串索引越界: {i}, 长度: {len(s)}")
            return DuanValue(s[i], '串')
        
        if obj.type_name == '列':
            lst = obj.value
            i = self._to_number(idx)
            if not isinstance(i, int):
                i = int(i)
            if i < 0 or i >= len(lst):
                raise RuntimeError(f"列表索引越界: {i}, 长度: {len(lst)}")
            return lst[i]
        
        raise RuntimeError(f"不支持索引访问的类型: '{obj.type_name}'")
    
    def _eval_property_access(self, node: PropertyAccess) -> DuanValue:
        """求值属性访问：对象之属性"""
        obj = self._eval(node.obj)
        prop = node.property_name
        
        if obj.type_name == '典':
            if prop == '长度':
                return DuanValue(len(obj.value), '数')
            if prop == '键列':
                return DuanValue([DuanValue(k, '串') if isinstance(k, str) else DuanValue(k) for k in obj.value.keys()], '列')
            if prop == '值列':
                return DuanValue(list(obj.value.values()), '列')
        
        if obj.type_name == '列':
            if prop == '长度':
                return DuanValue(len(obj.value), '数')
        
        if obj.type_name == '串':
            if prop == '长度':
                return DuanValue(len(obj.value), '数')
        
        # 字典/数据类型的属性访问
        if isinstance(obj.value, dict):
            if prop in obj.value:
                return obj.value[prop]
        
        raise RuntimeError(f"'{obj.type_name}' 没有属性 '{prop}'")
    
    def _eval_function_call(self, node: FunctionCall) -> DuanValue:
        """求值函数/段落调用"""
        # 获取函数名
        if isinstance(node.name, Identifier):
            func_name = node.name.name
        elif isinstance(node.name, SegmentName):
            func_name = node.name.name
        else:
            raise RuntimeError(f"不支持的函数名类型: {type(node.name).__name__}")
        
        # 求值参数
        args = [self._eval(a) for a in node.arguments]
        
        # 在环境中查找函数
        func_val = self.env.get(func_name)
        
        # 内置函数
        if isinstance(func_val.value, DuanBuiltinFunction):
            builtin = func_val.value
            if len(args) < builtin.min_args:
                raise RuntimeError(f"内置函数 '{func_name}' 需要至少 {builtin.min_args} 个参数")
            if builtin.max_args is not None and len(args) > builtin.max_args:
                raise RuntimeError(f"内置函数 '{func_name}' 最多接受 {builtin.max_args} 个参数")
            return builtin.func(args)
        
        if func_val.type_name != '段':
            raise RuntimeError(f"'{func_name}' 不是段落 (类型: {func_val.type_name})")
        
        func = func_val.value
        if not isinstance(func, DuanFunction):
            raise RuntimeError(f"'{func_name}' 不是可调用的段落")
        
        return self._call_function(func, args)
    
    def _call_function(self, func: DuanFunction, args: List[DuanValue]) -> DuanValue:
        """调用段落函数"""
        seg = func.definition
        
        # 创建新的作用域（闭包）
        call_env = func.closure.create_child(f"段({seg.name})")
        
        # 绑定参数
        param_names = [p.name for p in seg.parameters]
        for i, name in enumerate(param_names):
            if i < len(args):
                call_env.define(name, args[i])
            else:
                # 使用默认值
                param = seg.parameters[i]
                if param.default_value is not None:
                    # 默认值需要在定义时的环境中求值
                    old_env = self.env
                    self.env = func.closure
                    try:
                        default_val = self._eval(param.default_value)
                        call_env.define(name, default_val)
                    finally:
                        self.env = old_env
                else:
                    call_env.define(name, DuanValue(None, '空'))
        
        # 执行段落体
        old_env = self.env
        self.env = call_env
        try:
            result = DuanValue(None, '空')
            for stmt in seg.body:
                try:
                    self._execute(stmt)
                except ReturnSignal as rs:
                    result = rs.value or DuanValue(None, '空')
                    break
            return result
        finally:
            self.env = old_env
    
    def _eval_pipe(self, node: PipeExpression) -> DuanValue:
        """求值管道表达式"""
        current = self._eval(node.expressions[0])
        for i in range(1, len(node.expressions)):
            current = self._eval(node.expressions[i])
        return current
    
    # ----- 语句执行 -----
    
    def _execute(self, node: ASTNode):
        """执行语句"""
        if isinstance(node, VariableDeclaration):
            return self._exec_var_decl(node)
        if isinstance(node, Assignment):
            return self._exec_assignment(node)
        if isinstance(node, IfStatement):
            return self._exec_if(node)
        if isinstance(node, WhileStatement):
            return self._exec_while(node)
        if isinstance(node, ForeachStatement):
            return self._exec_foreach(node)
        if isinstance(node, PrintStatement):
            return self._exec_print(node)
        if isinstance(node, BreakStatement):
            raise BreakSignal()
        if isinstance(node, ContinueStatement):
            raise ContinueSignal()
        if isinstance(node, ReturnStatement):
            val = self._eval(node.value) if node.value else DuanValue(None, '空')
            raise ReturnSignal(val)
        if isinstance(node, ExpressionStatement):
            return self._eval(node.expression)
        if isinstance(node, TryStatement):
            return self._exec_try(node)
        if isinstance(node, ThrowStatement):
            val = self._eval(node.value)
            raise DuanError(str(val), val)
        if isinstance(node, ImportStatement):
            return self._exec_import(node)
        if isinstance(node, ExportStatement):
            # 导出语句在模块加载时已被处理，此处忽略
            return None
        # 跳过类型定义等
        return None
    
    def _exec_var_decl(self, node: VariableDeclaration):
        """执行变量声明"""
        value = DuanValue(None, '空')
        if node.value is not None:
            value = self._eval(node.value)
        self.env.define(node.name, value)
    
    def _exec_assignment(self, node: Assignment):
        """执行赋值"""
        target = node.target
        value = self._eval(node.value)
        
        if isinstance(target, Identifier):
            self.env.set(target.name, value)
        elif isinstance(target, PropertyAccess):
            # 属性赋值
            obj = self._eval(target.obj)
            if obj.type_name == '列' or obj.type_name == '串':
                raise RuntimeError(f"不能给 '{obj.type_name}' 类型赋值属性")
            if isinstance(obj.value, dict):
                obj.value[target.property_name] = value
            else:
                raise RuntimeError(f"不支持属性赋值的类型: '{obj.type_name}'")
        elif isinstance(target, IndexAccess):
            # 索引赋值
            obj = self._eval(target.obj)
            idx = self._eval(target.index)
            if obj.type_name == '典':
                obj.value[idx.value] = value
            elif obj.type_name == '列':
                i = self._to_number(idx)
                if not isinstance(i, int):
                    i = int(i)
                if i < 0 or i >= len(obj.value):
                    raise RuntimeError(f"列表索引越界: {i}")
                obj.value[i] = value
            else:
                raise RuntimeError(f"不支持索引赋值的类型: '{obj.type_name}'")
        else:
            raise RuntimeError(f"不支持的赋值目标: {type(target).__name__}")
    
    def _exec_if(self, node: IfStatement):
        """执行条件语句"""
        # 判断条件
        cond = self._eval(node.condition)
        
        if cond.is_truthy():
            self._execute_block(node.then_body)
            return
        
        # 检查 elseif
        for i, elseif_cond in enumerate(node.elseif_conditions):
            if self._eval(elseif_cond).is_truthy():
                self._execute_block(node.elseif_bodies[i])
                return
        
        # else 分支
        if node.else_body is not None:
            self._execute_block(node.else_body)
    
    def _exec_while(self, node: WhileStatement):
        """执行当循环"""
        while self._eval(node.condition).is_truthy():
            try:
                self._execute_block(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
    
    def _exec_foreach(self, node: ForeachStatement):
        """执行遍历循环"""
        iterable = self._eval(node.iterable)
        
        items = None
        if iterable.type_name == '列':
            items = iterable.value
        elif iterable.type_name == '典':
            items = [DuanValue(k, '串') if isinstance(k, str) else DuanValue(k) for k in iterable.value.keys()]
        else:
            raise RuntimeError(f"遍历目标必须是列表或典，实际类型: '{iterable.type_name}'")
        for item in items:
            self.env.define(node.variable, item)
            try:
                self._execute_block(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
    
    def _exec_print(self, node: PrintStatement):
        """执行打印语句"""
        value = self._eval(node.value)
        text = str(value)
        self.output_lines.append(text)
        # 同时输出到控制台
        print(text)
    
    def _exec_try(self, node: TryStatement):
        """执行异常捕获"""
        try:
            self._execute_block(node.try_body)
        except DuanError as e:
            catch_var = node.catch_var
            self.env.define(catch_var, e.value)
            self._execute_block(node.catch_body)

    def _exec_import(self, node: ImportStatement):
        """执行导入语句"""
        # ----- 直接导入（无模块名）：在当前环境中查找已注册的符号 -----
        if not node.module:
            for name in node.names:
                if not self.env.has(name):
                    raise RuntimeError(
                        f"直接导入失败: 未找到符号 '{name}'"
                    )
            return

        # ----- 从模块导入 -----
        # 已处理过的模块直接跳过
        if node.module in self._imported_modules:
            return

        # 计算 from_dir
        from_dir = None
        if self.current_filepath:
            from_dir = os.path.dirname(os.path.abspath(self.current_filepath))

        # 加载模块 AST
        try:
            module_ast, filepath = self.module_resolver.load_module(node.module, from_dir)
        except ModuleError as e:
            raise RuntimeError(f"导入失败: {e}")

        # ----- 递归处理被导入模块自身的依赖 -----
        self._imported_modules.add(node.module)

        old_filepath = self.current_filepath
        self.current_filepath = filepath
        try:
            for sub_import in module_ast.imports:
                self._exec_import(sub_import)

            # 将被导入模块的所有段落到全局环境（确保内部交叉调用可用）
            for seg in module_ast.segments:
                if not self.env.has(seg.name):
                    func = DuanFunction(seg, self.global_env)
                    self.env.define(seg.name, DuanValue(func, '段'))

            # 执行被导入模块的顶层语句
            old_env = self.env
            self.env = self.global_env
            try:
                for stmt in module_ast.statements:
                    try:
                        self._execute(stmt)
                    except (ReturnSignal, BreakSignal, ContinueSignal):
                        pass
            finally:
                self.env = old_env
        finally:
            self.current_filepath = old_filepath

        # ----- 验证并注册请求的导出符号 -----
        export_names = {exp.name for exp in module_ast.exports}
        segments_map = {seg.name: seg for seg in module_ast.segments}

        # 如果指定了要导入的名称，验证其可导出性
        if node.names:
            for name in node.names:
                if name not in segments_map:
                    raise RuntimeError(
                        f"模块 '{node.module}' 中未找到导出符号 '{name}'"
                    )
                if export_names and name not in export_names:
                    raise RuntimeError(
                        f"符号 '{name}' 未在模块 '{node.module}' 中导出"
                    )
                if not self.env.has(name):
                    func = DuanFunction(segments_map[name], self.global_env)
                    self.env.define(name, DuanValue(func, '段'))

    def _execute_block(self, statements: List[ASTNode]):
        """执行语句块"""
        for stmt in statements:
            self._execute(stmt)
    
    # ----- 辅助方法 -----
    
    def _to_number(self, val: DuanValue) -> Union[int, float]:
        """转换为数字"""
        if val.type_name == '数':
            return val.value
        if val.value is None:
            return 0
        if isinstance(val.value, bool):
            return 1 if val.value else 0
        if isinstance(val.value, str):
            try:
                if '.' in val.value:
                    return float(val.value)
                return int(val.value)
            except (ValueError, TypeError):
                raise RuntimeError(f"无法转换为数字: '{val.value}'")
        if isinstance(val.value, (int, float)):
            return val.value
        raise RuntimeError(f"无法转换为数字: 类型 '{val.type_name}'")
    
    def _equals(self, a: DuanValue, b: DuanValue) -> bool:
        """比较两个值是否相等"""
        if a.type_name != b.type_name:
            # 特殊处理：数字可跨类型比较
            if a.type_name == '数' and b.type_name == '数':
                return a.value == b.value
            return False
        if a.type_name == '空' and b.type_name == '空':
            return True
        return a.value == b.value


# =============================================================================
# 高层解释接口
# =============================================================================

def run_source(source: str, filepath: str = None, search_paths: List[str] = None) -> Interpreter:
    """解析并执行段言源代码

    Args:
        source: 段言源代码
        filepath: 源文件路径（用于模块相对导入）
        search_paths: 模块搜索路径列表

    Returns:
        执行后的解释器实例
    """
    from duan_visitor import DuanParser

    parser = DuanParser()
    module = parser.parse(source)
    if module is None:
        errors = '\n'.join(parser.errors)
        raise RuntimeError(f"解析失败:\n{errors}")

    interpreter = Interpreter(search_paths=search_paths)
    if filepath:
        interpreter.current_filepath = filepath
    # 从文件路径推导模块名
    module_name = None
    if filepath:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
    interpreter.interpret_module(module, module_name=module_name)
    return interpreter


def run_file(filepath: str, search_paths: List[str] = None) -> Interpreter:
    """从文件读取段言源代码并执行

    Args:
        filepath: 段言源文件路径
        search_paths: 模块搜索路径列表

    Returns:
        执行后的解释器实例
    """
    abs_path = os.path.abspath(filepath)
    with open(abs_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # 默认在文件所在目录搜索模块
    file_dir = os.path.dirname(abs_path)
    paths = search_paths or [file_dir, '.']

    return run_source(source, filepath=abs_path, search_paths=paths)


# =============================================================================
# CLI 入口
# =============================================================================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='段言编程语言解释器')
    parser.add_argument('file', nargs='?', help='段言源文件路径')
    parser.add_argument('-e', '--eval', help='直接执行代码字符串')
    
    args = parser.parse_args()
    
    try:
        if args.eval:
            interpreter = run_source(args.eval)
        elif args.file:
            interpreter = run_file(args.file)
        else:
            # REPL 模式
            print("段言 v0.1 交互模式 (输入 '退出()' 或 Ctrl+C 退出)")
            interpreter = Interpreter()
            while True:
                try:
                    line = input('段言> ')
                    if line.strip() in ('退出()', 'exit()', 'quit()'):
                        break
                    if not line.strip():
                        continue
                    try:
                        interpreter.interpret_module(
                            __import__('duan_visitor', fromlist=['DuanParser']).DuanParser().parse(line)
                        )
                    except Exception as e:
                        print(f"[错误] {e}")
                except (KeyboardInterrupt, EOFError):
                    print()
                    break
    except Exception as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()