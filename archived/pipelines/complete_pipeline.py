"""
段言（Duan）编程语言 - 完整编译流程测试

测试：段言代码 -> 词法分析 -> 语法解析 -> 语义分析 -> Python代码
"""

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator


def compile_duan(duan_code: str, verbose: bool = True) -> str:
    """编译段言代码到Python代码"""
    
    if verbose:
        print("=" * 60)
        print("段言编译器")
        print("=" * 60)
        print(f"\n段言代码:\n{duan_code}\n")
    
    # 1. 词法分析 + 语法解析
    if verbose:
        print("--- 阶段 1: 词法分析 + 语法解析 ---")
    
    parser = DuanParser()
    module = parser.parse(duan_code)
    
    if verbose:
        print(f"✓ 解析成功: {len(module.statements)} 条语句")
    
    # 2. 语义分析
    if verbose:
        print("\n--- 阶段 2: 语义分析 ---")
    
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(module)
    
    if verbose:
        if success:
            print("✓ 语义分析通过")
        else:
            print("✗ 语义错误:")
            for error in analyzer.errors:
                print(f"  - {error.message}")
    
    # 3. 代码生成
    if verbose:
        print("\n--- 阶段 3: Python代码生成 ---")
    
    generator = PythonCodeGenerator()
    python_code = generator.generate(module)
    
    if verbose:
        print("✓ 代码生成成功")
        print(f"\nPython代码:\n{python_code}")
    
    return python_code


# =============================================================================
# 测试用例
# =============================================================================

if __name__ == '__main__':
    import sys
    import io
    
    # 设置输出编码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 测试1：变量声明和运算
    print("\n" + "=" * 60)
    print("测试 1: 变量声明和运算")
    print("=" * 60)
    
    duan_code1 = '''
定义甲等于三。
定义乙等于五。
定义丙等于甲加乙。
'''
    
    python_code1 = compile_duan(duan_code1)
    
    # 测试2：条件语句
    print("\n" + "=" * 60)
    print("测试 2: 条件语句")
    print("=" * 60)
    
    duan_code2 = '''
定义分数等于85。
如果分数大于60那么打印及格。
'''
    
    python_code2 = compile_duan(duan_code2)
    
    # 测试3：段落定义
    print("\n" + "=" * 60)
    print("测试 3: 段落定义")
    print("=" * 60)
    
    duan_code3 = '''
《计算》段(甲, 乙)：
  返回甲加乙。

定义结果等于《计算》参数3参数5。
'''
    
    python_code3 = compile_duan(duan_code3)
    
    # 测试4：完整程序
    print("\n" + "=" * 60)
    print("测试 4: 完整程序")
    print("=" * 60)
    
    duan_code4 = '''
《阶乘》段(数)：
  如果数小于等于1那么返回1。
  返回数乘《阶乘》参数数减1。

定义结果等于《阶乘》参数5。
打印结果。
'''
    
    python_code4 = compile_duan(duan_code4)
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
