"""调试：检查 tokenizer.duan 解析问题"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from duan_tokenizer import DuanLangTokenizer

tokenizer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tokenizer.duan')
with open(tokenizer_path, 'r', encoding='utf-8') as f:
    source = f.read()

lines = source.split('\n')
print("Token 18~42:")
t = DuanLangTokenizer()
tokens = t.tokenize(source)
for i, tok in enumerate(tokens):
    if 18 <= i <= 42:
        print(f"  {i:2d}: {tok}")