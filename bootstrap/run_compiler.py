"""
run_compiler.py - Run the bootstrap compiler pipeline

This script demonstrates the bootstrap compilation pipeline by:
1. Using the existing Duan Python-based compiler to parse and compile
   a .duan source file into Python code
2. Executing the generated Python code to verify correctness

Usage:
    python run_compiler.py <source.duan> [output.py]

This validates the bootstrap compiler pipeline design end-to-end.
"""

import sys
import os

# Add required paths
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, '..', 'src'))
sys.path.insert(0, os.path.join(_script_dir, '..', 'antlrparser'))


def compile_source(source_path, output_path=None):
    """
    Compile a .duan source file using the existing compiler pipeline.
    
    Args:
        source_path: Path to the .duan source file
        output_path: Optional path to write generated Python code
        
    Returns:
        The generated Python code as a string
    """
    from code_generator_unified import UnifiedCodeGenerator
    from duan_visitor import DuanParser
    
    with open(source_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    print(f"Reading: {source_path} ({len(source)} chars)")
    
    # Parse with ANTLR
    print("Parsing with ANTLR...")
    parser = DuanParser()
    module = parser.parse(source)
    if module is None:
        print("Parse failed:")
        for err in parser.errors:
            print(f"  {err}")
        return None
    
    print(f"Parse succeeded! ({len(module.segments)} segments defined)")
    
    # Generate Python code
    print("Generating Python code...")
    generator = UnifiedCodeGenerator()
    py_code = generator.generate(module)
    
    print(f"Generated {len(py_code)} characters of Python code")
    
    # Write output if requested
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(py_code)
        print(f"Written to: {output_path}")
    
    return py_code


def execute_generated_code(py_code):
    """Execute generated Python code and return the namespace."""
    import types
    
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
    py_code = compile_source(source_path, output_path)
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