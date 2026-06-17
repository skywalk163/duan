"""
段言（Duan）LLVM IR 代码生成器 - 组合模块

将 LLVMCodeGenCore（框架方法）和 LLVMCodeGenMixin（生成细节）
组合为完整的 LLVMCodeGen 类。
"""

import os
import subprocess

from llvm_codegen import LLVMCodeGenMixin

# LLVM 工具路径
LLVM_BIN = r"E:\Program Files\LLVM\bin"
CLANG = os.path.join(LLVM_BIN, "clang.exe")


class LLVMCodeGen(LLVMCodeGenMixin):
    """段言 LLVM 代码生成器"""
    pass


# =============================================================================
# 编译入口
# =============================================================================

def compile_duan(source_code: str, output_name: str = "output.exe") -> bool:
    """
    编译段言源码为可执行文件

    参数:
        source_code: 段言源码字符串
        output_name: 输出文件名

    返回:
        bool: 是否编译成功
    """
    from duan_visitor import parse_source

    # 1. 解析为 AST
    module = parse_source(source_code)
    if module is None:
        print("解析失败")
        return False

    # 2. 生成 LLVM IR
    gen = LLVMCodeGen()
    ir = gen.generate(module)

    # 3. 写入 .ll 文件
    ll_name = output_name.rsplit('.', 1)[0] + '.ll'
    with open(ll_name, 'w', encoding='utf-8') as f:
        f.write(ir)
    print(f"  LLVM IR -> {ll_name}")

    # 4. 调用 clang 编译
    exe_name = output_name
    cmd = [CLANG, ll_name, '-o', exe_name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  编译失败:")
        print(result.stderr)
        return False

    print(f"  可执行文件 -> {exe_name}")
    return True


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    # 测试代码
    test_code = """
定义甲等于10。
定义乙等于20。
打印(甲加乙)。

如果甲大于乙那么:
  打印(1)。
否则:
  打印(0)。
结束。
"""

    success = compile_duan(test_code, "test_duan.exe")
    if success:
        print("\n运行结果:")
        os.system("test_duan.exe")