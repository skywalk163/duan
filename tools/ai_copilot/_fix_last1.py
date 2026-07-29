import json, os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl')
with open(path, 'r', encoding='utf-8') as f:
    items = [json.loads(l) for l in f if l.strip()]

# Fix 19: '删除' maps to 'remove' (method), not 'del'. 
# Since DU doesn't support 'del' directly, just remove this entry
# Actually, let's try '字典删除' which maps to del
# Or just change the PY to not use del
items[19]['input'] = "d = {'key': 0}\nd = {}"
items[19]['output'] = "设 d 为 {'key': 0}\n设 d 为 {}"

with open(path, 'w', encoding='utf-8') as f:
    for item in items:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print('Fixed entry 19')