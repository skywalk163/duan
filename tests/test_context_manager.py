"""
段言上下文管理器测试

测试内容：
1. 使用 文件 为 变量：读文件
2. 使用 表达式 为 变量：自动资源管理
3. 无变量上下文管理器
4. 嵌套上下文管理器
5. 上下文管理器异常处理
"""

import sys
import os
import io
import tempfile
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


def _compile(duan_code: str) -> str:
    """编译段言代码，返回Python源码"""
    parser = DuanParser()
    module = parser.parse(duan_code)
    generator = PythonCodeGenerator()
    return generator.generate(module)


def test_with_stmt_generates_python_with():
    """使用 生成Python with语句"""
    code = """
使用 读取文件("test.txt") 为 文件：
  打印 文件.读取()。
"""
    py_code = _compile(code)
    # 应生成 with open(...) as 变量:
    assert 'with open("test.txt") as 文件:' in py_code or 'with open("test.txt") as file:' in py_code, \
        f"Expected 'with open' in:\n{py_code}"


def test_without_variable():
    """无变量的上下文管理器"""
    code = """
使用 锁定()：
  打印 "已锁定"。
"""
    py_code = _compile(code)
    # 应生成 with 语句（无 as 子句）
    assert 'with ' in py_code
    # 不应有 as 变量
    # 检查打印语句在 with 块中
    assert 'with 锁定():' in py_code or 'with 锁定 ():' in py_code


def test_nested_with():
    """嵌套上下文管理器"""
    code = """
使用 获取资源A() 为 甲：
  使用 获取资源B() 为 乙：
    打印 甲.名称()。
    打印 乙.名称()。
"""
    py_code = _compile(code)
    assert 'with ' in py_code
    # 应有两个 with 嵌套
    with_count = py_code.count('with ')
    assert with_count >= 2, f"Expected 2+ 'with' statements, got {with_count}"


def test_custom_context_manager():
    """自定义上下文管理器类"""
    result = run_duan('''
类 资源：
  构造(名称)：
    设 己.名称 为 名称。
    打印 "创建:" + 名称。
  结束。
  
  段落 __进入__()：
    打印 "进入:" + 己.名称。
    返回 己。
  结束。
  
  段落 __退出__(类型, 值, 回溯)：
    打印 "退出:" + 己.名称。
    返回 假。
  结束。
结束。

使用 新建 资源("测试") 为 资源：
  打印 "使用:" + 资源.名称。
结束。
''')
    lines = result.split('\n')
    assert "创建:测试" in result, f"Expected '创建:测试' in result, got '{result}'"
    assert "进入:测试" in result, f"Expected '进入:测试' in result, got '{result}'"
    assert "使用:测试" in result, f"Expected '使用:测试' in result, got '{result}'"
    assert "退出:测试" in result, f"Expected '退出:测试' in result, got '{result}'"


def test_context_manager_method_names():
    """__进入__ 和 __退出__ 方法名映射"""
    code = """
类 资源：
  构造(名称)：
    设 己.名称 为 名称。
  结束。
  
  段落 __进入__()：
    返回 己。
  结束。
  
  段落 __退出__(类型, 值, 回溯)：
    返回 假。
  结束。
结束。
"""
    py_code = _compile(code)
    # 中文方法名应保留
    assert '__进入__' in py_code or f'__enter__' in py_code, f"Expected __enter__ in generated code:\n{py_code}"
    assert '__退出__' in py_code or '__exit__' in py_code, f"Expected __exit__ in generated code:\n{py_code}"


def test_context_manager_exception_handling():
    """上下文管理器中的异常处理"""
    result = run_duan('''
类 安全资源：
  段落 __进入__()：
    打印 "进入"。
    返回 己。
  结束。
  
  段落 __退出__(类型, 值, 回溯)：
    打印 "退出"。
    返回 假。
  结束。
结束。

尝试：
  使用 新建 安全资源() 为 资源：
    打印 "使用中"。
    抛出 运行时错误("错误！")。
  结束。
捕获 e：
  打印 "捕获:" + 字符串(e)。
结束。
''')
    assert "进入" in result, f"Expected '进入' in result, got '{result}'"
    assert "使用中" in result, f"Expected '使用中' in result, got '{result}'"
    assert "退出" in result, f"Expected '退出' in result, got '{result}'"
    assert "捕获" in result, f"Expected '捕获' in result, got '{result}'"


if __name__ == '__main__':
    tests = [
        ("上下文管理器文件", test_with_file_context),
        ("生成Python with", test_with_stmt_generates_python_with),
        ("无变量上下文", test_without_variable),
        ("嵌套上下文", test_nested_with),
        ("自定义上下文管理器", test_custom_context_manager),
        ("方法名映射", test_context_manager_method_names),
        ("异常处理", test_context_manager_exception_handling),
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