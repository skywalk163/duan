"""合并所有组件并运行测试"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from duan_interpreter import run_source


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("合并段言自举组件...")
    
    # 合并所有组件
    files = [
        'tokenizer.duan',
        'ast.duan', 
        'parser.duan',
        'interpreter.duan',
        'simple_test.duan'
    ]
    
    combined = ''
    for f in files:
        print(f"  加载 {f}")
        with open(os.path.join(BASE_DIR, f), 'r', encoding='utf-8') as fp:
            combined += fp.read() + '\n\n'
    
    print(f"\n总代码长度: {len(combined)} 字符")
    print()
    
    # 执行
    print("执行合并代码...")
    print("=" * 60)
    
    try:
        interp = run_source(combined)
        output = interp.get_output()
        print(output)
        print("=" * 60)
        print("执行成功！")
        return 0
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())