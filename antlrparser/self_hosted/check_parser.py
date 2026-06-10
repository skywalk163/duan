"""检查 parser.duan 的解析状态"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from duan_visitor import DuanParser

parser_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parser.duan')
with open(parser_path, 'r', encoding='utf-8') as f:
    source = f.read()

print(f"parser.duan 源码行数: {len(source.split(chr(10)))}")
print(f"源码字符数: {len(source)}")
print()

parser = DuanParser()
module = parser.parse(source)

if module is None:
    print(f"解析失败！共 {len(parser.errors)} 个错误:")
    for i, err in enumerate(parser.errors):
        print(f"  [{i}] {err}")
else:
    print("解析成功!")
    print(f"  段落定义: {len(module.segments)}")
    print(f"  顶层语句: {len(module.statements)}")
    for seg in module.segments:
        print(f"    - 《{seg.name}》({len(seg.parameters)} 参数)")