"""修复已恢复的5个文件I/O条目 - 移除PY cleanup和DU setup"""
import json, os, re

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl')
BACKUP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset_backup_v46.jsonl')

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    data = [json.loads(l) for l in f if l.strip()]

# Backup
with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
print(f"Backup saved to {BACKUP_PATH}")

for idx in [1194, 1195, 1196, 1197, 1198]:
    item = data[idx]
    py = item['input']
    du = item['output']
    
    # Remove os.remove lines from PY (JSON string has actual \n newlines)
    py = re.sub('\nos\\.remove\\([^)]+\\)', '', py)
    
    # Remove file setup from DU: the DU string also has actual \n newlines
    # Pattern: 使用 打开文件("...", "w") 为 _f：\n    _f.write(...)\n
    du = re.sub('使用 打开文件\\("[^"]+", "w"\\) 为 _f：\n    _f\\.write\\(.+?\n', '', du)
    
    item['input'] = py
    item['output'] = du
    print(f"Fixed [{idx}]")

# Save
with open(DATASET_PATH, 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"\nSaved {len(data)} entries to {DATASET_PATH}")