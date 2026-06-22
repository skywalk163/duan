"""
测试统一AST和语义分析器
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ast_unified import *
from semantic_analyzer import SemanticAnalyzer

def create_test_module() -> Module:
    """创建一个测试模块"""
    module = Module(name="test")
    
    # 添加一个简单的函数
    func_body = Block(statements=[
        # 声明变量
        VariableDeclaration(
            name="x",
            type=TYPE_INT,
            initializer=NumberLiteral(value=42),
            is_mutable=True
        ),
        # 赋值语句
        Assignment(
            target=Identifier(name="x"),
            value=BinaryOp(
                left=Identifier(name="x"),
                operator="+",
                right=NumberLiteral(value=1)
            )
        ),
        # 返回语句
        ReturnStatement(
            value=Identifier(name="x")
        )
    ])
    
    func = FunctionDefinition(
        name="add_one",
        parameters=[
            Parameter(name="n", type=TYPE_INT)
        ],
        return_type=TYPE_INT,
        body=func_body
    )
    
    module.functions.append(func)
    return module

def test_semantic_analysis():
    """测试语义分析"""
    print("=== 测试语义分析器 ===")
    
    # 创建测试模块
    module = create_test_module()
    print("✓ 创建测试模块")
    
    # 创建语义分析器
    analyzer = SemanticAnalyzer(module)
    print("✓ 创建语义分析器")
    
    # 执行分析
    errors = analyzer.analyze()
    print(f"✓ 执行语义分析，发现 {len(errors)} 个错误")
    
    # 打印错误
    if errors:
        print("\n发现的错误：")
        for i, error in enumerate(errors):
            print(f"  {i+1}. {error} (行 {error.line})")
    else:
        print("\n✓ 语义分析通过，没有错误！")
    
    # 打印符号表
    print("\n=== 符号表 ===")
    for scope_id, symbols in module.scopes.items():
        print(f"作用域 {scope_id}:")
        for name, symbol in symbols.items():
            print(f"  {name}: {symbol.type} (全局: {symbol.is_global}, 可变: {symbol.is_mutable})")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = test_semantic_analysis()
    sys.exit(0 if success else 1)