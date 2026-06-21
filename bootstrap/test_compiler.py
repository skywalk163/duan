"""
test_compiler.py - Test the bootstrap compiler pipeline

This script manually runs the bootstrap compilation pipeline:
1. Loads the bootstrap .duan source files
2. Sets up the runtime environment
3. Executes the compilation pipeline (lexer -> parser -> codegen)

This bypasses the broken ANTLR compile path in the CLI.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'antlrparser'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set up the _duan_builtin module for the bootstrap code to use
import types
_duan_builtin = types.ModuleType('_duan_builtin')
_duan_builtin.打印 = print
_duan_builtin.转字符串 = str
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

# Make _duan_builtin accessible globally
import builtins
builtins._duan_builtin = _duan_builtin


def load_duan_module(filepath, module_name=None):
    """Load a .duan file as a Python module by executing it."""
    if module_name is None:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
    
    # Read the source file
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Use the existing Duan ANTLR parser to compile
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cli'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    try:
        from duan_visitor import DuanParser
        parser = DuanParser()
        module = parser.parse(source)
        if module is None:
            print(f"Error parsing {filepath}:")
            for err in parser.errors:
                print(f"  {err}")
            return None
        
        from code_generator_unified import UnifiedCodeGenerator
        generator = UnifiedCodeGenerator()
        py_code = generator.generate(module)
        
        # Execute the generated Python code
        namespace = {'_duan_builtin': _duan_builtin}
        exec(py_code, namespace)
        
        return namespace
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    # The bootstrap directory
    bootstrap_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("Bootstrap Compiler Test")
    print("=" * 60)
    
    # Compile the bootstrap source file that we want to test
    # For now, let's just test the lexer by compiling a simple Duan program
    test_source = os.path.join(bootstrap_dir, 'test_simple.duan')
    if os.path.exists(test_source):
        with open(test_source, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"\n1. Parsing test source: {test_source}")
        print(f"   Source length: {len(source)} chars")
        
        from duan_visitor import DuanParser
        parser = DuanParser()
        module = parser.parse(source)
        
        if module is None:
            print("   Parse failed:")
            for err in parser.errors:
                print(f"     {err}")
        else:
            print(f"   Parse succeeded! AST: {type(module).__name__}")
            print(f"   Statements: {len(module.statements)}")
            
            # Try generating Python code
            from code_generator_unified import UnifiedCodeGenerator
            generator = UnifiedCodeGenerator()
            try:
                py_code = generator.generate(module)
                out_path = os.path.join(bootstrap_dir, 'test_simple_output.py')
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(py_code)
                print(f"   Generated Python code saved to: {out_path}")
                print(f"   Python output length: {len(py_code)} chars")
                print("\n   Generated output (first 30 lines):")
                for i, line in enumerate(py_code.split('\n')[:30]):
                    print(f"     {line}")
            except Exception as e:
                print(f"   Code generation error: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()