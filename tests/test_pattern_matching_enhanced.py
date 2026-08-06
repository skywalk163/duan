"""
段言模式匹配增强测试

测试内容：
1. 守卫条件：情况 模式 若 条件
2. 嵌套模式：列表嵌套、模式组合
3. 绑定变量：模式中捕获变量
"""

import sys
import os
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator


def run_duan(code: str) -> str:
    """使用 src 后端解析并执行段言代码，返回输出"""
    parser = DuanParser()
    module = parser.parse(code)
    generator = PythonCodeGenerator()
    py_code = generator.generate(module)
    
    # 执行生成的 Python 代码，捕获输出
    output = io.StringIO()
    local_vars = {}
    try:
        with redirect_stdout(output):
            exec(py_code, {}, local_vars)
    except SystemExit:
        pass
    result = output.getvalue().strip()
    return result


def test_guard_condition():
    """守卫条件：情况 模式 若 条件"""
    result = run_duan('''
设 分数 为 85。
匹配 分数：
  情况 100：
    打印 "满分"。
  情况 分数 若 分数 大于 80：
    打印 "优秀"。
  情况 _：
    打印 "加油"。
结束。
''')
    assert result == "优秀", f"Expected '优秀', got '{result}'"


def test_guard_condition_false():
    """守卫条件失败时走通配符"""
    result = run_duan('''
设 分数 为 60。
匹配 分数：
  情况 100：
    打印 "满分"。
  情况 分数 若 分数 大于 80：
    打印 "优秀"。
  情况 _：
    打印 "加油"。
结束。
''')
    assert result == "加油", f"Expected '加油', got '{result}'"


def test_guard_with_multiple_conditions():
    """守卫条件中使用且/或"""
    result = run_duan('''
设 年龄 为 25。
匹配 年龄：
  情况 年龄 若 年龄 大于 0 且 年龄 小于 18：
    打印 "未成年"。
  情况 年龄 若 年龄 大于 等于 18 且 年龄 小于 60：
    打印 "成年"。
  情况 _：
    打印 "老年"。
结束。
''')
    assert result == "成年", f"Expected '成年', got '{result}'"


def test_list_pattern():
    """列表模式匹配"""
    result = run_duan('''
设 列表 为 [1, 2, 3]。
匹配 列表：
  情况 [1, 2, 3]：
    打印 "一二三"。
  情况 _：
    打印 "其他"。
结束。
''')
    assert result == "一二三", f"Expected '一二三', got '{result}'"


def test_list_pattern_wildcard():
    """列表通配符模式"""
    result = run_duan('''
设 列表 为 [1, 2, 3]。
匹配 列表：
  情况 [1, _]：
    打印 "两个元素"。
  情况 [1, _, _]：
    打印 "三个元素"。
  情况 _：
    打印 "其他"。
结束。
''')
    assert result == "三个元素", f"Expected '三个元素', got '{result}'"


def test_variable_binding():
    """变量绑定模式"""
    result = run_duan('''
设 数值 为 42。
匹配 数值：
  情况 甲：
    打印 "绑定了" + 转字符串(甲)。
结束。
''')
    assert "绑定了42" in result, f"Expected '绑定了42', got '{result}'"


def test_type_check_pattern():
    """类型检查模式：类型 变量名"""
    result = run_duan('''
设 值 为 "你好"。
匹配 值：
  情况 整数 甲：
    打印 "整数：" + 转字符串(甲)。
  情况 文本 甲：
    打印 "文本：" + 甲。
结束。
''')
    assert "文本：你好" in result, f"Expected '文本：你好', got '{result}'"


def test_boolean_pattern():
    """布尔模式匹配"""
    result = run_duan('''
设 标志 为 真。
匹配 标志：
  情况 真：
    打印 "开启"。
  情况 假：
    打印 "关闭"。
结束。
''')
    assert result == "开启", f"Expected '开启', got '{result}'"


def test_nested_pattern():
    """嵌套列表模式"""
    result = run_duan('''
设 数据 为 [[1, 2], [3, 4]]。
匹配 数据：
  情况 [[1, 2], [3, 4]]：
    打印 "匹配二维"。
  情况 _：
    打印 "不匹配"。
结束。
''')
    assert result == "匹配二维", f"Expected '匹配二维', got '{result}'"


def test_combined_guard_and_binding():
    """守卫条件与变量绑定组合"""
    result = run_duan('''
设 值 为 7。
匹配 值：
  情况 甲 若 甲 大于 5：
    打印 "大于5：" + 转字符串(甲)。
  情况 _：
    打印 "不大于5"。
结束。
''')
    assert "大于5：7" in result, f"Expected '大于5：7', got '{result}'"


if __name__ == '__main__':
    tests = [
        ("守卫条件", test_guard_condition),
        ("守卫条件失败", test_guard_condition_false),
        ("守卫条件多条件", test_guard_with_multiple_conditions),
        ("列表模式", test_list_pattern),
        ("列表通配符", test_list_pattern_wildcard),
        ("变量绑定", test_variable_binding),
        ("类型检查模式", test_type_check_pattern),
        ("布尔模式", test_boolean_pattern),
        ("嵌套模式", test_nested_pattern),
        ("守卫+绑定组合", test_combined_guard_and_binding),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  [OK] {name}")
            passed += 1
        except Exception as e:
            import traceback
            print(f"  [失败] {name}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n总计: {len(tests)}  |  通过: {passed}  |  失败: {failed}")
    sys.exit(0 if failed == 0 else 1)