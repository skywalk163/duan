# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 高级语义集成测试

测试：
1. 元数驱动解析
2. 主谓/谓宾语义识别
3. 完整编译流程
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from duan_parser_v3 import DuanParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator
from verb_info import get_verb_info, get_python_mapping
from semantic_identifier import SemanticIdentifier, SemanticType

print("=" * 60)
print("段言高级语义集成测试")
print("=" * 60)

# =============================================================================
# 测试1：动词信息
# =============================================================================

print("\n--- 测试1: 动词信息 ---")

verbs = ['加', '排序', '添加', '过滤']

for verb in verbs:
    info = get_verb_info(verb)
    if info:
        print(f"\n动词: {verb}")
        print(f"  参数数量: {info.arity}")
        print(f"  修改模式: {info.mode}")
        print(f"  支持原地修改: {info.supports_modify()}")
        print(f"  支持函数式: {info.supports_functional()}")
        
        mapping = get_python_mapping(verb)
        if mapping:
            print(f"  Python映射: {mapping[0]} ({mapping[1]})")

# =============================================================================
# 测试2：编译流程（基础）
# =============================================================================

print("\n" + "=" * 60)
print("测试2: 编译流程（基础语法）")
print("=" * 60)

parser = DuanParser()
analyzer = SemanticAnalyzer()
generator = PythonCodeGenerator()

test_cases = [
    ('变量声明', '定义甲等于3。'),
    ('函数定义', '《计算》段(甲, 乙)：返回甲加乙。'),
]

for name, code in test_cases:
    print(f"\n--- {name} ---")
    print(f"段言: {code}")
    
    try:
        module = parser.parse(code)
        success = analyzer.analyze(module)
        python_code = generator.generate(module)
        
        print(f"解析: {len(module.statements)} 条语句")
        print(f"语义分析: {'通过' if success else '失败'}")
        print(f"Python:\n{python_code}")
    except Exception as e:
        print(f"错误: {e}")

# =============================================================================
# 测试3：语义识别
# =============================================================================

print("\n" + "=" * 60)
print("测试3: 语义识别（主谓/谓宾）")
print("=" * 60)

from duan_parser_v3 import BinaryOp, Identifier, ParagraphCall

symbol_table = {'列表': 'list', '数据': 'list'}
identifier = SemanticIdentifier(symbol_table)

# 测试用例
semantic_tests = [
    ('列表排序', BinaryOp('排序', Identifier('列表'), None)),
    ('排序列表', BinaryOp('排序', None, Identifier('列表'))),
    ('《排序》(列表)', ParagraphCall('排序', [Identifier('列表')])),
]

for name, expr in semantic_tests:
    print(f"\n--- {name} ---")
    
    semantic_type, verb = identifier.identify(expr)
    
    print(f"语义类型: {semantic_type}")
    print(f"动词: {verb}")
    
    # 生成Python代码
    if verb:
        from semantic_identifier import generate_python_code
        args = ['列表'] if isinstance(expr, ParagraphCall) else []
        python_code = generate_python_code(semantic_type, verb, args, symbol_table)
        print(f"Python代码: {python_code}")

# =============================================================================
# 测试4：完整编译示例
# =============================================================================

print("\n" + "=" * 60)
print("测试4: 完整编译示例")
print("=" * 60)

complete_examples = [
    ('计算平方', '''《平方》段(数)：
  返回数乘数。

定义结果等于《平方》参数5。
打印结果。
'''),
    ('条件判断', '''定义分数等于85。
如果分数大于60那么打印及格。
'''),
]

for name, code in complete_examples:
    print(f"\n--- {name} ---")
    print(f"段言代码:\n{code}")
    
    try:
        module = parser.parse(code)
        success = analyzer.analyze(module)
        python_code = generator.generate(module)
        
        print(f"\nPython代码:\n{python_code}")
    except Exception as e:
        print(f"错误: {e}")

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)
