"""检查 ast.duan 的解析状态"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from duan_visitor import DuanParser

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ast.duan')
with open(path, 'r', encoding='utf-8') as f:
    source = f.read()

parser = DuanParser()
module = parser.parse(source)

if module is None:
    print(f"解析失败！共 {len(parser.errors)} 个错误:")
    for i, err in enumerate(parser.errors):
        print(f"  [{i}] {err}")
else:
    print(f"解析成功! {len(module.segments)} 个段落定义")
    for seg in module.segments:
        print(f"  - 《{seg.name}》({len(seg.parameters)} 参数)")