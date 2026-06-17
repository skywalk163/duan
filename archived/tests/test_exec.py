"""
测试简单程序编译和运行
"""

import sys
sys.path.insert(0, 'src')

from duan_parser_v3 import DuanParser
from code_generator import PythonCodeGenerator

# 简单测试
code = '''
定义甲等于三。
打印甲。
'''

print("段言代码:")
print(code)

parser = DuanParser()
generator = PythonCodeGenerator()

try:
    # 解析
    module = parser.parse(code)
    print("[OK] 解析成功")
    
    # 生成Python代码
    python_code = generator.generate(module)
    print("\nPython代码:")
    print(python_code)
    
    # 运行
    print("\n运行结果:")
    exec_globals = {}
    exec(python_code, exec_globals)
    
except Exception as e:
    print(f"[FAIL] 失败: {e}")
    import traceback
    traceback.print_exc()
