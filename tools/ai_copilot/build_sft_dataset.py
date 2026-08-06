"""
段言 SFT 训练集构造器 v9（v5.0.0 升级版）

为 ERNIE-4.5-0.3B 微调生成 Python→段言 翻译对照数据。
输出 JSONL 格式，符合 ERNIEKit SFT 规范。

数据来源：
  1. 手工编写的高质量 v5.0 对照对（核心，按语法类别系统覆盖）
  2. 从 examples/ 目录 .duan 文件提取（需标注是否旧语法）
  3. 变体扩充：对每条基础对照对做等价变换，扩充训练规模
  4. 长样本补充：50+ 条超过 200 token 的长样本

注意：
  段言 v5.0 使用 v3.2 新语法（SRC 后端），包含 Trait/协议系统、模式匹配、
  迭代器协议、上下文管理器、异常映射等新特性。

用法：
    python build_sft_dataset.py          # 生成训练集到 sft_dataset.jsonl
    python build_sft_dataset.py --stats  # 只显示统计信息
    python build_sft_dataset.py --audit  # 运行数据质量审计
"""

import json
import os
import random
import re
import sys
from typing import List, Dict, Tuple

# ── 路径 ──
_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ═══════════════════════════════════════════════════════════════════
# 手工对照对：Python → 段言 v3.2（新语法/SRC后端）
# 每条 = (category, python_code, duan_code)
# ═══════════════════════════════════════════════════════════════════

_HANDCRAFTED: List[tuple] = [
    # ── 变量与赋值 ────────────────────────────────────────────────
    ("变量", "x = 10", "设 x 为 10"),
    ("变量", "name = 'hello'", "设 name 为 \"hello\""),
    ("变量", "lst = [1, 2, 3]", "设 lst 为 [1, 2, 3]"),
    ("变量", "x = 5\ny = 3", "设 x 为 5\n设 y 为 3"),
    ("变量", "flag = True", "设 flag 为 真"),
    ("变量", "empty = None", "设 empty 为 空"),
    ("变量", "pi = 3.14", "设 pi 为 3.14"),
    ("变量", "x = 10\nx = x + 1", "设 x 为 10\n设 x 为 x 加上 1"),
    ("变量", "count = 0\ncount += 1", "设 count 为 0\n设 count 为 count 加上 1"),
    ("变量", "total = 100\ntotal -= 20", "设 total 为 100\n设 total 为 total 减去 20"),
    ("变量", "n = 5\nn *= 3", "设 n 为 5\n设 n 为 n 乘以 3"),
    ("变量", "d = 10\nd /= 2", "设 d 为 10\n设 d 为 d 除以 2"),
    ("变量", 's = "world"', "设 s 为 \"world\""),
    ("变量", "nums = []", "设 nums 为 []"),
    ("变量", "pairs = {}", "设 pairs 为 {}"),

    # ── 段落（函数）─────────────────────────────────────────────
    ("段落", "def add(a, b):\n    return a + b", "段落 加法 接收 a, b：\n    返回 a 加上 b"),
    ("段落", "def greet():\n    print('hello')", "段落 打招呼：\n    打印(\"hello\")"),
    ("段落", "def square(n):\n    return n * n", "段落 平方 接收 n：\n    返回 n 乘以 n"),
    ("段落", "def is_positive(n):\n    return n > 0", "段落 是正数 接收 n：\n    返回 n 大于 0"),
    ("段落", "def max_of_two(a, b):\n    if a >= b:\n        return a\n    return b", "段落 最大值 接收 a, b：\n    如果 a 大于等于 b：\n        返回 a\n    返回 b"),
    ("段落", "def abs_val(n):\n    if n < 0:\n        return -n\n    return n", "段落 绝对值 接收 n：\n    如果 n 小于 0：\n        返回 0 减去 n\n    返回 n"),
    ("段落", "def fib(n):\n    if n <= 2:\n        return 1\n    return fib(n-1) + fib(n-2)", "段落 斐波那契 接收 n：\n    如果 n 小于等于 2：\n        返回 1\n    返回 斐波那契(n 减去 1) 加上 斐波那契(n 减去 2)"),
    ("段落", "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "段落 阶乘 接收 n：\n    如果 n 小于等于 1：\n        返回 1\n    返回 n 乘以 阶乘(n 减去 1)"),
    ("段落", "def area(width, height):\n    return width * height", "段落 面积 接收 宽, 高：\n    返回 宽 乘以 高"),
    ("段落", "def celsius_to_fahrenheit(c):\n    return c * 9 / 5 + 32", "段落 摄氏转华氏 接收 c：\n    返回 c 乘以 9 除以 5 加上 32"),
    ("段落", "def greet_name(name):\n    print('Hello, ' + name)",
     "段落 打招呼 接收 name：\n    打印(\"Hello, \" 加上 name)"),
    ("段落", "def count_down(n):\n    while n > 0:\n        print(n)\n        n -= 1", "段落 倒计时 接收 n：\n    当 n 大于 0：\n        打印(n)\n        设 n 为 n 减去 1"),

    
    # ── 复合赋值 (补充) ──
    ("复合", "x = 100\\nx %= 7", "设 x 为 100\\n设 x 为 x 取余 7"),
    ("复合", "a = 5\\na ^= 3", "设 a 为 5\\n设 a 为 a 异或 3"),
    ("复合", "x = 16\\nx >>= 2", "设 x 为 16\\n设 x 为 x 右移 2"),
    ("复合", "x = 1\\nx <<= 3", "设 x 为 1\\n设 x 为 x 左移 3"),
    ("复合", "n = 50\\nn //= 6", "设 n 为 50\\n设 n 为 n 整除 6"),
    # ── for…else 补充 ──
    ("for…else", "for i in range(5):\\n    if i == 3:\\n        break\\nelse:\\n    print('no break')",
     "遍历 i 于 0至4：\\n    如果 i 等于 3：\\n        跳出\\n否则：\\n    打印('no break')"),

# ── 条件 ──────────────────────────────────────────────────────
    ("条件", "if x > 0:\n    print('positive')", "如果 x 大于 0：\n    打印(\"positive\")"),
    ("条件", "if x > 0:\n    print('yes')\nelse:\n    print('no')",
     "如果 x 大于 0：\n    打印(\"yes\")\n否则：\n    打印(\"no\")"),
    ("条件", "if score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelse:\n    grade = 'C'",
     "如果 score 大于等于 90：\n    设 grade 为 \"A\"\n否则如果 score 大于等于 80：\n    设 grade 为 \"B\"\n否则：\n    设 grade 为 \"C\""),
    ("条件", "if x == 0:\n    print('zero')", "如果 x 等于 0：\n    打印(\"zero\")"),
    ("条件", "if x != 0:\n    print('not zero')", "如果 x 不等于 0：\n    打印(\"not zero\")"),
    ("条件", "if a and b:\n    print('both')", "如果 a 且 b：\n    打印(\"both\")"),
    ("条件", "if a or b:\n    print('either')", "如果 a 或 b：\n    打印(\"either\")"),
    ("条件", "if not flag:\n    print('off')", "如果 非 flag：\n    打印(\"off\")"),
    ("条件", "if x > 0 and x < 10:\n    print('in range')",
     "如果 x 大于 0 且 x 小于 10：\n    打印(\"in range\")"),
    ("条件", "if x <= 0:\n    print('non-positive')\nelse:\n    print('positive')",
     "如果 x 小于等于 0：\n    打印(\"non-positive\")\n否则：\n    打印(\"positive\")"),
    ("条件", "if n % 2 == 0:\n    print('even')\nelse:\n    print('odd')",
     "如果 n 取余 2 等于 0：\n    打印(\"even\")\n否则：\n    打印(\"odd\")"),

    # ── 循环 ──────────────────────────────────────────────────────
    ("循环", "while x > 0:\n    x -= 1", "当 x 大于 0：\n    设 x 为 x 减去 1"),
    ("循环", "while True:\n    if x == 0:\n        break\n    x -= 1", "当 真：\n    如果 x 等于 0：\n        跳出\n    设 x 为 x 减去 1"),
    ("循环", "for i in range(10):\n    print(i)", "遍历 i 于 0至9：\n    打印(i)"),
    ("循环", "for i in range(1, 11):\n    print(i)", "遍历 i 于 1至10：\n    打印(i)"),
    ("循环", "for i in range(0, 10, 2):\n    print(i)", "遍历 i 于 0至9步2：\n    打印(i)"),
    ("循环", "for item in lst:\n    print(item)", "遍历 item 于 lst：\n    打印(item)"),
    ("循环", "for i in range(len(lst)):\n    print(lst[i])", "遍历 i 于 0至len(lst)减去1：\n    打印(lst[i])"),
    ("循环", "i = 0\nwhile i < 10:\n    print(i)\n    i += 1", "设 i 为 0\n当 i 小于 10：\n    打印(i)\n    设 i 为 i 加上 1"),
    ("循环", "total = 0\nfor n in numbers:\n    total += n", "设 total 为 0\n遍历 n 于 numbers：\n    设 total 为 total 加上 n"),
    ("循环", "for i in range(5):\n    if i == 3:\n        continue\n    print(i)", "遍历 i 于 0至4：\n    如果 i 等于 3：\n        跳过\n    打印(i)"),
    ("循环", "found = False\nfor item in lst:\n    if item == target:\n        found = True\n        break", "设 found 为 假\n遍历 item 于 lst：\n    如果 item 等于 target：\n        设 found 为 真\n        跳出"),

    # ── 列表操作 ──────────────────────────────────────────────────
    ("列表", "lst.append(10)", "lst.追加(10)"),
    ("列表", "x = lst[0]", "设 x 为 lst[0]"),
    ("列表", "lst[0] = 10", "lst[0] = 10"),
    ("列表", "n = len(lst)", "设 n 为 len(lst)"),
    ("列表", "result = [x for x in lst if x > 0]", "设 result 为 []\n遍历 x 于 lst：\n    如果 x 大于 0：\n        result.追加(x)"),
    ("列表", "total = sum(lst)", "设 total 为 0\n遍历 x 于 lst：\n    设 total 为 total 加上 x"),
    ("列表", "lst.sort()", "设 n 为 len(lst)\n遍历 i 于 0至n减去2：\n    遍历 j 于 0至n减去i减去2：\n        如果 lst[j] 大于 lst[j 加上 1]：\n            设 tmp 为 lst[j]\n            lst[j] = lst[j 加上 1]\n            lst[j 加上 1] = tmp"),
    ("列表", "lst.reverse()", "设 n 为 len(lst)\n设 i 为 0\n设 j 为 n 减去 1\n当 i 小于 j：\n    设 tmp 为 lst[i]\n    lst[i] = lst[j]\n    lst[j] = tmp\n    设 i 为 i 加上 1\n    设 j 为 j 减去 1"),
    ("列表", "if 5 in lst:\n    print('found')",
     "设 found 为 假\n遍历 x 于 lst：\n    如果 x 等于 5：\n        设 found 为 真\n        跳出\n如果 found：\n    打印(\"found\")"),
    ("列表", "new_lst = lst[1:3]", "设 new_lst 为 []\n设 i 为 1\n当 i 小于 3：\n    new_lst.追加(lst[i])\n    设 i 为 i 加上 1"),
    ("列表", "count = lst.count(5)", "设 count 为 0\n遍历 x 于 lst：\n    如果 x 等于 5：\n        设 count 为 count 加上 1"),

    # ── 字符串 ────────────────────────────────────────────────────
    ("字符串", "s = 'hello' + ' world'", "设 s 为 \"hello\" 加上 \" world\""),
    ("字符串", "n = len(s)", "设 n 为 len(s)"),
    ("字符串", "upper_s = s.upper()", "设 upper_s 为 字符串转大写(s)"),
    ("字符串", "if 'hello' in s:\n    print('found')",
     "如果 字符串包含(s, \"hello\")：\n    打印(\"found\")"),
    ("字符串", "parts = s.split(',')",
     "设 parts 为 字符串分割(s, \",\")"),
    ("字符串", "result = s.replace('old', 'new')",
     "设 result 为 字符串替换(s, \"old\", \"new\")"),
    ("字符串", "idx = s.find('abc')",
     "设 idx 为 字符串查找(s, \"abc\")"),
    ("字符串", "print(f'{name} is {age} years old')",
     "打印(f\"{name} is {age} years old\")"),

    # ── 字典 ──────────────────────────────────────────────────────
    ("字典", "d = {'a': 1, 'b': 2}", "设 d 为 {\"a\": 1, \"b\": 2}"),
    ("字典", "d['key'] = 10", "d[\"key\"] = 10"),
    ("字典", "val = d.get('key', 0)", "设 val 为 d.get(\"key\", 0)"),
    ("字典", "if 'key' in d:\n    print(d['key'])",
     "如果 \"key\" 于 d：\n    打印(d[\"key\"])"),
    ("字典", "for k, v in d.items():\n    print(k, v)", "遍历 k 于 d：\n    打印(k)\n    打印(d[k])"),

    # ── 异常 ──────────────────────────────────────────────────────
    ("异常", "try:\n    x = int(s)\nexcept:\n    x = 0", "尝试：\n    设 x 为 int(s)\n捕获 异常：\n    设 x 为 0"),
    ("异常", "try:\n    f = open('data.txt')\nexcept FileNotFoundError:\n    print('file not found')",
     "尝试：\n    设 f 为 读取文件(\"data.txt\")\n捕获 异常：\n    打印(\"file not found\")"),
    ("异常", "raise ValueError('invalid')",
     "抛出 异常(\"invalid\")"),

    # ── 导入 ──────────────────────────────────────────────────────
    ("导入", "import math", "导入 数学工具"),
    ("导入", "from math import sqrt", "从 数学工具 导入 平方"),
    ("导入", "from collections import Counter", "从 集合操作 导入 计数"),

    # ── 类（需 LLVM 后端）────────────────────────────────────────
    ("类", "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        print(f'{self.name}: woof!')",
     "类 狗：\n    属性 名字\n    构造 接收 名字：\n        己.名字 为 名字\n    段落 说话：\n        打印(f\"{己.名字}: woof!\")"),
    ("类", "class Cat(Dog):\n    def speak(self):\n        print(f'{self.name}: meow!')",
     "类 猫 继承 狗：\n    段落 说话：\n        打印(f\"{己.名字}: meow!\")"),
    ("类", "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def distance(self):\n        return (self.x**2 + self.y**2)**0.5", "类 点：\n    属性 x\n    属性 y\n    构造 接收 x, y：\n        己.x 为 x\n        己.y 为 y\n    段落 距离：\n        返回 (己.x 乘以 己.x 加上 己.y 乘以 己.y) 的 0.5 次方"),
    ("类", "obj = Dog('Rex')\nobj.speak()",
     "设 obj 为 新建 狗(\"Rex\")\nobj.说话()"),

    # ── 复合示例（多语法混用）────────────────────────────────────
    ("复合", "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1", "段落 二分查找 接收 arr, target：\n    设 low 为 0\n    设 high 为 len(arr) 减去 1\n    当 low 小于等于 high：\n        设 mid 为 (low 加上 high) 除以 2\n        如果 arr[mid] 等于 target：\n            返回 mid\n        否则如果 arr[mid] 小于 target：\n            设 low 为 mid 加上 1\n        否则：\n            设 high 为 mid 减去 1\n    返回 -1"),
    ("复合", "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True", "段落 是素数 接收 n：\n    如果 n 小于 2：\n        返回 假\n    设 limit 为 int(n 的 0.5 次方) 加上 1\n    遍历 i 于 2至limit减去1：\n        如果 n 取余 i 等于 0：\n            返回 假\n    返回 真"),
    ("复合", "def fizzbuzz(n):\n    for i in range(1, n+1):\n        if i % 15 == 0:\n            print('FizzBuzz')\n        elif i % 3 == 0:\n            print('Fizz')\n        elif i % 5 == 0:\n            print('Buzz')\n        else:\n            print(i)",
     "段落 FizzBuzz 接收 n：\n    遍历 i 于 1至n：\n        如果 i 取余 15 等于 0：\n            打印(\"FizzBuzz\")\n        否则如果 i 取余 3 等于 0：\n            打印(\"Fizz\")\n        否则如果 i 取余 5 等于 0：\n            打印(\"Buzz\")\n        否则：\n            打印(i)"),
    ("复合", "def count_words(text):\n    words = text.split()\n    counts = {}\n    for w in words:\n        if w in counts:\n            counts[w] += 1\n        else:\n            counts[w] = 1\n    return counts", "段落 统计词频 接收 text：\n    设 words 为 字符串分割(text)\n    设 counts 为 {}\n    遍历 w 于 words：\n        如果 w 于 counts：\n            counts[w] = counts[w] 加上 1\n        否则：\n            counts[w] = 1\n    返回 counts"),
    ("复合", "def gcd(a, b):\n    while b != 0:\n        a, b = b, a % b\n    return a", "段落 最大公约数 接收 a, b：\n    当 b 不等于 0：\n        设 tmp 为 a 取余 b\n        设 a 为 b\n        设 b 为 tmp\n    返回 a"),
    ("复合", "def power(base, exp):\n    result = 1\n    for _ in range(exp):\n        result *= base\n    return result", "段落 幂运算 接收 base, exp：\n    设 result 为 1\n    遍历 _ 于 0至exp减去1：\n        设 result 为 result 乘以 base\n    返回 result"),
    ("复合", "def reverse_string(s):\n    result = ''\n    for i in range(len(s)-1, -1, -1):\n        result += s[i]\n    return result",
     "段落 反转字符串 接收 s：\n    设 result 为 \"\"\n    设 i 为 len(s) 减去 1\n    当 i 大于等于 0：\n        设 result 为 result 加上 s[i]\n        设 i 为 i 减去 1\n    返回 result"),
    ("复合", "def find_max(lst):\n    max_val = lst[0]\n    for item in lst[1:]:\n        if item > max_val:\n            max_val = item\n    return max_val", "段落 求最大值 接收 lst：\n    设 max_val 为 lst[0]\n    遍历 item 于 lst：\n        如果 item 大于 max_val：\n            设 max_val 为 item\n    返回 max_val"),
    ("复合", "def remove_duplicates(lst):\n    seen = []\n    result = []\n    for item in lst:\n        if item not in seen:\n            seen.append(item)\n            result.append(item)\n    return result", "段落 去重 接收 lst：\n    设 seen 为 []\n    设 result 为 []\n    遍历 item 于 lst：\n        设 found 为 假\n        遍历 s 于 seen：\n            如果 s 等于 item：\n                设 found 为 真\n                跳出\n        如果 非 found：\n            seen.追加(item)\n            result.追加(item)\n    返回 result"),
    ("复合", "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr", "段落 冒泡排序 接收 arr：\n    设 n 为 len(arr)\n    遍历 i 于 0至n减去1：\n        遍历 j 于 0至n减去i减去2：\n            如果 arr[j] 大于 arr[j 加上 1]：\n                设 tmp 为 arr[j]\n                arr[j] = arr[j 加上 1]\n                arr[j 加上 1] = tmp\n    返回 arr"),
    ("复合", "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr", "段落 选择排序 接收 arr：\n    设 n 为 len(arr)\n    遍历 i 于 0至n减去1：\n        设 min_idx 为 i\n        遍历 j 于 i加上1至n减去1：\n            如果 arr[j] 小于 arr[min_idx]：\n                设 min_idx 为 j\n        设 tmp 为 arr[i]\n        arr[i] = arr[min_idx]\n        arr[min_idx] = tmp\n    返回 arr"),

    # ── 补充：更多变量变体 ───────────────────────────────────────
    ("变量", "a = 1\nb = 2\nc = a + b", "设 a 为 1\n设 b 为 2\n设 c 为 a 加上 b"),
    ("变量", "width = 10\nheight = 5", "设 width 为 10\n设 height 为 5"),
    ("变量", "msg = 'ok'", "设 msg 为 \"ok\""),
    ("变量", "items = [10, 20, 30]", "设 items 为 [10, 20, 30]"),
    ("变量", "active = False", "设 active 为 假"),
    ("变量", "data = None", "设 data 为 空"),
    ("变量", "ratio = 2.5", "设 ratio 为 2.5"),
    ("变量", "x = 100\nx += 5", "设 x 为 100\n设 x 为 x 加上 5"),
    ("变量", "y = 50\ny -= 10", "设 y 为 50\n设 y 为 y 减去 10"),
    ("变量", "z = 3\nz *= 4", "设 z 为 3\n设 z 为 z 乘以 4"),
    ("变量", "w = 100\nw /= 5", "设 w 为 100\n设 w 为 w 除以 5"),

    # ── 补充：更多段落变体 ──────────────────────────────────────
    ("段落", "def double(n):\n    return n * 2", "段落 双倍 接收 n：\n    返回 n 乘以 2"),
    ("段落", "def subtract(a, b):\n    return a - b", "段落 减法 接收 a, b：\n    返回 a 减去 b"),
    ("段落", "def multiply(a, b):\n    return a * b", "段落 乘法 接收 a, b：\n    返回 a 乘以 b"),
    ("段落", "def divide(a, b):\n    return a / b", "段落 除法 接收 a, b：\n    返回 a 除以 b"),
    ("段落", "def modulo(a, b):\n    return a % b", "设 段落 为 段落 取余 接收 a, b：\n    返回 a 取余 b"),
    ("段落", "def is_even(n):\n    return n % 2 == 0", "段落 是偶数 接收 n：\n    返回 n 取余 2 等于 0"),
    ("段落", "def is_odd(n):\n    return n % 2 != 0", "段落 是奇数 接收 n：\n    返回 n 取余 2 不等于 0"),
    ("段落", "def clamp(val, lo, hi):\n    if val < lo:\n        return lo\n    if val > hi:\n        return hi\n    return val", "段落 限值 接收 val, lo, hi：\n    如果 val 小于 lo：\n        返回 lo\n    如果 val 大于 hi：\n        返回 hi\n    返回 val"),
    ("段落", "def sign(n):\n    if n > 0:\n        return 1\n    elif n < 0:\n        return -1\n    return 0", "段落 符号 接收 n：\n    如果 n 大于 0：\n        返回 1\n    否则如果 n 小于 0：\n        返回 -1\n    返回 0"),
    ("段落", "def min_of_three(a, b, c):\n    m = a\n    if b < m:\n        m = b\n    if c < m:\n        m = c\n    return m", "段落 三数最小 接收 a, b, c：\n    设 m 为 a\n    如果 b 小于 m：\n        设 m 为 b\n    如果 c 小于 m：\n        设 m 为 c\n    返回 m"),
    ("段落", "def swap(a, b):\n    return b, a", "段落 交换 接收 a, b：\n    返回 b, a"),
    ("段落", "def power2(n):\n    return 2 ** n", "段落 二的幂 接收 n：\n    返回 2 的 n 次方"),
    ("段落", "def negate(n):\n    return -n", "段落 取反 接收 n：\n    返回 0 减去 n"),

    # ── 补充：更多条件变体 ──────────────────────────────────────
    ("条件", "if age >= 18:\n    print('adult')", "如果 age 大于等于 18：\n    打印(\"adult\")"),
    ("条件", "if score > 60:\n    print('pass')\nelse:\n    print('fail')",
     "如果 score 大于 60：\n    打印(\"pass\")\n否则：\n    打印(\"fail\")"),
    ("条件", "if n > 0:\n    print('positive')\nelif n == 0:\n    print('zero')\nelse:\n    print('negative')",
     "如果 n 大于 0：\n    打印(\"positive\")\n否则如果 n 等于 0：\n    打印(\"zero\")\n否则：\n    打印(\"negative\")"),
    ("条件", "if a == b and b == c:\n    print('all equal')",
     "如果 a 等于 b 且 b 等于 c：\n    打印(\"all equal\")"),
    ("条件", "if x < 0 or x > 100:\n    print('out of range')",
     "如果 x 小于 0 或 x 大于 100：\n    打印(\"out of range\")"),
    ("条件", "if not done:\n    print('continue')",
     "如果 非 done：\n    打印(\"continue\")"),
    ("条件", "if len(s) > 0:\n    print('not empty')",
     "如果 len(s) 大于 0：\n    打印(\"not empty\")"),
    ("条件", "if n % 3 == 0:\n    print('divisible by 3')",
     "如果 n 取余 3 等于 0：\n    打印(\"divisible by 3\")"),
    ("条件", "if x >= 0 and x <= 100:\n    print('valid')",
     "如果 x 大于等于 0 且 x 小于等于 100：\n    打印(\"valid\")"),
    ("条件", "grade = 'A' if score >= 90 else 'B'",
     "如果 score 大于等于 90：\n    设 grade 为 \"A\"\n否则：\n    设 grade 为 \"B\""),

    # ── 补充：更多循环变体 ──────────────────────────────────────
    ("循环", "for i in range(5, 15):\n    print(i)", "遍历 i 于 5至14：\n    打印(i)"),
    ("循环", "for i in range(100, 0, -1):\n    print(i)", "遍历 i 于 100至1步1：\n    打印(i)"),
    ("循环", "total = 0\ni = 1\nwhile i <= 100:\n    total += i\n    i += 1", "设 total 为 0\n设 i 为 1\n当 i 小于等于 100：\n    设 total 为 total 加上 i\n    设 i 为 i 加上 1"),
    ("循环", "for c in 'hello':\n    print(c)", "遍历 c 于 \"hello\"：\n    打印(c)"),
    ("循环", "for key in d:\n    print(key, d[key])", "遍历 key 于 d：\n    打印(key)\n    打印(d[key])"),
    ("循环", "while True:\n    cmd = input()\n    if cmd == 'quit':\n        break",
     "当 真：\n    设 cmd 为 输入()\n    如果 cmd 等于 \"quit\"：\n        跳出"),
    ("循环", "for i in range(10):\n    if i % 2 == 0:\n        continue\n    print(i)", "遍历 i 于 0至9：\n    如果 i 取余 2 等于 0：\n        跳过\n    打印(i)"),
    ("循环", "i = 0\nwhile i < len(lst):\n    print(lst[i])\n    i += 1", "设 i 为 0\n当 i 小于 len(lst)：\n    打印(lst[i])\n    设 i 为 i 加上 1"),
    ("循环", "count = 0\nfor x in lst:\n    if x > 0:\n        count += 1", "设 count 为 0\n遍历 x 于 lst：\n    如果 x 大于 0：\n        设 count 为 count 加上 1"),
    ("循环", "for i in range(3):\n    for j in range(3):\n        print(i, j)", "遍历 i 于 0至2：\n    遍历 j 于 0至2：\n        打印(i)\n        打印(j)"),

    # ── 补充：更多列表操作 ──────────────────────────────────────
    ("列表", "first = lst[0]\nlast = lst[-1]", "设 first 为 lst[0]\n设 last 为 lst[len(lst) 减去 1]"),
    ("列表", "lst[2] = 99", "lst[2] = 99"),
    ("列表", "if len(lst) == 0:\n    print('empty')",
     "如果 len(lst) 等于 0：\n    打印(\"empty\")"),
    ("列表", "doubled = [x * 2 for x in lst]", "设 doubled 为 []\n遍历 x 于 lst：\n    doubled.追加(x 乘以 2)"),
    ("列表", "evens = [x for x in lst if x % 2 == 0]", "设 evens 为 []\n遍历 x 于 lst：\n    如果 x 取余 2 等于 0：\n        evens.追加(x)"),
    ("列表", "merged = a + b", "设 merged 为 []\n遍历 x 于 a：\n    merged.追加(x)\n遍历 x 于 b：\n    merged.追加(x)"),
    ("列表", "lst.insert(0, 10)", "设 new_lst 为 [10]\n遍历 x 于 lst：\n    new_lst.追加(x)\n设 lst 为 new_lst"),
    ("列表", "lst.pop()", "设 last 为 lst[len(lst) 减去 1]\n设 new_lst 为 []\n遍历 i 于 0至len(lst)减去2：\n    new_lst.追加(lst[i])\n设 lst 为 new_lst"),
    ("列表", "lst.remove(5)", "设 new_lst 为 []\n设 skip 为 假\n遍历 x 于 lst：\n    如果 x 等于 5 且 非 skip：\n        设 skip 为 真\n    否则：\n        new_lst.追加(x)\n设 lst 为 new_lst"),

    # ── 补充：更多字符串 ────────────────────────────────────────
    ("字符串", "greeting = 'hi' + ' ' + name", "设 greeting 为 \"hi\" 加上 \" \" 加上 name"),
    ("字符串", "print(f'Result: {x}')", "打印(f\"Result: {x}\")"),
    ("字符串", "lower_s = s.lower()", "设 lower_s 为 字符串转小写(s)"),
    ("字符串", "stripped = s.strip()", "设 stripped 为 字符串去空白(s)"),
    ("字符串", "if s.startswith('http'):", "如果 字符串开头是(s, \"http\")："),
    ("字符串", "if s.endswith('.txt'):", "如果 字符串结尾是(s, \".txt\")："),
    ("字符串", "idx = s.index('abc')", "设 idx 为 字符串查找(s, \"abc\")"),
    ("字符串", "repeated = s * 3", "设 repeated 为 字符串重复(s, 3)"),
    ("字符串", "clean = s.replace(' ', '_')", "设 clean 为 字符串替换(s, \" \", \"_\")"),

    # ── 补充：更多字典 ──────────────────────────────────────────
    ("字典", "d = {}", "设 d 为 {}"),
    ("字典", "d['name'] = 'test'", "d[\"name\"] = \"test\""),
    ("字典", "del d['key']", "d.删除(\"key\")"),
    ("字典", "keys = list(d.keys())", "设 keys 为 []\n遍历 k 于 d：\n    keys.追加(k)"),
    ("字典", "if 'age' in d:\n    age = d['age']",
     "如果 \"age\" 于 d：\n        设 age 为 d[\"age\"]"),
    ("字典", "for key in sorted(d):", "设 keys 为 []\n遍历 k 于 d：\n    keys.追加(k)\n# sorted需要自行实现"),

    # ── 补充：更多异常 ──────────────────────────────────────────
    ("异常", "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    result = 0", "尝试：\n    设 result 为 10 除以 0\n捕获 异常：\n    设 result 为 0"),
    ("异常", "try:\n    x = int(input())\nexcept ValueError:\n    x = 0\n    print('invalid')",
     "尝试：\n    设 x 为 int(输入())\n捕获 异常：\n    设 x 为 0\n    打印(\"invalid\")"),
    ("异常", "try:\n    f = open('data.txt')\n    content = f.read()\nexcept:\n    content = ''",
     "尝试：\n    设 f 为 读取文件(\"data.txt\")\n捕获 异常：\n    设 content 为 \"\""),
    ("异常", "raise Exception('error')", "抛出 异常(\"error\")"),
    ("异常", "try:\n    x = lst[100]\nexcept IndexError:\n    x = None", "尝试：\n    设 x 为 lst[100]\n捕获 异常：\n    设 x 为 空"),

    # ── 补充：更多导入 ──────────────────────────────────────────
    ("导入", "import json", "导入 JSON"),
    ("导入", "import os", "导入 文件系统"),
    ("导入", "from math import sqrt, pi", "从 数学工具 导入 平方, 圆周率"),
    ("导入", "from typing import List", "从 类型工具 导入 列表类型"),
    ("导入", "import random\nx = random.randint(1, 10)", "导入 随机数据\n设 x 为 随机整数(1, 10)"),

    # ── 补充：更多类 ────────────────────────────────────────────
    ("类", "class Counter:\n    def __init__(self):\n        self.count = 0\n    def increment(self):\n        self.count += 1\n    def get(self):\n        return self.count", "类 计数器：\n    属性 计数值\n    构造：\n        己.计数值 为 0\n    段落 增加：\n        己.计数值 加上 1\n    段落 获取：\n        返回 己.计数值"),
    ("类", "class Rect:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n    def area(self):\n        return self.w * self.h", "类 矩形：\n    属性 宽\n    属性 高\n    构造 接收 宽, 高：\n        己.宽 为 宽\n        己.高 为 高\n    段落 面积：\n        返回 己.宽 乘以 己.高"),
    ("类", "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        pass", "类 动物：\n    属性 名字\n    构造 接收 名字：\n        己.名字 为 名字\n    段落 说话：\n        空操作"),
    ("类", "class Bird(Animal):\n    def speak(self):\n        print(f'{self.name}: chirp!')",
     "类 鸟 继承 动物：\n    段落 说话：\n        打印(f\"{己.名字}: chirp!\")"),
    ("类", "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0", "类 栈：\n    属性 元素列表\n    构造：\n        己.元素列表 为 []\n    段落 入栈 接收 item：\n        己.元素列表.追加(item)\n    段落 出栈：\n        返回 己.元素列表.弹出()\n    段落 是否为空：\n        返回 len(己.元素列表) 等于 0"),
    ("类", "class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n    def deposit(self, amount):\n        self.balance += amount\n    def withdraw(self, amount):\n        if amount <= self.balance:\n            self.balance -= amount", "类 银行账户：\n    属性 户主\n    属性 余额\n    构造 接收 owner, balance：\n        己.户主 为 owner\n        己.余额 为 balance\n    段落 存款 接收 amount：\n        己.余额 加上 amount\n    段落 取款 接收 amount：\n        如果 amount 小于等于 己.余额：\n            己.余额 减去 amount"),

    # ── 补充：更多复合示例 ──────────────────────────────────────
    ("复合", "def linear_search(lst, target):\n    for i in range(len(lst)):\n        if lst[i] == target:\n            return i\n    return -1", "段落 线性查找 接收 lst, target：\n    遍历 i 于 0至len(lst)减去1：\n        如果 lst[i] 等于 target：\n            返回 i\n    返回 -1"),
    ("复合", "def insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j+1] = arr[j]\n            j -= 1\n        arr[j+1] = key\n    return arr", "段落 插入排序 接收 arr：\n    遍历 i 于 1至len(arr)减去1：\n        设 key 为 arr[i]\n        设 j 为 i 减去 1\n        当 j 大于等于 0 且 arr[j] 大于 key：\n            arr[j 加上 1] = arr[j]\n            设 j 为 j 减去 1\n        arr[j 加上 1] = key\n    返回 arr"),
    ("复合", "def palindrome_check(s):\n    return s == s[::-1]",
     "段落 回文判断 接收 s：\n    设 reversed 为 \"\"\n    设 i 为 len(s) 减去 1\n    当 i 大于等于 0：\n        设 reversed 为 reversed 加上 s[i]\n        设 i 为 i 减去 1\n    返回 s 等于 reversed"),
    ("复合", "def count_vowels(s):\n    vowels = 'aeiou'\n    count = 0\n    for c in s:\n        if c in vowels:\n            count += 1\n    return count",
     "段落 统计元音 接收 s：\n    设 vowels 为 \"aeiou\"\n    设 count 为 0\n    遍历 c 于 s：\n        如果 字符串包含(vowels, c)：\n            设 count 为 count 加上 1\n    返回 count"),
    ("复合", "def matrix_sum(matrix):\n    total = 0\n    for row in matrix:\n        for val in row:\n            total += val\n    return total", "段落 矩阵求和 接收 matrix：\n    设 total 为 0\n    遍历 row 于 matrix：\n        遍历 val 于 row：\n            设 total 为 total 加上 val\n    返回 total"),
    ("复合", "def leap_year(year):\n    if year % 400 == 0:\n        return True\n    if year % 100 == 0:\n        return False\n    if year % 4 == 0:\n        return True\n    return False", "段落 闰年判断 接收 year：\n    如果 year 取余 400 等于 0：\n        返回 真\n    如果 year 取余 100 等于 0：\n        返回 假\n    如果 year 取余 4 等于 0：\n        返回 真\n    返回 假"),
    ("复合", "def sum_digits(n):\n    total = 0\n    while n > 0:\n        total += n % 10\n        n //= 10\n    return total", "段落 数位求和 接收 n：\n    设 total 为 0\n    当 n 大于 0：\n        设 total 为 total 加上 n 取余 10\n        设 n 为 n 除以 10\n    返回 total"),
    ("复合", "def fibonacci_iter(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n+1):\n        a, b = b, a+b\n    return b", "段落 斐波那契迭代 接收 n：\n    如果 n 小于等于 1：\n        返回 n\n    设 a 为 0\n    设 b 为 1\n    遍历 _ 于 2至n：\n        设 tmp 为 b\n        设 b 为 a 加上 b\n        设 a 为 tmp\n    返回 b"),
    ("复合", "def temperature_report(celsius):\n    if celsius < 0:\n        return 'freezing'\n    elif celsius < 15:\n        return 'cold'\n    elif celsius < 25:\n        return 'comfortable'\n    elif celsius < 35:\n        return 'warm'\n    else:\n        return 'hot'",
     "段落 温度报告 接收 celsius：\n    如果 celsius 小于 0：\n        返回 \"freezing\"\n    否则如果 celsius 小于 15：\n        返回 \"cold\"\n    否则如果 celsius 小于 25：\n        返回 \"comfortable\"\n    否则如果 celsius 小于 35：\n        返回 \"warm\"\n    否则：\n        返回 \"hot\""),
    ("复合", "def rock_paper_scissors(p1, p2):\n    if p1 == p2:\n        return 'draw'\n    if (p1 == 'rock' and p2 == 'scissors') or (p1 == 'scissors' and p2 == 'paper') or (p1 == 'paper' and p2 == 'rock'):\n        return 'p1 wins'\n    return 'p2 wins'",
     "段落 石头剪刀布 接收 p1, p2：\n    如果 p1 等于 p2：\n        返回 \"draw\"\n    如果 (p1 等于 \"rock\" 且 p2 等于 \"scissors\") 或 (p1 等于 \"scissors\" 且 p2 等于 \"paper\") 或 (p1 等于 \"paper\" 且 p2 等于 \"rock\")：\n        返回 \"p1 wins\"\n    返回 \"p2 wins\""),
    ("复合", "def collatz(n):\n    steps = 0\n    while n != 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        steps += 1\n    return steps", "段落 考拉兹 接收 n：\n    设 steps 为 0\n    当 n 不等于 1：\n        如果 n 取余 2 等于 0：\n            设 n 为 n 除以 2\n        否则：\n            设 n 为 3 乘以 n 加上 1\n        设 steps 为 steps 加上 1\n    返回 steps"),
    ("复合", "def caesar_cipher(text, shift):\n    result = ''\n    for c in text:\n        if c.isalpha():\n            base = ord('a') if c.islower() else ord('A')\n            result += chr((ord(c) - base + shift) % 26 + base)\n        else:\n            result += c\n    return result",
     "段落 凯撒加密 接收 text, shift：\n    设 result 为 \"\"\n    遍历 c 于 text：\n        如果 字符串包含(小写字母表, c) 或 字符串包含(大写字母表, c)：\n            设 shifted 为 字符偏移(c, shift)\n            设 result 为 result 加上 shifted\n        否则：\n            设 result 为 result 加上 c\n    返回 result"),
    ("复合", "def histogram(data, bins):\n    counts = [0] * bins\n    for val in data:\n        idx = min(int(val * bins), bins - 1)\n        counts[idx] += 1\n    return counts", "段落 直方图 接收 data, bins：\n    设 counts 为 []\n    遍历 _ 于 0至bins减去1：\n        counts.追加(0)\n    遍历 val 于 data：\n        设 idx 为 int(val 乘以 bins)\n        如果 idx 大于等于 bins：\n            设 idx 为 bins 减去 1\n        counts[idx] = counts[idx] 加上 1\n    返回 counts"),

    # ── 补充：暗坑修正对照（教模型避开常见错误）──────────────────
    ("暗坑", "lst[0] = 10", "lst[0] = 10"),
    ("暗坑", "n = len(lst)", "设 n 为 len(lst)"),
    ("暗坑", "i = i + 1", "设 i 为 i 加上 1"),
    ("暗坑", "a + b", "设 a 为 a 加上 b"),
    ("暗坑", "a - b", "设 a 为 a 减去 b"),
    ("暗坑", "a * b", "设 a 为 a 乘以 b"),
    ("暗坑", "a / b", "设 a 为 a 除以 b"),
    ("暗坑", "a % b", "设 a 为 a 取余 b"),
    ("暗坑", "a == b", "a 等于 b"),
    ("暗坑", "a != b", "a 不等于 b"),
    ("暗坑", "a > b", "a 大于 b"),
    ("暗坑", "a < b", "a 小于 b"),
    ("暗坑", "a >= b", "a 大于等于 b"),
    ("暗坑", "a <= b", "a 小于等于 b"),
    ("暗坑", "a and b", "a 且 b"),
    ("暗坑", "a or b", "a 或 b"),
    ("暗坑", "not a", "非 a"),
    ("暗坑", "a += 1", "设 a 为 a 加上 1"),
    ("暗坑", "a -= 1", "设 a 为 a 减去 1"),
    ("暗坑", "a *= 2", "设 a 为 a 乘以 2"),
    ("暗坑", "a /= 2", "设 a 为 a 除以 2"),
    ("暗坑", "True", "真"),
    ("暗坑", "False", "假"),
    ("暗坑", "None", "空"),
    ("暗坑", "break", "跳出"),
    ("暗坑", "continue", "跳过"),
    ("暗坑", "return x", "返回 x"),
    ("暗坑", "def f(a, b):", "段落 f 接收 a, b："),
    ("暗坑", "while cond:", "当 cond："),
    ("暗坑", "for i in range(n):", "遍历 i 于 0至n减去1："),
    ("暗坑", "class Foo:", "类 Foo："),
    ("暗坑", "try:", "尝试："),
    ("暗坑", "except:", "捕获 异常："),
    ("暗坑", "raise Exception()", "抛出 异常()"),
    ("暗坑", "import math", "导入 数学工具"),
    ("暗坑", "from math import sqrt", "从 数学工具 导入 平方"),
    ("暗坑", "for x in lst:", "遍历 x 于 lst："),
    ("暗坑", "print('hello')", "打印(\"hello\")"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：Trait/协议系统
    # ═══════════════════════════════════════════════════════════════
    ("协议", "class Printable:\n    def display(self):\n        return self.name",
     "协议 可打印：\n    段落 显示：\n        返回 己.名称"),
    ("协议", "class Countable:\n    def count(self):\n        return len(self.items)",
     "协议 可计数：\n    段落 计数：\n        返回 len(己.元素列表)"),
    ("协议", "class Comparable:\n    def compare(self, other):\n        return self.val > other.val",
     "协议 可比较：\n    段落 比较 接收 其他：\n        返回 己.值 大于 其他.值"),
    ("协议", "class Iterable:\n    def __iter__(self):\n        return iter(self.items)",
     "协议 可迭代：\n    段落 __迭代__：\n        返回 迭代(己.元素列表)"),
    ("协议", "class Serializer:\n    def to_dict(self):\n        return {'name': self.name, 'val': self.val}",
     "协议 可序列化：\n    段落 转字典：\n        返回 {\"名称\": 己.名称, \"值\": 己.值}"),
    ("协议", "class Validator:\n    def validate(self, data):\n        return data is not None",
     "协议 可验证：\n    段落 验证 接收 数据：\n        返回 数据 不等于 空"),
    ("协议", "class Formatter:\n    def format(self, data):\n        return str(data).upper()",
     "协议 可格式化：\n    段落 格式化 接收 数据：\n        返回 字符串转大写(str(数据))"),
    ("协议", "class Logger:\n    def log(self, msg, level='INFO'):\n        print(f'[{level}] {msg}')",
     "协议 可日志：\n    段落 记录 接收 消息, 级别：\n        打印(f\"[{级别}] {消息}\")"),
    ("协议", "class Closable:\n    def close(self):\n        self.opened = False",
     "协议 可关闭：\n    段落 关闭：\n        己.已打开 为 假"),
    ("协议", "class Cacheable:\n    def get_cache(self, key):\n        return self.cache.get(key)",
     "协议 可缓存：\n    段落 取缓存 接收 键：\n        返回 己.缓存.get(键)"),
    ("协议", "class Drawable:\n    def draw(self, canvas):\n        canvas.append(self)",
     "协议 可绘制：\n    段落 绘制 接收 画布：\n        画布.追加(己)"),
    ("协议", "class Configurable:\n    def configure(self, settings):\n        for k, v in settings.items():\n            setattr(self, k, v)",
     "协议 可配置：\n    段落 配置 接收 设置：\n        遍历 k 于 设置：\n            设 己.k 为 设置[k]"),
    ("协议", "class Runnable:\n    def run(self):\n        self.execute()",
     "协议 可运行：\n    段落 运行：\n        己.执行()"),
    ("协议", "class Saveable:\n    def save(self, path):\n        with open(path, 'w') as f:\n            f.write(self.data)",
     "协议 可保存：\n    段落 保存 接收 路径：\n        使用 文件 为 打开(路径, \"w\")：\n            文件.写入(己.数据)"),
    ("协议", "class Loadable:\n    def load(self, path):\n        with open(path) as f:\n            return f.read()",
     "协议 可加载：\n    段落 加载 接收 路径：\n        使用 文件 为 打开(路径)：\n            返回 文件.读取()"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：模式匹配
    # ═══════════════════════════════════════════════════════════════
    ("模式匹配", "match value:\n    case 1:\n        print('one')\n    case 2:\n        print('two')",
     "匹配 值：\n    当 1：\n        打印(\"一\")\n    当 2：\n        打印(\"二\")"),
    ("模式匹配", "match x:\n    case 0:\n        print('zero')\n    case n:\n        print(f'other: {n}')",
     "匹配 x：\n    当 0：\n        打印(\"零\")\n    当 n：\n        打印(f\"其他: {n}\")"),
    ("模式匹配", "match code:\n    case 200:\n        return 'ok'\n    case 404:\n        return 'not found'\n    case _:\n        return 'error'",
     "匹配 code：\n    当 200：\n        返回 \"ok\"\n    当 404：\n        返回 \"未找到\"\n    当 _：\n        返回 \"错误\""),
    ("模式匹配", "match status:\n    case 'active':\n        print('running')\n    case 'inactive':\n        print('stopped')",
     "匹配 status：\n    当 \"active\"：\n        打印(\"运行中\")\n    当 \"inactive\"：\n        打印(\"已停止\")"),
    ("模式匹配", "match pair:\n    case (0, 0):\n        print('origin')\n    case (x, 0):\n        print(f'x={x}')\n    case (0, y):\n        print(f'y={y}')",
     "匹配 pair：\n    当 (0, 0)：\n        打印(\"原点\")\n    当 (x, 0)：\n        打印(f\"x={x}\")\n    当 (0, y)：\n        打印(f\"y={y}\")"),
    ("模式匹配", "match value:\n    case int(x):\n        print(f'integer: {x}')\n    case str(s):\n        print(f'string: {s}')",
     "匹配 值：\n    当 整数(x)：\n        打印(f\"整数: {x}\")\n    当 字符串(s)：\n        打印(f\"字符串: {s}\")"),
    ("模式匹配", "match data:\n    case [a, b]:\n        print(f'list: {a}, {b}')\n    case {'key': v}:\n        print(f'dict: {v}')",
     "匹配 data：\n    当 [a, b]：\n        打印(f\"列表: {a}, {b}\")\n    当 {\"key\": v}：\n        打印(f\"字典: {v}\")"),
    ("模式匹配", "match result:\n    case 1 if flag:\n        print('one and flag')\n    case 1:\n        print('one')",
     "匹配 结果：\n    当 1 若 flag：\n        打印(\"一且有旗标\")\n    当 1：\n        打印(\"一\")"),
    ("模式匹配", "match score:\n    case x if x >= 90:\n        grade = 'A'\n    case x if x >= 80:\n        grade = 'B'\n    case _:\n        grade = 'C'",
     "匹配 分数：\n    当 x 若 x 大于等于 90：\n        设 grade 为 \"A\"\n    当 x 若 x 大于等于 80：\n        设 grade 为 \"B\"\n    当 _：\n        设 grade 为 \"C\""),
    ("模式匹配", "match color:\n    case 'red' | 'blue' | 'green':\n        print('primary')\n    case _:\n        print('other')",
     "匹配 颜色：\n    当 \"red\" | \"blue\" | \"green\"：\n        打印(\"原色\")\n    当 _：\n        打印(\"其他\")"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：迭代器协议
    # ═══════════════════════════════════════════════════════════════
    ("迭代器", "class Counter:\n    def __init__(self, limit):\n        self.limit = limit\n        self.n = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.n >= self.limit:\n            raise StopIteration()\n        self.n += 1\n        return self.n",
     "类 计数器：\n    属性 上限\n    属性 当前值\n    构造 接收 上限：\n        己.上限 为 上限\n        己.当前值 为 0\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.当前值 大于等于 己.上限：\n            抛出 迭代停止()\n        设 己.当前值 为 己.当前值 加上 1\n        返回 己.当前值"),
    ("迭代器", "class Range:\n    def __init__(self, n):\n        self.n = n\n        self.i = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.i >= self.n:\n            raise StopIteration()\n        val = self.i\n        self.i += 1\n        return val",
     "类 范围：\n    属性 上限\n    属性 索引\n    构造 接收 上限：\n        己.上限 为 上限\n        己.索引 为 0\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.索引 大于等于 己.上限：\n            抛出 迭代停止()\n        设 val 为 己.索引\n        设 己.索引 为 己.索引 加上 1\n        返回 val"),
    ("迭代器", "for item in my_iterable:\n    print(item)",
     "遍历 元素 于 my_iterable：\n    打印(元素)"),
    ("迭代器", "for val in counter:\n    print(val)",
     "遍历 val 于 counter：\n    打印(val)"),
    ("迭代器", "for x in range_obj:\n    print(x * 2)",
     "遍历 x 于 range_obj：\n    打印(x 乘以 2)"),
    ("迭代器", "class FibIter:\n    def __init__(self, n):\n        self.n = n\n        self.a = 0\n        self.b = 1\n        self.i = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.i >= self.n:\n            raise StopIteration()\n        val = self.a\n        self.a, self.b = self.b, self.a + self.b\n        self.i += 1\n        return val",
     "类 斐波那契迭代器：\n    属性 上限\n    属性 前值\n    属性 后值\n    属性 索引\n    构造 接收 上限：\n        己.上限 为 上限\n        己.前值 为 0\n        己.后值 为 1\n        己.索引 为 0\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.索引 大于等于 己.上限：\n            抛出 迭代停止()\n        设 val 为 己.前值\n        设 tmp 为 己.后值\n        设 己.后值 为 己.前值 加上 己.后值\n        设 己.前值 为 tmp\n        设 己.索引 为 己.索引 加上 1\n        返回 val"),
    ("迭代器", "class EvenIter:\n    def __init__(self, max_n):\n        self.max_n = max_n\n        self.n = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.n > self.max_n:\n            raise StopIteration()\n        val = self.n\n        self.n += 2\n        return val",
     "类 偶数迭代器：\n    属性 最大值\n    属性 当前值\n    构造 接收 最大值：\n        己.最大值 为 最大值\n        己.当前值 为 0\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.当前值 大于 己.最大值：\n            抛出 迭代停止()\n        设 val 为 己.当前值\n        设 己.当前值 为 己.当前值 加上 2\n        返回 val"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：上下文管理器
    # ═══════════════════════════════════════════════════════════════
    ("上下文", "with open('file.txt') as f:\n    content = f.read()",
     "使用 文件 为 打开(\"file.txt\")：\n    设 content 为 文件.读取()"),
    ("上下文", "with open('data.txt', 'w') as f:\n    f.write('hello')",
     "使用 文件 为 打开(\"data.txt\", \"w\")：\n    文件.写入(\"hello\")"),
    ("上下文", "with open('log.txt', 'a') as f:\n    f.write(line + '\\n')",
     "使用 文件 为 打开(\"log.txt\", \"a\")：\n    文件.写入(line 加上 \"\\n\")"),
    ("上下文", "with lock:\n    shared_data += 1",
     "使用 锁：\n    设 shared_data 为 shared_data 加上 1"),
    ("上下文", "with open('a.txt') as f1, open('b.txt') as f2:\n    data1 = f1.read()\n    data2 = f2.read()",
     "使用 文件1 为 打开(\"a.txt\"), 文件2 为 打开(\"b.txt\")：\n    设 data1 为 文件1.读取()\n    设 data2 为 文件2.读取()"),
    ("上下文", "class ManagedFile:\n    def __enter__(self):\n        return self\n    def __exit__(self, *args):\n        self.close()",
     "类 托管文件：\n    段落 __进入__：\n        返回 己\n    段落 __退出__ 接收 *args：\n        己.关闭()"),
    ("上下文", "with open(src) as f:\n    data = json.load(f)",
     "使用 文件 为 打开(src)：\n    设 data 为 JSON.加载(文件)"),
    ("上下文", "with open('out.txt', 'w') as f:\n    for i in range(10):\n        f.write(str(i))",
     "使用 文件 为 打开(\"out.txt\", \"w\")：\n    遍历 i 于 0至9：\n        文件.写入(str(i))"),
    ("上下文", "with db.connection() as conn:\n    result = conn.query(sql)",
     "使用 连接 为 db.连接()：\n    设 result 为 连接.查询(sql)"),
    ("上下文", "with timer:\n    result = expensive_func()",
     "使用 计时器：\n    设 result 为 耗时函数()"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：异常映射
    # ═══════════════════════════════════════════════════════════════
    ("异常映射", "raise StopIteration()", "抛出 迭代停止()"),
    ("异常映射", "try:\n    next(it)\nexcept StopIteration:\n    print('done')",
     "尝试：\n    下一项(it)\n捕获 迭代停止：\n    打印(\"完成\")"),
    ("异常映射", "raise ValueError('invalid value')", "抛出 数值错误(\"无效值\")"),
    ("异常映射", "raise TypeError('type mismatch')", "抛出 类型错误(\"类型不匹配\")"),
    ("异常映射", "raise KeyError('key not found')", "抛出 键错误(\"键未找到\")"),
    ("异常映射", "raise IndexError('out of range')", "抛出 索引错误(\"超出范围\")"),
    ("异常映射", "try:\n    result = 1 / 0\nexcept ZeroDivisionError:\n    result = 0",
     "尝试：\n    设 result 为 1 除以 0\n捕获 除以零：\n    设 result 为 0"),
    ("异常映射", "try:\n    x = int('abc')\nexcept ValueError as e:\n    print(e)",
     "尝试：\n    设 x 为 整数(\"abc\")\n捕获 数值错误 为 e：\n    打印(e)"),
    ("异常映射", "try:\n    d = {}\n    x = d['missing']\nexcept KeyError:\n    x = None",
     "尝试：\n    设 d 为 {}\n    设 x 为 d[\"missing\"]\n捕获 键错误：\n    设 x 为 空"),
    ("异常映射", "try:\n    lst = [1, 2, 3]\n    x = lst[10]\nexcept IndexError:\n    x = -1",
     "尝试：\n    设 lst 为 [1, 2, 3]\n    设 x 为 lst[10]\n捕获 索引错误：\n    设 x 为 -1"),
    ("异常映射", "try:\n    f = open('nope.txt')\nexcept FileNotFoundError:\n    print('not found')",
     "尝试：\n    设 f 为 打开(\"nope.txt\")\n捕获 文件未找到：\n    打印(\"未找到\")"),
    ("异常映射", "try:\n    x = None\n    x.some()\nexcept AttributeError:\n    print('no attr')",
     "尝试：\n    设 x 为 空\n    x.某方法()\n捕获 属性错误：\n    打印(\"无属性\")"),
    ("异常映射", "try:\n    import math\n    x = math.non_existent\nexcept AttributeError as e:\n    x = 0",
     "尝试：\n    导入 数学工具\n    设 x 为 数学工具.不存在\n捕获 属性错误 为 e：\n    设 x 为 0"),
    ("异常映射", "try:\n    result = expensive()\nexcept (ValueError, TypeError):\n    result = fallback()",
     "尝试：\n    设 result 为 耗时操作()\n捕获 数值错误, 类型错误：\n    设 result 为 回退()"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 新特性：新语法对照
    # ═══════════════════════════════════════════════════════════════
    ("新语法", "x = 1", "设 x 为 1"),
    ("新语法", "result = a + b", "设 result 为 a 加上 b"),
    ("新语法", "def add(a, b):\n    return a + b",
     "段落 加法 接收 a, b：\n    返回 a 加上 b"),
    ("新语法", "def sub(a, b):\n    return a - b",
     "段落 减法 接收 a, b：\n    返回 a 减去 b"),
    ("新语法", "def mul(a, b):\n    return a * b",
     "段落 乘法 接收 a, b：\n    返回 a 乘以 b"),
    ("新语法", "def div(a, b):\n    return a / b",
     "段落 除法 接收 a, b：\n    返回 a 除以 b"),
    ("新语法", "def power(base, exp):\n    return base ** exp",
     "段落 幂 接收 base, exp：\n    返回 base 的 exp 次方"),
    ("新语法", "if x > 0:\n    print('positive')",
     "如果 x 大于 0：\n    打印(\"正数\")"),
    ("新语法", "total = 0\nfor i in range(5):\n    total += i",
     "设 total 为 0\n遍历 i 于 0至4：\n    设 total 为 total 加上 i"),
    ("新语法", "while x > 0:\n    x -= 1",
     "当 x 大于 0：\n    设 x 为 x 减去 1"),
    ("新语法", "class Person:\n    def __init__(self, name):\n        self.name = name",
     "类 人：\n    属性 名称\n    构造 接收 名称：\n        己.名称 为 名称"),
    ("新语法", "numbers = [1, 2, 3]\nfor n in numbers:\n    print(n)",
     "设 numbers 为 [1, 2, 3]\n遍历 n 于 numbers：\n    打印(n)"),
    ("新语法", "try:\n    x = int('42')\nexcept:\n    x = 0",
     "尝试：\n    设 x 为 整数(\"42\")\n捕获 异常：\n    设 x 为 0"),
    ("新语法", "def greet(name):\n    return f'Hello, {name}!'",
     "段落 打招呼 接收 名称：\n    返回 f\"Hello, {名称}!\""),
    ("新语法", "data = {'key': 'value'}\nprint(data['key'])",
     "设 data 为 {\"key\": \"value\"}\n打印(data[\"key\"])"),
    ("新语法", "cond = True\nresult = 'yes' if cond else 'no'",
     "设 cond 为 真\n设 result 为 \"yes\" 如果 cond 否则 \"no\""),
    ("新语法", "for i in range(1, 10, 2):\n    print(i)",
     "遍历 i 于 1至9步2：\n    打印(i)"),
    ("新语法", "items = ['a', 'b', 'c']\nfor idx, val in enumerate(items):\n    print(idx, val)",
     "设 items 为 [\"a\", \"b\", \"c\"]\n设 idx 为 0\n遍历 val 于 items：\n    打印(idx)\n    打印(val)\n    设 idx 为 idx 加上 1"),
    ("新语法", "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
     "段落 阶乘 接收 n：\n    如果 n 小于等于 1：\n        返回 1\n    返回 n 乘以 阶乘(n 减去 1)"),
    ("新语法", "s = 'hello'\nprint(s.upper())",
     "设 s 为 \"hello\"\n打印(字符串转大写(s))"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 补充：更多协议变体
    # ═══════════════════════════════════════════════════════════════
    ("协议", "class Sizable:\n    def size(self):\n        return len(self.data)",
     "协议 可度量：\n    段落 大小：\n        返回 len(己.数据)"),
    ("协议", "class Named:\n    def get_name(self):\n        return self.name",
     "协议 有名称：\n    段落 取名称：\n        返回 己.名称"),
    ("协议", "class Identifiable:\n    def get_id(self):\n        return self.id",
     "协议 可标识：\n    段落 取标识：\n        返回 己.标识"),
    ("协议", "class Encodable:\n    def encode(self):\n        return self.data.encode('utf-8')",
     "协议 可编码：\n    段落 编码：\n        返回 己.数据.编码(\"utf-8\")"),
    ("协议", "class Decodable:\n    def decode(self, raw):\n        self.data = raw.decode('utf-8')",
     "协议 可解码：\n    段落 解码 接收 raw：\n        己.数据 为 raw.解码(\"utf-8\")"),
    ("协议", "class Mergable:\n    def merge(self, other):\n        return self.data + other.data",
     "协议 可合并：\n    段落 合并 接收 其他：\n        返回 己.数据 加上 其他.数据"),
    ("协议", "class Cloneable:\n    def clone(self):\n        return copy(self.data)",
     "协议 可克隆：\n    段落 克隆：\n        返回 复制(己.数据)"),
    ("协议", "class Parsable:\n    def parse(self, text):\n        return self.parser(text)",
     "协议 可解析：\n    段落 解析 接收 文本：\n        返回 己.解析器(文本)"),
    ("协议", "class Filterable:\n    def filter(self, predicate):\n        return [x for x in self.items if predicate(x)]",
     "协议 可筛选：\n    段落 筛选 接收 判断：\n        设 result 为 []\n        遍历 x 于 己.元素列表：\n            如果 判断(x)：\n                result.追加(x)\n        返回 result"),
    ("协议", "class Sorted:\n    def sort(self):\n        return sorted(self.items)",
     "协议 可排序：\n    段落 排序：\n        返回 排序(己.元素列表)"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 补充：更多模式匹配变体
    # ═══════════════════════════════════════════════════════════════
    ("模式匹配", "match value:\n    case 0:\n        result = 'zero'\n    case 1:\n        result = 'one'\n    case 2:\n        result = 'two'\n    case _:\n        result = 'many'",
     "匹配 值：\n    当 0：\n        设 result 为 \"零\"\n    当 1：\n        设 result 为 \"一\"\n    当 2：\n        设 result 为 \"二\"\n    当 _：\n        设 result 为 \"多\""),
    ("模式匹配", "match point:\n    case (0, 0):\n        return 'origin'\n    case (x, 0):\n        return f'x={x}'\n    case (0, y):\n        return f'y={y}'\n    case (x, y):\n        return f'({x},{y})'",
     "匹配 point：\n    当 (0, 0)：\n        返回 \"原点\"\n    当 (x, 0)：\n        返回 f\"x={x}\"\n    当 (0, y)：\n        返回 f\"y={y}\"\n    当 (x, y)：\n        返回 f\"({x},{y})\""),
    ("模式匹配", "match status_code:\n    case 200 | 201 | 204:\n        return 'success'\n    case 400 | 404:\n        return 'client error'\n    case 500:\n        return 'server error'",
     "匹配 状态码：\n    当 200 | 201 | 204：\n        返回 \"成功\"\n    当 400 | 404：\n        返回 \"客户端错误\"\n    当 500：\n        返回 \"服务器错误\""),
    ("模式匹配", "match result:\n    case {'ok': value}:\n        return value\n    case {'error': msg}:\n        raise Exception(msg)",
     "匹配 result：\n    当 {\"ok\": value}：\n        返回 value\n    当 {\"error\": msg}：\n        抛出 异常(msg)"),
    ("模式匹配", "match shapes:\n    case []:\n        print('empty')\n    case [first]:\n        print(f'one: {first}')\n    case [first, *rest]:\n        print(f'first: {first}, rest: {len(rest)}')",
     "匹配 shapes：\n    当 []：\n        打印(\"空\")\n    当 [first]：\n        打印(f\"一个: {first}\")\n    当 [first, *rest]：\n        打印(f\"首个: {first}, 剩余: {len(rest)}\")"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 补充：更多迭代器变体
    # ═══════════════════════════════════════════════════════════════
    ("迭代器", "for item in iterable:\n    if item > 0:\n        print(item)",
     "遍历 元素 于 iterable：\n    如果 元素 大于 0：\n        打印(元素)"),
    ("迭代器", "class SquareIter:\n    def __init__(self, n):\n        self.n = n\n        self.i = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.i >= self.n:\n            raise StopIteration()\n        val = self.i ** 2\n        self.i += 1\n        return val",
     "类 平方迭代器：\n    属性 上限\n    属性 索引\n    构造 接收 上限：\n        己.上限 为 上限\n        己.索引 为 0\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.索引 大于等于 己.上限：\n            抛出 迭代停止()\n        设 val 为 己.索引 的 2 次方\n        设 己.索引 为 己.索引 加上 1\n        返回 val"),
    ("迭代器", "class StepIter:\n    def __init__(self, start, end, step):\n        self.val = start\n        self.end = end\n        self.step = step\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.val >= self.end:\n            raise StopIteration()\n        val = self.val\n        self.val += self.step\n        return val",
     "类 步进迭代器：\n    属性 当前值\n    属性 结束值\n    属性 步长\n    构造 接收 开始, 结束, 步长：\n        己.当前值 为 开始\n        己.结束值 为 结束\n        己.步长 为 步长\n    段落 __迭代__：\n        返回 己\n    段落 __下一项__：\n        如果 己.当前值 大于等于 己.结束值：\n            抛出 迭代停止()\n        设 val 为 己.当前值\n        设 己.当前值 为 己.当前值 加上 己.步长\n        返回 val"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 补充：更多上下文管理器变体
    # ═══════════════════════════════════════════════════════════════
    ("上下文", "with open('input.txt') as f:\n    for line in f:\n        print(line.strip())",
     "使用 文件 为 打开(\"input.txt\")：\n    遍历 line 于 文件：\n        打印(字符串去空白(line))"),
    ("上下文", "with open('log.txt', 'w') as f:\n    f.write('start\\n')\n    f.write('end\\n')",
     "使用 文件 为 打开(\"log.txt\", \"w\")：\n    文件.写入(\"start\\n\")\n    文件.写入(\"end\\n\")"),
    ("上下文", "with open('data.json') as f:\n    import json\n    data = json.load(f)",
     "使用 文件 为 打开(\"data.json\")：\n    导入 JSON\n    设 data 为 JSON.加载(文件)"),
    ("上下文", "class Timer:\n    def __enter__(self):\n        import time\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        import time\n        self.elapsed = time.time() - self.start",
     "类 计时器：\n    属性 开始时间\n    属性 已过时间\n    段落 __进入__：\n        己.开始时间 为 当前时间()\n        返回 己\n    段落 __退出__ 接收 *args：\n        己.已过时间 为 当前时间() 减去 己.开始时间"),
    ("上下文", "class Connection:\n    def __enter__(self):\n        self.open()\n        return self\n    def __exit__(self, *args):\n        self.close()",
     "类 连接：\n    段落 __进入__：\n        己.打开()\n        返回 己\n    段落 __退出__ 接收 *args：\n        己.关闭()"),

    # ═══════════════════════════════════════════════════════════════
    # v5.0 补充：更多异常映射变体
    # ═══════════════════════════════════════════════════════════════
    ("异常映射", "try:\n    x = int('abc')\nexcept ValueError:\n    x = -1\nfinally:\n    print('done')",
     "尝试：\n    设 x 为 整数(\"abc\")\n捕获 数值错误：\n    设 x 为 -1\n最终：\n    打印(\"完成\")"),
    ("异常映射", "try:\n    f = open('test.txt')\n    data = f.read()\nexcept (FileNotFoundError, PermissionError):\n    data = ''",
     "尝试：\n    设 f 为 打开(\"test.txt\")\n    设 data 为 f.读取()\n捕获 文件未找到, 权限错误：\n    设 data 为 \"\""),
    ("异常映射", "try:\n    result = risky_operation()\nexcept Exception as e:\n    print(f'Error: {e}')\n    result = None",
     "尝试：\n    设 result 为 危险操作()\n捕获 异常 为 e：\n    打印(f\"错误: {e}\")\n    设 result 为 空"),
]


# ═══════════════════════════════════════════════════════════════════
# 变体扩充：对基础对照对做等价变换
# ═══════════════════════════════════════════════════════════════════

def _expand_variants(pairs: List[tuple]) -> List[tuple]:
    """对手工对照对做变体扩充，增加训练数据量

    变体策略：
    1. 变量名替换：x→甲, y→乙, n→数, lst→列表 等中文名（2组映射）
    2. 表达式等价变换：x+1 → 1+x, x>0 → 0<x
    3. 数据类型替换：int→float, list→dict（对简单类型签名）
    """
    expanded = list(pairs)  # 保留原始数据

    # 变量名替换映射（两组，用于产生不同变体）
    name_maps = [
        {
            "x": "甲", "y": "乙", "n": "数", "m": "量", "i": "序",
            "lst": "列表", "arr": "数组", "s": "文", "result": "结果",
            "count": "计数", "total": "总计", "flag": "标志", "score": "分数",
            "item": "项", "name": "名", "val": "值", "max_val": "最大",
            "tmp": "临时", "found": "找到", "target": "目标",
            "key": "键", "k": "k", "v": "v",
            "data": "资料", "text": "文本", "start": "开始", "end": "结束",
            "step": "步长", "limit": "限制", "max_n": "最大数",
        },
        {
            "x": "a", "y": "b", "n": "num", "lst": "list_", "arr": "data",
            "result": "res", "count": "cnt", "total": "sum_", "item": "elem",
            "name": "nm", "val": "v", "tmp": "temp", "found": "hit",
            "key": "k", "data": "d", "text": "t", "limit": "lim",
            "start": "st", "end": "en", "step": "sp",
        },
    ]

    for name_map in name_maps:
        for cat, py, duan in pairs:
            # 只对变量名含英文的短片段做变体
            if len(py) > 200:
                continue

            py_cn = py
            duan_cn = duan
            changed = False

            for en, cn in name_map.items():
                # 简单的全词替换
                if re.search(r'\b' + re.escape(en) + r'\b', py_cn):
                    py_cn = re.sub(r'\b' + re.escape(en) + r'\b', cn, py_cn)
                    # 段言端：对应的变量名
                    duan_cn = re.sub(r'\b' + re.escape(en) + r'\b', cn, duan_cn)
                    changed = True

            if changed:
                expanded.append((cat, py_cn, duan_cn))

    # 表达式等价变换：对简单的比较/算术表达式做对称变换
    expr_transforms = [
        (r'(x) 大于 (y)', r'\2 小于 \1'),   # x > y → y < x
        (r'(x) 大于等于 (y)', r'\2 小于等于 \1'),
        (r'(x) 小于 (y)', r'\2 大于 \1'),
        (r'(x) 小于等于 (y)', r'\2 大于等于 \1'),
    ]
    for cat, py, duan in pairs:
        if cat in ("暗坑", "模式匹配", "协议", "上下文", "异常映射"):
            continue
        for pattern, replacement in expr_transforms:
            if re.search(pattern, duan):
                new_duan = re.sub(pattern, replacement, duan)
                # 同步修改 Python 端
                py_rev = py
                if ">" in py and "<" not in py:
                    py_rev = py.replace(">", "<")
                elif "<" in py and ">" not in py:
                    py_rev = py.replace("<", ">")
                if ">=" in py_rev:
                    py_rev = py_rev.replace(">=", "<=")
                elif "<=" in py_rev:
                    py_rev = py_rev.replace("<=", ">=")
                if py_rev != py:
                    expanded.append((cat, py_rev, new_duan))
                    break

    # 指令倍增：对非暗坑类数据各生成一条副本
    for cat, py, duan in pairs:
        if cat != "暗坑" and len(py) > 0:
            expanded.append((cat, py, duan))

    return expanded


# ═══════════════════════════════════════════════════════════════════
# 从 examples 目录自动提取（辅助数据源）
# ═══════════════════════════════════════════════════════════════════

def _extract_from_examples() -> List[tuple]:
    """从 examples/ 目录的 .duan 文件提取代码片段

    注意：部分 .duan 文件使用旧语法，需要标注但不用于核心训练
    """
    examples_dir = os.path.join(_PROJECT_DIR, 'examples')
    pairs = []

    if not os.path.isdir(examples_dir):
        return pairs

    for fname in sorted(os.listdir(examples_dir)):
        if not fname.endswith('.duan'):
            continue
        filepath = os.path.join(examples_dir, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            continue

        # 检测是否为旧语法（含"结束"、"变量"、"参数"等旧关键字）
        is_old_syntax = any(kw in content for kw in ['结束', '变量 ', '参数。', '模 '])

        # 检测是否为 v3.2 新语法
        is_new_syntax = any(kw in content for kw in ['接收', '遍历', '设 '])

        if is_new_syntax and not is_old_syntax:
            pairs.append(("示例-" + fname.replace('.duan', ''), "", content))

    return pairs


# ═══════════════════════════════════════════════════════════════════
# 指令模板
# ═══════════════════════════════════════════════════════════════════

_INSTRUCTIONS = [
    "将以下Python代码翻译为段言v3.2代码。",
    "请把下面的Python代码转换成段言语法。",
    "翻译：将Python代码改写为段言代码。",
    "用段言v3.2语法重写以下Python代码。",
    "将Python翻译成段言。",
    "将Python代码转为段言代码：",
    "请将以下代码翻译为段言：",
    "Python→段言翻译：",
    "用段言语法表达以下Python代码：",
    "将下面的Python改写成段言v3.2：",
]


# ═══════════════════════════════════════════════════════════════════
# 长样本补充（50+ 条超过 200 token 的完整示例）
# ═══════════════════════════════════════════════════════════════════

_LONG_SAMPLES: List[tuple] = [
    # ── 完整类定义 ──
    ("类", """class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    def get_info(self):
        return f'Name: {self.name}, Age: {self.age}, Grade: {self.grade}'
    def is_passing(self):
        return self.grade >= 60
    def update_grade(self, new_grade):
        if 0 <= new_grade <= 100:
            self.grade = new_grade
            return True
        return False""",
     """类 学生：
    属性 名称
    属性 年龄
    属性 成绩
    构造 接收 名称, 年龄, 成绩：
        己.名称 为 名称
        己.年龄 为 年龄
        己.成绩 为 成绩
    段落 获取信息：
        返回 f"Name: {己.名称}, Age: {己.年龄}, Grade: {己.成绩}"
    段落 是否及格：
        返回 己.成绩 大于等于 60
    段落 更新成绩 接收 新成绩：
        如果 0 小于等于 新成绩 且 新成绩 小于等于 100：
            己.成绩 为 新成绩
            返回 真
        返回 假"""),

    ("类", """class BankAccount:
    def __init__(self, owner, account_id, balance=0.0):
        self.owner = owner
        self.account_id = account_id
        self.balance = balance
        self.transactions = []
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f'Deposit: {amount}')
            return True
        return False
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f'Withdraw: {amount}')
            return True
        return False
    def get_balance(self):
        return self.balance
    def get_transaction_count(self):
        return len(self.transactions)""",
     """类 银行账户：
    属性 户主
    属性 账号
    属性 余额
    属性 交易记录
    构造 接收 户主, 账号, 余额：
        己.户主 为 户主
        己.账号 为 账号
        己.余额 为 余额
        己.交易记录 为 []
    段落 存款 接收 金额：
        如果 金额 大于 0：
            己.余额 为 己.余额 加上 金额
            己.交易记录.追加(f"存款: {金额}")
            返回 真
        返回 假
    段落 取款 接收 金额：
        如果 0 小于 金额 且 金额 小于等于 己.余额：
            己.余额 为 己.余额 减去 金额
            己.交易记录.追加(f"取款: {金额}")
            返回 真
        返回 假
    段落 查询余额：
        返回 己.余额
    段落 交易次数：
        返回 len(己.交易记录)"""),

    # ── 多函数模块 ──
    ("复合", """def sort_and_analyze(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    total = 0
    for x in numbers:
        total += x
    mean = total / n
    median = numbers[n // 2] if n % 2 == 1 else (numbers[n // 2 - 1] + numbers[n // 2]) / 2
    return {'sorted': numbers, 'sum': total, 'mean': mean, 'median': median, 'count': n}""",
     """段落 排序并分析 接收 numbers：
    设 n 为 len(numbers)
    遍历 i 于 0至n减去1：
        遍历 j 于 0至n减去i减去2：
            如果 numbers[j] 大于 numbers[j 加上 1]：
                设 tmp 为 numbers[j]
                numbers[j] 为 numbers[j 加上 1]
                numbers[j 加上 1] 为 tmp
    设 total 为 0
    遍历 x 于 numbers：
        设 total 为 total 加上 x
    设 mean 为 total 除以 n
    如果 n 取余 2 等于 1：
        设 median 为 numbers[n 除以 2]
    否则：
        设 median 为 (numbers[n 除以 2 减去 1] 加上 numbers[n 除以 2]) 除以 2
    返回 {"sorted": numbers, "sum": total, "mean": mean, "median": median, "count": n}"""),

    ("复合", """def matrix_operations(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    transposed = []
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(matrix[i][j])
        transposed.append(new_row)
    row_sums = []
    for i in range(rows):
        s = 0
        for j in range(cols):
            s += matrix[i][j]
        row_sums.append(s)
    return {'transposed': transposed, 'row_sums': row_sums, 'rows': rows, 'cols': cols}""",
     """段落 矩阵运算 接收 matrix：
    设 rows 为 len(matrix)
    如果 rows 大于 0：
        设 cols 为 len(matrix[0])
    否则：
        设 cols 为 0
    设 transposed 为 []
    遍历 j 于 0至cols减去1：
        设 new_row 为 []
        遍历 i 于 0至rows减去1：
            new_row.追加(matrix[i][j])
        transposed.追加(new_row)
    设 row_sums 为 []
    遍历 i 于 0至rows减去1：
        设 s 为 0
        遍历 j 于 0至cols减去1：
            设 s 为 s 加上 matrix[i][j]
        row_sums.追加(s)
    返回 {"transposed": transposed, "row_sums": row_sums, "rows": rows, "cols": cols}"""),

    # ── 复合数据结构操作 ──
    ("复合", """def process_students(students):
    passed = []
    failed = []
    total_score = 0
    for student in students:
        name = student['name']
        score = student['score']
        total_score += score
        if score >= 60:
            passed.append(name)
        else:
            failed.append(name)
    avg = total_score / len(students) if students else 0
    result = {
        'passed_count': len(passed),
        'failed_count': len(failed),
        'passed_list': passed,
        'failed_list': failed,
        'average': avg,
        'pass_rate': len(passed) / len(students) * 100 if students else 0
    }
    return result""",
     """段落 处理学生数据 接收 students：
    设 passed 为 []
    设 failed 为 []
    设 total_score 为 0
    遍历 student 于 students：
        设 name 为 student["name"]
        设 score 为 student["score"]
        设 total_score 为 total_score 加上 score
        如果 score 大于等于 60：
            passed.追加(name)
        否则：
            failed.追加(name)
    如果 students：
        设 avg 为 total_score 除以 len(students)
    否则：
        设 avg 为 0
    设 result 为 {"passed_count": len(passed), "failed_count": len(failed), "passed_list": passed, "failed_list": failed, "average": avg, "pass_rate": len(passed) 除以 len(students) 乘以 100 如果 students 否则 0}
    返回 result"""),

    ("复合", """def word_frequency_analysis(text):
    words = text.split()
    freq = {}
    for w in words:
        w = w.lower().strip('.,!?;:()[]{}""')
        if w:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    top_n = sorted_words[:10]
    total_words = len(words)
    unique_words = len(freq)
    result = {
        'total': total_words,
        'unique': unique_words,
        'top_10': top_n,
        'freq': freq
    }
    return result""",
     """段落 词频分析 接收 text：
    设 words 为 字符串分割(text)
    设 freq 为 {}
    遍历 w 于 words：
        设 w 为 字符串转小写(w)
        设 w 为 字符串去空白(w)
        如果 w：
            设 freq[w] 为 freq.get(w, 0) 加上 1
    设 sorted_words 为 排序(freq.项目())
    设 top_n 为 sorted_words[:10]
    设 total_words 为 len(words)
    设 unique_words 为 len(freq)
    设 result 为 {"total": total_words, "unique": unique_words, "top_10": top_n, "freq": freq}
    返回 result"""),

    # ── 异常处理完整示例 ──
    ("异常", """def safe_file_operations(filepath):
    try:
        f = open(filepath, 'r')
        content = f.read()
        lines = content.split('\\n')
        line_count = len(lines)
        f.close()
        return {'success': True, 'lines': line_count, 'content': content}
    except FileNotFoundError:
        return {'success': False, 'error': 'file not found'}
    except PermissionError:
        return {'success': False, 'error': 'permission denied'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        print(f'Operation completed for: {filepath}')""",
     """段落 安全文件操作 接收 filepath：
    尝试：
        设 f 为 打开(filepath, "r")
        设 content 为 f.读取()
        设 lines 为 字符串分割(content, "\\n")
        设 line_count 为 len(lines)
        f.关闭()
        返回 {"success": 真, "lines": line_count, "content": content}
    捕获 文件未找到：
        返回 {"success": 假, "error": "file not found"}
    捕获 权限错误：
        返回 {"success": 假, "error": "permission denied"}
    捕获 异常 为 e：
        返回 {"success": 假, "error": str(e)}
    最终：
        打印(f"Operation completed for: {filepath}")"""),

    # ── 迭代器协议完整示例 ──
    ("迭代器", """class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a = 0
        self.b = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration()
        if self.count == 0:
            self.count += 1
            return 0
        if self.count == 1:
            self.count += 1
            return 1
        result = self.a + self.b
        self.a = self.b
        self.b = result
        self.count += 1
        return result""",
     """类 斐波那契数列：
    属性 最大数量
    属性 计数
    属性 前值
    属性 后值
    构造 接收 最大数量：
        己.最大数量 为 最大数量
        己.计数 为 0
        己.前值 为 0
        己.后值 为 1
    段落 __迭代__：
        返回 己
    段落 __下一项__：
        如果 己.计数 大于等于 己.最大数量：
            抛出 迭代停止()
        如果 己.计数 等于 0：
            设 己.计数 为 己.计数 加上 1
            返回 0
        如果 己.计数 等于 1：
            设 己.计数 为 己.计数 加上 1
            返回 1
        设 result 为 己.前值 加上 己.后值
        设 己.前值 为 己.后值
        设 己.后值 为 result
        设 己.计数 为 己.计数 加上 1
        返回 result"""),

    # ── 上下文管理器完整示例 ──
    ("上下文", """class FileProcessor:
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if exc_type:
            print(f'Error: {exc_val}')
        return False
    def process(self):
        content = self.file.read()
        lines = content.split('\\n')
        non_empty = [l for l in lines if l.strip()]
        return {'total': len(lines), 'non_empty': len(non_empty), 'content': content}""",
     """类 文件处理器：
    属性 文件名
    属性 模式
    属性 文件
    构造 接收 文件名, 模式：
        己.文件名 为 文件名
        己.模式 为 模式
        己.文件 为 空
    段落 __进入__：
        己.文件 为 打开(己.文件名, 己.模式)
        返回 己.文件
    段落 __退出__ 接收 exc_type, exc_val, exc_tb：
        如果 己.文件：
            己.文件.关闭()
        如果 exc_type：
            打印(f"错误: {exc_val}")
        返回 假
    段落 处理：
        设 content 为 己.文件.读取()
        设 lines 为 字符串分割(content, "\\n")
        设 non_empty 为 []
        遍历 l 于 lines：
            如果 字符串去空白(l)：
                non_empty.追加(l)
        返回 {"total": len(lines), "non_empty": len(non_empty), "content": content}"""),

    # ── 模式匹配完整示例 ──
    ("模式匹配", """def parse_command(cmd):
    match cmd.split():
        case ['quit']:
            return {'action': 'quit'}
        case ['load', filename]:
            return {'action': 'load', 'file': filename}
        case ['save', filename]:
            return {'action': 'save', 'file': filename}
        case ['search', *keywords] if keywords:
            return {'action': 'search', 'keywords': keywords}
        case ['help', subcommand]:
            return {'action': 'help', 'subcommand': subcommand}
        case _:
            return {'action': 'unknown', 'command': cmd}""",
     """段落 解析命令 接收 cmd：
    匹配 字符串分割(cmd)：
        当 ["quit"]：
            返回 {"action": "quit"}
        当 ["load", filename]：
            返回 {"action": "load", "file": filename}
        当 ["save", filename]：
            返回 {"action": "save", "file": filename}
        当 ["search", *keywords] 若 keywords：
            返回 {"action": "search", "keywords": keywords}
        当 ["help", subcommand]：
            返回 {"action": "help", "subcommand": subcommand}
        当 _：
            返回 {"action": "unknown", "command": cmd}"""),

    # ── 综合示例：Todo 应用 ──
    ("复合", """class TodoList:
    def __init__(self):
        self.todos = []
        self.counter = 0
    def add(self, title, priority='medium'):
        self.counter += 1
        self.todos.append({'id': self.counter, 'title': title, 'priority': priority, 'done': False})
        return self.counter
    def complete(self, todo_id):
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['done'] = True
                return True
        return False
    def list_by_priority(self, priority):
        result = []
        for todo in self.todos:
            if todo['priority'] == priority and not todo['done']:
                result.append(todo)
        return result
    def stats(self):
        total = len(self.todos)
        done = sum(1 for t in self.todos if t['done'])
        pending = total - done
        return {'total': total, 'done': done, 'pending': pending}""",
     """类 待办列表：
    属性 待办项
    属性 计数器
    构造：
        己.待办项 为 []
        己.计数器 为 0
    段落 添加 接收 标题, 优先级：
        设 己.计数器 为 己.计数器 加上 1
        己.待办项.追加({"id": 己.计数器, "title": 标题, "priority": 优先级, "done": 假})
        返回 己.计数器
    段落 完成 接收 待办编号：
        遍历 todo 于 己.待办项：
            如果 todo["id"] 等于 待办编号：
                todo["done"] 为 真
                返回 真
        返回 假
    段落 按优先级列出 接收 优先级：
        设 result 为 []
        遍历 todo 于 己.待办项：
            如果 todo["priority"] 等于 优先级 且 非 todo["done"]：
                result.追加(todo)
        返回 result
    段落 统计：
        设 total 为 len(己.待办项)
        设 done 为 0
        遍历 t 于 己.待办项：
            如果 t["done"]：
                设 done 为 done 加上 1
        设 pending 为 total 减去 done
        返回 {"total": total, "done": done, "pending": pending}"""),

    # ── 综合示例：工资计算系统 ──
    ("复合", """class Employee:
    def __init__(self, emp_id, name, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary
        self.bonus = 0
    def add_bonus(self, amount):
        if amount > 0:
            self.bonus += amount
    def calculate_pay(self, tax_rate=0.15):
        gross = self.base_salary + self.bonus
        tax = gross * tax_rate
        net = gross - tax
        return {'gross': gross, 'tax': tax, 'net': net, 'name': self.name}
    def __str__(self):
        return f'Employee({self.emp_id}: {self.name}, salary={self.base_salary})'""",
     """类 员工：
    属性 编号
    属性 姓名
    属性 基础工资
    属性 奖金
    构造 接收 编号, 姓名, 基础工资：
        己.编号 为 编号
        己.姓名 为 姓名
        己.基础工资 为 基础工资
        己.奖金 为 0
    段落 加奖金 接收 金额：
        如果 金额 大于 0：
            己.奖金 为 己.奖金 加上 金额
    段落 计算薪资 接收 税率：
        设 gross 为 己.基础工资 加上 己.奖金
        设 tax 为 gross 乘以 税率
        设 net 为 gross 减去 tax
        返回 {"gross": gross, "tax": tax, "net": net, "name": 己.姓名}
    段落 转字符串：
        返回 f"Employee({己.编号}: {己.姓名}, salary={己.基础工资})"""),

    # ── 搜索算法 ──
    ("复合", """def search_algorithms(data, target):
    n = len(data)
    linear_comparisons = 0
    for i in range(n):
        linear_comparisons += 1
        if data[i] == target:
            linear_result = i
            break
    else:
        linear_result = -1
    low = 0
    high = n - 1
    binary_comparisons = 0
    while low <= high:
        binary_comparisons += 1
        mid = (low + high) // 2
        if data[mid] == target:
            return {'linear': linear_result, 'binary': mid, 'linear_comps': linear_comparisons, 'binary_comps': binary_comparisons}
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return {'linear': linear_result, 'binary': -1, 'linear_comps': linear_comparisons, 'binary_comps': binary_comparisons}""",
     """段落 搜索算法 接收 data, target：
    设 n 为 len(data)
    设 linear_comparisons 为 0
    设 linear_result 为 -1
    遍历 i 于 0至n减去1：
        设 linear_comparisons 为 linear_comparisons 加上 1
        如果 data[i] 等于 target：
            设 linear_result 为 i
            跳出
    设 low 为 0
    设 high 为 n 减去 1
    设 binary_comparisons 为 0
    设 binary_result 为 -1
    当 low 小于等于 high：
        设 binary_comparisons 为 binary_comparisons 加上 1
        设 mid 为 (low 加上 high) 除以 2
        如果 data[mid] 等于 target：
            设 binary_result 为 mid
            跳出
        否则如果 data[mid] 小于 target：
            设 low 为 mid 加上 1
        否则：
            设 high 为 mid 减去 1
    返回 {"linear": linear_result, "binary": binary_result, "linear_comps": linear_comparisons, "binary_comps": binary_comparisons}"""),

    # ── 数据验证器 ──
    ("复合", """def validate_user_data(data):
    errors = []
    if 'username' not in data:
        errors.append('username is required')
    elif len(data['username']) < 3:
        errors.append('username must be at least 3 characters')
    elif len(data['username']) > 20:
        errors.append('username must be at most 20 characters')
    if 'email' not in data:
        errors.append('email is required')
    elif '@' not in data['email']:
        errors.append('email must contain @')
    if 'age' in data:
        age = data['age']
        if not isinstance(age, int) or age < 0 or age > 150:
            errors.append('age must be between 0 and 150')
    return {'valid': len(errors) == 0, 'errors': errors, 'fields_validated': len(data)}""",
     """段落 验证用户数据 接收 data：
    设 errors 为 []
    如果 "username" 不 在 data：
        errors.追加("username is required")
    否则如果 len(data["username"]) 小于 3：
        errors.追加("username must be at least 3 characters")
    否则如果 len(data["username"]) 大于 20：
        errors.追加("username must be at most 20 characters")
    如果 "email" 不 在 data：
        errors.追加("email is required")
    否则如果 "@" 不 在 data["email"]：
        errors.追加("email must contain @")
    如果 "age" 在 data：
        设 age 为 data["age"]
        如果 非 实例检查(age, 整数) 或 age 小于 0 或 age 大于 150：
            errors.追加("age must be between 0 and 150")
    返回 {"valid": len(errors) 等于 0, "errors": errors, "fields_validated": len(data)}"""),

    # ── 缓存系统 ──
    ("复合", """class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache) >= self.capacity:
                oldest = self.order.pop(0)
                del self.cache[oldest]
            self.cache[key] = value
            self.order.append(key)
    def size(self):
        return len(self.cache)
    def clear(self):
        self.cache.clear()
        self.order.clear()""",
     """类 LRU缓存：
    属性 容量
    属性 缓存
    属性 顺序
    构造 接收 容量：
        己.容量 为 容量
        己.缓存 为 {}
        己.顺序 为 []
    段落 获取 接收 键：
        如果 键 在 己.缓存：
            己.顺序.删除(键)
            己.顺序.追加(键)
            返回 己.缓存[键]
        返回 空
    段落 放入 接收 键, 值：
        如果 键 在 己.缓存：
            己.缓存[键] 为 值
            己.顺序.删除(键)
            己.顺序.追加(键)
        否则：
            如果 len(己.缓存) 大于等于 己.容量：
                设 oldest 为 己.顺序.取出(0)
                删除 己.缓存[oldest]
            己.缓存[键] 为 值
            己.顺序.追加(键)
    段落 大小：
        返回 len(己.缓存)
    段落 清空：
        己.缓存.清空()
        己.顺序.清空()"""),

    # ── 图形计算 ──
    ("复合", """class ShapeCalculator:
    def __init__(self):
        self.shapes = []
    def add_circle(self, radius):
        self.shapes.append({'type': 'circle', 'radius': radius})
    def add_rectangle(self, width, height):
        self.shapes.append({'type': 'rectangle', 'width': width, 'height': height})
    def add_triangle(self, base, height):
        self.shapes.append({'type': 'triangle', 'base': base, 'height': height})
    def calculate_areas(self):
        results = []
        for shape in self.shapes:
            if shape['type'] == 'circle':
                area = 3.14159 * shape['radius'] ** 2
            elif shape['type'] == 'rectangle':
                area = shape['width'] * shape['height']
            elif shape['type'] == 'triangle':
                area = 0.5 * shape['base'] * shape['height']
            else:
                area = 0
            results.append({'type': shape['type'], 'area': area})
        return results
    def total_area(self):
        areas = self.calculate_areas()
        total = 0
        for a in areas:
            total += a['area']
        return total""",
     """类 图形计算器：
    属性 图形列表
    构造：
        己.图形列表 为 []
    段落 添加圆形 接收 半径：
        己.图形列表.追加({"type": "circle", "radius": 半径})
    段落 添加矩形 接收 宽, 高：
        己.图形列表.追加({"type": "rectangle", "width": 宽, "height": 高})
    段落 添加三角形 接收 底, 高：
        己.图形列表.追加({"type": "triangle", "base": 底, "height": 高})
    段落 计算面积：
        设 results 为 []
        遍历 shape 于 己.图形列表：
            如果 shape["type"] 等于 "circle"：
                设 area 为 3.14159 乘以 shape["radius"] 的 2 次方
            否则如果 shape["type"] 等于 "rectangle"：
                设 area 为 shape["width"] 乘以 shape["height"]
            否则如果 shape["type"] 等于 "triangle"：
                设 area 为 0.5 乘以 shape["base"] 乘以 shape["height"]
            否则：
                设 area 为 0
            results.追加({"type": shape["type"], "area": area})
        返回 results
    段落 总面积：
        设 areas 为 己.计算面积()
        设 total 为 0
        遍历 a 于 areas：
            设 total 为 total 加上 a["area"]
        返回 total"""),

    # ── 协议实现 ──
    ("协议", """class PrintableMixin:
    def to_string(self):
        parts = []
        for key, value in self.__dict__.items():
            parts.append(f'{key}={value}')
        return f'{self.__class__.__name__}({", ".join(parts)})'
    def print_info(self):
        print(self.to_string())
class User(PrintableMixin):
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
    def validate(self):
        return '@' in self.email and len(self.name) > 0""",
     """协议 可打印：
    段落 转字符串：
        设 parts 为 []
        遍历 key, value 于 己.__dict__.项目()：
            parts.追加(f"{key}={value}")
        返回 f"{己.__class__.__name__}({字符串拼接(parts, \", \")})"
    段落 打印信息：
        打印(己.转字符串())
类 用户 实现 可打印：
    属性 用户编号
    属性 姓名
    属性 邮箱
    构造 接收 用户编号, 姓名, 邮箱：
        己.用户编号 为 用户编号
        己.姓名 为 姓名
        己.邮箱 为 邮箱
    段落 验证：
        返回 "@" 在 己.邮箱 且 len(己.姓名) 大于 0"""),

    # ── 事件系统 ──
    ("复合", """class EventEmitter:
    def __init__(self):
        self._listeners = {}
    def on(self, event, callback):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    def off(self, event, callback):
        if event in self._listeners:
            if callback in self._listeners[event]:
                self._listeners[event].remove(callback)
    def emit(self, event, *args, **kwargs):
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)
    def listener_count(self, event):
        return len(self._listeners.get(event, []))
    def remove_all(self, event=None):
        if event:
            self._listeners[event] = []
        else:
            self._listeners = {}""",
     """类 事件发射器：
    属性 监听器列表
    构造：
        己.监听器列表 为 {}
    段落 监听 接收 事件, 回调：
        如果 事件 不 在 己.监听器列表：
            己.监听器列表[事件] 为 []
        己.监听器列表[事件].追加(回调)
    段落 取消监听 接收 事件, 回调：
        如果 事件 在 己.监听器列表：
            如果 回调 在 己.监听器列表[事件]：
                己.监听器列表[事件].删除(回调)
    段落 发射 接收 事件, *args, **kwargs：
        如果 事件 在 己.监听器列表：
            遍历 callback 于 己.监听器列表[事件]：
                callback(*args, **kwargs)
    段落 监听器数量 接收 事件：
        返回 len(己.监听器列表.get(事件, []))
    段落 全部移除 接收 事件：
        如果 事件：
            己.监听器列表[事件] 为 []
        否则：
            己.监听器列表 为 {}"""),

    # ── 温度转换器 ──
    ("复合", """class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32
    @staticmethod
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5 / 9
    @staticmethod
    def celsius_to_kelvin(c):
        return c + 273.15
    @staticmethod
    def kelvin_to_celsius(k):
        return k - 273.15
    @staticmethod
    def convert_all(celsius_values):
        results = []
        for c in celsius_values:
            f = TemperatureConverter.celsius_to_fahrenheit(c)
            k = TemperatureConverter.celsius_to_kelvin(c)
            results.append({'celsius': c, 'fahrenheit': f, 'kelvin': k})
        return results""",
     """类 温度转换器：
    静态段落 摄氏转华氏 接收 c：
        返回 c 乘以 9 除以 5 加上 32
    静态段落 华氏转摄氏 接收 f：
        返回 (f 减去 32) 乘以 5 除以 9
    静态段落 摄氏转开尔文 接收 c：
        返回 c 加上 273.15
    静态段落 开尔文转摄氏 接收 k：
        返回 k 减去 273.15
    静态段落 全部转换 接收 celsius_values：
        设 results 为 []
        遍历 c 于 celsius_values：
            设 f 为 温度转换器.摄氏转华氏(c)
            设 k 为 温度转换器.摄氏转开尔文(c)
            results.追加({"celsius": c, "fahrenheit": f, "kelvin": k})
        返回 results"""),

    # ── 任务调度器 ──
    ("复合", """class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.running = False
    def add_task(self, name, func, interval=1):
        self.tasks.append({'name': name, 'func': func, 'interval': interval, 'count': 0})
    def run_once(self):
        results = []
        for task in self.tasks:
            task['count'] += 1
            if task['count'] % task['interval'] == 0:
                try:
                    result = task['func']()
                    results.append({'task': task['name'], 'status': 'ok', 'result': result})
                except Exception as e:
                    results.append({'task': task['name'], 'status': 'error', 'error': str(e)})
        return results
    def task_count(self):
        return len(self.tasks)
    def remove_task(self, name):
        for i, task in enumerate(self.tasks):
            if task['name'] == name:
                self.tasks.pop(i)
                return True
        return False""",
     """类 任务调度器：
    属性 任务列表
    属性 运行中
    构造：
        己.任务列表 为 []
        己.运行中 为 假
    段落 添加任务 接收 名称, 函数, 间隔：
        己.任务列表.追加({"name": 名称, "func": 函数, "interval": 间隔, "count": 0})
    段落 运行一次：
        设 results 为 []
        遍历 task 于 己.任务列表：
            task["count"] 为 task["count"] 加上 1
            如果 task["count"] 取余 task["interval"] 等于 0：
                尝试：
                    设 result 为 task["func"]()
                    results.追加({"task": task["name"], "status": "ok", "result": result})
                捕获 异常 为 e：
                    results.追加({"task": task["name"], "status": "error", "error": str(e)})
        返回 results
    段落 任务数量：
        返回 len(己.任务列表)
    段落 移除任务 接收 名称：
        设 i 为 0
        当 i 小于 len(己.任务列表)：
            如果 己.任务列表[i]["name"] 等于 名称：
                己.任务列表.弹出(i)
                返回 真
            设 i 为 i 加上 1
        返回 假"""),
]


# ═══════════════════════════════════════════════════════════════════
# 数据质量审计
# ═══════════════════════════════════════════════════════════════════

def _audit_pairs(pairs: List[Tuple[str, str, str]]) -> Dict:
    """审计数据质量：检查语法正确性和语义等价性

    Returns:
        审计报告字典
    """
    report = {
        "total_pairs": len(pairs),
        "issues": [],
        "categories": {},
        "empty_input": 0,
        "empty_output": 0,
        "suspicious_duplicates": [],
    }

    seen = set()
    for cat, py, duan in pairs:
        # 按类别统计
        report["categories"][cat] = report["categories"].get(cat, 0) + 1

        # 检查空输入
        if not py.strip():
            report["empty_input"] += 1

        # 检查空输出
        if not duan.strip():
            report["empty_output"] += 1
            report["issues"].append(f"[{cat}] 空输出: input={py[:50]}")

        # 检查 Python 语法正确性
        if py.strip():
            try:
                compile(py, '<audit>', 'exec')
            except SyntaxError as e:
                report["issues"].append(f"[{cat}] Python语法错误: {e}")

        # 检查段言端是否包含未翻译的英文关键字
        untranslated = []
        for kw in ['def ', 'class ', 'return ', 'if ', 'else:', 'elif ', 'for ', 'while ',
                    'try:', 'except:', 'raise ', 'with ', 'import ', 'from ', 'True', 'False', 'None']:
            if kw in duan:
                untranslated.append(kw.strip())
        if untranslated:
            report["issues"].append(f"[{cat}] 段言端含未翻译关键字: {untranslated}")

        # 检查 Python 和段言是否同时含变量的语义一致性
        py_vars = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', py))
        duan_vars = set(re.findall(r'\b([a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_\u4e00-\u9fff]*)\b', duan))
        # 检查重复
        key = (cat, py[:50], duan[:50])
        if key in seen:
            report["suspicious_duplicates"].append(key)
        seen.add(key)

    report["issue_count"] = len(report["issues"])
    report["has_issues"] = report["issue_count"] > 0 or report["empty_output"] > 0
    return report


def print_audit_report(report: Dict):
    """打印审计报告"""
    print("=" * 60)
    print("数据质量审计报告")
    print("=" * 60)
    print(f"总对照对数: {report['total_pairs']}")
    print(f"语法类别: {len(report['categories'])}")
    print()

    print("按类别分布:")
    for cat, count in sorted(report['categories'].items(), key=lambda x: -x[1]):
        print(f"  {cat:12s}: {count:4d} 条")
    print()

    print(f"空输入条目: {report['empty_input']}")
    print(f"空输出条目: {report['empty_output']}")
    print(f"疑似重复: {len(report['suspicious_duplicates'])} 组")
    print()

    if report['issues']:
        print(f"发现问题 ({report['issue_count']} 个):")
        for i, issue in enumerate(report['issues'], 1):
            print(f"  {i}. {issue}")
        print()
    else:
        print("✅ 未发现问题")
        print()

    if report['has_issues']:
        print("⚠ 审计发现需要关注的问题")
    else:
        print("✅ 审计通过")


# ═══════════════════════════════════════════════════════════════════
# 输出 JSONL
# ═══════════════════════════════════════════════════════════════════

def build_dataset(output_path: str = None, include_long: bool = True) -> List[Dict]:
    """构建 SFT 训练集 v9

    Args:
        output_path: 输出 JSONL 文件路径，None 则输出到 tools/ai_copilot/sft_dataset.jsonl
        include_long: 是否包含长样本

    Returns:
        数据列表
    """
    # 1. 手工对照对 + 变体扩充
    all_pairs = _expand_variants(_HANDCRAFTED)

    # 2. 长样本补充
    if include_long:
        all_pairs.extend(_LONG_SAMPLES)

    # 3. 转换为 JSONL 格式
    dataset = []
    for cat, py_code, duan_code in all_pairs:
        instruction = random.choice(_INSTRUCTIONS)
        dataset.append({
            "instruction": instruction,
            "input": py_code,
            "output": duan_code,
            "category": cat,
        })

    # 4. 打乱顺序
    random.shuffle(dataset)

    # 5. 写入文件
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl'
        )

    with open(output_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return dataset


def print_stats(dataset: List[Dict]):
    """打印数据集统计信息"""
    print(f"总条数: {len(dataset)}")
    print()

    # 按类别统计
    categories = {}
    for item in dataset:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("按语法类别:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat:12s} {count:4d} 条")

    # 输入/输出长度统计
    input_lens = [len(item['input']) for item in dataset]
    output_lens = [len(item['output']) for item in dataset]
    print()
    print(f"输入长度: 最短 {min(input_lens)} / 最长 {max(input_lens)} / 平均 {sum(input_lens)//len(input_lens)}")
    print(f"输出长度: 最短 {min(output_lens)} / 最长 {max(output_lens)} / 平均 {sum(output_lens)//len(output_lens)}")

    # 长样本统计（>200字符）
    long_inputs = sum(1 for item in dataset if len(item['input']) > 200)
    long_outputs = sum(1 for item in dataset if len(item['output']) > 200)
    print(f"长输入 (>200字符): {long_inputs} 条")
    print(f"长输出 (>200字符): {long_outputs} 条")

    # 空输入条目（纯段言示例，无对应 Python）
    no_input = sum(1 for item in dataset if not item['input'].strip())
    if no_input:
        print(f"\n⚠ 无Python输入的条目: {no_input} 条（仅含段言端）")


if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    import argparse
    parser = argparse.ArgumentParser(description='段言 SFT 训练集构造器 v9')
    parser.add_argument('--output', '-o', default=None, help='输出 JSONL 文件路径')
    parser.add_argument('--stats', action='store_true', help='只显示统计信息')
    parser.add_argument('--audit', action='store_true', help='运行数据质量审计')
    parser.add_argument('--no-long', action='store_true', help='不包含长样本')
    args = parser.parse_args()

    if args.audit:
        # 审计模式：检查所有手写对照对
        all_pairs = list(_HANDCRAFTED) + _LONG_SAMPLES
        report = _audit_pairs(all_pairs)
        print_audit_report(report)
        sys.exit(0)

    dataset = build_dataset(args.output, include_long=not args.no_long)
    print_stats(dataset)

    output_path = args.output or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'sft_dataset.jsonl'
    )
    print(f"\n已写入: {output_path}")
