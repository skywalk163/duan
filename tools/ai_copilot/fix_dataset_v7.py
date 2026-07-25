#!/usr/bin/env python3
"""
v7 修复脚本: 修复 41 条错误数据
- 28 条 ** 幂运算错误 (乘以x -> 幂N)
- 5 条 负数错误 (减去1 -> -1, len(lst)减去1 -> lst[-1])
- 8 条 类名翻译为中文
"""
import json
import copy

DATASET = 'sft_dataset.jsonl'

with open(DATASET, 'r', encoding='utf-8') as f:
    samples = [json.loads(line) for line in f]

print(f"修复前样本数: {len(samples)}")

fixes_applied = 0

# ============================================================
# 1. 修复 ** 幂运算错误 (28条)
# ============================================================
# Pattern: Python has x**N, output incorrectly uses "x 乘以 x" (N times)
# Fix: replace with "x 幂 N"

power_fixes = {
    # Circle area: self.radius ** 2 -> 3.14159 * (己.radius 幂 2)
    464: '''类 Circle：
    属性 radius
    构造 接收 radius：
        己.radius 为 radius
    段落 area：
        返回 3.14159 乘以 (己.radius 幂 2)
    段落 circumference：
        返回 2 乘以 3.14159 乘以 己.radius''',

    469: '''类 Shape：
    段落 area：
        返回 0

类 Circle 继承 Shape：
    属性 radius
    构造 接收 r：
        己.radius 为 r
    段落 area：
        返回 3.14159 乘以 (己.radius 幂 2)''',

    # List comprehensions with **
    597: '设 squares 为 [x 幂 2 遍历 x 之 0至9]',
    615: '设 odd_squares 为 [x 幂 2 遍历 x 之 0至19 若 x 取余 2 不等于 0]',
    616: '设 even_cubes 为 [x 幂 3 遍历 x 之 0至9 若 x 取余 2 等于 0]',
    621: '设 squared_evens 为 [x 幂 2 遍历 x 之 nums 若 x 取余 2 等于 0]',
    622: '设 cubed_odds 为 [x 幂 3 遍历 x 之 nums 若 x 取余 2 不等于 0]',

    # Dict unpacking: {**d1, **d2} - this is dict merge, not power
    # Keep as-is since ** in dict context is unpacking, not power
    # 773: '设 merged 为 {**d1, **d2}' -> this is actually correct!

    # Dict comprehension with **
    778: '设 d 为 {i: i 幂 2 遍历 i 之 0至9}',

    # Lambda with **
    815: '设 f 为 接收 x：返回 x 幂 2',
    816: '设 f 为 接收 x：返回 x 幂 3',

    # Map with lambda **
    856: '设 result 为 映射(接收 x：返回 x 幂 2, data)',

    # Variance: (x - m) ** 2
    912: '''段落 variance 接收 numbers：
    设 m 为 mean(numbers)
    返回 sum((x 减去 m) 幂 2 遍历 x 之 numbers) 除以 len(numbers)''',

    # Decorators with ** in wrapper signatures - these use *args/**kwargs
    # The ** in *args/**kwargs is NOT power, it's dict unpacking
    # These are actually CORRECT - skip them
    # 918, 919, 920, 943, 1124, 1125, 1126, 1127 - skip

    # Shape class with area
    949: '''类 Shape：
    属性 color
    构造 接收 color 等于 "black"：
        己.color 为 color
    段落 area：
        返回 0
    段落 describe：
        返回 f"{type(己).__name__} (color={己.color})"''',

    # Animal class
    954: '''类 Animal：
    属性 name
    属性 sound
    构造 接收 name, sound：
        己.name 为 name
        己.sound 为 sound
    段落 speak：
        返回 f"{己.name} says {己.sound}"''',

    # Timer decorator
    1119: '''段落 timer 接收 func：
    段落 wrapper 接收 *args, **kwargs：
        设 result 为 func(*args, **kwargs)
        返回 result
    返回 wrapper

@timer 标注
段落 slow_function：
    设 x 为 0
    遍历 i 于 0至100：
        x 加上 i
    返回 x''',

    # Log call decorator
    1120: '''段落 log_call 接收 func：
    段落 wrapper 接收 *args, **kwargs：
        打印(f"Calling {func.__name__}")
        返回 func(*args, **kwargs)
    返回 wrapper

@log_call 标注
段落 greet 接收 name：
    返回 f"Hello, {name}"''',

    # Repeat decorator
    1121: '''段落 repeat 接收 n：
    段落 decorator 接收 func：
        段落 wrapper 接收 *args, **kwargs：
            遍历 i 于 0至n 减去 1：
                设 result 为 func(*args, **kwargs)
            返回 result
        返回 wrapper
    返回 decorator

@repeat(3) 标注
段落 say_hi：
    打印("Hi!")''',

    # Memoize
    1124: '''段落 memoize 接收 func：
    设 cache 为 {}
    段落 wrapper 接收 *args：
        如果 args 不在 cache：
            设 cache[args] 为 func(*args)
        返回 cache[args]
    返回 wrapper''',

    # Retry decorator
    1125: '''段落 retry 接收 max_attempts：
    段落 decorator 接收 func：
        段落 wrapper 接收 *args, **kwargs：
            遍历 attempt 于 0至max_attempts 减去 1：
                尝试：
                    返回 func(*args, **kwargs)
                捕获 Exception 为 e：
                    如果 attempt 等于 max_attempts 减去 1：
                        抛出 e
        返回 wrapper
    返回 decorator''',

    # Uppercase result decorator
    1126: '''段落 uppercase_result 接收 func：
    段落 wrapper 接收 *args, **kwargs：
        设 result 为 func(*args, **kwargs)
        返回 result.upper()
    返回 wrapper

@uppercase_result 标注
段落 get_name：
    返回 "hello world"''',

    # Count calls decorator
    1127: '''段落 count_calls 接收 func：
    段落 wrapper 接收 *args, **kwargs：
        设 wrapper.count 为 wrapper.count 加上 1
        返回 func(*args, **kwargs)
    设 wrapper.count 为 0
    返回 wrapper''',

    # Lambda square
    1138: '''设 square 为 接收 x：返回 x 幂 2
打印(square(5))''',

    # Map with lambda
    1140: '''设 squares 为 list(映射(接收 x：返回 x 幂 2, range(5)))
打印(squares)''',
}

# ============================================================
# 2. 修复负数错误 (5条)
# ============================================================

neg_fixes = {
    # index = -1 -> 设 index 为 -1 (not 减去 1)
    692: '''尝试：
    设 index 为 list.index(item)
捕获 ValueError：
    设 index 为 -1''',

    753: '''尝试：
    设 index 为 string.index(sub)
捕获 ValueError：
    设 index 为 -1''',

    # lst[-1] -> lst[-1] (not len(lst) 减去 1)
    98: '''设 first 为 list_[0]
设 last 为 list_[-1]''',

    204: '''设 first 为 lst[0]
设 last 为 lst[-1]''',

    214: '''设 first 为 lst[0]
设 last 为 lst[-1]''',
}

# ============================================================
# 3. 修复类名翻译为中文 (8条)
# ============================================================

class_fixes = {
    457: '''类 Rectangle：
    属性 width
    属性 height
    构造 接收 w, h：
        己.width 为 w
        己.height 为 h
    段落 area：
        返回 己.width 乘以 己.height
    段落 perimeter：
        返回 2 乘以 (己.width 加上 己.height)''',

    502: '''类 UniqueList：
    属性 data
    构造：
        己.data 为 []
    段落 add 接收 item：
        如果 item 不在 己.data：
            己.data.append(item)
    段落 contains 接收 item：
        返回 item 在 己.data''',

    505: '''类 Database：
    属性 tables
    构造：
        己.tables 为 {}
    段落 create_table 接收 name, columns：
        己.tables[name] 为 {col: [] 遍历 col 之 columns}
    段落 drop_table 接收 name：
        如果 name 在 己.tables：
            删除 己.tables[name]''',

    509: '''类 Playlist：
    属性 name
    属性 songs
    构造 接收 name：
        己.name 为 name
        己.songs 为 []
    段落 add_song 接收 title, artist：
        己.songs.append({"title": title, "artist": artist})
    段落 count：
        返回 len(己.songs)''',

    924: '''类 CSVWriter：
    属性 filename
    属性 rows
    构造 接收 filename：
        己.filename 为 filename
        己.rows 为 []
    段落 write_header 接收 headers：
        己.rows.append(headers)
    段落 write_row 接收 row：
        己.rows.append(row)''',

    925: '''类 JSONStore：
    属性 filename
    属性 data
    构造 接收 filename：
        己.filename 为 filename
        己.data 为 {}
    段落 load：
        设 text 为 读取文件(己.filename)
        己.data 为 解析JSON(text)
    段落 get 接收 key：
        如果 key 在 己.data：
            返回 己.data[key]
        否则：
            返回 空''',

    928: '''类 NumberSeries：
    属性 current
    属性 step
    构造 接收 start, step：
        己.current 为 start
        己.step 为 step
    段落 next：
        设 result 为 己.current
        己.current 加上 己.step
        返回 result''',

    952: '''类 Subject：
    属性 observers
    属性 state
    构造：
        己.observers 为 []
        己.state 为 空
    段落 attach 接收 observer：
        己.observers.append(observer)
    段落 detach 接收 observer：
        己.observers.remove(observer)
    段落 notify：
        遍历 observer 于 己.observers：
            observer.update(己.state)''',
}

# ============================================================
# Apply all fixes
# ============================================================

all_fixes = {}
all_fixes.update(power_fixes)
all_fixes.update(neg_fixes)
all_fixes.update(class_fixes)

# Remove 773 from fixes (dict unpacking {**d1, **d2} is correct as-is)
if 773 in all_fixes:
    del all_fixes[773]

# Remove decorator samples where ** is in *args/**kwargs (not power operator)
# These are correct as-is: 918, 919, 920, 943
for idx in [918, 919, 920, 943]:
    if idx in all_fixes:
        del all_fixes[idx]

print(f"\n待修复样本数: {len(all_fixes)}")

for idx, new_output in all_fixes.items():
    old_output = samples[idx]['output']
    samples[idx]['output'] = new_output.strip()
    fixes_applied += 1
    print(f"  [{idx}] fixed ({samples[idx].get('category', '')})")

print(f"\n总修复: {fixes_applied} 条")

# Save
with open(DATASET, 'w', encoding='utf-8') as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + '\n')

print(f"已保存到 {DATASET}")
