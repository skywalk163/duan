"""
段言编译器 - Python实现（用于自举）
将段言代码编译为Python代码
"""

import sys
sys.path.insert(0, '../src')

from lexer import Lexer
from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

def compile_duan(source_code: str, output_path: str = None):
    """编译段言代码"""
    # 词法分析
    lexer = Lexer()
    tokens = lexer.tokenize(source_code)
    
    # 语法分析
    parser = DuanParser()
    ast = parser.parse(source_code)
    
    # 代码生成
    generator = PythonCodeGenerator()
    python_code = generator.generate(ast)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(python_code)
    
    return python_code

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='段言编译器')
    parser.add_argument('input', help='输入文件(.duan)')
    parser.add_argument('-o', '--output', help='输出文件(.py)')
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        source = f.read()
    
    output = args.output or args.input.replace('.duan', '.py')
    compile_duan(source, output)
    print(f'[OK] Compiled {args.input} -> {output}')
