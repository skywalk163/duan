# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from lexer import Lexer
from duan_parser_v3 import *
from arity_parser import ArityParser
from verb_info import is_verb

print("=" * 60)
print("元数驱动解析器测试")
print("=" * 60)

# 测试用例
test_cases = [
    ('单参数', '打印甲。', '打印(甲)'),
    ('二元运算', '加1乘2 3。', '加(1, 乘(2, 3))'),
    ('可变参数', '列1 2 3 4 5。', '列(1, 2, 3, 4, 5)'),
]

lexer = Lexer()

for name, code, expected in test_cases:
    print(f"\n--- 测试: {name} ---")
    print(f"代码: {code}")
    print(f"期望: {expected}")
    sys.stdout.flush()
    
    try:
        # 词法分析
        tokens = list(lexer.tokenize(code))
        
        # 过滤掉EOF
        tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        print(f"Tokens: {[f'{t.type.name}:{t.value}' for t in tokens]}")
        
        # 元数驱动解析（检查第一个token是否是动词）
        if tokens and is_verb(tokens[0].value):
            parser = ArityParser(tokens)
            result, consumed = parser.parse_verb_call(tokens[0].value)
            print(f"解析结果: {result}")
            print(f"消耗token数: {consumed}")
            print(f"[OK] 成功")
        else:
            print(f"[SKIP] 不是动词调用")
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
