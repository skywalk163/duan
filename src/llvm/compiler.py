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

# 支持包内相对导入和直接导入两种方式
try:
    from .codegen import LLVMCodeGen
    from .codegen_typed import TypedLLVMCodeGen
    from ..lexer import Lexer
    from ..duan_parser_v3 import DuanParser
    from ..compiler import AstAdapter
    import ast_nodes as ast
except ImportError:
    # 直接导入模式（sys.path 包含 src 目录）
    from llvm.codegen import LLVMCodeGen
    from llvm.codegen_typed import TypedLLVMCodeGen
    from lexer import Lexer
    from duan_parser_v3 import DuanParser
    from compiler import AstAdapter
    import ast_nodes as ast


def get_exe_extension(target_arch: str = None) -> str:
    """根据当前平台返回可执行文件后缀

    Args:
        target_arch: 目标架构（'x64'/'arm64'/None），None 表示本地架构
    """
    if sys.platform == 'win32':
        return '.exe'
    return ''


def _strip_exe_ext(path: str) -> str:
    """移除路径中的可执行文件后缀（跨平台）"""
    ext = get_exe_extension()
    if ext and path.endswith(ext):
        return path[:-len(ext)]
    return path


def detect_target_arch(target_arg: str = None) -> str:
    """检测目标架构

    根据 --target 参数或 -arch 参数自动选择 x64/ARM64 目标三元组。

    Args:
        target_arg: 目标架构参数（如 'x86_64'、'aarch64'、'arm64'、'x64'）

    Returns:
        目标架构字符串：'x86_64' 或 'aarch64'
    """
    if target_arg is None:
        return 'x86_64'

    target_lower = target_arg.lower().replace('-', '_').replace(' ', '_')

    # ARM64 架构匹配
    if any(t in target_lower for t in ('aarch64', 'arm64', 'armv8')):
        return 'aarch64'

    # x86_64 架构匹配
    if any(t in target_lower for t in ('x86_64', 'x64', 'amd64', 'x86')):
        return 'x86_64'

    # 默认返回本地架构
    import platform as _platform
    machine = _platform.machine().lower()
    if machine in ('aarch64', 'arm64', 'armv8l', 'armv8b'):
        return 'aarch64'
    return 'x86_64'


def get_target_triple(target_arch: str, target_platform: str = None) -> str:
    """获取 LLVM 目标三元组

    Args:
        target_arch: 目标架构（'x86_64'/'aarch64'）
        target_platform: 目标平台（win32/linux/darwin），None 表示当前平台

    Returns:
        LLVM 目标三元组字符串
    """
    if target_platform is None:
        target_platform = sys.platform

    os_part = {
        'win32': 'windows-msvc',
        'linux': 'linux-gnu',
        'darwin': 'macosx',
    }.get(target_platform, 'linux-gnu')

    if target_arch == 'aarch64':
        if target_platform == 'win32':
            return 'aarch64-pc-windows-msvc'
        elif target_platform == 'darwin':
            return 'arm64-apple-macosx'
        else:
            return 'aarch64-unknown-linux-gnu'
    else:
        if target_platform == 'win32':
            return 'x86_64-pc-windows-msvc'
        elif target_platform == 'darwin':
            return 'x86_64-apple-macosx'
        else:
            return 'x86_64-unknown-linux-gnu'


def get_optimization_flags(optimize_level: int, optimize_size: bool = False,
                           lto: bool = False) -> list:
    """根据优化级别返回 clang 编译参数

    将 -O0/-O1/-O2/-O3 映射到对应的 clang 编译参数，
    并添加 -mllvm 传递的 LLVM Pass 控制参数。

    Args:
        optimize_level: 优化级别（0-3）
        optimize_size: 是否启用 -Os 尺寸优化（覆盖 optimize_level 的 -Ox 标志）
        lto: 是否启用 LTO (Link Time Optimization)

    Returns:
        clang 编译参数列表
    """
    if optimize_size:
        flags = ['-Os', '-fdata-sections', '-ffunction-sections']
        if sys.platform != 'darwin':
            flags.extend(['-Wl,--gc-sections'])
        else:
            flags.extend(['-Wl,-dead_strip'])
    else:
        flags = [f'-O{optimize_level}']

    # 根据优化级别添加 LLVM Pass 控制参数
    if not optimize_size and optimize_level >= 1:
        # -O1 及以上：启用内联、mem2reg（SSA 构建）
        flags.extend(['-mllvm', '-inline'])
        flags.extend(['-mllvm', '-mem2reg'])

    if not optimize_size and optimize_level >= 2:
        # -O2 及以上：启用循环展开、合并、GVN
        flags.extend(['-mllvm', '-loop-unroll'])
        flags.extend(['-mllvm', '-loop-rotate'])
        flags.extend(['-mllvm', '-gvn'])

    if not optimize_size and optimize_level >= 3:
        # -O3：启用向量化、SLP、更多循环优化
        flags.extend(['-mllvm', '-loop-vectorize'])
        flags.extend(['-mllvm', '-slp-vectorize'])
        flags.extend(['-mllvm', '-licm'])
        flags.extend(['-mllvm', '-simplifycfg'])

    # LTO (Link Time Optimization)
    if lto:
        flags.append('-flto')
        if sys.platform == 'win32':
            flags.append('-fuse-ld=lld')
        elif sys.platform == 'darwin':
            flags.append('-flto=full')
        else:
            flags.append('-flto=auto')

    return flags


def get_size_reduction_summary(original_size: int, stripped_size: int) -> str:
    """生成体积缩减报告

    Args:
        original_size: 原始文件大小（字节）
        stripped_size: 优化后文件大小（字节）

    Returns:
        格式化的体积缩减报告字符串
    """
    reduction = original_size - stripped_size
    reduction_pct = (reduction / max(original_size, 1)) * 100
    return (
        f"体积优化摘要:\n"
        f"  - 优化前: {_format_size(original_size)}\n"
        f"  - 优化后: {_format_size(stripped_size)}\n"
        f"  - 缩减:   {_format_size(reduction)} ({reduction_pct:.1f}%)"
    )


def _format_size(size_bytes: int) -> str:
    """将字节数格式化为人类可读的大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


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


def _run_type_check_on_ast(source: str, module, verbose: bool = False):
    """在 LLVM 编译管线中运行类型检查"""
    try:
        from core.config import DuanConfig, TypeCheckLevel
        from type_checker import create_checker_from_source

        config = DuanConfig()
        config.type_check_level = TypeCheckLevel.SIGNATURE
        checker = create_checker_from_source(source, config)

        if checker.config.check_level != TypeCheckLevel.NONE:
            from type_inferencer import TypeInferencer
            inferencer = TypeInferencer()
            inferencer.infer(module)
            checker.check(module, inferencer)

            if checker.has_errors():
                errors = checker.get_errors()
                error_msgs = '\n'.join(str(r) for r in errors)
                raise RuntimeError(f"类型检查失败:\n{error_msgs}")

            if checker.get_warnings() and verbose:
                for w in checker.get_warnings():
                    print(f"  [类型警告] {w.message}")
    except ImportError:
        pass  # 类型检查器不可用时跳过
    except RuntimeError:
        raise
    except Exception as e:
        if verbose:
            print(f"  [类型检查] 跳过: {e}")


def compile_source_typed(source: str, verbose: bool = False, target_platform: str = None,
                         target_arch: str = None, debug: bool = False) -> str:
    """
    编译段言源码为 LLVM IR 字符串（typed 模式）

    Args:
        source: 段言源码字符串
        verbose: 是否输出详细信息
        target_platform: 目标平台（win32/linux/darwin），默认自动检测
        target_arch: 目标架构（'x86_64'/'aarch64'），影响数据模型选择
        debug: 是否生成 DWARF 调试信息

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

    # 类型检查（如果配置了检查级别）
    _run_type_check_on_ast(source, module, verbose)

    if verbose:
        print(f"[3/3] 生成 LLVM IR (typed)...")

    codegen = TypedLLVMCodeGen(target_platform=target_platform, target_arch=target_arch, debug=debug)
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


def compile_duan(source_path: str, output_path: str = None, verbose: bool = False,
                 target: str = None, optimize_level: int = 2, debug: bool = False,
                 optimize_size: bool = False, lto: bool = False, strip: bool = False):
    """
    编译 .duan 文件为原生可执行文件

    Args:
        source_path: .duan 源文件路径
        output_path: 输出 .exe 路径（默认与源文件同名）
        verbose: 是否输出详细信息
        target: 目标架构（'x86_64'/'aarch64'/'arm64'），默认本地架构
        optimize_level: 优化级别（0-3），默认 2
        debug: 是否生成 DWARF 调试信息
        optimize_size: 是否启用 -Os 尺寸优化（替代 -O2）
        lto: 是否启用 LTO (Link Time Optimization)
        strip: 是否剥离调试符号
    """
    # 读取源码
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    if verbose:
        print(f"[1/5] 读取源码: {len(source)} 字符")

    # 检测目标架构
    target_arch = detect_target_arch(target)

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
    clang = find_clang(target_arch=target_arch)
    if verbose:
        print(f"  使用编译器: {clang}")

    # 编译运行时库
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    runtime_c = os.path.join(runtime_dir, 'runtime.c')
    runtime_o = base_path + '_runtime.o'

    opt_flags = get_optimization_flags(optimize_level, optimize_size=optimize_size, lto=lto)
    arch_flags = get_arch_specific_cflags(target_arch)
    debug_flags = ['-g'] if debug else []

    if verbose:
        print("[3/6] 编译运行时库...")

    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, runtime_c, '-o', runtime_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"运行时库编译失败:\n{result.stderr}")

    # 编译 .ll 为 .o
    if verbose:
        print("[3/5] 编译 LLVM IR...")

    ir_o = base_path + '.o'
    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, ll_path, '-o', ir_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"IR 编译失败:\n{result.stderr}")

    # 链接为 .exe
    exe_ext = get_exe_extension()
    exe_path = base_path + exe_ext
    if verbose:
        print(f"[5/6] 链接为 .exe...")

    link_args = [clang, *arch_flags, ir_o, runtime_o, '-o', exe_path]
    if debug:
        link_args.append('-g')
    if not sys.platform.startswith('win'):
        link_args.append('-lm')
    # LTO 链接参数
    if lto:
        link_args.append('-flto')

    result = subprocess.run(
        link_args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{result.stderr}")

    # 剥离调试符号
    original_size = os.path.getsize(exe_path) if os.path.exists(exe_path) else 0
    if strip and not debug:
        try:
            if sys.platform == 'win32':
                strip_tools = ['llvm-strip', 'strip']
                for tool in strip_tools:
                    try:
                        subprocess.run([tool, exe_path], capture_output=True, timeout=30)
                        break
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
            else:
                subprocess.run(['strip', exe_path], check=True, timeout=30)
        except (subprocess.SubprocessError, OSError):
            if verbose:
                print("  [警告] 无法剥离调试符号")

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
        final_size = os.path.getsize(exe_path)
        print(f"编译成功: {source_path} -> {exe_path} ({final_size} 字节)")
        if original_size > 0 and strip:
            print(get_size_reduction_summary(original_size, final_size))

    return exe_path


def compile_duan_typed(source_path: str, output_path: str = None, verbose: bool = False,
                       target_platform: str = None, target: str = None,
                       optimize_level: int = 2, debug: bool = False,
                       optimize_size: bool = False, lto: bool = False, strip: bool = False):
    """
    编译 .duan 文件为原生可执行文件（typed 模式）

    使用 DuanValue 结构体，算术运算直接操作原生类型。

    Args:
        source_path: .duan 源文件路径
        output_path: 输出可执行文件路径（默认与源文件同名）
        verbose: 是否输出详细信息
        target_platform: 目标平台（win32/linux/darwin），默认自动检测
        target: 目标架构（'x86_64'/'aarch64'/'arm64'），默认本地架构
        optimize_level: 优化级别（0-3），默认 2
        debug: 是否生成 DWARF 调试信息
        optimize_size: 是否启用 -Os 尺寸优化（替代 -O2）
        lto: 是否启用 LTO (Link Time Optimization)
        strip: 是否剥离调试符号
    """
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    if verbose:
        print(f"[1/5] 读取源码: {len(source)} 字符")

    # 检测目标架构
    target_arch = detect_target_arch(target)
    if verbose:
        print(f"  目标架构: {target_arch}")

    ir = compile_source_typed(source, verbose=verbose, target_platform=target_platform,
                              target_arch=target_arch, debug=debug)

    base_path = output_path or source_path.replace('.duan', '')
    base_path = _strip_exe_ext(base_path)
    ll_path = base_path + '.ll'

    with open(ll_path, 'w', encoding='utf-8') as f:
        f.write(ir)

    if verbose:
        print(f"  IR 已写入: {ll_path} ({len(ir)} 字符)")

    # 根据目标架构查找编译器
    clang = find_clang(target_arch=target_arch)
    if verbose:
        print(f"  使用编译器: {clang}")

    # IR 验证：用 clang 解析 .ll 文件检查语法和结构正确性
    verify_ir_with_clang(ll_path, clang, verbose)

    # 编译 typed 运行时库
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    runtime_c = os.path.join(runtime_dir, 'runtime_typed.c')
    runtime_o = base_path + '_runtime.o'

    # 使用优化级别对应的编译参数
    opt_flags = get_optimization_flags(optimize_level, optimize_size=optimize_size, lto=lto)
    arch_flags = get_arch_specific_cflags(target_arch)
    debug_flags = ['-g'] if debug else []

    if verbose:
        print("[3/6] 编译 typed 运行时库...")

    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, runtime_c, '-o', runtime_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"运行时库编译失败:\n{result.stderr}")

    # 编译 .ll 为 .o
    if verbose:
        print("[4/6] 编译 LLVM IR...")

    ir_o = base_path + '.o'
    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, ll_path, '-o', ir_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"IR 编译失败:\n{result.stderr}")

    # 链接为可执行文件
    exe_ext = get_exe_extension()
    exe_path = base_path + exe_ext
    if verbose:
        print(f"[5/6] 链接为可执行文件...")

    link_args = [clang, *arch_flags, ir_o, runtime_o, '-o', exe_path]
    if debug:
        link_args.append('-g')
    if not sys.platform.startswith('win'):
        link_args.append('-lm')
    if lto:
        link_args.append('-flto')

    result = subprocess.run(
        link_args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{result.stderr}")

    # 剥离调试符号
    original_size = os.path.getsize(exe_path) if os.path.exists(exe_path) else 0
    if strip and not debug:
        try:
            if sys.platform == 'win32':
                for tool in ['llvm-strip', 'strip']:
                    try:
                        subprocess.run([tool, exe_path], capture_output=True, timeout=30)
                        break
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
            else:
                subprocess.run(['strip', exe_path], check=True, timeout=30)
        except (subprocess.SubprocessError, OSError):
            if verbose:
                print("  [警告] 无法剥离调试符号")

    if verbose:
        print(f"[6/6] 清理临时文件...")

    for f in [ir_o, runtime_o]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            pass

    if verbose:
        final_size = os.path.getsize(exe_path)
        print(f"编译成功: {source_path} -> {exe_path} ({final_size} 字节)")
        if original_size > 0 and strip:
            print(get_size_reduction_summary(original_size, final_size))

    return exe_path


def verify_ir_with_clang(ll_path: str, clang_path: str = None, verbose: bool = False) -> bool:
    """使用 clang 验证 LLVM IR 文件的语法和结构正确性

    通过 `clang -c -x ir file.ll -o NUL` 让 clang 解析 .ll 文件，
    如果 IR 有语法错误或结构问题（如基本块未终止、类型不匹配等），
    clang 会返回非零退出码并输出错误信息。

    Args:
        ll_path: .ll 文件路径
        clang_path: clang 可执行文件路径（默认自动查找）
        verbose: 是否输出详细信息

    Returns:
        True 表示验证通过

    Raises:
        RuntimeError: IR 验证失败时抛出，包含 clang 的错误信息
    """
    if clang_path is None:
        clang_path = find_clang()

    if verbose:
        print("  验证 LLVM IR (clang -x ir)...")

    result = subprocess.run(
        [clang_path, '-c', '-x', 'ir', ll_path, '-o', os.devnull],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"LLVM IR 验证失败（clang -x ir）:\n{result.stderr}")

    if verbose:
        print("  IR 验证通过")
    return True


def verify_ir_with_llvmlite(ll_path: str, verbose: bool = False) -> bool:
    """使用 llvmlite 本地验证 LLVM IR 文件的语法和结构正确性

    clang 不可用时的替代方案：调用 llvmlite.binding.parse_assembly + verify()
    做与 clang -x ir 等价的语法/结构验证，不依赖外部工具链。

    Args:
        ll_path: .ll 文件路径
        verbose: 是否输出详细信息

    Returns:
        True 表示验证通过

    Raises:
        RuntimeError: llvmlite 未安装或 IR 验证失败
    """
    try:
        import llvmlite.binding as _llvm
    except ImportError:
        raise RuntimeError(
            "llvmlite 未安装，且未找到 clang 编译器，无法验证 IR。\n"
            "请安装 clang（https://llvm.org）或运行 pip install llvmlite。"
        )

    if verbose:
        print("  验证 LLVM IR (llvmlite parse_assembly)...")

    try:
        with open(ll_path, 'r', encoding='utf-8') as f:
            ir_text = f.read()
        module = _llvm.parse_assembly(ir_text)
        module.verify()
    except Exception as e:  # noqa: BLE001 - 统一转为 RuntimeError 报告
        raise RuntimeError(f"LLVM IR 验证失败（llvmlite）:\n{e}") from e

    if verbose:
        print("  IR 验证通过（llvmlite）")
    return True


def verify_ir(ll_path: str, verbose: bool = False) -> bool:
    """验证 LLVM IR 文件（优先 clang，回退 llvmlite）

    优先使用 clang 验证；clang 不可用时回退到 llvmlite 本地验证，
    保证 IR 验证在任何环境下都真实执行（而非跳过）。

    Args:
        ll_path: .ll 文件路径
        verbose: 是否输出详细信息

    Returns:
        True 表示验证通过

    Raises:
        RuntimeError: 两种验证方式均不可用或验证失败
    """
    try:
        return verify_ir_with_clang(ll_path, verbose=verbose)
    except RuntimeError as e:
        if "未找到 clang" in str(e):
            return verify_ir_with_llvmlite(ll_path, verbose=verbose)
        raise


def find_clang(target_arch: str = None):
    """查找 clang 编译器（支持 MSVC 和 MinGW 两种模式）

    Args:
        target_arch: 目标架构（'x86_64'/'aarch64'/None），
                    指定 ARM64 时会检测交叉编译器

    Returns:
        clang 可执行文件路径
    """
    import sys as _sys

    # 如果指定了 ARM64 目标，先尝试查找交叉编译器
    if target_arch == 'aarch64':
        arm64_candidates = get_arm64_cross_compiler_candidates()
        for c in arm64_candidates:
            if os.path.exists(c):
                return c

    # 常见路径（优先 MinGW，因为它自带 C 标准库头文件）
    candidates = [
        # MinGW-w64 LLVM 工具链（自带 C 标准库）
        r'c:\traework\duan\llvm-mingw-20240619-ucrt-x86_64\bin\clang.exe',
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
        clang_path = os.path.join(path, 'clang.exe' if _sys.platform == 'win32' else 'clang')
        if os.path.exists(clang_path):
            return clang_path
        # 也查找 mingw 版本的 clang
        mingw_clang = os.path.join(path, 'x86_64-w64-mingw32-clang.exe')
        if os.path.exists(mingw_clang):
            return mingw_clang
    raise RuntimeError("未找到 clang 编译器。请安装 LLVM:\n  Windows: https://github.com/llvm/llvm-project/releases\n  macOS: brew install llvm\n  Linux: sudo apt install clang")


def get_arm64_cross_compiler_candidates() -> list:
    """获取 ARM64 交叉编译器候选路径

    Returns:
        ARM64 交叉编译器候选路径列表
    """
    import sys as _sys
    if _sys.platform == 'win32':
        return [
            # llvm-mingw ARM64 工具链
            r'c:\traework\duan\llvm-mingw-20240619-ucrt-aarch64\bin\clang.exe',
            r'c:\traework\duan\llvm-mingw-20240619-ucrt-x86_64\bin\clang.exe',
            # MSVC ARM64 交叉编译器
            r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\bin\clang.exe',
            # 通用 ARM64 工具链
            r'E:\Program Files\LLVM\bin\clang.exe',
            r'C:\Program Files\LLVM\bin\clang.exe',
        ]
    elif _sys.platform == 'darwin':
        return [
            '/usr/bin/clang',
            '/usr/local/bin/clang',
            '/opt/homebrew/bin/clang',
        ]
    else:
        # Linux
        return [
            'aarch64-linux-gnu-gcc',
            'aarch64-linux-gnu-g++',
            '/usr/bin/aarch64-linux-gnu-gcc',
            '/usr/bin/clang',
            '/usr/local/bin/clang',
        ]


def get_arch_specific_cflags(target_arch: str) -> list:
    """获取架构特定的编译参数

    Args:
        target_arch: 目标架构（'x86_64'/'aarch64'）

    Returns:
        架构特定的编译参数列表
    """
    if target_arch == 'aarch64':
        return ['--target=aarch64-linux-gnu']
    return []


def compile_modules_typed(sources: dict, main_module: str = None, verbose: bool = False, target_platform: str = None, debug: bool = False) -> str:
    """
    编译多个段言模块为合并的 LLVM IR（typed 模式）

    使用单个 codegen 实例编译所有模块，避免全局常量和声明重复。

    Args:
        sources: 模块名 -> 源码字符串 的字典
        main_module: 主模块名（生成 main 函数的模块），默认为第一个
        verbose: 是否输出详细信息
        target_platform: 目标平台
        debug: 是否生成 DWARF 调试信息

    Returns:
        合并的 LLVM IR 字符串
    """
    if not sources:
        raise ValueError("没有源文件可编译")

    if main_module is None:
        main_module = list(sources.keys())[0]

    if verbose:
        print(f"[1/3] 多模块编译: {len(sources)} 个模块")
        for mod_name, src in sources.items():
            print(f"  - {mod_name}: {len(src)} 字符")

    parser = DuanParser()
    adapter = AstAdapter()

    # 第一步：解析所有模块，收集 AST
    modules = {}
    for mod_name, source in sources.items():
        if verbose:
            print(f"[2/3] 解析模块: {mod_name}")

        v3_module = parser.parse(source)
        if v3_module is None:
            errors = '\n'.join(parser.errors) if hasattr(parser, 'errors') and parser.errors else "未知解析错误"
            raise RuntimeError(f"模块 {mod_name} 解析失败:\n{errors}")

        module = adapter.convert_module(v3_module)
        module.name = mod_name
        modules[mod_name] = module

    # 第二步：使用单个 codegen 实例编译所有模块
    if verbose:
        print(f"[3/3] 生成合并 IR（{len(modules)} 个模块）")

    codegen = TypedLLVMCodeGen(target_platform=target_platform, debug=debug)

    # 初始化运行时声明（只做一次）
    codegen.declare_runtime()
    codegen._declare_typed_runtime()

    # 初始化调试信息（DWARF）
    if debug:
        codegen._gen_debug_compile_unit()
        codegen._gen_debug_types()

    # 收集所有模块的导入和段落
    all_module_list = list(modules.values())
    main_mod = modules.get(main_module, all_module_list[0])

    # 先处理所有模块的导入语句（记录导入映射）
    for mod in all_module_list:
        codegen._process_imports(mod)

    # 收集所有模块的语句、类和段落（先收集，再生成）
    for mod in all_module_list:
        for stmt in mod.statements:
            if isinstance(stmt, ast.ImportStatement):
                continue
            if isinstance(stmt, ast.ExportStatement):
                continue
            codegen._collect_statement(stmt)
        if hasattr(mod, 'classes'):
            for cls_def in mod.classes:
                codegen._collect_class(cls_def)
        # 收集接口定义（Level 7）
        if hasattr(mod, 'interfaces'):
            for iface_def in mod.interfaces:
                codegen._collect_interface(iface_def)
        for seg in mod.segments:
            codegen._collect_segment(seg)

    # 生成导入的外部段函数声明（仅声明那些不在本地定义的符号）
    # 由于所有模块都在同一个 codegen 中，大部分导入符号都有本地定义
    # 这里只生成真正外部的（不在 _segments 中的）
    # 注意：_module_decls 中的名称是 "模块名_符号名" 经过 safe_func_name 转换的
    # 我们需要跳过那些已经在本地有定义的符号
    local_seg_safe_names = set()
    for seg_name in codegen._segments:
        safe = codegen._safe_func_name(seg_name)
        local_seg_safe_names.add(safe)
        # 同时把模块前缀的也加入（因为导出别名会生成这些名字）
        # 但别名和 define 不会冲突，只有 declare 和 define/alias 会冲突
        # 所以我们只需要从 _module_decls 中移除那些已经有本地定义的
    
    # 过滤 _module_decls：只保留真正外部的（不在本地段名中的）
    # 注意：_module_decls 中的名称是 safe name（如 f2），我们需要反向映射
    # 更简单的方法：直接清空 _module_decls，因为多模块编译时所有符号都有定义
    codegen._module_decls = []
    # 但为了未来支持真正的外部模块（如动态链接库），我们保留机制，只是当前清空

    # 生成全局初始化
    codegen._gen_global_init()

    # 生成类方法
    for cls_name, cls_def in codegen._classes.items():
        codegen._gen_typed_class_methods(cls_name, cls_def)

    # 生成所有段落函数
    for seg_name in codegen._segment_order:
        params = codegen._segments[seg_name]
        body = codegen._segment_bodies.get(seg_name, [])
        codegen._gen_typed_segment(seg_name, params, body)

    # 为所有模块生成导出名别名
    for mod in all_module_list:
        codegen._gen_exported_aliases(mod)

    # 生成 main 函数（主模块的顶层语句）
    codegen._gen_typed_main()

    ir = codegen.finalize()

    # IR 生成阶段验证
    errors = codegen._verify_module_ir(codegen._lines)
    if errors:
        error_msg = '\n'.join(f"  - {e}" for e in errors)
        raise RuntimeError(f"LLVM IR 验证失败，发现 {len(errors)} 个问题:\n{error_msg}")

    return ir


def compile_duan_project(source_path: str, output_path: str = None, verbose: bool = False,
                         target_platform: str = None, target: str = None,
                         optimize_level: int = 2, debug: bool = False,
                         optimize_size: bool = False, lto: bool = False, strip: bool = False):
    """
    编译段言项目为原生可执行文件（支持多模块）

    自动解析导入语句，递归编译依赖的模块，合并 IR 后编译。

    Args:
        source_path: 主源文件路径
        output_path: 输出路径
        verbose: 是否输出详细信息
        target_platform: 目标平台
        target: 目标架构（'x86_64'/'aarch64'/'arm64'），默认本地架构
        optimize_level: 优化级别（0-3），默认 2
        debug: 是否生成 DWARF 调试信息
        optimize_size: 是否启用 -Os 尺寸优化（替代 -O2）
        lto: 是否启用 LTO (Link Time Optimization)
        strip: 是否剥离调试符号
    """
    # 检测目标架构
    target_arch = detect_target_arch(target)
    if verbose:
        print(f"  目标架构: {target_arch}")

    try:
        from ..module_resolver import ModuleResolver
    except ImportError:
        from module_resolver import ModuleResolver

    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    source_dir = os.path.dirname(os.path.abspath(source_path))
    resolver = ModuleResolver(search_paths=[source_dir])

    # 递归收集所有依赖的模块
    sources = {}
    visited = set()

    def collect_modules(src, mod_name):
        if mod_name in visited:
            return
        visited.add(mod_name)
        sources[mod_name] = src

        # 解析导入
        parser = DuanParser()
        v3_mod = parser.parse(src)
        if v3_mod is None:
            return
        adapter = AstAdapter()
        module = adapter.convert_module(v3_mod)
        for imp in (getattr(module, 'imports', None) or []):
            dep_name = imp.module if hasattr(imp, 'module') else None
            if dep_name and dep_name not in visited:
                dep_path = resolver.find_module(dep_name)
                if dep_path and os.path.exists(dep_path):
                    with open(dep_path, 'r', encoding='utf-8') as f:
                        dep_src = f.read()
                    collect_modules(dep_src, dep_name)

    main_name = os.path.splitext(os.path.basename(source_path))[0]
    collect_modules(source, main_name)

    if verbose:
        print(f"[1/4] 收集到 {len(sources)} 个模块: {', '.join(sources.keys())}")

    # 编译所有模块
    ir = compile_modules_typed(sources, main_module=main_name, verbose=verbose, target_platform=target_platform, debug=debug)

    # 写入 .ll 文件
    base_path = output_path or source_path.replace('.duan', '')
    base_path = _strip_exe_ext(base_path)
    ll_path = base_path + '.ll'

    with open(ll_path, 'w', encoding='utf-8') as f:
        f.write(ir)

    if verbose:
        print(f"  IR 已写入: {ll_path} ({len(ir)} 字符)")

    # 根据目标架构查找编译器
    clang = find_clang(target_arch=target_arch)
    if verbose:
        print(f"  使用编译器: {clang}")

    # IR 验证
    verify_ir_with_clang(ll_path, clang, verbose)

    # 编译 typed 运行时库
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    runtime_c = os.path.join(runtime_dir, 'runtime_typed.c')
    runtime_o = base_path + '_runtime.o'

    # 使用优化级别对应的编译参数
    opt_flags = get_optimization_flags(optimize_level, optimize_size=optimize_size, lto=lto)
    arch_flags = get_arch_specific_cflags(target_arch)
    debug_flags = ['-g'] if debug else []

    if verbose:
        print("[3/5] 编译 typed 运行时库...")

    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, runtime_c, '-o', runtime_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"运行时库编译失败:\n{result.stderr}")

    # 编译 .ll 为 .o
    if verbose:
        print("[4/5] 编译 LLVM IR...")

    ir_o = base_path + '.o'
    result = subprocess.run(
        [clang, '-c', *opt_flags, *arch_flags, *debug_flags, ll_path, '-o', ir_o],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"IR 编译失败:\n{result.stderr}")

    # 链接为可执行文件
    exe_ext = get_exe_extension()
    exe_path = base_path + exe_ext
    if verbose:
        print(f"[5/5] 链接为可执行文件...")

    link_args = [clang, *arch_flags, ir_o, runtime_o, '-o', exe_path]
    if debug:
        link_args.append('-g')
    if not sys.platform.startswith('win'):
        link_args.append('-lm')
    if lto:
        link_args.append('-flto')

    result = subprocess.run(
        link_args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        raise RuntimeError(f"链接失败:\n{result.stderr}")

    # 剥离调试符号
    original_size = os.path.getsize(exe_path) if os.path.exists(exe_path) else 0
    if strip and not debug:
        try:
            if sys.platform == 'win32':
                for tool in ['llvm-strip', 'strip']:
                    try:
                        subprocess.run([tool, exe_path], capture_output=True, timeout=30)
                        break
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
            else:
                subprocess.run(['strip', exe_path], check=True, timeout=30)
        except (subprocess.SubprocessError, OSError):
            if verbose:
                print("  [警告] 无法剥离调试符号")

    if verbose:
        for f in [ir_o, runtime_o]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        final_size = os.path.getsize(exe_path)
        print(f"编译成功: {source_path} -> {exe_path} ({final_size} 字节)")
        if original_size > 0 and strip:
            print(get_size_reduction_summary(original_size, final_size))

    return exe_path


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='段言 LLVM 编译器')
    ap.add_argument('source', help='.duan 源文件')
    ap.add_argument('output', nargs='?', help='输出 .exe 路径')
    ap.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    ap.add_argument('--ir-only', action='store_true', help='仅生成 LLVM IR，不编译为 .exe')
    ap.add_argument('--optimize-size', action='store_true',
                    help='启用 -Os 尺寸优化，替代 -O2（可减少 30-50% 体积）')
    ap.add_argument('--lto', action='store_true',
                    help='启用 LTO (Link Time Optimization)，进一步优化体积和性能')
    ap.add_argument('--strip', action='store_true',
                    help='剥离调试符号，减小最终二进制体积')
    args = ap.parse_args()

    try:
        if args.ir_only:
            source = open(args.source, 'r', encoding='utf-8').read()
            output_ll = (args.output or args.source).replace('.duan', '.ll')
            compile_source_to_ir(source, output_ll, verbose=True)
        else:
            compile_duan(args.source, args.output, verbose=args.verbose or True,
                         optimize_size=args.optimize_size, lto=args.lto, strip=args.strip)
    except Exception as e:
        print(f"编译错误: {e}", file=sys.stderr)
        sys.exit(1)