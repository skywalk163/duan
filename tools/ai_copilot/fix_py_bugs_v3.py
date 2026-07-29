#!/usr/bin/env python3
"""综合修复 Python 代码 bug - 第三轮：同时修复PY和DU"""
import json, os, re

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl')
BACKUP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sft_dataset_backup_v41.jsonl')

items = []
with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            items.append(json.loads(line))

# Backup
with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
    for item in items:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
print(f"Backup saved to {BACKUP_PATH}")

fix_count = 0
remove_indices = set()

# ============================================================
# Fix 168: Dog stub needs __init__
# ============================================================
item = items[168]
py = item['input']
# Add __init__ to Dog stub
py = py.replace('class Dog:\n    pass', 'class Dog:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        print(f"{self.name}: woof!")')
item['input'] = py
# Fix DU: add proper class definition
du = item['output']
du = du.replace('类 Dog：\n    跳过', '类 Dog：\n    构造 接收 name：\n        己.name 为 name\n    段落 speak：\n        打印(f"{己.name}: woof!")')
# Remove fake var defs
du = re.sub(r'设 Rex 为 空\\n', '', du)
du = re.sub(r'设 speak 为 空\\n', '', du)
item['output'] = du
fix_count += 1
print(f"  [168] fixed Dog class with __init__")

# ============================================================
# Fix 425: text = [] should be text = ['abc']
# ============================================================
item = items[425]
py = item['input']
py = py.replace('text = []', "text = ['abc']")
item['input'] = py
du = item['output']
du = du.replace('设 text 为 []', "设 text 为 ['abc']")
du = re.sub(r'设 abc 为 空\\n', '', du)
item['output'] = du
fix_count += 1
print(f"  [425] fixed text = ['abc']")

# ============================================================
# Fix PY entries that have str/int type mismatches
# For these, the PY and DU are fundamentally mismatched - remove them
# ============================================================
# 495: PY x='Result: ' y=5, DU x=0 y=0
# 506: PY x='', DU x=0 (format code d)
# 507: PY x='', DU x=0 (format specifier)
# 509: PY x='', DU x=0 (format code %)
# 518: PY mixed str/int, DU all int
# 519: PY mem='', DU mem=0
# 524: PY n='', DU n=''
# 529: PY a=0 b=0 (mod zero), DU a='' b=''
# 530: PY a=10 b='', DU a='' b=''
# 548: PY p=0 s='', DU p=0 s=''
# 549: PY p=0 s='', DU p=0 s=''
# 552: PY s=[], DU s=[]
# 560: PY temp='', DU temp=0
# 562-573: PY str op str, DU str op str
# 639, 640, 641: PY int zip, DU int zip
# 685, 686, 687: PY int mock, DU complex
# 707: PY s=0 (datetime.strptime), DU s=0
# 715, 716: PY f not defined
# 718: PY queue module issues
# 1246, 1247: PY results not defined, DU async issues

# These entries have fundamental PY/DU mismatches - remove them
fundamentally_broken = {
    495, 506, 507, 509, 518, 519, 524, 529, 530,
    548, 549, 552, 560, 562, 563, 564, 565, 566, 567,
    568, 569, 570, 572, 573,
    639, 640, 641,
    685, 686, 687, 707, 715, 716, 718,
    1246, 1247
}
remove_indices.update(fundamentally_broken)
print(f"  Marked {len(fundamentally_broken)} fundamentally broken PY entries for removal")

# ============================================================
# Fix DU exec fails
# These are entries where PY passes but DU fails
# ============================================================

# 19: DU 'dict' has no attribute 'delete' - DU uses d.delete("key") instead of del
item = items[19]
du = item['output']
# Fix DU: change d.delete("key") to use del
du = du.replace('d.delete("key")', '删除 d["key"]')
item['output'] = du
fix_count += 1
print(f"  [19] fixed DU dict.delete -> del")

# 216, 217, 308: DU raise exceptions - need to wrap in try/except too
for idx in [216, 217, 308]:
    item = items[idx]
    du = item['output']
    py = item['input']
    # The PY was already wrapped in try/except. Update DU to match.
    if 'try:' in py:
        if '尝试' not in du:
            if idx == 216:
                du = '尝试：\n    抛出 Exception("invalid")\n捕获 Exception：\n    打印("invalid")\n'
            elif idx == 217:
                du = '尝试：\n    抛出 Exception("error")\n捕获 Exception：\n    打印("error")\n'
            elif idx == 308:
                du = '尝试：\n    抛出 Exception()\n捕获 Exception：\n    跳过\n'
            item['output'] = du
            fix_count += 1
            print(f"  [{idx}] fixed DU raise exception")

# 242: DU integer modulo by zero
item = items[242]
du = item['output']
# DU has a=0 b=0, need to fix to match PY (a=10 b=3)
du = du.replace('设 a 为 0', '设 a 为 10')
du = du.replace('设 b 为 0', '设 b 为 3')
item['output'] = du
fix_count += 1
print(f"  [242] fixed DU modulo by zero")

# 498: DU division by zero
item = items[498]
du = item['output']
# DU should have nums initialized
du = du.replace('设 nums 为 []', '设 nums 为 [10, 20, 30]')
item['output'] = du
fix_count += 1
print(f"  [498] fixed DU division by zero")

# 503: DU str/str division
item = items[503]
du = item['output']
du = du.replace("设 done 为 ''", '设 done 为 3')
du = du.replace("设 total 为 ''", '设 total 为 10')
item['output'] = du
fix_count += 1
print(f"  [503] fixed DU str/str")

# 515: DU max() empty
item = items[515]
du = item['output']
du = du.replace('设 values 为 []', '设 values 为 [1, 5, 3]')
item['output'] = du
fix_count += 1
print(f"  [515] fixed DU empty max")

# 516: DU list index out of range
item = items[516]
du = item['output']
du = du.replace('设 items 为 []', '设 items 为 [10, 20, 30]')
item['output'] = du
fix_count += 1
print(f"  [516] fixed DU index out of range")

# 521, 522: DU str ** int
for idx in [521, 522]:
    item = items[idx]
    du = item['output']
    du = du.replace("设 x 为 ''", '设 x 为 5')
    item['output'] = du
    fix_count += 1
    print(f"  [{idx}] fixed DU str**int")

# 528: DU str/str
item = items[528]
du = item['output']
du = du.replace("设 a 为 ''", '设 a 为 10')
du = du.replace("设 b 为 ''", '设 b 为 3')
item['output'] = du
fix_count += 1
print(f"  [528] fixed DU str/str")

# 531: DU format string
item = items[531]
du = item['output']
du = du.replace('%s', '%d')
item['output'] = du
fix_count += 1
print(f"  [531] fixed DU format string")

# 537: DU 'NoneType' not callable
item = items[537]
du = item['output']
# Replace lambda with function that returns proper value
# This is complex - let's remove it
remove_indices.add(537)
print(f"  [537] marked for removal (complex DU issue)")

# 547: DU find() int arg
item = items[547]
du = item['output']
du = du.replace('设 c 为 0', "设 c 为 'a'")
du = du.replace("设 s 为 ''", "设 s 为 'abc'")
item['output'] = du
fix_count += 1
print(f"  [547] fixed DU find int arg")

# 553: DU 'NoneType' not callable
item = items[553]
du = item['output']
# This is complex - remove
remove_indices.add(553)
print(f"  [553] marked for removal (complex DU issue)")

# 571: DU bad operand for ~str
item = items[571]
du = item['output']
du = du.replace("设 x 为 ''", '设 x 为 5')
item['output'] = du
fix_count += 1
print(f"  [571] fixed DU ~str")

# 649, 889: DU No module named 'sub'
for idx in [649, 889]:
    item = items[idx]
    du = item['output']
    # Fix import statement
    du = du.replace('导入 sub', '导入 re')
    item['output'] = du
    fix_count += 1
    print(f"  [{idx}] fixed DU import sub->re")

# 675: DU invalid syntax
remove_indices.add(675)
print(f"  [675] marked for removal (DU syntax error)")

# 681: DU 'NoneType' has no attribute 'release'
remove_indices.add(681)
print(f"  [681] marked for removal (complex DU issue)")

# 699: DU catching non-exception
remove_indices.add(699)
print(f"  [699] marked for removal (DU catch issue)")

# 710: DU 'function' has no attribute 'signal'
remove_indices.add(710)
print(f"  [710] marked for removal (complex DU issue)")

# 728: DU name 'deleted' not defined
remove_indices.add(728)
print(f"  [728] marked for removal (DU undefined var)")

# 736: DU str cannot be interpreted as int
remove_indices.add(736)
print(f"  [736] marked for removal (DU str/int issue)")

# 737: DU pop expected at most 1 arg
remove_indices.add(737)
print(f"  [737] marked for removal (DU pop issue)")

# 740: DU int not a mapping
remove_indices.add(740)
print(f"  [740] marked for removal (DU mapping issue)")

# 819-828: DU int not iterable (filter/map/reduce with int data)
# These are entries where PY was fixed to use list but DU still has int
for idx in range(819, 829):
    if idx < len(items):
        item = items[idx]
        du = item['output']
        du = du.replace('设 data 为 0', '设 data 为 [1, 2, 3, 4, 5]')
        du = du.replace('设 data 为 空', '设 data 为 [1, 2, 3, 4, 5]')
        item['output'] = du
        fix_count += 1
        print(f"  [{idx}] fixed DU int not iterable")

# 836: DU bytes-like required
remove_indices.add(836)
print(f"  [836] marked for removal (DU bytes issue)")

# 927: DU name 'count' not defined
remove_indices.add(927)
print(f"  [927] marked for removal (DU undefined var)")

# 1139: DU division by zero
remove_indices.add(1139)
print(f"  [1139] marked for removal (DU div zero)")

# 1141: DU 'NoneType' not callable
remove_indices.add(1141)
print(f"  [1141] marked for removal (DU NoneType)")

# 1217: DU int has no attribute 'search'
remove_indices.add(1217)
print(f"  [1217] marked for removal (DU int.search)")

# ============================================================
# Fix parse failures
# ============================================================
# 720: DU has '导入 "sub"' - invalid
remove_indices.add(720)
print(f"  [720] marked for removal (DU parse error)")

# 742: DU has '段落 from["a", "b"]' - invalid
remove_indices.add(742)
print(f"  [742] marked for removal (DU parse error)")

# ============================================================
# Fix mismatches
# ============================================================
# 505: PY Date: 2024-00-15, DU Date: -00-00
remove_indices.add(505)
print(f"  [505] marked for removal (mismatch)")

# 555: PY Formatted: 1,234.56, DU Formatted: 0.00
remove_indices.add(555)
print(f"  [555] marked for removal (mismatch)")

# 561: PY Random: 34, DU Random: 80 (random values differ)
# Both use random, so outputs will differ. Remove.
remove_indices.add(561)
print(f"  [561] marked for removal (random mismatch)")

# 708: PY Command not found, DU empty
remove_indices.add(708)
print(f"  [708] marked for removal (mismatch)")

# 1004: PY Whiskers says meow, DU empty
remove_indices.add(1004)
print(f"  [1004] marked for removal (mismatch)")

# ============================================================
# Remove marked entries
# ============================================================
if remove_indices:
    new_items = [item for i, item in enumerate(items) if i not in remove_indices]
    removed = len(items) - len(new_items)
    print(f"\nRemoved {removed} entries")
    items = new_items

with open(DATASET_PATH, 'w', encoding='utf-8') as f:
    for item in items:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"\nTotal fixes applied: {fix_count}")
print(f"Remaining entries: {len(items)}")
print(f"Saved to {DATASET_PATH}")