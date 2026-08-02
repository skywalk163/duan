"""IR 生成阶段验证（verifyFunction）单元测试"""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import unittest
from llvm.codegen_typed import TypedLLVMCodeGen
from llvm.compiler import compile_source_typed, verify_ir_with_clang, find_clang
from llvm.core import LLVMCodeGenCore


class TestVerifyFunction(unittest.TestCase):
    """测试 _verify_function 结构化验证"""

    def setUp(self):
        self.core = LLVMCodeGenCore()

    def test_verify_function_valid(self):
        """验证合法函数通过"""
        func_lines = [
            'define void @_seg_test(ptr %result, ptr %args, i32 %num_args) {',
            'entry:',
            '  %1 = alloca i32',
            '  store i32 0, ptr %1',
            '  ret void',
            '}',
        ]
        errors = self.core._verify_function(func_lines, '_seg_test')
        self.assertEqual(errors, [], f"合法函数不应有错误，实际: {errors}")

    def test_verify_function_missing_terminator(self):
        """验证缺少终止指令的函数被检测到"""
        func_lines = [
            'define void @_seg_test(ptr %result) {',
            'entry:',
            '  %1 = alloca i32',
            '  store i32 0, ptr %1',
            '}',
        ]
        errors = self.core._verify_function(func_lines, '_seg_test')
        self.assertTrue(any('缺少终止指令' in e for e in errors),
                        f"应检测到缺少终止指令，实际: {errors}")

    def test_verify_function_duplicate_label(self):
        """验证重复标签被检测到"""
        func_lines = [
            'define void @_seg_test(ptr %result) {',
            'entry:',
            '  br label %entry',
            'entry:',
            '  ret void',
            '}',
        ]
        errors = self.core._verify_function(func_lines, '_seg_test')
        self.assertTrue(any('重复' in e for e in errors),
                        f"应检测到重复标签，实际: {errors}")

    def test_verify_function_dead_code(self):
        """验证 ret 后的死代码被检测到"""
        func_lines = [
            'define void @_seg_test(ptr %result) {',
            'entry:',
            '  ret void',
            '  %1 = add i32 1, 2',
            '}',
        ]
        errors = self.core._verify_function(func_lines, '_seg_test')
        self.assertTrue(any('终止指令之后' in e for e in errors),
                        f"应检测到死代码，实际: {errors}")

    def test_verify_function_multiple_blocks(self):
        """验证多基本块函数（if-else）通过"""
        func_lines = [
            'define void @_seg_test(ptr %result) {',
            'entry:',
            '  %1 = icmp sgt i32 10, 5',
            '  br i1 %1, label %then_1, label %else_1',
            'then_1:',
            '  store i32 1, ptr %result',
            '  br label %end_1',
            'else_1:',
            '  store i32 0, ptr %result',
            '  br label %end_1',
            'end_1:',
            '  ret void',
            '}',
        ]
        errors = self.core._verify_function(func_lines, '_seg_test')
        self.assertEqual(errors, [], f"合法多块函数不应有错误，实际: {errors}")


class TestVerifyModuleIR(unittest.TestCase):
    """测试 _verify_module_ir 模块级验证"""

    def setUp(self):
        self.core = LLVMCodeGenCore()

    def test_verify_module_multiple_functions(self):
        """验证包含多个函数的模块"""
        ir_lines = [
            'define void @_seg_a(ptr %result) {',
            'entry:',
            '  ret void',
            '}',
            '',
            'define void @_seg_b(ptr %result) {',
            'entry:',
            '  %1 = add i32 1, 2',
            '  ret void',
            '}',
        ]
        errors = self.core._verify_module_ir(ir_lines)
        self.assertEqual(errors, [], f"合法模块不应有错误，实际: {errors}")

    def test_verify_module_detects_error(self):
        """验证模块级检测能发现函数级错误"""
        ir_lines = [
            'define void @_seg_a(ptr %result) {',
            'entry:',
            '  %1 = add i32 1, 2',
            '}',
            '',
            'define void @_seg_b(ptr %result) {',
            'entry:',
            '  ret void',
            '}',
        ]
        errors = self.core._verify_module_ir(ir_lines)
        self.assertTrue(len(errors) > 0, "应检测到 _seg_a 缺少终止指令")
        self.assertTrue(any('_seg_a' in e for e in errors))


class TestIRValidationInCodegen(unittest.TestCase):
    """测试 codegen 中的 IR 验证集成"""

    def test_simple_ir_generation_passes_validation(self):
        """简单程序的 IR 生成应通过验证"""
        source = '打印 "Hello"'
        ir = compile_source_typed(source)
        self.assertIsInstance(ir, str)
        self.assertTrue(len(ir) > 0)

    def test_if_else_ir_generation_passes_validation(self):
        """if-else 程序的 IR 生成应通过验证"""
        source = '''设 x 为 10
如果 x 大于 5：
  打印 "大于"
否则：
  打印 "小于"
'''
        ir = compile_source_typed(source)
        self.assertIsInstance(ir, str)
        self.assertTrue(len(ir) > 0)

    def test_while_loop_ir_generation_passes_validation(self):
        """while 循环程序的 IR 生成应通过验证"""
        source = '''设 i 为 0
当 i 小于 5：
  设 i 为 i 加 1
'''
        ir = compile_source_typed(source)
        self.assertIsInstance(ir, str)
        self.assertTrue(len(ir) > 0)

    def test_paragraph_ir_generation_passes_validation(self):
        """段落定义和调用的 IR 生成应通过验证"""
        source = '''段落 加法 接收 a, b：
  返回 a 加 b

设 结果 为 加法(3, 5)
'''
        ir = compile_source_typed(source)
        self.assertIsInstance(ir, str)
        self.assertTrue(len(ir) > 0)


class TestVerifyIRWithClang(unittest.TestCase):
    """测试 compiler 层的 clang IR 验证"""

    def setUp(self):
        self.clang = find_clang()

    def test_valid_ir_passes_clang_verify(self):
        """合法 IR 应通过 clang 验证"""
        source = '打印 "Hello"'
        ir = compile_source_typed(source)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.ll', delete=False, encoding='utf-8') as f:
            f.write(ir)
            ll_path = f.name

        try:
            result = verify_ir_with_clang(ll_path, self.clang)
            self.assertTrue(result)
        finally:
            if os.path.exists(ll_path):
                os.remove(ll_path)


if __name__ == '__main__':
    unittest.main()
