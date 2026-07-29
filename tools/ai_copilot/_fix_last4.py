import json, os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl')
with open(path, 'r', encoding='utf-8') as f:
    items = [json.loads(l) for l in f if l.strip()]

# Fix 19: DU should match PY (d = {'key': 0}, del d['key'])
items[19]['output'] = "设 d 为 {'key': 0}\\n删除 d[\"key\"]"

# Fix 168: DU should match PY (full Dog class)
items[168]['output'] = '类 Dog：\\n    构造 接收 name：\\n        己.name 为 name\\n    段落 speak：\\n        打印(f\"{己.name}: woof!\")\\n设 obj 为 新建 Dog("Rex")\\nobj.speak()'

# Fix 425: DU should use text.index not text.find
items[425]['output'] = '设 index 为 0\\n设 text 为 ["abc"]\\n设 idx 为 text.index("abc")'

# Fix 521: DU should have n = 0 not n = ''
items[521]['output'] = '设 n 为 0\\n打印(f"Is {n} even? {n 取余 2 等于 0}")'

with open(path, 'w', encoding='utf-8') as f:
    for item in items:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print('Fixed 4 remaining issues')