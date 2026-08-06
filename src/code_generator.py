"""
段言（Duan）编程语言 - Python代码生成器

将段言AST转换为Python代码
"""

from typing import List, Optional, Dict
from duan_parser_v3 import *
import ast_nodes as ast_nodes_module


# 需要导入新的AST节点类型
from duan_parser_v3 import ImportStmt, ExportStmt, IndexAccess, SliceExpr, SetComprehension, TupleLiteral, BreakStmt, ContinueStmt, PassStmt, ClassInstantiation, MemberAccess, TryStmt, ThrowStmt, Parameter, ParameterList, StringInterpolation, ListComprehension, LambdaExpression, MatchStmt, MatchCase, MatchPattern, DictComprehension, DestructuringAssignment, WithStmt, DecoratorDefinition, DictLiteral, InterfaceDefinition, MethodSignature, IndexedAssignment, RangeExpr, FFILoadLibrary, FFIFunctionDecl, FFIStructDef, FFICallbackDef, FFICreateArray, FFISetArrayElement, FFIAllocMemory, FFIFreeMemory, FFISetPointerValue, FFISetErrno, FFITryCatch, FFIEnumDef, FFIUnionDef, FFICreateCallback, FFIVarArgsDecl, FFIStructByValue, FFILibraryPath, FFITypedefDef, FFIBitfieldDef, FFIFuncPtrDef, FFIDebugConfig, FFIPreprocessorDef, FFIPointerType, FFIArrayType, FFIAddressOf, FFIDereference, FFIPointerOffset, FFIGetLastError, FFIGetErrno
from ast_nodes_v3 import Assignment, TypeCheckToggleStmt, AwaitExpr, KeywordArg, IndexedCompoundAssignment, PassStmt, AssignmentExpression, SetLiteral, EmbedBlock, FunctionCallExpr
from ast_nodes import ExpressionStatement, SegmentName


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
        
        # 运行时类型检查开关（默认关闭，零开销）
        self._runtime_type_check = False
        
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
        # 用户自定义函数名追踪（避免内置函数映射覆盖用户定义）
        self._user_defined_functions: set = set()
        # 当前方法参数名追踪（避免将参数名误判为类属性）
        self._current_method_params: set = set()
        
        # 是否在函数/段落内部（控制 return 生成）
        self._in_function: bool = False
        
        # 是否在循环内部（控制 break/continue 生成）
        self._in_loop: bool = False
        
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
            '获取': 'get',
            '设置': '__setitem__',
            # 字符串方法
            '转大写': 'upper',
            '转小写': 'lower',
            '替换': 'replace',
            '截取': 'slice',
            '开头': 'startswith',
            '结尾': 'endswith',
            '去除空白': 'strip',
            '分割': 'split',
            '连接': 'join',
            '查找': 'find',
            '计数': 'count',
        }
        
        # 模块名映射（中文到Python模块）
        self.module_name_map = {
            'JSON': 'json',
            '日期时间': 'datetime',
        }
        
        # 异常名映射（中文→Python）
        self.exception_name_map = {
            '迭代停止': 'StopIteration',
            '值错误': 'ValueError',
            '类型错误': 'TypeError',
            '索引错误': 'IndexError',
            '键错误': 'KeyError',
            '属性错误': 'AttributeError',
            '导入错误': 'ImportError',
            '零除错误': 'ZeroDivisionError',
            '文件错误': 'FileNotFoundError',
            '运行时错误': 'RuntimeError',
            '溢出错误': 'OverflowError',
            '递归错误': 'RecursionError',
            '内存错误': 'MemoryError',
            '系统错误': 'SystemError',
            '断言错误': 'AssertionError',
            '停止迭代': 'StopIteration',
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
            '除以': '/',
            '整除': '//',  # 整数除法（对应Python的//）
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
            '不小于': '>=',   # P2-3：比较运算符短形式
            '不大于': '<=',   # P2-3：比较运算符短形式
            '且': 'and',
            '与': 'and',
            '或': 'or',
            '非': 'not',
        }
        
        # 内置函数映射
        self.builtin_map = {
            # 基础函数
            '打印': 'print',
            '显示': 'print',
            '输出': 'print',
            '断言': '_duan_assert',
            '读取': 'input',
            '长': 'len',
            '长度': 'len',
            '首': 'lambda x: x[0]',
            '末': 'lambda x: x[-1]',
            # 可空类型解包（等价于 值!）
            'unwrap': '_duan_unwrap',
            '解包': '_duan_unwrap',
            
            # 数学函数（P1-1：补全反向映射）
            '求和': 'sum',
            '求最大': 'max',
            '求最小': 'min',
            '最大值': 'max',
            '最小值': 'min',
            '绝对值': 'abs',
            '四舍五入': 'round',
            '次方': 'pow',
            '范围': 'range',
            '全部': 'all',
            '任意': 'any',
            '整数': 'int',
            '浮点数': 'float',
            '字符串': 'str',
            '列表': 'list',
            '字典': 'dict',
            '集合': 'set',
            '布尔': 'bool',
            '类型': 'type',
            '去重': 'lambda x: list(set(x))',
            
            # 文件I/O
            '读取文件': '_duan_builtin.读取文件',
            '_读文件': '_duan_builtin._读文件',
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

            # 函数式编程
            '筛选': 'filter',
            '映射': 'map',
            '归约': 'functools.reduce',
            '折叠': 'functools.reduce',
            '排序': 'sorted',
            '反转': 'reversed',
            '枚举': 'enumerate',
            '打包': 'zip',

            # 文件操作
            '打开文件': 'open',

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
            '包含': '_duan_builtin.包含',
            '字符串替换': '_duan_builtin.字符串替换',
            '字符串分割': '_duan_builtin.字符串分割',
            '分割字符串': '_duan_builtin.分割字符串',
            '连接字符串': '_duan_builtin.连接字符串',
            '替换字符串': '_duan_builtin.替换字符串',
            '去除空白': '_duan_builtin.去除空白',
            '转大写': '_duan_builtin.转大写',
            '转小写': '_duan_builtin.转小写',
            '截取': '_duan_builtin.截取',
            '子串': '_duan_builtin.截取',
            '字符串截取': '_duan_builtin.截取',
            '开头': '_duan_builtin.开头',
            '结尾': '_duan_builtin.结尾',
            '查找子串': '_duan_builtin.查找子串',
            '替换字符串次数': '_duan_builtin.替换字符串次数',
            '截取到末尾': '_duan_builtin.截取到末尾',
            '字符串计数': '_duan_builtin.字符串计数',
            '字符串重复': '_duan_builtin.字符串重复',
            '字符串反转': '_duan_builtin.字符串反转',
            '转标题': '_duan_builtin.转标题',
            '去除左侧空白': '_duan_builtin.去除左侧空白',
            '去除右侧空白': '_duan_builtin.去除右侧空白',
            '字符串对齐居中': '_duan_builtin.字符串对齐居中',
            '字符串对齐左': '_duan_builtin.字符串对齐左',
            '字符串对齐右': '_duan_builtin.字符串对齐右',
            
            # 列表工具
            '列': '_duan_builtin.列',
            '列表长度': '_duan_builtin.列表长度',
            '列表获取': '_duan_builtin.列表获取',
            '列表追加': '_duan_builtin.列表追加',
            '列表弹出': '_duan_builtin.列表弹出',
            '列表插入': '_duan_builtin.列表插入',
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

            # 随机数
            '随机整数': '_duan_builtin.随机整数',
            '随机浮点': '_duan_builtin.随机浮点',
            '随机选择': '_duan_builtin.随机选择',

            # C FFI 指针/数组/错误处理
            '取地址': '_duan_ffi.取地址',
            '解引用': '_duan_ffi.解引用',
            '指针偏移': '_duan_ffi.指针偏移',
            'FFI错误': '_duan_ffi.获取FFI错误',
            '系统错误码': '_duan_ffi.获取系统错误码',
            '设系统错误码': '_duan_ffi.设系统错误码',
            '创建数组': '_duan_ffi.创建数组',
            '设置数组': '_duan_ffi.设置数组',
            '分配内存': '_duan_ffi.分配内存',
            '释放内存': '_duan_ffi.释放内存',
            '设指针值': '_duan_ffi.设指针值',
            # C FFI 第三阶段
            '创建回调': '_duan_ffi.创建回调函数',
            '创建结构体值': '_duan_ffi.创建结构体值',
            '创建枚举': '_duan_ffi.创建枚举',
            '创建联合体': '_duan_ffi.创建联合体',
            '解析库路径': '_duan_ffi.解析库路径',
            '变长参数调用': '_duan_ffi.变长参数调用',
            '获取平台': '_duan_ffi.获取平台',
            '查找库': '_duan_ffi.查找库',
            '结构体大小': '_duan_ffi.结构体大小',
            '字段偏移': '_duan_ffi.字段偏移',
            '结构体转字节': '_duan_ffi.结构体转字节',
            '字节转结构体': '_duan_ffi.字节转结构体',
            # C FFI 第四阶段
            '注册回调': '_duan_ffi.注册回调',
            '注销回调': '_duan_ffi.注销回调',
            '获取回调': '_duan_ffi.获取回调',
            'FFI调试': '_duan_ffi.启用调试',
            'FFI禁用调试': '_duan_ffi.禁用调试',
            'FFI获取日志': '_duan_ffi.获取日志',
            '位域设置': '_duan_ffi.位域设置',
            '位域获取': '_duan_ffi.位域获取',
            '创建函数指针': '_duan_ffi.创建函数指针',
            '创建类型别名': '_duan_ffi.创建类型别名',
            '定义宏': '_duan_ffi.定义宏',
            '获取宏': '_duan_ffi.获取宏',
        }
    
    def generate(self, module: Module) -> str:
        """生成Python代码"""
        self.output_lines = []
        self.indent_level = 0  # 重置缩进级别，防止跨条目状态污染
        self._user_defined_functions = set()  # 重置用户自定义函数追踪
        self._ffi_user_types = {}  # 重置 FFI 用户自定义类型注册表
        
        # 添加文件头
        self._add_line("# 由段言编译器生成")
        self._add_line("# 源文件: 段言代码")
        self._add_line("")
        
        # 添加标准库导入
        self._add_line("import sys")
        self._add_line("import os")
        self._add_line("import ctypes")
        self._add_line("from typing import Any, Optional")
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
        self._add_line("if _duan_stdlib:")
        self._add_line("    _duan_parent = os.path.dirname(_duan_stdlib)")
        self._add_line("    if _duan_parent not in sys.path:")
        self._add_line("        sys.path.insert(0, _duan_parent)")
        self._add_line("")
        self._add_line("import stdlib.FFI as _duan_ffi")
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
        self._add_line("        _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read() if __import__('os').path.isfile(path) else ''")
        self._add_line("        _duan_builtin._读文件 = lambda path: open(path, 'r', encoding='utf-8').read() if __import__('os').path.isfile(path) else ''")
        self._add_line("        _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None")
        self._add_line("        _duan_builtin.删除文件 = lambda path: __import__('os').remove(path) if __import__('os').path.isfile(path) else None")
        self._add_line("        _duan_builtin.删除目录 = lambda path: __import__('os').rmdir(path)")
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
        self._add_line("        _duan_builtin.转整数 = int")
        self._add_line("        _duan_builtin.转浮点 = float")
        self._add_line("        _duan_builtin.chr = chr")
        self._add_line("        _duan_builtin.bin = bin")
        self._add_line("        _duan_builtin.hex = hex")
        self._add_line("        _duan_builtin.oct = oct")
        self._add_line("        _duan_builtin.列表创建 = list")
        self._add_line("        _duan_builtin.列表长度 = len")
        self._add_line("        _duan_builtin.列 = lambda *args: list(args)")
        self._add_line("        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("        _duan_builtin.列表获取 = lambda lst, i: lst[i]")
        self._add_line("        _duan_builtin.列表弹出 = lambda lst, i=-1: lst.pop(i)")
        self._add_line("        _duan_builtin.列表插入 = lambda lst, i, v: lst.insert(i, v)")
        self._add_line("        _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("        _duan_builtin.包含 = lambda sub, s: sub in s")
        self._add_line("        _duan_builtin.字符串长度 = len")
        self._add_line("        _duan_builtin.截取 = lambda s, start, end: s[start:end]")
        self._add_line("        _duan_builtin.转大写 = lambda s: s.upper()")
        self._add_line("        _duan_builtin.转小写 = lambda s: s.lower()")
        self._add_line("        _duan_builtin.结尾 = lambda s, suffix: s.endswith(suffix)")
        self._add_line("        _duan_builtin.开头 = lambda s, prefix: s.startswith(prefix)")
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
        self._add_line("    _duan_builtin.转整数 = int")
        self._add_line("    _duan_builtin.转浮点 = float")
        self._add_line("    _duan_builtin.chr = chr")
        self._add_line("    _duan_builtin.bin = bin")
        self._add_line("    _duan_builtin.hex = hex")
        self._add_line("    _duan_builtin.oct = oct")
        self._add_line("    _duan_builtin.列表创建 = list")
        self._add_line("    _duan_builtin.列表长度 = len")
        self._add_line("    _duan_builtin.列 = lambda *args: list(args)")
        self._add_line("    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)")
        self._add_line("    _duan_builtin.列表获取 = lambda lst, i: lst[i]")
        self._add_line("    _duan_builtin.列表弹出 = lambda lst, i=-1: lst.pop(i)")
        self._add_line("    _duan_builtin.列表插入 = lambda lst, i, v: lst.insert(i, v)")
        self._add_line("    _duan_builtin.列表包含 = lambda lst, item: item in lst")
        self._add_line("    _duan_builtin.包含 = lambda sub, s: sub in s")
        self._add_line("    _duan_builtin.字符串长度 = len")
        self._add_line("    _duan_builtin.截取 = lambda s, start, end: s[start:end]")
        self._add_line("    _duan_builtin.转大写 = lambda s: s.upper()")
        self._add_line("    _duan_builtin.转小写 = lambda s: s.lower()")
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
        self._add_line("# 断言辅助函数")
        self._add_line("def _duan_assert(_cond, _msg=''):")
        self._add_line("    if not _cond:")
        self._add_line("        raise AssertionError(_msg)")
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
            if self._in_loop:
                self._add_line("break")
            else:
                self._add_line("pass")
        elif isinstance(stmt, ContinueStmt):
            if self._in_loop:
                self._add_line("continue")
            else:
                self._add_line("pass")
        elif isinstance(stmt, PassStmt):
            self._add_line("pass")
        elif isinstance(stmt, TypeCheckToggleStmt):
            # 类型检查开关
            self._runtime_type_check = stmt.enable
            action = "开启" if stmt.enable else "关闭"
            if stmt.enable:
                # 生成运行时类型检查辅助函数（仅一次）
                if not hasattr(self, '_type_check_helper_added'):
                    self._add_line("# 运行时类型检查已开启")
                    self._add_line("def _duan_check_type(value, expected_type, var_name=''):")
                    self.indent_level += 1
                    self._add_line("actual_type = type(value).__name__")
                    self._add_line("type_map = {'int': '整数', 'float': '小数', 'str': '文本', 'bool': '布尔', 'list': '列表', 'dict': '字典', 'set': '集合', 'type(None)': '空'}")
                    self._add_line("actual_cn = type_map.get(actual_type, actual_type)")
                    self._add_line("if expected_type and actual_cn != expected_type and expected_type != '任意':")
                    self.indent_level += 1
                    self._add_line("raise TypeError(f'类型错误: 变量 {var_name} 期望类型 {expected_type}, 实际类型 {actual_cn}')")
                    self.indent_level -= 1
                    self._add_line("return value")
                    self.indent_level -= 1
                    self._type_check_helper_added = True
                else:
                    self._add_line(f"# {action}类型检查")
            else:
                self._add_line(f"# {action}类型检查")
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
        elif isinstance(stmt, IndexedCompoundAssignment):
            # 索引复合赋值：甲[丁] 加上 1 → 甲[丁] += 1
            self._generate_indexed_compound_assignment(stmt)
        elif isinstance(stmt, Assignment):
            # 普通赋值语句：甲 = 值
            target = self._generate_expr(stmt.target)
            value = self._generate_expr(stmt.value)
            self._add_line(f"{target} = {value}")
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
            # 顶层参数声明是解析FFI时产生的多余语句，跳过
            pass
        elif isinstance(stmt, ParameterList):
            # 参数列表声明（段落体内部）
            # 顶层参数列表声明是解析FFI时产生的多余语句，跳过
            pass
        elif isinstance(stmt, FFILoadLibrary):
            self._generate_ffi_load_library(stmt)
        elif isinstance(stmt, FFIFunctionDecl):
            self._generate_ffi_function_decl(stmt)
        elif isinstance(stmt, FFIStructDef):
            self._generate_ffi_struct_def(stmt)
        elif isinstance(stmt, FFICallbackDef):
            self._generate_ffi_callback_def(stmt)
        elif isinstance(stmt, FFICreateArray):
            self._generate_ffi_create_array(stmt)
        elif isinstance(stmt, FFISetArrayElement):
            self._generate_ffi_set_array_element(stmt)
        elif isinstance(stmt, FFIAllocMemory):
            self._generate_ffi_alloc_memory(stmt)
        elif isinstance(stmt, FFIFreeMemory):
            self._generate_ffi_free_memory(stmt)
        elif isinstance(stmt, FFISetPointerValue):
            self._generate_ffi_set_pointer_value(stmt)
        elif isinstance(stmt, FFISetErrno):
            self._generate_ffi_set_errno(stmt)
        elif isinstance(stmt, FFITryCatch):
            self._generate_ffi_try_catch(stmt)
        elif isinstance(stmt, FFIEnumDef):
            self._generate_ffi_enum_def(stmt)
        elif isinstance(stmt, FFIUnionDef):
            self._generate_ffi_union_def(stmt)
        elif isinstance(stmt, FFIVarArgsDecl):
            self._generate_ffi_varargs_decl(stmt)
        elif isinstance(stmt, FFICreateCallback):
            self._generate_ffi_create_callback(stmt)
        elif isinstance(stmt, FFIStructByValue):
            self._generate_ffi_struct_by_value(stmt)
        elif isinstance(stmt, FFILibraryPath):
            self._generate_ffi_library_path(stmt)
        elif isinstance(stmt, FFITypedefDef):
            self._generate_ffi_typedef_def(stmt)
        elif isinstance(stmt, FFIBitfieldDef):
            self._generate_ffi_bitfield_def(stmt)
        elif isinstance(stmt, FFIFuncPtrDef):
            self._generate_ffi_funcptr_def(stmt)
        elif isinstance(stmt, FFIDebugConfig):
            self._generate_ffi_debug_config(stmt)
        elif isinstance(stmt, FFIPreprocessorDef):
            self._generate_ffi_preprocessor_def(stmt)
        elif isinstance(stmt, AwaitExpr):
            # 等待语句 → await expression
            inner = self._generate_expr(stmt.expression)
            self._add_line(f"await {inner}")
        elif type(stmt).__name__ == 'CForStmt':
            # C风格for循环
            self._generate_c_for_stmt(stmt)
        elif type(stmt).__name__ == 'Block':
            # 花括号代码块
            for s in stmt.statements:
                self._generate_statement(s)
        elif isinstance(stmt, ExpressionStatement):
            # 表达式语句包装（如 "打印 xxx。" 解析为 ExpressionStatement）
            expr_str = self._generate_expr(stmt.expression)
            self._add_line(expr_str)
        elif isinstance(stmt, (IndexAccess, MemberAccess, ParagraphCall)):
            # 表达式语句（如 obj[key].append(v) 或 obj.method()）
            expr_str = self._generate_expr(stmt)
            self._add_line(expr_str)
        elif isinstance(stmt, EmbedBlock):
            self._generate_embed_block(stmt)
        elif isinstance(stmt, StringLiteral):
            # 裸字符串语句（docstring）生成：配合 lexer/parser 的三引号 docstring 修复
            # （lexer.py _tokenize_string、parser_stmt.py _parse_statement），
            # 这里输出 Python 字符串表达式语句——
            # Python 会把函数/类/模块体首行的字符串视为 docstring，
            # 其余位置的裸字符串为无操作表达式（与 Python 语义一致）。
            # 修复前该节点没有语句级分支，会抛 CodeGenError「未知语句类型」。
            self._add_line(self._generate_expr(stmt))
        else:
            raise CodeGenError(f"未知语句类型", type(stmt).__name__)
    
    def _generate_var_decl(self, stmt: VarDecl):
        """生成变量声明"""
        name = self._sanitize_name(stmt.name)
        value = self._generate_expr(stmt.value)
        
        # 处理 己.xxx 形式的属性赋值
        if name.startswith('己.'):
            name = 'self.' + name[2:]
        
        type_annotation = ''
        if stmt.type_annotation:
            python_type = self._map_type(stmt.type_annotation)
            type_annotation = f': {python_type}'
        
        # 类方法中，如果变量是类属性，使用 self. 前缀
        if self._in_class_method and stmt.name in self._class_attr_names:
            self._add_line(f"self.{name}{type_annotation} = {value}")
        else:
            self._add_line(f"{name}{type_annotation} = {value}")
        
        # 运行时类型检查（仅在开启时生成）
        if self._runtime_type_check and stmt.type_annotation:
            duan_type = stmt.type_annotation
            if self._in_class_method and stmt.name in self._class_attr_names:
                self._add_line(f"_duan_check_type(self.{name}, '{duan_type}', '{stmt.name}')")
            else:
                self._add_line(f"_duan_check_type({name}, '{duan_type}', '{stmt.name}')")
    
    def _map_type(self, duan_type: str) -> str:
        """将段言类型名映射为Python类型名（支持泛型尖括号/方括号）"""
        type_map = {
            '整数': 'int',
            '小数': 'float',
            '浮数': 'float',
            '文本': 'str',
            '串': 'str',
            '布尔': 'bool',
            '列表': 'list',
            '列': 'list',
            '字典': 'dict',
            '典': 'dict',
            '集合': 'set',
            '集': 'set',
            '任意': 'Any',
            '空': 'None',
            '数': 'float',
        }
        stripped = (duan_type or '').strip()
        # 泛型形式：列表<整数> / 字典<字符串, 小数> / 可选<整数> / 列表[整数]
        if stripped.endswith('>') or stripped.endswith(']'):
            open_char = '<' if stripped.endswith('>') else '['
            bracket = stripped.find(open_char)
            if bracket > 0:
                base = stripped[:bracket].strip()
                args_str = stripped[bracket + 1:-1].strip()
                if base in ('列表', '列', 'List'):
                    if args_str:
                        # 嵌套泛型递归映射：列表<列表<整数>> → list[list[int]]
                        first_arg = args_str.split(',')[0].strip()
                        return f"list[{self._map_type(first_arg)}]"
                    return 'list'
                if base in ('字典', '典', 'Map'):
                    return 'dict'
                if base in ('集合', '集', 'Set'):
                    return 'set'
                if base in ('元组', 'Tuple'):
                    return 'tuple'
                if base in ('可选', '可空', 'Optional'):
                    inner = self._map_type(args_str) if args_str else 'Any'
                    return f"Optional[{inner}]"
                # 未知泛型基名：退化为基名本身
                return type_map.get(base, base)
        return type_map.get(stripped, stripped)
    
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
            # 处理否则如果链（else_body 是 IfStmt）
            if isinstance(stmt.else_body, IfStmt):
                self._generate_elif(stmt.else_body)
            elif isinstance(stmt.else_body, list):
                self._add_line("else:")
                self.indent_level += 1
                for s in stmt.else_body:
                    self._generate_statement(s)
                self.indent_level -= 1
    
    def _generate_elif(self, stmt: IfStmt):
        """生成否则如果（elif）分支"""
        condition = self._generate_expr(stmt.condition)
        self._add_line(f"elif {condition}:")
        
        self.indent_level += 1
        if stmt.then_body:
            for s in stmt.then_body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        
        if stmt.else_body:
            # 进一步嵌套的否则如果链
            if isinstance(stmt.else_body, IfStmt):
                self._generate_elif(stmt.else_body)
            elif isinstance(stmt.else_body, list):
                self._add_line("else:")
                self.indent_level += 1
                for s in stmt.else_body:
                    self._generate_statement(s)
                self.indent_level -= 1
    
    def _generate_foreach_stmt(self, stmt: ForeachStmt):
        """生成遍历循环"""
        var_name = self._sanitize_name(stmt.variable)
        iterable = self._generate_expr(stmt.iterable)
        
        for_keyword = "async for" if getattr(stmt, 'is_async', False) else "for"
        self._add_line(f"{for_keyword} {var_name} in {iterable}:")
        
        old_in_loop = self._in_loop
        self._in_loop = True
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        self._in_loop = old_in_loop
    
    def _generate_while_stmt(self, stmt: WhileStmt):
        """生成当循环"""
        condition = self._generate_expr(stmt.condition)
        
        self._add_line(f"while {condition}:")
        
        old_in_loop = self._in_loop
        self._in_loop = True
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        self._in_loop = old_in_loop
    
    def _generate_c_for_stmt(self, stmt):
        """生成C风格for循环：init; while(cond){ body; incr; }"""
        # 生成初始化语句
        if stmt.init:
            self._generate_statement(stmt.init)
        # 生成while循环
        condition = self._generate_expr(stmt.condition) if stmt.condition else 'True'
        self._add_line(f"while {condition}:")
        old_in_loop = self._in_loop
        self._in_loop = True
        self.indent_level += 1
        if stmt.body:
            for s in stmt.body:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        # 生成增量语句
        if stmt.increment:
            self._generate_statement(stmt.increment)
        self.indent_level -= 1
        self._in_loop = old_in_loop
        self._add_line("")

    def _generate_paragraph(self, stmt: Paragraph):
        """生成段落定义"""
        name = self._sanitize_name(stmt.name)
        
        # 从段落体中提取参数声明
        params = []
        body_without_params = []
        for s in (stmt.body or []):
            if isinstance(s, Parameter):
                params.append({'name': self._sanitize_name(s.name), 'type': s.type_annotation})
            elif isinstance(s, ParameterList):
                for param_name in s.params:
                    params.append({'name': self._sanitize_name(param_name), 'type': None})
            else:
                body_without_params.append(s)
        
        # 如果段落头有参数定义，也加入
        for param in (stmt.params or []):
            param_name = self._sanitize_name(param['name'])
            param_type = param.get('type')
            existing = next((p for p in params if p['name'] == param_name), None)
            if existing:
                if param_type:
                    existing['type'] = param_type
            else:
                params.append({'name': param_name, 'type': param_type})
        
        # 生成带类型注解的参数列表
        params_parts = []
        for p in params:
            if p['type']:
                python_type = self._map_type(p['type'])
                params_parts.append(f"{p['name']}: {python_type}")
            else:
                params_parts.append(p['name'])
        
        params_str = ', '.join(params_parts) if params_parts else ''
        
        # 生成返回类型注解
        return_type_annotation = ''
        if stmt.return_type:
            python_return_type = self._map_type(stmt.return_type)
            return_type_annotation = f" -> {python_return_type}"
        
        # 函数定义
        def_prefix = "async def" if '异步' in (stmt.modifiers or []) else "def"
        self._add_line(f"{def_prefix} {name}({params_str}){return_type_annotation}:")
        
        # 记录用户自定义函数名，避免内置函数映射覆盖
        self._user_defined_functions.add(stmt.name)
        
        old_in_function = self._in_function
        self._in_function = True
        self.indent_level += 1
        if body_without_params:
            for s in body_without_params:
                self._generate_statement(s)
        else:
            self._add_line("pass")
        self.indent_level -= 1
        self._in_function = old_in_function
        
        self._add_line("")
    
    def _generate_return_stmt(self, stmt: ReturnStmt):
        """生成返回语句

        模块级 return 在 Python 中非法，仅在函数/段落内部生成 return。
        否则将返回值作为裸表达式输出（用于 REPL 或模块级执行）。
        """
        if self._in_function:
            if stmt.value:
                value = self._generate_expr(stmt.value)
                self._add_line(f"return {value}")
            else:
                self._add_line("return")
        else:
            # 模块级：将返回值作为表达式输出，不生成 return
            if stmt.value:
                value = self._generate_expr(stmt.value)
                self._add_line(f"print({value})")
            else:
                self._add_line("pass")
    
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
            if stmt.catch_type == '外部错误':
                # FFI 外部错误处理
                if stmt.catch_var:
                    self._add_line(f"except (ctypes.ArgumentError, OSError, RuntimeError) as {stmt.catch_var}:")
                else:
                    self._add_line("except (ctypes.ArgumentError, OSError, RuntimeError):")
            elif stmt.catch_type and stmt.catch_var:
                # 捕获指定类型 + 变量：except 值错误 as 错误:
                # 支持多类型捕获：(Type1, Type2) 格式
                ct = stmt.catch_type
                if ',' in ct:
                    ct = f"({ct})"
                self._add_line(f"except {ct} as {stmt.catch_var}:")
            elif stmt.catch_type:
                # 捕获指定类型无变量：except 值错误:
                ct = stmt.catch_type
                if ',' in ct:
                    ct = f"({ct})"
                self._add_line(f"except {ct}:")
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
        else:
            # 有尝试块但没有捕获块：生成默认except块
            self._add_line("except Exception:")
            self.indent_level += 1
            self._add_line("pass")
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
        if stmt.value is None:
            # 裸抛出：重新抛出当前异常
            self._add_line("raise")
            return
        # 检查是否抛出已知中文异常名（如 迭代停止 → StopIteration）
        if isinstance(stmt.value, Identifier) and stmt.value.name in self.exception_name_map:
            py_exc_name = self.exception_name_map[stmt.value.name]
            from_part = ""
            if stmt.from_expr:
                from_val = self._generate_expr(stmt.from_expr)
                from_part = f" from {from_val}"
            self._add_line(f"raise {py_exc_name}(){from_part}")
            return
        value = self._generate_expr(stmt.value)
        # 确保抛出的是合法异常对象（Python 3 不允许 raise 字符串）
        from_part = ""
        if stmt.from_expr:
            from_val = self._generate_expr(stmt.from_expr)
            from_part = f" from {from_val}"
        self._add_line(f"_duan_exc = {value}")
        self._add_line(f"raise _duan_exc if isinstance(_duan_exc, BaseException) else Exception(_duan_exc){from_part}")
    
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
            '除以': '/=',
            '整除': '//=',  # 整数除法复合赋值
            '模': '%=',
            '幂': '**=',
        }
        py_op = py_ops.get(stmt.operator, '+=')
        value = self._generate_expr(stmt.value)
        self._add_line(f"{target} {py_op} {value}")

    def _generate_indexed_compound_assignment(self, stmt):
        """生成索引复合赋值语句：甲[丁] 加上 1 → 甲[丁] += 1"""
        target = self._sanitize_name(stmt.target)
        index = self._generate_expr(stmt.index)
        py_ops = {
            '加': '+=',
            '减': '-=',
            '乘': '*=',
            '除': '/=',
            '除以': '/=',
            '整除': '//=',  # 整数除法复合赋值
            '模': '%=',
            '幂': '**=',
        }
        py_op = py_ops.get(stmt.operator, '+=')
        value = self._generate_expr(stmt.value)
        self._add_line(f"{target}[{index}] {py_op} {value}")

    def _generate_indexed_assignment(self, stmt):
        """生成索引赋值语句：甲[丁] = 值 或 甲[i][j] = 值"""
        if isinstance(stmt.target, ASTNode):
            target = self._generate_expr(stmt.target)
        else:
            target = self._sanitize_name(stmt.target)
        value = self._generate_expr(stmt.value)
        # 多重索引时 index=None，target 已经是 IndexAccess 节点
        if stmt.index is not None:
            index = self._generate_expr(stmt.index)
            self._add_line(f"{target}[{index}] = {value}")
        else:
            self._add_line(f"{target} = {value}")

    def _generate_class_definition(self, stmt):
        """生成类定义"""
        class_name = self._sanitize_name(stmt.name)

        # 检查是否有抽象方法
        has_abstract = False
        if hasattr(stmt, 'methods') and stmt.methods:
            for method in stmt.methods:
                if getattr(method, 'is_abstract', False):
                    has_abstract = True
                    break

        # 类定义行（包含父类和实现的接口）
        all_bases = list(stmt.base_classes) + list(getattr(stmt, 'interfaces', []) or [])
        if has_abstract:
            self._needs_abc = True
            if 'ABC' not in all_bases:
                all_bases.insert(0, 'ABC')
        if all_bases:
            bases = ', '.join(self._sanitize_name(b) for b in all_bases)
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
    
    _TYPE_NAME_MAP = {
        '整数': 'int', '整数型': 'int', '整型': 'int',
        '小数': 'float', '浮数': 'float', '浮点数': 'float', '浮点': 'float',
        '文本': 'str', '串': 'str', '字符串': 'str',
        '列表': 'list', '列': 'list', '数组': 'list',
        '字典': 'dict', '典': 'dict', '词典': 'dict', '映射': 'dict',
        '集合': 'set', '集': 'set',
        '布尔': 'bool', '布尔值': 'bool',
        '空': 'None', '空值': 'None',
        '任意': 'object', '任意类型': 'object',
    }

    def _sanitize_type_name(self, name: str) -> str:
        """将段言类型名转换为Python类型名"""
        return self._TYPE_NAME_MAP.get(name, self._sanitize_name(name))

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
            type_name = self._sanitize_type_name(pattern.type_name)
            binding = self._sanitize_name(pattern.binding)
            return f"{type_name}() as {binding}"
        return '_'

    def _generate_with_stmt(self, stmt: WithStmt):
        """生成上下文管理语句"""
        context_expr = self._generate_expr(stmt.context_expr)
        # 在 with 语句中，读取文件(...) 应替换为 open(...)
        context_expr = context_expr.replace('_duan_builtin.读取文件', 'open').replace('读取文件', 'open')
        # 写入文件(...) 也应替换为 open(..., 'w')
        context_expr = context_expr.replace('_duan_builtin.写入文件', 'open').replace('写入文件', 'open')
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
            # 自定义装饰器（支持带参数：@decorator(args)）
            # 使用 getattr 兼容旧 AST（ast_nodes.DecoratorDefinition 无 args 字段）
            sanitized = self._sanitize_name(decorator_name)
            decorator_args = getattr(stmt, 'args', None)
            if decorator_args:
                args_parts = []
                for a in decorator_args:
                    if isinstance(a, KeywordArg):
                        args_parts.append(f"{a.name}={self._generate_expr(a.value)}")
                    else:
                        args_parts.append(self._generate_expr(a))
                args_str = ', '.join(args_parts)
                self._add_line(f"@{sanitized}({args_str})")
            else:
                self._add_line(f"@{sanitized}")
        
        if isinstance(stmt.paragraph, Paragraph):
            self._generate_paragraph(stmt.paragraph)
        else:
            raise CodeGenError("装饰器后必须是段落定义", type(stmt.paragraph).__name__)

    def _generate_method(self, method, class_attributes=None):
        """生成方法定义"""
        method_name = method.name

        # 构造函数特殊处理
        is_ctor = getattr(method, 'is_constructor', False) or method_name == '构造'
        if is_ctor:
            method_name = '__init__'

        # 迭代器协议方法名映射
        if method_name == '__迭代__':
            method_name = '__iter__'
        elif method_name == '__下一项__':
            method_name = '__next__'
        # 上下文管理器协议方法名映射
        elif method_name == '__进入__':
            method_name = '__enter__'
        elif method_name == '__退出__':
            method_name = '__exit__'

        # 静态方法不需要 self 参数
        is_static = getattr(method, 'is_static', False)
        is_classmethod = getattr(method, 'is_classmethod', False)
        is_abstract = getattr(method, 'is_abstract', False)
        if is_static or is_abstract:
            # 抽象方法可以有 self 也可以没有，但测试用例中的抽象方法通常无参数
            params = [] if is_static else ['self']
        else:
            params = ['self']

        # 访问修饰符：私有方法加 _ 前缀
        access = getattr(method, 'access_modifier', 'public')
        if access == 'private':
            method_name = f"_{method_name}"

        # 收集参数名（用于排除 self. 前缀）
        self._current_method_params = set()
        # 兼容 MethodDefinition(.parameters) 和 Paragraph(.params)
        method_params = getattr(method, 'parameters', None)
        if method_params is None:
            method_params = getattr(method, 'params', None)
        if method_params:
            for param in method_params:
                # Paragraph 的 params 是 List[Dict[str,str]]，MethodDefinition 的是 List[Parameter]
                if isinstance(param, dict):
                    param_name = self._sanitize_name(param.get('name', ''))
                    self._current_method_params.add(param.get('name', ''))
                    if param.get('default'):
                        params.append(f"{param_name}={param['default']}")
                    else:
                        params.append(param_name)
                else:
                    param_name = self._sanitize_name(param.name)
                    self._current_method_params.add(param.name)
                    if getattr(param, 'default_value', None):
                        default = self._generate_expr(param.default_value)
                        params.append(f"{param_name}={default}")
                    else:
                        params.append(param_name)

        params_str = ', '.join(params)

        # 方法定义（必须包含括号）
        if is_abstract:
            self._needs_abc = True
            self._add_line("@abstractmethod")
        if is_static:
            self._add_line(f"@staticmethod")
        if is_classmethod:
            self._add_line(f"@classmethod")
        if getattr(method, 'is_property', False):
            self._add_line("@property")
        self._add_line(f"def {method_name}({params_str}):")

        old_in_function = self._in_function
        old_in_class = self._in_class_method
        self._in_function = True
        self._in_class_method = not is_static
        self.indent_level += 1

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
        
        # 重置上下文
        self._in_function = old_in_function
        self._in_class_method = old_in_class
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
            value = value.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t').replace('"', '\\"').replace('\0', '\\0').replace('\x00', '\\0')
            return f'"{value}"'
        
        elif isinstance(expr, Identifier):
            name = self._sanitize_name(expr.name)
            # 检查是否是中文数字
            if expr.name in self.chinese_numbers:
                return str(self.chinese_numbers[expr.name])
            # 己 → self，己.attr → self.attr
            if name == '己':
                return 'self'
            if name.startswith('己.'):
                return 'self.' + name[2:]
            # 类方法中，如果引用的是类属性且不是参数名，添加 self. 前缀
            if self._in_class_method and expr.name in self._class_attr_names and expr.name not in self._current_method_params:
                return f"self.{name}"
            return name
        
        # 检查 ast_nodes 模块中的 Identifier（兼容两种定义）
        elif hasattr(expr, 'name') and hasattr(expr, 'line'):
            # 可能是来自 ast_nodes 的 Identifier
            name_val = expr.name
            if isinstance(name_val, str):
                return self._sanitize_name(name_val)
            elif hasattr(name_val, 'name'):
                # SegmentName 嵌套：name 字段本身可能是 SegmentName 对象
                # 尝试递归提取字符串
                inner = name_val
                while hasattr(inner, 'name') and not isinstance(inner.name, str):
                    inner = inner.name
                if hasattr(inner, 'name'):
                    return self._sanitize_name(inner.name)
                return self._sanitize_name(str(inner))
            return self._sanitize_name(str(name_val))
        
        elif isinstance(expr, SegmentName):
            # SegmentName 段落名
            name_val = expr.name
            if isinstance(name_val, str):
                return self._sanitize_name(name_val)
            # 递归提取
            while hasattr(name_val, 'name') and not isinstance(name_val.name, str):
                name_val = name_val.name
            if hasattr(name_val, 'name'):
                return self._sanitize_name(name_val.name)
            return self._sanitize_name(str(name_val))
        
        elif isinstance(expr, BinaryOp):
            left = self._generate_expr(expr.left)
            right = self._generate_expr(expr.right)
            op = self.operator_map.get(expr.operator, expr.operator)
            return f"({left} {op} {right})"
        
        elif isinstance(expr, UnaryOp):
            operand = self._generate_expr(expr.operand)
            op = self.operator_map.get(expr.operator, expr.operator)
            # 一元运算符不留空格：(-5) 而非 (- 5)
            return f"({op}{operand})"
        
        elif isinstance(expr, ParagraphCall):
            name = self._sanitize_name(expr.name)
            
            # 检查是否是内置函数（但不覆盖用户自定义的函数）
            if expr.name in self.builtin_map and expr.name not in self._user_defined_functions:
                py_name = self.builtin_map[expr.name]
            else:
                py_name = name
                # 类方法中，如果调用的是同类其他方法，添加 self. 前缀
                if self._in_class_method and expr.name in self._class_method_names:
                    py_name = f"self.{name}"
            
            # 参数（支持关键字参数）
            args = []
            for arg in expr.args:
                if isinstance(arg, KeywordArg):
                    args.append(f"{arg.name}={self._generate_expr(arg.value)}")
                else:
                    args.append(self._generate_expr(arg))
            args_str = ', '.join(args)
            
            return f"{py_name}({args_str})"
        
        elif isinstance(expr, FunctionCallExpr):
            # 链式函数调用：expr()  → callee(args)
            callee = self._generate_expr(expr.callee)
            args = []
            for arg in expr.args:
                if isinstance(arg, KeywordArg):
                    args.append(f"{arg.name}={self._generate_expr(arg.value)}")
                else:
                    args.append(self._generate_expr(arg))
            args_str = ', '.join(args)
            return f"{callee}({args_str})"
        
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
            # 索引访问：obj[index] 或 obj[start:stop:step]（切片）
            obj = self._generate_expr(expr.obj)
            if isinstance(expr.index, SliceExpr):
                start = self._generate_expr(expr.index.start) if expr.index.start else ''
                stop = self._generate_expr(expr.index.stop) if expr.index.stop else ''
                step = self._generate_expr(expr.index.step) if expr.index.step else ''
                if step:
                    return f"{obj}[{start}:{stop}:{step}]"
                else:
                    return f"{obj}[{start}:{stop}]"
            else:
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
                    args = []
                    for arg in expr.args:
                        if isinstance(arg, KeywordArg):
                            args.append(f"{arg.name}={self._generate_expr(arg.value)}")
                        else:
                            args.append(self._generate_expr(arg))
                    args_str = ', '.join(args)
                    return f"{mapped}({args_str})"
                else:
                    return mapped
            
            if expr.is_method_call:
                # 方法调用（支持关键字参数）
                args = []
                for arg in expr.args:
                    if isinstance(arg, KeywordArg):
                        args.append(f"{arg.name}={self._generate_expr(arg.value)}")
                    else:
                        args.append(self._generate_expr(arg))
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

                # P5 核心改造：内置函数式优先
                # 如果方法名在 builtin_map 中且映射到 _duan_builtin，转为函数式调用
                # 这样 obj.方法(args) 自动转为 _duan_builtin.方法(obj, args)
                # 外部库方法（不在 builtin_map 中）则原样透传 obj.method(args)
                builtin_target = self.builtin_map.get(expr.member)
                if builtin_target and builtin_target.startswith('_duan_builtin.'):
                    # 内置函数：转为函数式调用
                    func_name = builtin_target.split('.', 1)[1]
                    # 若 obj 本身已是内置命名空间（_duan_builtin.方法(...)，如
                    # test_turing.duan 的 _duan_builtin.字典设置(...)），方法名已可
                    # 直接调用，不能再把 _duan_builtin 注入为第一个参数，
                    # 否则会多出一个参数（lambda 形参不匹配，TypeError）。
                    if obj == '_duan_builtin':
                        return f"{builtin_target}({args_str})"
                    if args_str:
                        return f"{builtin_target}({obj}, {args_str})"
                    else:
                        return f"{builtin_target}({obj})"

                return f"{obj}.{mapped_member}({args_str})"
            else:
                # 属性访问
                return f"{obj}.{mapped_member}"
        
        elif isinstance(expr, ListLiteral):
            # 列表字面量
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"
        
        elif isinstance(expr, TupleLiteral):
            # 元组字面量
            elements = [self._generate_expr(e) for e in expr.elements]
            if len(elements) == 1:
                return f"({elements[0]},)"
            return f"({', '.join(elements)})"
        
        elif isinstance(expr, SetLiteral):
            # 集合字面量
            if not expr.elements:
                return "set()"
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"{{{', '.join(elements)}}}"
        
        elif isinstance(expr, StringInterpolation):
            # 字符串插值 -> f-string
            parts = []
            expr_parts = []  # 表达式部分（花括号内代码），用于选择外层引号
            for part in expr.parts:
                if isinstance(part, str):
                    # 转义特殊字符（反斜杠、换行、回车、制表符）
                    escaped = part.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                    parts.append(escaped)
                elif isinstance(part, tuple):
                    # 带格式说明符的表达式：(expr_node, format_spec)
                    expr_code = self._generate_expr(part[0])
                    parts.append('{' + expr_code + ':' + part[1] + '}')
                    expr_parts.append(expr_code)
                elif isinstance(part, ASTNode):
                    # 生成表达式代码并放入花括号
                    expr_code = self._generate_expr(part)
                    parts.append('{' + expr_code + '}')
                    expr_parts.append(expr_code)

            # 选择外层引号并只在【字面量部分】转义，避免破坏花括号内表达式。
            #
            # Bug 根因：原实现先拼接整个 f-string，再用 fstr.replace('"', '\\"')
            # 全局转义双引号。若花括号内表达式含字符串（如 {处理数据("hello")}），
            # 表达式里的 " 会被转成 \" —— 在 f-string 花括号内属于无效语法
            # （"unexpected character after line continuation character"）。
            #
            # 修复方案：
            # 1) 表达式部分由 _generate_expr 生成（字符串统一用双引号），
            #    因此只要表达式含 "，外层引号就必须选单引号 '（花括号内出现 " 合法）；
            # 2) 外层引号只出现在字面量部分，若字面量含同种引号则仅在该处转义
            #    （花括号外的 \' 或 \" 是合法转义）。
            if any('"' in p for p in expr_parts):
                outer = "'"
            elif any("'" in p for p in parts if isinstance(p, str)):
                outer = '"'
            else:
                outer = '"'
            # 仅转义字面量部分中的外层引号
            out = []
            for p in parts:
                if isinstance(p, str) and outer in p:
                    out.append(p.replace(outer, '\\' + outer))
                else:
                    out.append(p)
            return f"f{outer}{''.join(out)}{outer}"
        
        elif isinstance(expr, ListComprehension):
            # 列表推导 -> [expr for var in iterable if condition ...]
            expression = self._generate_expr(expr.expression)
            if expr.generators and len(expr.generators) > 1:
                # 多重generator
                parts = []
                for var, it, cond in expr.generators:
                    var_name = self._sanitize_name(var)
                    it_str = self._generate_expr(it)
                    part = f"for {var_name} in {it_str}"
                    if cond:
                        cond_str = self._generate_expr(cond)
                        part += f" if {cond_str}"
                    parts.append(part)
                return f"[{expression} {' '.join(parts)}]"
            else:
                variable = self._sanitize_name(expr.variable)
                iterable = self._generate_expr(expr.iterable)
                result = f"[{expression} for {variable} in {iterable}"
                if expr.condition:
                    condition = self._generate_expr(expr.condition)
                    result += f" if {condition}"
                result += "]"
                return result
        
        elif isinstance(expr, SetComprehension):
            # 集合推导 -> {expr for var in iterable if condition ...}
            expression = self._generate_expr(expr.expression)
            if expr.generators and len(expr.generators) > 1:
                # 多重generator
                parts = []
                for var, it, cond in expr.generators:
                    var_name = self._sanitize_name(var)
                    it_str = self._generate_expr(it)
                    part = f"for {var_name} in {it_str}"
                    if cond:
                        cond_str = self._generate_expr(cond)
                        part += f" if {cond_str}"
                    parts.append(part)
                return f"{{{expression} {' '.join(parts)}}}"
            else:
                variable = self._sanitize_name(expr.variable)
                iterable = self._generate_expr(expr.iterable)
                result = f"{{{expression} for {variable} in {iterable}"
                if expr.condition:
                    condition = self._generate_expr(expr.condition)
                    result += f" if {condition}"
                result += "}"
                return result
        
        elif isinstance(expr, LambdaExpression):
            # 匿名函数 -> lambda params: body
            params = ', '.join(self._sanitize_name(p) for p in expr.params)
            body = self._generate_expr(expr.body)
            return f"lambda {params}: {body}"
        
        elif isinstance(expr, DictComprehension):
            # 字典推导 -> {key: value for var in iterable if condition ...}
            key = self._generate_expr(expr.key_expr)
            val = self._generate_expr(expr.value_expr)
            if expr.generators and len(expr.generators) > 1:
                # 多重generator
                parts = []
                for var, it, cond in expr.generators:
                    var_name = self._sanitize_name(var)
                    it_str = self._generate_expr(it)
                    part = f"for {var_name} in {it_str}"
                    if cond:
                        cond_str = self._generate_expr(cond)
                        part += f" if {cond_str}"
                    parts.append(part)
                return f"{{{key}: {val} {' '.join(parts)}}}"
            else:
                var_name = self._sanitize_name(expr.variable)
                iterable = self._generate_expr(expr.iterable)
                result = f"{{{key}: {val} for {var_name} in {iterable}"
                if expr.condition:
                    condition = self._generate_expr(expr.condition)
                    result += f" if {condition}"
                result += "}"
                return result

        elif isinstance(expr, DictLiteral):
            # 字典字面量 -> {key: val, key2: val2, ...} 或 {**d1, key: val}
            items = []
            for k, v in expr.entries:
                if k is None:
                    # **展开
                    items.append(f"**{self._generate_expr(v)}")
                else:
                    items.append(f"{self._generate_expr(k)}: {self._generate_expr(v)}")
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

        elif isinstance(expr, AssignmentExpression):
            # 赋值表达式（海象运算符） -> (name := value)
            name = self._sanitize_name(expr.name)
            value = self._generate_expr(expr.value)
            return f"({name} := {value})"

        elif isinstance(expr, RangeExpr):
            # 范围表达式 -> range(start, end+1) 或 range(start, end+1, step)
            # 处理递减范围：当 start>end 时，自动将步长取反
            start = self._generate_expr(expr.start)
            end = self._generate_expr(expr.end)
            if expr.step:
                step = self._generate_expr(expr.step)
                # 运行时判断方向：start<=end 时正常步长，否则步长取反
                return f"range({start}, ({end}) + (1 if ({start}) <= ({end}) else -1), ({step}) if ({start}) <= ({end}) else -({step}))"
            else:
                return f"range({start}, ({end}) + 1)"

        elif isinstance(expr, AwaitExpr):
            # 等待表达式 → await expression
            inner = self._generate_expr(expr.expression)
            return f"await {inner}"
        
        # FFI 表达式节点
        elif isinstance(expr, FFIPointerType):
            return self._generate_ffi_pointer_type(expr)
        elif isinstance(expr, FFIArrayType):
            return self._generate_ffi_array_type(expr)
        elif isinstance(expr, FFIAddressOf):
            return self._generate_ffi_address_of(expr)
        elif isinstance(expr, FFIDereference):
            return self._generate_ffi_dereference(expr)
        elif isinstance(expr, FFIPointerOffset):
            return self._generate_ffi_pointer_offset(expr)
        elif isinstance(expr, FFIGetLastError):
            return self._generate_ffi_get_last_error(expr)
        elif isinstance(expr, FFIGetErrno):
            return self._generate_ffi_get_errno(expr)
        
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
        """生成导入语句
        
        支持三种语言前缀：
        - None: 段言标准库（中文模块名映射到 stdlib 路径）
        - 'python': Python 第三方库（直接 import 原名）
        - 'c': C 语言库（通过 ctypes/FFI 加载）
        """
        module_name = stmt.module_name
        
        # Python 第三方库导入：直接 import 原名
        if getattr(stmt, 'language', None) == 'python':
            if stmt.symbols:
                symbols_str = ', '.join(stmt.symbols)
                if stmt.alias:
                    self._add_line(f"from {module_name} import {symbols_str} as {stmt.alias}")
                    self._imported_symbols.add(stmt.alias)
                else:
                    self._add_line(f"from {module_name} import {symbols_str}")
                    for symbol in stmt.symbols:
                        self._imported_symbols.add(symbol)
            else:
                if stmt.alias:
                    self._add_line(f"import {module_name} as {stmt.alias}")
                    self._imported_symbols.add(stmt.alias)
                else:
                    self._add_line(f"import {module_name}")
                    self._imported_symbols.add(module_name)
            # 处理多模块导入
            if hasattr(stmt, 'extra_modules') and stmt.extra_modules:
                for extra_mod, extra_alias in stmt.extra_modules:
                    if extra_alias:
                        self._add_line(f"import {extra_mod} as {extra_alias}")
                        self._imported_symbols.add(extra_alias)
                    else:
                        self._add_line(f"import {extra_mod}")
                        self._imported_symbols.add(extra_mod)
            return
        
        # C 语言库导入：通过 ctypes 加载共享库
        if getattr(stmt, 'language', None) == 'c':
            if stmt.symbols:
                # from 模块导入符号 → 声明 ctypes 函数
                symbols_str = ', '.join(stmt.symbols)
                self._add_line(f"# 导入 C 库 {module_name} 的符号: {symbols_str}")
                # 尝试通过 ctypes 加载
                self._add_line(f"try:")
                self._add_line(f"    _c_lib_{module_name} = ctypes.CDLL('{module_name}')")
                self._add_line(f"except:")
                self._add_line(f"    _c_lib_{module_name} = None")
                for symbol in stmt.symbols:
                    if stmt.alias:
                        self._add_line(f"{stmt.alias}_{symbol} = getattr(_c_lib_{module_name}, '{symbol}', None) if _c_lib_{module_name} else None")
                        self._imported_symbols.add(f"{stmt.alias}_{symbol}")
                    else:
                        self._add_line(f"_c_{module_name}_{symbol} = getattr(_c_lib_{module_name}, '{symbol}', None) if _c_lib_{module_name} else None")
                        self._imported_symbols.add(symbol)
            else:
                self._add_line(f"# 导入 C 库: {module_name}")
                self._add_line(f"try:")
                self._add_line(f"    _c_lib_{module_name} = ctypes.CDLL('{module_name}')")
                self._add_line(f"except:")
                self._add_line(f"    _c_lib_{module_name} = None")
                if stmt.alias:
                    self._add_line(f"{stmt.alias} = _c_lib_{module_name}")
                    self._imported_symbols.add(stmt.alias)
                else:
                    self._imported_symbols.add(module_name)
            return
        
        # 段言标准库导入：使用模块名映射转换中文模块名
        # 1. 先查 duanpub 加载器（支持 "标准文件系统" / "文件系统" 等导入名）
        mapped_module = self._resolve_duanpub_import(module_name)
        # 2. 如果 duanpub 没有命中，回退到内置模块名映射
        if mapped_module is None:
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
        
        # 处理多模块导入（extra_modules）
        if hasattr(stmt, 'extra_modules') and stmt.extra_modules:
            for extra_mod, extra_alias in stmt.extra_modules:
                mapped_extra = self.module_name_map.get(extra_mod, extra_mod)
                if extra_alias:
                    self._add_line(f"import {mapped_extra} as {extra_alias}")
                    self._imported_symbols.add(extra_alias)
                else:
                    self._add_line(f"import {mapped_extra}")
                    self._imported_symbols.add(extra_mod)
    
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
    
    def _resolve_duanpub_import(self, module_name: str):
        """
        通过 duanpub 加载器解析导入名，返回 Python 模块名。
        
        解析顺序：
        1. duanpub P0 包 → get_stdlib_bridge() 返回 Python 模块名
        2. duanpub P1 包 → 返回 "stdlib.duanpub.<包名>"（桥接模块路径）
        3. 未命中 → 返回 None（回退到 module_name_map）
        """
        try:
            import sys
            import os
            # 确保 stdlib 目录在 path 中
            stdlib_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stdlib')
            if stdlib_dir not in sys.path:
                sys.path.insert(0, stdlib_dir)
            from duanpub import resolve_import, get_stdlib_bridge
            
            pkg_info = resolve_import(module_name)
            if pkg_info is None:
                return None
            
            priority = pkg_info.get('priority', 'P2')
            
            # P0: 已有 stdlib 实现，桥接到 Python 模块
            if priority == 'P0':
                # 去掉"标准"前缀后查找桥接
                real_name = module_name[2:] if module_name.startswith('标准') else module_name
                bridge = get_stdlib_bridge(real_name)
                if bridge:
                    return bridge
                # 没有桥接映射时，用真实包名作为 Python 模块名
                return real_name
            
            # P1: 有 Python 桥接模块
            if priority == 'P1':
                # 去掉"标准"前缀后得到真实包名
                real_name = module_name[2:] if module_name.startswith('标准') else module_name
                return 'stdlib.duanpub.' + real_name
        except Exception:
            pass
        return None

    
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

    # =========================================================================
    # C FFI 代码生成方法
    # =========================================================================

    # FFI 基本类型映射：段言类型 → ctypes 类型表达式
    _ffi_type_map = {
        '整数': 'ctypes.c_int',
        '小数': 'ctypes.c_double',
        '浮数': 'ctypes.c_double',
        '文本': 'ctypes.c_char_p',
        '串': 'ctypes.c_char_p',
        '布尔': 'ctypes.c_bool',
        '空': 'ctypes.c_void_p',
        '数': 'ctypes.c_double',
        '无': 'None',
    }

    # 用户自定义 FFI 类型名 → 生成的 Python 类型表达式
    # 在 _generate_ffi_struct_def / _union_def / _funcptr_def / _typedef_def 中注册
    _ffi_user_types: Dict[str, str] = {}

    def _get_ffi_type(self, type_name: str) -> str:
        """解析 FFI 类型名 → ctypes 类型表达式。
        优先查找基本类型映射，再查找用户自定义类型。
        """
        if type_name in self._ffi_type_map:
            return self._ffi_type_map[type_name]
        if type_name in self._ffi_user_types:
            return self._ffi_user_types[type_name]
        # 未知类型：回退到 void*
        return 'ctypes.c_void_p'

    def _generate_ffi_load_library(self, stmt: FFILoadLibrary):
        """生成加载动态库代码"""
        path = stmt.library_path
        alias = self._sanitize_name(stmt.alias)
        self._add_line(f"# 加载动态库: {path}")
        self._add_line(f"{alias} = ctypes.CDLL({repr(path)})")

    def _generate_ffi_function_decl(self, stmt: FFIFunctionDecl):
        """生成外部函数声明"""
        name = self._sanitize_name(stmt.name)
        library_alias = self._sanitize_name(stmt.library_alias)
        c_name = stmt.c_name or stmt.name

        # 确定参数类型和返回类型
        arg_types = []
        for p in stmt.params:
            duan_type = p.get('type', '整数')
            ctype = self._get_ffi_type(duan_type)
            arg_types.append(ctype)

        restype = 'None'
        if stmt.return_type:
            restype = self._get_ffi_type(stmt.return_type)

        # 生成 ctypes 函数绑定
        self._add_line(f"# 外部函数声明: {c_name}({', '.join(p['name'] for p in stmt.params)})")
        if library_alias:
            self._add_line(f"_{name}_ffi = {library_alias}.{c_name}")
            if arg_types:
                arg_types_str = ', '.join(arg_types)
                self._add_line(f"_{name}_ffi.argtypes = [{arg_types_str}]")
            self._add_line(f"_{name}_ffi.restype = {restype}")

        # 生成包装函数，处理类型转换
        params_str = ', '.join(self._sanitize_name(p['name']) for p in stmt.params)
        param_names = [self._sanitize_name(p['name']) for p in stmt.params]

        self._add_line(f"def {name}({params_str}):")
        self.indent_level += 1
        # 类型转换：文本类型需要 encode
        for i, p in enumerate(stmt.params):
            pname = self._sanitize_name(p['name'])
            ptype = p.get('type', '')
            if ptype in ('文本', '串'):
                self._add_line(f"{pname}_c = {pname}.encode('utf-8') if isinstance({pname}, str) else {pname}")
        # 调用 FFI 函数
        args_pass = []
        for i, p in enumerate(stmt.params):
            pname = self._sanitize_name(p['name'])
            ptype = p.get('type', '')
            if ptype in ('文本', '串'):
                args_pass.append(f"{pname}_c")
            else:
                args_pass.append(pname)
        args_str = ', '.join(args_pass)
        self._add_line(f"_result = _{name}_ffi({args_str})")
        # 返回类型转换：c_char_p 需要 decode
        if stmt.return_type in ('文本', '串'):
            self._add_line(f"return _result.decode('utf-8') if _result else ''")
        else:
            self._add_line("return _result")
        self.indent_level -= 1
        self._add_line("")

    def _generate_ffi_struct_def(self, stmt: FFIStructDef):
        """生成外部结构体定义"""
        name = self._sanitize_name(stmt.name)
        fields_code = []
        for f in stmt.fields:
            fname = self._sanitize_name(f['name'])
            ftype = self._get_ffi_type(f['type'])
            fields_code.append(f"('{fname}', {ftype})")
        fields_str = ', '.join(fields_code)
        self._add_line(f"# 外部结构体: {name}")
        self._add_line(f"class {name}(ctypes.Structure):")
        self.indent_level += 1
        self._add_line(f"_fields_ = [{fields_str}]")
        self.indent_level -= 1
        self._add_line("")
        # 注册到用户自定义类型表，供后续使用（如作为函数参数/返回类型、嵌套结构体字段）
        self._ffi_user_types[stmt.name] = name
        # 也注册到运行时类型注册表，供 获取类型() 在运行时查找
        self._add_line(f"_duan_ffi.注册类型('{stmt.name}', {name})")

    def _generate_ffi_callback_def(self, stmt: FFICallbackDef):
        """生成外部回调类型定义"""
        name = self._sanitize_name(stmt.name)
        arg_types = []
        for p in stmt.params:
            duan_type = p.get('type', '整数')
            ctype = self._get_ffi_type(duan_type)
            arg_types.append(ctype)
        restype = 'None'
        if stmt.return_type:
            restype = self._get_ffi_type(stmt.return_type)
        arg_types_str = ', '.join(arg_types)
        self._add_line(f"# 外部回调类型: {name}")
        self._add_line(f"{name} = ctypes.CFUNCTYPE({restype}, {arg_types_str})")
        self._add_line("")
        # 注册回调类型，供函数声明等使用
        self._ffi_user_types[stmt.name] = name
        self._add_line(f"_duan_ffi.注册类型('{stmt.name}', {name})")

    def _generate_ffi_create_array(self, stmt: FFICreateArray):
        """生成创建数组代码"""
        base_type = stmt.base_type
        ctype = self._get_ffi_type(base_type)
        size = self._generate_expr(stmt.size)
        name = self._sanitize_name(stmt.base_type)
        self._add_line(f"# 创建数组: {base_type}[{size}]")
        self._add_line(f"_ffi_arr_{name} = ({ctype} * {size})()")
        self._add_line("")

    def _generate_ffi_set_array_element(self, stmt: FFISetArrayElement):
        """生成设置数组元素代码"""
        arr = self._sanitize_name(stmt.array)
        idx = self._generate_expr(stmt.index)
        val = self._generate_expr(stmt.value)
        self._add_line(f"{arr}[{idx}] = {val}")

    def _generate_ffi_alloc_memory(self, stmt: FFIAllocMemory):
        """生成分配内存代码"""
        size = self._generate_expr(stmt.size)
        self._add_line(f"# 分配内存: {size} 字节")
        self._add_line(f"_ffi_mem = ctypes.create_string_buffer({size})")

    def _generate_ffi_free_memory(self, stmt: FFIFreeMemory):
        """生成释放内存代码"""
        ptr = self._sanitize_name(stmt.pointer)
        self._add_line(f"# 释放内存: {ptr}")
        self._add_line(f"del {ptr}")

    def _generate_ffi_set_pointer_value(self, stmt: FFISetPointerValue):
        """生成设指针值代码"""
        ptr = self._sanitize_name(stmt.pointer)
        val = self._generate_expr(stmt.value)
        self._add_line(f"{ptr}[0] = {val}")

    def _generate_ffi_set_errno(self, stmt: FFISetErrno):
        """生成设系统错误码代码"""
        val = self._generate_expr(stmt.value)
        self._add_line(f"ctypes.set_errno({val})")

    def _generate_ffi_try_catch(self, stmt: FFITryCatch):
        """生成FFI错误捕获代码"""
        self._add_line("try:")
        self.indent_level += 1
        for s in stmt.try_body:
            self._generate_statement(s)
        self.indent_level -= 1
        if stmt.catch_body:
            self._add_line(f"except (ctypes.ArgumentError, OSError, RuntimeError) as {stmt.error_var}:")
            self.indent_level += 1
            for s in stmt.catch_body:
                self._generate_statement(s)
            self.indent_level -= 1

    def _generate_ffi_enum_def(self, stmt: FFIEnumDef):
        """生成C枚举定义代码"""
        name = self._sanitize_name(stmt.name)
        self._add_line(f"# C枚举: {name}")
        self._add_line(f"class {name}:")
        self.indent_level += 1
        for member_name, member_val in stmt.values.items():
            self._add_line(f"{self._sanitize_name(member_name)} = {member_val}")
        self.indent_level -= 1
        self._add_line("")

    def _generate_ffi_union_def(self, stmt: FFIUnionDef):
        """生成C联合体定义代码"""
        name = self._sanitize_name(stmt.name)
        fields_code = []
        for f in stmt.fields:
            fname = self._sanitize_name(f['name'])
            ftype = self._get_ffi_type(f['type'])
            fields_code.append(f"('{fname}', {ftype})")
        fields_str = ', '.join(fields_code)
        self._add_line(f"# C联合体: {name}")
        self._add_line(f"class {name}(ctypes.Union):")
        self.indent_level += 1
        self._add_line(f"_fields_ = [{fields_str}]")
        self.indent_level -= 1
        self._add_line("")
        # 注册联合体类型
        self._ffi_user_types[stmt.name] = name
        self._add_line(f"_duan_ffi.注册类型('{stmt.name}', {name})")

    def _generate_ffi_varargs_decl(self, stmt: FFIVarArgsDecl):
        """生成变长参数函数声明代码"""
        name = self._sanitize_name(stmt.name)
        library_alias = self._sanitize_name(stmt.library_alias)
        c_name = stmt.c_name or stmt.name
        
        arg_types = []
        for p in stmt.params:
            duan_type = p.get('type', '整数')
            ctype = self._get_ffi_type(duan_type)
            arg_types.append(ctype)
        
        restype = 'None'
        if stmt.return_type:
            restype = self._get_ffi_type(stmt.return_type)
        
        self._add_line(f"# 变长参数函数声明: {c_name}")
        self._add_line(f"_{name}_ffi = {library_alias}.{c_name}")
        if arg_types:
            arg_types_str = ', '.join(arg_types)
            self._add_line(f"_{name}_ffi.argtypes = [{arg_types_str}]")
        self._add_line(f"_{name}_ffi.restype = {restype}")
        
        fixed_params = ', '.join(self._sanitize_name(p['name']) for p in stmt.params)
        self._add_line(f"def {name}({fixed_params}, *args):")
        self.indent_level += 1
        self._add_line(f"return _{name}_ffi({fixed_params}, *args)")
        self.indent_level -= 1
        self._add_line("")

    def _generate_ffi_create_callback(self, stmt: FFICreateCallback):
        """生成创建回调函数代码"""
        cb_type = self._sanitize_name(stmt.callback_type)
        duan_func = self._sanitize_name(stmt.duan_function)
        self._add_line(f"# 创建回调: {duan_func} -> {cb_type}")
        self._add_line(f"_cb_{duan_func} = {cb_type}({duan_func})")
        self._add_line("")

    def _generate_ffi_struct_by_value(self, stmt: FFIStructByValue):
        """生成结构体按值传递代码"""
        struct_type = self._sanitize_name(stmt.struct_type)
        self._add_line(f"# 结构体按值传递: {struct_type}")
        self._add_line(f"_struct_val = {struct_type}()")
        for fname, fval in stmt.fields.items():
            sfname = self._sanitize_name(fname)
            val_code = self._generate_expr(fval)
            self._add_line(f"_struct_val.{sfname} = {val_code}")
        self._add_line("")

    def _generate_ffi_library_path(self, stmt: FFILibraryPath):
        """生成跨平台库路径解析代码"""
        name = self._sanitize_name(stmt.name)
        self._add_line(f"# 跨平台库路径: {name}")
        self._add_line(f"_platform = sys.platform")
        if stmt.platform_map:
            self._add_line(f"_lib_map_{name} = {{")
            for plat, path in stmt.platform_map.items():
                self._add_line(f"    '{plat}': '{path}',")
            self._add_line("}")
            self._add_line(f"_{name}_libpath = _lib_map_{name}.get(_platform, '')")
        else:
            self._add_line(f"_{name}_libpath = ''")
        self._add_line("")

    def _generate_ffi_typedef_def(self, stmt: FFITypedefDef):
        """生成C类型别名代码"""
        name = self._sanitize_name(stmt.name)
        base_type = self._get_ffi_type(stmt.base_type)
        self._add_line(f"# C类型别名: {name} -> {base_type}")
        self._add_line(f"{name} = {base_type}")
        self._add_line("")
        # 注册类型别名
        self._ffi_user_types[stmt.name] = name
        self._add_line(f"_duan_ffi.注册类型('{stmt.name}', {name})")

    def _generate_ffi_bitfield_def(self, stmt: FFIBitfieldDef):
        """生成C位域定义代码"""
        name = self._sanitize_name(stmt.name)
        base_type = self._get_ffi_type(stmt.base_type)
        fields_code = []
        for f in stmt.fields:
            fname = self._sanitize_name(f['name'])
            bits = f['bits']
            fields_code.append(f"('{fname}', {base_type}, {bits})")
        fields_str = ', '.join(fields_code)
        self._add_line(f"# C位域: {name}")
        self._add_line(f"class {name}(ctypes.Structure):")
        self.indent_level += 1
        self._add_line(f"_fields_ = [{fields_str}]")
        self.indent_level -= 1
        self._add_line("")

    def _generate_ffi_funcptr_def(self, stmt: FFIFuncPtrDef):
        """生成C函数指针类型代码"""
        name = self._sanitize_name(stmt.name)
        arg_types = []
        for p in stmt.params:
            duan_type = p.get('type', '整数')
            ctype = self._get_ffi_type(duan_type)
            arg_types.append(ctype)
        restype = 'None'
        if stmt.return_type:
            restype = self._get_ffi_type(stmt.return_type)
        arg_types_str = ', '.join(arg_types) if arg_types else ''
        self._add_line(f"# C函数指针类型: {name}")
        self._add_line(f"{name} = ctypes.CFUNCTYPE({restype}, {arg_types_str})")
        self._add_line("")
        # 注册函数指针类型
        self._ffi_user_types[stmt.name] = name
        self._add_line(f"_duan_ffi.注册类型('{stmt.name}', {name})")

    def _generate_ffi_debug_config(self, stmt: FFIDebugConfig):
        """生成FFI调试配置代码"""
        self._add_line("# FFI调试配置")
        self._add_line(f"_duan_ffi.set_debug(")
        self.indent_level += 1
        self._add_line(f"enabled={stmt.enabled},")
        self._add_line(f"log_calls={stmt.log_calls},")
        self._add_line(f"log_types={stmt.log_types},")
        self._add_line(f"trace_memory={stmt.trace_memory},")
        self.indent_level -= 1
        self._add_line(")")
        self._add_line("")

    def _generate_ffi_preprocessor_def(self, stmt: FFIPreprocessorDef):
        """生成C预处理器宏代码"""
        name = self._sanitize_name(stmt.name)
        self._add_line(f"# C预处理器宏: {name} = {stmt.value}")
        self._add_line(f"_duan_ffi.定义宏('{name}', {repr(stmt.value)})")
        self._add_line("")

    # =========================================================================
    # C FFI 表达式级代码生成（第二阶段：指针/数组/错误处理）
    # =========================================================================

    def _generate_ffi_pointer_type(self, expr: FFIPointerType) -> str:
        """生成指针类型表达式：指针[整数] → ctypes.POINTER(ctypes.c_int)"""
        base_type = self._get_ffi_type(expr.base_type)
        return f"ctypes.POINTER({base_type})"

    def _generate_ffi_array_type(self, expr: FFIArrayType) -> str:
        """生成数组类型表达式：数组[整数, 5] → (ctypes.c_int * 5)"""
        base_type = self._get_ffi_type(expr.base_type)
        if expr.size is not None:
            size = self._generate_expr(expr.size) if isinstance(expr.size, ASTNode) else str(expr.size)
            return f"({base_type} * {size})"
        return f"({base_type} * 0)"

    def _generate_ffi_address_of(self, expr: FFIAddressOf) -> str:
        """生成取地址表达式：取地址(变量) → ctypes.pointer(变量)"""
        target = self._generate_expr(expr.target)
        return f"ctypes.pointer({target})"

    def _generate_ffi_dereference(self, expr: FFIDereference) -> str:
        """生成解引用表达式：解引用(指针) → 指针[0]"""
        pointer = self._generate_expr(expr.pointer)
        return f"{pointer}[0]"

    def _generate_ffi_pointer_offset(self, expr: FFIPointerOffset) -> str:
        """生成指针偏移表达式：指针偏移(指针, 偏移量) → ctypes.cast(指针, ctypes.POINTER(ctypes.c_byte))[偏移量]"""
        pointer = self._generate_expr(expr.pointer)
        offset = self._generate_expr(expr.offset)
        return f"ctypes.cast({pointer}, ctypes.POINTER(ctypes.c_byte))[{offset}]"

    def _generate_ffi_get_last_error(self, expr: FFIGetLastError) -> str:
        """生成获取FFI错误表达式：获取FFI错误() → _duan_ffi.获取FFI错误()"""
        return "_duan_ffi.获取FFI错误()"

    def _generate_ffi_get_errno(self, expr: FFIGetErrno) -> str:
        """生成获取系统错误码表达式：获取系统错误码() → ctypes.get_errno()"""
        return "ctypes.get_errno()"

    def _generate_embed_block(self, stmt: EmbedBlock):
        """生成嵌入块代码
        
        Python 嵌入块：直接输出原始 Python 代码，共享段言变量作用域。
        C 嵌入块：通过 ctypes 编译执行。
        其他语言：以注释形式保留，提示不支持。
        """
        import textwrap
        
        lang = stmt.language.strip()
        code = textwrap.dedent(stmt.code).strip()
        
        if lang.lower() in ('python', 'py'):
            # Python 嵌入块：直接输出原始代码，保持缩进
            self._add_line(f"# --- 嵌入 Python ---")
            for line in code.split('\n'):
                self._add_line(line)
            self._add_line(f"# --- 结束嵌入 ---")
        elif lang.lower() in ('c',):
            # C 嵌入块：通过 ctypes/cffi 编译执行
            self._add_line(f"# --- 嵌入 C（通过 ctypes 执行）---")
            self._add_line("import ctypes")
            self._add_line("import tempfile")
            self._add_line("import os")
            self._add_line("_duan_c_code = '''")
            for line in code.split('\n'):
                self._add_line(line)
            self._add_line("'''")
            # 编译并加载
            self._add_line("_duan_c_src = tempfile.NamedTemporaryFile(suffix='.c', delete=False, mode='w')")
            self._add_line("_duan_c_src.write(_duan_c_code)")
            self._add_line("_duan_c_src.close()")
            self._add_line("_duan_c_lib_path = _duan_c_src.name.replace('.c', '.so')")
            self._add_line("import subprocess")
            self._add_line("subprocess.run(['cc', '-shared', '-fPIC', '-o', _duan_c_lib_path, _duan_c_src.name], check=True)")
            self._add_line("_duan_c_lib = ctypes.CDLL(_duan_c_lib_path)")
            self._add_line(f"# --- 结束嵌入 C ---")
        else:
            # 不支持的语言：以注释保留
            self._add_line(f"# --- 嵌入 {lang}（暂不支持直接执行）---")
            for line in code.split('\n'):
                self._add_line(f"# {line}")
            self._add_line(f"# --- 结束嵌入 ---")


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
