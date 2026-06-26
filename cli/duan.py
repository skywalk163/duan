#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言（Duan）编译器命令行工具 — 统一入口（默认使用 ANTLR 后端）

用法：
  duan run <源文件.duan>            解释执行
  duan compile <源文件.duan> [-o 输出]  编译为 Python 文件
  duan ast <源文件.duan>            显示 AST
  duan tokens <源文件.duan>         显示 Token 流
  duan --help
  duan --version

示例：
  duan run hello.duan                # 用 ANTLR 解释器执行
  duan compile hello.duan -o out.py  # 编译为 Python
  duan compile hello.duan --src      # 用旧版 src 后端编译
"""

import sys
import os
import argparse
from pathlib import Path

# ── 路径设置 ──────────────────────────────────────────────────────
_CLI_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_CLI_DIR)

# 确保各模块路径可访问
sys.path.insert(0, os.path.join(_PROJECT_DIR, 'antlrparser'))
sys.path.insert(0, os.path.join(_PROJECT_DIR, 'src'))
sys.path.insert(0, _PROJECT_DIR)

VERSION = '段言编译器 v1.7.0'


# ═══════════════════════════════════════════════════════════════════
# ANTLR 后端（默认）
# ═══════════════════════════════════════════════════════════════════

def _run_antlr(source: str) -> str:
    """用 ANTLR 解释器执行代码，返回输出"""
    from duan_visitor import DuanParser
    from duan_interpreter import Interpreter

    parser = DuanParser()
    module = parser.parse(source)
    if module is None:
        errors = '\n'.join(parser.errors)
        raise RuntimeError(f"解析失败:\n{errors}")

    interpreter = Interpreter()
    interpreter.interpret(module)
    return interpreter.get_output()


def _ast_antlr(source: str):
    """用 ANTLR 后端构建并打印 AST"""
    from duan_visitor import DuanParser

    parser = DuanParser()
    module = parser.parse(source)
    if module is None:
        errors = '\n'.join(parser.errors)
        raise RuntimeError(f"解析失败:\n{errors}")
    _print_ast(module)


# ═══════════════════════════════════════════════════════════════════
# SRC 后端（旧版）
# ═══════════════════════════════════════════════════════════════════

def _compile_src(source: str) -> str:
    """用 src 后端编译为 Python 代码"""
    from duan_parser_v3 import DuanParser
    from code_generator import PythonCodeGenerator

    parser = DuanParser()
    module = parser.parse(source)

    generator = PythonCodeGenerator()
    return generator.generate(module)


def _run_src(source: str, file_path: str | None = None) -> str:
    """用 src 后端执行，返回输出"""
    import os

    py_code = _compile_src(source)
    output_lines = []

    def _capture_print(*args, **kwargs):
        line = ' '.join(str(a) for a in args)
        output_lines.append(line)

    namespace = {'print': _capture_print, '__name__': '__main__'}
    if file_path:
        namespace['__file__'] = os.path.abspath(file_path)
    exec(py_code, namespace)
    return '\n'.join(output_lines)


def _tokens_src(source: str) -> list:
    """用 src 后端获取 Token 流"""
    from lexer import Lexer
    lexer = Lexer()
    return lexer.tokenize(source)


def _ast_src(source: str):
    """用 src 后端构建并打印 AST"""
    from duan_parser_v3 import DuanParser
    parser = DuanParser()
    module = parser.parse(source)
    _print_ast(module)


# ═══════════════════════════════════════════════════════════════════
# 通用工具
# ═══════════════════════════════════════════════════════════════════

def _print_ast(node, indent=0):
    """递归打印 AST 节点"""
    prefix = "  " * indent
    node_type = type(node).__name__
    print(f"{prefix}{node_type}")

    if hasattr(node, '__dict__'):
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                print(f"{prefix}  {key}:")
                for item in value:
                    if hasattr(item, '__dict__'):
                        _print_ast(item, indent + 2)
                    else:
                        print(f"{'  ' * (indent + 2)}{item}")
            elif hasattr(value, '__dict__'):
                print(f"{prefix}  {key}:")
                _print_ast(value, indent + 2)
            elif value is not None:
                print(f"{prefix}  {key}: {value}")


def _read_source(file_path: str) -> str:
    """读取源代码文件"""
    path = Path(file_path)
    if not path.exists():
        print(f"错误: 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding='utf-8')


# ═══════════════════════════════════════════════════════════════════
# 子命令实现
# ═══════════════════════════════════════════════════════════════════

def cmd_run(args):
    """解释执行段言源代码"""
    source = _read_source(args.file)

    try:
        if args.backend == 'src':
            output = _run_src(source, file_path=args.file)
            if output:
                print(output)
        else:
            # ANTLR 解释器内部已直接打印到控制台
            _run_antlr(source)

    except Exception as e:
        print(f"运行错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cmd_compile(args):
    """编译段言源代码为 Python 文件或可执行文件"""
    source = _read_source(args.file)

    # LLVM 后端：直接编译为原生 .exe
    if args.backend == 'llvm':
        try:
            from duan_llvm import compile_duan
            output = args.output or (Path(args.file).stem + '.exe')
            compile_duan(args.file, output, verbose=args.verbose)
            return
        except Exception as e:
            print(f"LLVM 编译错误: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    try:
        if args.backend == 'src':
            py_code = _compile_src(source)
        else:
            # ANTLR 后端：使用 code_generator_unified 生成 Python
            from duan_visitor import DuanParser
            from code_generator_unified import UnifiedCodeGenerator

            parser = DuanParser()
            module = parser.parse(source)
            if module is None:
                errors = '\n'.join(parser.errors)
                raise RuntimeError(f"解析失败:\n{errors}")
            generator = UnifiedCodeGenerator()
            py_code = generator.generate(module)

    except Exception as e:
        print(f"编译错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # 确定输出路径
    output_path = args.output or (Path(args.file).stem + '.py')
    output_path = Path(output_path)

    # 如果目标是 .exe，使用 PyInstaller 打包
    if output_path.suffix.lower() == '.exe':
        _compile_to_exe(py_code, output_path, args)
    else:
        output_path.write_text(py_code, encoding='utf-8')
        print(f"编译成功: {args.file} -> {output_path}")


def _compile_to_exe(py_code: str, exe_path: Path, args):
    """使用 PyInstaller 将 Python 代码打包为 .exe"""
    import tempfile
    import subprocess
    import shutil

    exe_name = exe_path.stem
    exe_dir = exe_path.parent.resolve()

    # 写入临时 .py 文件
    py_path = exe_dir / f"{exe_name}.py"
    py_path.write_text(py_code, encoding='utf-8')
    print(f"生成 Python 代码: {py_path}")

    # 调用 PyInstaller 打包
    print(f"正在打包为 .exe（使用 PyInstaller）...")
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'PyInstaller',
                '--onefile', '--console',
                '--name', exe_name,
                '--distpath', str(exe_dir),
                '--workpath', str(exe_dir / 'build'),
                '--specpath', str(exe_dir / 'build'),
                str(py_path),
            ],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=str(exe_dir),
        )
        if result.returncode != 0:
            # 输出 PyInstaller 的错误信息
            error_msg = result.stderr or result.stdout
            if error_msg:
                # 只显示最后几行关键错误
                lines = error_msg.strip().split('\n')
                print(f"PyInstaller 错误:\n{'\n'.join(lines[-10:])}", file=sys.stderr)
            raise RuntimeError(f"PyInstaller 打包失败 (exit code {result.returncode})")

        # 清理构建文件
        build_dir = exe_dir / 'build'
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)

        print(f"编译成功: {args.file} -> {exe_path}")

    except FileNotFoundError:
        print("错误: 未找到 PyInstaller。请运行: pip install pyinstaller", file=sys.stderr)
        print(f"已生成 Python 文件: {py_path}，可直接用 python 运行", file=sys.stderr)
        sys.exit(1)


def cmd_ast(args):
    """显示 AST"""
    source = _read_source(args.file)

    try:
        if args.backend == 'src':
            _ast_src(source)
        else:
            _ast_antlr(source)
    except Exception as e:
        print(f"AST 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cmd_tokens(args):
    """显示 Token 流"""
    source = _read_source(args.file)

    try:
        tokens = _tokens_src(source)
        print("Token 流:")
        print("-" * 60)
        for i, token in enumerate(tokens, 1):
            print(f"{i:3d}. {token}")
    except Exception as e:
        print(f"Token 分析错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog='duan',
        description='段言（Duan）编程语言编译器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  duan run hello.duan                 解释执行
  duan compile hello.duan             编译为 Python 文件
  duan compile hello.duan --src       用旧版后端编译
  duan ast hello.duan                 显示 AST
  duan tokens hello.duan              显示 Token 流
  duan --version                      显示版本
        """
    )

    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # ── run ──
    run_p = subparsers.add_parser('run', help='解释执行段言源代码')
    run_p.add_argument('file', help='源文件路径')
    run_p.add_argument('--backend', choices=['antlr', 'src'], default='antlr',
                       help='使用的后端（默认: antlr）')

    # ── compile ──
    comp_p = subparsers.add_parser('compile', help='编译为 Python 文件')
    comp_p.add_argument('file', help='源文件路径')
    comp_p.add_argument('-o', '--output', help='输出文件路径（默认: 同名 .py）')
    comp_p.add_argument('--backend', choices=['antlr', 'src', 'llvm'], default='antlr',
                        help='使用的后端（默认: antlr，llvm=原生编译）')

    # ── ast ──
    ast_p = subparsers.add_parser('ast', help='显示 AST')
    ast_p.add_argument('file', help='源文件路径')
    ast_p.add_argument('--backend', choices=['antlr', 'src'], default='antlr',
                       help='使用的后端（默认: antlr）')

    # ── tokens ──
    tok_p = subparsers.add_parser('tokens', help='显示 Token 流')
    tok_p.add_argument('file', help='源文件路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'run':
        cmd_run(args)
    elif args.command == 'compile':
        cmd_compile(args)
    elif args.command == 'ast':
        cmd_ast(args)
    elif args.command == 'tokens':
        cmd_tokens(args)


if __name__ == '__main__':
    main()