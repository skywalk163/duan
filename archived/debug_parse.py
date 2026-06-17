"""Debug script to find exact location of parsing error"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from duan_interpreter import run_source, DuanValue

BASE_DIR = '.'

def uw(v):
    if isinstance(v, DuanValue):
        return uw(v.value)
    if isinstance(v, dict):
        return {k: uw(v) for k, v in v.items()}
    if isinstance(v, list):
        return [uw(x) for x in v]
    return v

# Load tokenizer
with open(os.path.join(BASE_DIR, 'tokenizer.duan'), 'r', encoding='utf-8') as f:
    ti = run_source(f.read())
tf = ti.env.get('分词器').value

def gt(code):
    r = ti._call_function(tf, [DuanValue(code, '串')])
    raw = uw(r)
    wr = []
    for t in raw:
        wr.append(DuanValue({
            'type': DuanValue(t['type'], '串'),
            'text': DuanValue(t['text'], '串'),
            'line': DuanValue(t['line'], '数'),
            'col': DuanValue(t['col'], '数'),
        }, '典'))
    return DuanValue(wr, '列'), raw

# Load parser
c = ''
for n in ['ast.duan', 'parser.duan']:
    with open(os.path.join(BASE_DIR, n), 'r', encoding='utf-8') as f:
        c += f.read() + '\n'

with open(os.path.join(BASE_DIR, 'parser.duan'), 'r', encoding='utf-8') as f:
    src = f.read()

tv, raw_tokens = gt(src)
print('Total tokens:', len(raw_tokens))

# Find all K_EQUAL positions in tokens
print('\nK_EQUAL tokens (up to 5):')
count = 0
for i, t in enumerate(raw_tokens):
    if t['type'] == 'K_EQUAL':
        print(f'  Token {i}: line={t["line"]}, col={t["col"]}, text="{t["text"]}"')
        # Show source line
        lines = src.split('\n')
        if 0 < t['line'] <= len(lines):
            print(f'    Source: {lines[t["line"]-1][:100]}')
        count += 1
        if count >= 5:
            break

i = run_source(c)
pf = i.env.get('解析').value

try:
    r = i._call_function(pf, [tv])
    p = uw(r)
    print(f'\nResult type: {p.get("_type")}')
    if p.get('_type') == 'Error':
        line = p.get('line', 0)
        col = p.get('col', 0)
        msg = p.get('message', '')
        print(f'Error: {msg} at line {line}, col {col}')
        src_lines = src.split('\n')
        if 0 < line <= len(src_lines):
            start = max(0, line-4)
            end = min(len(src_lines), line+3)
            for i in range(start, end):
                marker = '>>>' if i+1 == line else '   '
                print(f'{marker} {i+1}: {src_lines[i][:120]}')
        # Find token context
        print(f'\nToken context around error:')
        for i, t in enumerate(raw_tokens):
            if t['line'] == line and abs(t['col'] - col) < 10:
                start_idx = max(0, i-3)
                end_idx = min(len(raw_tokens), i+4)
                print(f'  Tokens [{start_idx}-{end_idx}]:')
                for j in range(start_idx, end_idx):
                    tok = raw_tokens[j]
                    mark = '>>>' if j == i else '   '
                    print(f'    {mark} [{j}] {tok["type"]}="{tok["text"]}" L{tok["line"]}:{tok["col"]}')
                break
    else:
        inner = p.get('result', {})
        segs = inner.get('segments', [])
        print(f'Segments: {len(segs)}')
except Exception as e:
    print(f'Exception: {e}')
    import traceback
    traceback.print_exc()