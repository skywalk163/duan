#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言（Duan）编译器命令行工具 — 统一入口（默认使用 SRC 后端）

用法：
  duan run <源文件.duan>            解释执行
  duan compile <源文件.duan> [-o 输出]  编译为 Python 文件
  duan ast <源文件.duan>            显示 AST
  duan tokens <源文件.duan>         显示 Token 流
  duan --help
  duan --version

示例：
  duan run hello.duan                # 用 SRC 后端执行（无需额外依赖）
  duan run hello.duan --backend antlr  # 用 ANTLR 后端执行（需安装 antlr4-python3-runtime）
  duan compile hello.duan -o out.py  # 编译为 Python
"""

import re
import sys
import os
import argparse
import subprocess
from pathlib import Path

# ── 路径设置 ──────────────────────────────────────────────────────
_CLI_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_CLI_DIR)

# 确保各模块路径可访问
sys.path.insert(0, os.path.join(_PROJECT_DIR, 'antlrparser'))
sys.path.insert(0, os.path.join(_PROJECT_DIR, 'src'))
sys.path.insert(0, _PROJECT_DIR)

VERSION = '段言编译器 v1.9.0'


# ═══════════════════════════════════════════════════════════════════
# ANTLR 后端（默认）
# ═══════════════════════════════════════════════════════════════════

def _preprocess_v3(source: str) -> str:
    """预处理 v3 纯缩进语法（转换为带结束标记的形式）"""
    from indent_preprocessor import preprocess_v3_syntax
    return preprocess_v3_syntax(source)


def _run_antlr(source: str) -> str:
    """用 ANTLR 解释器执行代码，返回输出"""
    from duan_visitor import DuanParser
    from duan_interpreter import Interpreter

    # 预处理 v3 语法
    processed_source = _preprocess_v3(source)

    parser = DuanParser()
    module = parser.parse(processed_source)
    if module is None:
        errors = '\n'.join(parser.errors)
        raise RuntimeError(f"解析失败:\n{errors}")

    interpreter = Interpreter()
    interpreter.interpret(module)
    return interpreter.get_output()


def _ast_antlr(source: str):
    """用 ANTLR 后端构建并打印 AST"""
    from duan_visitor import DuanParser

    # 预处理 v3 语法
    processed_source = _preprocess_v3(source)

    parser = DuanParser()
    module = parser.parse(processed_source)
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

    # 解析优化级别（'O0' -> 0, 'O1' -> 1, etc.）
    opt_level = 2
    if args.optimize and args.optimize.startswith('O'):
        try:
            opt_level = int(args.optimize[1:])
        except ValueError:
            opt_level = 2

    # LLVM 后端（模式1：字符串模式）
    if args.backend == 'llvm':
        try:
            from src.llvm.compiler import compile_duan
            output = args.output or (Path(args.file).stem + '.exe')
            compile_duan(args.file, output, verbose=args.verbose,
                         optimize_level=opt_level, debug=args.debug)
            return
        except ImportError:
            try:
                from llvm.compiler import compile_duan
            except ImportError:
                from ..llvm.compiler import compile_duan
            output = args.output or (Path(args.file).stem + '.exe')
            compile_duan(args.file, output, verbose=args.verbose,
                         optimize_level=opt_level, debug=args.debug)
            return
        except Exception as e:
            print(f"LLVM (string) 编译错误: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    # LLVM 后端（模式2：typed 模式，使用 DuanValue 结构体）
    if args.backend == 'llvm-typed':
        try:
            from src.llvm.compiler import compile_duan_typed
            output = args.output or (Path(args.file).stem + '.exe')
            compile_duan_typed(args.file, output, verbose=args.verbose,
                               optimize_level=opt_level, debug=args.debug)
            return
        except ImportError:
            try:
                from llvm.compiler import compile_duan_typed
            except ImportError:
                from ..llvm.compiler import compile_duan_typed
            output = args.output or (Path(args.file).stem + '.exe')
            compile_duan_typed(args.file, output, verbose=args.verbose,
                               optimize_level=opt_level, debug=args.debug)
            return
        except Exception as e:
            print(f"LLVM (typed) 编译错误: {e}", file=sys.stderr)
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

            # 预处理 v3 语法
            processed_source = _preprocess_v3(source)

            parser = DuanParser()
            module = parser.parse(processed_source)
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


def cmd_check(args):
    """语法检查：解析源代码但不执行"""
    source = _read_source(args.file)

    errors = []
    warnings = []

    try:
        if args.backend == 'src':
            from duan_parser_v3 import DuanParser
            parser = DuanParser()
            module = parser.parse(source)
            if module is None:
                errors.append("解析失败")
        else:
            from duan_visitor import DuanParser
            from code_generator_unified import UnifiedCodeGenerator
            processed_source = _preprocess_v3(source)
            parser = DuanParser()
            module = parser.parse(processed_source)
            if module is None:
                errors.extend(parser.errors)
    except Exception as e:
        errors.append(str(e))

    # 简单统计
    lines = source.split('\n')
    stats = {
        'total_lines': len(lines),
        'code_lines': sum(1 for l in lines if l.strip() and not l.strip().startswith('#')),
        'comment_lines': sum(1 for l in lines if l.strip().startswith('#')),
    }

    print(f"检查文件: {args.file}")
    print(f"  总行数: {stats['total_lines']}")
    print(f"  代码行: {stats['code_lines']}")
    print(f"  注释行: {stats['comment_lines']}")

    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for err in errors:
            print(f"    - {err}")
        sys.exit(1)
    else:
        print(f"\n✅ 语法检查通过，未发现错误。")

    # 类型检查
    if args.type_check:
        _run_type_check(source, args.type_check, args.file)


def _run_type_check(source: str, level_str: str, file_path: str):
    """运行类型检查并输出结果"""
    from compiler import DuanCompiler
    from core.config import TypeCheckLevel

    level_map = {
        '签名': TypeCheckLevel.SIGNATURE, 'signature': TypeCheckLevel.SIGNATURE,
        '变量': TypeCheckLevel.VARIABLE, 'variable': TypeCheckLevel.VARIABLE,
        '表达式': TypeCheckLevel.EXPRESSION, 'expression': TypeCheckLevel.EXPRESSION,
    }
    level = level_map.get(level_str, TypeCheckLevel.EXPRESSION)

    # 创建编译器实例并配置类型检查级别
    compiler = DuanCompiler()
    compiler._config.type_check_level = level

    # 解析并运行类型检查
    result = compiler.compile(source, optimize=False)

    print(f"\n━━━ 类型检查（级别: {level_str}）━━━")

    if compiler.warnings:
        print(f"\n⚠ 警告 ({len(compiler.warnings)} 个):")
        for w in compiler.warnings:
            print(f"  {w}")

    type_errors = [e for e in compiler.errors if '类型错误' in e]
    if type_errors:
        print(f"\n❌ 类型错误 ({len(type_errors)} 个):")
        for e in type_errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ 类型检查通过")


def cmd_type_check(args):
    """独立类型检查命令"""
    source = _read_source(args.file)
    _run_type_check(source, args.level, args.file)


def cmd_init(args):
    """初始化段言项目（创建 package.toml 配置）"""
    from package_manager import PackageManager

    project_name = args.name
    project_dir = Path(project_name)

    if project_dir.exists():
        print(f"错误: 目录已存在: {project_dir}", file=sys.stderr)
        sys.exit(1)

    project_dir.mkdir(parents=True)
    (project_dir / 'src').mkdir()
    (project_dir / 'tests').mkdir()

    # 使用 PackageManager 创建 package.toml 与 主.duan
    pm = PackageManager(project_root=project_dir)
    if not pm.init_project(name=project_name):
        print("错误: 项目初始化失败", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 项目 '{project_name}' 初始化完成")
    print(f"   目录: {project_dir.resolve()}")
    print(f"   配置: package.toml")
    print(f"   入口: 主.duan")
    print(f"\n可用命令:")
    print(f"   duan pkg run                  运行项目")
    print(f"   duan pkg build                编译项目")
    print(f"   duan run {project_name}/主.duan      直接运行入口")


def cmd_pkg(args):
    """包管理子命令（统一入口：init/build/run/native）"""
    from package_manager import PackageManager

    project_root = Path(getattr(args, 'project', None) or '.').resolve()

    if args.pkg_command == 'init':
        name = args.name
        if name:
            # 在 ./name/ 子目录下初始化
            target_root = project_root / name
            if target_root.exists():
                print(f"错误: 目录已存在: {target_root}", file=sys.stderr)
                sys.exit(1)
            target_root.mkdir(parents=True)
            pkg_name = name
        else:
            target_root = project_root
            pkg_name = project_root.name
        pm = PackageManager(project_root=target_root)
        if pm.init_project(name=pkg_name):
            print(f"✅ 包 '{pkg_name}' 初始化完成")
            print(f"   配置: {target_root / 'package.toml'}")
            if pm.config:
                print(f"   入口: {target_root / pm.config.entry}")
        else:
            print("❌ 初始化失败", file=sys.stderr)
            sys.exit(1)

    elif args.pkg_command == 'build':
        pm = PackageManager(project_root=project_root)
        result = pm.build_project()
        if result.get('success'):
            print(f"✅ 构建成功")
            print(f"   入口: {result.get('entry', '')}")
            order = result.get('order', [])
            if order:
                print(f"   模块拓扑顺序: {' -> '.join(order)}")
        else:
            print("❌ 构建失败:", file=sys.stderr)
            for err in result.get('errors', []):
                print(f"   - {err}", file=sys.stderr)
            sys.exit(1)

    elif args.pkg_command == 'run':
        pm = PackageManager(project_root=project_root)
        ret = pm.run_project()
        if ret != 0:
            sys.exit(ret)

    elif args.pkg_command == 'native':
        pm = PackageManager(project_root=project_root)
        try:
            output = pm.build_project_native(
                output_path=args.output,
                verbose=args.verbose
            )
            print(f"✅ 原生编译成功: {output}")
        except Exception as e:
            print(f"❌ 原生编译失败: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    else:
        print(f"未知子命令: {args.pkg_command}", file=sys.stderr)
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# AI Copilot 子命令
# ═══════════════════════════════════════════════════════════════════

def _ensure_utf8():
    """确保 stdout 使用 UTF-8 编码"""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def _cmd_ai(args):
    """AI Copilot 入口"""
    _ensure_utf8()

    # 动态导入，避免影响非 AI 命令的启动速度
    _AI_DIR = os.path.join(_PROJECT_DIR, 'tools', 'ai_copilot')
    sys.path.insert(0, _AI_DIR)

    ai_cmd = getattr(args, 'ai_command', None)
    if not ai_cmd:
        print('用法: duan ai <子命令> [选项]')
        print('子命令: prompt, card, snippets, examples, check')
        return

    if ai_cmd == 'prompt':
        from prompt_generator import generate_prompt
        mode = args.mode or 'auto'
        compact = not args.full
        user_input = args.input
        if os.path.isfile(user_input):
            with open(user_input, encoding='utf-8') as f:
                user_input = f.read()
        prompt = generate_prompt(user_input, mode=mode, compact=compact)
        print(prompt)

    elif ai_cmd == 'card':
        from syntax_card import generate_syntax_card
        compact = not args.full
        card = generate_syntax_card(compact=compact, include_verbs=args.verbs)
        print(card)

    elif ai_cmd == 'snippets':
        from snippets import list_snippets, get_snippet
        if args.name:
            snippet = get_snippet(args.name)
            if not snippet:
                print(f"片段不存在: {args.name}")
                return
            print(f"名称：{args.name}")
            print(f"用途：{snippet['desc']}")
            print(f"模板：\n{snippet['code']}")
            if 'example' in snippet:
                print(f"示例：\n{snippet['example']}")
            if 'pitfall' in snippet:
                print(f"⚠暗坑：{snippet['pitfall']}")
        else:
            print(list_snippets())

    elif ai_cmd == 'examples':
        from syntax_card import generate_example_pairs
        print(generate_example_pairs())

    elif ai_cmd == 'check':
        filepath = args.file
        if not os.path.isfile(filepath):
            print(f"文件不存在: {filepath}")
            return

        # ── 后端感知检测 ──
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        _LLVM_KEYWORDS = {
            '类': 'class 定义',
            '继承': '类继承',
            '构造': '构造函数',
            '属性': '类属性',
            '方法': '类方法',
            '静态方法': '静态方法',
            '抽象': '抽象类/方法',
        }
        detected = []
        for kw, desc in _LLVM_KEYWORDS.items():
            # 匹配独立关键字：前面不是标识符字符，后面是空格/冒号/换行/括号
            if re.search(r'(?<![a-zA-Z0-9_\u4e00-\u9fff])' + re.escape(kw) + r'(?![a-zA-Z0-9_\u4e00-\u9fff])', source):
                detected.append((kw, desc))

        if detected:
            print(f"[0/2] ⚠ 后端感知检测")
            for kw, desc in detected:
                print(f"  · 检测到「{kw}」({desc})")
            print(f"  → 类系统在 SRC 后端下运行无输出，建议使用 LLVM 后端：")
            print(f"     duan compile {filepath} --backend llvm-typed")
            print()

        # 语法检查
        print(f"[1/2] 语法检查: {filepath}")
        result = subprocess.run(
            [sys.executable, '-X', 'utf8', '-m', 'cli.duan', 'check', filepath],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            cwd=_PROJECT_DIR,
        )
        if result.returncode != 0:
            print(f"  ✗ 语法检查失败:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        else:
            print(f"  ✓ 语法检查通过")

        if args.run:
            print(f"[2/2] 运行测试: {filepath}")
            try:
                result = subprocess.run(
                    [sys.executable, '-X', 'utf8', '-m', 'cli.duan', 'run', filepath],
                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                    cwd=_PROJECT_DIR,
                    timeout=args.timeout,
                )
                if result.returncode != 0:
                    print(f"  ✗ 运行失败:")
                    if result.stdout:
                        print(result.stdout)
                    if result.stderr:
                        print(result.stderr)
                else:
                    print(f"  ✓ 运行成功")
                    if result.stdout and result.stdout.strip():
                        print(f"  输出:")
                        for line in result.stdout.strip().split('\n'):
                            print(f"    {line}")
            except subprocess.TimeoutExpired:
                print(f"  ✗ 运行超时（{args.timeout}秒）")
        else:
            print("[2/2] 跳过运行检查（使用 --run 启用）")

    elif ai_cmd == 'generate':
        from pipeline import generate_pipeline
        prompt = generate_pipeline(
            requirement=args.requirement,
            model_size=args.model_size,
            mode=args.mode,
        )
        print(prompt)

    elif ai_cmd == 'fix':
        from pipeline import fix_pipeline
        if not os.path.isfile(args.file):
            print(f"文件不存在: {args.file}")
            return
        prompt = fix_pipeline(
            filepath=args.file,
            error=args.error,
            model_size=args.model_size,
        )
        print(prompt)


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
    run_p.add_argument('--backend', choices=['antlr', 'src'], default='src',
                       help='使用的后端（默认: src，无需额外依赖；antlr 需安装 antlr4-python3-runtime）')

    # ── compile ──
    comp_p = subparsers.add_parser('compile', help='编译为 Python 文件')
    comp_p.add_argument('file', help='源文件路径')
    comp_p.add_argument('-o', '--output', help='输出文件路径（默认: 同名 .py）')
    comp_p.add_argument('--backend', choices=['antlr', 'src', 'llvm', 'llvm-typed'], default='src',
                        help='使用的后端（默认: src；antlr 需安装 antlr4-python3-runtime；llvm 需安装 LLVM）')
    comp_p.add_argument('--optimize', choices=['O0', 'O1', 'O2', 'O3'], default='O2',
                        help='LLVM 优化级别（默认: O2）')
    comp_p.add_argument('--debug', action='store_true',
                        help='生成 DWARF 调试信息')

    # ── ast ──
    ast_p = subparsers.add_parser('ast', help='显示 AST')
    ast_p.add_argument('file', help='源文件路径')
    ast_p.add_argument('--backend', choices=['antlr', 'src'], default='src',
                       help='使用的后端（默认: src）')

    # ── tokens ──
    tok_p = subparsers.add_parser('tokens', help='显示 Token 流')
    tok_p.add_argument('file', help='源文件路径')

    # ── check ──
    check_p = subparsers.add_parser('check', help='语法检查')
    check_p.add_argument('file', help='源文件路径')
    check_p.add_argument('--backend', choices=['antlr', 'src'], default='src',
                         help='使用的后端（默认: src）')
    check_p.add_argument('--type-check', choices=['签名', '变量', '表达式', 'signature', 'variable', 'expression'],
                         default=None, help='启用类型检查并指定级别')

    # ── type-check ──
    tc_p = subparsers.add_parser('type-check', help='独立类型检查')
    tc_p.add_argument('file', help='源文件路径')
    tc_p.add_argument('--level', choices=['签名', '变量', '表达式', 'signature', 'variable', 'expression'],
                      default='表达式', help='类型检查级别（默认: 表达式）')

    # ── init ──
    init_p = subparsers.add_parser('init', help='初始化段言项目')
    init_p.add_argument('name', help='项目名称')

    # ── pkg ──
    pkg_p = subparsers.add_parser('pkg', help='包管理（init/build/run/native）')
    pkg_p.add_argument('--project', '-p', default='.', help='项目根目录（默认: 当前目录）')
    pkg_sub = pkg_p.add_subparsers(dest='pkg_command', help='包管理子命令')

    pkg_init = pkg_sub.add_parser('init', help='初始化新包（创建 package.toml 与 主.duan）')
    pkg_init.add_argument('name', nargs='?', default=None, help='包名（默认: 目录名）')

    pkg_sub.add_parser('build', help='编译整个项目')

    pkg_sub.add_parser('run', help='运行项目入口')

    pkg_native = pkg_sub.add_parser('native', help='使用 LLVM 后端编译为原生可执行文件')
    pkg_native.add_argument('-o', '--output', default=None, help='输出文件路径')
    pkg_native.add_argument('-v', '--verbose', action='store_true', help='详细输出')

    # ── ai ──
    ai_p = subparsers.add_parser('ai', help='AI Copilot 辅助工具（算力不足场景下的段言代码生成）')
    ai_sub = ai_p.add_subparsers(dest='ai_command', help='AI 子命令')

    ai_prompt = ai_sub.add_parser('prompt', help='生成让 AI 写段言代码的 prompt')
    ai_prompt.add_argument('input', help='需求描述或 Python 代码（也支持文件路径）')
    ai_prompt.add_argument('--mode', choices=['auto', 'translate', 'create', 'paragraph'],
                           default='auto', help='生成模式（默认 auto 自动检测）')
    ai_prompt.add_argument('--full', action='store_true', help='使用完整语法卡（默认精简卡）')

    ai_card = ai_sub.add_parser('card', help='输出段言语法速查卡')
    ai_card.add_argument('--full', action='store_true', help='完整版（默认精简版）')
    ai_card.add_argument('--verbs', action='store_true', help='包含动词参数参照表')

    ai_snippets = ai_sub.add_parser('snippets', help='列出代码片段库')
    ai_snippets.add_argument('name', nargs='?', help='查看指定片段详情')

    ai_sub.add_parser('examples', help='Python→段言对照示例')

    ai_check = ai_sub.add_parser('check', help='校验段言代码（语法+运行+后端感知）')
    ai_check.add_argument('file', help='段言代码文件路径')
    ai_check.add_argument('--run', action='store_true', help='同时运行测试')
    ai_check.add_argument('--timeout', type=int, default=10, help='运行超时秒数（默认10）')

    ai_gen = ai_sub.add_parser('generate', help='★ 一键生成：需求→完整prompt（推荐）')
    ai_gen.add_argument('requirement', help='代码需求描述，如"写一个冒泡排序"')
    ai_gen.add_argument('--model-size', choices=['small', 'medium', 'large'],
                        default='medium', help='目标模型大小（默认medium）：small≤7B / medium7-14B / large≥14B')
    ai_gen.add_argument('--mode', choices=['auto', 'translate', 'create', 'paragraph'],
                        default='auto', help='生成模式（默认auto）')

    ai_fix = ai_sub.add_parser('fix', help='★ 一键修复：出错代码→修复prompt')
    ai_fix.add_argument('file', help='出错的段言代码文件路径')
    ai_fix.add_argument('error', help='错误信息（可用引号包裹）')
    ai_fix.add_argument('--model-size', choices=['small', 'medium', 'large'],
                        default='medium', help='目标模型大小（默认medium）')

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
    elif args.command == 'check':
        cmd_check(args)
    elif args.command == 'type-check':
        cmd_type_check(args)
    elif args.command == 'init':
        cmd_init(args)
    elif args.command == 'ai':
        _cmd_ai(args)
    elif args.command == 'pkg':
        if not getattr(args, 'pkg_command', None):
            parser.parse_args(['pkg', '--help'])
        else:
            cmd_pkg(args)


if __name__ == '__main__':
    main()