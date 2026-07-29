"""修复已恢复的5个文件I/O条目 - 移除DU代码中的删除文件调用（parser bug workaround）"""
import json, os, re

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl')
BACKUP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset_backup_v45.jsonl')

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    data = [json.loads(l) for l in f if l.strip()]

# Backup
with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
print(f"Backup saved to {BACKUP_PATH}")

# Fix entries 1194-1198: remove 删除文件 from DU code
# The PY code handles file cleanup. Removing 删除文件 avoids the parser bug
# where statements after a 使用 block are incorrectly placed inside it.
for idx in [1194, 1195, 1196, 1197, 1198]:
    item = data[idx]
    du = item['output']
    # Remove 删除文件("...") calls
    du = re.sub(r'\\n删除文件\("[^"]+"\)', '', du)
    item['output'] = du
    print(f"Fixed [{idx}]: removed 删除文件 from DU")

# Save
with open(DATASET_PATH, 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"\nSaved {len(data)} entries to {DATASET_PATH}")