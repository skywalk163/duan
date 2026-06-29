"""
段言（Duan）编程语言 - Python代码生成器

将段言AST转换为Python代码
"""

from typing import List, Optional, Dict
from duan_parser_v3 import *
from keywords import VERB_ARITY
import ast_nodes as ast_nodes_module


# 需要导入新的AST节点类型
from duan_parser_v3 import ImportStmt, ExportStmt, IndexAccess, BreakStmt, ContinueStmt, ClassInstantiation, MemberAccess, TryStmt, ThrowStmt, Parameter, ParameterList, StringInterpolation, ListComprehension, LambdaExpression, MatchStmt, MatchCase, MatchPattern, DictComprehension, DestructuringAssignment, WithStmt, DecoratorDefinition, DictLiteral, InterfaceDefinition, MethodSignature, IndexedAssignment, RangeExpr


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
        self._indent_cache: Dict[int, str] = {}
        
        # 追踪导入的符号
        self._imported_symbols: set = set()
        
        # 是否需要导入 ABC/abstractmethod
        self._needs_abc = False
        
        # 中文数字映射
        self.chinese_numbers = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000, '万': 10000
        }
        
        # 类属性追踪（用于方法内自动添加 self. 前缀）
        self._class_attr_names: set = set()
        # 类方法名追踪（用于方法内自动添加 self. 前缀调用其他方法）
        self._class_method_names: set = set()
        self._in_class_method: bool = False
        # 当前方法参数名追踪（避免将参数名误判为类属性）
        self._current_method_params: set = set()
        
        # 方法名映射（中文到英文）
        self.method_name_map = {
            '追加': 'append',
            '添加': 'append',
            '长度': '__len__',
            '取长度': '__len__',
            '插入': 'insert',
            '删除': 'remove',
            '弹出': 'pop',
            '清空': 'clear',
            '反转': 'reverse',
            '排序': 'sort',
            '包含': '__contains__',
            '获取': '__getitem__',
            '设置': '__setitem__',
        }
        
        # 模块名映射（中文到Python模块）
        self.module_name_map = {
            'JSON': 'json',
            '日期时间': 'datetime',
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
            '模': '%',
            '幂': '**',
            '%': '%',
            '^': '**',
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '大于等于': '>=',
            '小于等于': '<=',
            '且': 'and',
            '与': 'and',
            '或': 'or',
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

            # 标准输入输出
            '读取行': '_duan_builtin.读取行',
            '读取N字节': '_duan_builtin.读取N字节',
            '写入输出': '_duan_builtin.写入输出',
            '打印输出': '_duan_builtin.打印输出',
            '刷新输出': '_duan_builtin.刷新输出',
            '写入错误': '_duan_builtin.写入错误',
            '打印错误': '_duan_builtin.打印错误',

            # JSON 处理
            '解析JSON': '_duan_builtin.解析JSON',
            '序列化JSON': '_duan_builtin.序列化JSON',
            '美化JSON': '_duan_builtin.美化JSON',

            # 字符串工具
            '转整数': '_duan_builtin.转整数',
            '转浮点': '_duan_builtin.转浮点',
            '转字符串': '_duan_builtin.转字符串',
            '到字符串': '_duan_builtin.转字符串',
            '转换字符串': '_duan_builtin.转字符串',
            '到数字': '_duan_builtin.转浮点',
            '转数字': '_duan_builtin.转浮点',
            '字符串长度': '_duan_builtin.字符串长度',
            '字符串获取': '_duan_builtin.字符串获取',
            '字符串包含': '_duan_builtin.字符串包含',
            '字符串替换': '_duan_builtin.字符串替换',
            '字符串分割': '_duan_builtin.字符串分割',
            '分割字符串': '_duan_builtin.分割字符串',
            '连接字符串': '_duan_builtin.连接字符串',
            '替换字符串': '_duan_builtin.替换字符串',
            '去除空白': '_duan_builtin.去除空白',
            
            # 列表工具
            '列': '_duan_builtin.列',
            '列表长度': '_duan_builtin.列表长度',
            '列表获取': '_duan_builtin.列表获取',
            '列表追加': '_duan_builtin.列表追加',
            '列表弹出': '_duan_builtin.列表弹出',
            '列表排序': '_duan_builtin.列表排序',
            '列表反转': '_duan_builtin.列表反转',
            '列表包含': '_duan_builtin.列表包含',
            '列表创建': '_duan_builtin.列表创建',
            
            # 字典工具
            '字典': '_duan_builtin.字典创建',
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
            
            # 日期时间
            '时间戳': '_duan_builtin.时间戳',
            '格式化时间': '_duan_builtin.格式化时间',
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
        self._add_line("# 解析 stdlib 路径（依次尝试多种可能）")
        self._add_line("_duan_stdlib = None")
        self._add_line("try:")
        self._add_line("    _duan_file_dir = os.path.dirname(os.path.abspath(__file__))")
        self._add_line("except NameError:")
        self._add_line("    _duan_file_dir = None")
        self._add_line("for _try_path in [")
        self._add_line("    os.path.join(_duan_file_dir, 'stdlib') if _duan_file_dir else None,")
        self._add_line("    os.path.join(_duan_file_dir, '..', 'stdlib') if _duan_file_dir else None,")
        self._add_line("    os.path.join(os.getcwd(), 'stdlib'),")
        self._add_line("    os.path.normpath(os.path.join(_duan_file_dir, '..', '..', 'stdlib')) if _duan_file_dir else None,")
        self._add_line("]:")
        self._add_line("    if _try_path and os.path.isdir(_try_path):")
        self._add_line("        _duan_stdlib = _try_path")
        self._add_line("        break")
        self._add_line("")
        self._add_line("if _duan_stdlib and _duan_stdlib not in sys.path:")
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
        self._add_line("        _duan_builtin.读取行 = lambda: sys.stdin.readline().rstrip('\\r\\n')")
        self._add_line("        _duan_builtin.读取N字节 = lambda n: sys.stdin.read(n)")
        self._add_line("        _duan_builtin.写入输出 = lambda t: (sys.stdout.write(t), sys.stdout.flush()) and None")
        self._add_line("        _duan_builtin.打印输出 = lambda t: print(t, flush=True)")
        self._add_line("        _duan_builtin.刷新输出 = lambda: sys.stdout.flush()")
        self._add_line("        _duan_builtin.写入错误 = lambda t: (sys.stderr.write(t), sys.stderr.flush()) and None")
        self._add_line("        _duan_builtin.打印错误 = lambda t: print(t, file=sys.stderr, flush=True)")
        self._add_line("        _duan_builtin.解析JSON = lambda t: __import__('json').loads(t)")
        self._add_line("        _duan_builtin.序列化JSON = lambda v, i=None: (__import__('json').dumps(v, ensure_ascii=False, indent=i) if i is not None else __import__('json').dumps(v, ensure_ascii=False))")
        self._add_line("        _duan_builtin.美化JSON = lambda v: __import__('json').dumps(v, ensure_ascii=False, indent=2)")
        self._add_line("        _duan_builtin.转字符串 = str")
        self._add_line("        _duan_builtin.列表创建 = list")
        self._add_line("        _duan_builtin.列表长度 = len")
        self._add_line("        _duan_builtin.列 = lambda *args: list(args)")
        self._add_line("        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("        _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("        _duan_builtin.字符串长度 = len")
        self._add_line("        _duan_builtin.字典创建 = dict")
        self._add_line("        _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})")
        self._add_line("        _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)")
        self._add_line("        _duan_builtin.字典键列表 = lambda d: list(d.keys())")
        self._add_line("        _duan_builtin.字典包含键 = lambda d, k: k in d")
        self._add_line("        _duan_builtin.时间戳 = lambda: __import__('time').time()")
        self._add_line("        _duan_builtin.格式化时间 = lambda t, f='%Y-%m-%d %H:%M:%S': __import__('datetime').datetime.fromtimestamp(t).strftime(f) if isinstance(t, (int, float)) else __import__('datetime').datetime.strptime(t, '%Y-%m-%d %H:%M:%S').strftime(f)")
        self._add_line("else:")
        self._add_line("    import types")
        self._add_line("    _duan_builtin = types.ModuleType('_duan_builtin')")
        self._add_line("    _duan_builtin.打印 = print")
        self._add_line("    _duan_builtin.读取行 = lambda: sys.stdin.readline().rstrip('\\n')")
        self._add_line("    _duan_builtin.读取N字节 = lambda n: sys.stdin.read(n)")
        self._add_line("    _duan_builtin.写入输出 = lambda t: (sys.stdout.write(t), sys.stdout.flush()) and None")
        self._add_line("    _duan_builtin.打印输出 = lambda t: print(t, flush=True)")
        self._add_line("    _duan_builtin.刷新输出 = lambda: sys.stdout.flush()")
        self._add_line("    _duan_builtin.写入错误 = lambda t: (sys.stderr.write(t), sys.stderr.flush()) and None")
        self._add_line("    _duan_builtin.打印错误 = lambda t: print(t, file=sys.stderr, flush=True)")
        self._add_line("    _duan_builtin.解析JSON = lambda t: __import__('json').loads(t)")
        self._add_line("    _duan_builtin.序列化JSON = lambda v, i=None: (__import__('json').dumps(v, ensure_ascii=False, indent=i) if i is not None else __import__('json').dumps(v, ensure_ascii=False))")
        self._add_line("    _duan_builtin.美化JSON = lambda v: __import__('json').dumps(v, ensure_ascii=False, indent=2)")
        self._add_line("    _duan_builtin.转字符串 = str")
        self._add_line("    _duan_builtin.列表创建 = list")
        self._add_line("    _duan_builtin.列表长度 = len")
        self._add_line("    _duan_builtin.列 = lambda *args: list(args)")
        self._add_line("    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("    _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("    _duan_builtin.字符串长度 = len")
        self._add_line("    _duan_builtin.字典创建 = dict")
        self._add_line("    _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})")
        self._add_line("    _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)")
        self._add_line("    _duan_builtin.字典键列表 = lambda d: list(d.keys())")
        self._add_line("    _duan_builtin.字典包含键 = lambda d, k: k in d")
        self._add_line("    _duan_builtin.时间戳 = lambda: __import__('time').time()")
        self._add_line("    _duan_builtin.格式化时间 = lambda t, f='%Y-%m-%d %H:%M:%S': __import__('datetime').datetime.fromtimestamp(t).strftime(f) if isinstance(t, (int, float)) else __import__('datetime').datetime.strptime(t, '%Y-%m-%d %H:%M:%S').strftime(f)")
        self._add_line("")

        # 可空类型解包辅助函数：_duan_unwrap(x) = assert x is not None; return x
        self._add_line("# 可空类型解包辅助函数")
        self._add_line("def _duan_unwrap(_x):")
        self._add_line("    assert _x is not None, \"尝试解包空值\"")
        self._add_line("    return _x")
        self._add_line("")

        # 生成语句
        for stmt in module.statements:
            self._generate_statement(stmt)
        
        # 如果第一行没有 from abc import ABC, abstractmethod，在前面插入
        # 查找第一个非空且非注释行的位置，在后面插入
        if self._needs_abc:
            abc_import = "from abc import ABC, abstractmethod"
            # 插入在文件头之后，第一个语句之前
            # 找到最后一个空行或注释后的位置
            insert_pos = 0
            for i, line in enumerate(self.output_lines):
                if line.startswith("#") or line == "":
                    insert_pos = i + 1
                else:
                    break
            self.output_lines.insert(insert_pos, "")
            self.output_lines.insert(insert_pos, abc_import)
        
        return self._build_output()
    
    def _build_output(self) -> str:
        """构建最终输出字符串"""
        return '\n'.join(self.output_lines)
    
    def _get_indent(self, level: int) -> str:
        """获取指定层级的缩进字符串（带缓存）"""
        if level not in self._indent_cache:
            self._indent_cache[level] = self.indent_str * level
        return self._indent_cache[level]
    
    def _add_line(self, line: str):
        """添加一行代码"""
        if line:
            self.output_lines.append(self._get_indent(self.indent_level) + line)
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
        elif isinstance(stmt, ast_nodes_module.ImportStatement):
            # 支持 ast_nodes.py 的 ImportStatement
            self._generate_import_statement(stmt)
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
        elif isinstance(stmt, SelfAssignment):
            # self赋值语句
            self._generate_self_assignment(stmt)
        elif isinstance(stmt, CompoundAssignment):
            # 复合赋值语句：甲 加上 1 → 甲 += 1
            self._generate_compound_assignment(stmt)
        elif isinstance(stmt, IndexedAssignment):
            # 索引赋值语句：甲[丁] = 值
            self._generate_indexed_assignment(stmt)
        elif isinstance(stmt, ClassDefinition):
            # 类定义
            self._generate_class_definition(stmt)
        elif isinstance(stmt, MemberAccess):
            # 成员访问作为独立语句
            expr_code = self._generate_expr(stmt)
            self._add_line(expr_code)
        elif isinstance(stmt, MatchStmt):
            # 模式匹配语句
            self._generate_match_stmt(stmt)
        elif isinstance(stmt, DestructuringAssignment):
            # 解构赋值：a, b = value
            vars_str = ', '.join(self._sanitize_name(v) for v in stmt.variables)
            value = self._generate_expr(stmt.value)
            self._add_line(f"{vars_str} = {value}")
        elif isinstance(stmt, WithStmt):
            # 上下文管理器
            self._generate_with_stmt(stmt)
        elif isinstance(stmt, DecoratorDefinition):
            # 装饰器定义
            self._generate_decorator_definition(stmt)
        elif isinstance(stmt, InterfaceDefinition):
            # 接口定义
            self._generate_interface_definition(stmt)
        elif isinstance(stmt, Parameter):
            # 参数声明（段落体内部）
            param_name = self._sanitize_name(stmt.name)
            # 忽略参数声明，参数已由段落定义处理
            pass
        elif isinstance(stmt, ParameterList):
            # 参数列表声明（段落体内部）
            # 忽略参数列表，参数已由段落定义处理
            pass
        else:
            raise CodeGenError(f"未知语句类型", type(stmt).__name__)
    
    def _generate_var_decl(self, stmt: VarDecl):
        """生成变量声明"""
        name = self._sanitize_name(stmt.name)
        value = self._generate_expr(stmt.value)
        # 类方法中，如果变量是类属性，使用 self. 前缀
        if self._in_class_method and stmt.name in self._class_attr_names:
            self._add_line(f"self.{name} = {value}")
        else:
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
            if stmt.catch_type and stmt.catch_var:
                # 捕获指定类型 + 变量：except 值错误 as 错误:
                self._add_line(f"except {stmt.catch_type} as {stmt.catch_var}:")
            elif stmt.catch_type:
                # 捕获指定类型无变量：except 值错误:
                self._add_line(f"except {stmt.catch_type}:")
            elif stmt.catch_var:
                # 无类型有变量（向后兼容）：except Exception as 错误:
                self._add_line(f"except Exception as {stmt.catch_var}:")
            else:
                # 无类型无变量：except Exception:
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
        # 确保抛出的是合法异常对象（Python 3 不允许 raise 字符串）
        self._add_line(f"_duan_exc = {value}")
        self._add_line("raise _duan_exc if isinstance(_duan_exc, BaseException) else Exception(_duan_exc)")
    
    def _generate_self_assignment(self, stmt):
        """生成self赋值语句"""
        attr_name = self._sanitize_name(stmt.attr_name)
        value = self._generate_expr(stmt.value)
        self._add_line(f"self.{attr_name} = {value}")
    
    def _generate_compound_assignment(self, stmt):
        """生成复合赋值语句：甲 加上 1 → 甲 += 1"""
        target = self._sanitize_name(stmt.target)
        # 运算符映射
        py_ops = {
            '加': '+=',
            '减': '-=',
            '乘': '*=',
            '除': '/=',
            '模': '%=',
            '幂': '**=',
        }
        py_op = py_ops.get(stmt.operator, '+=')
        value = self._generate_expr(stmt.value)
        self._add_line(f"{target} {py_op} {value}")

    def _generate_indexed_assignment(self, stmt):
        """生成索引赋值语句：甲[丁] = 值"""
        target = self._sanitize_name(stmt.target)
        index = self._generate_expr(stmt.index)
        value = self._generate_expr(stmt.value)
        self._add_line(f"{target}[{index}] = {value}")

    def _generate_class_definition(self, stmt):
        """生成类定义"""
        class_name = self._sanitize_name(stmt.name)

        # 类定义行
        if stmt.base_classes:
            bases = ', '.join(self._sanitize_name(b) for b in stmt.base_classes)
            self._add_line(f"class {class_name}({bases}):")
        else:
            self._add_line(f"class {class_name}:")

        self.indent_level += 1

        # 分离静态属性和实例属性
        static_attrs = []
        instance_attrs = []
        if hasattr(stmt, 'attributes') and stmt.attributes:
            for attr in stmt.attributes:
                if getattr(attr, 'is_static', False):
                    static_attrs.append(attr)
                else:
                    instance_attrs.append(attr)

        # 收集类属性名（用于方法内自动添加 self. 前缀）
        self._class_attr_names = set()
        for attr in instance_attrs:
            self._class_attr_names.add(self._sanitize_name(attr.name))
        for attr in static_attrs:
            self._class_attr_names.add(self._sanitize_name(attr.name))

        # 收集类方法名
        self._class_method_names = set()
        if hasattr(stmt, 'methods') and stmt.methods:
            for method in stmt.methods:
                method_name = method.name if hasattr(method, 'name') else ''
                self._class_method_names.add(method_name)

        # 检查是否有用户定义的构造函数
        has_constructor = False
        ctor_method = None
        if hasattr(stmt, 'methods') and stmt.methods:
            for method in stmt.methods:
                method_name = method.name if hasattr(method, 'name') else ''
                is_ctor = getattr(method, 'is_constructor', False) or method_name in ('构造', '初始化')
                if is_ctor or method_name == '__init__':
                    has_constructor = True
                    ctor_method = method
                    break

        # 生成静态属性（类变量）
        for attr in static_attrs:
            attr_name = self._sanitize_name(attr.name)
            if attr.default_value:
                default = self._generate_expr(attr.default_value)
                self._add_line(f"{attr_name} = {default}")
            else:
                self._add_line(f"{attr_name} = None")

        # 如果没有用户构造函数但有实例属性，自动生成 __init__
        if instance_attrs and not has_constructor:
            self._add_line("def __init__(self):")
            self.indent_level += 1
            for attr in instance_attrs:
                attr_name = self._sanitize_name(attr.name)
                if attr.default_value:
                    default = self._generate_expr(attr.default_value)
                    self._add_line(f"self.{attr_name} = {default}")
                else:
                    self._add_line(f"self.{attr_name} = None")
            self.indent_level -= 1

        # 生成方法
        if hasattr(stmt, 'methods') and stmt.methods:
            for method in stmt.methods:
                method_name = method.name if hasattr(method, 'name') else ''
                is_ctor = getattr(method, 'is_constructor', False) or method_name in ('构造', '初始化')
                if is_ctor and instance_attrs:
                    self._generate_method(method, instance_attrs)
                else:
                    self._generate_method(method)

        # 如果类体为空，添加 pass
        if not static_attrs and not instance_attrs and not (hasattr(stmt, 'methods') and stmt.methods):
            self._add_line("pass")

        # 清理类属性追踪
        self._class_attr_names = set()
        self._class_method_names = set()

        self.indent_level -= 1
        self._add_line("")
    
    def _generate_interface_definition(self, stmt: InterfaceDefinition):
        """生成接口定义"""
        self._needs_abc = True
        class_name = self._sanitize_name(stmt.name)
        
        # 基类
        bases = ['ABC']
        for sup in stmt.super_interfaces:
            bases.append(self._sanitize_name(sup))
        bases_str = ', '.join(bases)
        
        self._add_line(f"class {class_name}({bases_str}):")
        self.indent_level += 1
        
        # 生成抽象方法
        for method in stmt.methods:
            self._generate_abstract_method(method)
        
        # 如果没有方法，添加 pass
        if not stmt.methods:
            self._add_line("pass")
        
        self.indent_level -= 1
        self._add_line("")
    
    def _generate_abstract_method(self, method: MethodSignature):
        """生成抽象方法"""
        self._needs_abc = True
        method_name = self._sanitize_name(method.name)
        
        # 参数列表
        params = ['self']
        for param in method.parameters:
            param_name = self._sanitize_name(param.name)
            params.append(param_name)
        
        params_str = ', '.join(params)
        
        self._add_line("@abstractmethod")
        if method.return_type:
            ret_type = self._sanitize_name(method.return_type)
            self._add_line(f"def {method_name}({params_str}) -> {ret_type}:")
        else:
            self._add_line(f"def {method_name}({params_str}):")
        self.indent_level += 1
        self._add_line("pass")
        self.indent_level -= 1
    
    def _generate_match_stmt(self, stmt: MatchStmt):
        """生成模式匹配语句
        
        转换为 Python 3.10+ 的 match/case 语句，
        如果不支持则降级为 if/elif/else 链
        """
        subject = self._generate_expr(stmt.subject)
        self._add_line(f"match {subject}:")
        
        self.indent_level += 1
        for case in stmt.cases:
            self._generate_match_case(case)
        self.indent_level -= 1
        self._add_line("")
    
    def _generate_match_case(self, case: MatchCase):
        """生成匹配分支"""
        pattern = self._generate_match_pattern(case.pattern)
        
        guard_str = ""
        if case.guard:
            guard_str = f" if {self._generate_expr(case.guard)}"
        
        self._add_line(f"case {pattern}{guard_str}:")
        
        self.indent_level += 1
        if case.body:
            for stmt in case.body:
                self._generate_statement(stmt)
        else:
            self._add_line("pass")
        self.indent_level -= 1
    
    def _generate_match_pattern(self, pattern: MatchPattern) -> str:
        """生成匹配模式"""
        if pattern.kind == 'wildcard':
            return '_'
        elif pattern.kind == 'number':
            return str(pattern.value)
        elif pattern.kind == 'string':
            escaped = pattern.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        elif pattern.kind == 'bool':
            return 'True' if pattern.value else 'False'
        elif pattern.kind == 'null':
            return 'None'
        elif pattern.kind == 'variable':
            return self._sanitize_name(pattern.binding)
        elif pattern.kind == 'list':
            elements = [self._generate_match_pattern(e) for e in pattern.elements]
            return f"[{', '.join(elements)}]"
        elif pattern.kind == 'type_check':
            type_name = self._sanitize_name(pattern.type_name)
            binding = self._sanitize_name(pattern.binding)
            return f"{type_name}() as {binding}"
        return '_'

    def _generate_with_stmt(self, stmt: WithStmt):
        """生成上下文管理语句"""
        context_expr = self._generate_expr(stmt.context_expr)
        if stmt.variable:
            var_name = self._sanitize_name(stmt.variable)
            self._add_line(f"with {context_expr} as {var_name}:")
        else:
            self._add_line(f"with {context_expr}:")
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1

    def _generate_decorator_definition(self, stmt: DecoratorDefinition):
        """生成装饰器定义"""
        decorator_name = stmt.decorator_name
        
        # 内置装饰器映射
        builtin_decorators = {
            '静态方法': '@staticmethod',
            '类方法': '@classmethod',
            '特性': '@property',
            '抽象': '@abstractmethod',
        }
        
        if decorator_name in builtin_decorators:
            self._add_line(builtin_decorators[decorator_name])
            # 抽象装饰器需要导入 ABC
            if decorator_name == '抽象':
                self._needs_abc = True
        else:
            # 自定义装饰器
            sanitized = self._sanitize_name(decorator_name)
            self._add_line(f"@{sanitized}")
        
        if isinstance(stmt.paragraph, Paragraph):
            self._generate_paragraph(stmt.paragraph)
        else:
            raise CodeGenError("装饰器后必须是段落定义", type(stmt.paragraph).__name__)

    def _generate_method(self, method, class_attributes=None):
        """生成方法定义"""
        method_name = method.name

        # 构造函数特殊处理
        if method.is_constructor or method_name == '构造':
            method_name = '__init__'

        # 静态方法不需要 self 参数
        is_static = getattr(method, 'is_static', False)
        if is_static:
            params = []
        else:
            params = ['self']

        # 访问修饰符：私有方法加 _ 前缀
        access = getattr(method, 'access_modifier', 'public')
        if access == 'private':
            method_name = f"_{method_name}"

        # 收集参数名（用于排除 self. 前缀）
        self._current_method_params = set()
        if hasattr(method, 'parameters') and method.parameters:
            for param in method.parameters:
                param_name = self._sanitize_name(param.name)
                self._current_method_params.add(param.name)
                params.append(param_name)

        params_str = ', '.join(params)

        # 方法定义（必须包含括号）
        if is_static:
            self._add_line(f"@staticmethod")
        self._add_line(f"def {method_name}({params_str}):")

        self.indent_level += 1

        # 设置类方法上下文，用于自动添加 self. 前缀
        self._in_class_method = not is_static

        # 如果是构造函数且有类属性，为未在构造函数体中初始化的属性生成默认值
        attr_init_lines = []
        if method_name == '__init__' and class_attributes:
            # 收集已在构造函数中初始化的属性名
            initialized_attrs = set()
            if hasattr(method, 'body') and method.body:
                for stmt in method.body:
                    if isinstance(stmt, tuple):
                        if stmt[0] == 'var':
                            initialized_attrs.add(self._sanitize_name(stmt[1]))
                    elif isinstance(stmt, VarDecl):
                        initialized_attrs.add(self._sanitize_name(stmt.name))
                    elif hasattr(stmt, 'target'):
                        # Assignment 或 SelfAssignment 节点
                        target = stmt.target
                        if isinstance(target, str):
                            initialized_attrs.add(self._sanitize_name(target))
                        elif hasattr(target, 'name'):
                            initialized_attrs.add(self._sanitize_name(target.name))
            # 只为有默认值且未在构造函数中初始化的属性生成初始化语句
            for attr in class_attributes:
                attr_name = self._sanitize_name(attr.name)
                if attr_name not in initialized_attrs and attr.default_value:
                    default = self._generate_expr(attr.default_value)
                    attr_init_lines.append(f"self.{attr_name} = {default}")

        # 先输出属性初始化语句，再生成方法体
        if attr_init_lines:
            for line in attr_init_lines:
                self._add_line(line)

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
        
        # 重置类方法上下文和参数追踪
        self._in_class_method = False
        self._current_method_params = set()
    
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
        
        # 解包表达式：值! 或 unwrap(值)
        # 翻译成 (lambda _x: (_duan_assert_not_none(_x), _x)[1])(inner_expr)
        if type(expr).__name__ == 'UnwrapExpression':
            inner = self._generate_expr(expr.value)
            return f"(_duan_unwrap({inner}))"
        
        if isinstance(expr, NumberLiteral):
            # 检查是否是中文数字
            if expr.value in self.chinese_numbers:
                return str(self.chinese_numbers[expr.value])
            return str(expr.value)
        
        elif isinstance(expr, StringLiteral):
            # 转义引号和不可见字符
            value = expr.value
            # 先处理反斜杠（必须是第一步）
            value = value.replace('\\', '\\\\')
            # 再处理不可见字符
            value = value.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t').replace('"', '\\"')
            return f'"{value}"'
        
        elif isinstance(expr, Identifier):
            name = self._sanitize_name(expr.name)
            # 检查是否是中文数字
            if expr.name in self.chinese_numbers:
                return str(self.chinese_numbers[expr.name])
            # 类方法中，如果引用的是类属性且不是参数名，添加 self. 前缀
            if self._in_class_method and expr.name in self._class_attr_names and expr.name not in self._current_method_params:
                return f"self.{name}"
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
                # 类方法中，如果调用的是同类其他方法，添加 self. 前缀
                if self._in_class_method and expr.name in self._class_method_names:
                    py_name = f"self.{name}"
            
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
            
            # 检查方法名是否需要映射转换
            mapped_member = self.method_name_map.get(expr.member, member)
            
            # 检查导入的模块成员访问映射
            # 如 JSON.序列化 → _duan_builtin.序列化JSON, JSON.解析 → _duan_builtin.解析JSON
            module_member_map = {
                'JSON.序列化': '_duan_builtin.序列化JSON',
                'JSON.解析': '_duan_builtin.解析JSON',
                'JSON.美化': '_duan_builtin.美化JSON',
            }
            full_access = f"{obj}.{member}"
            if full_access in module_member_map:
                mapped = module_member_map[full_access]
                if expr.is_method_call:
                    args = [self._generate_expr(arg) for arg in expr.args]
                    args_str = ', '.join(args)
                    return f"{mapped}({args_str})"
                else:
                    return mapped
            
            if expr.is_method_call:
                # 方法调用
                args = [self._generate_expr(arg) for arg in expr.args]
                args_str = ', '.join(args)

                # 特殊处理：父.构造(...) -> super().__init__(...)
                if obj == "super()" and expr.member == '构造':
                    return f"super().__init__({args_str})"
                # 特殊处理：长度方法 -> len(obj)
                if expr.member == '长度':
                    return f"len({obj})"
                # 特殊处理：包含方法 -> item in obj
                elif expr.member == '包含':
                    return f"{args_str} in {obj}"

                return f"{obj}.{mapped_member}({args_str})"
            else:
                # 属性访问
                return f"{obj}.{mapped_member}"
        
        elif isinstance(expr, ListLiteral):
            # 列表字面量
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"
        
        elif isinstance(expr, StringInterpolation):
            # 字符串插值 -> f-string
            parts = []
            for part in expr.parts:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, ASTNode):
                    # 生成表达式代码并放入花括号
                    expr_code = self._generate_expr(part)
                    parts.append('{' + expr_code + '}')
            # 转义已有的花括号
            fstr = ''.join(parts)
            # 确保字符串内的引号转义
            fstr = fstr.replace('\\', '\\\\')
            return f'f"{fstr}"'
        
        elif isinstance(expr, ListComprehension):
            # 列表推导 -> [expr for var in iterable if condition]
            expression = self._generate_expr(expr.expression)
            variable = self._sanitize_name(expr.variable)
            iterable = self._generate_expr(expr.iterable)
            result = f"[{expression} for {variable} in {iterable}"
            if expr.condition:
                condition = self._generate_expr(expr.condition)
                result += f" if {condition}"
            result += "]"
            return result
        
        elif isinstance(expr, LambdaExpression):
            # 匿名函数 -> lambda params: body
            params = ', '.join(self._sanitize_name(p) for p in expr.params)
            body = self._generate_expr(expr.body)
            return f"lambda {params}: {body}"
        
        elif isinstance(expr, DictComprehension):
            # 字典推导 -> {key: value for var in iterable if condition}
            key = self._generate_expr(expr.key_expr)
            val = self._generate_expr(expr.value_expr)
            var_name = self._sanitize_name(expr.variable)
            iterable = self._generate_expr(expr.iterable)
            result = f"{{{key}: {val} for {var_name} in {iterable}"
            if expr.condition:
                condition = self._generate_expr(expr.condition)
                result += f" if {condition}"
            result += "}"
            return result

        elif isinstance(expr, DictLiteral):
            # 字典字面量 -> {key: val, key2: val2, ...}
            items = [f"{self._generate_expr(k)}: {self._generate_expr(v)}" for k, v in expr.entries]
            return f"{{{', '.join(items)}}}"

        elif isinstance(expr, ConditionalExpression):
            # 三元条件表达式 -> 值1 if 条件 else 值2
            condition = self._generate_expr(expr.condition)
            then_expr = self._generate_expr(expr.then_expr)
            if expr.else_expr:
                else_expr = self._generate_expr(expr.else_expr)
                return f"({then_expr} if {condition} else {else_expr})"
            else:
                return f"({then_expr} if {condition} else None)"

        elif isinstance(expr, RangeExpr):
            # 范围表达式 -> range(start, end+1) 或 range(start, end+1, step)
            start = self._generate_expr(expr.start)
            end = self._generate_expr(expr.end)
            if expr.step:
                step = self._generate_expr(expr.step)
                return f"range({start}, ({end}) + 1, {step})"
            return f"range({start}, ({end}) + 1)"

        else:
            raise CodeGenError(f"不支持的表达式类型", type(expr).__name__)
    
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
        
        # 使用模块名映射转换中文模块名
        mapped_module = self.module_name_map.get(module_name, module_name)
        
        if stmt.symbols:
            # 从...导入：from 数学 import 平方根, 幂
            symbols_str = ', '.join(stmt.symbols)
            if stmt.alias:
                if mapped_module:
                    self._add_line(f"from {mapped_module} import {symbols_str} as {stmt.alias}")
                else:
                    self._add_line(f"import {symbols_str} as {stmt.alias}")
                self._imported_symbols.add(stmt.alias)
            else:
                if mapped_module:
                    self._add_line(f"from {mapped_module} import {symbols_str}")
                else:
                    self._add_line(f"import {symbols_str}")
                # 追踪导入的符号
                for symbol in stmt.symbols:
                    self._imported_symbols.add(symbol)
        else:
            # 导入整个模块：import 数学
            if stmt.alias:
                self._add_line(f"import {mapped_module} as {stmt.alias}")
                self._imported_symbols.add(stmt.alias)
            else:
                self._add_line(f"import {mapped_module}")
                self._imported_symbols.add(module_name)
    
    def _generate_import_statement(self, stmt):
        """生成 ast_nodes.py 的 ImportStatement"""
        module_name = stmt.module
        
        # 使用模块名映射转换中文模块名
        mapped_module = self.module_name_map.get(module_name, module_name)
        
        if stmt.names:
            # from module import names
            names_str = ', '.join(stmt.names)
            if mapped_module:
                self._add_line(f"from {mapped_module} import {names_str}")
            else:
                self._add_line(f"import {names_str}")
            for name in stmt.names:
                self._imported_symbols.add(name)
        else:
            # import module
            self._add_line(f"import {mapped_module}")
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
