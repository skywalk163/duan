"""
段言（Duan）LLVM IR 代码生成器 - 基类

LLVM 代码生成器基类，包含核心框架方法。
"""

import os
import subprocess
from typing import List, Optional

from duan_ast import (
    ASTNode, Module, NumberLiteral, StringLiteral, BooleanLiteral,
    NullLiteral, Identifier, SegmentName, ModuleName,
    BinaryOp, UnaryOp, FunctionCall, PipeExpression,
    PropertyAccess, IndexAccess, ListLiteral, DictLiteral, DictEntry,
    VariableDeclaration, Assignment, CompoundAssignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    TryStatement, ThrowStatement, PrintStatement, ExpressionStatement,
    Parameter, SegmentDefinition, ImportStatement, ExportStatement,
    ClassDefinition, InterfaceDefinition, MethodDefinition, ConstructorDefinition,
    NewExpression,
)

# LLVM 工具路径
LLVM_BIN = r"E:\Program Files\LLVM\bin"
CLANG = os.path.join(LLVM_BIN, "clang.exe")


class LLVMCodeGenCore:
    """AST → LLVM IR 文本生成器（基类，核心框架方法）"""

    def __init__(self):
        self.lines: List[str] = []
        self.indent_level = 0
        self.variables: dict = {}         # 变量名 -> 寄存器名（指针）
        self.strings: dict = {}           # 字符串常量 -> 全局变量名
        self.string_counter = 0
        self.label_counter = 0
        self.current_function = None
        self.reg_counter = 0              # 寄存器编号计数器
        self.global_decls: List[str] = [] # 全局声明（函数之前）
        self.float_vars: set = set()      # 浮点变量集合
        self.array_vars: set = set()      # 数组变量集合
        self.dict_vars: set = set()       # 字典变量集合
        self.type_info: dict = {}         # 变量类型信息
        self.segment_counter = 0          # 段落计数器（用于生成唯一函数名）
        self.segment_name_map: dict = {}  # 中文函数名 -> 英文函数名映射

    # =========================================================================
    # 辅助方法
    # =========================================================================

    def emit(self, line: str = ""):
        """写一行 LLVM IR"""
        indent = "  " * self.indent_level
        self.lines.append(f"{indent}{line}")

    def new_label(self, prefix: str = "L") -> str:
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"

    def new_register(self) -> str:
        """分配一个新的虚拟寄存器 (%1, %2, ...)"""
        self.reg_counter += 1
        return f"%{self.reg_counter}"

    def get_string_ref(self, value: str) -> str:
        """为字符串常量创建全局变量，返回指针"""
        if value in self.strings:
            return self.strings[value]
        name = f".str.{self.string_counter}"
        self.string_counter += 1
        self.strings[value] = name
        return name

    def _get_segment_name(self, chinese_name: str) -> str:
        """将中文段落名转换为有效的LLVM函数名"""
        if chinese_name in self.segment_name_map:
            return self.segment_name_map[chinese_name]

        # 生成唯一的英文函数名（确保是有效的 LLVM 标识符）
        self.segment_counter += 1
        # 特殊处理主段
        if chinese_name == '主段':
            name = 'main'
        else:
            import hashlib
            # 使用哈希生成一个确定性的标识符
            hash_val = hashlib.md5(chinese_name.encode('utf-8')).hexdigest()[:6]
            name = f'seg_{self.segment_counter}_{hash_val}'

        self.segment_name_map[chinese_name] = name
        return name

    # =========================================================================
    # 模块级生成
    # =========================================================================

    def generate(self, module: Module) -> str:
        """生成完整的 LLVM IR 模块"""
        self.lines = []
        self.variables = {}
        self.strings = {}
        self.string_counter = 0
        self.label_counter = 0
        self.global_decls: List[str] = []  # 全局声明（函数之前）

        # 模块声明
        self.emit(f'; 段言 (Duan) 编译输出')
        self.emit(f'target triple = "x86_64-pc-windows-msvc"')
        self.emit('')

        # 声明运行时函数
        self._declare_runtime()

        # 添加默认的 printf 格式字符串
        self._add_global('.printf_fmt', '[4 x i8] c"%d\\0A\\00"')

        # 生成段落定义
        for seg in module.segments:
            self._generate_segment(seg)

        # 生成类定义
        for cls in module.classes:
            self._generate_class(cls)

        # 生成接口定义（接口暂时只做声明）
        for iface in module.interfaces:
            self._generate_interface(iface)

        # 生成顶层语句（包装在 main 中）
        if module.statements:
            self._generate_main(module.statements)

        # 把全局声明插入到 runtime 声明之后、函数之前
        # 重建输出
        header_end = 0
        for i, line in enumerate(self.lines):
            if line.startswith('define ') or line.startswith('; 段言'):
                continue
            if line.strip() == '':
                header_end = i + 1

        result_lines = []
        in_header = True
        for line in self.lines:
            if line.startswith('define '):
                if in_header:
                    # 在这里插入全局声明
                    for g in self.global_decls:
                        result_lines.append(g)
                    result_lines.append('')
                    in_header = False
                result_lines.append(line)
            else:
                result_lines.append(line)

        return "\n".join(result_lines)

    def _add_global(self, name: str, value: str):
        """添加一个全局变量声明"""
        decl = f'@{name} = private unnamed_addr constant {value}'
        if decl not in self.global_decls:
            self.global_decls.append(decl)

    def _declare_runtime(self):
        """声明需要用到的 C 运行时函数"""
        # 标准IO函数
        self.emit('declare i32 @printf(i8*, ...)')
        self.emit('declare i32 @puts(i8*)')
        self.emit('declare i32 @fputs(i8*, i8*)')

        # 内存管理
        self.emit('declare i8* @malloc(i64)')
        self.emit('declare void @free(i8*)')

        # 数学函数（浮点数）
        self.emit('declare double @sin(double)')
        self.emit('declare double @cos(double)')
        self.emit('declare double @tan(double)')
        self.emit('declare double @exp(double)')
        self.emit('declare double @log(double)')
        self.emit('declare double @log10(double)')
        self.emit('declare double @sqrt(double)')
        self.emit('declare double @pow(double, double)')
        self.emit('declare double @fabs(double)')
        self.emit('declare double @floor(double)')
        self.emit('declare double @ceil(double)')
        self.emit('declare double @round(double)')
        self.emit('declare double @cbrt(double)')
        self.emit('declare double @fmod(double, double)')
        self.emit('declare double @fmin(double, double)')
        self.emit('declare double @fmax(double, double)')

        # 字符串函数
        self.emit('declare i32 @strlen(i8*)')
        self.emit('declare i8* @strcpy(i8*, i8*)')
        self.emit('declare i8* @strcat(i8*, i8*)')
        self.emit('declare i32 @strcmp(i8*, i8*)')
        self.emit('declare i8* @strstr(i8*, i8*)')

        # 文件操作
        self.emit('declare i8* @fopen(i8*, i8*)')
        self.emit('declare i32 @fclose(i8*)')
        self.emit('declare i64 @fread(i8*, i64, i64, i8*)')
        self.emit('declare i32 @fwrite(i8*, i64, i64, i8*)')

        # 列表操作（数组）
        self.emit('declare i32* @duan_list_new(i64)')
        self.emit('declare i32 @duan_list_length(i32*)')
        self.emit('declare i32 @duan_list_append(i32*, i32)')
        self.emit('declare i32 @duan_list_get(i32*, i64)')
        self.emit('declare void @duan_list_set(i32*, i64, i32)')
        self.emit('declare i32* @duan_list_copy(i32*)')
        self.emit('declare void @duan_list_free(i32*)')

        # 类型转换函数
        self.emit('declare i8* @duan_itoa(i32)')

        # 字典操作（哈希表）
        self.emit('declare i8* @duan_dict_new()')
        self.emit('declare void @duan_dict_set(i8*, i8*, i32)')
        self.emit('declare i32 @duan_dict_get(i8*, i8*)')
        self.emit('declare i1 @duan_dict_contains(i8*, i8*)')
        self.emit('declare void @duan_dict_remove(i8*, i8*)')
        self.emit('declare void @duan_dict_free(i8*)')
        self.emit('')

    def _collect_strings(self, module):
        """预收集所有字符串常量（遍历 AST）"""
        # 简化：在 generate_string_global 中动态添加
        pass

    def _generate_string_global(self, name: str, value: str):
        """生成字符串全局常量定义"""
        # 将字符串转换为 UTF-8 字节
        utf8_bytes = value.encode('utf-8')
        # 转义特殊字符
        escaped = []
        for b in utf8_bytes:
            if b == ord('\\'):
                escaped.append('\\5C')
            elif b == ord('\n'):
                escaped.append('\\0A')
            elif b == ord('"'):
                escaped.append('\\22')
            elif b < 32 or b > 126:
                # 非 ASCII 字符用十六进制转义
                escaped.append(f'\\{b:02X}')
            else:
                escaped.append(chr(b))
        escaped_str = ''.join(escaped)
        # 使用字节长度而非字符长度
        byte_length = len(utf8_bytes)
        self._add_global(name, f'[{byte_length + 1} x i8] c"{escaped_str}\\00"')

    # =========================================================================
    # main 包装
    # =========================================================================

    def _generate_main(self, statements: List[ASTNode]):
        """将顶层语句包装在 main 函数中"""
        self.emit('define i32 @main() {')
        self.indent_level = 1
        self.variables = {}
        self.reg_counter = 0
        self.current_function = 'main'

        # 为变量分配 alloca
        for stmt in statements:
            if isinstance(stmt, VariableDeclaration):
                reg = self.new_register()
                # 判断变量类型
                is_class = isinstance(stmt.value, NewExpression) if stmt.value else False
                if is_class:
                    self.emit(f'{reg} = alloca i8*, align 8')
                    self.type_info[stmt.name] = f'class_{stmt.value.class_name}'
                else:
                    self.emit(f'{reg} = alloca i32, align 4')
                    self.type_info[stmt.name] = 'int'
                self.variables[stmt.name] = reg

        for stmt in statements:
            self._generate_statement(stmt)

        self.emit('ret i32 0')
        self.indent_level = 0
        self.emit('}')
        self.emit('')