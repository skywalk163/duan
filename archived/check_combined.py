"""检查合并后源码的解析状态"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from duan_visitor import DuanParser

base_dir = os.path.dirname(os.path.abspath(__file__))

# Read and combine
ast_path = os.path.join(base_dir, 'ast.duan')
with open(ast_path, 'r', encoding='utf-8') as f:
    ast_source = f.read()

parser_path = os.path.join(base_dir, 'parser.duan')
with open(parser_path, 'r', encoding='utf-8') as f:
    parser_source = f.read()

combined = ast_source + '\n' + parser_source

print(f"合并源码总行数: {len(combined.split(chr(10)))}")
print(f"合并源码字符数: {len(combined)}")

parser = DuanParser()
module = parser.parse(combined)

if module is None:
    print(f"解析失败！共 {len(parser.errors)} 个错误:")
    for i, err in enumerate(parser.errors):
        print(f"  [{i}] {err}")
else:
    print(f"解析成功!")
    print(f"  段落定义: {len(module.segments)}")
    print(f"  顶层语句: {len(module.statements)}")