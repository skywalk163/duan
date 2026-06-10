#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模块系统完整工作流

测试：
1. 编译模块文件为Python
2. 验证导入语句生成正确
3. 验证导出语句生成正确
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from duan_parser_v3 import DuanParser, ImportStmt, ExportStmt
from code_generator import PythonCodeGenerator


def compile_duan_file(duan_path: str, output_dir: str = None):
    """编译单个 .duan 文件为 Python"""
    
    print(f"\n{'='*60}")
    print(f"编译: {duan_path}")
    print('='*60)
    
    # 读取段言代码
    with open(duan_path, 'r', encoding='utf-8') as f:
        duan_code = f.read()
    
    print(f"\n段言代码:\n{duan_code}")
    
    # 编译
    parser = DuanParser()
    generator = PythonCodeGenerator()
    
    try:
        module = parser.parse(duan_code)
        python_code = generator.generate(module)
        
        print(f"\n生成的Python代码:\n{python_code}")
        
        # 保存到输出目录
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 使用相同的文件名，但改为 .py 扩展名
            py_filename = Path(duan_path).stem + '.py'
            py_path = output_path / py_filename
            
            with open(py_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
            
            print(f"\n[OK] 已保存到: {py_path}")
        
        return python_code
        
    except Exception as e:
        print(f"\n[ERROR] 编译失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_module_workflow():
    """测试完整的模块工作流"""
    
    print("="*60)
    print("段言模块系统 - 完整工作流测试")
    print("="*60)
    
    # 模块目录
    modules_dir = Path("examples/modules")
    output_dir = Path("examples/compiled")
    
    # 测试文件列表
    test_files = [
        "math_utils.duan",
        "string_utils.duan",
        "main.duan"
    ]
    
    results = []
    
    for filename in test_files:
        duan_path = modules_dir / filename
        
        if not duan_path.exists():
            print(f"\n[ERROR] 文件不存在: {duan_path}")
            continue
        
        python_code = compile_duan_file(str(duan_path), str(output_dir))
        
        if python_code:
            results.append((filename, True, python_code))
        else:
            results.append((filename, False, None))
    
    # 总结
    print("\n" + "="*60)
    print("编译结果总结")
    print("="*60)
    
    for filename, success, code in results:
        status = "[OK] 成功" if success else "[FAIL] 失败"
        print(f"{status}: {filename}")
    
    # 统计
    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    print(f"\n成功: {success_count}/{total_count}")
    
    # 检查关键内容
    print("\n" + "="*60)
    print("关键内容验证")
    print("="*60)
    
    for filename, success, code in results:
        if not success:
            continue
        
        print(f"\n{filename}:")
        
        # 检查导入语句
        if 'import' in code:
            import_lines = [line for line in code.split('\n') if 'import' in line]
            print(f"  导入语句: {len(import_lines)} 条")
            for line in import_lines:
                print(f"    {line.strip()}")
        
        # 检查导出语句
        if '__all__' in code:
            print(f"  导出语句: [OK]")
        
        # 检查函数定义
        def_lines = [line for line in code.split('\n') if line.strip().startswith('def ')]
        print(f"  函数定义: {len(def_lines)} 个")


if __name__ == '__main__':
    test_module_workflow()
