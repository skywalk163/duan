"""
段言（Duan）双后端功能对齐测试

对每个特性同时跑 src 和 ANTLR 两个后端，比较输出结果。
用于确保两个后端的行为一致。

运行方式：
    python antlrparser/test/test_dual_backend.py
"""

import sys
import os
import traceback

# 添加 src 后端路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# 添加 ANTLR 后端路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# 添加当前目录
sys.path.insert(0, os.path.dirname(__file__))


# =============================================================================
# SRC 后端（parser_v3 + code_generator）
# =============================================================================

def run_src(code: str) -> str:
    """使用 src 后端（parser_v3 → code_generator → exec）"""
    from duan_parser_v3 import DuanParser
    from code_generator import PythonCodeGenerator
    
    parser = DuanParser()
    try:
        module = parser.parse(code)
    except Exception as e:
        raise RuntimeError(f"SRC解析失败: {e}")
    
    generator = PythonCodeGenerator()
    try:
        py_code = generator.generate(module)
    except Exception as e:
        raise RuntimeError(f"SRC代码生成失败: {e}")
    
    # 执行生成的代码并捕获输出
    output_lines = []
    namespace = {}
    
    # 替换 print 为捕获输出
    original_print = __builtins__.print if isinstance(__builtins__, dict) else __builtins__.print
    def _capture_print(*args, **kwargs):
        line = ' '.join(str(a) for a in args)
        output_lines.append(line)
        # 同时也输出到控制台（便于调试）
        original_print(*args, **kwargs)
    
    namespace['print'] = _capture_print
    
    try:
        exec(py_code, namespace)
    except Exception as e:
        raise RuntimeError(f"SRC执行失败: {type(e).__name__}: {e}")
    return '\n'.join(output_lines)


# =============================================================================
# ANTLR 后端（antlrparser 路径）
# =============================================================================

def run_antlr(code: str) -> str:
    """使用 ANTLR 后端（duan_visitor → duan_interpreter）"""
    from duan_visitor import DuanParser
    from duan_interpreter import Interpreter
    
    parser = DuanParser()
    module = parser.parse(code)
    if module is None:
        errors = '\n'.join(parser.errors)
        raise RuntimeError(f"ANTLR 解析失败:\n{errors}")
    
    interpreter = Interpreter()
    interpreter.interpret(module)
    return interpreter.get_output()


# =============================================================================
# 测试用例
# =============================================================================

PASS = 0
FAIL = 0

def test_feature(name: str, code: str):
    """测试单个特性"""
    global PASS, FAIL
    src_output = None
    antlr_output = None
    src_error = None
    antlr_error = None
    
    try:
        src_output = run_src(code)
    except Exception as e:
        src_error = f"{type(e).__name__}: {e}"
    
    try:
        antlr_output = run_antlr(code)
    except Exception as e:
        antlr_error = f"{type(e).__name__}: {e}"
    
    if src_output == antlr_output:
        PASS += 1
        print(f"  [OK] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")
        src_display = src_output if src_output is not None else (src_error or "(无输出)")
        antlr_display = antlr_output if antlr_output is not None else (antlr_error or "(无输出)")
        print(f"     SRC:   {src_display}")
        print(f"     ANTLR: {antlr_display}")


def main():
    global PASS, FAIL
    
    print("=" * 60)
    print("段言 双后端功能对齐测试")
    print("=" * 60)
    
    # ─── 基础表达式 ───
    print("\n--- 基础表达式 ---")
    
    test_feature("整数", """
设 甲 为 四十二。
打印 甲。
""")
    
    test_feature("浮点数", """
设 甲 为 三点一四。
打印 甲。
""")
    
    test_feature("字符串", """
设 甲 为 "你好，世界"。
打印 甲。
""")
    
    test_feature("布尔值", """
打印 真。
打印 假。
""")
    
    # ─── 算术运算 ───
    print("\n--- 算术运算 ---")
    
    test_feature("加法", """
设 甲 为 一 加 二。
打印 甲。
""")
    
    test_feature("减法", """
设 甲 为 十 减 三。
打印 甲。
""")
    
    test_feature("乘法", """
设 甲 为 六 乘 七。
打印 甲。
""")
    
    test_feature("除法", """
设 甲 为 十 除 三。
打印 甲。
""")
    
    test_feature("混合运算", """
设 甲 为 一 加 二 乘 三。
打印 甲。
""")
    
    # ─── 比较运算 ───
    print("\n--- 比较运算 ---")
    
    test_feature("大于", """
设 甲 为 五 大于 三。
打印 甲。
""")
    
    test_feature("小于", """
设 甲 为 二 小于 八。
打印 甲。
""")
    
    test_feature("相等", """
设 甲 为 三 等于 三。
打印 甲。
""")
    
    # ─── 逻辑运算 ───
    print("\n--- 逻辑运算 ---")
    
    test_feature("且（and）", """
设 甲 为 真 且 真。
打印 甲。
设 乙 为 真 且 假。
打印 乙。
""")
    
    test_feature("或（or）", """
设 甲 为 真 或 假。
打印 甲。
设 乙 为 假 或 假。
打印 乙。
""")
    
    test_feature("与（and 别名）", """
设 甲 为 真 与 真。
打印 甲。
设 乙 为 假 与 真。
打印 乙。
""")
    
    # ─── 变量 ───
    print("\n--- 变量 ---")
    
    test_feature("变量声明和使用", """
设 甲 为 十。
设 乙 为 甲 加 五。
打印 乙。
""")
    
    test_feature("变量重新赋值", """
设 甲 为 一。
设 甲 为 甲 加 一。
打印 甲。
""")
    
    # ─── 条件语句 ───
    print("\n--- 条件语句 ---")
    
    test_feature("如果-真分支", """
设 甲 为 五。
如果 甲 大于 三：
打印 真。
结束。
""")
    
    test_feature("如果-假分支", """
设 甲 为 一。
如果 甲 大于 三：
打印 真。
否则：
打印 假。
结束。
""")
    
    # ─── 循环 ───
    print("\n--- 循环 ---")
    
    test_feature("当循环", """
设 甲 为 一。
当 甲 小于 四：
打印 甲。
设 甲 为 甲 加 一。
结束。
""")
    
    # ─── 自定义函数 ───
    print("\n--- 函数 ---")
    
    test_feature("无参数函数", """
段 问候 接收：
打印 "你好"。
结束。
问候。
""")
    
    test_feature("有参数函数", """
段 加法 接收 甲, 乙 返回：
返回 甲 加 乙。
结束。
设 结果 为 加法 三 五。
打印 结果。
""")
    
    # ─── 打印 ───
    print("\n--- 打印 ---")
    
    test_feature("多值打印", """
打印 一。
打印 二。
打印 三。
""")
    
    # ─── 新建（类实例化）─
    print("\n--- 新建（类实例化）---")
    
    test_feature("新建 有括号", """
设 点 为 类 接收 甲, 乙：
属性 横 为 甲。
属性 纵 为 乙。
结束。
设 位置 为 新建 点(三, 五)。
打印 位置。
""")
    
    test_feature("新建 无括号", """
设 点 为 类 接收 甲, 乙：
属性 横 为 甲。
属性 纵 为 乙。
结束。
设 位置 为 新建 点 三, 五。
打印 位置。
""")
    
    # ─── SelfReference ───
    print("\n--- SelfReference ---")
    
    test_feature("SelfReference", """
设 点 为 类 接收 甲, 乙：
属性 横 为 甲。
属性 纵 为 乙。
段 显示 接收：
打印 己横。
打印 己纵。
结束。
结束。
设 位置 为 新建 点 三, 五。
位置。显示。
""")
    
    # ─── 总计 ───
    print(f"\n{'=' * 60}")
    total = PASS + FAIL
    print(f"总计: {total}  |  通过: {PASS}  |  失败: {FAIL}")
    if FAIL == 0:
        print("全部通过！双后端行为一致")
    else:
        print(f"{FAIL} 个测试不匹配，需要进一步对齐")
    print('=' * 60)
    
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())