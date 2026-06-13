"""
段言编译器 - 编译段言代码为Python代码
"""
import sys
import os

# 添加antlrparser目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'antlrparser'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from antlr4 import *
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from duan_visitor import DuanLangASTBuilder
from code_generator_unified import UnifiedCodeGenerator


def compile_duan(source_file: str, output_file: str = None):
    """编译段言文件
    
    Args:
        source_file: 段言源文件路径
        output_file: 输出的Python文件路径（可选，默认为同名.py文件）
    
    Returns:
        生成的Python代码
    """
    # 读取源文件
    with open(source_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 词法分析
    input_stream = InputStream(code)
    lexer = DuanLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    
    # 语法分析
    parser = DuanLangParser(token_stream)
    tree = parser.program()
    
    # 转换为AST
    visitor = DuanLangASTBuilder()
    ast = visitor.visit(tree)
    
    # 生成Python代码
    gen = UnifiedCodeGenerator()
    py_code = gen.generate(ast)
    
    # 保存输出文件
    if output_file is None:
        output_file = source_file.rsplit('.', 1)[0] + '.py'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(py_code)
    
    print(f"编译成功: {source_file} → {output_file}")
    return py_code


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python compile.py <源文件.duan> [输出文件.py]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    py_code = compile_duan(source_file, output_file)
    print("\n生成的Python代码：")
    print(py_code)
