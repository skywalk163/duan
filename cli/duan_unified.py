#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 统一命令行工具 v2.0

用法：
  duan <源文件.duan> [选项]
  duan run <源文件.duan>
  duan compile <源文件.duan> [-o <输出>]
  duan repl
  duan --help

示例：
  duan hello.duan                    # 编译并运行（使用ANTLR后端）
  duan hello.duan --backend src      # 使用src手写解析器
  duan run hello.duan                # 解释执行
  duan compile hello.duan -o hello.py
  duan repl                          # 启动REPL
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, List

# 添加路径 - 先尝试本地路径（开发模式），再尝试已安装路径
_local_src = str(Path(__file__).parent.parent / 'src')
_local_antlr = str(Path(__file__).parent.parent / 'antlrparser')

if os.path.isdir(_local_src):
    sys.path.insert(0, _local_src)
if os.path.isdir(_local_antlr):
    sys.path.insert(0, _local_antlr)

# 已安装版本（pip install），将 src 下模块暴露到顶层路径
try:
    import src as _src_pkg
    _installed_src = str(Path(_src_pkg.__file__).parent)
    if _installed_src not in sys.path and os.path.isdir(_installed_src):
        sys.path.insert(0, _installed_src)
except ImportError:
    pass


class DuanUnifiedCLI:
    """段言统一CLI"""
    
    def __init__(self):
        self.antlr_available = self._check_antlr()
        self.src_available = self._check_src()
    
    def _check_antlr(self) -> bool:
        """检查ANTLR后端是否可用"""
        try:
            from antlr4 import InputStream, CommonTokenStream
            from DuanLangLexer import DuanLangLexer
            from DuanLangParser import DuanLangParser
            from duan_visitor import DuanLangASTBuilder
            from code_generator_unified import UnifiedCodeGenerator
            return True
        except ImportError:
            return False
    
    def _check_src(self) -> bool:
        """检查src手写解析器是否可用"""
        try:
            from lexer import Lexer
            from duan_parser_v3 import DuanParser
            from code_generator import PythonCodeGenerator
            return True
        except ImportError:
            return False
    
    def compile_with_antlr(self, source: str, output_file: Optional[str] = None, run: bool = False) -> int:
        """使用ANTLR后端编译"""
        from duan_visitor import DuanParser
        from code_generator_unified import UnifiedCodeGenerator
        
        # 使用 DuanParser 进行完整的预处理（_auto_close_blocks、_preprocess_async 等）
        duan_parser = DuanParser()
        module = duan_parser.parse(source)
        
        if duan_parser.errors:
            for error in duan_parser.errors:
                print(error, file=sys.stderr)
            return 1
        
        if module is None:
            print("[错误] 解析失败", file=sys.stderr)
            return 1
        
        # 代码生成
        generator = UnifiedCodeGenerator()
        python_code = generator.generate(module)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(python_code)
            print(f"[成功] 已生成: {output_file}")
        
        if run:
            # 执行代码
            try:
                # 创建执行环境，包含必要的内置变量
                exec_globals = {
                    '__name__': '__main__',
                    '__file__': output_file or '<duan_script>',
                    '__builtins__': __builtins__,
                }
                exec(python_code, exec_globals)
            except Exception as e:
                print(f"[运行错误] {e}", file=sys.stderr)
                return 1
        
        return 0
    
    def _resolve_user_module_imports(self, source: str, source_dir: str,
                                      resolved: set = None) -> str:
        """解析用户自定义模块导入，将模块源码内联到主源码中。

        src 后端在生成 Python 代码时，会将 `从 清洗器 导入 ...` 直接翻译为
        `from 清洗器 import ...`，但 Python 解析器无法识别中文模块名。
        本方法在解析前将用户自定义模块的源码内联，消除跨模块导入依赖。

        Args:
            source: 源代码
            source_dir: 源文件所在目录（用于查找模块文件）
            resolved: 已解析的模块名集合（避免循环依赖）

        Returns:
            内联后的源码（所有用户模块已内联为单一源码）
        """
        import re
        import os
        from duan_parser_v3 import DuanParser, ImportStmt

        if resolved is None:
            resolved = set()

        # 已知的标准库 / Python 模块名（不应被内联）
        KNOWN_STDLIB = {
            '文件系统', 'JSON', 'sys', '字符串工具', '数学', '时间', '日期时间',
            'csv', 'json', 'os', 're', 'random', 'math', 'datetime', 'time',
            'pathlib', 'typing', 'collections', 'itertools', 'functools',
            'subprocess', 'shutil', 'glob', 'tempfile', 'io', 'builtins',
            '复制', 'os路径',
        }

        # 解析源码以提取导入语句
        parser = DuanParser()
        module = parser.parse(source)
        if not module:
            return source

        # 收集用户自定义模块导入
        replacements = []
        for stmt in getattr(module, 'statements', []):
            if not isinstance(stmt, ImportStmt):
                continue
            mod_name = stmt.module_name
            if mod_name in resolved or mod_name in KNOWN_STDLIB:
                continue
            # 检查模块文件是否存在
            mod_path = os.path.join(source_dir, f"{mod_name}.duan")
            if not os.path.exists(mod_path):
                continue
            # 读取模块源码
            with open(mod_path, 'r', encoding='utf-8') as f:
                mod_source = f.read()
            # 递归解析模块中的导入
            resolved.add(mod_name)
            mod_source = self._resolve_user_module_imports(
                mod_source, source_dir, resolved
            )
            # 构建匹配导入语句的正则表达式
            # 格式: 从 模块名 导入 符号1, 符号2, ...
            # 或: 导入 模块名。
            # 使用 re.DOTALL 以支持多行符号列表
            if stmt.symbols:
                pattern = rf'从\s+{re.escape(mod_name)}\s+导入\s+.+?。'
            else:
                pattern = rf'导入\s+{re.escape(mod_name)}。'
            replacements.append((pattern, mod_source))

        # 逆序替换，保持行号位置正确
        for pattern, mod_source in reversed(replacements):
            source = re.sub(pattern, mod_source, source, count=1, flags=re.DOTALL)

        return source

    def compile_with_src(self, source: str, output_file: Optional[str] = None,
                         run: bool = False, target: str = 'python',
                         source_file: str = None) -> int:
        """使用src手写解析器编译
        
        Args:
            source: 源代码
            output_file: 输出文件路径
            run: 是否执行
            target: 目标格式 ('python' 或 'llvm')
            source_file: 源文件路径（用于解析用户模块导入）
        """
        from compiler import DuanCompiler
        
        compiler = DuanCompiler()
        
        if target == 'llvm':
            # LLVM IR 生成：只做解析和适配，跳过类型检查
            try:
                tokens = compiler.tokenize(source)
                raw_ast = compiler.parse_raw(source)
                module = compiler.adapt(raw_ast)
                
                if not module:
                    print("[语法错误] 解析失败", file=sys.stderr)
                    return 1
                
                llvm_ir = compiler.generate_llvm_ir(module)
                
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(llvm_ir)
                    print(f"[成功] 已生成 LLVM IR: {output_file}")
                else:
                    print(llvm_ir)
                
                return 0
            except Exception as e:
                print(f"[LLVM IR 生成错误] {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return 1
        else:
            # Python 代码生成：直接使用 v3 解析器 + 代码生成器
            # （注意：不走 DuanCompiler.compile 的 adapt 步骤 —— adapt 会把
            #   Paragraph/段落定义丢弃，导致运行时 NameError 或生成器报
            #   “未知语句类型 VariableDeclaration”，与 cli/duan.py 的
            #   _compile_src 保持一致的可用路径）

            # 解析用户自定义模块导入（内联 .duan 文件内容）
            if source_file:
                source_dir = os.path.dirname(os.path.abspath(source_file))
                source = self._resolve_user_module_imports(source, source_dir)

            from duan_parser_v3 import DuanParser
            from code_generator import PythonCodeGenerator

            parser = DuanParser()
            module = parser.parse(source)
            if not module:
                print("[语法错误] 解析失败", file=sys.stderr)
                return 1

            generator = PythonCodeGenerator()
            python_code = generator.generate(module)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(python_code)
                print(f"[成功] 已生成: {output_file}")
            
            if run:
                try:
                    exec_globals = {
                        '__name__': '__main__',
                        '__file__': output_file or '<duan_script>',
                        '__builtins__': __builtins__,
                    }
                    exec(python_code, exec_globals)
                except Exception as e:
                    print(f"[运行错误] {e}", file=sys.stderr)
                    return 1
            
            return 0
    
    def interpret_run(self, source_file: str, script_args: list = None) -> int:
        """使用编译器编译并运行（替代旧版解释器）
        
        Args:
            source_file: 源文件路径
            script_args: 传递给脚本的参数列表（不含文件路径）
        """
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source = f.read()
            # 设置脚本的 sys.argv
            old_argv = sys.argv
            sys.argv = [source_file] + (script_args or [])
            try:
                return self.compile_with_src(source, run=True, source_file=source_file)
            finally:
                sys.argv = old_argv
        except Exception as e:
            print(f"[运行错误] {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    
    def start_repl(self) -> int:
        """启动REPL"""
        try:
            # 先尝试导入 tools.repl（新位置）
            from tools.repl import DuanREPL
            repl = DuanREPL()
            repl.run()
            return 0
        except ImportError:
            pass
        
        try:
            # 再尝试导入 duan_repl（旧位置）
            from duan_repl import main as repl_main
            repl_main()
            return 0
        except ImportError:
            print("[错误] REPL模块不可用", file=sys.stderr)
            return 1
    
    def start_debug_repl(self) -> int:
        """启动调试REPL"""
        try:
            from tools.duan_debug_repl import DuanDebugREPL
            repl = DuanDebugREPL()
            repl.run()
            return 0
        except ImportError:
            print("[错误] 调试REPL模块不可用", file=sys.stderr)
            return 1
    
    def pkg_init(self, project_name: str) -> int:
        """创建新的段言项目骨架"""
        project_dir = Path(project_name)
        if project_dir.exists():
            print(f"[错误] 目录已存在: {project_dir}", file=sys.stderr)
            return 1

        project_dir.mkdir(parents=True)

        # main.duan - 示例入口文件
        main_duan = project_dir / 'main.duan'
        main_duan.write_text('''# 段言示例程序
# 这是 main.duan — 项目入口文件

设 甲 为 42。
打印("甲 = ", 甲)

段落 加法 接收 数甲, 数乙:
    返回 数甲 加 数乙。

设 结果 为 加法(3, 5)。
打印("3 + 5 = ", 结果)
''', encoding='utf-8')

        # duan.json - 项目配置文件
        duan_json = project_dir / 'duan.json'
        duan_json.write_text('''{
    "name": "%s",
    "version": "0.1.0",
    "entry": "main.duan",
    "description": "段言项目"
}
''' % project_name, encoding='utf-8')

        # build.py - 构建脚本
        build_py = project_dir / 'build.py'
        build_py.write_text('''#!/usr/bin/env python3
"""段言项目构建脚本 - 编译 .duan 文件为 .py"""

import os
import sys
import subprocess
from pathlib import Path


def build():
    """编译项目中所有 .duan 文件"""
    project_dir = Path(__file__).parent
    entry = project_dir / "main.duan"

    if not entry.exists():
        print(f"[错误] 入口文件不存在: {entry}")
        return False

    # 调用 duan compile
    result = subprocess.run(
        [sys.executable, "-m", "cli.duan_unified", "compile", str(entry)],
        capture_output=True, text=True, cwd=str(project_dir)
    )
    if result.returncode != 0:
        print(result.stderr or result.stdout)
        return False

    print(f"[成功] 已编译: {entry}")
    return True


if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
''', encoding='utf-8')

        print(f"[成功] 已创建项目: {project_name}/")
        print(f"  main.duan    入口文件")
        print(f"  duan.json    项目配置")
        print(f"  build.py     构建脚本")
        print(f"\n运行: duan run {project_name}/main.duan")
        print(f"构建: cd {project_name} && duan pkg build")
        return 0

    def pkg_build(self, project_dir: str = '.') -> int:
        """编译项目中的 .duan 文件为 .py"""
        root = Path(project_dir)
        if not root.is_dir():
            print(f"[错误] 目录不存在: {root}", file=sys.stderr)
            return 1

        duan_files = list(root.glob('*.duan'))
        if not duan_files:
            print(f"[错误] 未找到 .duan 文件: {root}", file=sys.stderr)
            return 1

        success_count = 0
        for f in duan_files:
            source = f.read_text(encoding='utf-8')
            output_file = f.with_suffix('.py')
            try:
                # 尝试 src 后端
                from duan_parser_v3 import DuanParser
                from code_generator import PythonCodeGenerator
                parser = DuanParser()
                module = parser.parse(source)
                if module is None:
                    print(f"[跳过] 解析失败: {f}", file=sys.stderr)
                    continue
                generator = PythonCodeGenerator()
                py_code = generator.generate(module)
                output_file.write_text(py_code, encoding='utf-8')
                print(f"[编译] {f.name} -> {output_file.name}")
                success_count += 1
            except ImportError:
                # 尝试 ANTLR 后端
                try:
                    from duan_visitor import DuanParser as DuanParser2
                    from code_generator_unified import UnifiedCodeGenerator
                    from indent_preprocessor import preprocess_v3_syntax
                    processed = preprocess_v3_syntax(source)
                    parser = DuanParser2()
                    module = parser.parse(processed)
                    if module is None:
                        print(f"[跳过] 解析失败: {f}", file=sys.stderr)
                        continue
                    generator = UnifiedCodeGenerator()
                    py_code = generator.generate(module)
                    output_file.write_text(py_code, encoding='utf-8')
                    print(f"[编译] {f.name} -> {output_file.name}")
                    success_count += 1
                except ImportError:
                    print(f"[错误] 无可用编译后端", file=sys.stderr)
                    return 1
            except Exception as e:
                print(f"[错误] 编译 {f.name} 失败: {e}", file=sys.stderr)
                continue

        print(f"\n[摘要] 成功: {success_count}/{len(duan_files)}")
        return 0 if success_count > 0 else 1

    def syntax_check(self, source_file: str) -> int:
        """检查文件语法是否正确"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source = f.read()

            # 尝试 src 后端解析
            try:
                from duan_parser_v3 import DuanParser
                parser = DuanParser()
                module = parser.parse(source)
                if module is None:
                    print("[语法错误] 解析失败", file=sys.stderr)
                    return 1
                if hasattr(parser, 'errors') and parser.errors:
                    for error in parser.errors:
                        print(error, file=sys.stderr)
                    return 1
                print("[通过] 语法检查通过")
                return 0
            except ImportError:
                pass

            # 尝试 ANTLR 后端解析
            try:
                from antlr4 import InputStream, CommonTokenStream
                from DuanLangLexer import DuanLangLexer
                from DuanLangParser import DuanLangParser
                from duan_visitor import DuanLangASTBuilder

                input_stream = InputStream(source)
                lexer = DuanLangLexer(input_stream)
                tokens = CommonTokenStream(lexer)
                parser = DuanLangParser(tokens)
                tree = parser.program()
                if parser.getNumberOfSyntaxErrors() > 0:
                    print("[语法错误] 存在语法错误", file=sys.stderr)
                    return 1
                print("[通过] 语法检查通过")
                return 0
            except ImportError:
                print("[错误] 无可用解析后端", file=sys.stderr)
                return 1
        except Exception as e:
            print(f"[错误] 语法检查失败: {e}", file=sys.stderr)
            return 1

    def show_ast(self, source: str, backend: str = 'antlr') -> int:
        """显示AST结构"""
        if backend == 'antlr':
            from antlr4 import InputStream, CommonTokenStream
            from DuanLangLexer import DuanLangLexer
            from DuanLangParser import DuanLangParser
            from duan_visitor import DuanLangASTBuilder
            
            input_stream = InputStream(source)
            lexer = DuanLangLexer(input_stream)
            tokens = CommonTokenStream(lexer)
            parser = DuanLangParser(tokens)
            tree = parser.program()
            builder = DuanLangASTBuilder()
            module = builder.visitProgram(tree)
        else:
            from duan_parser_v3 import DuanParser
            parser = DuanParser()
            module = parser.parse(source)
        
        if module:
            self._print_ast(module, 0)
            return 0
        else:
            print("[错误] 解析失败", file=sys.stderr)
            return 1
    
    def _print_ast(self, node, indent: int):
        """打印AST节点"""
        prefix = "  " * indent
        node_type = type(node).__name__
        
        if hasattr(node, 'name'):
            print(f"{prefix}{node_type}: {node.name}")
        else:
            print(f"{prefix}{node_type}")
        
        # 递归打印子节点
        for attr in ['statements', 'segments', 'classes', 'body', 'parameters', 'arguments']:
            if hasattr(node, attr):
                children = getattr(node, attr)
                if isinstance(children, list):
                    for child in children:
                        self._print_ast(child, indent + 1)
                elif children:
                    self._print_ast(children, indent + 1)


def main():
    """主函数"""
    # 中文别名映射表
    _cn_alias_map = {
        '运行': 'run',
        '编译': 'compile',
        '语法检查': 'check',
        '项目构建': 'pkg build',
        '原生编译': 'compile --target llvm',
        '交互式': 'repl',
        '调试': 'debug',
        '新建项目': 'pkg init',
        '版本': '--version',
        '帮助': '--help',
    }

    # 检查并转换中文别名
    if len(sys.argv) > 1 and sys.argv[1] in _cn_alias_map:
        mapped = _cn_alias_map[sys.argv[1]]
        mapped_parts = mapped.split()
        # 替换 sys.argv[1] 为映射后的英文命令
        # 例如 'duan 项目构建' → 'duan pkg build'
        # 例如 'duan 版本' → 'duan --version'
        sys.argv[1:2] = mapped_parts

    cli = DuanUnifiedCLI()
    
    # 检查是否是子命令模式
    if len(sys.argv) > 1 and sys.argv[1] in ['run', 'compile', 'repl', 'debug', 'pkg', 'check']:
        # 子命令模式
        parser = argparse.ArgumentParser(description='段言（Duan）编程语言编译器')
        subparsers = parser.add_subparsers(dest='command', help='子命令')
        
        # run 子命令
        run_parser = subparsers.add_parser('run', help='解释执行文件')
        run_parser.add_argument('file', help='源文件路径')
        
        # compile 子命令
        compile_parser = subparsers.add_parser('compile', help='编译文件')
        compile_parser.add_argument('file', help='源文件路径')
        compile_parser.add_argument('-o', '--output', help='输出文件路径')
        compile_parser.add_argument('--backend', choices=['antlr', 'src'], default='src',
                                   help='选择编译后端（默认：src）')
        compile_parser.add_argument('--target', choices=['py', 'js', 'wasm', 'llvm'], default='py',
                                   help='目标代码（默认：py，llvm 生成 LLVM IR）')
        
        # repl 子命令
        subparsers.add_parser('repl', help='启动交互式REPL')
        
        # debug 子命令
        debug_parser = subparsers.add_parser('debug', help='启动调试REPL')
        debug_parser.add_argument('file', nargs='?', help='要调试的文件路径（可选）')
        
        # check 子命令
        check_parser = subparsers.add_parser('check', help='语法检查')
        check_parser.add_argument('file', help='源文件路径')
        check_parser.add_argument('--backend', choices=['antlr', 'src'], default='src',
                                  help='选择解析后端（默认：src）')
        
        # pkg 子命令
        pkg_parser = subparsers.add_parser('pkg', help='项目管理（init/build）')
        pkg_sub = pkg_parser.add_subparsers(dest='pkg_command', help='pkg 子命令')
        
        pkg_init_parser = pkg_sub.add_parser('init', help='创建新项目骨架')
        pkg_init_parser.add_argument('name', help='项目名称')
        
        pkg_build_parser = pkg_sub.add_parser('build', help='编译项目中的 .duan 文件为 .py')
        pkg_build_parser.add_argument('--dir', default='.', help='项目目录（默认: 当前目录）')
        pkg_build_parser.add_argument('--incremental', action='store_true', help='使用增量编译（仅编译变更文件）')
        pkg_build_parser.add_argument('--force', '-f', action='store_true', help='强制全量编译（忽略增量缓存）')
        
        args, unknown = parser.parse_known_args()
        
        if args.command == 'run':
            if not os.path.exists(args.file):
                print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                return 1
            # 将未知参数作为脚本参数传递（--input, --output 等）
            return cli.interpret_run(args.file, script_args=unknown)
        
        elif args.command == 'compile':
            if not os.path.exists(args.file):
                print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                return 1
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            output_file = args.output or args.file.replace('.duan', '.py')
            
            if args.backend == 'antlr':
                return cli.compile_with_antlr(source, output_file=output_file, run=False)
            else:
                return cli.compile_with_src(source, output_file=output_file, run=False, target=args.target)
        
        elif args.command == 'repl':
            return cli.start_repl()
        
        elif args.command == 'debug':
            if args.file:
                # 调试模式下加载文件
                if not os.path.exists(args.file):
                    print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                    return 1
                from tools.duan_debug_repl import DuanDebugREPL
                repl = DuanDebugREPL()
                repl.load_file(args.file)
                return 0
            else:
                return cli.start_debug_repl()
        
        elif args.command == 'check':
            if not os.path.exists(args.file):
                print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                return 1
            return cli.syntax_check(args.file)
        
        elif args.command == 'pkg':
            if not getattr(args, 'pkg_command', None):
                pkg_parser.print_help()
                return 1
            if args.pkg_command == 'init':
                return cli.pkg_init(args.name)
            elif args.pkg_command == 'build':
                if getattr(args, 'incremental', False):
                    try:
                        from incremental_build import incremental_build_cli
                        result = incremental_build_cli(
                            project_dir=args.dir,
                            force=getattr(args, 'force', False),
                            verbose=True
                        )
                        return 0 if result == 0 else 1
                    except ImportError as e:
                        print(f"❌ 增量编译模块不可用: {e}", file=sys.stderr)
                        return 1
                else:
                    return cli.pkg_build(args.dir)
    
    else:
        # 默认模式：编译并运行
        parser = argparse.ArgumentParser(
            description='段言（Duan）编程语言编译器',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例：
  duan hello.duan                      # 编译并运行
  duan hello.duan --backend src        # 使用src后端
  duan run hello.duan                  # 解释执行
  duan compile hello.duan -o hello.py  # 编译为Python文件
  duan repl                            # 启动交互式REPL
  duan hello.duan --ast                # 显示AST结构
            """
        )
        
        parser.add_argument('file', nargs='?', help='源文件路径')
        parser.add_argument('--backend', choices=['antlr', 'src'], default='antlr',
                           help='选择编译后端（默认：antlr）')
        parser.add_argument('-o', '--output', help='输出文件路径')
        parser.add_argument('--run', action='store_true', help='编译并运行')
        parser.add_argument('--ast', action='store_true', help='显示AST结构')
        parser.add_argument('--welcome', action='store_true',
                           help='显示首次运行欢迎引导')
        parser.add_argument('--version', action='version', version='段言 v6.3.0')
        
        args = parser.parse_args()
        
        # --welcome 标志：触发首次运行引导
        if args.welcome:
            try:
                sys.path.insert(0, _local_src)
                from first_run import run_welcome
                result = run_welcome()
                if result == 'repl':
                    from first_run import start_repl
                    start_repl()
            except ImportError as e:
                print(f"[错误] 无法加载首次运行引导模块: {e}", file=sys.stderr)
                return 1
            return 0
        
        if args.file:
            if not os.path.exists(args.file):
                print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                return 1
            
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            output_file = args.output
            
            if args.ast:
                return cli.show_ast(source, args.backend)
            
            run_mode = args.run or (not args.output)
            
            if args.backend == 'antlr':
                return cli.compile_with_antlr(source, output_file=output_file, run=run_mode)
            else:
                return cli.compile_with_src(source, output_file=output_file, run=run_mode)
        
        else:
            # 无参数时启动REPL
            return cli.start_repl()


if __name__ == '__main__':
    sys.exit(main())
