"""
段言 LLVM 编译器入口

使用 SRC 解析器（纯缩进语法）解析源码，通过 AstAdapter 适配，
再经由 LLVMCodeGen 生成 LLVM IR，然后用 clang 编译为原生可执行文件。

完整链路：
  .duan → Lexer → DuanParser(v3) → AstAdapter → ast_nodes → LLVMCodeGen
  → .ll → clang → 可执行文件 (.exe on Windows, 无后缀 on Linux/macOS)
"""

import sys
import os
import subprocess
from pathlib import Path

from .codegen import LLVMCodeGen
from .codegen_typed import TypedLLVMCodeGen

# SRC 解析器
from ..lexer import Lexer
from ..duan_parser_v3 import DuanParser
from ..compiler import AstAdapter


def get_exe_extension() -> str:
    """根据当前平台返回可执行文件后缀"""
    if sys.platform == 'win32':
        return '.exe'
    return ''


def _strip_exe_ext(path: str) -> str:
    """移除路径中的可执行文件后缀（跨平台）"""
    ext = get_exe_extension()
    if ext and path.endswith(ext):
        return path[:-len(ext)]
    return path


def compile_source(source: str, verbose: bool = False) -> str:
    """
    编译段言源码为 LLVM IR 字符串

    Args:
        source: 段言源码字符串
        verbose: 是否输出详细信息

    Returns:
        LLVM IR 字符串
    """
    # 1) 语法解析（v3 纯缩进语法，内部完成词法分析）
    if verbose:
        print(f"[1/3] 语法解析: {len(source)} 字符")

    parser = DuanParser()
    v3_module = parser.parse(source)
    if v3_module is None:
        errors = '\n'.join(parser.errors) if hasattr(parser, 'errors') and parser.errors else "未知解析错误"
        raise RuntimeError(f"解析失败:\n{errors}")

    # 2) AST 适配（v3 → ast_nodes）
    if verbose:
        print(f"[2/3] AST 适配...")

    adapter = AstAdapter()
    module = adapter.convert_module(v3_module)

    # 3) LLVM IR 生成
    if verbose:
        print(f"[3/3] 生成 LLVM IR...")

    codegen = LLVMCodeGen()
    ir = codegen.generate(module)

    if verbose:
        print(f"  IR 生成完成: {len(ir)} 字符")

    return ir


def compile_source_typed(source: str, verbose: bool = False, target_platform: str = None) -> str:
    """
    编译段言源码为 LLVM IR 字符串（typed 模式）

    Args:
        source: 段言源码字符串
        verbose: 是否输出详细信息
        target_platform: 目标平台（win32/linux/darwin），默认自动检测

    Returns:
        LLVM IR 字符串
    """
    if verbose:
        print(f"[1/3] 语法解析: {len(source)} 字符")

    parser = DuanParser()
    v3_module = parser.parse(source)
    if v3_module is None:
        errors = '\n'.join(parser.errors) if hasattr(parser, 'errors') and parser.errors else "未知解析错误"
        raise RuntimeError(f"解析失败:\n{errors}")

    if verbose:
        print(f"[2/3] AST 适配...")

    adapter = AstAdapter()
    module = adapter.convert_module(v3_module)

    if verbose:
        print(f"[3/3] 生成 LLVM IR (typed)...")

    codegen = TypedLLVMCodeGen(target_platform=target_platform)
    ir = codegen.generate(module)

    if verbose:
        print(f"  IR 生成完成: {len(ir)} 字符")

    return ir


def compile_source_to_ir(source: str, output_ll: str = None, verbose: bool = False) -> str:
    """
    编译段言源码到 .ll 文件

    Args:
        source: 段言源码字符串
        output_ll: .ll 文件输出路径（可选）
        verbose: 是否输出详细信息

    Returns:
        .ll 文件路径
    """
    ir = compile_source(source, verbose=verbose)

    if output_ll is None:
        output_ll = 'output.ll'

    with open(output_ll, 'w', encoding='utf-8') as f:
        f.write(ir)

    if verbose:
        print(f"LLVM IR 已写入: {output_ll}")

    return output_ll


def compile_duan(source_path: str, output_path: str = None, verbose: bool = False):
    """
    编译 .duan 文件为原生可执行文件

    Args:
        source_path: .duan 源文件路径
        output_path: 输出 .exe 路径（默认与源文件同名）
        verbose: 是否输出详细信息
    """
    # 读取源码
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    if verbose:
        print(f"[1/5] 读取源码: {len(source)} 字符")

    # 生成 LLVM IR
    ir = compile_source(source, verbose=verbose)

    # 写入 .ll 文件
    base_path = output_path or source_path.replace('.duan', '')
    if base_path.endswith('.exe'):
        base_path = base_path[:-4]
    ll_path = base_path + '.ll'

    with open(ll_path, 'w', encoding='utf-8') as f:
        f.write(ir)

    if verbose:
        print(f"  IR 已写入: {ll_path} ({len(ir)} 字符)")

    # 查找 clang
    clang = find_clang()
    if verbose:
        print(f"  使用编译器: {clang}")

    # 编译运行时库
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    runtime_c = os.path.join(runtime_dir, 'runtime.c')
    runtime_o = base_path + '_runtime.o'

    if verbose:
        print("[3/6] 编译运行时库...")

    result = subprocess.run(
        [clang, '-c', '-O2', runtime_c, '-o', runtime_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"运行时库编译失败:\n{result.stderr}")

    # 编译 .ll 为 .o
    if verbose:
        print("[3/5] 编译 LLVM IR...")

    ir_o = base_path + '.o'
    result = subprocess.run(
        [clang, '-c', '-O2', ll_path, '-o', ir_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"IR 编译失败:\n{result.stderr}")

    # 链接为 .exe
    exe_path = base_path + '.exe'
    if verbose:
        print(f"[5/6] 链接为 .exe...")

    link_args = [clang, ir_o, runtime_o, '-o', exe_path]
    if not sys.platform.startswith('win'):
        link_args.append('-lm')

    result = subprocess.run(
        link_args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{result.stderr}")

    # 清理临时文件
    if verbose:
        print(f"[5/5] 清理临时文件...")

    for f in [ir_o, runtime_o]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            pass

    if verbose:
        size = os.path.getsize(exe_path)
        print(f"编译成功: {source_path} -> {exe_path} ({size} 字节)")

    return exe_path


def compile_duan_typed(source_path: str, output_path: str = None, verbose: bool = False, target_platform: str = None):
    """
    编译 .duan 文件为原生可执行文件（typed 模式）

    使用 DuanValue 结构体，算术运算直接操作原生类型。

    Args:
        source_path: .duan 源文件路径
        output_path: 输出可执行文件路径（默认与源文件同名）
        verbose: 是否输出详细信息
        target_platform: 目标平台（win32/linux/darwin），默认自动检测
    """
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    if verbose:
        print(f"[1/5] 读取源码: {len(source)} 字符")

    ir = compile_source_typed(source, verbose=verbose, target_platform=target_platform)

    base_path = output_path or source_path.replace('.duan', '')
    base_path = _strip_exe_ext(base_path)
    ll_path = base_path + '.ll'

    with open(ll_path, 'w', encoding='utf-8') as f:
        f.write(ir)

    if verbose:
        print(f"  IR 已写入: {ll_path} ({len(ir)} 字符)")

    clang = find_clang()
    if verbose:
        print(f"  使用编译器: {clang}")

    # 编译 typed 运行时库
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    runtime_c = os.path.join(runtime_dir, 'runtime_typed.c')
    runtime_o = base_path + '_runtime.o'

    if verbose:
        print("[2/5] 编译 typed 运行时库...")

    result = subprocess.run(
        [clang, '-c', '-O2', runtime_c, '-o', runtime_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"运行时库编译失败:\n{result.stderr}")

    # 编译 .ll 为 .o
    if verbose:
        print("[3/5] 编译 LLVM IR...")

    ir_o = base_path + '.o'
    result = subprocess.run(
        [clang, '-c', '-O2', ll_path, '-o', ir_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"IR 编译失败:\n{result.stderr}")

    # 链接为可执行文件
    exe_ext = get_exe_extension()
    exe_path = base_path + exe_ext
    if verbose:
        print(f"[4/5] 链接为可执行文件...")

    link_args = [clang, ir_o, runtime_o, '-o', exe_path]
    if not sys.platform.startswith('win'):
        link_args.append('-lm')

    result = subprocess.run(
        link_args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{result.stderr}")

    if verbose:
        print(f"[5/5] 清理临时文件...")

    for f in [ir_o, runtime_o]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            pass

    if verbose:
        size = os.path.getsize(exe_path)
        print(f"编译成功: {source_path} -> {exe_path} ({size} 字节)")

    return exe_path


def find_clang():
    """查找 clang 编译器"""
    # 常见路径
    candidates = [
        r'E:\Program Files\LLVM\bin\clang.exe',
        r'C:\Program Files\LLVM\bin\clang.exe',
        r'D:\Program Files\LLVM\bin\clang.exe',
        '/usr/bin/clang',
        '/usr/local/bin/clang',
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # 从 PATH 查找
    for path in os.environ.get('PATH', '').split(os.pathsep):
        clang_path = os.path.join(path, 'clang.exe' if sys.platform == 'win32' else 'clang')
        if os.path.exists(clang_path):
            return clang_path
    raise RuntimeError("未找到 clang 编译器。请安装 LLVM:\n  Windows: https://github.com/llvm/llvm-project/releases\n  macOS: brew install llvm\n  Linux: sudo apt install clang")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='段言 LLVM 编译器')
    ap.add_argument('source', help='.duan 源文件')
    ap.add_argument('output', nargs='?', help='输出 .exe 路径')
    ap.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    ap.add_argument('--ir-only', action='store_true', help='仅生成 LLVM IR，不编译为 .exe')
    args = ap.parse_args()

    try:
        if args.ir_only:
            source = open(args.source, 'r', encoding='utf-8').read()
            output_ll = (args.output or args.source).replace('.duan', '.ll')
            compile_source_to_ir(source, output_ll, verbose=True)
        else:
            compile_duan(args.source, args.output, verbose=args.verbose or True)
    except Exception as e:
        print(f"编译错误: {e}", file=sys.stderr)
        sys.exit(1)