"""
LLVM 代码生成器 - 类型版 (v3)
使用 DuanValue 结构体（{ i32, i64, double, ptr }），
算术运算在原生类型上直接操作，无需 atoi/itoa 转换。
"""

from typing import Optional, Tuple, List
import sys
import ast_nodes as ast
from .codegen import LLVMCodeGen


# LLVM 结构体类型：{ i32 type, i64 i64_val, double f64_val, ptr str_val }
DUANVALUE_STRUCT = '{ i32, i64, double, ptr, i32, [4 x i8] }'


class TypedLLVMCodeGen(LLVMCodeGen):
    """类型版 LLVM 代码生成器"""

    def __init__(self, target_platform: str = None):
        super().__init__()
        self._dv_struct_slots = {}  # 栈上分配的结构体槽位
        self._classes = {}  # 类定义收集：class_name -> ClassDefinition
        self._method_result_ptr = None  # 当前方法的 result 指针（None 表示不在方法中）
        self._current_class = None  # 当前方法所属的类名（None 表示不在方法中）
        self._current_method_type = None  # 当前方法类型：'instance' / 'class' / 'static'
        # 目标平台：win32 / linux / darwin，默认根据当前系统判断
        self.target_platform = target_platform or sys.platform

    @property
    def is_windows(self) -> bool:
        return self.target_platform.startswith('win')

    @property
    def is_linux(self) -> bool:
        return self.target_platform.startswith('linux')

    @property
    def is_macos(self) -> bool:
        return self.target_platform == 'darwin'

    def alloca_local(self, name):
        """为局部变量分配 DuanValue 栈空间（重写父类）"""
        if name not in self._local_vars or self._local_vars[name] is None:
            reg = self.new_register()
            line = f'{reg} = alloca {DUANVALUE_STRUCT}'
            self._pending_allocas.append(line)
            self._local_vars[name] = reg

    # ============================================================
    # 类型控制
    # ============================================================

    def _declare_typed_runtime(self):
        """声明类型版的运行时函数（所有 DuanValue 通过 ptr 传递）"""
        funcs = [
            f'declare void @dv_int(ptr, i64)',
            f'declare void @dv_float(ptr, double)',
            f'declare void @dv_str(ptr, ptr)',
            f'declare void @dv_bool(ptr, i32)',
            f'declare void @dv_null(ptr)',
            f'declare i32 @dv_is_null(ptr)',
            f'declare void @dv_null_coalesce(ptr, ptr, ptr)',
            f'declare void @dv_safe_get(ptr, ptr, ptr)',
            f'declare void @dv_add(ptr, ptr, ptr)',
            f'declare void @dv_sub(ptr, ptr, ptr)',
            f'declare void @dv_mul(ptr, ptr, ptr)',
            f'declare void @dv_div(ptr, ptr, ptr)',
            f'declare i32 @dv_eq(ptr, ptr)',
            f'declare i32 @dv_lt(ptr, ptr)',
            f'declare i32 @dv_gt(ptr, ptr)',
            f'declare i32 @dv_le(ptr, ptr)',
            f'declare i32 @dv_ge(ptr, ptr)',
            f'declare void @dv_println(ptr)',
            f'declare void @dv_print(ptr)',
            f'declare void @dv_input(ptr)',
            f'declare void @dv_concat(ptr, ptr, ptr)',
            f'declare i64 @dv_str_len(ptr)',
            f'declare void @dv_list_new(ptr)',
            f'declare i64 @dv_list_len(ptr)',
            f'declare i64 @dv_len(ptr)',
            f'declare void @dv_list_get(ptr, ptr, i64)',
            f'declare void @dv_list_append(ptr, ptr, ptr)',
            f'declare void @dv_list_insert(ptr, ptr, i64, ptr)',
            f'declare void @dv_list_remove(ptr, ptr, i64)',
            f'declare void @dv_list_set(ptr, ptr, i64, ptr)',
            f'declare i64 @dv_list_index_of(ptr, ptr)',
            f'declare i64 @dv_list_contains(ptr, ptr)',
            f'declare void @dv_list_reverse(ptr, ptr)',
            f'declare void @dv_list_sort(ptr, ptr)',
            f'declare void @dv_list_clear(ptr, ptr)',
            f'declare void @dv_sin(ptr, ptr)',
            f'declare void @dv_cos(ptr, ptr)',
            f'declare void @dv_sqrt(ptr, ptr)',
            f'declare void @dv_abs(ptr, ptr)',
            f'declare void @dv_pow(ptr, ptr, ptr)',
            f'declare void @dv_floor(ptr, ptr)',
            f'declare void @dv_ceil(ptr, ptr)',
            f'declare void @dv_mod(ptr, ptr, ptr)',
            f'declare void @dv_substr(ptr, ptr, i64, i64)',
            f'declare i64 @dv_str_find(ptr, ptr)',
            f'declare void @dv_upper(ptr, ptr)',
            f'declare void @dv_lower(ptr, ptr)',
            f'declare void @dv_trim(ptr, ptr)',
            f'declare void @dv_str_replace(ptr, ptr, ptr, ptr)',
            f'declare void @dv_str_split(ptr, ptr, ptr)',
            f'declare void @dv_to_int(ptr, ptr)',
            f'declare void @dv_to_float(ptr, ptr)',
            f'declare void @dv_to_bool_val(ptr, ptr)',
            f'declare double @dv_timestamp()',
            f'declare ptr @dv_format_time(double, ptr)',
            f'declare i32 @dv_file_exists(ptr)',
            f'declare ptr @dv_read_file(ptr)',
            f'declare void @dv_write_file(ptr, ptr)',
            f'declare void @dv_append_file(ptr, ptr)',
            f'declare i64 @dv_file_size(ptr)',
            f'declare i32 @dv_delete_file(ptr)',
            f'declare void @dv_list_dir(ptr, ptr)',
            f'declare ptr @dv_str_join(ptr, ptr)',
            f'declare ptr @dv_getenv(ptr)',
            f'declare i32 @dv_setenv(ptr, ptr)',
            f'declare ptr @dv_getcwd()',
            f'declare i32 @dv_chdir(ptr)',
            f'declare i32 @dv_system(ptr)',
            f'declare void @dv_exit(i32)',
            f'declare void @dv_init_args(i32, ptr)',
            f'declare void @dv_get_args(ptr)',
            f'declare void @dv_try_enter(ptr, ptr)',
            f'declare void @dv_try_end()',
            f'declare ptr @dv_try_push()',
            f'declare void @dv_try_pop()',
            f'declare void @dv_throw(ptr)',
            f'declare ptr @dv_get_exception_str()',
            f'declare void @dv_clear_exception()',
            f'declare void @dv_throw_exception(ptr)',
            f'declare void @dv_get_current_exception(ptr)',
            f'declare i32 @dv_exception_match(ptr, ptr)',
            f'declare void @dv_clear_exception_obj()',
            # 类系统
            f'declare void @dv_class_new(ptr, i32)',
            f'declare void @dv_class_set_member(ptr, ptr, ptr)',
            f'declare void @dv_class_get_member(ptr, ptr, ptr)',
            f'declare i32 @dv_register_class(ptr, ptr)',
            f'declare i32 @dv_register_method(ptr, ptr, ptr)',
            f'declare i32 @dv_register_attr(ptr, ptr)',
            f'declare ptr @dv_find_method(ptr, ptr)',
            f'declare void @dv_class_new_named(ptr, ptr)',
            f'declare void @dv_get_class_name(ptr, ptr, i32)',
            f'declare void @dv_value_to_string(ptr, ptr)',
            f'declare void @dv_call_method(ptr, ptr, ptr, ptr, i32)',
            f'declare void @dv_call_super_method(ptr, ptr, ptr, ptr, ptr, i32)',
            f'declare i32 @dv_isinstance(ptr, ptr)',
            f'declare void @dv_get_type_name(ptr, ptr, i32)',
            f'declare i32 @dv_register_class_method(ptr, ptr, ptr)',
            f'declare i32 @dv_register_static_method(ptr, ptr, ptr)',
            f'declare void @dv_call_class_method(ptr, ptr, ptr, ptr, i32)',
            f'declare void @dv_call_static_method(ptr, ptr, ptr, ptr, i32)',
            # 异常栈追踪
            f'declare void @dv_stack_push(ptr, ptr, i32)',
            f'declare void @dv_stack_pop()',
            f'declare void @dv_create_exception_with_cause(ptr, ptr, ptr, ptr)',
            f'declare i64 @dv_exception_to_full_string(ptr, ptr, i32)',
            # 字典操作
            f'declare void @dv_dict_new(ptr)',
            f'declare void @dv_dict_set(ptr, ptr, ptr, ptr)',
            f'declare void @dv_dict_get(ptr, ptr, ptr)',
            f'declare void @dv_dict_has(ptr, ptr, ptr)',
            f'declare void @dv_dict_keys(ptr, ptr)',
            f'declare void @dv_dict_values(ptr, ptr)',
        ]
        for f in funcs:
            self._func_decls.add(f)

        # setjmp 声明：平台相关
        if self.is_windows:
            # Windows x64: _setjmp 需两个参数（jmp_buf + frameaddress）
            self._func_decls.add(f'declare i32 @_setjmp(ptr, ptr)')
        else:
            # Linux / macOS: 标准 setjmp 只需一个参数（jmp_buf）
            self._func_decls.add(f'declare i32 @setjmp(ptr)')

    # ============================================================
    # DuanValue 堆栈操作
    # ============================================================

    def _new_dv_slot(self) -> str:
        """分配一个新的 DuanValue 栈槽"""
        reg = self.new_register()
        self.emit(f'{reg} = alloca {DUANVALUE_STRUCT}')
        return reg

    def _set_type(self, slot: str, type_val: int):
        """设置 DuanValue 槽位的 type 字段"""
        ptr = self.new_register()
        self.emit(f'{ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {slot}, i32 0, i32 0')
        self.emit(f'store i32 {type_val}, ptr {ptr}')

    def _set_i64(self, slot: str, i64_val: str):
        """设置 DuanValue 槽位的 i64 字段"""
        ptr = self.new_register()
        self.emit(f'{ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {slot}, i32 0, i32 1')
        self.emit(f'store i64 {i64_val}, ptr {ptr}')

    def _set_f64(self, slot: str, f64_val: str):
        """设置 DuanValue 槽位的 f64 字段"""
        ptr = self.new_register()
        self.emit(f'{ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {slot}, i32 0, i32 2')
        self.emit(f'store i64 {f64_val}, ptr {ptr}')

    def _set_str(self, slot: str, str_val: str):
        """设置 DuanValue 槽位的 str 字段"""
        ptr = self.new_register()
        self.emit(f'{ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {slot}, i32 0, i32 3')
        self.emit(f'store ptr {str_val}, ptr {ptr}')

    def _load_dv(self, slot: str) -> str:
        """加载整个 DuanValue 作为 SSA 值"""
        reg = self.new_register()
        self.emit(f'{reg} = load {DUANVALUE_STRUCT}, ptr {slot}')
        return reg

    def _store_dv(self, dv_reg: str) -> str:
        """将 DuanValue SSA 寄存器存入槽位，返回槽位指针"""
        slot = self._new_dv_slot()
        self.emit(f'store {DUANVALUE_STRUCT} {dv_reg}, ptr {slot}')
        return slot

    def _create_int_dv(self, i64_str: str) -> str:
        """创建整数 DuanValue 并返回 SSA 值"""
        slot = self._new_dv_slot()
        self.emit(f'call void @dv_int(ptr {slot}, i64 {i64_str})')
        return self._load_dv(slot)

    def _create_str_dv(self, ptr_val: str) -> str:
        """创建字符串 DuanValue 并返回 SSA 值"""
        slot = self._new_dv_slot()
        self.emit(f'call void @dv_str(ptr {slot}, ptr {ptr_val})')
        return self._load_dv(slot)

    def _create_bool_dv(self, i1_val: str) -> str:
        """根据 i1 条件创建布尔 DuanValue"""
        slot = self._new_dv_slot()
        ext = self.new_register()
        self.emit(f'{ext} = zext i1 {i1_val} to i32')
        self.emit(f'call void @dv_bool(ptr {slot}, i32 {ext})')
        return self._load_dv(slot)

    def _call_dv_func(self, func_name: str, *args: str) -> str:
        """调用通过 ptr 输出 DuanValue 的运行时函数"""
        result_slot = self._new_dv_slot()
        call_args = [f'ptr {result_slot}']
        for a in args:
            if ' ' in a:
                # 已有类型注释（如 'double %dbl', 'i64 %idx'），直接传递
                call_args.append(a)
            else:
                # DuanValue SSA 寄存器 → 存入槽位后传 ptr
                slot = self._new_dv_slot()
                self.emit(f'store {DUANVALUE_STRUCT} {a}, ptr {slot}')
                call_args.append(f'ptr {slot}')
        self.emit(f'call void @{func_name}({", ".join(call_args)})')
        return self._load_dv(result_slot)

    # ============================================================
    # 覆盖父类的表达式/语句生成
    # ============================================================

    def generate(self, module: ast.Module) -> str:
        self.declare_runtime()
        self._declare_typed_runtime()

        for stmt in module.statements:
            if isinstance(stmt, ast.ImportStatement):
                continue
            self._collect_statement(stmt)
        if hasattr(module, 'classes'):
            for cls_def in module.classes:
                self._collect_class(cls_def)
        for seg in module.segments:
            self._collect_segment(seg)

        self._gen_global_init()
        for cls_name, cls_def in self._classes.items():
            self._gen_typed_class_methods(cls_name, cls_def)
        for seg_name in self._segment_order:
            params = self._segments[seg_name]
            body = self._segment_bodies.get(seg_name, [])
            self._gen_typed_segment(seg_name, params, body)

        self._gen_typed_main()
        return self.finalize()

    # ============================================================
    # 重写表达式生成：使用 DuanValue
    # ============================================================

    def _gen_expression(self, expr) -> Tuple[str, str]:
        """生成表达式，返回 (DuanValue_SSA, 'dv')"""
        if expr is None:
            return self._create_int_dv('0'), 'dv'

        if isinstance(expr, ast.NumberLiteral):
            val = expr.value
            if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
                return self._create_int_dv(str(val)), 'dv'
            return self._call_dv_func('dv_float', f'double {val}'), 'dv'

        if isinstance(expr, ast.StringLiteral):
            s_reg = self.gen_string_constant(expr.value)
            return self._create_str_dv(s_reg), 'dv'

        if isinstance(expr, ast.BooleanLiteral):
            val_i1 = '1' if expr.value else '0'
            reg = self.new_register()
            self.emit(f'{reg} = zext i1 {val_i1} to i64')
            return self._create_int_dv(reg), 'dv'

        if isinstance(expr, ast.NullLiteral):
            return self._call_dv_func('dv_null'), 'dv'

        if isinstance(expr, ast.Identifier):
            return self._gen_typed_identifier(expr)

        if isinstance(expr, ast.BinaryOp):
            return self._gen_typed_binary_op(expr)

        if isinstance(expr, ast.UnaryOp):
            return self._gen_typed_unary_op(expr)

        if isinstance(expr, ast.FunctionCall):
            return self._gen_typed_function_call(expr)

        if hasattr(ast, 'ParagraphCall') and isinstance(expr, ast.ParagraphCall):
            args = [self._gen_expression(arg)[0] for arg in expr.args]
            builtin = self._gen_typed_builtin(expr.name, args)
            if builtin is not None:
                return builtin
            if expr.name in self._segments:
                return self._gen_typed_segment_call(expr.name, args)
            return self._create_int_dv('0'), 'dv'

        if isinstance(expr, ast.IndexAccess):
            return self._gen_typed_index_access(expr)

        if isinstance(expr, ast.ListLiteral):
            return self._gen_typed_list_literal(expr)

        if isinstance(expr, ast.ConditionalExpression):
            return self._gen_typed_conditional(expr)

        if isinstance(expr, ast.PropertyAccess):
            return self._gen_typed_property_access(expr)

        if hasattr(ast, 'ClassInstantiation') and isinstance(expr, ast.ClassInstantiation):
            return self._gen_typed_class_instantiation(expr)

        if hasattr(ast, 'NewExpression') and isinstance(expr, ast.NewExpression):
            return self._gen_typed_class_instantiation(expr)

        return self._create_int_dv('0'), 'dv'

    def _gen_typed_identifier(self, expr: ast.Identifier) -> Tuple[str, str]:
        name = expr.name
        var = self.get_var(name)
        if var is not None:
            return var, 'dv'
        
        # 方法内部：以"self."开头的标识符视为 self 的属性访问
        if self._method_result_ptr is not None and name.startswith('self.') and len(name) > 5:
            attr_name = name[5:]
            self_dv = self.get_var('己')
            if self_dv is not None:
                obj_slot = self._store_dv(self_dv)
                member_reg = self.gen_string_constant(attr_name)
                result_slot = self._new_dv_slot()
                self.emit(f'call void @dv_class_get_member(ptr {result_slot}, ptr {obj_slot}, ptr {member_reg})')
                return self._load_dv(result_slot), 'dv'
        
        # 方法内部：以"己"开头的标识符视为 self 的属性访问
        if self._method_result_ptr is not None and name.startswith('己') and len(name) > 1:
            attr_name = name[1:]
            self_dv = self.get_var('己')
            if self_dv is not None:
                obj_slot = self._store_dv(self_dv)
                member_reg = self.gen_string_constant(attr_name)
                result_slot = self._new_dv_slot()
                self.emit(f'call void @dv_class_get_member(ptr {result_slot}, ptr {obj_slot}, ptr {member_reg})')
                return self._load_dv(result_slot), 'dv'
        
        # 内置函数名当作字符串
        str_reg = self.gen_string_constant(name)
        return self._create_str_dv(str_reg), 'dv'

    def _gen_typed_binary_op(self, expr: ast.BinaryOp) -> Tuple[str, str]:
        left_dv, _ = self._gen_expression(expr.left)
        right_dv, _ = self._gen_expression(expr.right)
        op = expr.operator

        type_map = {
            '+': 'dv_add', '-': 'dv_sub', '*': 'dv_mul', '/': 'dv_div',
            '加': 'dv_add', '减': 'dv_sub', '乘': 'dv_mul', '除': 'dv_div',
        }
        if op in type_map:
            dv_func = type_map[op]
            return self._call_dv_func(dv_func, left_dv, right_dv), 'dv'

        cmp_map = {
            '==': 'dv_eq', '等于': 'dv_eq',
            '!=': None, '不等于': None,
            '<': 'dv_lt', '小于': 'dv_lt',
            '>': 'dv_gt', '大于': 'dv_gt',
            '<=': 'dv_le', '小于等于': 'dv_le',
            '>=': 'dv_ge', '大于等于': 'dv_ge',
        }
        if op in cmp_map:
            cmp_name = cmp_map[op]
            if cmp_name is None:
                # !=: 取反 dv_eq
                left_slot = self._store_dv(left_dv)
                right_slot = self._store_dv(right_dv)
                eq = self.new_register()
                self.emit(f'{eq} = call i32 @dv_eq(ptr {left_slot}, ptr {right_slot})')
                cmp = self.new_register()
                self.emit(f'{cmp} = icmp eq i32 {eq}, 0')
                return self._create_bool_dv(cmp), 'dv'
            left_slot = self._store_dv(left_dv)
            right_slot = self._store_dv(right_dv)
            cmp_reg = self.new_register()
            self.emit(f'{cmp_reg} = call i32 @{cmp_name}(ptr {left_slot}, ptr {right_slot})')
            final = self.new_register()
            self.emit(f'{final} = icmp ne i32 {cmp_reg}, 0')
            return self._create_bool_dv(final), 'dv'

        if op == '连接':
            return self._call_dv_func('dv_concat', left_dv, right_dv), 'dv'

        # 默认加法
        return self._call_dv_func('dv_add', left_dv, right_dv), 'dv'

    def _gen_typed_unary_op(self, expr: ast.UnaryOp) -> Tuple[str, str]:
        reg, _ = self._gen_expression(expr.operand)
        if expr.operator == '非':
            zero_dv = self._create_int_dv('0')
            reg_slot = self._store_dv(reg)
            zero_slot = self._store_dv(zero_dv)
            eq = self.new_register()
            self.emit(f'{eq} = call i32 @dv_eq(ptr {reg_slot}, ptr {zero_slot})')
            final = self.new_register()
            self.emit(f'{final} = icmp ne i32 {eq}, 0')
            return self._create_bool_dv(final), 'dv'
        return reg, 'dv'

    def _gen_typed_function_call(self, expr: ast.FunctionCall) -> Tuple[str, str]:
        if isinstance(expr.name, ast.Identifier):
            func_name = expr.name.name
        elif isinstance(expr.name, ast.SegmentName):
            func_name = expr.name.name
        elif isinstance(expr.name, ast.PropertyAccess):
            return self._gen_typed_method_call(expr)
        elif isinstance(expr.name, str):
            func_name = expr.name
        else:
            func_name = str(expr.name)

        args = [self._gen_expression(arg)[0] for arg in expr.arguments]

        # 内置函数
        builtin = self._gen_typed_builtin(func_name, args)
        if builtin is not None:
            return builtin

        # 用户分段
        if func_name in self._segments:
            return self._gen_typed_segment_call(func_name, args)

        return self._create_int_dv('0'), 'dv'

    def _gen_typed_builtin(self, name: str, args: List[str]) -> Optional[Tuple[str, str]]:
        if name in ('输出', '打印'):
            if args:
                slot = self._store_dv(args[0])
                self.emit(f'call void @dv_println(ptr {slot})')
            else:
                null_slot = self._new_dv_slot()
                self.emit(f'call void @dv_null(ptr {null_slot})')
                self.emit(f'call void @dv_println(ptr {null_slot})')
            return self._create_int_dv('0'), 'dv'

        if name in ('输入', 'input'):
            slot = self._new_dv_slot()
            self.emit(f'call void @dv_input(ptr {slot})')
            reg = self._load_dv(slot)
            return reg, 'dv'

        if name in ('时间戳', '时间'):
            dbl = self.new_register()
            self.emit(f'{dbl} = call double @dv_timestamp()')
            return self._call_dv_func('dv_float', f'double {dbl}'), 'dv'

        if name == '格式化时间':
            if not args:
                return self._create_int_dv('0'), 'dv'
            dbl = self.new_register()
            # 从 DuanValue 提取 double
            ptr = self.new_register()
            self.emit(f'{ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 2')
            self.emit(f'{dbl} = bitcast double* {ptr} to double')
            fmt_reg = self.gen_string_constant("%Y-%m-%d %H:%M:%S")
            out = self.new_register()
            self.emit(f'{out} = call ptr @dv_format_time(double {dbl}, ptr {fmt_reg})')
            return self._create_str_dv(out), 'dv'

        if name in ('文件存在', 'file_exists', 'path_exists'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                file_reg = self.new_register()
                self.emit(f'{file_reg} = call i32 @dv_file_exists(ptr {path_ptr})')
                cmp = self.new_register()
                self.emit(f'{cmp} = icmp ne i32 {file_reg}, 0')
                return self._create_bool_dv(cmp), 'dv'
            return self._create_bool_dv('false'), 'dv'

        if name in ('读取文件', 'read_file', 'load_file'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                out = self.new_register()
                self.emit(f'{out} = call ptr @dv_read_file(ptr {path_ptr})')
                return self._create_str_dv(out), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('写入文件', 'write_file', 'save_file'):
            if len(args) >= 2:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                str_ptr = self.new_register()
                self.emit(f'{str_ptr} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 3')
                self.emit(f'call void @dv_write_file(ptr {path_ptr}, ptr {str_ptr})')
            return self._create_int_dv('0'), 'dv'

        if name in ('追加文件', 'append_file', 'write_append'):
            if len(args) >= 2:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                str_ptr = self.new_register()
                self.emit(f'{str_ptr} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 3')
                self.emit(f'call void @dv_append_file(ptr {path_ptr}, ptr {str_ptr})')
            return self._create_int_dv('0'), 'dv'

        if name in ('文件大小', 'file_size'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                size = self.new_register()
                self.emit(f'{size} = call i64 @dv_file_size(ptr {path_ptr})')
                return self._create_int_dv(size), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('删除文件', 'delete_file', 'remove_file'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                ret = self.new_register()
                self.emit(f'{ret} = call i32 @dv_delete_file(ptr {path_ptr})')
                ret_i64 = self.new_register()
                self.emit(f'{ret_i64} = sext i32 {ret} to i64')
                return self._create_int_dv(ret_i64), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('列出目录', 'list_dir', 'dir_list'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                return self._call_dv_func('dv_list_dir', f'ptr {path_ptr}'), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('环境变量', 'getenv', 'get_env'):
            if args:
                name_ptr = self.new_register()
                self.emit(f'{name_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                out = self.new_register()
                self.emit(f'{out} = call ptr @dv_getenv(ptr {name_ptr})')
                return self._create_str_dv(out), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('设置环境变量', 'setenv', 'set_env'):
            if len(args) >= 2:
                name_ptr = self.new_register()
                self.emit(f'{name_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                val_ptr = self.new_register()
                self.emit(f'{val_ptr} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 3')
                ret = self.new_register()
                self.emit(f'{ret} = call i32 @dv_setenv(ptr {name_ptr}, ptr {val_ptr})')
                ret_i64 = self.new_register()
                self.emit(f'{ret_i64} = sext i32 {ret} to i64')
                return self._create_int_dv(ret_i64), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('当前目录', 'getcwd', 'cwd'):
            out = self.new_register()
            self.emit(f'{out} = call ptr @dv_getcwd()')
            return self._create_str_dv(out), 'dv'

        if name in ('切换目录', 'chdir', 'cd'):
            if args:
                path_ptr = self.new_register()
                self.emit(f'{path_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                ret = self.new_register()
                self.emit(f'{ret} = call i32 @dv_chdir(ptr {path_ptr})')
                ret_i64 = self.new_register()
                self.emit(f'{ret_i64} = sext i32 {ret} to i64')
                return self._create_int_dv(ret_i64), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('执行命令', 'system', 'exec'):
            if args:
                cmd_ptr = self.new_register()
                self.emit(f'{cmd_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                ret = self.new_register()
                self.emit(f'{ret} = call i32 @dv_system(ptr {cmd_ptr})')
                ret_i64 = self.new_register()
                self.emit(f'{ret_i64} = sext i32 {ret} to i64')
                return self._create_int_dv(ret_i64), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('退出程序', '退出', 'exit'):
            if args:
                code_i64 = self.new_register()
                self.emit(f'{code_i64} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 1')
                code_i32 = self.new_register()
                self.emit(f'{code_i32} = trunc i64 {code_i64} to i32')
                self.emit(f'call void @dv_exit(i32 {code_i32})')
            else:
                self.emit(f'call void @dv_exit(i32 0)')
            return self._create_int_dv('0'), 'dv'

        if name in ('参数列表', 'argv', 'args'):
            return self._call_dv_func('dv_get_args'), 'dv'

        if name in ('整数', 'int', '转整数', 'to_int'):
            if not args:
                return self._create_int_dv('0'), 'dv'
            return self._call_dv_func('dv_to_int', args[0]), 'dv'

        if name in ('浮点数', 'float', '转浮点', 'to_float'):
            if not args:
                return self._call_dv_func('dv_float', 'double 0.0'), 'dv'
            return self._call_dv_func('dv_to_float', args[0]), 'dv'

        if name == '长度' or name == 'len':
            if not args:
                return self._create_int_dv('0'), 'dv'
            slot = self._store_dv(args[0])
            i64_val = self.new_register()
            self.emit(f'{i64_val} = call i64 @dv_len(ptr {slot})')
            return self._create_int_dv(i64_val), 'dv'

        if name in ('新建', '新建列表', 'new_list'):
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('追加', 'append'):
            if len(args) >= 2:
                return self._call_dv_func('dv_list_append', args[0], args[1]), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('插入', 'insert', 'list_insert'):
            if len(args) >= 3:
                idx_i64 = self.new_register()
                self.emit(f'{idx_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                return self._call_dv_func('dv_list_insert', args[0], f'i64 {idx_i64}', args[2]), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('删除', 'remove', 'list_remove'):
            if len(args) >= 2:
                idx_i64 = self.new_register()
                self.emit(f'{idx_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                return self._call_dv_func('dv_list_remove', args[0], f'i64 {idx_i64}'), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('设置', 'set', 'list_set'):
            if len(args) >= 3:
                idx_i64 = self.new_register()
                self.emit(f'{idx_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                return self._call_dv_func('dv_list_set', args[0], f'i64 {idx_i64}', args[2]), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('索引查找', 'index_of', 'list_index'):
            if len(args) >= 2:
                slot0 = self._new_dv_slot()
                self.emit(f'store {DUANVALUE_STRUCT} {args[0]}, ptr {slot0}')
                slot1 = self._new_dv_slot()
                self.emit(f'store {DUANVALUE_STRUCT} {args[1]}, ptr {slot1}')
                idx = self.new_register()
                self.emit(f'{idx} = call i64 @dv_list_index_of(ptr {slot0}, ptr {slot1})')
                return self._create_int_dv(idx), 'dv'
            return self._create_int_dv('-1'), 'dv'

        if name in ('包含', 'contains', 'list_contains'):
            if len(args) >= 2:
                slot0 = self._new_dv_slot()
                self.emit(f'store {DUANVALUE_STRUCT} {args[0]}, ptr {slot0}')
                slot1 = self._new_dv_slot()
                self.emit(f'store {DUANVALUE_STRUCT} {args[1]}, ptr {slot1}')
                val = self.new_register()
                self.emit(f'{val} = call i64 @dv_list_contains(ptr {slot0}, ptr {slot1})')
                cmp = self.new_register()
                self.emit(f'{cmp} = icmp ne i64 {val}, 0')
                return self._create_bool_dv(cmp), 'dv'
            return self._create_bool_dv('false'), 'dv'

        if name in ('反转', 'reverse', 'list_reverse'):
            if args:
                return self._call_dv_func('dv_list_reverse', args[0]), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('排序', 'sort', 'list_sort'):
            if args:
                return self._call_dv_func('dv_list_sort', args[0]), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('获取', 'get', '索引'):
            if len(args) >= 2:
                idx_i64 = self.new_register()
                self.emit(f'{idx_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                return self._call_dv_func('dv_list_get', args[0], f'i64 {idx_i64}'), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name == '转文本' or name == 'to_string' or name == '转字符串':
            if args:
                return self._call_dv_func('dv_value_to_string', args[0]), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name == '连接':
            a = args[0] if len(args) > 0 else self._create_int_dv('0')
            b = args[1] if len(args) > 1 else self._create_int_dv('0')
            return self._call_dv_func('dv_concat', a, b), 'dv'

        if name in ('正弦', 'sin'):
            if args:
                return self._call_dv_func('dv_sin', args[0]), 'dv'
            return self._call_dv_func('dv_float', 'double 0.0'), 'dv'

        if name in ('余弦', 'cos'):
            if args:
                return self._call_dv_func('dv_cos', args[0]), 'dv'
            return self._call_dv_func('dv_float', 'double 0.0'), 'dv'

        if name in ('平方根', 'sqrt'):
            if args:
                return self._call_dv_func('dv_sqrt', args[0]), 'dv'
            return self._call_dv_func('dv_float', 'double 0.0'), 'dv'

        if name in ('绝对值', 'abs'):
            if args:
                return self._call_dv_func('dv_abs', args[0]), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('幂', 'pow'):
            if len(args) >= 2:
                return self._call_dv_func('dv_pow', args[0], args[1]), 'dv'
            return self._call_dv_func('dv_float', 'double 0.0'), 'dv'

        if name in ('向下取整', 'floor'):
            if args:
                return self._call_dv_func('dv_floor', args[0]), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('向上取整', 'ceil'):
            if args:
                return self._call_dv_func('dv_ceil', args[0]), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('取模', 'mod'):
            if len(args) >= 2:
                return self._call_dv_func('dv_mod', args[0], args[1]), 'dv'
            return self._create_int_dv('0'), 'dv'

        if name in ('截取', 'substr', 'substring'):
            if len(args) >= 3:
                start_i64 = self.new_register()
                self.emit(f'{start_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                len_i64 = self.new_register()
                self.emit(f'{len_i64} = extractvalue {DUANVALUE_STRUCT} {args[2]}, 1')
                return self._call_dv_func('dv_substr', args[0], f'i64 {start_i64}', f'i64 {len_i64}'), 'dv'
            if len(args) >= 2:
                start_i64 = self.new_register()
                self.emit(f'{start_i64} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 1')
                return self._call_dv_func('dv_substr', args[0], f'i64 {start_i64}', f'i64 -1'), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('查找', 'find', 'str_find'):
            if len(args) >= 2:
                slot0 = self._store_dv(args[0])
                slot1 = self._store_dv(args[1])
                i64_val = self.new_register()
                self.emit(f'{i64_val} = call i64 @dv_str_find(ptr {slot0}, ptr {slot1})')
                return self._create_int_dv(i64_val), 'dv'
            return self._create_int_dv('-1'), 'dv'

        if name in ('大写', 'upper', 'to_upper'):
            if args:
                return self._call_dv_func('dv_upper', args[0]), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('小写', 'lower', 'to_lower'):
            if args:
                return self._call_dv_func('dv_lower', args[0]), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('去除空格', 'trim', 'strip'):
            if args:
                return self._call_dv_func('dv_trim', args[0]), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('替换', 'replace', 'str_replace'):
            if len(args) >= 3:
                return self._call_dv_func('dv_str_replace', args[0], args[1], args[2]), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('分割', 'split', 'str_split'):
            if len(args) >= 2:
                return self._call_dv_func('dv_str_split', args[0], args[1]), 'dv'
            return self._call_dv_func('dv_list_new'), 'dv'

        if name in ('连接字符串', 'join', 'str_join', 'implode'):
            if len(args) >= 2:
                list_ptr = self.new_register()
                self.emit(f'{list_ptr} = extractvalue {DUANVALUE_STRUCT} {args[0]}, 3')
                sep_ptr = self.new_register()
                self.emit(f'{sep_ptr} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 3')
                out = self.new_register()
                self.emit(f'{out} = call ptr @dv_str_join(ptr {list_ptr}, ptr {sep_ptr})')
                return self._create_str_dv(out), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name in ('转布尔', 'to_bool', 'bool'):
            if args:
                return self._call_dv_func('dv_to_bool_val', args[0]), 'dv'
            return self._create_bool_dv('false'), 'dv'

        if name in ('是实例', 'isinstance', '是否实例', '是类实例', 'instance_of'):
            if len(args) >= 2:
                obj_slot = self._store_dv(args[0])
                class_name_ptr = self.new_register()
                self.emit(f'{class_name_ptr} = extractvalue {DUANVALUE_STRUCT} {args[1]}, 3')
                result = self.new_register()
                self.emit(f'{result} = call i32 @dv_isinstance(ptr {obj_slot}, ptr {class_name_ptr})')
                cmp = self.new_register()
                self.emit(f'{cmp} = icmp ne i32 {result}, 0')
                return self._create_bool_dv(cmp), 'dv'
            return self._create_bool_dv('false'), 'dv'

        if name in ('取类型', 'type', '获取类型', 'typeof', '类型名', 'type_name'):
            if args:
                obj_slot = self._store_dv(args[0])
                buf_size = 256
                buf_ptr = self.new_register()
                self.emit(f'{buf_ptr} = alloca [256 x i8]')
                buf_cast = self.new_register()
                self.emit(f'{buf_cast} = getelementptr inbounds [256 x i8], ptr {buf_ptr}, i32 0, i32 0')
                self.emit(f'call void @dv_get_type_name(ptr {obj_slot}, ptr {buf_cast}, i32 {buf_size})')
                return self._create_str_dv(buf_cast), 'dv'
            return self._create_str_dv(self.gen_string_constant("")), 'dv'

        if name == '范围':
            return self._gen_typed_range(args)

        if name in ('list', '列表', '创建列表'):
            return self._gen_typed_list_from_builtin_args(args)

        # 字典操作
        if name in ('dict', '字典', '新建字典', '创建字典'):
            dict_dv = self._call_dv_func('dv_dict_new')
            return dict_dv, 'dv'

        # 可空类型操作
        if name in ('是空', 'is_null', 'null?'):
            if args:
                slot = self._store_dv(args[0])
                result = self.new_register()
                self.emit(f'{result} = call i32 @dv_is_null(ptr {slot})')
                return self._create_bool_dv(result), 'dv'
            return self._create_bool_dv('true'), 'dv'

        if name in ('空合并', 'null_coalesce', '??'):
            if len(args) >= 2:
                v_slot = self._store_dv(args[0])
                default_slot = self._store_dv(args[1])
                result_slot = self._new_dv_slot()
                self.emit(f'call void @dv_null_coalesce(ptr {result_slot}, ptr {v_slot}, ptr {default_slot})')
                return self._load_dv(result_slot), 'dv'
            return self._call_dv_func('dv_null'), 'dv'

        if name in ('安全获取', 'safe_get', '?.'):
            if len(args) >= 2:
                obj_slot = self._store_dv(args[0])
                attr_slot = self._store_dv(args[1])
                result_slot = self._new_dv_slot()
                self.emit(f'call void @dv_safe_get(ptr {result_slot}, ptr {obj_slot}, ptr {attr_slot})')
                return self._load_dv(result_slot), 'dv'
            return self._call_dv_func('dv_null'), 'dv'

        return None

    def _gen_typed_list_from_builtin_args(self, args: List[str]) -> Tuple[str, str]:
        """从内置函数调用参数创建列表"""
        list_dv = self._call_dv_func('dv_list_new')
        if not args:
            return list_dv, 'dv'
        
        list_slot = self._new_dv_slot()
        self.emit(f'store {DUANVALUE_STRUCT} {list_dv}, ptr {list_slot}')
        
        for arg in args:
            cur_list = self.new_register()
            self.emit(f'{cur_list} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
            new_list = self._call_dv_func('dv_list_append', cur_list, arg)
            self.emit(f'store {DUANVALUE_STRUCT} {new_list}, ptr {list_slot}')
        
        result = self.new_register()
        self.emit(f'{result} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
        return result, 'dv'

    def _gen_typed_range(self, args: List[str]) -> Tuple[str, str]:
        """生成范围列表"""
        start_dv = args[0] if args else self._create_int_dv('1')
        end_dv = args[1] if len(args) > 1 else self._create_int_dv('10')

        # 提取数值
        start_i64 = self.new_register()
        end_i64 = self.new_register()
        self.emit(f'{start_i64} = extractvalue {DUANVALUE_STRUCT} {start_dv}, 1')
        self.emit(f'{end_i64} = extractvalue {DUANVALUE_STRUCT} {end_dv}, 1')

        list_dv = self._call_dv_func('dv_list_new')
        # 使用 alloca 保存列表
        list_slot = self._new_dv_slot()
        self.emit(f'store {DUANVALUE_STRUCT} {list_dv}, ptr {list_slot}')

        idx_slot = self.new_register()
        self.emit(f'{idx_slot} = alloca i64')
        self.emit(f'store i64 {start_i64}, ptr {idx_slot}')

        range_cond = self.new_label('range_cond')
        range_body = self.new_label('range_body')
        range_end = self.new_label('range_end')
        self.emit(f'br label %{range_cond}')

        self.emit(f'{range_cond}:')
        cur = self.new_register()
        self.emit(f'{cur} = load i64, ptr {idx_slot}')
        cmp = self.new_register()
        self.emit(f'{cmp} = icmp sle i64 {cur}, {end_i64}')
        self.emit(f'br i1 {cmp}, label %{range_body}, label %{range_end}')

        self.emit(f'{range_body}:')
        cur_val = self.new_register()
        self.emit(f'{cur_val} = load i64, ptr {idx_slot}')
        elem_dv = self._create_int_dv(cur_val)
        list_val_load = self.new_register()
        self.emit(f'{list_val_load} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
        new_list_dv = self._call_dv_func('dv_list_append', list_val_load, elem_dv)
        self.emit(f'store {DUANVALUE_STRUCT} {new_list_dv}, ptr {list_slot}')
        next_i = self.new_register()
        self.emit(f'{next_i} = add i64 {cur_val}, 1')
        self.emit(f'store i64 {next_i}, ptr {idx_slot}')
        self.emit(f'br label %{range_cond}')

        self.emit(f'{range_end}:')
        final = self.new_register()
        self.emit(f'{final} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
        return final, 'dv'

    def _gen_typed_property_access(self, expr) -> Tuple[str, str]:
        """处理 obj.成员 (属性访问表达式)"""
        obj_dv, _ = self._gen_expression(expr.obj)
        member = expr.property_name
        if member == '长度' or member == 'len' or member == '大小' or member == 'size':
            slot = self._store_dv(obj_dv)
            i64_val = self.new_register()
            self.emit(f'{i64_val} = call i64 @dv_len(ptr {slot})')
            return self._create_int_dv(i64_val), 'dv'
        obj_slot = self._store_dv(obj_dv)
        member_reg = self.gen_string_constant(member)
        result_slot = self._new_dv_slot()
        self.emit(f'call void @dv_class_get_member(ptr {result_slot}, ptr {obj_slot}, ptr {member_reg})')
        return self._load_dv(result_slot), 'dv'

    def _gen_typed_method_call(self, expr: ast.FunctionCall) -> Tuple[str, str]:
        """处理 obj.方法(args) - FunctionCall with PropertyAccess name"""
        prop = expr.name  # PropertyAccess
        method_name = prop.property_name
        
        # 检测是否是 super 调用（父.方法() 或 super.方法()）
        is_super_call = False
        if isinstance(prop.obj, ast.Identifier):
            obj_name = prop.obj.name
            if obj_name in ('super()', '父', 'super'):
                is_super_call = True
        
        if is_super_call and self._current_class is not None:
            # super 调用：使用 dv_call_super_method
            self_dv = self.get_var('己')
            if self_dv is None:
                return self._create_int_dv('0'), 'dv'
            
            obj_slot = self._store_dv(self_dv)
            method_name_reg = self.gen_string_constant(method_name)
            class_name_reg = self.gen_string_constant(self._current_class)
            
            num_args = len(expr.arguments)
            args_array = self.new_register()
            self.emit(f'{args_array} = alloca {DUANVALUE_STRUCT}, i32 {num_args}')
            
            for i, arg in enumerate(expr.arguments):
                arg_dv, _ = self._gen_expression(arg)
                arg_elem_ptr = self.new_register()
                self.emit(f'{arg_elem_ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {args_array}, i32 {i}')
                self.emit(f'store {DUANVALUE_STRUCT} {arg_dv}, ptr {arg_elem_ptr}')
            
            result_slot = self._new_dv_slot()
            num_args_i32 = self.new_register()
            self.emit(f'{num_args_i32} = add i32 0, {num_args}')
            self.emit(f'call void @dv_call_super_method(ptr {result_slot}, ptr {obj_slot}, ptr {class_name_reg}, ptr {method_name_reg}, ptr {args_array}, i32 {num_args_i32})')
            
            # 更新己变量
            updated_obj = self._load_dv(obj_slot)
            self.set_var('己', updated_obj)
            
            return self._load_dv(result_slot), 'dv'
        
        obj_dv, _ = self._gen_expression(prop.obj)

        # 检查是否是 类名.方法名() 形式的调用（通过类名调用类方法/静态方法）
        if isinstance(prop.obj, ast.Identifier):
            obj_name = prop.obj.name
            if obj_name in self._classes:
                # 这是通过类名调用方法，先判断方法类型
                class_name = obj_name
                cls_def = self._classes[class_name]
                method_type = 'instance'
                # 在类的方法中查找
                for method in getattr(cls_def, 'methods', []) or []:
                    if method.name == method_name:
                        method_type = self._get_method_type(method)
                        break
                
                class_name_reg = self.gen_string_constant(class_name)
                method_name_reg = self.gen_string_constant(method_name)
                
                num_args = len(expr.arguments)
                args_array = self.new_register()
                self.emit(f'{args_array} = alloca {DUANVALUE_STRUCT}, i32 {num_args}')
                
                for i, arg in enumerate(expr.arguments):
                    arg_dv, _ = self._gen_expression(arg)
                    arg_elem_ptr = self.new_register()
                    self.emit(f'{arg_elem_ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {args_array}, i32 {i}')
                    self.emit(f'store {DUANVALUE_STRUCT} {arg_dv}, ptr {arg_elem_ptr}')
                
                result_slot = self._new_dv_slot()
                num_args_i32 = self.new_register()
                self.emit(f'{num_args_i32} = add i32 0, {num_args}')
                
                if method_type == 'static':
                    self.emit(f'call void @dv_call_static_method(ptr {result_slot}, ptr {class_name_reg}, ptr {method_name_reg}, ptr {args_array}, i32 {num_args_i32})')
                else:
                    self.emit(f'call void @dv_call_class_method(ptr {result_slot}, ptr {class_name_reg}, ptr {method_name_reg}, ptr {args_array}, i32 {num_args_i32})')
                
                return self._load_dv(result_slot), 'dv'

        # 先检查是否是内置方法（列表、字符串等）
        # 内置方法调用：把对象作为第一个参数传给内置函数
        args_dv = [obj_dv]
        for arg in expr.arguments:
            arg_dv, _ = self._gen_expression(arg)
            args_dv.append(arg_dv)

        # 尝试使用内置函数处理
        builtin_result = self._gen_typed_builtin(method_name, args_dv)
        if builtin_result is not None:
            return builtin_result

        # 否则使用 dv_call_method 调用类方法
        obj_slot = self._store_dv(obj_dv)
        method_name_reg = self.gen_string_constant(method_name)
        
        num_args = len(expr.arguments)
        args_array = self.new_register()
        self.emit(f'{args_array} = alloca {DUANVALUE_STRUCT}, i32 {num_args}')
        
        for i, arg in enumerate(expr.arguments):
            arg_dv, _ = self._gen_expression(arg)
            arg_elem_ptr = self.new_register()
            self.emit(f'{arg_elem_ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {args_array}, i32 {i}')
            self.emit(f'store {DUANVALUE_STRUCT} {arg_dv}, ptr {arg_elem_ptr}')
        
        result_slot = self._new_dv_slot()
        num_args_i32 = self.new_register()
        self.emit(f'{num_args_i32} = add i32 0, {num_args}')
        self.emit(f'call void @dv_call_method(ptr {result_slot}, ptr {obj_slot}, ptr {method_name_reg}, ptr {args_array}, i32 {num_args_i32})')
        
        # 如果对象是一个变量，把更新后的对象写回变量
        if isinstance(prop.obj, ast.Identifier):
            obj_name = prop.obj.name
            updated_obj = self._load_dv(obj_slot)
            self.set_var(obj_name, updated_obj)
        
        return self._load_dv(result_slot), 'dv'

    def _gen_typed_class_instantiation(self, expr) -> Tuple[str, str]:
        """生成类实例化 new ClassName(args)"""
        class_name = expr.class_name if hasattr(expr, 'class_name') else str(getattr(expr, 'name', 'object'))
        if class_name == '列表' or class_name == 'list':
            return self._call_dv_func('dv_list_new'), 'dv'
        if class_name == '字典' or class_name == 'dict':
            return self._call_dv_func('dv_dict_new'), 'dv'
        
        name_reg = self.gen_string_constant(class_name)
        result_slot = self._new_dv_slot()
        self.emit(f'call void @dv_class_new_named(ptr {result_slot}, ptr {name_reg})')
        
        has_ctor = False
        if class_name in self._classes:
            cls_def = self._classes[class_name]
            constructor = getattr(cls_def, 'constructor', None)
            if constructor is not None:
                has_ctor = True
        
        if has_ctor:
            obj_dv = self._load_dv(result_slot)
            obj_slot = self._store_dv(obj_dv)
            ctor_name_reg = self.gen_string_constant(class_name)
            
            args = getattr(expr, 'arguments', []) or []
            num_args = len(args)
            args_array = self.new_register()
            self.emit(f'{args_array} = alloca {DUANVALUE_STRUCT}, i32 {num_args}')
            
            for i, arg in enumerate(args):
                arg_dv, _ = self._gen_expression(arg)
                arg_elem_ptr = self.new_register()
                self.emit(f'{arg_elem_ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr {args_array}, i32 {i}')
                self.emit(f'store {DUANVALUE_STRUCT} {arg_dv}, ptr {arg_elem_ptr}')
            
            ctor_result_slot = self._new_dv_slot()
            num_args_i32 = self.new_register()
            self.emit(f'{num_args_i32} = add i32 0, {num_args}')
            self.emit(f'call void @dv_call_method(ptr {ctor_result_slot}, ptr {obj_slot}, ptr {ctor_name_reg}, ptr {args_array}, i32 {num_args_i32})')
            
            updated_obj = self._load_dv(obj_slot)
            self.emit(f'store {DUANVALUE_STRUCT} {updated_obj}, ptr {result_slot}')
        
        return self._load_dv(result_slot), 'dv'

    def _gen_typed_try(self, stmt):
        """生成 try-catch 语句 - 使用内联 setjmp 避免栈帧失效问题"""
        # 获取 catch 子句列表（优先使用 catch_clauses，向后兼容 catch_body）
        catch_clauses = []
        if hasattr(stmt, 'catch_clauses') and stmt.catch_clauses and len(stmt.catch_clauses) > 0:
            catch_clauses = stmt.catch_clauses
        elif stmt.catch_body and len(stmt.catch_body) > 0:
            # 向后兼容：旧的单 catch 形式
            from dataclasses import dataclass
            catch_clauses = [type('CatchClause', (), {
                'catch_type': stmt.catch_type or '',
                'catch_var': stmt.catch_var or '',
                'catch_body': stmt.catch_body
            })()]
        
        has_catch = len(catch_clauses) > 0
        has_finally = bool(stmt.finally_body and len(stmt.finally_body) > 0)

        # 既无 catch 也无 finally：直接执行 try 体（不需要 setjmp）
        if not has_catch and not has_finally:
            for s in stmt.try_body:
                self._gen_statement(s)
            return

        end_lab = self.new_label('try_end')
        try_lab = self.new_label('try_body')

        if has_catch:
            dispatch_catch_lab = self.new_label('catch_dispatch')
        else:
            dispatch_catch_lab = self.new_label('catch_dispatch')

        if has_finally:
            finally_lab = self.new_label('finally_body')
            finally_from_try_lab = self.new_label('finally_from_try')

        # 获取 jmp_buf 指针
        jmp_buf_ptr = self.new_register()
        self.emit(f'{jmp_buf_ptr} = call ptr @dv_try_push()')

        # 内联调用 setjmp（平台相关）
        if self.is_windows:
            frame_addr = self.new_register()
            setjmp_result = self.new_register()
            self.emit(f'{frame_addr} = call ptr @llvm.frameaddress.p0(i32 0)')
            self.emit(f'{setjmp_result} = call i32 @_setjmp(ptr {jmp_buf_ptr}, ptr {frame_addr})')
        else:
            setjmp_result = self.new_register()
            self.emit(f'{setjmp_result} = call i32 @setjmp(ptr {jmp_buf_ptr})')

        cmp = self.new_register()
        self.emit(f'{cmp} = icmp ne i32 {setjmp_result}, 0')
        self.emit(f'br i1 {cmp}, label %{dispatch_catch_lab}, label %{try_lab}')

        # ---- try 块 ----
        self.emit(f'{try_lab}:')
        for s in stmt.try_body:
            self._gen_statement(s)
        if not self._ends_with_terminator(stmt.try_body):
            self.emit(f'call void @dv_try_pop()')
            if has_finally:
                self.emit(f'br label %{finally_from_try_lab}')
            else:
                self.emit(f'br label %{end_lab}')

        # ---- catch 分发 ----
        if has_catch:
            self.emit(f'{dispatch_catch_lab}:')
            self.emit(f'call void @dv_try_pop()')
            
            # 获取当前异常对象
            exc_slot = self._new_dv_slot()
            self.emit(f'call void @dv_get_current_exception(ptr {exc_slot})')
            
            # 生成多个 catch 块的匹配逻辑
            catch_end_lab = self.new_label('catch_end')
            next_catch_labs = []
            
            for i, clause in enumerate(catch_clauses):
                catch_lab = self.new_label(f'catch_{i}')
                if i < len(catch_clauses) - 1:
                    next_catch_lab = self.new_label(f'catch_next_{i}')
                else:
                    next_catch_lab = catch_end_lab
                next_catch_labs.append(next_catch_lab)
                
                if clause.catch_type:
                    # 有类型过滤：检查异常类型是否匹配
                    type_reg = self.gen_string_constant(clause.catch_type)
                    match_result = self.new_register()
                    self.emit(f'{match_result} = call i32 @dv_exception_match(ptr {exc_slot}, ptr {type_reg})')
                    cmp_match = self.new_register()
                    self.emit(f'{cmp_match} = icmp ne i32 {match_result}, 0')
                    self.emit(f'br i1 {cmp_match}, label %{catch_lab}, label %{next_catch_lab}')
                else:
                    # 无类型过滤：直接匹配（捕获所有）
                    self.emit(f'br label %{catch_lab}')
                
                # catch 块体
                self.emit(f'{catch_lab}:')
                if clause.catch_var:
                    self.alloca_local(clause.catch_var)
                    exc_val = self._load_dv(exc_slot)
                    self.set_var(clause.catch_var, exc_val)
                for s in clause.catch_body:
                    self._gen_statement(s)
                if has_finally:
                    self.emit(f'br label %{finally_lab}')
                else:
                    self.emit(f'br label %{end_lab}')
                
                # 下一个 catch 块的入口（如果不是最后一个）
                if i < len(catch_clauses) - 1:
                    self.emit(f'{next_catch_lab}:')
            
            # catch 全部不匹配：重新抛出异常
            self.emit(f'{catch_end_lab}:')
            if has_finally:
                self.emit(f'br label %{finally_lab}')
            else:
                # 没有 finally，重新抛出异常向外层传播
                self.emit(f'call void @dv_throw_exception(ptr {exc_slot})')
                self.emit(f'br label %{end_lab}')
        else:
            # 无 catch 但有 finally：异常先执行 finally，然后重新抛出
            self.emit(f'{dispatch_catch_lab}:')
            self.emit(f'call void @dv_try_pop()')
            self.emit(f'br label %{finally_lab}')

        # ---- finally 块 ----
        if has_finally:
            # 从 try 块正常进入 finally
            self.emit(f'{finally_from_try_lab}:')
            self.emit(f'br label %{finally_lab}')

            self.emit(f'{finally_lab}:')
            for s in stmt.finally_body:
                self._gen_statement(s)

            if has_catch:
                # 有 catch 时，finally 后直接结束
                self.emit(f'br label %{end_lab}')
            else:
                # 无 catch 时，finally 执行完重新抛出异常（向外层传播）
                exc_slot = self._new_dv_slot()
                self.emit(f'call void @dv_get_current_exception(ptr {exc_slot})')
                self.emit(f'call void @dv_throw_exception(ptr {exc_slot})')
                self.emit(f'br label %{end_lab}')

        self.emit(f'{end_lab}:')

    def _gen_typed_throw(self, stmt):
        """生成抛出异常语句"""
        dv_val, _ = self._gen_expression(stmt.value)
        slot = self._store_dv(dv_val)
        self.emit(f'call void @dv_throw_exception(ptr {slot})')

    def _collect_segment(self, seg):
        """覆盖父类方法：在收集阶段预先注册所有段名"""
        raw_name = seg.name.name if hasattr(seg.name, 'name') else str(seg.name)
        params = [(p.name, p.default_value) for p in seg.parameters]
        self._segments[raw_name] = params
        self._segment_order.append(raw_name)
        self._segment_bodies[raw_name] = seg.body
        # 预先注册到 _func_name_map，确保 f# 编号稳定
        self._safe_func_name(raw_name)

    def _collect_statement(self, stmt):
        """覆盖父类方法"""
        super()._collect_statement(stmt)

    def _collect_class(self, cls_def):
        """收集类定义"""
        self._classes[cls_def.name] = cls_def

    def _get_method_type(self, method_def) -> str:
        """判断方法类型：'instance' | 'class' | 'static'
        
        通过方法名前缀识别：
        - 以 '类' 开头 → 类方法
        - 以 '静' 开头 → 静态方法
        - 否则 → 实例方法
        """
        name = method_def.name if hasattr(method_def, 'name') else str(method_def)
        if name.startswith('类'):
            return 'class'
        if name.startswith('静'):
            return 'static'
        if getattr(method_def, 'is_static', False):
            return 'static'
        return 'instance'

    def _gen_typed_segment_call(self, name: str, args: List[str]) -> Tuple[str, str]:
        safe = self._safe_func_name(name)
        arg_strs = [f'{DUANVALUE_STRUCT} {a}' for a in args]
        reg = self.new_register()
        self.emit(f'{reg} = call {DUANVALUE_STRUCT} @_seg_{safe}({", ".join(arg_strs)})')
        return reg, 'dv'

    def _gen_typed_index_access(self, expr) -> Tuple[str, str]:
        obj_dv, _ = self._gen_expression(expr.obj)
        if isinstance(expr.index, ast.NumberLiteral):
            idx_val = int(expr.index.value)
            i64_reg = f'{idx_val}'
        else:
            idx_dv, _ = self._gen_expression(expr.index)
            i64_reg = self.new_register()
            self.emit(f'{i64_reg} = extractvalue {DUANVALUE_STRUCT} {idx_dv}, 1')
        return self._call_dv_func('dv_list_get', obj_dv, f'i64 {i64_reg}'), 'dv'

    def _gen_typed_list_literal(self, expr) -> Tuple[str, str]:
        list_dv = self._call_dv_func('dv_list_new')
        list_slot = self._new_dv_slot()
        self.emit(f'store {DUANVALUE_STRUCT} {list_dv}, ptr {list_slot}')
        for elem in expr.elements:
            elem_dv, _ = self._gen_expression(elem)
            cur = self.new_register()
            self.emit(f'{cur} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
            new_list = self._call_dv_func('dv_list_append', cur, elem_dv)
            self.emit(f'store {DUANVALUE_STRUCT} {new_list}, ptr {list_slot}')
        final = self.new_register()
        self.emit(f'{final} = load {DUANVALUE_STRUCT}, ptr {list_slot}')
        return final, 'dv'

    def _gen_typed_conditional(self, expr) -> Tuple[str, str]:
        cond_dv, _ = self._gen_expression(expr.condition)
        zero_dv = self._create_int_dv('0')
        cond_slot = self._store_dv(cond_dv)
        zero_slot = self._store_dv(zero_dv)
        eq = self.new_register()
        self.emit(f'{eq} = call i32 @dv_eq(ptr {cond_slot}, ptr {zero_slot})')
        final = self.new_register()
        self.emit(f'{final} = icmp ne i32 {eq}, 0')

        then_lab = self.new_label('cond_then')
        else_lab = self.new_label('cond_else')
        end_lab = self.new_label('cond_end')
        result_slot = self._new_dv_slot()
        self.emit(f'br i1 {final}, label %{else_lab}, label %{then_lab}')

        self.emit(f'{then_lab}:')
        then_dv, _ = self._gen_expression(expr.then_expr)
        self.emit(f'store {DUANVALUE_STRUCT} {then_dv}, ptr {result_slot}')
        self.emit(f'br label %{end_lab}')

        self.emit(f'{else_lab}:')
        else_dv, _ = self._gen_expression(expr.else_expr)
        self.emit(f'store {DUANVALUE_STRUCT} {else_dv}, ptr {result_slot}')
        self.emit(f'br label %{end_lab}')

        self.emit(f'{end_lab}:')
        loaded = self.new_register()
        self.emit(f'{loaded} = load {DUANVALUE_STRUCT}, ptr {result_slot}')
        return loaded, 'dv'

    # ============================================================
    # 语句生成（重写，使用 DuanValue）
    # ============================================================

    def _gen_statement(self, stmt):
        if stmt is None:
            return
        if isinstance(stmt, ast.VariableDeclaration):
            self._gen_typed_var_decl(stmt)
        elif isinstance(stmt, ast.Assignment):
            self._gen_typed_assignment(stmt)
        elif hasattr(ast, 'SelfAssignment') and isinstance(stmt, ast.SelfAssignment):
            self._gen_typed_self_assignment(stmt)
        elif isinstance(stmt, ast.CompoundAssignment):
            self._gen_typed_compound_assignment(stmt)
        elif isinstance(stmt, ast.IfStatement):
            self._gen_typed_if(stmt)
        elif isinstance(stmt, ast.ForeachStatement):
            self._gen_typed_foreach(stmt)
        elif isinstance(stmt, ast.WhileStatement):
            self._gen_typed_while(stmt)
        elif isinstance(stmt, ast.ReturnStatement):
            self._gen_typed_return(stmt)
        elif isinstance(stmt, ast.BreakStatement):
            super()._gen_break(stmt)
        elif isinstance(stmt, ast.ContinueStatement):
            super()._gen_continue(stmt)
        elif isinstance(stmt, ast.PrintStatement):
            self._gen_typed_print(stmt)
        elif isinstance(stmt, ast.TryStatement):
            self._gen_typed_try(stmt)
        elif isinstance(stmt, ast.ThrowStatement):
            self._gen_typed_throw(stmt)
        elif isinstance(stmt, ast.ExpressionStatement):
            expr = stmt.expression
            if isinstance(expr, ast.FunctionCall) and isinstance(expr.name, ast.PropertyAccess):
                method_name = expr.name.property_name
                obj = expr.name.obj
                if isinstance(obj, ast.Identifier):
                    obj_name = obj.name
                    mutating_methods = {'追加', 'append', '清空', 'clear', '设置', 'set', '插入', 'insert', '删除', 'remove', '弹出', 'pop'}
                    if method_name in mutating_methods:
                        result_dv, _ = self._gen_expression(expr)
                        self.set_var(obj_name, result_dv)
                        return
            self._gen_expression(expr)
        elif isinstance(stmt, ast.ImportStatement):
            pass

    def _gen_typed_var_decl(self, stmt: ast.VariableDeclaration):
        self.alloca_local(stmt.name)
        if stmt.value:
            dv_val, _ = self._gen_expression(stmt.value)
        else:
            dv_val = self._create_int_dv('0')
        self.set_var(stmt.name, dv_val)

    def _gen_typed_assignment(self, stmt: ast.Assignment):
        if isinstance(stmt.target, ast.PropertyAccess):
            obj_dv, _ = self._gen_expression(stmt.target.obj)
            member = stmt.target.property_name
            value_dv, _ = self._gen_expression(stmt.value)
            obj_slot = self._store_dv(obj_dv)
            member_reg = self.gen_string_constant(member)
            value_slot = self._store_dv(value_dv)
            self.emit(f'call void @dv_class_set_member(ptr {obj_slot}, ptr {member_reg}, ptr {value_slot})')
            if isinstance(stmt.target.obj, ast.Identifier):
                obj_name = stmt.target.obj.name
                updated_dv = self._load_dv(obj_slot)
                self.set_var(obj_name, updated_dv)
        elif isinstance(stmt.target, ast.Identifier):
            name = stmt.target.name
            # 方法内部：self.xxx 赋值
            if self._method_result_ptr is not None and name.startswith('self.') and len(name) > 5:
                attr_name = name[5:]
                self_dv = self.get_var('己')
                if self_dv is not None:
                    value_dv, _ = self._gen_expression(stmt.value)
                    obj_slot = self._store_dv(self_dv)
                    member_reg = self.gen_string_constant(attr_name)
                    value_slot = self._store_dv(value_dv)
                    self.emit(f'call void @dv_class_set_member(ptr {obj_slot}, ptr {member_reg}, ptr {value_slot})')
                    updated_dv = self._load_dv(obj_slot)
                    self.set_var('己', updated_dv)
                    return
            # 方法内部：己xxx 赋值
            if self._method_result_ptr is not None and name.startswith('己') and len(name) > 1:
                attr_name = name[1:]
                self_dv = self.get_var('己')
                if self_dv is not None:
                    value_dv, _ = self._gen_expression(stmt.value)
                    obj_slot = self._store_dv(self_dv)
                    member_reg = self.gen_string_constant(attr_name)
                    value_slot = self._store_dv(value_dv)
                    self.emit(f'call void @dv_class_set_member(ptr {obj_slot}, ptr {member_reg}, ptr {value_slot})')
                    updated_dv = self._load_dv(obj_slot)
                    self.set_var('己', updated_dv)
                    return
            name = self._get_var_name(stmt.target)
            dv_val, _ = self._gen_expression(stmt.value)
            self.set_var(name, dv_val)
        else:
            name = self._get_var_name(stmt.target)
            dv_val, _ = self._gen_expression(stmt.value)
            self.set_var(name, dv_val)

    def _gen_typed_self_assignment(self, stmt):
        """生成 SelfAssignment 语句（己.属性名 为 值）"""
        self_dv = self.get_var('己')
        if self_dv is None:
            return
        attr_name = stmt.attr_name if hasattr(stmt, 'attr_name') else ''
        value_dv, _ = self._gen_expression(stmt.value)
        obj_slot = self._store_dv(self_dv)
        member_reg = self.gen_string_constant(attr_name)
        value_slot = self._store_dv(value_dv)
        self.emit(f'call void @dv_class_set_member(ptr {obj_slot}, ptr {member_reg}, ptr {value_slot})')
        updated_dv = self._load_dv(obj_slot)
        self.set_var('己', updated_dv)

    def _gen_typed_compound_assignment(self, stmt: ast.CompoundAssignment):
        name = self._get_var_name(stmt.target)
        cur = self.get_var(name)
        if cur is None:
            return
        val_dv, _ = self._gen_expression(stmt.value)
        op_map = {'加': 'dv_add', '减': 'dv_sub', '乘': 'dv_mul', '除': 'dv_div'}
        func = op_map.get(stmt.operator, 'dv_add')
        result = self._call_dv_func(func, cur, val_dv)
        self.set_var(name, result)

    def _gen_typed_if(self, stmt: ast.IfStatement):
        cond_dv, _ = self._gen_expression(stmt.condition)
        # 条件为假/零 → 跳转 else
        zero_dv = self._create_int_dv('0')
        cond_slot = self._store_dv(cond_dv)
        zero_slot = self._store_dv(zero_dv)
        eq = self.new_register()
        self.emit(f'{eq} = call i32 @dv_eq(ptr {cond_slot}, ptr {zero_slot})')
        final = self.new_register()
        self.emit(f'{final} = icmp ne i32 {eq}, 0')

        then_lab = self.new_label('then')
        end_lab = self.new_label('endif')
        else_lab = self.new_label('else') if stmt.else_body else end_lab

        elseif_labs = [self.new_label('elseif') for _ in stmt.elseif_conditions]

        next_lab = elseif_labs[0] if elseif_labs else else_lab
        self.emit(f'br i1 {final}, label %{next_lab}, label %{then_lab}')

        self.emit(f'{then_lab}:')
        for s in stmt.then_body:
            self._gen_statement(s)
        if not self._ends_with_terminator(stmt.then_body):
            self.emit(f'br label %{end_lab}')

        for idx, (eif_cond, eif_body) in enumerate(zip(stmt.elseif_conditions, stmt.elseif_bodies)):
            eif_lab = elseif_labs[idx]
            next_l = elseif_labs[idx + 1] if idx + 1 < len(elseif_labs) else else_lab
            self.emit(f'{eif_lab}:')
            c_dv, _ = self._gen_expression(eif_cond)
            c_slot = self._store_dv(c_dv)
            z_slot = self._store_dv(zero_dv)
            z = self.new_register()
            self.emit(f'{z} = call i32 @dv_eq(ptr {c_slot}, ptr {z_slot})')
            f = self.new_register()
            self.emit(f'{f} = icmp ne i32 {z}, 0')
            e_then = self.new_label('eif_then')
            self.emit(f'br i1 {f}, label %{next_l}, label %{e_then}')
            self.emit(f'{e_then}:')
            for s in eif_body:
                self._gen_statement(s)
            if not self._ends_with_terminator(eif_body):
                self.emit(f'br label %{end_lab}')

        if stmt.else_body:
            self.emit(f'{else_lab}:')
            for s in stmt.else_body:
                self._gen_statement(s)
            if not self._ends_with_terminator(stmt.else_body):
                self.emit(f'br label %{end_lab}')

        self.emit(f'{end_lab}:')

    def _gen_typed_foreach(self, stmt: ast.ForeachStatement):
        var_name = stmt.variable if isinstance(stmt.variable, str) else str(stmt.variable)
        self.alloca_local(var_name)
        list_dv, _ = self._gen_expression(stmt.iterable)

        idx_slot = self.new_register()
        self.emit(f'{idx_slot} = alloca i64')
        self.emit(f'store i64 0, ptr {idx_slot}')

        slot = self._store_dv(list_dv)
        len_val = self.new_register()
        self.emit(f'{len_val} = call i64 @dv_list_len(ptr {slot})')

        loop_lab = self.new_label('foreach_loop')
        body_lab = self.new_label('foreach_body')
        end_lab = self.new_label('foreach_end')
        self._loop_break_labels.append(end_lab)
        self._loop_continue_labels.append(loop_lab)
        self.emit(f'br label %{loop_lab}')

        self.emit(f'{loop_lab}:')
        i = self.new_register()
        self.emit(f'{i} = load i64, ptr {idx_slot}')
        cmp = self.new_register()
        self.emit(f'{cmp} = icmp slt i64 {i}, {len_val}')
        self.emit(f'br i1 {cmp}, label %{body_lab}, label %{end_lab}')

        self.emit(f'{body_lab}:')
        elem = self._call_dv_func('dv_list_get', list_dv, f'i64 {i}')
        self.set_var(var_name, elem)
        for s in stmt.body:
            self._gen_statement(s)
        if not self._ends_with_terminator(stmt.body):
            next_i = self.new_register()
            self.emit(f'{next_i} = add i64 {i}, 1')
            self.emit(f'store i64 {next_i}, ptr {idx_slot}')
            self.emit(f'br label %{loop_lab}')

        self.emit(f'{end_lab}:')
        self._loop_break_labels.pop()
        self._loop_continue_labels.pop()

    def _gen_typed_while(self, stmt: ast.WhileStatement):
        cond_lab = self.new_label('while_cond')
        body_lab = self.new_label('while_body')
        end_lab = self.new_label('while_end')
        self._loop_break_labels.append(end_lab)
        self._loop_continue_labels.append(cond_lab)
        self.emit(f'br label %{cond_lab}')

        self.emit(f'{cond_lab}:')
        cond_dv, _ = self._gen_expression(stmt.condition)
        zero_dv = self._create_int_dv('0')
        cond_slot = self._store_dv(cond_dv)
        zero_slot = self._store_dv(zero_dv)
        eq = self.new_register()
        self.emit(f'{eq} = call i32 @dv_eq(ptr {cond_slot}, ptr {zero_slot})')
        final = self.new_register()
        self.emit(f'{final} = icmp ne i32 {eq}, 0')
        self.emit(f'br i1 {final}, label %{end_lab}, label %{body_lab}')

        self.emit(f'{body_lab}:')
        for s in stmt.body:
            self._gen_statement(s)
        self.emit(f'br label %{cond_lab}')

        self.emit(f'{end_lab}:')
        self._loop_break_labels.pop()
        self._loop_continue_labels.pop()

    def _gen_typed_return(self, stmt: ast.ReturnStatement):
        if self._method_result_ptr is not None:
            # 把己变量写回 self（仅非静态方法）
            if self._current_method_type != 'static':
                self_var_slot = self._local_vars.get('己')
                if self_var_slot is not None:
                    self_dv = self.new_register()
                    self.emit(f'{self_dv} = load {DUANVALUE_STRUCT}, ptr {self_var_slot}')
                    self.emit(f'store {DUANVALUE_STRUCT} {self_dv}, ptr %self')
            if stmt.value:
                dv_val, _ = self._gen_expression(stmt.value)
                self.emit(f'store {DUANVALUE_STRUCT} {dv_val}, ptr {self._method_result_ptr}')
            else:
                self.emit(f'call void @dv_null(ptr {self._method_result_ptr})')
            self.emit('call void @dv_stack_pop()')
            self.emit('ret void')
        else:
            if stmt.value:
                dv_val, _ = self._gen_expression(stmt.value)
                self.emit('call void @dv_stack_pop()')
                self.emit(f'ret {DUANVALUE_STRUCT} {dv_val}')
            else:
                null_dv = self._call_dv_func('dv_null')
                self.emit('call void @dv_stack_pop()')
                self.emit(f'ret {DUANVALUE_STRUCT} {null_dv}')

    def _gen_typed_print(self, stmt: ast.PrintStatement):
        if stmt.value:
            dv_val, _ = self._gen_expression(stmt.value)
            slot = self._store_dv(dv_val)
            self.emit(f'call void @dv_println(ptr {slot})')
        else:
            null_slot = self._new_dv_slot()
            self.emit(f'call void @dv_null(ptr {null_slot})')
            self.emit(f'call void @dv_println(ptr {null_slot})')

    # ============================================================
    # 全局初始化
    # ============================================================

    def _gen_builtin_exception_classes(self):
        """注册内置异常类"""
        builtin_exceptions = [
            ("异常", "", ["消息", "类型", "栈追踪", "原因"]),
            ("运行时异常", "异常", []),
            ("值异常", "异常", []),
            ("索引异常", "异常", []),
            ("类型异常", "异常", []),
            ("IO异常", "异常", []),
            ("内存异常", "异常", []),
            ("算术异常", "异常", []),
            ("Exception", "", ["消息", "类型", "栈追踪", "原因"]),
            ("RuntimeException", "Exception", []),
            ("ValueError", "Exception", []),
            ("IndexError", "Exception", []),
            ("TypeError", "Exception", []),
            ("IOException", "Exception", []),
            ("MemoryError", "Exception", []),
            ("ArithmeticError", "Exception", []),
        ]
        
        for cls_name, super_name, attrs in builtin_exceptions:
            name_reg = self.gen_string_constant(cls_name)
            super_reg = self.gen_string_constant(super_name)
            _ = self.new_register()
            self.emit(f'{_} = call i32 @dv_register_class(ptr {name_reg}, ptr {super_reg})')
            
            for attr in attrs:
                attr_reg = self.gen_string_constant(attr)
                _ = self.new_register()
                self.emit(f'{_} = call i32 @dv_register_attr(ptr {name_reg}, ptr {attr_reg})')

    def _gen_global_init(self):
        self._current_func = '__init__'
        self._local_vars.clear()
        self._pending_allocas = []
        self._reg_counter = 0
        self.emit(f'define void @__duan_init() {{')
        self.emit('entry:')

        self._collect_vars_from_stmts(self._module_statements)
        for vname in self._local_vars.keys():
            reg = self.new_register()
            self.emit(f'{reg} = alloca {DUANVALUE_STRUCT}')
            self._local_vars[vname] = reg

        # 注册内置异常类
        self._gen_builtin_exception_classes()

        # 注册所有类
        for cls_name, cls_def in self._classes.items():
            name_reg = self.gen_string_constant(cls_name)
            # 目前只支持单继承，取第一个父类
            super_name = cls_def.superclasses[0] if cls_def.superclasses else ""
            super_reg = self.gen_string_constant(super_name)
            _ = self.new_register()
            self.emit(f'{_} = call i32 @dv_register_class(ptr {name_reg}, ptr {super_reg})')
            
            # 注册属性
            for attr in cls_def.fields:
                attr_reg = self.gen_string_constant(attr.name)
                _ = self.new_register()
                self.emit(f'{_} = call i32 @dv_register_attr(ptr {name_reg}, ptr {attr_reg})')
            
            # 注册方法
            methods = getattr(cls_def, 'methods', []) or []
            for method in methods:
                method_name_reg = self.gen_string_constant(method.name)
                method_safe_name = f'_method_{self._safe_func_name(cls_name)}_{self._safe_func_name(method.name)}'
                method_type = self._get_method_type(method)
                _ = self.new_register()
                if method_type == 'class':
                    self.emit(f'{_} = call i32 @dv_register_class_method(ptr {name_reg}, ptr {method_name_reg}, ptr @{method_safe_name})')
                elif method_type == 'static':
                    self.emit(f'{_} = call i32 @dv_register_static_method(ptr {name_reg}, ptr {method_name_reg}, ptr @{method_safe_name})')
                else:
                    self.emit(f'{_} = call i32 @dv_register_method(ptr {name_reg}, ptr {method_name_reg}, ptr @{method_safe_name})')
            
            # 注册构造函数（方法名与类名相同）
            constructor = getattr(cls_def, 'constructor', None)
            if constructor is not None:
                ctor_name_reg = self.gen_string_constant(cls_name)
                ctor_safe_name = f'_method_{self._safe_func_name(cls_name)}_{self._safe_func_name(cls_name)}'
                _ = self.new_register()
                self.emit(f'{_} = call i32 @dv_register_method(ptr {name_reg}, ptr {ctor_name_reg}, ptr @{ctor_safe_name})')

        for stmt in self._module_statements:
            self._gen_global_statement(stmt)

        self.emit('ret void')
        self.emit('}')
        self.emit_blank()

    def _gen_global_statement(self, stmt):
        if isinstance(stmt, ast.VariableDeclaration):
            name = stmt.name
            if name and name in self._globals:
                if stmt.value:
                    dv_val, _ = self._gen_expression(stmt.value)
                    safe = self._safe_var_name(name)
                    slot_alloc = self._new_dv_slot()
                    # For globals, store DuanValue in a global struct
                    self.emit(f'store {DUANVALUE_STRUCT} {dv_val}, {DUANVALUE_STRUCT}* @__var_{safe}')
                return
        self._gen_statement(stmt)

    def gen_global_var(self, name, init_value=''):
        """覆盖：全局变量存 DuanValue"""
        self._globals[name] = init_value

    # ============================================================
    # 段落函数生成
    # ============================================================

    def _gen_typed_segment(self, name, params, body):
        self._current_func = name
        self._current_func_params = {}
        self._local_vars.clear()
        self._pending_allocas = []
        self._reg_counter = 0
        safe = self._safe_func_name(name)

        param_strs = []
        for i, (pname, default) in enumerate(params):
            reg = f'%__param_{i}'
            self._current_func_params[pname] = reg
            param_strs.append(f'{DUANVALUE_STRUCT} {reg}')

        self.emit(f'define {DUANVALUE_STRUCT} @_seg_{safe}({", ".join(param_strs)}) {{')
        self.emit('entry:')

        # 栈追踪：函数入口压栈
        func_name_ptr = self.gen_string_constant(name)
        file_name_ptr = self.gen_string_constant("")
        self.emit(f'call void @dv_stack_push(ptr {func_name_ptr}, ptr {file_name_ptr}, i32 0)')

        self._collect_vars_from_stmts(body)
        for vname in self._local_vars.keys():
            reg = self.new_register()
            self.emit(f'{reg} = alloca {DUANVALUE_STRUCT}')
            self._local_vars[vname] = reg

        for stmt in body:
            self._gen_statement(stmt)

        if not self._ends_with_terminator(body):
            null_dv = self._call_dv_func('dv_null')
            self.emit('call void @dv_stack_pop()')
            self.emit(f'ret {DUANVALUE_STRUCT} {null_dv}')
        self.emit('}')
        self.emit_blank()

    def _gen_typed_class_methods(self, class_name, cls_def):
        """生成类的所有方法"""
        methods = getattr(cls_def, 'methods', []) or []
        for method in methods:
            self._gen_typed_method(class_name, method)
        constructor = getattr(cls_def, 'constructor', None)
        if constructor is not None:
            self._gen_typed_constructor(class_name, constructor)

    def _gen_typed_method(self, class_name, method_def):
        """生成单个方法函数
        
        根据方法类型生成不同签名：
        - 实例方法: void @_method_xxx(ptr result, ptr self, ptr args, i32 num_args)
        - 类方法: void @_method_xxx(ptr result, ptr cls_val, ptr args, i32 num_args)
        - 静态方法: void @_method_xxx(ptr result, ptr args, i32 num_args)
        """
        method_type = self._get_method_type(method_def)
        self._current_func = f'{class_name}.{method_def.name}'
        self._current_func_params = {}
        self._local_vars.clear()
        self._pending_allocas = []
        self._reg_counter = 0
        self._method_result_ptr = '%result'
        self._current_class = class_name
        self._current_method_type = method_type

        method_safe_name = f'_method_{self._safe_func_name(class_name)}_{self._safe_func_name(method_def.name)}'

        if method_type == 'static':
            self.emit(f'define void @{method_safe_name}(ptr %result, ptr %args, i32 %num_args) {{')
        else:
            self.emit(f'define void @{method_safe_name}(ptr %result, ptr %self, ptr %args, i32 %num_args) {{')
        self.emit('entry:')

        # 栈追踪：方法入口压栈
        method_name = f'{class_name}.{method_def.name}'
        func_name_ptr = self.gen_string_constant(method_name)
        file_name_ptr = self.gen_string_constant("")
        self.emit(f'call void @dv_stack_push(ptr {func_name_ptr}, ptr {file_name_ptr}, i32 0)')

        params = getattr(method_def, 'parameters', []) or []

        self._collect_vars_from_stmts(getattr(method_def, 'body', []) or [])
        
        # 添加己（self/cls）变量（仅实例方法和类方法有）
        if method_type != 'static':
            self._local_vars['己'] = None
        # 添加方法参数
        for param in params:
            pname = param.name if hasattr(param, 'name') else str(param)
            self._local_vars[pname] = None

        for vname in self._local_vars.keys():
            reg = self.new_register()
            self.emit(f'{reg} = alloca {DUANVALUE_STRUCT}')
            self._local_vars[vname] = reg

        # 加载 self/cls 变量（仅实例方法和类方法有）
        if method_type != 'static':
            self_var_slot = self._local_vars.get('己')
            if self_var_slot is not None:
                self_dv = self.new_register()
                self.emit(f'{self_dv} = load {DUANVALUE_STRUCT}, ptr %self')
                self.emit(f'store {DUANVALUE_STRUCT} {self_dv}, ptr {self_var_slot}')

        for i, param in enumerate(params):
            pname = param.name if hasattr(param, 'name') else str(param)
            param_slot = self._local_vars.get(pname)
            if param_slot is not None:
                idx_reg = self.new_register()
                self.emit(f'{idx_reg} = sext i32 %num_args to i64')
                i_reg = self.new_register()
                self.emit(f'{i_reg} = add i64 0, {i}')
                in_bounds = self.new_register()
                self.emit(f'{in_bounds} = icmp slt i64 {i_reg}, {idx_reg}')
                then_lab = self.new_label('param_valid')
                else_lab = self.new_label('param_invalid')
                end_lab = self.new_label('param_end')
                self.emit(f'br i1 {in_bounds}, label %{then_lab}, label %{else_lab}')
                self.emit(f'{then_lab}:')
                elem_ptr = self.new_register()
                self.emit(f'{elem_ptr} = getelementptr inbounds {DUANVALUE_STRUCT}, ptr %args, i64 {i_reg}')
                param_val = self.new_register()
                self.emit(f'{param_val} = load {DUANVALUE_STRUCT}, ptr {elem_ptr}')
                self.emit(f'store {DUANVALUE_STRUCT} {param_val}, ptr {param_slot}')
                self.emit(f'br label %{end_lab}')
                self.emit(f'{else_lab}:')
                null_slot = self._new_dv_slot()
                self.emit(f'call void @dv_null(ptr {null_slot})')
                null_val = self.new_register()
                self.emit(f'{null_val} = load {DUANVALUE_STRUCT}, ptr {null_slot}')
                self.emit(f'store {DUANVALUE_STRUCT} {null_val}, ptr {param_slot}')
                self.emit(f'br label %{end_lab}')
                self.emit(f'{end_lab}:')

        for stmt in (getattr(method_def, 'body', []) or []):
            self._gen_statement(stmt)

        if not self._ends_with_terminator(getattr(method_def, 'body', []) or []):
            # 把己变量写回 self（仅实例方法和类方法有）
            if method_type != 'static':
                self_var_slot = self._local_vars.get('己')
                if self_var_slot is not None:
                    self_dv = self.new_register()
                    self.emit(f'{self_dv} = load {DUANVALUE_STRUCT}, ptr {self_var_slot}')
                    self.emit(f'store {DUANVALUE_STRUCT} {self_dv}, ptr %self')
            self.emit(f'call void @dv_null(ptr %result)')

        self.emit('ret void')
        self.emit('}')
        self.emit_blank()
        self._method_result_ptr = None
        self._current_class = None
        self._current_method_type = None

    def _gen_typed_constructor(self, class_name, constructor_def):
        """生成构造函数
        构造函数名就是类名，方法名与类名相同
        """
        original_name = constructor_def.name
        constructor_def.name = class_name
        try:
            self._gen_typed_method(class_name, constructor_def)
        finally:
            constructor_def.name = original_name

    def _gen_typed_main(self):
        self._reg_counter = 0
        self.emit(f'define i32 @main(i32 %argc, ptr %argv) {{')
        self.emit('entry:')
        self.emit('call void @dv_init_args(i32 %argc, ptr %argv)')
        self.emit('call void @__duan_init()')

        main_names = {'主程序', '主入口', 'main'}
        main_called = False

        # 检查顶层是否已经调用了主程序
        for stmt in self._module_statements:
            if isinstance(stmt, ast.ExpressionStatement):
                expr = stmt.expression
                if isinstance(expr, ast.FunctionCall):
                    call_name = None
                    if hasattr(expr, 'name'):
                        if hasattr(expr.name, 'name'):
                            call_name = expr.name.name
                        elif isinstance(expr.name, str):
                            call_name = expr.name
                    if call_name and call_name in main_names:
                        main_called = True
                        break

        # 如果顶层没有调用主程序，但定义了主程序段落，则调用它
        if not main_called:
            for name in main_names:
                if name in self._segments:
                    params = self._segments[name]
                    safe = self._safe_func_name(name)
                    if params:
                        slot = self._new_dv_slot()
                        self.emit(f'call void @dv_null(ptr {slot})')
                        obj_val = self.new_register()
                        self.emit(f'{obj_val} = load {DUANVALUE_STRUCT}, ptr {slot}')
                        self.emit(f'call {DUANVALUE_STRUCT} @_seg_{safe}({DUANVALUE_STRUCT} {obj_val})')
                    else:
                        self.emit(f'call {DUANVALUE_STRUCT} @_seg_{safe}()')
                    main_called = True
                    break

        self.emit('ret i32 0')
        self.emit('}')
        self.emit_blank()

    # ============================================================
    # 变量管理（存储/加载 DuanValue）
    # ============================================================

    def get_var(self, name):
        """获取 DuanValue（覆写父类）"""
        if name in self._current_func_params:
            return self._current_func_params[name]
        if name in self._globals:
            safe = self._safe_var_name(name)
            reg = self.new_register()
            self.emit(f'{reg} = load {DUANVALUE_STRUCT}, {DUANVALUE_STRUCT}* @__var_{safe}')
            return reg
        if name in self._local_vars:
            slot = self._local_vars[name]
            reg = self.new_register()
            self.emit(f'{reg} = load {DUANVALUE_STRUCT}, ptr {slot}')
            return reg
        return None

    def set_var(self, name, value_reg):
        """设置变量（覆写父类）"""
        if name in self._globals:
            safe = self._safe_var_name(name)
            self.emit(f'store {DUANVALUE_STRUCT} {value_reg}, {DUANVALUE_STRUCT}* @__var_{safe}')
        elif name in self._local_vars:
            slot = self._local_vars[name]
            self.emit(f'store {DUANVALUE_STRUCT} {value_reg}, ptr {slot}')
        elif name in self._current_func_params:
            self._current_func_params[name] = value_reg

    # ============================================================
    # finalize - 生成全局声明（使用 DuanValue 结构体）
    # ============================================================

    def finalize(self) -> str:
        """生成最终 IR（覆写父类）"""
        lines = []
        for s in self._string_decls:
            lines.append(s)
        if self._string_decls:
            lines.append('')
        for f in sorted(self._func_decls):
            lines.append(f)
        lines.append('')
        for name in self._globals:
            safe = self._safe_var_name(name)
            lines.append(f'@__var_{safe} = global {DUANVALUE_STRUCT} zeroinitializer')
        if self._globals:
            lines.append('')
        lines.extend(self._lines)
        return '\n'.join(lines)