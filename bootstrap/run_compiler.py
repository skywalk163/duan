"""
run_compiler.py - Run the bootstrap compiler pipeline (v3.2)

This script uses the SRC backend to compile the bootstrap compiler
(written in Duan) to Python, then executes it to verify correctness.

Usage:
    python run_compiler.py <source.duan> [output.py]

This validates the bootstrap compiler pipeline design end-to-end.
"""

import sys
import os
import types

# Add required paths
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, '..', 'src'))
sys.path.insert(0, os.path.join(_script_dir, '..'))


def _compile_src(source: str) -> str:
    """用 SRC 后端编译为 Python 代码"""
    from duan_parser_v3 import DuanParser
    from code_generator import PythonCodeGenerator

    parser = DuanParser()
    module = parser.parse(source)

    generator = PythonCodeGenerator()
    return generator.generate(module)


def compile_bootstrap_dir(source_path, output_path=None):
    """
    Compile a .duan source file using the SRC backend.

    The bootstrap compiler files use v3.2 syntax and are compiled
    to Python using the SRC parser + PythonCodeGenerator.

    Args:
        source_path: Path to the .duan source file
        output_path: Optional path to write generated Python code

    Returns:
        The generated Python code as a string
    """
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"Reading: {source_path} ({len(source)} chars)")

    # Parse with SRC backend
    print("Parsing with SRC backend...")
    py_code = _compile_src(source)

    print(f"Generated {len(py_code)} characters of Python code")

    # Write output if requested
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(py_code)
        print(f"Written to: {output_path}")

    return py_code


def execute_generated_code(py_code):
    """Execute generated Python code and return the namespace."""
    # Set up _duan_builtin namespace
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.打印 = print
    _duan_builtin.输出 = print
    _duan_builtin.转字符串 = str
    _duan_builtin.转整数 = int
    _duan_builtin.列表创建 = list
    _duan_builtin.列表长度 = len
    _duan_builtin.列表获取 = lambda lst, i: lst[i]
    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
    _duan_builtin.列表弹出 = lambda lst: lst.pop()
    _duan_builtin.列表包含 = lambda lst, item: item in lst
    _duan_builtin.字典创建 = dict
    _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
    _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)
    _duan_builtin.字典包含键 = lambda d, k: k in d
    _duan_builtin.字典键列表 = lambda d: list(d.keys())
    _duan_builtin.字符串长度 = len
    _duan_builtin.字符串获取 = lambda s, i: s[i]
    _duan_builtin.截取 = lambda s, start, end: s[start:end]
    _duan_builtin.分割字符串 = lambda s, sep=' ': s.split(sep)
    _duan_builtin.连接字符串 = lambda parts, sep='': sep.join(parts)
    _duan_builtin.替换字符串 = lambda s, old, new: s.replace(old, new)
    _duan_builtin.去除空白 = lambda s: s.strip()
    _duan_builtin.列表排序 = lambda lst, reverse=False: lst.sort(reverse=reverse)
    _duan_builtin.列表反转 = lambda lst: lst.reverse()
    _duan_builtin.是整数 = lambda x: isinstance(x, int)
    _duan_builtin.是浮点 = lambda x: isinstance(x, float)
    _duan_builtin.是字符串 = lambda x: isinstance(x, str)
    _duan_builtin.是列表 = lambda x: isinstance(x, list)
    _duan_builtin.是字典 = lambda x: isinstance(x, dict)
    _duan_builtin.是空 = lambda x: x is None
    _duan_builtin.字典值列表 = lambda d: list(d.values())
    _duan_builtin.字典项列表 = lambda d: list(d.items())
    _duan_builtin.字典删除 = lambda d, k: d.pop(k, None)
    _duan_builtin.随机整数 = lambda a, b: __import__('random').randint(a, b)
    _duan_builtin.随机浮点 = lambda: __import__('random').random()
    _duan_builtin.随机选择 = lambda lst: __import__('random').choice(lst)
    _duan_builtin._读文件 = lambda path: open(path, 'r', encoding='utf-8').read()

    namespace = {'_duan_builtin': _duan_builtin}
    exec(py_code, namespace)
    return namespace


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    source_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(source_path):
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    # Step 1: Compile the source
    py_code = compile_bootstrap_dir(source_path, output_path)
    if py_code is None:
        sys.exit(1)

    # Step 2: Display or execute the generated code
    if not output_path:
        print("\n" + "=" * 60)
        print("Generated Python Code:")
        print("=" * 60)
        for i, line in enumerate(py_code.split('\n')[:50]):
            print(f"  {i:4d}: {line}")

        remaining = py_code.split('\n')[50:]
        if remaining:
            print(f"  ... ({len(remaining)} more lines)")

    # Step 3: Try to execute the generated code
    print("\n" + "=" * 60)
    print("Executing generated code...")
    print("=" * 60)
    try:
        execute_generated_code(py_code)
        print("\nExecution succeeded!")
    except Exception as e:
        print(f"\nExecution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()