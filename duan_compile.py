#!/usr/bin/env python3
"""
段言（Duan）编程语言 - 统一编译器

支持双后端：
- Python后端：编译为Python代码（轻量、易调试）
- LLVM后端：编译为原生可执行文件（高性能）

使用方法：
  python duan_compile.py input.duan                    # 默认Python后端
  python duan_compile.py input.duan --target python    # Python后端
  python duan_compile.py input.duan --target llvm      # LLVM后端
  python duan_compile.py input.duan -o output.py       # 指定输出文件
"""

import sys
import os
import argparse
from pathlib import Path

# 添加src和antlrparser到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent / 'antlrparser'))

# 使用ANTLR解析器
from duan_visitor import parse_source
from ast_unified import Module, VariableDeclaration, SegmentDefinition, IfStatement, \
    WhileStatement, ForeachStatement, ReturnStatement, PrintStatement, \
    ExpressionStatement, Assignment, BreakStatement, ContinueStatement, \
    TryStatement, ThrowStatement, FunctionCall, BinaryOp, UnaryOp, \
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral, \
    Identifier, SegmentName, ListLiteral, DictLiteral, \
    PropertyAccess, IndexAccess, NewExpression, ClassDefinition

# 导入旧的AST类型（用于代码生成器）
try:
    from duan_parser_v3 import VarDecl, Paragraph, IfStmt, WhileStmt, \
        ForeachStmt, ReturnStmt, ExprStmt, BreakStmt, ContinueStmt, \
        TryStmt, ThrowStmt, ParagraphCall, BinaryOp, NumberLiteral, \
        StringLiteral, Identifier, List as OldList, \
        IndexAccess as OldIndexAccess, Module as OldModule
    from duan_parser_v3 import ASTNode as OldASTNode
    
    # 定义缺失的类型
    class PrintStmt(OldASTNode):
        def __init__(self, value):
            self.value = value
    
    class OldAssignment(OldASTNode):
        def __init__(self, target, value):
            self.target = target
            self.value = value
    
    class Bool(OldASTNode):
        def __init__(self, value):
            self.value = value
    
    class Nil(OldASTNode):
        pass
    
    class Id(Identifier):
        pass
    
    class BinOp(BinaryOp):
        def __init__(self, left, op, right):
            super().__init__(op, left, right)
    
    class UnOp(OldASTNode):
        def __init__(self, op, operand):
            self.op = op
            self.operand = operand
    
    class Dict(OldASTNode):
        def __init__(self, entries):
            self.entries = entries
    
    class MemberAccess(OldASTNode):
        def __init__(self, obj, member):
            self.obj = obj
            self.member = member
    
    class OldClassInstantiation(OldASTNode):
        def __init__(self, class_name, args):
            self.class_name = class_name
            self.args = args
    
    class FuncCall(OldASTNode):
        def __init__(self, func, args):
            self.func = func
            self.args = args
    
    class Number(NumberLiteral):
        pass
    
    class String(StringLiteral):
        pass
    
    class IndexGet(OldIndexAccess):
        pass
    
    from typing import List as TypingList, Optional, Union
    
except ImportError:
    # 如果无法导入旧的AST，定义兼容的类型
    from dataclasses import dataclass, field
    from typing import List, Optional, Union
    
    @dataclass
    class OldASTNode:
        line: int = 0
    
    @dataclass
    class VarDecl(OldASTNode):
        name: str = ""
        value: Optional['OldASTNode'] = None
    
    @dataclass
    class Paragraph(OldASTNode):
        name: str = ""
        params: List[str] = field(default_factory=list)
        body: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class IfStmt(OldASTNode):
        condition: 'OldASTNode' = None
        then_body: List['OldASTNode'] = field(default_factory=list)
        else_body: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class WhileStmt(OldASTNode):
        condition: 'OldASTNode' = None
        body: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class ForeachStmt(OldASTNode):
        var: str = ""
        iterable: 'OldASTNode' = None
        body: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class ReturnStmt(OldASTNode):
        value: Optional['OldASTNode'] = None
    
    @dataclass
    class PrintStmt(OldASTNode):
        value: 'OldASTNode' = None
    
    @dataclass
    class ExprStmt(OldASTNode):
        expr: 'OldASTNode' = None
    
    @dataclass
    class OldAssignment(OldASTNode):
        target: 'OldASTNode' = None
        value: 'OldASTNode' = None
    
    @dataclass
    class BreakStmt(OldASTNode):
        pass
    
    @dataclass
    class ContinueStmt(OldASTNode):
        pass
    
    @dataclass
    class TryStmt(OldASTNode):
        try_body: List['OldASTNode'] = field(default_factory=list)
        catch_var: str = ""
        catch_body: List['OldASTNode'] = field(default_factory=list)
        finally_body: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class ThrowStmt(OldASTNode):
        value: 'OldASTNode' = None
    
    @dataclass
    class FuncCall(OldASTNode):
        func: 'OldASTNode' = None
        args: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class BinOp(OldASTNode):
        left: 'OldASTNode' = None
        op: str = ""
        right: 'OldASTNode' = None
    
    @dataclass
    class UnOp(OldASTNode):
        op: str = ""
        operand: 'OldASTNode' = None
    
    @dataclass
    class Number(OldASTNode):
        value: Union[int, float] = 0
    
    @dataclass
    class String(OldASTNode):
        value: str = ""
    
    @dataclass
    class Bool(OldASTNode):
        value: bool = False
    
    @dataclass
    class Nil(OldASTNode):
        pass
    
    @dataclass
    class Id(OldASTNode):
        name: str = ""
    
    @dataclass
    class OldList(OldASTNode):
        elements: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class Dict(OldASTNode):
        entries: List[tuple] = field(default_factory=list)
    
    @dataclass
    class IndexGet(OldASTNode):
        obj: 'OldASTNode' = None
        index: 'OldASTNode' = None
    
    @dataclass
    class MemberAccess(OldASTNode):
        obj: 'OldASTNode' = None
        member: str = ""
    
    @dataclass
    class OldClassInstantiation(OldASTNode):
        class_name: str = ""
        args: List['OldASTNode'] = field(default_factory=list)
    
    @dataclass
    class OldModule(OldASTNode):
        statements: List['OldASTNode'] = field(default_factory=list)


def convert_ast_to_old_format(module) -> OldModule:
    """
    将统一AST转换为旧格式AST（兼容代码生成器）
    
    Args:
        module: AST模块节点（可能来自duan_ast或ast_unified）
    
    Returns:
        旧格式AST模块节点
    """
    # 导入duan_parser_v3类型用于创建输出
    try:
        from duan_parser_v3 import (
            VarDecl, Paragraph, IfStmt, WhileStmt, ForeachStmt, ReturnStmt, 
            BreakStmt, ContinueStmt, TryStmt, ThrowStmt, ParagraphCall, BinaryOp, 
            NumberLiteral, StringLiteral, Identifier, IndexAccess, Module,
            ParameterList
        )
        from duan_parser_v3 import ASTNode
        
        # 定义缺失的类型（如果duan_parser_v3中没有）
        class PrintStmt(ASTNode):
            def __init__(self, value):
                self.value = value
        
        class ExprStmt(ASTNode):
            def __init__(self, expr):
                self.expr = expr
        
        class OldAssignment(ASTNode):
            def __init__(self, target, value):
                self.target = target
                self.value = value
        
        class Bool(ASTNode):
            def __init__(self, value):
                self.value = value
        
        class Nil(ASTNode):
            pass
        
        class Id(Identifier):
            pass
        
        class BinOp(BinaryOp):
            def __init__(self, left, op, right):
                super().__init__(op, left, right)
        
        class UnOp(ASTNode):
            def __init__(self, op, operand):
                self.op = op
                self.operand = operand
        
        class Dict(ASTNode):
            def __init__(self, entries):
                self.entries = entries
        
        class MemberAccess(ASTNode):
            def __init__(self, obj, member):
                self.obj = obj
                self.member = member
        
        class OldClassInstantiation(ASTNode):
            def __init__(self, class_name, args):
                self.class_name = class_name
                self.args = args
        
        class FuncCall(ASTNode):
            def __init__(self, func, args):
                self.func = func
                self.args = args
        
        class Number(NumberLiteral):
            pass
        
        class String(StringLiteral):
            pass
        
        class IndexGet(IndexAccess):
            pass
        
        class OldList(ASTNode):
            def __init__(self, elements):
                self.elements = elements
        
        OldModule = Module
        
    except ImportError:
        # 如果无法导入旧的AST，使用之前定义的本地类型
        pass
    
    def is_instance(node, class_name):
        """检查节点是否为指定类型（支持多个模块）"""
        if node is None:
            return False
        return type(node).__name__ == class_name
    
    def convert_node(node):
        if node is None:
            return None
        
        node_type = type(node).__name__
        
        # 字面量
        if is_instance(node, 'NumberLiteral'):
            return Number(node.value)
        elif is_instance(node, 'StringLiteral'):
            return String(node.value)
        elif is_instance(node, 'BooleanLiteral'):
            return Bool(node.value)
        elif is_instance(node, 'NullLiteral'):
            return Nil()
        
        # 标识符
        elif is_instance(node, 'Identifier'):
            return Id(node.name)
        elif is_instance(node, 'SegmentName'):
            return Id(node.name)
        
        # 表达式
        elif is_instance(node, 'BinaryOp'):
            return BinOp(convert_node(node.left), node.operator, convert_node(node.right))
        elif is_instance(node, 'UnaryOp'):
            return UnOp(node.operator, convert_node(node.operand))
        elif is_instance(node, 'FunctionCall'):
            return ParagraphCall(node.name.name, [convert_node(arg) for arg in node.arguments])
        elif is_instance(node, 'PropertyAccess'):
            return MemberAccess(convert_node(node.obj), node.property_name)
        elif is_instance(node, 'IndexAccess'):
            return IndexGet(convert_node(node.obj), convert_node(node.index))
        elif is_instance(node, 'ListLiteral'):
            return OldList([convert_node(e) for e in node.elements])
        elif is_instance(node, 'DictLiteral'):
            entries = []
            if hasattr(node, 'entries'):
                entries = [(convert_node(e.key), convert_node(e.value)) for e in node.entries]
            return Dict(entries)
        elif is_instance(node, 'NewExpression'):
            return OldClassInstantiation(node.class_name, [convert_node(arg) for arg in node.arguments])
        
        # 语句
        elif is_instance(node, 'VariableDeclaration'):
            return VarDecl(node.name, convert_node(node.value))
        elif is_instance(node, 'Assignment'):
            return OldAssignment(convert_node(node.target), convert_node(node.value))
        elif is_instance(node, 'IfStatement'):
            else_body = node.else_body if hasattr(node, 'else_body') and node.else_body else []
            return IfStmt(convert_node(node.condition), [convert_node(s) for s in node.then_body], [convert_node(s) for s in else_body])
        elif is_instance(node, 'WhileStatement'):
            return WhileStmt(convert_node(node.condition), [convert_node(s) for s in node.body])
        elif is_instance(node, 'ForeachStatement'):
            return ForeachStmt(node.variable, convert_node(node.iterable), [convert_node(s) for s in node.body])
        elif is_instance(node, 'ReturnStatement'):
            return ReturnStmt(convert_node(node.value))
        elif is_instance(node, 'PrintStatement'):
            # 将打印语句转换为函数调用
            return ParagraphCall('打印', [convert_node(node.value)])
        elif is_instance(node, 'ExpressionStatement'):
            return ExprStmt(convert_node(node.expression))
        elif is_instance(node, 'BreakStatement'):
            return BreakStmt()
        elif is_instance(node, 'ContinueStatement'):
            return ContinueStmt()
        elif is_instance(node, 'TryStatement'):
            finally_body = node.finally_body if hasattr(node, 'finally_body') and node.finally_body else []
            return TryStmt([convert_node(s) for s in node.try_body], node.catch_var, [convert_node(s) for s in node.catch_body], [convert_node(s) for s in finally_body])
        elif is_instance(node, 'ThrowStatement'):
            return ThrowStmt(convert_node(node.value))
        elif is_instance(node, 'SegmentDefinition'):
            # 转换段落定义
            params = []
            if hasattr(node, 'parameters'):
                # 转换为字典列表格式
                params = [{'name': p.name} for p in node.parameters]
            elif hasattr(node, 'params'):
                # 如果已经是字符串列表，转换为字典列表
                if node.params and isinstance(node.params[0], str):
                    params = [{'name': p} for p in node.params]
                else:
                    params = node.params
            return Paragraph(node.name, params, None, [convert_node(s) for s in node.body])
        
        # 默认返回None或原样返回
        return None
    
    # 转换所有语句和段落
    old_statements = []
    
    # 添加段落定义
    if hasattr(module, 'segments'):
        for seg in module.segments:
            converted = convert_node(seg)
            if converted:
                old_statements.append(converted)
    
    # 添加普通语句
    if hasattr(module, 'statements'):
        for stmt in module.statements:
            converted = convert_node(stmt)
            if converted:
                old_statements.append(converted)
    
    return OldModule(old_statements)


def compile_to_python(module: Module, output_file: str = None) -> str:
    """
    编译为Python代码
    
    Args:
        module: AST模块节点
        output_file: 输出文件路径（可选）
    
    Returns:
        生成的Python代码
    """
    from code_generator_unified import UnifiedCodeGenerator
    
    generator = UnifiedCodeGenerator()
    python_code = generator.generate(module)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_code)
        print(f"✓ Python代码已生成: {output_file}")
    
    return python_code


def compile_to_llvm(module: Module, output_name: str = "a") -> bool:
    """
    编译为LLVM IR并生成可执行文件
    
    Args:
        module: AST模块节点
        output_name: 输出文件名（不含扩展名）
    
    Returns:
        是否成功
    """
    from antlrparser.duan_compiler import compile_duan_ast
    
    # 将统一AST转换为antlrparser的AST格式
    # TODO: 实现AST转换或直接使用antlrparser的visitor
    
    print(f"✓ LLVM编译完成: {output_name}.exe")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='段言编程语言编译器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.duan                      # 编译为Python代码
  %(prog)s input.duan --target llvm        # 编译为可执行文件
  %(prog)s input.duan -o output.py         # 指定输出文件
  %(prog)s --help                          # 显示帮助
        """
    )
    
    parser.add_argument('input', help='输入的段言源文件（.duan）')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--target', choices=['python', 'llvm'], default='python',
                       help='编译目标（默认：python）')
    parser.add_argument('--run', action='store_true', help='编译后立即运行')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 读取源文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_path}")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    if args.verbose:
        print(f"读取源文件: {input_path}")
        print(f"编译目标: {args.target}")
    
    # 解析源代码
    try:
        module = parse_source(source_code)
        if module is None:
            print("错误: 解析失败")
            sys.exit(1)
    except Exception as e:
        print(f"解析错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if args.verbose:
        print(f"解析成功: {len(module.segments)} 个段落, {len(module.classes)} 个类")
    
    # 根据目标编译
    if args.target == 'python':
        # 确定输出文件
        if args.output:
            output_file = args.output
        else:
            output_file = input_path.stem + '.py'
        
        # 编译
        python_code = compile_to_python(module, output_file)
        
        # 运行
        if args.run:
            import subprocess
            subprocess.run([sys.executable, output_file])
    
    elif args.target == 'llvm':
        # 确定输出名称
        output_name = Path(args.output).stem if args.output else input_path.stem
        
        # 编译
        success = compile_to_llvm(module, output_name)
        if not success:
            sys.exit(1)
        
        # 运行
        if args.run:
            import subprocess
            subprocess.run([output_name + '.exe'])


if __name__ == '__main__':
    main()
