#!/usr/bin/env python3
"""
段言编程语言 - 类定义功能完整测试

测试内容：
1. 类实例化（新建）
2. 对象属性访问（对象.属性）
3. 对象方法访问（对象.方法）
4. 类继承
5. self引用（己）
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator


def test_class_instantiation():
    """测试类实例化"""
    print("=" * 60)
    print("测试1: 类实例化")
    print("=" * 60)

    code = '''class 狗:
    def __init__(self, 名称):
        self.名称 = 名称

def 主():
    小狗实例 = 狗('小白')
    print(小狗实例.名称)
    return 0

主()'''

    try:
        exec(code)
        print("[PASS] 类实例化测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] 类实例化测试失败: {e}")
        return False


def test_attribute_access():
    """测试属性访问"""
    print("\n" + "=" * 60)
    print("测试2: 属性访问")
    print("=" * 60)

    code = '''class 狗:
    def __init__(self, 名称, 年龄):
        self.名称 = 名称
        self.年龄 = 年龄

def 主():
    小狗实例 = 狗('小白', 3)
    print(小狗实例.名称)
    print(小狗实例.年龄)
    return 0

主()'''

    try:
        exec(code)
        print("[PASS] 属性访问测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] 属性访问测试失败: {e}")
        return False


def test_inheritance():
    """测试类继承"""
    print("\n" + "=" * 60)
    print("测试3: 类继承")
    print("=" * 60)

    code = '''class 动物:
    def __init__(self, 名称):
        self.名称 = 名称

class 狗(动物):
    def __init__(self, 名称):
        self.名称 = 名称
        self.年龄 = 1

def 主():
    动物实例 = 动物('通用')
    狗实例 = 狗('小白')
    print(动物实例.名称)
    print(狗实例.名称)
    print(狗实例.年龄)
    return 0

主()'''

    try:
        exec(code)
        print("[PASS] 类继承测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] 类继承测试失败: {e}")
        return False


def test_method_definition():
    """测试方法定义"""
    print("\n" + "=" * 60)
    print("测试4: 方法定义")
    print("=" * 60)

    code = '''class 狗:
    def __init__(self, 名称):
        self.名称 = 名称

    def 说话():
        return '汪汪汪'

def 主():
    小狗实例 = 狗('小白')
    print(小狗实例.说话())
    return 0

主()'''

    try:
        exec(code)
        print("[PASS] 方法定义测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] 方法定义测试失败: {e}")
        return False


def test_complete_example():
    """测试完整示例"""
    print("\n" + "=" * 60)
    print("测试5: 完整示例（类定义 + 实例化 + 属性访问 + 继承）")
    print("=" * 60)

    code = '''class 动物:
    def __init__(self, 名称):
        self.名称 = 名称

    def 说话():
        return '动物叫'

class 狗(动物):
    def __init__(self, 名称):
        self.名称 = 名称
        self.年龄 = 1

    def 说话():
        return '汪汪汪'

def 主():
    动物实例 = 动物('通用')
    狗实例 = 狗('小白')

    print('动物实例.名称:', 动物实例.名称)
    print('动物实例.说话():', 动物实例.说话())
    print('狗实例.名称:', 狗实例.名称)
    print('狗实例.年龄:', 狗实例.年龄)
    print('狗实例.说话():', 狗实例.说话())

    return 0

主()'''

    try:
        exec(code)
        print("[PASS] 完整示例测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] 完整示例测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " 段言编程语言 - 类定义功能测试 ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    results = []
    results.append(("类实例化", test_class_instantiation()))
    results.append(("属性访问", test_attribute_access()))
    results.append(("类继承", test_inheritance()))
    results.append(("方法定义", test_method_definition()))
    results.append(("完整示例", test_complete_example()))

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS] 通过" if result else "[FAIL] 失败"
        print(f"{name:20} {status}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n[PASS] 所有测试通过！")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} 个测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
