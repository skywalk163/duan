"""
段言（Duan）编程语言 - Python代码生成器（统一AST版本）

支持统一AST格式，兼容来自duan_ast和ast_unified的AST节点
集成类型推断系统，正确处理字符串连接和数字加法
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field

# 导入类型推断器
from type_inferencer import TypeInferencer, StringType, NumberType


# =============================================================================
# 工具函数
# =============================================================================

def is_instance(node, class_name):
    """检查节点是否为指定类型（通过名称检查，支持多个模块）"""
    if node is None:
        return False
    return type(node).__name__ == class_name


def get_attr(node, attr_name, default=None):
    """安全获取节点属性"""
    return getattr(node, attr_name, default)


# =============================================================================
# Python代码生成器
# =============================================================================

class UnifiedCodeGenerator:
    """段言到Python代码生成器（支持统一AST）"""
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4空格缩进
        self.output_lines: List[str] = []
        self.type_inferencer = TypeInferencer()
        self.type_cache: Dict[int, 'Type'] = {}  # 存储推断的类型
        self.user_functions = set()  # 用户定义的函数名
        
        # 运算符映射
        self.operator_map = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '>': '>',
            '<': '<',
            '==': '==',
            '!=': '!=',
            '>=': '>=',
            '<=': '<=',
            '加': '+',
            '减': '-',
            '乘': '*',
            '除': '/',
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '大于等于': '>=',
            '小于等于': '<=',
        }
        
        # 内置函数映射
        self.builtin_map = {
            '打印': 'print',
            '显示': 'print',
            '读取': 'input',
            # 列表操作动词
            '长': 'len',
            '首': '__import__("operator").itemgetter(0)',
            '末': '__import__("operator").itemgetter(-1)',
            '余': '__import__("builtins").slice(1, None)',
            '排序': 'sorted',
            '反转': 'reversed',
            '求和': 'sum',
            '求最大': 'max',
            '求最小': 'min',
            '去重': 'lambda x: list(dict.fromkeys(x))',
            '筛选': 'filter',
            '映射': 'map',
            # 文件操作动词
            '读取文件': '_duan_builtin.读取文件',
            '写入文件': '_duan_builtin.写入文件',
            '追加文件': '_duan_builtin.追加文件',
            '文件存在': '_duan_builtin.文件存在',
            '目录存在': '_duan_builtin.目录存在',
            '路径存在': '_duan_builtin.路径存在',
            '创建目录': '_duan_builtin.创建目录',
            '删除文件': '_duan_builtin.删除文件',
            '删除目录': '_duan_builtin.删除目录',
            '列出目录': '_duan_builtin.列出目录',
            '文件大小': '_duan_builtin.文件大小',
            '绝对路径': '_duan_builtin.绝对路径',
            '连接路径': '_duan_builtin.连接路径',
            '目录名': '_duan_builtin.目录名',
            '文件名': '_duan_builtin.文件名',
            '扩展名': '_duan_builtin.扩展名',
            # 系统操作动词
            '环境变量': '_duan_builtin.环境变量',
            '设置环境变量': '_duan_builtin.设置环境变量',
            '参数列表': '_duan_builtin.参数列表',
            '退出程序': '_duan_builtin.退出程序',
            '当前目录': '_duan_builtin.当前目录',
            '切换目录': '_duan_builtin.切换目录',
            '执行命令': '_duan_builtin.执行命令',
            # 字符串操作动词
            '转整数': '_duan_builtin.转整数',
            '转浮点': '_duan_builtin.转浮点',
            '转字符串': '_duan_builtin.转字符串',
            '字符串长度': '_duan_builtin.字符串长度',
            '分割字符串': '_duan_builtin.分割字符串',
            '连接字符串': '_duan_builtin.连接字符串',
            '替换字符串': '_duan_builtin.替换字符串',
            '去除空白': '_duan_builtin.去除空白',
            # 列表操作（备用）
            '列表长度': '_duan_builtin.列表长度',
            '列表获取': '_duan_builtin.列表获取',
            '列表追加': '_duan_builtin.列表追加',
            '列表弹出': '_duan_builtin.列表弹出',
            '列表排序': '_duan_builtin.列表排序',
            '列表反转': '_duan_builtin.列表反转',
            '列表包含': '_duan_builtin.列表包含',
            '列表创建': '_duan_builtin.列表创建',
            '字典创建': '_duan_builtin.字典创建',
            '字典设置': '_duan_builtin.字典设置',
            '字典删除': '_duan_builtin.字典删除',
            '字典键列表': '_duan_builtin.字典键列表',
            '字典值列表': '_duan_builtin.字典值列表',
            '字典项列表': '_duan_builtin.字典项列表',
            '字典包含键': '_duan_builtin.字典包含键',
            '字典获取': '_duan_builtin.字典获取',
            '是整数': '_duan_builtin.是整数',
            '是浮点': '_duan_builtin.是浮点',
            '是字符串': '_duan_builtin.是字符串',
            '是列表': '_duan_builtin.是列表',
            '是字典': '_duan_builtin.是字典',
            '是空': '_duan_builtin.是空',
        }
    
    def generate(self, module) -> str:
        """生成Python代码"""
        self.output_lines = []
        
        # 先进行类型推断
        self.type_cache = self.type_inferencer.infer(module)
        
        # 添加文件头
        self._add_line("# 由段言编译器生成")
        self._add_line("# 源文件: 段言代码")
        self._add_line("")
        
        # 添加标准库导入
        self._add_line("# 导入段言标准库")
        self._add_line("import sys")
        self._add_line("import importlib.util")
        self._add_line("try:")
        self._add_line("    spec = importlib.util.spec_from_file_location('duan_builtins', 'src/stdlib/builtins.py')")
        self._add_line("    _duan_builtin = importlib.util.module_from_spec(spec)")
        self._add_line("    spec.loader.exec_module(_duan_builtin)")
        self._add_line("except:")
        self._add_line("    import types")
        self._add_line("    _duan_builtin = types.ModuleType('_duan_builtin')")
        self._add_line("    _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()")
        self._add_line("    _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None")
        self._add_line("    _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)")
        self._add_line("    _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)")
        self._add_line("    _duan_builtin.打印 = print")
        self._add_line("    _duan_builtin.列表创建 = list")
        self._add_line("    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("    _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("    _duan_builtin.字符串长度 = len")
        self._add_line("    _duan_builtin.字典创建 = dict")
        self._add_line("    _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})")
        self._add_line("    _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)")
        self._add_line("")
        
        # 生成段落定义
        if hasattr(module, 'segments'):
            for segment in module.segments:
                self._generate_segment(segment)
        
        # 生成类定义
        if hasattr(module, 'classes'):
            for cls in module.classes:
                self._generate_class(cls)
        
        # 生成语句
        if hasattr(module, 'statements'):
            for stmt in module.statements:
                self._generate_statement(stmt)
        
        return '\n'.join(self.output_lines)
    
    def _add_line(self, line: str):
        """添加一行代码"""
        if line:
            self.output_lines.append(self.indent_str * self.indent_level + line)
        else:
            self.output_lines.append('')
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称（处理Python关键字冲突）"""
        python_keywords = {'def', 'class', 'if', 'else', 'for', 'while', 'return', 'import', 'from', 'print'}
        if name in python_keywords:
            return f"_{name}"
        return name
    
    def _generate_statement(self, stmt):
        """生成语句（支持统一AST）"""
        if stmt is None:
            return
        
        node_type = type(stmt).__name__
        
        # 变量声明
        if is_instance(stmt, 'VariableDeclaration'):
            self._generate_var_decl(stmt)
        
        # 条件语句
        elif is_instance(stmt, 'IfStatement'):
            self._generate_if_stmt(stmt)
        
        # 遍历循环
        elif is_instance(stmt, 'ForeachStatement'):
            self._generate_foreach_stmt(stmt)
        
        # 当循环
        elif is_instance(stmt, 'WhileStatement'):
            self._generate_while_stmt(stmt)
        
        # 返回语句
        elif is_instance(stmt, 'ReturnStatement'):
            self._generate_return_stmt(stmt)
        
        # 打印语句
        elif is_instance(stmt, 'PrintStatement'):
            self._generate_print_stmt(stmt)
        
        # 表达式语句
        elif is_instance(stmt, 'ExpressionStatement'):
            expr_code = self._generate_expr(stmt.expression)
            self._add_line(expr_code)
        
        # 赋值语句
        elif is_instance(stmt, 'Assignment'):
            target_code = self._generate_expr(stmt.target)
            value_code = self._generate_expr(stmt.value)
            self._add_line(f"{target_code} = {value_code}")
        
        # 跳出语句
        elif is_instance(stmt, 'BreakStatement'):
            self._add_line("break")
        
        # 跳过语句
        elif is_instance(stmt, 'ContinueStatement'):
            self._add_line("continue")
        
        # 异常处理
        elif is_instance(stmt, 'TryStatement'):
            self._generate_try_stmt(stmt)
        
        # 抛出异常
        elif is_instance(stmt, 'ThrowStatement'):
            value_code = self._generate_expr(stmt.value)
            self._add_line(f"raise {value_code}")
        
        # 导入语句
        elif is_instance(stmt, 'ImportStatement'):
            self._generate_import_stmt(stmt)
        
        # 导出语句
        elif is_instance(stmt, 'ExportStatement'):
            pass  # Python中不需要特殊处理
        
        # 函数调用作为语句
        elif is_instance(stmt, 'FunctionCall'):
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        
        # 标识符作为语句（调用）
        elif is_instance(stmt, 'Identifier'):
            name = self._sanitize_name(stmt.name)
            self._add_line(f"{name}()")
        
        # 段落定义
        elif is_instance(stmt, 'SegmentDefinition'):
            self._generate_segment(stmt)
        
        # 类定义
        elif is_instance(stmt, 'ClassDefinition'):
            self._generate_class(stmt)
        
        # 未知类型
        else:
            print(f"警告：未知语句类型: {node_type}")
    
    def _generate_var_decl(self, stmt):
        """生成变量声明"""
        name = self._sanitize_name(stmt.name)
        value = self._generate_expr(stmt.value)
        self._add_line(f"{name} = {value}")
    
    def _generate_if_stmt(self, stmt):
        """生成条件语句"""
        condition = self._generate_expr(stmt.condition)
        self._add_line(f"if {condition}:")
        
        self.indent_level += 1
        for s in stmt.then_body:
            self._generate_statement(s)
        self.indent_level -= 1
        
        # 处理elif
        if hasattr(stmt, 'elseif_conditions') and stmt.elseif_conditions:
            for i, elif_cond in enumerate(stmt.elseif_conditions):
                elif_body = stmt.elseif_bodies[i] if hasattr(stmt, 'elseif_bodies') and i < len(stmt.elseif_bodies) else []
                cond_code = self._generate_expr(elif_cond)
                self._add_line(f"elif {cond_code}:")
                self.indent_level += 1
                for s in elif_body:
                    self._generate_statement(s)
                self.indent_level -= 1
        
        # 处理else
        if hasattr(stmt, 'else_body') and stmt.else_body:
            self._add_line("else:")
            self.indent_level += 1
            for s in stmt.else_body:
                self._generate_statement(s)
            self.indent_level -= 1
    
    def _generate_foreach_stmt(self, stmt):
        """生成遍历循环"""
        var_name = self._sanitize_name(stmt.variable)
        iterable = self._generate_expr(stmt.iterable)
        self._add_line(f"for {var_name} in {iterable}:")
        
        self.indent_level += 1
        for s in stmt.body:
            self._generate_statement(s)
        self.indent_level -= 1
    
    def _generate_while_stmt(self, stmt):
        """生成当循环"""
        condition = self._generate_expr(stmt.condition)
        self._add_line(f"while {condition}:")
        
        self.indent_level += 1
        for s in stmt.body:
            self._generate_statement(s)
        self.indent_level -= 1
    
    def _generate_return_stmt(self, stmt):
        """生成返回语句"""
        if stmt.value is not None:
            value_code = self._generate_expr(stmt.value)
            self._add_line(f"return {value_code}")
        else:
            self._add_line("return")
    
    def _generate_print_stmt(self, stmt):
        """生成打印语句"""
        value_code = self._generate_expr(stmt.value)
        self._add_line(f"print({value_code})")
    
    def _generate_try_stmt(self, stmt):
        """生成异常处理"""
        self._add_line("try:")
        
        self.indent_level += 1
        for s in stmt.try_body:
            self._generate_statement(s)
        self.indent_level -= 1
        
        if stmt.catch_var:
            self._add_line(f"except Exception as {stmt.catch_var}:")
            self.indent_level += 1
            for s in stmt.catch_body:
                self._generate_statement(s)
            self.indent_level -= 1
        
        if hasattr(stmt, 'finally_body') and stmt.finally_body:
            self._add_line("finally:")
            self.indent_level += 1
            for s in stmt.finally_body:
                self._generate_statement(s)
            self.indent_level -= 1
    
    def _generate_import_stmt(self, stmt):
        """生成导入语句"""
        module_name = stmt.module.replace('《', '').replace('》', '')
        if hasattr(stmt, 'names') and stmt.names:
            names = ', '.join(stmt.names)
            self._add_line(f"from {module_name} import {names}")
        else:
            self._add_line(f"import {module_name}")
    
    def _generate_segment(self, segment):
        """生成段落定义"""
        name = self._sanitize_name(segment.name)
        
        # 记录用户定义的函数名
        self.user_functions.add(name)
        
        # 提取参数
        params = []
        if hasattr(segment, 'parameters'):
            for param in segment.parameters:
                params.append(self._sanitize_name(param.name))
        elif hasattr(segment, 'params'):
            for param in segment.params:
                if isinstance(param, dict) and 'name' in param:
                    params.append(self._sanitize_name(param['name']))
                else:
                    params.append(self._sanitize_name(str(param)))
        
        params_str = ', '.join(params) if params else ''
        
        # 函数定义
        self._add_line(f"def {name}({params_str}):")
        
        self.indent_level += 1
        if hasattr(segment, 'body') and segment.body:
            for s in segment.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        
        self._add_line("")
    
    def _generate_class(self, cls):
        """生成类定义"""
        name = self._sanitize_name(cls.name)
        
        # 处理继承
        bases = []
        if hasattr(cls, 'superclasses') and cls.superclasses:
            for base in cls.superclasses:
                if isinstance(base, str):
                    bases.append(self._sanitize_name(base))
                elif hasattr(base, 'name'):
                    bases.append(self._sanitize_name(base.name))
        
        bases_str = ', '.join(bases) if bases else ''
        
        # 类定义
        if bases_str:
            self._add_line(f"class {name}({bases_str}):")
        else:
            self._add_line(f"class {name}:")
        
        self.indent_level += 1
        
        # 生成字段
        if hasattr(cls, 'fields') and cls.fields:
            for field in cls.fields:
                if is_instance(field, 'VariableDeclaration') or is_instance(field, 'AttributeDeclaration'):
                    field_name = self._sanitize_name(field.name)
                    if hasattr(field, 'default_value') and field.default_value is not None:
                        value_code = self._generate_expr(field.default_value)
                        self._add_line(f"self.{field_name} = {value_code}")
                    else:
                        self._add_line(f"self.{field_name} = None")
        
        # 生成构造函数
        if hasattr(cls, 'constructor') and cls.constructor:
            self._generate_constructor(cls.constructor)
        
        # 生成方法
        if hasattr(cls, 'methods') and cls.methods:
            for method in cls.methods:
                self._generate_method(method)
        
        self.indent_level -= 1
        self._add_line("")
    
    def _generate_constructor(self, constructor):
        """生成构造函数"""
        params = ['self']
        if hasattr(constructor, 'parameters'):
            for param in constructor.parameters:
                params.append(self._sanitize_name(param.name))
        
        params_str = ', '.join(params)
        self._add_line(f"def __init__({params_str}):")
        
        self.indent_level += 1
        
        # 不自动调用父类构造函数，让用户在构造函数体中显式处理
        # 如果父类没有构造函数，这会导致问题，所以需要检查父类是否需要初始化
        # 简化方案：不调用super().__init__()，由构造函数体中的语句决定
        

        # 生成构造函数体（用户自己写赋值语句）
        if hasattr(constructor, 'body') and constructor.body:
            for s in constructor.body:
                self._generate_statement(s)
        
        self.indent_level -= 1
    
    def _generate_method(self, method):
        """生成方法定义"""
        name = self._sanitize_name(method.name)
        
        # 方法参数（第一个是self）
        params = ['self']
        if hasattr(method, 'parameters'):
            for param in method.parameters:
                params.append(self._sanitize_name(param.name))
        
        params_str = ', '.join(params)
        
        # 方法定义
        self._add_line(f"def {name}({params_str}):")
        
        self.indent_level += 1
        if hasattr(method, 'body') and method.body:
            for s in method.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
    
    def _generate_expr(self, expr):
        """生成表达式"""
        if expr is None:
            return "None"
        
        node_type = type(expr).__name__
        
        # 字面量
        if is_instance(expr, 'NumberLiteral'):
            return str(expr.value)
        
        elif is_instance(expr, 'StringLiteral'):
            return repr(expr.value)
        
        elif is_instance(expr, 'BooleanLiteral'):
            return 'True' if expr.value else 'False'
        
        elif is_instance(expr, 'NullLiteral'):
            return "None"
        
        # 标识符
        elif is_instance(expr, 'Identifier'):
            return self._sanitize_name(expr.name)
        
        elif is_instance(expr, 'SegmentName'):
            return self._sanitize_name(expr.name)
        
        # 二元运算
        elif is_instance(expr, 'BinaryOp'):
            left = self._generate_expr(expr.left)
            right = self._generate_expr(expr.right)
            op = self.operator_map.get(expr.operator, expr.operator)
            
            # 处理加法：如果任一操作数是字符串，需要进行类型转换
            if op == '+' and expr.operator in ['+', '加']:
                expr_type = self.type_cache.get(id(expr))
                left_type = self.type_cache.get(id(expr.left))
                right_type = self.type_cache.get(id(expr.right))
                
                if isinstance(expr_type, StringType):
                    # 结果是字符串，需要确保两边都是字符串
                    if not isinstance(left_type, StringType):
                        left = f"str({left})"
                    if not isinstance(right_type, StringType):
                        right = f"str({right})"
            
            return f"({left} {op} {right})"
        
        # 一元运算
        elif is_instance(expr, 'UnaryOp'):
            operand = self._generate_expr(expr.operand)
            return f"{expr.operator}{operand}"
        
        # 函数调用
        elif is_instance(expr, 'FunctionCall'):
            # 正确处理函数名（可能是 PropertyAccess、Identifier 等）
            func_expr = expr.name
            if is_instance(func_expr, 'PropertyAccess'):
                # 方法调用：obj.method(args)
                obj = self._generate_expr(func_expr.obj)
                func_name = f"{obj}.{func_expr.property_name}"
            elif is_instance(func_expr, 'Identifier'):
                func_name = self._sanitize_name(func_expr.name)
            elif hasattr(func_expr, 'name'):
                func_name = self._sanitize_name(func_expr.name)
            elif isinstance(func_expr, str):
                func_name = func_expr
            else:
                func_name = self._generate_expr(func_expr)
            
            # 检查是否是内置函数（用户定义的函数优先）
            if func_name not in self.user_functions and func_name in self.builtin_map:
                func_name = self.builtin_map[func_name]
            
            args = [self._generate_expr(arg) for arg in expr.arguments]
            args_str = ', '.join(args)
            return f"{func_name}({args_str})"
        
        # 属性访问
        elif is_instance(expr, 'PropertyAccess'):
            obj = self._generate_expr(expr.obj)
            return f"{obj}.{expr.property_name}"
        
        # 索引访问
        elif is_instance(expr, 'IndexAccess'):
            obj = self._generate_expr(expr.obj)
            index = self._generate_expr(expr.index)
            return f"{obj}[{index}]"
        
        # 列表字面量
        elif is_instance(expr, 'ListLiteral'):
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"
        
        # 字典字面量
        elif is_instance(expr, 'DictLiteral'):
            entries = []
            if hasattr(expr, 'entries'):
                for entry in expr.entries:
                    key = self._generate_expr(entry.key)
                    value = self._generate_expr(entry.value)
                    entries.append(f"{key}: {value}")
            elif hasattr(expr, 'elements'):
                for e in expr.elements:
                    if hasattr(e, 'key') and hasattr(e, 'value'):
                        key = self._generate_expr(e.key)
                        value = self._generate_expr(e.value)
                        entries.append(f"{key}: {value}")
            return f"{{{', '.join(entries)}}}"
        
        # 类实例化
        elif is_instance(expr, 'NewExpression'):
            class_name = self._sanitize_name(expr.class_name)
            args = [self._generate_expr(arg) for arg in expr.arguments]
            args_str = ', '.join(args)
            return f"{class_name}({args_str})"
        
        # 管道表达式
        elif is_instance(expr, 'PipeExpression'):
            exprs = [self._generate_expr(e) for e in expr.expressions]
            return '('.join(exprs) + ')' * (len(exprs) - 1)
        
        # 方法调用
        elif is_instance(expr, 'MethodCall'):
            obj = self._generate_expr(expr.obj)
            args = [self._generate_expr(arg) for arg in expr.arguments]
            args_str = ', '.join(args)
            return f"{obj}.{expr.method}({args_str})"
        
        # Self引用
        elif is_instance(expr, 'SelfReference'):
            return "self"
        
        # 默认：尝试直接转换为字符串
        return str(expr)


# 保持向后兼容性：旧名称别名
CodeGenerator = UnifiedCodeGenerator
