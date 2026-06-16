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
        from antlr4 import InputStream, CommonTokenStream
        from DuanLangLexer import DuanLangLexer
        from DuanLangParser import DuanLangParser
        from duan_visitor import DuanLangASTBuilder
        from code_generator_unified import UnifiedCodeGenerator
        from duan_error_handler import ChineseErrorListener
        
        # 词法分析
        input_stream = InputStream(source)
        lexer = DuanLangLexer(input_stream)
        
        # 添加中文错误监听器
        error_listener = ChineseErrorListener()
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        
        tokens = CommonTokenStream(lexer)
        
        # 语法分析
        parser = DuanLangParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        
        tree = parser.program()
        
        if error_listener.has_errors():
            for error in error_listener.get_errors():
                print(error, file=sys.stderr)
            return 1
        
        # AST构建
        builder = DuanLangASTBuilder()
        module = builder.visitProgram(tree)
        
        if builder.errors:
            for error in builder.errors:
                print(f"[语义错误] {error}", file=sys.stderr)
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
    
    def compile_with_src(self, source: str, output_file: Optional[str] = None, run: bool = False) -> int:
        """使用src手写解析器编译"""
        from lexer import Lexer
        from duan_parser_v3 import DuanParser
        from code_generator import PythonCodeGenerator
        
        # 词法分析
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        
        # 语法分析
        parser = DuanParser()
        module = parser.parse(source)
        
        if not module:
            print("[语法错误] 解析失败", file=sys.stderr)
            return 1
        
        # 代码生成
        generator = PythonCodeGenerator()
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
    
    def interpret_run(self, source_file: str) -> int:
        """使用解释器直接运行"""
        try:
            from duan_interpreter import run_file
            run_file(source_file)
            return 0
        except ImportError:
            print("[错误] 解释器模块不可用", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"[运行错误] {e}", file=sys.stderr)
            return 1
    
    def start_repl(self) -> int:
        """启动REPL"""
        try:
            from duan_repl import main as repl_main
            repl_main()
            return 0
        except ImportError:
            print("[错误] REPL模块不可用", file=sys.stderr)
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
    cli = DuanUnifiedCLI()
    
    # 检查是否是子命令模式
    if len(sys.argv) > 1 and sys.argv[1] in ['run', 'compile', 'repl']:
        # 子命令模式
        parser = argparse.ArgumentParser(description='段言（Duan）编程语言编译器')
        subparsers = parser.add_subparsers(dest='command', help='子命令')
        
        # run 子命令
        run_parser = subparsers.add_parser('run', help='解释执行')
        run_parser.add_argument('file', help='源文件路径')
        
        # compile 子命令
        compile_parser = subparsers.add_parser('compile', help='编译为Python文件')
        compile_parser.add_argument('file', help='源文件路径')
        compile_parser.add_argument('-o', '--output', help='输出文件路径')
        compile_parser.add_argument('--backend', choices=['antlr', 'src'], default='antlr',
                                   help='选择编译后端')
        
        # repl 子命令
        subparsers.add_parser('repl', help='启动交互式REPL')
        
        args = parser.parse_args()
        
        if args.command == 'run':
            if not os.path.exists(args.file):
                print(f"[错误] 文件不存在: {args.file}", file=sys.stderr)
                return 1
            return cli.interpret_run(args.file)
        
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
                return cli.compile_with_src(source, output_file=output_file, run=False)
        
        elif args.command == 'repl':
            return cli.start_repl()
    
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
        parser.add_argument('--version', action='version', version='段言 v1.0.0')
        
        args = parser.parse_args()
        
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
