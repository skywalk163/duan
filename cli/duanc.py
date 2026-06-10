#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言（Duan）编译器命令行工具

用法：
  duanc <源文件.duan> [选项]
  duanc --help
  duanc --version

示例：
  duanc hello.duan                    # 编译并运行
  duanc hello.duan -o hello.py        # 编译为 Python 文件
  duanc hello.duan --run              # 编译并运行
  duanc hello.duan --ast              # 显示 AST
  duanc hello.duan --tokens           # 显示 Token 流
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional, List

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator
from core.errors import DuanError, LexerError, ParserError, SemanticError


class DuanCompiler:
    """段言编译器"""
    
    def __init__(self, verbose: bool = False):
        self.lexer = Lexer()
        self.parser = DuanParser()
        self.analyzer = SemanticAnalyzer()
        self.generator = PythonCodeGenerator()
        self.verbose = verbose
    
    def compile(self, source: str, filename: Optional[str] = None) -> str:
        """完整编译流程"""
        if self.verbose:
            print(f"[编译] 开始编译: {filename or '<字符串>'}")
        
        # 1. 词法分析
        tokens = self.lexer.tokenize(source)
        if self.verbose:
            print(f"[词法] 生成 {len(tokens)} 个 token")
        
        # 2. 语法解析
        module = self.parser.parse(source)
        if self.verbose:
            print(f"[语法] 解析 {len(module.statements)} 条语句")
        
        # 3. 语义分析
        success = self.analyzer.analyze(module)
        if not success:
            raise SemanticError("语义分析失败")
        if self.verbose:
            print(f"[语义] 分析通过")
        
        # 4. 代码生成
        code = self.generator.generate(module)
        if self.verbose:
            print(f"[生成] 生成 {len(code)} 字节代码")
        
        return code
    
    def compile_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """编译文件"""
        # 读取源文件
        with open(input_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 编译
        code = self.compile(source, input_path)
        
        # 输出
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            if self.verbose:
                print(f"[输出] 已写入: {output_path}")
        
        return code
    
    def get_tokens(self, source: str) -> List:
        """获取 Token 流"""
        return self.lexer.tokenize(source)
    
    def get_ast(self, source: str):
        """获取 AST"""
        return self.parser.parse(source)


def main():
    """主函数"""
    # 创建参数解析器
    parser = argparse.ArgumentParser(
        description='段言（Duan）编程语言编译器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s hello.duan                  编译并运行
  %(prog)s hello.duan -o hello.py      编译为 Python 文件
  %(prog)s hello.duan --run            编译并运行
  %(prog)s hello.duan --ast            显示 AST
  %(prog)s hello.duan --tokens         显示 Token 流
  %(prog)s --version                   显示版本信息
        """
    )
    
    # 位置参数
    parser.add_argument('file', nargs='?', help='要编译的段言源文件')
    
    # 输出选项
    parser.add_argument('-o', '--output', metavar='FILE', help='输出文件路径')
    parser.add_argument('--run', action='store_true', help='编译并运行')
    
    # 调试选项
    parser.add_argument('--tokens', action='store_true', help='显示 Token 流')
    parser.add_argument('--ast', action='store_true', help='显示 AST')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    
    # 其他选项
    parser.add_argument('--version', action='version', version='段言编译器 v0.7.0')
    parser.add_argument('--init', action='store_true', help='创建示例项目')
    
    # 解析参数
    args = parser.parse_args()
    
    # 创建示例项目
    if args.init:
        create_sample_project()
        return 0
    
    # 检查是否提供了文件
    if not args.file:
        parser.print_help()
        return 1
    
    # 检查文件是否存在
    input_file = Path(args.file)
    if not input_file.exists():
        print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
        return 1
    
    try:
        # 创建编译器
        compiler = DuanCompiler(verbose=args.verbose)
        
        # 读取源文件
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 显示 Token 流
        if args.tokens:
            tokens = compiler.get_tokens(source)
            print("Token 流:")
            print("-" * 60)
            for i, token in enumerate(tokens, 1):
                print(f"{i:3d}. {token}")
            return 0
        
        # 显示 AST
        if args.ast:
            ast = compiler.get_ast(source)
            print("抽象语法树 (AST):")
            print("-" * 60)
            print_ast(ast, indent=0)
            return 0
        
        # 编译
        output_file = args.output
        if not output_file:
            # 默认输出到同名 .py 文件
            output_file = str(input_file.with_suffix('.py'))
        
        code = compiler.compile_file(str(input_file), output_file)
        
        # 运行
        if args.run:
            print("-" * 60)
            print("运行结果:")
            print("-" * 60)
            exec_globals = {}
            exec(code, exec_globals)
        else:
            print(f"编译成功: {args.file} -> {output_file}")
        
        return 0
        
    except DuanError as e:
        print(f"编译错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        import traceback
        if args.verbose:
            traceback.print_exc()
        return 1


def print_ast(node, indent=0):
    """打印 AST"""
    prefix = "  " * indent
    
    if hasattr(node, '__dict__'):
        # 打印节点类型
        node_type = type(node).__name__
        print(f"{prefix}{node_type}")
        
        # 打印属性
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                print(f"{prefix}  {key}:")
                for item in value:
                    print_ast(item, indent + 2)
            elif hasattr(value, '__dict__'):
                print(f"{prefix}  {key}:")
                print_ast(value, indent + 2)
            else:
                print(f"{prefix}  {key}: {value}")


def create_sample_project():
    """创建示例项目"""
    import shutil
    
    project_dir = Path('duan_project')
    project_dir.mkdir(exist_ok=True)
    
    # 创建示例文件
    sample_code = '''# 段言示例程序

# 变量声明
定义甲等于123。
定义乙等于三加五。

# 条件语句
如果甲大于乙那么打印甲。
否则打印乙。

# 函数定义
《加法》段(甲, 乙)：
  返回甲加乙。

# 函数调用
定义结果等于《加法》参数三，五。
打印结果。

# 循环
定义列表等于1，2，3，4，5。
遍历列表中的元素：
  打印元素。
'''
    
    sample_file = project_dir / 'main.duan'
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_code)
    
    # 创建 README
    readme = '''# 段言项目

## 编译

```bash
duanc main.duan
```

## 运行

```bash
duanc main.duan --run
```

或

```bash
python main.py
```
'''
    
    readme_file = project_dir / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"✓ 已创建示例项目: {project_dir}/")
    print(f"  - main.duan  示例代码")
    print(f"  - README.md  项目说明")
    print()
    print("下一步:")
    print(f"  cd {project_dir}")
    print("  duanc main.duan --run")


if __name__ == '__main__':
    sys.exit(main())
