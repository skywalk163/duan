"""测试 LLVM 后端异步支持"""
import sys
import os
import tempfile
import subprocess
sys.path.insert(0, 'src')

from llvm.compiler import compile_source_typed, find_clang

def run_test(name, code):
    """运行一个测试"""
    print("=" * 60)
    print(f"测试: {name}")
    print("=" * 60)
    
    try:
        # 生成 IR
        ir = compile_source_typed(code, verbose=False)
        
        # 保存 IR
        ir_path = f'tests/_test_{name}.ll'
        with open(ir_path, 'w', encoding='utf-8') as f:
            f.write(ir)
        
        # 编译为可执行文件
        clang = find_clang()
        runtime_c = 'src/llvm/runtime_typed.c'
        exe_path = f'tests/_test_{name}.exe'
        
        result = subprocess.run(
            [clang, '-O2', '-o', exe_path, ir_path, runtime_c],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        
        if result.returncode != 0:
            print(f"编译失败!")
            print("stderr:", result.stderr[:3000])
            return False
        
        print(f"编译成功")
        
        # 运行
        run_result = subprocess.run(
            [exe_path],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=10
        )
        print(f"输出:\n{run_result.stdout}")
        if run_result.stderr:
            print(f"错误输出: {run_result.stderr}")
        print(f"返回码: {run_result.returncode}")
        
        return True
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"错误: {e}")
        return False

def test_async_simple():
    """测试简单的异步段落（仅创建，不执行）"""
    code = """
异步 段落 测试异步：
    输出("异步函数开始")
结束

输出("主程序开始")
x = 测试异步()
输出("主程序结束")
"""
    return run_test("async_simple", code)

def test_async_scope():
    """测试异步作用域（结构化并发）"""
    code = """
异步 段落 任务1：
    输出("任务1开始")
    返回(42)
结束

异步 段落 任务2：
    输出("任务2开始")
    返回("hello")
结束

输出("程序开始")

异步作用域：
    任务1()
    任务2()
结束

输出("程序结束")
"""
    return run_test("async_scope", code)

def test_async_await():
    """测试在异步作用域中使用 await"""
    code = """
异步 段落 任务1：
    输出("任务1开始")
    返回(42)
结束

异步 段落 主任务：
    输出("主任务开始")
    x = 等待 任务1()
    输出("等待结果:")
    输出(x)
    返回(x)
结束

输出("程序开始")

异步作用域：
    主任务()
结束

输出("程序结束")
"""
    return run_test("async_await", code)

def test_async_chain():
    """测试链式 await：一个协程 await 另一个协程"""
    code = """
异步 段落 计算：
    输出("计算开始")
    返回(100)
结束

异步 段落 累加器：
    输出("累加器开始")
    a = 等待 计算()
    输出("累加器得到:")
    输出(a)
    返回(a)
结束

输出("程序开始")

异步作用域：
    累加器()
结束

输出("程序结束")
"""
    return run_test("async_chain", code)

def test_async_multiple_await():
    """测试一个协程中多次 await"""
    code = """
异步 段落 任务甲：
    输出("任务甲")
    返回(10)
结束

异步 段落 任务乙：
    输出("任务乙")
    返回(20)
结束

异步 段落 主任务：
    输出("主任务开始")
    a = 等待 任务甲()
    b = 等待 任务乙()
    输出("结果:")
    输出(a)
    输出(b)
    返回(a)
结束

输出("程序开始")

异步作用域：
    主任务()
结束

输出("程序结束")
"""
    return run_test("async_multiple_await", code)

if __name__ == '__main__':
    test_async_simple()
    print()
    test_async_scope()
    print()
    test_async_await()
    print()
    test_async_chain()
    print()
    test_async_multiple_await()
