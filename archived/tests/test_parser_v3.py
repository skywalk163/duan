"""
段言（Duan）编程语言 - 完整语法解析器测试（简化版）
"""

from duan_parser_v3 import DuanParser
import sys


def test_basic():
    """测试基本语法"""
    parser = DuanParser()
    
    print("=" * 60)
    print("段言完整语法解析器测试（v3.0）")
    print("=" * 60)
    
    # 测试1：变量声明
    print("\n--- 测试1: 变量声明 ---")
    try:
        result = parser.parse('定义甲等于三。')
        print(f"[OK] 解析成功")
        print(f"  类型: {type(result).__name__}")
        print(f"  语句数: {len(result.statements)}")
        for i, stmt in enumerate(result.statements):
            print(f"  语句{i+1}: {type(stmt).__name__} - {stmt}")
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试2：条件语句（简化版）
    print("\n--- 测试2: 条件语句 ---")
    try:
        code = '如果甲大于十那么打印甲。'
        result = parser.parse(code)
        print(f"[OK] 解析成功")
        print(f"  语句数: {len(result.statements)}")
        for i, stmt in enumerate(result.statements):
            print(f"  语句{i+1}: {type(stmt).__name__}")
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
    
    # 测试3：段落定义（简化版）
    print("\n--- 测试3: 段落定义 ---")
    try:
        code = '《计算》段返回甲加乙。'
        result = parser.parse(code)
        print(f"[OK] 解析成功")
        print(f"  语句数: {len(result.statements)}")
        for i, stmt in enumerate(result.statements):
            print(f"  语句{i+1}: {type(stmt).__name__}")
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
    
    # 测试4：管道操作
    print("\n--- 测试4: 管道操作 ---")
    try:
        result = parser.parse('数据 -> 过滤 -> 排序。')
        print(f"[OK] 解析成功")
        print(f"  语句数: {len(result.statements)}")
        for i, stmt in enumerate(result.statements):
            print(f"  语句{i+1}: {type(stmt).__name__} - {stmt}")
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_basic()
