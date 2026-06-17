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
    PropertyAccess, IndexAccess, NewExpression,
    VariableDeclaration, Assignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    TryStatement, ThrowStatement, PrintStatement, ExpressionStatement,
    Parameter, SegmentDefinition, DataTypeDefinition, ErrorTypeDefinition,
    ImportStatement, ExportStatement,
    ClassDefinition, InterfaceDefinition, MethodDefinition, ConstructorDefinition,
    InterfaceMethod, InterfaceProperty, SelfReference,
    AwaitExpression, DeferStatement, AsyncScope,
    StringInterpolation,
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
            return 'True' if self.value else 'False'
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


class DuanClass:
    """段言类的运行时表示"""
    
    def __init__(self, definition, closure):
        self.definition = definition
        self.name = definition.name
        self.superclasses = definition.superclasses
        self.interfaces = definition.interfaces
        self.closure = closure
        self.methods = {}
        for method in definition.methods:
            self.methods[method.name] = method
        self.constructor = definition.constructor
    
    def new_instance(self, args=None):
        return DuanInstance(self, args or [])
    
    def __repr__(self):
        return f"类({self.name})"


class DuanInterface:
    """段言接口的运行时表示"""
    
    def __init__(self, definition):
        self.definition = definition
        self.name = definition.name
        self.superinterfaces = definition.superinterfaces
        self.method_signatures = {}
        for method in definition.methods:
            self.method_signatures[method.name] = method
        self.properties = {}
        for prop in definition.properties:
            self.properties[prop.name] = prop
    
    def __repr__(self):
        return f"接口({self.name})"


class DuanInstance:
    """段言类实例的运行时表示"""
    
    def __init__(self, cls, args):
        self.cls = cls
        self.fields = {}
        
        for field in cls.definition.fields:
            if isinstance(field, VariableDeclaration):
                self.fields[field.name] = DuanValue(None, '空')
        
        # 调用构造函数
        if cls.constructor:
            self._call_constructor(args)
    
    def _call_constructor(self, args):
        """调用构造函数"""
        constructor = self.cls.constructor
        if constructor is None:
            return
        
        # 创建构造函数执行环境
        call_env = self.cls.closure.create_child(f"构造({self.cls.name})")
        
        # 绑定参数
        param_names = [p.name for p in constructor.parameters]
        for i, name in enumerate(param_names):
            if i < len(args):
                call_env.define(name, args[i])
            else:
                call_env.define(name, DuanValue(None, '空'))
        
        # 设置 self 引用
        call_env.define('自我', DuanValue(self, '实例'))
        
        # 将实例字段添加到调用环境中
        for field_name, field_value in self.fields.items():
            call_env.define(field_name, field_value)
        
        # 执行构造函数体
        from duan_interpreter import Interpreter
        interpreter = Interpreter()
        interpreter.env = call_env
        
        try:
            for stmt in constructor.body:
                interpreter._execute(stmt)
        finally:
            # 更新实例字段（构造函数中可能修改了字段值）
            for field_name in self.fields.keys():
                if call_env.has(field_name):
                    self.fields[field_name] = call_env.get(field_name)
    
    def get_field(self, name):
        if name in self.fields:
            return self.fields[name]
        raise RuntimeError(f"实例没有字段 '{name}'")
    
    def set_field(self, name, value):
        self.fields[name] = value
    
    def get_method(self, name):
        if name in self.cls.methods:
            return self.cls.methods[name]
        return None
    
    def __repr__(self):
        return f"实例({self.cls.name})"


class DuanBoundMethod:
    """绑定到实例的方法"""
    
    def __init__(self, instance, method):
        self.instance = instance
        self.method = method
    
    def __repr__(self):
        return f"方法({self.method.name})"


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
        # 优化：缓存变量查找结果
        self._cache: Dict[str, DuanValue] = {}
    
    def define(self, name: str, value: DuanValue):
        """定义新变量（当前作用域）"""
        self.variables[name] = value
        # 更新缓存
        self._cache[name] = value
    
    def get(self, name: str) -> DuanValue:
        """获取变量值（沿作用域链查找）- 优化版"""
        # 优化：先检查缓存
        cache = self._cache
        if name in cache:
            return cache[name]
        
        # 优化：使用局部变量减少属性查找
        vars = self.variables
        if name in vars:
            val = vars[name]
            cache[name] = val
            return val
        
        parent = self.parent
        if parent is not None:
            val = parent.get(name)
            cache[name] = val
            return val
        
        raise NameError(f"未定义的变量: '{name}'")
    
    def set(self, name: str, value: DuanValue):
        """设置变量值（沿作用域链查找并修改）- 优化版"""
        if name in self.variables:
            self.variables[name] = value
            # 更新缓存
            self._cache[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            # 更新缓存
            self._cache[name] = value
            return
        raise NameError(f"未定义的变量: '{name}'")
    
    def has(self, name: str) -> bool:
        """检查变量是否存在 - 优化版"""
        # 优化：先检查缓存
        if name in self._cache:
            return True
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

    # 预编译运算符映射表（类级别常量，避免重复创建）
    _OP_PLUS = ('加', 'PLUS', '+')
    _OP_MINUS = ('减', 'MINUS', '-', 'K_MINUS')
    _OP_MULT = ('乘', 'MULTIPLY', '*')
    _OP_DIV = ('除', 'DIVIDE', '/')
    _OP_MOD = ('模', 'MOD', '%')
    _OP_POW = ('幂', 'POW', '^')
    _OP_GT = ('大于', 'GT', '>')
    _OP_LT = ('小于', 'LT', '<')
    _OP_EQ = ('等于', 'EQ', '==')
    _OP_NE = ('不等于', 'NE', '!=')
    _OP_GE = ('大于等于', 'GE', '>=')
    _OP_LE = ('小于等于', 'LE', '<=')
    _OP_AND = ('且', 'and', 'AND', '&&')
    _OP_OR = ('或', 'or', 'OR', '||')
    _OP_NOT = ('非', 'NOT', '!')

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
        
        # 性能优化：缓存内置函数查找
        self._builtin_cache: Dict[str, Optional[DuanValue]] = {}
        self._fill_builtin_cache()

    def _fill_builtin_cache(self):
        """预填充内置函数缓存"""
        for name in ['abs', 'max', 'min', 'sqrt', 'pow', 'round', 'len', 'trim',
                     'substring', 'listLen', 'listAppend', 'listReverse',
                     'listIndexOf', 'listContains', 'listSlice', 'listConcat',
                     'printDebug', 'assert', '_典', '_串化', '_数化']:
            try:
                val = self.global_env.get(name)
                self._builtin_cache[name] = val
            except NameError:
                self._builtin_cache[name] = None

    def _register_builtins(self):
        """注册内置函数"""
        builtins = [
            # I/O操作
            DuanBuiltinFunction('打印', self._builtin_print, min_args=1),
            DuanBuiltinFunction('输出', self._builtin_print, min_args=1),
            # 典操作
            DuanBuiltinFunction('_典', self._builtin_dict, min_args=0),
            # 类型转换
            DuanBuiltinFunction('_串化', self._builtin_to_string, min_args=1, max_args=1),
            DuanBuiltinFunction('_数化', self._builtin_to_number, min_args=1, max_args=1),
            DuanBuiltinFunction('_布尔化', self._builtin_to_bool, min_args=1, max_args=1),
            # 字符分类
            DuanBuiltinFunction('_是中文', self._builtin_is_cjk, min_args=1, max_args=1),
            DuanBuiltinFunction('_是字母', self._builtin_is_letter, min_args=1, max_args=1),
            DuanBuiltinFunction('_是数字', self._builtin_is_digit, min_args=1, max_args=1),
            # 文件IO
            DuanBuiltinFunction('_读文件', self._builtin_read_file, min_args=1, max_args=1),
            DuanBuiltinFunction('_写文件', self._builtin_write_file, min_args=2, max_args=2),
            DuanBuiltinFunction('_文件存在', self._builtin_file_exists, min_args=1, max_args=1),
            # 数学函数
            DuanBuiltinFunction('abs', self._builtin_abs, min_args=1, max_args=1),
            DuanBuiltinFunction('max', self._builtin_max, min_args=2),
            DuanBuiltinFunction('min', self._builtin_min, min_args=2),
            DuanBuiltinFunction('sqrt', self._builtin_sqrt, min_args=1, max_args=1),
            DuanBuiltinFunction('pow', self._builtin_pow, min_args=2, max_args=2),
            DuanBuiltinFunction('round', self._builtin_round, min_args=1, max_args=1),
            DuanBuiltinFunction('sin', self._builtin_sin, min_args=1, max_args=1),
            DuanBuiltinFunction('cos', self._builtin_cos, min_args=1, max_args=1),
            DuanBuiltinFunction('tan', self._builtin_tan, min_args=1, max_args=1),
            DuanBuiltinFunction('log', self._builtin_log, min_args=1, max_args=1),
            DuanBuiltinFunction('exp', self._builtin_exp, min_args=1, max_args=1),
            DuanBuiltinFunction('floor', self._builtin_floor, min_args=1, max_args=1),
            DuanBuiltinFunction('ceil', self._builtin_ceil, min_args=1, max_args=1),
            # 字符串函数
            DuanBuiltinFunction('len', self._builtin_len, min_args=1, max_args=1),
            DuanBuiltinFunction('trim', self._builtin_trim, min_args=1, max_args=1),
            DuanBuiltinFunction('substring', self._builtin_substring, min_args=3, max_args=3),
            DuanBuiltinFunction('lower', self._builtin_lower, min_args=1, max_args=1),
            DuanBuiltinFunction('upper', self._builtin_upper, min_args=1, max_args=1),
            DuanBuiltinFunction('replace', self._builtin_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('split', self._builtin_split, min_args=2, max_args=2),
            DuanBuiltinFunction('join', self._builtin_join, min_args=2, max_args=2),
            DuanBuiltinFunction('indexOf', self._builtin_index_of, min_args=2, max_args=2),
            DuanBuiltinFunction('contains', self._builtin_contains, min_args=2, max_args=2),
            # 列表函数
            DuanBuiltinFunction('listLen', self._builtin_list_len, min_args=1, max_args=1),
            DuanBuiltinFunction('listAppend', self._builtin_list_append, min_args=2, max_args=2),
            DuanBuiltinFunction('listReverse', self._builtin_list_reverse, min_args=1, max_args=1),
            DuanBuiltinFunction('listIndexOf', self._builtin_list_index_of, min_args=2, max_args=2),
            DuanBuiltinFunction('listContains', self._builtin_list_contains, min_args=2, max_args=2),
            DuanBuiltinFunction('listSlice', self._builtin_list_slice, min_args=3, max_args=3),
            DuanBuiltinFunction('listConcat', self._builtin_list_concat, min_args=2, max_args=2),
            DuanBuiltinFunction('listSort', self._builtin_list_sort, min_args=1, max_args=1),
            DuanBuiltinFunction('listInsert', self._builtin_list_insert, min_args=3, max_args=3),
            DuanBuiltinFunction('listRemove', self._builtin_list_remove, min_args=2, max_args=2),
            DuanBuiltinFunction('listPop', self._builtin_list_pop, min_args=1, max_args=2),
            # 时间函数
            DuanBuiltinFunction('now', self._builtin_now, min_args=0, max_args=0),
            DuanBuiltinFunction('sleep', self._builtin_sleep, min_args=1, max_args=1),
            # 其他实用函数
            DuanBuiltinFunction('range', self._builtin_range, min_args=1, max_args=3),
            DuanBuiltinFunction('type', self._builtin_type, min_args=1, max_args=1),
            DuanBuiltinFunction('id', self._builtin_id, min_args=1, max_args=1),
            # 调试函数
            DuanBuiltinFunction('printDebug', self._builtin_print_debug, min_args=2, max_args=2),
            DuanBuiltinFunction('assert', self._builtin_assert, min_args=2, max_args=2),
            # 新数学函数
            DuanBuiltinFunction('随机整数', self._builtin_random_int, min_args=2, max_args=2),
            DuanBuiltinFunction('randomInt', self._builtin_random_int, min_args=2, max_args=2),
            DuanBuiltinFunction('随机浮点', self._builtin_random_float, min_args=0, max_args=0),
            DuanBuiltinFunction('randomFloat', self._builtin_random_float, min_args=0, max_args=0),
            DuanBuiltinFunction('阶乘', self._builtin_factorial, min_args=1, max_args=1),
            DuanBuiltinFunction('factorial', self._builtin_factorial, min_args=1, max_args=1),
            DuanBuiltinFunction('平均数', self._builtin_mean, min_args=1, max_args=1),
            DuanBuiltinFunction('mean', self._builtin_mean, min_args=1, max_args=1),
            DuanBuiltinFunction('中位数', self._builtin_median, min_args=1, max_args=1),
            DuanBuiltinFunction('median', self._builtin_median, min_args=1, max_args=1),
            DuanBuiltinFunction('求和', self._builtin_sum, min_args=1, max_args=1),
            DuanBuiltinFunction('sum', self._builtin_sum, min_args=1, max_args=1),
            DuanBuiltinFunction('圆周率', self._builtin_pi, min_args=0, max_args=0),
            DuanBuiltinFunction('pi', self._builtin_pi, min_args=0, max_args=0),
            DuanBuiltinFunction('自然常数', self._builtin_e, min_args=0, max_args=0),
            DuanBuiltinFunction('e', self._builtin_e, min_args=0, max_args=0),
            # JSON 函数
            DuanBuiltinFunction('解析JSON', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('解析字典', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('parseJSON', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('序列化JSON', self._builtin_stringify_json, min_args=1, max_args=2),
            DuanBuiltinFunction('序列化字典', self._builtin_stringify_json, min_args=1, max_args=2),
            DuanBuiltinFunction('stringifyJSON', self._builtin_stringify_json, min_args=1, max_args=2),
            # 日期时间函数
            DuanBuiltinFunction('当前时间', self._builtin_current_time, min_args=0, max_args=1),
            DuanBuiltinFunction('formatTime', self._builtin_current_time, min_args=0, max_args=1),
            DuanBuiltinFunction('当前日期', self._builtin_current_date, min_args=0, max_args=1),
            DuanBuiltinFunction('formatDate', self._builtin_current_date, min_args=0, max_args=1),
            DuanBuiltinFunction('时间戳', self._builtin_timestamp, min_args=0, max_args=0),
            DuanBuiltinFunction('timestamp', self._builtin_timestamp, min_args=0, max_args=0),
            DuanBuiltinFunction('格式化时间', self._builtin_format_time, min_args=2, max_args=2),
            DuanBuiltinFunction('formatTime', self._builtin_format_time, min_args=2, max_args=2),
            DuanBuiltinFunction('日期差', self._builtin_date_diff, min_args=2, max_args=2),
            DuanBuiltinFunction('dateDiff', self._builtin_date_diff, min_args=2, max_args=2),
            # 哈希函数
            DuanBuiltinFunction('MD5', self._builtin_md5, min_args=1, max_args=1),
            DuanBuiltinFunction('md5', self._builtin_md5, min_args=1, max_args=1),
            DuanBuiltinFunction('SHA256', self._builtin_sha256, min_args=1, max_args=1),
            DuanBuiltinFunction('sha256', self._builtin_sha256, min_args=1, max_args=1),
            DuanBuiltinFunction('Base64编码', self._builtin_base64_encode, min_args=1, max_args=1),
            DuanBuiltinFunction('base64Encode', self._builtin_base64_encode, min_args=1, max_args=1),
            DuanBuiltinFunction('Base64解码', self._builtin_base64_decode, min_args=1, max_args=1),
            DuanBuiltinFunction('base64Decode', self._builtin_base64_decode, min_args=1, max_args=1),
            # 正则表达式函数
            DuanBuiltinFunction('匹配', self._builtin_regex_match, min_args=2, max_args=2),
            DuanBuiltinFunction('regexMatch', self._builtin_regex_match, min_args=2, max_args=2),
            DuanBuiltinFunction('搜索', self._builtin_regex_search, min_args=2, max_args=2),
            DuanBuiltinFunction('regexSearch', self._builtin_regex_search, min_args=2, max_args=2),
            DuanBuiltinFunction('查找所有', self._builtin_regex_find_all, min_args=2, max_args=2),
            DuanBuiltinFunction('regexFindAll', self._builtin_regex_find_all, min_args=2, max_args=2),
            DuanBuiltinFunction('替换', self._builtin_regex_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('regexReplace', self._builtin_regex_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('分割', self._builtin_regex_split, min_args=2, max_args=2),
            DuanBuiltinFunction('regexSplit', self._builtin_regex_split, min_args=2, max_args=2),
        ]
        for b in builtins:
            self.global_env.define(b.name, DuanValue(b, '内置段'))
    
    # ----- 内置函数实现 -----

    def _builtin_print(self, args: List[DuanValue]) -> DuanValue:
        """打印输出"""
        text = ' '.join(str(a) for a in args)
        self.output_lines.append(text)
        print(text)
        return DuanValue(None, '空')

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
    
    def _builtin_file_exists(self, args: List[DuanValue]) -> DuanValue:
        """检查文件是否存在"""
        path = str(args[0])
        import os
        return DuanValue(os.path.exists(path), '布尔')
    
    def _builtin_to_bool(self, args: List[DuanValue]) -> DuanValue:
        """转换为布尔值"""
        val = args[0].value
        if val is None:
            return DuanValue(False, '布尔')
        if isinstance(val, bool):
            return DuanValue(val, '布尔')
        if isinstance(val, (int, float)):
            return DuanValue(val != 0, '布尔')
        if isinstance(val, str):
            return DuanValue(len(val) > 0, '布尔')
        if isinstance(val, (list, dict)):
            return DuanValue(len(val) > 0, '布尔')
        return DuanValue(bool(val), '布尔')
    
    # ----- 数学函数 -----
    
    def _builtin_abs(self, args: List[DuanValue]) -> DuanValue:
        """绝对值"""
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(abs(val), '数')
        raise RuntimeError("abs 需要数字参数")
    
    def _builtin_max(self, args: List[DuanValue]) -> DuanValue:
        """最大值"""
        max_val = None
        for arg in args:
            val = arg.value
            if not isinstance(val, (int, float)):
                raise RuntimeError("max 需要数字参数")
            if max_val is None or val > max_val:
                max_val = val
        return DuanValue(max_val, '数')
    
    def _builtin_min(self, args: List[DuanValue]) -> DuanValue:
        """最小值"""
        min_val = None
        for arg in args:
            val = arg.value
            if not isinstance(val, (int, float)):
                raise RuntimeError("min 需要数字参数")
            if min_val is None or val < min_val:
                min_val = val
        return DuanValue(min_val, '数')
    
    def _builtin_sqrt(self, args: List[DuanValue]) -> DuanValue:
        """平方根"""
        val = args[0].value
        if isinstance(val, (int, float)):
            if val < 0:
                raise RuntimeError("sqrt 参数不能为负数")
            return DuanValue(val ** 0.5, '数')
        raise RuntimeError("sqrt 需要数字参数")
    
    def _builtin_pow(self, args: List[DuanValue]) -> DuanValue:
        """幂运算"""
        base = args[0].value
        exp = args[1].value
        if isinstance(base, (int, float)) and isinstance(exp, (int, float)):
            return DuanValue(base ** exp, '数')
        raise RuntimeError("pow 需要数字参数")
    
    def _builtin_round(self, args: List[DuanValue]) -> DuanValue:
        """四舍五入"""
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(round(val), '数')
        raise RuntimeError("round 需要数字参数")
    
    def _builtin_sin(self, args: List[DuanValue]) -> DuanValue:
        """正弦函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.sin(val), '数')
        raise RuntimeError("sin 需要数字参数")
    
    def _builtin_cos(self, args: List[DuanValue]) -> DuanValue:
        """余弦函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.cos(val), '数')
        raise RuntimeError("cos 需要数字参数")
    
    def _builtin_tan(self, args: List[DuanValue]) -> DuanValue:
        """正切函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.tan(val), '数')
        raise RuntimeError("tan 需要数字参数")
    
    def _builtin_log(self, args: List[DuanValue]) -> DuanValue:
        """自然对数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            if val <= 0:
                raise RuntimeError("log 参数必须大于0")
            return DuanValue(math.log(val), '数')
        raise RuntimeError("log 需要数字参数")
    
    def _builtin_exp(self, args: List[DuanValue]) -> DuanValue:
        """指数函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.exp(val), '数')
        raise RuntimeError("exp 需要数字参数")
    
    def _builtin_floor(self, args: List[DuanValue]) -> DuanValue:
        """向下取整"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.floor(val), '数')
        raise RuntimeError("floor 需要数字参数")
    
    def _builtin_ceil(self, args: List[DuanValue]) -> DuanValue:
        """向上取整"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.ceil(val), '数')
        raise RuntimeError("ceil 需要数字参数")
    
    # ----- 字符串函数 -----
    
    def _builtin_len(self, args: List[DuanValue]) -> DuanValue:
        """长度"""
        val = args[0].value
        if isinstance(val, str):
            return DuanValue(len(val), '数')
        if isinstance(val, list):
            return DuanValue(len(val), '数')
        raise RuntimeError("len 需要字符串或列表参数")
    
    def _builtin_trim(self, args: List[DuanValue]) -> DuanValue:
        """去除首尾空白"""
        val = args[0].value
        if isinstance(val, str):
            return DuanValue(val.strip(), '串')
        raise RuntimeError("trim 需要字符串参数")
    
    def _builtin_substring(self, args: List[DuanValue]) -> DuanValue:
        """子串"""
        s = args[0].value
        start = args[1].value
        end = args[2].value
        if isinstance(s, str) and isinstance(start, int) and isinstance(end, int):
            return DuanValue(s[start:end], '串')
        raise RuntimeError("substring 参数类型错误")
    
    def _builtin_lower(self, args: List[DuanValue]) -> DuanValue:
        """转换为小写"""
        s = args[0].value
        if isinstance(s, str):
            return DuanValue(s.lower(), '串')
        raise RuntimeError("lower 需要字符串参数")
    
    def _builtin_upper(self, args: List[DuanValue]) -> DuanValue:
        """转换为大写"""
        s = args[0].value
        if isinstance(s, str):
            return DuanValue(s.upper(), '串')
        raise RuntimeError("upper 需要字符串参数")
    
    def _builtin_replace(self, args: List[DuanValue]) -> DuanValue:
        """字符串替换"""
        s = args[0].value
        old = args[1].value
        new = args[2].value
        if isinstance(s, str) and isinstance(old, str) and isinstance(new, str):
            return DuanValue(s.replace(old, new), '串')
        raise RuntimeError("replace 参数类型错误")
    
    def _builtin_split(self, args: List[DuanValue]) -> DuanValue:
        """字符串分割"""
        s = args[0].value
        sep = args[1].value
        if isinstance(s, str) and isinstance(sep, str):
            return DuanValue(s.split(sep), '列')
        raise RuntimeError("split 参数类型错误")
    
    def _builtin_join(self, args: List[DuanValue]) -> DuanValue:
        """列表拼接为字符串"""
        lst = args[0].value
        sep = args[1].value
        if isinstance(lst, list) and isinstance(sep, str):
            str_list = []
            for item in lst:
                if isinstance(item, DuanValue):
                    str_list.append(str(item.value))
                else:
                    str_list.append(str(item))
            return DuanValue(sep.join(str_list), '串')
        raise RuntimeError("join 参数类型错误")
    
    def _builtin_index_of(self, args: List[DuanValue]) -> DuanValue:
        """字符串索引查找"""
        s = args[0].value
        substr = args[1].value
        if isinstance(s, str) and isinstance(substr, str):
            return DuanValue(s.find(substr), '数')
        raise RuntimeError("indexOf 参数类型错误")
    
    def _builtin_contains(self, args: List[DuanValue]) -> DuanValue:
        """字符串包含检查"""
        s = args[0].value
        substr = args[1].value
        if isinstance(s, str) and isinstance(substr, str):
            return DuanValue(substr in s, '布尔')
        raise RuntimeError("contains 参数类型错误")
    
    # ----- 列表函数 -----
    
    def _builtin_list_len(self, args: List[DuanValue]) -> DuanValue:
        """列表长度"""
        val = args[0].value
        if isinstance(val, list):
            return DuanValue(len(val), '数')
        raise RuntimeError("listLen 需要列表参数")
    
    def _builtin_list_append(self, args: List[DuanValue]) -> DuanValue:
        """列表追加"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            lst.append(item)
            return DuanValue(None, '空')
        raise RuntimeError("listAppend 需要列表参数")
    
    def _builtin_list_reverse(self, args: List[DuanValue]) -> DuanValue:
        """列表反转"""
        lst = args[0].value
        if isinstance(lst, list):
            lst.reverse()
            return DuanValue(None, '空')
        raise RuntimeError("listReverse 需要列表参数")
    
    def _builtin_list_index_of(self, args: List[DuanValue]) -> DuanValue:
        """列表索引查找"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            for i, val in enumerate(lst):
                # 比较值而非对象引用
                val_val = val.value if isinstance(val, DuanValue) else val
                item_val = item.value if isinstance(item, DuanValue) else item
                if val_val == item_val:
                    return DuanValue(i, '数')
            return DuanValue(-1, '数')
        raise RuntimeError("listIndexOf 需要列表参数")
    
    def _builtin_list_contains(self, args: List[DuanValue]) -> DuanValue:
        """列表包含检查"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            item_val = item.value if isinstance(item, DuanValue) else item
            for val in lst:
                val_val = val.value if isinstance(val, DuanValue) else val
                if val_val == item_val:
                    return DuanValue(True, '布尔')
            return DuanValue(False, '布尔')
        raise RuntimeError("listContains 需要列表参数")
    
    def _builtin_list_slice(self, args: List[DuanValue]) -> DuanValue:
        """列表切片"""
        lst = args[0].value
        start = args[1].value
        end = args[2].value
        if isinstance(lst, list) and isinstance(start, int) and isinstance(end, int):
            return DuanValue(lst[start:end], '列')
        raise RuntimeError("listSlice 参数类型错误")
    
    def _builtin_list_concat(self, args: List[DuanValue]) -> DuanValue:
        """列表拼接"""
        lst1 = args[0].value
        lst2 = args[1].value
        if isinstance(lst1, list) and isinstance(lst2, list):
            return DuanValue(lst1 + lst2, '列')
        raise RuntimeError("listConcat 需要两个列表参数")
    
    def _builtin_list_sort(self, args: List[DuanValue]) -> DuanValue:
        """列表排序"""
        lst = args[0].value
        if isinstance(lst, list):
            lst.sort(key=lambda x: x.value if isinstance(x, DuanValue) else x)
            return DuanValue(None, '空')
        raise RuntimeError("listSort 需要列表参数")
    
    def _builtin_list_insert(self, args: List[DuanValue]) -> DuanValue:
        """列表插入"""
        lst = args[0].value
        index = args[1].value
        item = args[2]
        if isinstance(lst, list) and isinstance(index, int):
            lst.insert(index, item)
            return DuanValue(None, '空')
        raise RuntimeError("listInsert 参数类型错误")
    
    def _builtin_list_remove(self, args: List[DuanValue]) -> DuanValue:
        """列表移除元素"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            item_val = item.value if isinstance(item, DuanValue) else item
            for i, val in enumerate(lst):
                val_val = val.value if isinstance(val, DuanValue) else val
                if val_val == item_val:
                    del lst[i]
                    return DuanValue(None, '空')
            raise RuntimeError("元素不在列表中")
        raise RuntimeError("listRemove 需要列表参数")
    
    def _builtin_list_pop(self, args: List[DuanValue]) -> DuanValue:
        """列表弹出元素"""
        lst = args[0].value
        if isinstance(lst, list):
            if len(args) > 1:
                index = args[1].value
                if isinstance(index, int):
                    return lst.pop(index)
                raise RuntimeError("pop 索引必须是整数")
            return lst.pop()
        raise RuntimeError("listPop 需要列表参数")
    
    # ----- 时间函数 -----
    
    def _builtin_now(self, args: List[DuanValue]) -> DuanValue:
        """获取当前时间戳"""
        import time
        return DuanValue(time.time(), '数')
    
    def _builtin_sleep(self, args: List[DuanValue]) -> DuanValue:
        """暂停执行"""
        import time
        val = args[0].value
        if isinstance(val, (int, float)):
            time.sleep(val)
            return DuanValue(None, '空')
        raise RuntimeError("sleep 需要数字参数")
    
    # ----- 其他函数 -----
    
    def _builtin_range(self, args: List[DuanValue]) -> DuanValue:
        """生成范围列表"""
        if len(args) == 1:
            end = args[0].value
            if isinstance(end, int):
                return DuanValue(list(range(end)), '列')
        elif len(args) == 2:
            start = args[0].value
            end = args[1].value
            if isinstance(start, int) and isinstance(end, int):
                return DuanValue(list(range(start, end)), '列')
        elif len(args) == 3:
            start = args[0].value
            end = args[1].value
            step = args[2].value
            if isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
                return DuanValue(list(range(start, end, step)), '列')
        raise RuntimeError("range 参数类型错误")
    
    def _builtin_type(self, args: List[DuanValue]) -> DuanValue:
        """获取类型名称"""
        val = args[0]
        return DuanValue(val.type_name, '串')
    
    def _builtin_id(self, args: List[DuanValue]) -> DuanValue:
        """获取对象ID"""
        val = args[0].value
        return DuanValue(id(val), '数')
    
    # ----- 调试函数 -----
    
    def _builtin_print_debug(self, args: List[DuanValue]) -> DuanValue:
        """调试打印"""
        msg = str(args[0].value)
        val = str(args[1].value)
        self.output_lines.append(f"DEBUG: {msg} = {val}")
        print(f"DEBUG: {msg} = {val}")
        return DuanValue(None, '空')
    
    def _builtin_assert(self, args: List[DuanValue]) -> DuanValue:
        """断言"""
        condition = args[0].value
        msg = str(args[1].value)
        if not condition:
            self.output_lines.append(f"断言失败: {msg}")
            print(f"断言失败: {msg}")
            raise RuntimeError(f"断言失败: {msg}")
        return DuanValue(None, '空')
    
    # ----- 新数学函数 -----
    
    def _builtin_random_int(self, args: List[DuanValue]) -> DuanValue:
        """随机整数"""
        import random
        lo = int(args[0].value)
        hi = int(args[1].value)
        return DuanValue(random.randint(lo, hi), '数')
    
    def _builtin_random_float(self, args: List[DuanValue]) -> DuanValue:
        """随机浮点 [0,1)"""
        import random
        return DuanValue(random.random(), '数')
    
    def _builtin_factorial(self, args: List[DuanValue]) -> DuanValue:
        """阶乘"""
        n = int(args[0].value)
        if n < 0:
            raise RuntimeError("阶乘参数不能为负数")
        import math
        return DuanValue(math.factorial(n), '数')
    
    def _builtin_mean(self, args: List[DuanValue]) -> DuanValue:
        """平均数"""
        data = args[0].value
        if not isinstance(data, list) or len(data) == 0:
            raise RuntimeError("数据列表为空")
        import statistics
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(statistics.mean(values), '数')
    
    def _builtin_median(self, args: List[DuanValue]) -> DuanValue:
        """中位数"""
        data = args[0].value
        if not isinstance(data, list) or len(data) == 0:
            raise RuntimeError("数据列表为空")
        import statistics
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(statistics.median(values), '数')
    
    def _builtin_sum(self, args: List[DuanValue]) -> DuanValue:
        """求和"""
        data = args[0].value
        if not isinstance(data, list):
            raise RuntimeError("参数必须是列表")
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(sum(values), '数')
    
    def _builtin_pi(self, args: List[DuanValue]) -> DuanValue:
        """圆周率"""
        import math
        return DuanValue(math.pi, '数')
    
    def _builtin_e(self, args: List[DuanValue]) -> DuanValue:
        """自然常数"""
        import math
        return DuanValue(math.e, '数')
    
    # ----- JSON 函数 -----
    
    def _builtin_parse_json(self, args: List[DuanValue]) -> DuanValue:
        """解析JSON字符串"""
        import json
        text = str(args[0].value)
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return DuanValue(result, '典')
            elif isinstance(result, list):
                return DuanValue(result, '列')
            elif isinstance(result, str):
                return DuanValue(result, '串')
            elif isinstance(result, bool):
                return DuanValue(result, '布尔')
            elif isinstance(result, (int, float)):
                return DuanValue(result, '数')
            elif result is None:
                return DuanValue(None, '空')
            return DuanValue(result)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON解析失败: {e}")
    
    def _builtin_stringify_json(self, args: List[DuanValue]) -> DuanValue:
        """序列化为JSON字符串"""
        import json
        val = args[0].value
        indent = None
        if len(args) >= 2 and args[1].value is not None:
            indent = int(args[1].value)
        try:
            result = json.dumps(val, ensure_ascii=False, indent=indent)
            return DuanValue(result, '串')
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"JSON序列化失败: {e}")
    
    # ----- 日期时间函数 -----
    
    def _builtin_current_time(self, args: List[DuanValue]) -> DuanValue:
        """当前时间字符串"""
        from datetime import datetime
        fmt = '%Y-%m-%d %H:%M:%S'
        if args:
            fmt = str(args[0].value)
        return DuanValue(datetime.now().strftime(fmt), '串')
    
    def _builtin_current_date(self, args: List[DuanValue]) -> DuanValue:
        """当前日期字符串"""
        from datetime import date
        fmt = '%Y-%m-%d'
        if args:
            fmt = str(args[0].value)
        return DuanValue(date.today().strftime(fmt), '串')
    
    def _builtin_timestamp(self, args: List[DuanValue]) -> DuanValue:
        """当前时间戳"""
        import time
        return DuanValue(time.time(), '数')
    
    def _builtin_format_time(self, args: List[DuanValue]) -> DuanValue:
        """格式化时间"""
        from datetime import datetime
        time_str = str(args[0].value)
        fmt = str(args[1].value)
        try:
            dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            return DuanValue(dt.strftime(fmt), '串')
        except ValueError:
            try:
                dt = datetime.strptime(time_str, '%Y-%m-%d')
                return DuanValue(dt.strftime(fmt), '串')
            except ValueError:
                raise RuntimeError(f"无法解析时间: '{time_str}'")
    
    def _builtin_date_diff(self, args: List[DuanValue]) -> DuanValue:
        """日期差"""
        from datetime import datetime
        d1 = str(args[0].value)
        d2 = str(args[1].value)
        try:
            dt1 = datetime.strptime(d1, '%Y-%m-%d')
            dt2 = datetime.strptime(d2, '%Y-%m-%d')
            diff = (dt2 - dt1).days
            return DuanValue(diff, '数')
        except ValueError as e:
            raise RuntimeError(f"日期格式无效: {e}")
    
    # ----- 哈希函数 -----
    
    def _builtin_md5(self, args: List[DuanValue]) -> DuanValue:
        """MD5哈希"""
        import hashlib
        text = str(args[0].value)
        return DuanValue(hashlib.md5(text.encode('utf-8')).hexdigest(), '串')
    
    def _builtin_sha256(self, args: List[DuanValue]) -> DuanValue:
        """SHA256哈希"""
        import hashlib
        text = str(args[0].value)
        return DuanValue(hashlib.sha256(text.encode('utf-8')).hexdigest(), '串')
    
    def _builtin_base64_encode(self, args: List[DuanValue]) -> DuanValue:
        """Base64编码"""
        import base64
        text = str(args[0].value)
        return DuanValue(base64.b64encode(text.encode('utf-8')).decode('ascii'), '串')
    
    def _builtin_base64_decode(self, args: List[DuanValue]) -> DuanValue:
        """Base64解码"""
        import base64
        text = str(args[0].value)
        try:
            return DuanValue(base64.b64decode(text).decode('utf-8'), '串')
        except Exception as e:
            raise RuntimeError(f"Base64解码失败: {e}")
    
    # ----- 正则表达式函数 -----
    
    def _builtin_regex_match(self, args: List[DuanValue]) -> DuanValue:
        """正则匹配（开头匹配）"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        m = re.match(pattern, text)
        if m:
            return DuanValue(m.group(0), '串')
        return DuanValue(None, '空')
    
    def _builtin_regex_search(self, args: List[DuanValue]) -> DuanValue:
        """正则搜索（第一个匹配）"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        m = re.search(pattern, text)
        if m:
            return DuanValue(m.group(0), '串')
        return DuanValue(None, '空')
    
    def _builtin_regex_find_all(self, args: List[DuanValue]) -> DuanValue:
        """查找所有正则匹配"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        result = re.findall(pattern, text)
        return DuanValue(result, '列')
    
    def _builtin_regex_replace(self, args: List[DuanValue]) -> DuanValue:
        """正则替换"""
        import re
        pattern = str(args[0].value)
        repl = str(args[1].value)
        text = str(args[2].value)
        try:
            result = re.sub(pattern, repl, text)
            return DuanValue(result, '串')
        except re.error as e:
            raise RuntimeError(f"正则替换失败: {e}")
    
    def _builtin_regex_split(self, args: List[DuanValue]) -> DuanValue:
        """正则分割"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        result = re.split(pattern, text)
        return DuanValue(result, '列')
    
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

        # 注册类定义
        for cls in module.classes:
            class_obj = DuanClass(cls, self.env)
            self.env.define(cls.name, DuanValue(class_obj, '类'))

        # 注册接口定义
        for iface in module.interfaces:
            interface_obj = DuanInterface(iface)
            self.env.define(iface.name, DuanValue(interface_obj, '接口'))

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
    
    # 性能优化：使用类级别的方法映射表
    _EVAL_METHODS = {
        NumberLiteral: '_eval_number',
        StringLiteral: '_eval_string',
        BooleanLiteral: '_eval_boolean',
        NullLiteral: '_eval_null',
        Identifier: '_eval_identifier',
        BinaryOp: '_eval_binary_op',
        UnaryOp: '_eval_unary_op',
        ListLiteral: '_eval_list_literal',
        DictLiteral: '_eval_dict_literal',
        IndexAccess: '_eval_index_access',
        PropertyAccess: '_eval_property_access',
        FunctionCall: '_eval_function_call',
        PipeExpression: '_eval_pipe',
        NewExpression: '_eval_new_expression',
        SelfReference: '_eval_self_reference',
        AwaitExpression: '_eval_await',
    }

    def _eval(self, node: ASTNode) -> DuanValue:
        """求值表达式 - 优化版使用字典分发"""
        node_type = type(node)
        method_name = self._EVAL_METHODS.get(node_type)
        if method_name:
            return getattr(self, method_name)(node)
        
        # 兜底处理（使用 isinstance 作为备用）
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
        if isinstance(node, StringInterpolation):
            parts = []
            for part in node.parts:
                if isinstance(part, str):
                    parts.append(part)
                else:
                    val = self._eval(part)
                    parts.append(str(val.value))
            return DuanValue(''.join(parts), '串')
        
        raise RuntimeError(f"不支持的表达式类型: {type(node).__name__}")
    
    # 优化：独立的字面量求值方法（减少分支判断）
    def _eval_number(self, node: NumberLiteral) -> DuanValue:
        return DuanValue(node.value, '数')
    
    def _eval_string(self, node: StringLiteral) -> DuanValue:
        return DuanValue(node.value, '串')
    
    def _eval_boolean(self, node: BooleanLiteral) -> DuanValue:
        return DuanValue(node.value, '布尔')
    
    def _eval_null(self, node: NullLiteral) -> DuanValue:
        return DuanValue(None, '空')
    
    def _eval_identifier(self, node: Identifier) -> DuanValue:
        return self.env.get(node.name)
    
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
        
        # 对象实例的属性访问
        if obj.type_name == '实例':
            instance = obj.value
            if isinstance(instance, DuanInstance):
                # 先检查字段
                try:
                    return instance.get_field(prop)
                except RuntimeError:
                    pass
                # 再检查方法
                method = instance.get_method(prop)
                if method is not None:
                    # 返回一个包装的方法对象，供后续调用
                    return DuanValue(DuanBoundMethod(instance, method), '方法')
        
        # 字典/数据类型的属性访问
        if isinstance(obj.value, dict):
            if prop in obj.value:
                return obj.value[prop]
        
        raise RuntimeError(f"'{obj.type_name}' 没有属性 '{prop}'")
    
    def _eval_function_call(self, node: FunctionCall) -> DuanValue:
        """求值函数/段落调用 - 优化版"""
        # 获取函数名
        if isinstance(node.name, PropertyAccess):
            # 方法调用：对象之方法()
            # 先求值属性访问得到方法对象
            func_val = self._eval_property_access(node.name)
            args = [self._eval(a) for a in node.arguments]
            
            # 如果是绑定方法，直接调用
            if func_val.type_name == '方法':
                bound_method = func_val.value
                if isinstance(bound_method, DuanBoundMethod):
                    return self._call_method(bound_method, args)
            
            # 否则当作普通函数调用
            if isinstance(func_val.value, DuanFunction):
                return self._call_function(func_val.value, args)
            
            raise RuntimeError(f"'{func_val.type_name}' 不是可调用的")
        
        if isinstance(node.name, Identifier):
            func_name = node.name.name
        elif isinstance(node.name, SegmentName):
            func_name = node.name.name
        else:
            raise RuntimeError(f"不支持的函数名类型: {type(node.name).__name__}")
        
        # 求值参数
        args = [self._eval(a) for a in node.arguments]
        
        # 优化：首先检查内置函数缓存
        cached = self._builtin_cache.get(func_name)
        if cached is not None:
            func_val = cached
            if isinstance(func_val.value, DuanBuiltinFunction):
                builtin = func_val.value
                if len(args) < builtin.min_args:
                    raise RuntimeError(f"内置函数 '{func_name}' 需要至少 {builtin.min_args} 个参数")
                if builtin.max_args is not None and len(args) > builtin.max_args:
                    raise RuntimeError(f"内置函数 '{func_name}' 最多接受 {builtin.max_args} 个参数")
                return builtin.func(args)
        
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
        
        # 绑定方法调用
        if func_val.type_name == '方法':
            bound_method = func_val.value
            if isinstance(bound_method, DuanBoundMethod):
                return self._call_method(bound_method, args)
        
        if func_val.type_name != '段':
            raise RuntimeError(f"'{func_name}' 不是段落 (类型: {func_val.type_name})")
        
        func = func_val.value
        if not isinstance(func, DuanFunction):
            raise RuntimeError(f"'{func_name}' 不是可调用的段落")
        
        return self._call_function(func, args)
    
    def _eval_new_expression(self, node: NewExpression) -> DuanValue:
        """求值类实例化表达式（新类名()）"""
        class_name = node.class_name
        
        # 在环境中查找类
        class_val = self.env.get(class_name)
        if class_val.type_name != '类':
            raise RuntimeError(f"'{class_name}' 不是类（类型: {class_val.type_name}）")
        
        cls = class_val.value
        if not isinstance(cls, DuanClass):
            raise RuntimeError(f"'{class_name}' 不是有效的类定义")
        
        # 求值构造函数参数
        args = [self._eval(a) for a in node.arguments]
        
        # 创建实例
        instance = cls.new_instance(args)
        return DuanValue(instance, '实例')

    def _eval_self_reference(self, node: SelfReference) -> DuanValue:
        """求值 self 引用（己）"""
        return self.env.get('自我')

    def _eval_await(self, node: AwaitExpression) -> DuanValue:
        """求值等待表达式

        在同步解释器中，直接求值内部表达式。
        如果表达式返回协程/coroutine，则运行它直到完成。
        """
        result = self._eval(node.expression)
        # 如果结果是协程（异步函数调用返回），执行它
        if hasattr(result.value, '__await__') or hasattr(result.value, '__aenter__'):
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                try:
                    result = DuanValue(loop.run_until_complete(result.value), '数')
                finally:
                    loop.close()
            except (ImportError, RuntimeError, TypeError):
                pass  # 同步模式下直接返回
        return result

    def _call_method(self, bound_method: DuanBoundMethod, args: List[DuanValue]) -> DuanValue:
        """调用绑定到实例的方法"""
        method = bound_method.method
        instance = bound_method.instance
        
        # 创建方法执行环境
        call_env = instance.cls.closure.create_child(f"方法({method.name})")
        
        # 绑定参数
        param_names = [p.name for p in method.parameters]
        for i, name in enumerate(param_names):
            if i < len(args):
                call_env.define(name, args[i])
            else:
                call_env.define(name, DuanValue(None, '空'))
        
        # 设置 self 引用
        call_env.define('自我', DuanValue(instance, '实例'))
        
        # 将实例字段添加到调用环境中
        for field_name, field_value in instance.fields.items():
            call_env.define(field_name, field_value)
        
        # 执行方法体
        old_env = self.env
        self.env = call_env
        try:
            result = DuanValue(None, '空')
            for stmt in method.body:
                try:
                    self._execute(stmt)
                except ReturnSignal as rs:
                    result = rs.value
                    break
            return result
        finally:
            # 更新实例字段（方法中可能修改了字段值）
            for field_name in instance.fields.keys():
                if call_env.has(field_name):
                    instance.fields[field_name] = call_env.get(field_name)
            # 执行推迟栈
            self._run_defer_stack()
            self.env = old_env
    
    def _call_function(self, func: DuanFunction, args: List[DuanValue]) -> DuanValue:
        """调用段落函数 - 优化版"""
        seg = func.definition
        
        # 创建新的作用域（闭包）
        call_env = func.closure.create_child(f"段({seg.name})")
        
        # 优化：使用局部变量减少属性查找
        param_names = [p.name for p in seg.parameters]
        seg_body = seg.body
        
        # 绑定参数
        args_len = len(args)
        for i, name in enumerate(param_names):
            if i < args_len:
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
        
        # 执行段落体 - 优化：减少 try-finally 开销
        old_env = self.env
        self.env = call_env
        try:
            result = DuanValue(None, '空')
            for stmt in seg_body:
                try:
                    self._execute(stmt)
                except ReturnSignal as rs:
                    result = rs.value or DuanValue(None, '空')
                    break
            return result
        finally:
            # 执行推迟栈（后进先出）
            self._run_defer_stack()
            self.env = old_env

    def call_function(self, func_val: DuanValue, args: List[DuanValue]) -> Optional[DuanValue]:
        """公共接口：调用函数值 - 用于自举测试"""
        if isinstance(func_val.value, DuanFunction):
            return self._call_function(func_val.value, args)
        elif isinstance(func_val.value, DuanBuiltinFunction):
            return func_val.value.func(args)
        else:
            raise RuntimeError(f"无法调用非函数类型: {func_val.type_name}")
    
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
        # 异步/并发语句
        if isinstance(node, DeferStatement):
            return self._exec_defer(node)
        if isinstance(node, AsyncScope):
            return self._exec_async_scope(node)
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
            
            # 对象实例的字段赋值
            if obj.type_name == '实例':
                instance = obj.value
                if isinstance(instance, DuanInstance):
                    instance.set_field(target.property_name, value)
                    return
            
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

    def _exec_defer(self, node: DeferStatement):
        """执行推迟语句

        将推迟的语句保存到当前环境的延迟执行栈中，
        在作用域/段落退出时执行。
        """
        if not hasattr(self.env, '_defer_stack'):
            self.env._defer_stack = []
        # 将推迟语句体压栈（后进先出）
        self.env._defer_stack.append(node.body)

    def _run_defer_stack(self):
        """运行当前环境的推迟栈（后进先出）"""
        if hasattr(self.env, '_defer_stack') and self.env._defer_stack:
            while self.env._defer_stack:
                deferred_body = self.env._defer_stack.pop()
                try:
                    self._execute_block(deferred_body)
                except Exception as e:
                    # 推迟语句执行出错，打印错误但继续执行其余推迟
                    print(f"[推迟执行错误] {e}", file=sys.stderr)

    def _exec_async_scope(self, node: AsyncScope):
        """执行并行作用域（结构化并发）

        在同步解释器中，顺序执行所有任务。
        如果启用了 asyncio，使用 asyncio.gather 并发执行。
        """
        tasks = node.tasks
        if not tasks:
            return DuanValue(None, '空')

        try:
            import asyncio

            async def run_task(task_stmt):
                """执行单个异步任务"""
                if isinstance(task_stmt, ExpressionStatement) and isinstance(task_stmt.expression, AwaitExpression):
                    val = self._eval(task_stmt.expression)
                    return val
                return self._execute(task_stmt)

            async def run_all():
                results = await asyncio.gather(*[run_task(t) for t in tasks])
                return results

            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(run_all())
            finally:
                loop.close()
        except (ImportError, RuntimeError, TypeError):
            # 没有 asyncio 时顺序执行
            for task_stmt in tasks:
                self._execute(task_stmt)

        return DuanValue(None, '空')

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

            # 将被导入模块的所有段落和类注册到全局环境（确保内部交叉调用可用）
            for seg in module_ast.segments:
                if not self.env.has(seg.name):
                    func = DuanFunction(seg, self.global_env)
                    self.env.define(seg.name, DuanValue(func, '段'))
            
            # 注册类定义
            for cls in module_ast.classes:
                if not self.env.has(cls.name):
                    class_obj = DuanClass(cls, self.global_env)
                    self.env.define(cls.name, DuanValue(class_obj, '类'))

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
        # 构建符号映射（包括段落和类）
        symbols_map = {}
        for seg in module_ast.segments:
            symbols_map[seg.name] = ('segment', seg)
        for cls in module_ast.classes:
            symbols_map[cls.name] = ('class', cls)

        # 如果指定了要导入的名称，验证其可导出性
        if node.names:
            for name in node.names:
                if name not in symbols_map:
                    raise RuntimeError(
                        f"模块 '{node.module}' 中未找到导出符号 '{name}'"
                    )
                if export_names and name not in export_names:
                    raise RuntimeError(
                        f"符号 '{name}' 未在模块 '{node.module}' 中导出"
                    )
                if not self.env.has(name):
                    symbol_type, symbol_def = symbols_map[name]
                    if symbol_type == 'segment':
                        func = DuanFunction(symbol_def, self.global_env)
                        self.env.define(name, DuanValue(func, '段'))
                    elif symbol_type == 'class':
                        class_obj = DuanClass(symbol_def, self.global_env)
                        self.env.define(name, DuanValue(class_obj, '类'))

    def _execute_block(self, statements: List[ASTNode]):
        """执行语句块"""
        for stmt in statements:
            self._execute(stmt)
    
    # ----- 辅助方法 -----
    
    def _to_number(self, val: DuanValue) -> Union[int, float]:
        """转换为数字 - 优化版"""
        # 优化：直接访问 value 属性减少开销
        v = val.value
        type_name = val.type_name
        
        if type_name == '数':
            return v
        if v is None:
            return 0
        if isinstance(v, bool):
            return 1 if v else 0
        if isinstance(v, (int, float)):
            return v
        if isinstance(v, str):
            try:
                if '.' in v:
                    return float(v)
                return int(v)
            except (ValueError, TypeError):
                raise RuntimeError(f"无法转换为数字: '{v}'")
        raise RuntimeError(f"无法转换为数字: 类型 '{type_name}'")
    
    def _equals(self, a: DuanValue, b: DuanValue) -> bool:
        """比较两个值是否相等 - 优化版"""
        # 优化：直接访问 type_name 减少属性查找
        a_type = a.type_name
        b_type = b.type_name
        
        if a_type != b_type:
            return False
        if a_type == '空':
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