"""
段言（Duan）编程语言 - Python代码生成器

将段言AST转换为Python代码
"""

from typing import List, Optional
from duan_parser_v3 import *
from keywords import VERB_ARITY


# 需要导入新的AST节点类型
from duan_parser_v3 import ImportStmt, ExportStmt, IndexAccess, BreakStmt, ContinueStmt, ClassInstantiation, MemberAccess, TryStmt, ThrowStmt, Parameter, ParameterList


# =============================================================================
# 代码生成错误
# =============================================================================

class CodeGenError(Exception):
    """代码生成错误"""
    def __init__(self, message: str, node_type: str = None):
        self.message = message
        self.node_type = node_type
        msg = f"代码生成错误: {message}"
        if node_type:
            msg += f" (节点类型: {node_type})"
        super().__init__(msg)


# =============================================================================
# Python代码生成器
# =============================================================================

class PythonCodeGenerator:
    """段言到Python代码生成器"""
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4空格缩进
        self.output_lines: List[str] = []
        
        # 追踪导入的符号
        self._imported_symbols: set = set()
        
        # 中文数字映射
        self.chinese_numbers = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000, '万': 10000
        }
        
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
            # 基础函数
            '打印': 'print',
            '显示': 'print',
            '读取': 'input',
            '长': 'len',
            '首': 'lambda x: x[0]',
            '末': 'lambda x: x[-1]',
            
            # 文件I/O
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
            
            # 路径操作
            '绝对路径': '_duan_builtin.绝对路径',
            '连接路径': '_duan_builtin.连接路径',
            '目录名': '_duan_builtin.目录名',
            '文件名': '_duan_builtin.文件名',
            '扩展名': '_duan_builtin.扩展名',
            
            # 系统函数
            '环境变量': '_duan_builtin.环境变量',
            '设置环境变量': '_duan_builtin.设置环境变量',
            '参数列表': '_duan_builtin.参数列表',
            '退出程序': '_duan_builtin.退出程序',
            '当前目录': '_duan_builtin.当前目录',
            '切换目录': '_duan_builtin.切换目录',
            '执行命令': '_duan_builtin.执行命令',
            
            # 字符串工具
            '转整数': '_duan_builtin.转整数',
            '转浮点': '_duan_builtin.转浮点',
            '转字符串': '_duan_builtin.转字符串',
            '字符串长度': '_duan_builtin.字符串长度',
            '分割字符串': '_duan_builtin.分割字符串',
            '连接字符串': '_duan_builtin.连接字符串',
            '替换字符串': '_duan_builtin.替换字符串',
            '去除空白': '_duan_builtin.去除空白',
            
            # 列表工具
            '列表长度': '_duan_builtin.列表长度',
            '列表获取': '_duan_builtin.列表获取',
            '列表追加': '_duan_builtin.列表追加',
            '列表弹出': '_duan_builtin.列表弹出',
            '列表排序': '_duan_builtin.列表排序',
            '列表反转': '_duan_builtin.列表反转',
            '列表包含': '_duan_builtin.列表包含',
            '列表创建': '_duan_builtin.列表创建',
            
            # 字典工具
            '字典创建': '_duan_builtin.字典创建',
            '字典设置': '_duan_builtin.字典设置',
            '字典删除': '_duan_builtin.字典删除',
            '字典键列表': '_duan_builtin.字典键列表',
            '字典值列表': '_duan_builtin.字典值列表',
            '字典项列表': '_duan_builtin.字典项列表',
            '字典包含键': '_duan_builtin.字典包含键',
            '字典获取': '_duan_builtin.字典获取',
            
            # 类型检查
            '是整数': '_duan_builtin.是整数',
            '是浮点': '_duan_builtin.是浮点',
            '是字符串': '_duan_builtin.是字符串',
            '是列表': '_duan_builtin.是列表',
            '是字典': '_duan_builtin.是字典',
            '是空': '_duan_builtin.是空',
        }
    
    def generate(self, module: Module) -> str:
        """生成Python代码"""
        self.output_lines = []
        
        # 添加文件头
        self._add_line("# 由段言编译器生成")
        self._add_line("# 源文件: 段言代码")
        self._add_line("")
        
        # 添加标准库导入
        self._add_line("import sys")
        self._add_line("import os")
        self._add_line("")
        self._add_line("try:")
        self._add_line("    import importlib.util")
        self._add_line("except ImportError:")
        self._add_line("    importlib = None")
        self._add_line("")
        self._add_line("try:")
        self._add_line("    _duan_stdlib = os.path.join(os.path.dirname(__file__), 'stdlib')")
        self._add_line("except NameError:")
        self._add_line("    _duan_stdlib = os.path.join(os.getcwd(), 'stdlib')")
        self._add_line("    if not os.path.isdir(_duan_stdlib):")
        self._add_line("        # 尝试父目录（当从子目录运行时）")
        self._add_line("        parent_stdlib = os.path.normpath(os.path.join(os.getcwd(), '..', 'stdlib'))")
        self._add_line("        if os.path.isdir(parent_stdlib):")
        self._add_line("            _duan_stdlib = parent_stdlib")
        self._add_line("")
        self._add_line("if os.path.isdir(_duan_stdlib) and _duan_stdlib not in sys.path:")
        self._add_line("    sys.path.insert(0, _duan_stdlib)")
        self._add_line("")
        self._add_line("if importlib:")
        self._add_line("    try:")
        self._add_line("        _duan_builtin_path = os.path.join(_duan_stdlib, 'builtins.py')")
        self._add_line("        if os.path.isfile(_duan_builtin_path):")
        self._add_line("            spec = importlib.util.spec_from_file_location('duan_builtins', _duan_builtin_path)")
        self._add_line("            _duan_builtin = importlib.util.module_from_spec(spec)")
        self._add_line("            spec.loader.exec_module(_duan_builtin)")
        self._add_line("        else:")
        self._add_line("            raise ImportError()")
        self._add_line("    except:")
        self._add_line("        import types")
        self._add_line("        _duan_builtin = types.ModuleType('_duan_builtin')")
        self._add_line("        _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()")
        self._add_line("        _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None")
        self._add_line("        _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)")
        self._add_line("        _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)")
        self._add_line("        _duan_builtin.打印 = print")
        self._add_line("        _duan_builtin.列表创建 = list")
        self._add_line("        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("        _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("        _duan_builtin.字符串长度 = len")
        self._add_line("        _duan_builtin.字典创建 = dict")
        self._add_line("        _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})")
        self._add_line("        _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)")
        self._add_line("else:")
        self._add_line("    import types")
        self._add_line("    _duan_builtin = types.ModuleType('_duan_builtin')")
        self._add_line("    _duan_builtin.打印 = print")
        self._add_line("")
        
        # 生成语句
        for stmt in module.statements:
            self._generate_statement(stmt)
        
        return '\n'.join(self.output_lines)
    
    def _add_line(self, line: str):
        """添加一行代码"""
        if line:
            self.output_lines.append(self.indent_str * self.indent_level + line)
        else:
            self.output_lines.append('')
    
    def _generate_statement(self, stmt: ASTNode):
        """生成语句"""
        if isinstance(stmt, VarDecl):
            self._generate_var_decl(stmt)
        elif isinstance(stmt, IfStmt):
            self._generate_if_stmt(stmt)
        elif isinstance(stmt, ForeachStmt):
            self._generate_foreach_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self._generate_while_stmt(stmt)
        elif isinstance(stmt, Paragraph):
            self._generate_paragraph(stmt)
        elif isinstance(stmt, ReturnStmt):
            self._generate_return_stmt(stmt)
        elif isinstance(stmt, ImportStmt):
            self._generate_import_stmt(stmt)
        elif isinstance(stmt, ExportStmt):
            # 导出语句在Python中不需要生成代码
            # Python通过 __all__ 或直接定义来实现导出
            self._generate_export_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            self._add_line("break")
        elif isinstance(stmt, ContinueStmt):
            self._add_line("continue")
        elif isinstance(stmt, TryStmt):
            self._generate_try_stmt(stmt)
        elif isinstance(stmt, ThrowStmt):
            self._generate_throw_stmt(stmt)
        elif isinstance(stmt, ParagraphCall):
            # 动词调用作为独立语句
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        elif isinstance(stmt, Identifier):
            # 标识符作为独立语句：生成为段落调用（带括号）
            name = self._sanitize_name(stmt.name)
            self._add_line(f"{name}()")
        elif isinstance(stmt, BinaryOp):
            # 二元运算作为独立语句
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        elif isinstance(stmt, Pipeline):
            # 管道操作作为独立语句
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        elif hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'SelfAssignment':
            # self赋值语句（新增）
            self._generate_self_assignment(stmt)
        elif hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'ClassDefinition':
            # 类定义（新增）
            self._generate_class_definition(stmt)
        elif isinstance(stmt, MemberAccess):
            # 成员访问作为独立语句
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        else:
            raise CodeGenError(f"未知语句类型", type(stmt).__name__)
    
    def _generate_var_decl(self, stmt: VarDecl):
        """生成变量声明"""
        name = self._sanitize_name(stmt.name)
        value = self._generate_expr(stmt.value)
        self._add_line(f"{name} = {value}")
    
    def _generate_if_stmt(self, stmt: IfStmt):
        """生成条件语句"""
        condition = self._generate_expr(stmt.condition)
        self._add_line(f"if {condition}:")
        
        self.indent_level += 1
        if stmt.then_body:
            for s in stmt.then_body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        
        if stmt.else_body:
            self._add_line("else:")
            self.indent_level += 1
            for s in stmt.else_body:
                self._generate_statement(s)
            self.indent_level -= 1
    
    def _generate_foreach_stmt(self, stmt: ForeachStmt):
        """生成遍历循环"""
        var_name = self._sanitize_name(stmt.variable)
        iterable = self._generate_expr(stmt.iterable)
        
        self._add_line(f"for {var_name} in {iterable}:")
        
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
    
    def _generate_while_stmt(self, stmt: WhileStmt):
        """生成当循环"""
        condition = self._generate_expr(stmt.condition)
        
        self._add_line(f"while {condition}:")
        
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
    
    def _generate_paragraph(self, stmt: Paragraph):
        """生成段落定义"""
        name = self._sanitize_name(stmt.name)
        
        # 从段落体中提取参数声明
        params = []
        body_without_params = []
        for s in (stmt.body or []):
            if isinstance(s, Parameter):
                params.append(self._sanitize_name(s.name))
            elif isinstance(s, ParameterList):
                # 处理参数列表语句
                for param_name in s.params:
                    params.append(self._sanitize_name(param_name))
            else:
                body_without_params.append(s)
        
        # 如果段落头有参数定义，也加入
        for param in (stmt.params or []):
            param_name = self._sanitize_name(param['name'])
            if param_name not in params:
                params.append(param_name)
        
        params_str = ', '.join(params) if params else ''
        
        # 函数定义
        self._add_line(f"def {name}({params_str}):")
        
        self.indent_level += 1
        if body_without_params:
            for s in body_without_params:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        
        self._add_line("")
    
    def _generate_return_stmt(self, stmt: ReturnStmt):
        """生成返回语句"""
        if stmt.value:
            value = self._generate_expr(stmt.value)
            self._add_line(f"return {value}")
        else:
            self._add_line("return")
    
    def _generate_try_stmt(self, stmt: TryStmt):
        """生成异常捕获语句"""
        # try块
        self._add_line("try:")
        self.indent_level += 1
        if stmt.try_body:
            for s in stmt.try_body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        
        # except块
        if stmt.catch_body:
            if stmt.catch_var:
                self._add_line(f"except Exception as {stmt.catch_var}:")
            else:
                self._add_line("except Exception:")
            
            self.indent_level += 1
            for s in stmt.catch_body:
                self._generate_statement(s)
            self.indent_level -= 1
        
        # finally块
        if stmt.finally_body:
            self._add_line("finally:")
            self.indent_level += 1
            for s in stmt.finally_body:
                self._generate_statement(s)
            self.indent_level -= 1
    
    def _generate_throw_stmt(self, stmt: ThrowStmt):
        """生成抛出异常语句"""
        value = self._generate_expr(stmt.value)
        self._add_line(f"raise {value}")
    
    def _generate_self_assignment(self, stmt):
        """生成self赋值语句"""
        attr_name = self._sanitize_name(stmt.attr_name)
        value = self._generate_expr(stmt.value)
        self._add_line(f"self.{attr_name} = {value}")
    
    def _generate_class_definition(self, stmt):
        """生成类定义"""
        class_name = self._sanitize_name(stmt.name)
        
        # 类定义行
        if stmt.base_class:
            base = self._sanitize_name(stmt.base_class)
            self._add_line(f"class {class_name}({base}):")
        else:
            self._add_line(f"class {class_name}:")
        
        self.indent_level += 1
        
        # 生成属性（使用类型注解）
        if hasattr(stmt, 'attributes') and stmt.attributes:
            for attr in stmt.attributes:
                attr_name = self._sanitize_name(attr.name)
                if attr.type_annotation:
                    attr_type = self._sanitize_name(attr.type_annotation)
                    self._add_line(f"{attr_name}: {attr_type}")
                if attr.default_value:
                    default = self._generate_expr(attr.default_value)
                    self._add_line(f"{attr_name} = {default}")
        
        # 生成方法
        if hasattr(stmt, 'methods') and stmt.methods:
            for method in stmt.methods:
                self._generate_method(method)
        
        # 如果类体为空，添加 pass
        if not (hasattr(stmt, 'attributes') and stmt.attributes) and not (hasattr(stmt, 'methods') and stmt.methods):
            self._add_line("pass")
        
        self.indent_level -= 1
        self._add_line("")
    
    def _generate_method(self, method):
        """生成方法定义"""
        method_name = method.name
        
        # 构造函数特殊处理
        if method.is_constructor or method_name == '构造':
            method_name = '__init__'
        
        # 参数列表（第一个参数是 self）
        params = ['self']
        if hasattr(method, 'parameters') and method.parameters:
            for param in method.parameters:
                param_name = self._sanitize_name(param.name)
                params.append(param_name)
        
        params_str = ', '.join(params)
        
        # 方法定义（必须包含括号）
        self._add_line(f"def {method_name}({params_str}):")
        
        self.indent_level += 1
        
        # 生成方法体
        if hasattr(method, 'body') and method.body:
            for stmt in method.body:
                if isinstance(stmt, tuple):
                    # 简化的语句表示
                    if stmt[0] == 'return':
                        value = self._generate_expr(stmt[1]) if stmt[1] else 'None'
                        self._add_line(f"return {value}")
                    elif stmt[0] == 'var':
                        var_name = self._sanitize_name(stmt[1])
                        var_value = self._generate_expr(stmt[2])
                        self._add_line(f"{var_name} = {var_value}")
                else:
                    # AST节点
                    self._generate_statement(stmt)
        else:
            self._add_line("pass")
        
        self.indent_level -= 1
        self._add_line("")
    
    def _generate_expr(self, expr: ASTNode) -> str:
        """生成表达式"""
        if expr is None:
            return 'None'
        
        if isinstance(expr, str):
            # 字符串字面量
            return f'"{expr}"'
        
        if isinstance(expr, (int, float)):
            # 数字字面量
            return str(expr)
        
        if isinstance(expr, NumberLiteral):
            # 检查是否是中文数字
            if expr.value in self.chinese_numbers:
                return str(self.chinese_numbers[expr.value])
            return str(expr.value)
        
        elif isinstance(expr, StringLiteral):
            # 转义引号
            escaped = expr.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        
        elif isinstance(expr, Identifier):
            name = self._sanitize_name(expr.name)
            # 检查是否是中文数字
            if expr.name in self.chinese_numbers:
                return str(self.chinese_numbers[expr.name])
            # 如果是导入的符号且无参数，生成为函数调用（0参数函数）
            if expr.name in self._imported_symbols:
                return f"{name}()"
            return name
        
        # 检查 ast_nodes 模块中的 Identifier（兼容两种定义）
        elif hasattr(expr, 'name') and hasattr(expr, 'line'):
            # 可能是来自 ast_nodes 的 Identifier
            return self._sanitize_name(expr.name)
        
        elif isinstance(expr, BinaryOp):
            left = self._generate_expr(expr.left)
            right = self._generate_expr(expr.right)
            op = self.operator_map.get(expr.operator, expr.operator)
            return f"({left} {op} {right})"
        
        elif isinstance(expr, ParagraphCall):
            name = self._sanitize_name(expr.name)
            
            # 检查是否是内置函数
            if expr.name in self.builtin_map:
                py_name = self.builtin_map[expr.name]
            else:
                py_name = name
            
            # 参数
            args = [self._generate_expr(arg) for arg in expr.args]
            args_str = ', '.join(args)
            
            return f"{py_name}({args_str})"
        
        elif isinstance(expr, Pipeline):
            # 管道操作：从左到右依次调用
            # 例如：数据 -> 过滤 -> 排序
            # 转换为：排序(过滤(数据))
            
            if len(expr.stages) == 1:
                return self._generate_expr(expr.stages[0])
            
            # 反向调用
            result = self._generate_expr(expr.stages[-1])
            for stage in reversed(expr.stages[:-1]):
                stage_expr = self._generate_expr(stage)
                result = f"{stage_expr}({result})"
            
            return result
        
        elif isinstance(expr, IndexAccess):
            # 索引访问：obj[index]
            obj = self._generate_expr(expr.obj)
            index = self._generate_expr(expr.index)
            return f"{obj}[{index}]"
        
        elif isinstance(expr, ClassInstantiation):
            # 类实例化：类名(参数...)
            class_name = self._sanitize_name(expr.class_name)
            args = [self._generate_expr(arg) for arg in expr.args]
            args_str = ', '.join(args)
            return f"{class_name}({args_str})"
        
        elif isinstance(expr, MemberAccess):
            # 成员访问：obj.member 或 obj.method(args...)
            obj = self._generate_expr(expr.obj)
            member = self._sanitize_name(expr.member)
            
            if expr.is_method_call:
                # 方法调用
                args = [self._generate_expr(arg) for arg in expr.args]
                args_str = ', '.join(args)
                return f"{obj}.{member}({args_str})"
            else:
                # 属性访问
                return f"{obj}.{member}"
        
        elif isinstance(expr, ListLiteral):
            # 列表字面量
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"
        
        else:
            raise CodeGenError(f"未知表达式类型", type(expr).__name__)
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称（转换为合法Python标识符）"""
        # 中文变量名在Python3中是合法的
        # 但为了更好的兼容性，可以选择转拼音或保留中文
        
        # 如果名称以ASCII数字开头，加前缀"_"
        if name and '0' <= name[0] <= '9':
            return f"_{name}"
        
        # 简单方案：保留中文
        return name
    
    def _generate_import_stmt(self, stmt: ImportStmt):
        """生成导入语句"""
        module_name = stmt.module_name
        
        if stmt.symbols:
            # 从...导入：from 数学 import 平方根, 幂
            symbols_str = ', '.join(stmt.symbols)
            self._add_line(f"from {module_name} import {symbols_str}")
            # 追踪导入的符号
            for symbol in stmt.symbols:
                self._imported_symbols.add(symbol)
        else:
            # 导入整个模块：import 数学
            if stmt.alias:
                self._add_line(f"import {module_name} as {stmt.alias}")
                self._imported_symbols.add(stmt.alias)
            else:
                self._add_line(f"import {module_name}")
                self._imported_symbols.add(module_name)
    
    def _is_chinese(self, text: str) -> bool:
        """判断字符串是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def _generate_export_stmt(self, stmt: ExportStmt):
        """生成导出语句"""
        if stmt.symbols == ['*']:
            # 导出全部：生成 __all__ 包含所有函数
            # 注意：这需要在编译器中收集所有函数名
            # 简化处理：生成注释
            self._add_line("# 导出全部")
        else:
            # 导出指定符号：生成 __all__ 列表
            symbols_str = ', '.join(f"'{s}'" for s in stmt.symbols)
            self._add_line(f"__all__ = [{symbols_str}]")


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    from duan_parser_v3 import DuanParser
    
    print("=" * 60)
    print("段言Python代码生成器测试")
    print("=" * 60)
    
    # 测试代码
    test_cases = [
        # 变量声明
        ('变量声明', '定义甲等于三。'),
        
        # 运算
        ('运算', '定义丙等于三加五。'),
        
        # 条件语句
        ('条件', '如果甲大于十那么打印甲。'),
        
        # 段落定义
        ('段落', '《计算》段(甲, 乙)：返回甲加乙。'),
        
        # 管道操作
        ('管道', '数据 -> 过滤 -> 排序。'),
    ]
    
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    for name, code in test_cases:
        print(f"\n--- 测试: {name} ---")
        print(f"段言代码: {code}")
        
        try:
            # 解析
            module = parser.parse(code)
            
            # 生成Python代码
            python_code = generator.generate(module)
            
            print(f"\nPython代码:")
            print(python_code)
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
