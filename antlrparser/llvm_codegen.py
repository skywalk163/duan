"""
段言（Duan）LLVM IR 代码生成器 - 混入类

包含具体的代码生成方法（语句、表达式、段落、类等）。
"""

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

from llvm_core import LLVMCodeGenCore


class LLVMCodeGenMixin(LLVMCodeGenCore):
    """LLVM 代码生成细节混入类"""

    # =========================================================================
    # 段落生成
    # =========================================================================

    def _generate_segment(self, seg: SegmentDefinition):
        """生成一个段落的 LLVM IR"""
        func_name = self._get_segment_name(seg.name)
        self.current_function = func_name
        self.variables = {}
        self.reg_counter = 0

        # 目前都返回 i32，后续可扩展
        self.emit(f'define i32 @{func_name}(i32 %{func_name}_args) {{')
        self.indent_level = 1

        # 为参数分配变量
        # 简化：参数通过栈传递

        # 生成函数体
        for stmt in seg.body:
            self._generate_statement(stmt)

        # 默认返回 0
        self.emit('ret i32 0')
        self.indent_level = 0
        self.emit('}')
        self.emit('')
        self.current_function = None

    # =========================================================================
    # 类生成
    # =========================================================================

    def _generate_class(self, cls: ClassDefinition):
        """生成类的 LLVM IR"""
        class_name = cls.name
        llvm_class_name = self._get_segment_name(class_name)

        # 生成构造函数（即使没有显式构造函数也生成默认的）
        ctor_name = f'{llvm_class_name}_ctor'
        self.emit(f'; 类 {class_name} 的构造函数')
        self.emit(f'define i8* @{ctor_name}(i32 %args) {{')
        self.indent_level = 1

        # 分配对象内存（简化：每个对象固定大小）
        size_reg = self.new_register()
        self.emit(f'{size_reg} = add i64 0, 1024')
        result_reg = self.new_register()
        self.emit(f'{result_reg} = call i8* @malloc(i64 {size_reg})')

        # 如果有构造函数体，生成初始化代码
        if cls.constructor and cls.constructor.body:
            self.variables = {}
            self.reg_counter = 0
            for stmt in cls.constructor.body:
                self._generate_statement(stmt)

        self.emit(f'ret i8* {result_reg}')
        self.indent_level = 0
        self.emit('}')
        self.emit('')

        # 生成类方法
        for method in cls.methods:
            # 使用类名和哈希生成唯一的方法名
            method_llvm_name = self._get_segment_name(f'{class_name}_{method.name}')
            method_name = f'{llvm_class_name}_{method.name}'
            self.emit(f'; 类 {class_name} 的方法 {method.name}')
            self.current_function = method_llvm_name
            self.variables = {}
            self.reg_counter = 0

            # 方法签名：接收 this 指针和参数
            self.emit(f'define i32 @{method_llvm_name}(i8* %this, i32 %args) {{')
            self.indent_level = 1

            # 生成方法体
            for stmt in method.body:
                self._generate_statement(stmt)

            self.emit('ret i32 0')
            self.indent_level = 0
            self.emit('}')
            self.emit('')

        self.current_function = None

    def _generate_interface(self, iface: InterfaceDefinition):
        """生成接口声明（接口不生成实现代码）"""
        self.emit(f'; 接口 {iface.name}（仅声明）')
        self.emit(f'; 父接口: {", ".join(iface.superinterfaces)}')
        for method in iface.methods:
            method_name = self._get_segment_name(f'{iface.name}_{method.name}')
            # 声明接口方法（外部链接）
            self.emit(f'declare i32 @{method_name}(i8*, ...)')
        self.emit('')

    # =========================================================================
    # 语句生成
    # =========================================================================

    def _generate_statement(self, stmt: ASTNode):
        if isinstance(stmt, VariableDeclaration):
            self._gen_var_decl(stmt)
        elif isinstance(stmt, Assignment):
            self._gen_assignment(stmt)
        elif isinstance(stmt, CompoundAssignment):
            # 复合赋值：展开为 变量 = 变量 运算符 值
            operator = stmt.operator
            op_map = {'加': 'add', '减': 'sub', '乘': 'mul', '除': 'sdiv', '模': 'srem', '幂': 'call_pow'}
            llvm_op = op_map.get(operator, 'add')
            # 获取当前变量值
            reg = self._get_or_create_var(stmt.target)
            val_reg = self._gen_expression(stmt.value)
            if llvm_op == 'call_pow':
                self._add(f"%{self.reg_counter} = call double @pow(double %{reg}, double %{val_reg})")
            else:
                self._add(f"%{self.reg_counter} = {llvm_op} i32 %{reg}, %{val_reg}")
            self.reg_counter += 1
            self._add(f"store i32 %{self.reg_counter - 1}, i32* %{reg}")
        elif isinstance(stmt, PrintStatement):
            self._gen_print(stmt)
        elif isinstance(stmt, ExpressionStatement):
            self._gen_expression(stmt.expression)
        elif isinstance(stmt, IfStatement):
            self._gen_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._gen_while(stmt)
        elif isinstance(stmt, ReturnStatement):
            self._gen_return(stmt)

    # =========================================================================
    # 变量声明
    # =========================================================================

    def _gen_var_decl(self, stmt: VariableDeclaration):
        """生成变量声明"""
        if stmt.name not in self.variables:
            reg = self.new_register()
            # 判断变量类型
            is_list = isinstance(stmt.value, ListLiteral) if stmt.value else False
            is_class = isinstance(stmt.value, NewExpression) if stmt.value else False

            if is_list or is_class:
                # 列表和类实例使用指针类型
                self.emit(f'{reg} = alloca i8*, align 8')
                if is_class:
                    self.type_info[stmt.name] = f'class_{stmt.value.class_name}'
                else:
                    self.type_info[stmt.name] = 'list'
            else:
                self.emit(f'{reg} = alloca i32, align 4')
                self.type_info[stmt.name] = 'int'
            self.variables[stmt.name] = reg

        if stmt.value:
            ptr = self.variables[stmt.name]
            val = self._gen_expression(stmt.value)
            var_type = self.type_info.get(stmt.name, 'int')
            if var_type.startswith('class_') or var_type == 'list':
                self.emit(f'store i8* {val}, i8** {ptr}, align 8')
            else:
                self.emit(f'store i32 {val}, i32* {ptr}, align 4')

    def _gen_assignment(self, stmt: Assignment):
        """生成赋值语句"""
        if isinstance(stmt.target, Identifier) and stmt.target.name in self.variables:
            ptr = self.variables[stmt.target.name]
            val = self._gen_expression(stmt.value)
            var_type = self.type_info.get(stmt.target.name, 'int')
            if var_type == 'list':
                self.emit(f'store i8* {val}, i8** {ptr}, align 8')
            else:
                self.emit(f'store i32 {val}, i32* {ptr}, align 4')

    # =========================================================================
    # 表达式生成
    # =========================================================================

    def _gen_expression(self, expr: ASTNode, is_float=False) -> str:
        """生成表达式，返回存放结果的寄存器名

        Args:
            expr: AST节点
            is_float: 是否按浮点处理
        """
        if isinstance(expr, NumberLiteral):
            # 检测浮点数
            val_str = str(expr.value)
            if '.' in val_str or 'e' in val_str.lower():
                reg = self.new_register()
                self.emit(f'{reg} = fadd double 0.0, {val_str}')
                return reg
            # 整数
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, {int(expr.value)}')
            return reg

        elif isinstance(expr, StringLiteral):
            name = self.get_string_ref(expr.value)
            if not any(name in l for l in self.lines):
                self._generate_string_global(name, expr.value)
            reg = self.new_register()
            self.emit(f'{reg} = getelementptr inbounds [{len(expr.value) + 1} x i8], [{len(expr.value) + 1} x i8]* @{name}, i32 0, i32 0')
            return reg

        elif isinstance(expr, ListLiteral):
            # 生成列表字面量
            return self._gen_list_literal(expr)

        elif isinstance(expr, DictLiteral):
            # 生成字典字面量
            return self._gen_dict_literal(expr)

        elif isinstance(expr, PropertyAccess):
            # 生成属性访问表达式
            return self._gen_property_access(expr)

        elif isinstance(expr, IndexAccess):
            # 生成索引访问表达式
            return self._gen_index_access(expr)

        elif isinstance(expr, Identifier):
            if expr.name in self.variables:
                ptr = self.variables[expr.name]
                var_type = self.type_info.get(expr.name, 'int')
                if var_type == 'list' or var_type.startswith('class_'):
                    # 列表和类实例类型加载为指针
                    reg = self.new_register()
                    self.emit(f'{reg} = load i8*, i8** {ptr}, align 8')
                    return reg
                if expr.name in self.float_vars:
                    reg = self.new_register()
                    self.emit(f'{reg} = load double, double* {ptr}, align 8')
                    return reg
                reg = self.new_register()
                self.emit(f'{reg} = load i32, i32* {ptr}, align 4')
                return reg
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        elif isinstance(expr, BinaryOp):
            # 检测是否涉及浮点数
            left_is_float = self._is_float_expression(expr.left)
            right_is_float = self._is_float_expression(expr.right)

            left = self._gen_expression(expr.left, left_is_float)
            right = self._gen_expression(expr.right, right_is_float)
            reg = self.new_register()

            # 算术运算符（支持整数和浮点）
            arith_ops_int = {'加': 'add', '减': 'sub', '乘': 'mul', '除': 'sdiv', '模': 'srem'}
            arith_ops_float = {'加': 'fadd', '减': 'fsub', '乘': 'fmul', '除': 'fdiv'}
            # 比较运算符
            cmp_ops_int = {
                '大于': 'sgt', '小于': 'slt', '等于': 'eq',
                '大于等于': 'sge', '小于等于': 'sle', '不等于': 'ne',
            }
            cmp_ops_float = {
                '大于': 'ogt', '小于': 'olt', '等于': 'oeq',
                '大于等于': 'oge', '小于等于': 'ole', '不等于': 'one',
            }

            if left_is_float or right_is_float:
                # 浮点运算
                if expr.operator in arith_ops_float:
                    op = arith_ops_float[expr.operator]
                    # 需要将整数操作数转换为浮点
                    if not left_is_float:
                        left_reg = self.new_register()
                        self.emit(f'{left_reg} = sitofp i32 {left} to double')
                        left = left_reg
                    if not right_is_float:
                        right_reg = self.new_register()
                        self.emit(f'{right_reg} = sitofp i32 {right} to double')
                        right = right_reg
                    self.emit(f'{reg} = {op} double {left}, {right}')
                elif expr.operator in cmp_ops_float:
                    op = cmp_ops_float[expr.operator]
                    if not left_is_float:
                        left_reg = self.new_register()
                        self.emit(f'{left_reg} = sitofp i32 {left} to double')
                        left = left_reg
                    if not right_is_float:
                        right_reg = self.new_register()
                        self.emit(f'{right_reg} = sitofp i32 {right} to double')
                        right = right_reg
                    cmp_reg = self.new_register()
                    self.emit(f'{cmp_reg} = fcmp {op} double {left}, {right}')
                    reg = self.new_register()
                    self.emit(f'{reg} = zext i1 {cmp_reg} to i32')
                else:
                    self.emit(f'{reg} = fadd double {left}, {right}')
            else:
                # 整数运算
                if expr.operator in arith_ops_int:
                    op = arith_ops_int[expr.operator]
                    self.emit(f'{reg} = {op} i32 {left}, {right}')
                elif expr.operator in cmp_ops_int:
                    op = cmp_ops_int[expr.operator]
                    cmp_reg = self.new_register()
                    self.emit(f'{cmp_reg} = icmp {op} i32 {left}, {right}')
                    reg = self.new_register()
                    self.emit(f'{reg} = zext i1 {cmp_reg} to i32')
                else:
                    self.emit(f'{reg} = add i32 {left}, {right}')
            return reg

        elif isinstance(expr, FunctionCall):
            # 方法调用：对象之方法()
            if isinstance(expr.name, PropertyAccess):
                return self._gen_method_call(expr)

            if isinstance(expr.name, Identifier):
                func_name = expr.name.name

                # 打印函数
                if func_name == '打印':
                    return self._gen_print_call(expr)

                # 数学函数
                math_funcs = {
                    'sin': '@sin', 'cos': '@cos', 'tan': '@tan',
                    'exp': '@exp', 'log': '@log', 'log10': '@log10',
                    'sqrt': '@sqrt', 'pow': '@pow',
                    'floor': '@floor', 'ceil': '@ceil', 'round': '@round',
                    'cbrt': '@cbrt', 'fmod': '@fmod', 'min': '@fmin', 'max': '@fmax'
                }

                if func_name in math_funcs:
                    return self._gen_math_call(expr, math_funcs[func_name])

                # 整数绝对值函数
                if func_name == 'abs':
                    return self._gen_abs_call(expr)

                # 字符串函数
                str_funcs = {
                    'len': '@strlen', 'strcmp': '@strcmp', 'strstr': '@strstr',
                    'strcpy': '@strcpy', 'strcat': '@strcat'
                }

                if func_name in str_funcs:
                    return self._gen_string_call(expr, str_funcs[func_name])

                # 列表操作函数
                list_funcs = {
                    'listAppend': '@duan_list_append',
                    'listLen': '@duan_list_length',
                    'listGet': '@duan_list_get',
                    'listSet': '@duan_list_set',
                    'listCopy': '@duan_list_copy',
                    'listFree': '@duan_list_free'
                }

                if func_name in list_funcs:
                    return self._gen_list_call(expr, list_funcs[func_name])

                # 类型转换函数
                if func_name == '_串化':
                    return self._gen_to_string_call(expr)
                if func_name == '_数化':
                    return self._gen_to_number_call(expr)

            # 处理段落调用（SegmentName）
            if isinstance(expr.name, SegmentName):
                seg_name = expr.name.name
                # 获取转换后的函数名
                llvm_func_name = self._get_segment_name(seg_name)

                # 生成参数
                arg_regs = []
                for arg in expr.arguments:
                    arg_reg = self._gen_expression(arg)
                    arg_regs.append(arg_reg)

                # 生成函数调用
                result = self.new_register()
                args_str = ', '.join([f'i32 {reg}' for reg in arg_regs])
                self.emit(f'{result} = call i32 @{llvm_func_name}(i32 0' + (f', {args_str}' if args_str else '') + ')')
                return result

            # 默认情况
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        elif isinstance(expr, BooleanLiteral):
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, {1 if expr.value else 0}')
            return reg

        elif isinstance(expr, NullLiteral):
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        elif isinstance(expr, NewExpression):
            # 类实例化：新 类名()
            return self._gen_new_expression(expr)

        return self._gen_expression(NumberLiteral(0))

    def _is_float_expression(self, expr: ASTNode) -> bool:
        """检测表达式是否为浮点类型"""
        if isinstance(expr, NumberLiteral):
            val_str = str(expr.value)
            return '.' in val_str or 'e' in val_str.lower()
        if isinstance(expr, Identifier):
            return expr.name in self.float_vars
        if isinstance(expr, BinaryOp):
            return self._is_float_expression(expr.left) or self._is_float_expression(expr.right)
        if isinstance(expr, FunctionCall):
            math_funcs = {'sin', 'cos', 'tan', 'exp', 'log', 'log10', 'sqrt', 'pow'}
            if isinstance(expr.name, Identifier) and expr.name.name in math_funcs:
                return True
        return False

    def _gen_math_call(self, expr: FunctionCall, llvm_func: str) -> str:
        """生成数学函数调用"""
        args = []
        for arg in expr.arguments:
            is_float = self._is_float_expression(arg)
            arg_reg = self._gen_expression(arg, is_float)
            if not is_float:
                # 转换为浮点
                float_reg = self.new_register()
                self.emit(f'{float_reg} = sitofp i32 {arg_reg} to double')
                args.append(float_reg)
            else:
                args.append(arg_reg)

        float_reg = self.new_register()
        if len(args) == 1:
            self.emit(f'{float_reg} = call double {llvm_func}(double {args[0]})')
        elif len(args) == 2:
            self.emit(f'{float_reg} = call double {llvm_func}(double {args[0]}, double {args[1]})')
        else:
            self.emit(f'{float_reg} = call double {llvm_func}(double 0.0)')

        # 将浮点数结果转换为整数
        result_reg = self.new_register()
        self.emit(f'{result_reg} = fptosi double {float_reg} to i32')

        return result_reg

    def _gen_list_call(self, expr: FunctionCall, llvm_func: str) -> str:
        """生成列表函数调用"""
        args = []
        for i, arg in enumerate(expr.arguments):
            arg_reg = self._gen_expression(arg)
            # 索引参数需要转换为 i64
            if llvm_func == '@duan_list_get' or llvm_func == '@duan_list_set':
                if i == 1:  # 第二个参数是索引
                    idx64 = self.new_register()
                    self.emit(f'{idx64} = zext i32 {arg_reg} to i64')
                    args.append(idx64)
                    continue
            args.append(arg_reg)

        result_reg = self.new_register()
        args_str = ', '.join([f'i32 {args[0]}' if i == 0 and llvm_func != '@duan_list_length' else f'i64 {args[i]}' if i == 1 and (llvm_func == '@duan_list_get' or llvm_func == '@duan_list_set') else f'i32 {args[i]}' for i in range(len(args))])

        if llvm_func == '@duan_list_length':
            self.emit(f'{result_reg} = call i32 {llvm_func}(i32* {args[0]})')
        elif llvm_func == '@duan_list_append':
            self.emit(f'{result_reg} = call i32 {llvm_func}(i32* {args[0]}, i32 {args[1]})')
        elif llvm_func == '@duan_list_get':
            self.emit(f'{result_reg} = call i32 {llvm_func}(i32* {args[0]}, i64 {args[1]})')
        elif llvm_func == '@duan_list_set':
            self.emit(f'call void {llvm_func}(i32* {args[0]}, i64 {args[1]}, i32 {args[2]})')
            result_reg = self.new_register()
            self.emit(f'{result_reg} = add i32 0, 0')
        else:
            self.emit(f'{result_reg} = call i32 {llvm_func}({args_str})')

        return result_reg

    def _gen_abs_call(self, expr: FunctionCall) -> str:
        """生成 abs() 调用（整数绝对值）"""
        if not expr.arguments:
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        arg = self._gen_expression(expr.arguments[0])

        # 使用条件选择指令实现整数绝对值 - 按顺序创建寄存器
        cond = self.new_register()
        neg = self.new_register()
        result = self.new_register()

        # 检查是否小于0
        self.emit(f'{cond} = icmp slt i32 {arg}, 0')
        # 计算负数
        self.emit(f'{neg} = sub i32 0, {arg}')
        # 如果小于0，返回 -arg，否则返回 arg
        self.emit(f'{result} = select i1 {cond}, i32 {neg}, i32 {arg}')

        return result

    def _gen_to_string_call(self, expr: FunctionCall) -> str:
        """生成 _串化() 调用（整数转字符串）"""
        if not expr.arguments:
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        arg = self._gen_expression(expr.arguments[0])
        # 使用 duan_itoa 函数
        result = self.new_register()
        self.emit(f'{result} = call i8* @duan_itoa(i32 {arg})')
        return result

    def _gen_to_number_call(self, expr: FunctionCall) -> str:
        """生成 _数化() 调用（字符串转整数）"""
        if not expr.arguments:
            reg = self.new_register()
            self.emit(f'{reg} = add i32 0, 0')
            return reg

        arg = self._gen_expression(expr.arguments[0])
        # 使用 atoi 函数
        result = self.new_register()
        self.emit(f'{result} = call i32 @atoi(i8* {arg})')
        return result

    def _gen_new_expression(self, expr: NewExpression) -> str:
        """生成类实例化表达式（新 类名()）"""
        class_name = expr.class_name
        llvm_class_name = self._get_segment_name(class_name)
        ctor_name = f'{llvm_class_name}_ctor'

        # 生成构造函数参数
        args_str = ''
        if expr.arguments:
            arg_regs = []
            for arg in expr.arguments:
                arg_reg = self._gen_expression(arg)
                arg_regs.append(arg_reg)
            args_str = ', ' + ', '.join([f'i32 {reg}' for reg in arg_regs])

        # 调用构造函数
        result = self.new_register()
        self.emit(f'{result} = call i8* @{ctor_name}(i32 0{args_str})')

        return result

    def _gen_method_call(self, expr: FunctionCall) -> str:
        """生成方法调用：对象之方法()"""
        prop_access = expr.name
        # 生成对象表达式（this 指针）
        this_reg = self._gen_expression(prop_access.obj)

        # 获取类名（简化：假设对象是类实例，通过类型信息获取类名）
        class_name = self._get_class_name_from_expr(prop_access.obj)
        method_name = prop_access.property_name

        # 生成方法名（使用哈希确保是有效的 LLVM 标识符）
        if class_name:
            full_method_name = f'{class_name}_{method_name}'
            llvm_method_name = self._get_segment_name(full_method_name)
        else:
            llvm_method_name = f'obj_{method_name}'

        # 生成方法参数
        arg_regs = []
        for arg in expr.arguments:
            arg_reg = self._gen_expression(arg)
            arg_regs.append(arg_reg)

        # 生成方法调用
        result = self.new_register()
        args_str = ', '.join([f'i32 {reg}' for reg in arg_regs])
        if args_str:
            self.emit(f'{result} = call i32 @{llvm_method_name}(i8* {this_reg}, i32 0, {args_str})')
        else:
            self.emit(f'{result} = call i32 @{llvm_method_name}(i8* {this_reg}, i32 0)')

        return result

    def _get_class_name_from_expr(self, expr: ASTNode) -> Optional[str]:
        """从表达式获取类名（简化实现）"""
        if isinstance(expr, Identifier):
            # 尝试从类型信息中获取类名
            var_type = self.type_info.get(expr.name)
            if var_type and var_type.startswith('class_'):
                return var_type[6:]
            # 默认返回变量名作为类名（简化假设）
            return expr.name
        return None

    def _gen_string_call(self, expr: FunctionCall, llvm_func: str) -> str:
        """生成字符串函数调用"""
        args = []
        for arg in expr.arguments:
            arg_reg = self._gen_expression(arg)
            args.append(arg_reg)

        result_reg = self.new_register()
        if llvm_func == '@strlen':
            self.emit(f'{result_reg} = call i32 {llvm_func}(i8* {args[0]})')
        elif llvm_func == '@strcmp':
            self.emit(f'{result_reg} = call i32 {llvm_func}(i8* {args[0]}, i8* {args[1]})')
        elif llvm_func == '@strstr':
            self.emit(f'{result_reg} = call i8* {llvm_func}(i8* {args[0]}, i8* {args[1]})')
        else:
            self.emit(f'{result_reg} = add i32 0, 0')

        return result_reg

    # =========================================================================
    # 打印语句
    # =========================================================================

    def _gen_print(self, stmt: PrintStatement):
        """生成打印语句"""
        # 判断是否是字符串字面量
        if isinstance(stmt.value, StringLiteral):
            # 字符串使用 puts 打印
            val = self._gen_expression(stmt.value)
            creg = self.new_register()
            self.emit(f'{creg} = call i32 @puts(i8* {val})')
        else:
            # 其他类型使用 printf 打印整数
            val = self._gen_expression(stmt.value)
            self._add_global('.printf_fmt', '[4 x i8] c"%d\\0A\\00"')
            reg = self.new_register()
            self.emit(f'{reg} = getelementptr inbounds [4 x i8], [4 x i8]* @.printf_fmt, i32 0, i32 0')
            creg = self.new_register()
            self.emit(f'{creg} = call i32 (i8*, ...) @printf(i8* {reg}, i32 {val})')

    def _gen_print_call(self, expr: FunctionCall) -> str:
        """处理 打印() 调用表达式"""
        for arg in expr.arguments:
            # 判断是否是字符串字面量
            if isinstance(arg, StringLiteral):
                # 字符串使用 puts 打印
                val = self._gen_expression(arg)
                creg = self.new_register()
                self.emit(f'{creg} = call i32 @puts(i8* {val})')
            else:
                # 其他类型使用 printf 打印整数
                self._add_global('.printf_fmt', '[4 x i8] c"%d\\0A\\00"')
                reg_fmt = self.new_register()
                self.emit(f'{reg_fmt} = getelementptr inbounds [4 x i8], [4 x i8]* @.printf_fmt, i32 0, i32 0')
                val = self._gen_expression(arg)
                creg = self.new_register()
                self.emit(f'{creg} = call i32 (i8*, ...) @printf(i8* {reg_fmt}, i32 {val})')

        result = self.new_register()
        self.emit(f'{result} = add i32 0, 0')
        return result

    # =========================================================================
    # 列表与字典操作
    # =========================================================================

    def _gen_list_literal(self, expr: ListLiteral) -> str:
        """生成列表字面量"""
        elements = expr.elements
        if not elements:
            # 空列表
            reg = self.new_register()
            self.emit(f'{reg} = call i8* @duan_list_new(i64 0)')
            return reg

        # 创建列表
        size_reg = self.new_register()
        self.emit(f'{size_reg} = add i64 0, {len(elements)}')
        list_reg = self.new_register()
        self.emit(f'{list_reg} = call i8* @duan_list_new(i64 {size_reg})')

        # 添加元素 - 需要转换为 i32* 来调用列表函数
        list_i32 = self.new_register()
        self.emit(f'{list_i32} = bitcast i8* {list_reg} to i32*')

        # 添加元素
        for i, elem in enumerate(elements):
            val = self._gen_expression(elem)
            idx_reg = self.new_register()
            self.emit(f'{idx_reg} = add i64 0, {i}')
            self.emit(f'call void @duan_list_set(i32* {list_i32}, i64 {idx_reg}, i32 {val})')

        return list_reg

    def _gen_dict_literal(self, expr: DictLiteral) -> str:
        """生成字典字面量"""
        # 创建字典
        dict_reg = self.new_register()
        self.emit(f'{dict_reg} = call i8* @duan_dict_new()')

        # 添加键值对
        for entry in expr.entries:
            key = self._gen_expression(entry.key)
            val = self._gen_expression(entry.value)
            self.emit(f'call void @duan_dict_set(i8* {dict_reg}, i8* {key}, i32 {val})')

        return dict_reg

    def _gen_index_access(self, expr: IndexAccess) -> str:
        """生成索引访问表达式"""
        obj = self._gen_expression(expr.obj)
        idx = self._gen_expression(expr.index)

        # 转换索引为 i64
        idx64 = self.new_register()
        self.emit(f'{idx64} = zext i32 {idx} to i64')

        # 将 i8* 转换为 i32*
        obj_i32 = self.new_register()
        self.emit(f'{obj_i32} = bitcast i8* {obj} to i32*')

        # 调用列表获取函数
        result = self.new_register()
        self.emit(f'{result} = call i32 @duan_list_get(i32* {obj_i32}, i64 {idx64})')
        return result

    def _gen_property_access(self, expr: PropertyAccess) -> str:
        """生成属性访问表达式"""
        obj = self._gen_expression(expr.obj)
        prop_name = expr.property_name

        if prop_name == '长度':
            # 获取列表长度 - 将 i8* 转换为 i32*
            obj_i32 = self.new_register()
            self.emit(f'{obj_i32} = bitcast i8* {obj} to i32*')
            result = self.new_register()
            self.emit(f'{result} = call i32 @duan_list_length(i32* {obj_i32})')
            return result

        # 默认情况：字典访问
        key = self._gen_expression(StringLiteral(prop_name))
        result = self.new_register()
        self.emit(f'{result} = call i32 @duan_dict_get(i8* {obj}, i8* {key})')
        return result

    # =========================================================================
    # 条件与循环
    # =========================================================================

    def _gen_if(self, stmt: IfStatement):
        cond = self._gen_expression(stmt.condition)
        label_then = self.new_label("if.then")
        label_else = self.new_label("if.else")
        label_end = self.new_label("if.end")

        # 比较条件：cond != 0
        cmp = self.new_register()
        self.emit(f'{cmp} = icmp ne i32 {cond}, 0')
        self.emit(f'br i1 {cmp}, label %{label_then}, label %{label_else}')

        # then 分支
        self.emit(f'{label_then}:')
        self.indent_level = 1
        for s in stmt.then_body:
            self._generate_statement(s)
        self.emit(f'br label %{label_end}')
        self.indent_level = 0

        # else 分支
        self.emit(f'{label_else}:')
        self.indent_level = 1
        if stmt.else_body:
            for s in stmt.else_body:
                self._generate_statement(s)
        self.emit(f'br label %{label_end}')
        self.indent_level = 0

        self.emit(f'{label_end}:')

    def _gen_while(self, stmt: WhileStatement):
        label_cond = self.new_label("while.cond")
        label_body = self.new_label("while.body")
        label_end = self.new_label("while.end")

        self.emit(f'br label %{label_cond}')
        self.emit(f'{label_cond}:')
        cond = self._gen_expression(stmt.condition)
        cmp = self.new_register()
        self.emit(f'{cmp} = icmp ne i32 {cond}, 0')
        self.emit(f'br i1 {cmp}, label %{label_body}, label %{label_end}')

        self.emit(f'{label_body}:')
        self.indent_level = 1
        for s in stmt.body:
            self._generate_statement(s)
        self.emit(f'br label %{label_cond}')
        self.indent_level = 0

        self.emit(f'{label_end}:')

    def _gen_return(self, stmt: ReturnStatement):
        if stmt.value:
            val = self._gen_expression(stmt.value)
            self.emit(f'ret i32 {val}')
        else:
            self.emit(f'ret i32 0')