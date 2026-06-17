import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from duan_interpreter import run_source, DuanValue

tokenizer_path = os.path.join(os.path.dirname(__file__), 'tokenizer.duan')
with open(tokenizer_path, 'r', encoding='utf-8') as f:
    tokenizer_code = f.read()

tok_interp = run_source(tokenizer_code)
tok_func = tok_interp.env.get('分词器').value

test_code = '定义x等于10加20。'
tokens = tok_interp._call_function(tok_func, [DuanValue(test_code, '串')])

def unwrap(v):
    if isinstance(v, DuanValue):
        return unwrap(v.value)
    if isinstance(v, dict):
        return {k: unwrap(v) for k, v in v.items()}
    if isinstance(v, list):
        return [unwrap(x) for x in v]
    return v

token_list = unwrap(tokens)
for t in token_list:
    print(f"类型: {t['type']}, 文本: {t['text']}")