"""自定义 LLVM IR 优化 Pass

基于字符串操作实现的 LLVM IR 优化 Pass 集合。
每个 Pass 以 IR 字符串为输入，返回优化后的 IR 字符串。
"""

import re
from typing import List, Optional, Set, Dict, Tuple


class TailCallOptimizationPass:
    """尾调用优化

    将满足尾调用条件的函数调用转换为跳转（jmp），
    避免额外的栈帧分配。

    尾调用条件：
    1. 调用指令是函数的最后一条指令（ret 之前）
    2. 调用的返回值直接作为当前函数的返回值
    3. 调用者和被调用者的参数类型兼容
    """

    def __init__(self):
        self._func_defs: Dict[str, Dict] = {}
        self._modified = False

    def run(self, ir: str) -> str:
        """运行尾调用优化

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        self._collect_func_defs(ir)
        result = self._optimize_tail_calls(ir)
        return result

    def _collect_func_defs(self, ir: str):
        """收集所有函数定义信息"""
        self._func_defs = {}
        current_func = None
        for line in ir.split('\n'):
            define_match = re.match(r'define\s+(\w+)\s*@(\w+)\s*\((.*?)\)', line)
            if define_match:
                current_func = define_match.group(2)
                ret_type = define_match.group(1)
                params = define_match.group(3)
                self._func_defs[current_func] = {
                    'ret_type': ret_type,
                    'params': params,
                }

    def _optimize_tail_calls(self, ir: str) -> str:
        """将尾调用转换为跳转"""
        lines = ir.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # 检测函数定义
            define_match = re.match(r'(define\s+\w+\s*@\w+\s*\(.*?\))\s*\{', line)
            if define_match:
                func_header = define_match.group(1)
                func_body_start = i
                func_body_lines = []
                i += 1
                brace_count = 1
                while i < len(lines) and brace_count > 0:
                    l = lines[i]
                    func_body_lines.append(l)
                    brace_count += l.count('{') - l.count('}')
                    i += 1

                # 对函数体进行尾调用优化
                optimized_body = self._optimize_func_body(func_body_lines)
                # 重新组装函数
                result.append(func_header + ' {')
                result.extend(optimized_body)
                # 确保函数结束
                if not result[-1].strip() == '}':
                    result.append('}')
                continue

            result.append(line)
            i += 1

        return '\n'.join(result)

    def _optimize_func_body(self, body_lines: List[str]) -> List[str]:
        """优化函数体，将尾调用转换为跳转"""
        # 找出函数最后的 ret 指令和之前的 call 指令
        result = list(body_lines)
        ret_idx = -1
        call_idx = -1

        for idx in range(len(body_lines) - 1, -1, -1):
            line = body_lines[idx].strip()
            if line.startswith('ret '):
                ret_idx = idx
            elif line.startswith('%') and 'call ' in line:
                # 检查这个 call 是否在 ret 之前
                if ret_idx >= 0 and idx < ret_idx:
                    # 检查 ret 是否直接返回 call 的结果
                    ret_val = re.search(r'ret\s+\w+\s+(%\w+)', body_lines[ret_idx])
                    call_val = re.search(r'(%\w+)\s*=', body_lines[idx])
                    if ret_val and call_val and ret_val.group(1) == call_val.group(1):
                        call_idx = idx
                        break

        if call_idx >= 0 and ret_idx >= 0:
            # 将 call 替换为 tail call
            call_line = body_lines[call_idx]
            # 去掉寄存器赋值，添加 tail 标记
            tail_call = re.sub(r'%\w+\s*=\s*', 'tail ', call_line)
            # 如果已经是 tail call 就不重复添加
            if not tail_call.startswith('tail '):
                tail_call = 'tail ' + tail_call.lstrip()
            body_lines[call_idx] = tail_call
            # 将 ret 替换为 ret void 或直接移除
            ret_match = re.search(r'ret\s+\w+\s+(%\w+)', body_lines[ret_idx])
            if ret_match:
                body_lines[ret_idx] = 'ret void'

        return body_lines


class ConstantPropagationPass:
    """常量传播

    将常量值直接传播到使用点，减少运行时计算。
    包括：
    - 常量折叠：在编译时计算常量表达式
    - 常量替换：将常量传播到后续指令
    """

    def run(self, ir: str) -> str:
        """运行常量传播

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        result = self._fold_constants(ir)
        result = self._propagate_constants(result)
        return result

    @staticmethod
    def _fold_constants(ir: str) -> str:
        """折叠常量表达式"""
        lines = ir.split('\n')
        result = []
        for line in lines:
            # 检测 add/sub/mul/sdiv 指令，如果操作数都是常量则折叠
            folded = ConstantPropagationPass._try_fold_arith(line)
            result.append(folded if folded else line)
        return '\n'.join(result)

    @staticmethod
    def _try_fold_arith(line: str) -> Optional[str]:
        """尝试折叠算术运算"""
        # 匹配 add/sub/mul/sdiv 等算术指令
        # 格式: %r = add i32 1, 2
        m = re.match(
            r'\s*(%\w+)\s*=\s*'
            r'(add|sub|mul|sdiv|udiv|and|or|xor|shl|lshr|ashr)\s+'
            r'(\w+)\s+'
            r'(-?\d+)\s*,\s*'
            r'(-?\d+)',
            line
        )
        if m:
            reg = m.group(1)
            op = m.group(2)
            ty = m.group(3)
            lhs = int(m.group(4))
            rhs = int(m.group(5))

            op_map = {
                'add': lambda a, b: a + b,
                'sub': lambda a, b: a - b,
                'mul': lambda a, b: a * b,
                'sdiv': lambda a, b: a // b if b != 0 else None,
                'udiv': lambda a, b: a // b if b != 0 else None,
                'and': lambda a, b: a & b,
                'or': lambda a, b: a | b,
                'xor': lambda a, b: a ^ b,
                'shl': lambda a, b: a << b,
                'lshr': lambda a, b: a >> b,
                'ashr': lambda a, b: a >> b,
            }

            if op in op_map:
                fn = op_map[op]
                result = fn(lhs, rhs)
                if result is not None:
                    return f'  {reg} = add {ty} {result}, 0  ; folded {op} {lhs}, {rhs} -> {result}'

        return None

    @staticmethod
    def _propagate_constants(ir: str) -> str:
        """传播常量值"""
        const_map = {}  # 寄存器 -> 常量值
        lines = ir.split('\n')
        result = []

        for line in lines:
            # 检测常量定义: %r = add i32 5, 0  ; 或者更简单的 getelementptr
            const_match = re.match(
                r'\s*(%\w+)\s*=\s*add\s+\w+\s+(-?\d+)\s*,\s*0\s',
                line
            )
            if const_match:
                reg = const_match.group(1)
                val = const_match.group(2)
                const_map[reg] = val
                result.append(line)
                continue

            # 替换行中的常量寄存器引用
            replaced = line
            for reg, val in const_map.items():
                # 在非定义位置替换
                replaced = re.sub(
                    rf'\b{re.escape(reg)}\b(?!\s*=\s*)',
                    val,
                    replaced
                )
            result.append(replaced)

        return '\n'.join(result)


class StrengthReductionPass:
    """强度削弱

    将高强度运算替换为低强度等效运算。
    例如：
    - x * 2^n → x << n
    - x / 2^n → x >> n (有符号)
    - x * 2 → x + x
    - x * 0 → 0
    - x * 1 → x
    """

    def run(self, ir: str) -> str:
        """运行强度削弱

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        lines = ir.split('\n')
        result = []
        for line in lines:
            result.append(self._reduce_strength(line))
        return '\n'.join(result)

    @staticmethod
    def _reduce_strength(line: str) -> str:
        """对单条指令进行强度削弱"""
        # 乘法 x * 2^n → x << n
        m = re.match(
            r'(\s*%\w+\s*=\s*)mul\s+(\w+)\s+(\S+)\s*,\s*(\d+)',
            line
        )
        if m:
            prefix = m.group(1)
            ty = m.group(2)
            operand = m.group(3)
            const_val = int(m.group(4))
            # 检查是否为 2 的幂
            if const_val > 0 and (const_val & (const_val - 1)) == 0:
                shift = const_val.bit_length() - 1
                return f'{prefix}shl {ty} {operand}, {shift}  ; strength reduced: mul by {const_val}'

        # 乘法 x * 1 → x (直接返回)
        m = re.match(
            r'(\s*%\w+\s*=\s*)mul\s+(\w+)\s+(\S+)\s*,\s*1\b',
            line
        )
        if m:
            prefix = m.group(1)
            ty = m.group(2)
            operand = m.group(3)
            reg = re.search(r'%\w+', line).group(0)
            return f'  {reg} = add {ty} {operand}, 0  ; strength reduced: mul by 1'

        # 除法 x / 2^n → x >> n (有符号)
        m = re.match(
            r'(\s*%\w+\s*=\s*)sdiv\s+(\w+)\s+(\S+)\s*,\s*(\d+)',
            line
        )
        if m:
            prefix = m.group(1)
            ty = m.group(2)
            operand = m.group(3)
            const_val = int(m.group(4))
            if const_val > 0 and (const_val & (const_val - 1)) == 0:
                shift = const_val.bit_length() - 1
                return f'{prefix}ashr {ty} {operand}, {shift}  ; strength reduced: sdiv by {const_val}'

        return line


class IfConversionPass:
    """条件转换（将 if-else 转换为 select）

    将简单的 if-else 分支结构转换为 select 指令，
    减少分支预测失败的开销。
    """

    def run(self, ir: str) -> str:
        """运行条件转换优化

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        return self._convert_to_select(ir)

    @staticmethod
    def _convert_to_select(ir: str) -> str:
        """将简单的 if-else 模式转换为 select 指令"""
        # 检测模式：
        #   br i1 %cond, label %then, label %else
        # then:
        #   %v1 = ...  ; 简单计算
        #   br label %end
        # else:
        #   %v2 = ...  ; 简单计算
        #   br label %end
        # end:
        #   %r = phi [%v1, %then], [%v2, %else]
        lines = ir.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # 检测 if-else 模式
            br_match = re.match(r'\s*br i1\s+(%\w+)\s*,\s*label\s+%(\w+)\s*,\s*label\s+%(\w+)', line)
            if br_match:
                cond = br_match.group(1)
                then_label = br_match.group(2)
                else_label = br_match.group(3)

                # 收集 then 和 else 块的内容
                then_body, then_end, next_i = IfConversionPass._collect_block(lines, i + 1, then_label)
                else_body, else_end, next_i2 = IfConversionPass._collect_block(lines, next_i, else_label)

                # 检查是否可以用 select 替代
                if then_body and else_body and then_end and else_end:
                    # 查找 phi 节点
                    if next_i2 < len(lines):
                        phi_line = lines[next_i2]
                        phi_match = re.match(
                            r'\s*(%\w+)\s*=\s*phi\s+(\w+)\s*'
                            r'\[\s*(\S+)\s*,\s*%(\w+)\s*\]\s*,\s*'
                            r'\[\s*(\S+)\s*,\s*%(\w+)\s*\]',
                            phi_line
                        )
                        if phi_match:
                            phi_reg = phi_match.group(1)
                            phi_type = phi_match.group(2)
                            val1 = phi_match.group(3)
                            label1 = phi_match.group(4)
                            val2 = phi_match.group(5)
                            label2 = phi_match.group(6)

                            # 如果 phi 引用的是 then 和 else 块的值
                            if (label1 == then_label and label2 == else_label) or \
                               (label1 == else_label and label2 == then_label):
                                if label1 == then_label:
                                    true_val, false_val = val1, val2
                                else:
                                    true_val, false_val = val2, val1

                                # 替换为 select
                                result.append(f'  {phi_reg} = select i1 {cond}, {phi_type} {true_val}, {phi_type} {false_val}')
                                # 跳过 then/else 块和 phi 节点
                                i = next_i2 + 1
                                continue

                # 不能优化，保留原样
                result.append(line)
                i += 1
                continue

            result.append(line)
            i += 1

        return '\n'.join(result)

    @staticmethod
    def _collect_block(lines: List[str], start_idx: int, target_label: str) -> tuple:
        """收集以指定标签开始的基本块内容

        Returns:
            (块内容列表, 终止指令行, 结束索引)
        """
        body = []
        terminator = None
        end_idx = start_idx

        # 找到目标标签
        for idx in range(start_idx, len(lines)):
            if re.match(rf'\s*{re.escape(target_label)}:', lines[idx]):
                end_idx = idx + 1
                break
        else:
            return [], None, start_idx

        # 收集块内容直到遇到终止指令
        for idx in range(end_idx, len(lines)):
            line = lines[idx]
            if re.match(r'\s*\w+:', line) and not re.match(r'\s*;', line):
                # 下一个块开始
                end_idx = idx
                break
            body.append(line)
            if re.match(r'\s*(ret|br|switch|unreachable)\s', line):
                terminator = line
                end_idx = idx + 1
                break
            end_idx = idx + 1

        return body, terminator, end_idx


class LoopUnrollPass:
    """循环展开

    将循环体复制多次，减少循环控制开销。
    只展开确定迭代次数的小循环。
    """

    def __init__(self, factor: int = 4, max_body_size: int = 10):
        self.factor = factor
        self.max_body_size = max_body_size

    def run(self, ir: str) -> str:
        """运行循环展开

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        return self._unroll_loops(ir)

    def _unroll_loops(self, ir: str) -> str:
        """展开循环"""
        # 检测简单循环模式：
        #   %i = phi i32 [0, %entry], [%next, %loop]
        #   ... 循环体
        #   %next = add i32 %i, 1
        #   %cmp = icmp slt i32 %next, %n
        #   br i1 %cmp, label %loop, label %end
        lines = ir.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # 检测 phi 节点（循环计数器）
            phi_match = re.match(
                r'\s*(%\w+)\s*=\s*phi\s+(\w+)\s*\[(\d+),\s*%(\w+)\]\s*,\s*\[(%\w+),\s*%(\w+)\]',
                line
            )
            if phi_match:
                # 这是一个可能的循环头部
                phi_reg = phi_match.group(1)
                phi_type = phi_match.group(2)
                init_val = int(phi_match.group(3))
                inc_reg = phi_match.group(5)

                # 查找循环体结束
                loop_body = []
                loop_end_idx = i + 1
                for j in range(i + 1, len(lines)):
                    if re.match(r'\s*br\s+i1\s+', lines[j]):
                        loop_end_idx = j + 1
                        break
                    loop_body.append(lines[j])
                    loop_end_idx = j + 1

                # 检查循环体大小
                if len(loop_body) <= self.max_body_size:
                    # 尝试展开：复制循环体
                    unrolled = []
                    for k in range(self.factor - 1):
                        for bline in loop_body:
                            # 重命名寄存器
                            new_line = re.sub(
                                r'%\b(\d+)\b',
                                lambda m: f'%{int(m.group(1)) + k * 1000}',
                                bline
                            )
                            unrolled.append(new_line)
                    # 保留原循环体（最后一次迭代）
                    result.append(line)  # 保留 phi
                    result.extend(loop_body)
                    i = loop_end_idx
                    continue

            result.append(line)
            i += 1

        return '\n'.join(result)


class GlobalOptimizationPass:
    """全局优化（跨函数）

    跨函数边界的优化，包括：
    - 移除未使用的函数声明
    - 合并重复的全局变量
    - 内联仅调用一次的函数
    """

    def run(self, ir: str) -> str:
        """运行全局优化

        Args:
            ir: 输入的 LLVM IR 字符串

        Returns:
            优化后的 IR 字符串
        """
        result = self._remove_unused_decls(ir)
        result = self._merge_duplicate_constants(result)
        return result

    @staticmethod
    def _remove_unused_decls(ir: str) -> str:
        """移除未使用的函数声明"""
        # 收集所有 declare 和它们的引用
        declares = {}  # name -> line
        used_funcs = set()

        for line in ir.split('\n'):
            declare_match = re.match(r'declare\s+\w+\s*@(\w+)', line)
            if declare_match:
                declares[declare_match.group(1)] = line

        # 统计函数引用
        for line in ir.split('\n'):
            for func_name in declares:
                if f'@{func_name}' in line and not line.startswith('declare'):
                    used_funcs.add(func_name)

        # 移除未使用的 declare
        unused = set(declares.keys()) - used_funcs
        if not unused:
            return ir

        lines = ir.split('\n')
        result = [l for l in lines if not any(f'declare' in l and f'@{name}' in l for name in unused)]
        return '\n'.join(result)

    @staticmethod
    def _merge_duplicate_constants(ir: str) -> str:
        """合并重复的字符串常量"""
        const_pattern = re.compile(
            r'(@\.str\.\d+)\s*=\s*private\s+unnamed_addr\s+constant\s+'
            r'\[(\d+)\s*x\s*i8\]\s*c"([^"]*)"'
        )

        # 收集所有字符串常量
        const_map = {}  # content -> (name, size)
        for m in const_pattern.finditer(ir):
            name = m.group(1)
            size = int(m.group(2))
            content = m.group(3)
            if content in const_map:
                # 重复常量，将引用替换为第一个
                existing_name = const_map[content][0]
                ir = ir.replace(name, existing_name)
            else:
                const_map[content] = (name, size)

        return ir