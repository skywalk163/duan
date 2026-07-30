import json, re

data = [json.loads(l) for l in open('sft_dataset.jsonl', encoding='utf-8')]

fixes = 0
for i, item in enumerate(data):
    du = item['output']
    original = du
    
    # DU strings use \\n (two chars: backslash+n) for line breaks
    # Replace \\n<spaces>pass at end of block with \\n<spaces>设 _ 为 空
    du = re.sub(r'(\\n\s+)pass(\\n|$)', r'\1设 _ 为 空\2', du)
    
    if du != original:
        fixes += 1
        data[i]['output'] = du

print(f"修复了 {fixes} 个条目")

# Verify
pass_count = 0
for i, item in enumerate(data):
    du = item['output']
    for m in re.finditer(r'\bpass\b', du):
        before = du[:m.start()]
        sq = before.count("'")
        dq = before.count('"')
        if sq % 2 == 0 and dq % 2 == 0:
            pass_count += 1
            print(f"  [{i}] still has pass: ...{du[max(0,m.start()-10):m.end()+10]}...")
            break

print(f"残留: pass={pass_count}")

# Save
with open('sft_dataset.jsonl', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
print(f"数据集已保存: {len(data)} 条")