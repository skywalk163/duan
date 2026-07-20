#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言数据增强脚本 — 从 .duan 示例文件和 Python 对照中提取更多训练对

策略：
  1. 从 examples/ 和 benchmarks/ 的 .duan 文件中提取段言代码片段
  2. 为每个段言片段构造对应的 Python 等价代码
  3. 从段言语法规则中生成更多对照对（边界情况、特殊语法）
  4. 合并到 sft_dataset.jsonl

输出：sft_dataset_enhanced.jsonl
"""

import json
import os
import re
import random

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_SCRIPT_DIR))
_DATASET_PATH = os.path.join(_SCRIPT_DIR, "sft_dataset.jsonl")
_OUTPUT_PATH = os.path.join(_SCRIPT_DIR, "sft_dataset_enhanced.jsonl")

# ── 手工构造的高质量 Python→段言 对照对 ──
# 涵盖 examples/ 中的实际代码和更多边界情况
ENHANCED_PAIRS = [
    # ── 冒泡排序（来自 benchmarks/programs/bubble_sort.duan）──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "arr = [64, 34, 25, 12, 22, 11, 90]\nn = len(arr)\nfor i in range(n - 1):\n    for j in range(n - i - 1):\n        if arr[j] > arr[j + 1]:\n            arr[j], arr[j + 1] = arr[j + 1], arr[j]\nfor item in arr:\n    print(item)",
        "output": "设 列表 为 [64, 34, 25, 12, 22, 11, 90]\n设 长度 为 len(列表)\n\n设 i 为 0\n遍历 i 于 0至 长度 减 2：\n  设 j 为 0\n  遍历 j 于 0至 长度 减 i 减 2：\n    如果 列表[j] 大于 列表[j 加 1]：\n      设 临时 为 列表[j]\n      列表[j] = 列表[j 加 1]\n      列表[j 加 1] = 临时\n\n遍历 元素 于 列表：\n  打印(元素)",
        "category": "复合",
    },
    # ── 斐波那契（来自 benchmarks/programs/fibonacci.duan）──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nresult = fib(20)\nprint(result)",
        "output": "段落 斐波那契 接收 n：\n  如果 n 小于 2：\n    返回 n\n  返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)\n\n设 结果 为 斐波那契(20)\n打印(结果)",
        "category": "段落",
    },
    # ── 汉诺塔（来自 examples/hanoi.duan）──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def hanoi(n, src, dst, aux):\n    if n == 1:\n        print(f'移动盘子 1 从 {src} 到 {dst}')\n    else:\n        hanoi(n - 1, src, aux, dst)\n        print(f'移动盘子 {n} 从 {src} 到 {dst}')\n        hanoi(n - 1, aux, dst, src)\n\nhanoi(3, 'A', 'C', 'B')",
        "output": "段落 汉诺塔 接收 层数, 源柱, 目标柱, 辅助柱：\n  如果 层数 等于 1：\n    打印(\"移动盘子 1 从 \" 加 源柱 加 \" 到 \" 加 目标柱)\n  否则：\n    汉诺塔(层数 减 1, 源柱, 辅助柱, 目标柱)\n    打印(\"移动盘子 \" 加 转字符串(层数) 加 \" 从 \" 加 源柱 加 \" 到 \" 加 目标柱)\n    汉诺塔(层数 减 1, 辅助柱, 目标柱, 源柱)\n\n汉诺塔(3, \"A\", \"C\", \"B\")",
        "category": "段落",
    },
    # ── 计算器类（来自 examples/calculator.duan）──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "class Calculator:\n    def __init__(self):\n        self.result = 0\n    def add(self, x):\n        self.result += x\n    def sub(self, x):\n        self.result -= x\n    def mul(self, x):\n        self.result *= x\n    def div(self, x):\n        if x != 0:\n            self.result /= x\n    def clear(self):\n        self.result = 0\n    def get_result(self):\n        return self.result\n\ncalc = Calculator()\ncalc.add(10)\ncalc.mul(2)\nprint(calc.get_result())",
        "output": "类 计算器：\n  设 结果 为 0\n\n  段落 加 接收 x：\n    设 结果 为 结果 加 x\n\n  段落 减 接收 x：\n    设 结果 为 结果 减 x\n\n  段落 乘 接收 x：\n    设 结果 为 结果 乘 x\n\n  段落 除 接收 x：\n    如果 x 不等于 0：\n      设 结果 为 结果 除以 x\n\n  段落 清零：\n    设 结果 为 0\n\n  段落 获取结果：\n    返回 结果\n\n设计算器1为计算器()\n计算器1.加(10)\n计算器1.乘(2)\n打印(计算器1.获取结果())",
        "category": "类",
    },
    # ── 基础语法演示（来自 examples/basic.duan）──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "a = 123\nb = 3 + 5\nprint(a)\nprint(b)\nresult = a + b * 2\nprint(result)\nif a > b:\n    print('a大于b')\nelse:\n    print('a小于等于b')",
        "output": "设 甲 为 123\n设 乙 为 3 加 5\n打印(甲)\n打印(乙)\n设 结果 为 甲 加 乙 乘 2\n打印(结果)\n如果 甲 大于 乙：\n  打印(\"a大于b\")\n否则：\n  打印(\"a小于等于b\")",
        "category": "变量",
    },
    # ── 阶乘递归 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nresult = factorial(5)\nprint(f'阶乘(5) = {result}')",
        "output": "段落 阶乘 接收 数：\n  如果 数 小于等于 1：\n    返回 1\n  返回 数 乘 阶乘(数 减 1)\n\n设 阶乘结果 为 阶乘(5)\n打印(f\"阶乘(5) = {阶乘结果}\")",
        "category": "段落",
    },
    # ── 加法段落 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def add(a, b):\n    return a + b\n\ns = add(3, 5)\nprint(s)",
        "output": "段落 加法 接收 甲, 乙：\n  返回 甲 加 乙\n\n设 和 为 加法(3, 5)\n打印(和)",
        "category": "段落",
    },
    # ── while循环 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "count = 0\nwhile count < 10:\n    print(count)\n    count += 1",
        "output": "设 计数 为 0\n当 计数 小于 10：\n  打印(计数)\n  设 计数 为 计数 加 1",
        "category": "循环",
    },
    # ── 列表操作 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "nums = [1, 2, 3, 4, 5]\ntotal = 0\nfor n in nums:\n    total += n\nprint(f'总和: {total}')\nprint(f'平均: {total / len(nums)}')",
        "output": "设 数字列表 为 [1, 2, 3, 4, 5]\n设 总和 为 0\n遍历 n 于 数字列表：\n  设 总和 为 总和 加 n\n打印(f\"总和: {总和}\")\n打印(f\"平均: {总和 除以 len(数字列表)}\")",
        "category": "列表",
    },
    # ── 字典操作 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "scores = {'语文': 90, '数学': 85, '英语': 95}\nfor subject, score in scores.items():\n    print(f'{subject}: {score}')\ntotal = sum(scores.values())\nprint(f'总分: {total}')",
        "output": "设 成绩 为 {\"语文\": 90, \"数学\": 85, \"英语\": 95}\n遍历 科目, 分数 于 成绩.项目()：\n  打印(f\"{科目}: {分数}\")\n设 总分 为 0\n遍历 分数 于 成绩.值()：\n  设 总分 为 总分 加 分数\n打印(f\"总分: {总分}\")",
        "category": "字典",
    },
    # ── 异常处理 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f'错误: {e}')\nfinally:\n    print('计算结束')",
        "output": "尝试：\n  设 结果 为 10 除以 0\n捕获 异常：\n  打印(\"错误: 除数不能为零\")\n打印(\"计算结束\")",
        "category": "异常",
    },
    # ── 字符串操作 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "name = '世界'\ngreeting = f'你好, {name}!'\nprint(greeting)\nprint(greeting.upper())\nprint(len(greeting))",
        "output": "定义 名字 等于 \"世界\"\n定义 问候 等于 f\"你好, {名字}!\"\n打印(问候)\n打印(问候.大写())\n打印(len(问候))",
        "category": "字符串",
    },
    # ── 条件链 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "score = 85\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelif score >= 70:\n    grade = 'C'\nelif score >= 60:\n    grade = 'D'\nelse:\n    grade = 'F'\nprint(f'等级: {grade}')",
        "output": "设 分数 为 85\n如果 分数 大于等于 90：\n  设 等级 为 \"A\"\n否则如果 分数 大于等于 80：\n  设 等级 为 \"B\"\n否则如果 分数 大于等于 70：\n  设 等级 为 \"C\"\n否则如果 分数 大于等于 60：\n  设 等级 为 \"D\"\n否则：\n  设 等级 为 \"F\"\n打印(f\"等级: {等级}\")",
        "category": "条件",
    },
    # ── 嵌套循环+break ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "for i in range(1, 10):\n    for j in range(1, 10):\n        if i * j > 50:\n            break\n        print(f'{i}x{j}={i*j}', end=' ')\n    print()",
        "output": "遍历 i 于 1至 9：\n  遍历 j 于 1至 9：\n    如果 i 乘 j 大于 50：\n      跳出\n    打印(f\"{i}x{j}={i 乘 j}\")\n  打印(\"\")",
        "category": "循环",
    },
    # ── 列表推导式 → 遍历 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "squares = [x**2 for x in range(1, 11)]\nprint(squares)\nevens = [x for x in squares if x % 2 == 0]\nprint(evens)",
        "output": "设 平方列表 为 []\n遍历 x 于 1至 10：\n  平方列表.追加(x 乘 x)\n打印(平方列表)\n\n设 偶数列表 为 []\n遍历 x 于 平方列表：\n  如果 x 取余 2 等于 0：\n    偶数列表.追加(x)\n打印(偶数列表)",
        "category": "列表",
    },
    # ── 布尔逻辑 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "x = True\ny = False\nz = x and (not y or x)\nprint(z)\nif x and not y:\n    print('条件成立')",
        "output": "设 x 为 真\n设 y 为 假\n设 z 为 x 且 (非 y 或 x)\n打印(z)\n如果 x 且 非 y：\n  打印(\"条件成立\")",
        "category": "变量",
    },
    # ── 模块导入 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "from math_utils import add, multiply\nfrom string_utils import concat\n\nresult = add(3, 5)\ntext = concat('hello', 'world')\nprint(result, text)",
        "output": "从 数学工具 导入 加法, 乘法\n从 字符串工具 导入 连接\n\n设 结果 为 加法(3, 5)\n设 文本 为 连接(\"hello\", \"world\")\n打印(结果)\n打印(文本)",
        "category": "导入",
    },
    # ── 学生管理 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "class Student:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def greet(self):\n        return f'我是{self.name}, 今年{self.age}岁'\n\nstudents = [Student('张三', 18), Student('李四', 20)]\nfor s in students:\n    print(s.greet())",
        "output": "类 学生：\n  构造 接收 姓名, 年龄：\n    己.姓名 为 姓名\n    己.年龄 为 年龄\n\n  段落 问候：\n    返回 f\"我是{己.姓名}, 今年{己.年龄}岁\"\n\n设 学生列表 为 [新建学生(\"张三\", 18), 新建学生(\"李四\", 20)]\n遍历 s 于 学生列表：\n  打印(s.问候())",
        "category": "类",
    },
    # ── 二分查找 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
        "output": "段落 二分查找 接收 列表, 目标：\n  设 左 为 0\n  设 右 为 len(列表) 减 1\n  当 左 小于等于 右：\n    设 中 为 (左 加 右) 除以 2\n    如果 列表[中] 等于 目标：\n      返回 中\n    否则如果 列表[中] 小于 目标：\n      设 左 为 中 加 1\n    否则：\n      设 右 为 中 减 1\n  返回 -1",
        "category": "复合",
    },
    # ── 选择排序 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n - 1):\n        min_idx = i\n        for j in range(i + 1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr",
        "output": "段落 选择排序 接收 列表：\n  设 长度 为 len(列表)\n  遍历 i 于 0至 长度 减 2：\n    设 最小索引 为 i\n    遍历 j 于 i 加 1至 长度 减 1：\n      如果 列表[j] 小于 列表[最小索引]：\n        设 最小索引 为 j\n    设 临时 为 列表[i]\n    列表[i] = 列表[最小索引]\n    列表[最小索引] = 临时\n  返回 列表",
        "category": "复合",
    },
    # ── 线性搜索 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def linear_search(arr, target):\n    for i in range(len(arr)):\n        if arr[i] == target:\n            return i\n    return -1\n\nresult = linear_search([3, 1, 4, 1, 5, 9], 5)\nprint(result)",
        "output": "段落 线性查找 接收 列表, 目标：\n  遍历 i 于 0至 len(列表) 减 1：\n    如果 列表[i] 等于 目标：\n      返回 i\n  返回 -1\n\n设 结果 为 线性查找([3, 1, 4, 1, 5, 9], 5)\n打印(结果)",
        "category": "复合",
    },
    # ── 回文检测 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "def is_palindrome(s):\n    s = s.lower()\n    return s == s[::-1]\n\nprint(is_palindrome('racecar'))\nprint(is_palindrome('hello'))",
        "output": "段落 是否回文 接收 文本：\n  设 文本 为 文本.小写()\n  设 反转 为 文本[::-1]\n  返回 文本 等于 反转\n\n打印(是否回文(\"racecar\"))\n打印(是否回文(\"hello\"))",
        "category": "字符串",
    },
    # ── 计数器 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "text = 'hello world hello python world'\nwords = text.split()\ncounts = {}\nfor word in words:\n    if word in counts:\n        counts[word] += 1\n    else:\n        counts[word] = 1\nfor word, count in sorted(counts.items()):\n    print(f'{word}: {count}')",
        "output": "定义 文本 等于 \"hello world hello python world\"\n设 词语列表 为 文本.分割()\n设 计数 为 {}\n遍历 词语 于 词语列表：\n  如果 词语 在 计数：\n    设 计数[词语] 为 计数[词语] 加 1\n  否则：\n    设 计数[词语] 为 1\n遍历 词语, 次数 于 计数.项目()：\n  打印(f\"{词语}: {次数}\")",
        "category": "字典",
    },
    # ── GCD最大公约数 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\nresult = gcd(48, 36)\nprint(f'GCD: {result}')",
        "output": "段落 最大公约数 接收 a, b：\n  当 b 不等于 0：\n    设 临时 为 a\n    设 a 为 b\n    设 b 为 临时 取余 b\n  返回 a\n\n设 结果 为 最大公约数(48, 36)\n打印(f\"GCD: {结果}\")",
        "category": "复合",
    },
    # ── 矩阵转置 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\ntransposed = []\nfor i in range(len(matrix[0])):\n    row = []\n    for j in range(len(matrix)):\n        row.append(matrix[j][i])\n    transposed.append(row)\nprint(transposed)",
        "output": "设 矩阵 为 [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n设 转置 为 []\n遍历 i 于 0至 len(矩阵[0]) 减 1：\n  设 行 为 []\n  遍历 j 于 0至 len(矩阵) 减 1：\n    行.追加(矩阵[j][i])\n  转置.追加(行)\n打印(转置)",
        "category": "列表",
    },
    # ── 类继承 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        pass\n\nclass Dog(Animal):\n    def speak(self):\n        return f'{self.name} says Woof!'\n\nd = Dog('Buddy')\nprint(d.speak())",
        "output": "类 动物：\n  构造 接收 名字：\n    己.名字 为 名字\n  段落 发声：\n    返回 空\n\n类 狗(动物)：\n  段落 发声：\n    返回 f\"{己.名字} says Woof!\"\n\n设 d 为 新建狗(\"Buddy\")\n打印(d.发声())",
        "category": "类",
    },
    # ── continue跳过 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "for i in range(1, 21):\n    if i % 3 == 0:\n        continue\n    if i % 5 == 0:\n        break\n    print(i)",
        "output": "遍历 i 于 1至 20：\n  如果 i 取余 3 等于 0：\n    跳过\n  如果 i 取余 5 等于 0：\n    跳出\n  打印(i)",
        "category": "循环",
    },
    # ── 多条件组合 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "age = 25\nhas_license = True\nif age >= 18 and has_license:\n    print('可以驾驶')\nelif age >= 18 and not has_license:\n    print('需要考驾照')\nelse:\n    print('未成年')",
        "output": "设 年龄 为 25\n设 有驾照 为 真\n如果 年龄 大于等于 18 且 有驾照：\n  打印(\"可以驾驶\")\n否则如果 年龄 大于等于 18 且 非 有驾照：\n  打印(\"需要考驾照\")\n否则：\n  打印(\"未成年\")",
        "category": "条件",
    },
    # ── f-string格式化 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "name = '张三'\nage = 25\nheight = 1.75\nprint(f'姓名: {name}, 年龄: {age}岁, 身高: {height:.2f}米')",
        "output": "定义 姓名 等于 \"张三\"\n设 年龄 为 25\n设 身高 为 1.75\n打印(f\"姓名: {姓名}, 年龄: {年龄}岁, 身高: {身高:.2f}米\")",
        "category": "字符串",
    },
    # ── try-except嵌套 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "try:\n    nums = [1, 2, 3]\n    print(nums[5])\nexcept IndexError:\n    print('索引越界')\nexcept Exception as e:\n    print(f'未知错误: {e}')",
        "output": "尝试：\n  设 列表 为 [1, 2, 3]\n  打印(列表[5])\n捕获 异常：\n  打印(\"索引越界\")",
        "category": "异常",
    },
    # ── 导出模块 ──
    {
        "instruction": "用段言v3.2语法编写以下功能：",
        "input": "# math_utils.py\ndef add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n\n# main.py\nfrom math_utils import add, multiply\nprint(add(2, 3))\nprint(multiply(4, 5))",
        "output": "# 数学工具.duan\n段落 加法 接收 a, b：\n  返回 a 加 b\n段落 乘法 接收 a, b：\n  返回 a 乘 b\n导出 加法, 乘法\n\n# 主.duan\n从 数学工具 导入 加法, 乘法\n打印(加法(2, 3))\n打印(乘法(4, 5))",
        "category": "导入",
    },
    # ── 冒泡排序优化版 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "def bubble_sort_optimized(arr):\n    n = len(arr)\n    for i in range(n - 1):\n        swapped = False\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return arr",
        "output": "段落 冒泡排序 接收 列表：\n  设 长度 为 len(列表)\n  遍历 i 于 0至 长度 减 2：\n    设 已交换 为 假\n    遍历 j 于 0至 长度 减 i 减 2：\n      如果 列表[j] 大于 列表[j 加 1]：\n        设 临时 为 列表[j]\n        列表[j] = 列表[j 加 1]\n        列表[j 加 1] = 临时\n        设 已交换 为 真\n    如果 非 已交换：\n      跳出\n  返回 列表",
        "category": "复合",
    },
    # ── 统计字符 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "text = 'aabbbcccc'\ncounts = {}\nfor ch in text:\n    counts[ch] = counts.get(ch, 0) + 1\nfor ch in sorted(counts):\n    print(f'{ch}: {counts[ch]}')",
        "output": "定义 文本 等于 \"aabbbcccc\"\n设 计数 为 {}\n遍历 字符 于 文本：\n  如果 字符 在 计数：\n    设 计数[字符] 为 计数[字符] 加 1\n  否则：\n    设 计数[字符] 为 1\n遍历 字符 于 计数.键().排序()：\n  打印(f\"{字符}: {计数[字符]}\")",
        "category": "字典",
    },
    # ── 判断闰年 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def is_leap_year(year):\n    if year % 400 == 0:\n        return True\n    if year % 100 == 0:\n        return False\n    if year % 4 == 0:\n        return True\n    return False\n\nprint(is_leap_year(2024))\nprint(is_leap_year(1900))\nprint(is_leap_year(2000))",
        "output": "段落 是否闰年 接收 年份：\n  如果 年份 取余 400 等于 0：\n    返回 真\n  如果 年份 取余 100 等于 0：\n    返回 假\n  如果 年份 取余 4 等于 0：\n    返回 真\n  返回 假\n\n打印(是否闰年(2024))\n打印(是否闰年(1900))\n打印(是否闰年(2000))",
        "category": "条件",
    },
    # ── 打印九九乘法表 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "for i in range(1, 10):\n    for j in range(1, i + 1):\n        print(f'{j}x{i}={i*j}', end=' ')\n    print()",
        "output": "遍历 i 于 1至 9：\n  遍历 j 于 1至 i：\n    打印(f\"{j}x{i}={i 乘 j} \")\n  打印(\"\")",
        "category": "循环",
    },
    # ── 字符串反转 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def reverse_string(s):\n    result = ''\n    for ch in s:\n        result = ch + result\n    return result\n\nprint(reverse_string('hello'))",
        "output": "段落 反转字符串 接收 文本：\n  定义 结果 等于 \"\"\n  遍历 字符 于 文本：\n    定义 结果 等于 字符 加 结果\n  返回 结果\n\n打印(反转字符串(\"hello\"))",
        "category": "字符串",
    },
    # ── 列表求最大值 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "def find_max(arr):\n    if not arr:\n        return None\n    max_val = arr[0]\n    for val in arr[1:]:\n        if val > max_val:\n            max_val = val\n    return max_val\n\nprint(find_max([3, 1, 4, 1, 5, 9, 2, 6]))",
        "output": "段落 查找最大值 接收 列表：\n  如果 len(列表) 等于 0：\n    返回 空\n  设 最大值 为 列表[0]\n  遍历 值 于 列表[1:]：\n    如果 值 大于 最大值：\n      设 最大值 为 值\n  返回 最大值\n\n打印(查找最大值([3, 1, 4, 1, 5, 9, 2, 6]))",
        "category": "复合",
    },
    # ── 打印星号三角形 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "n = 5\nfor i in range(1, n + 1):\n    print('*' * i)\nfor i in range(n - 1, 0, -1):\n    print('*' * i)",
        "output": "设 n 为 5\n遍历 i 于 1至 n：\n  打印(\"*\" 乘 i)\n遍历 i 于 n 减 1至 1：\n  打印(\"*\" 乘 i)",
        "category": "循环",
    },
    # ── 简单计算器段落 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def calculate(a, op, b):\n    if op == '+':\n        return a + b\n    elif op == '-':\n        return a - b\n    elif op == '*':\n        return a * b\n    elif op == '/':\n        if b != 0:\n            return a / b\n        return None\n    return None\n\nprint(calculate(10, '+', 5))\nprint(calculate(10, '/', 3))",
        "output": "段落 计算 接收 a, 运算符, b：\n  如果 运算符 等于 \"+\"：\n    返回 a 加 b\n  否则如果 运算符 等于 \"-\"：\n    返回 a 减 b\n  否则如果 运算符 等于 \"*\"：\n    返回 a 乘 b\n  否则如果 运算符 等于 \"/\"：\n    如果 b 不等于 0：\n      返回 a 除以 b\n    返回 空\n  返回 空\n\n打印(计算(10, \"+\", 5))\n打印(计算(10, \"/\", 3))",
        "category": "条件",
    },
    # ── 银行账户类 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n    def withdraw(self, amount):\n        if amount <= self.balance:\n            self.balance -= amount\n            return True\n        return False\n    def get_balance(self):\n        return self.balance\n\nacc = BankAccount('张三', 1000)\nacc.deposit(500)\nacc.withdraw(200)\nprint(acc.get_balance())",
        "output": "类 银行账户：\n  构造 接收 户主, 余额为0：\n    己.户主 为 户主\n    己.余额 为 余额\n\n  段落 存款 接收 金额：\n    设 己.余额 为 己.余额 加 金额\n    返回 己.余额\n\n  段落 取款 接收 金额：\n    如果 金额 小于等于 己.余额：\n      设 己.余额 为 己.余额 减 金额\n      返回 真\n    返回 假\n\n  段落 获取余额：\n    返回 己.余额\n\n设 账户 为 新建银行账户(\"张三\", 1000)\n账户.存款(500)\n账户.取款(200)\n打印(账户.获取余额())",
        "category": "类",
    },
    # ── 列表过滤和映射 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n# 过滤偶数\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)\n# 映射平方\nsquares = list(map(lambda x: x ** 2, evens))\nprint(squares)",
        "output": "设 数字 为 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n设 偶数 为 []\n遍历 x 于 数字：\n  如果 x 取余 2 等于 0：\n    偶数.追加(x)\n打印(偶数)\n\n设 平方 为 []\n遍历 x 于 偶数：\n  平方.追加(x 乘 x)\n打印(平方)",
        "category": "列表",
    },
    # ── 进制转换 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def to_binary(n):\n    if n == 0:\n        return '0'\n    result = ''\n    while n > 0:\n        result = str(n % 2) + result\n        n = n // 2\n    return result\n\nprint(to_binary(10))\nprint(to_binary(255))",
        "output": "段落 转二进制 接收 n：\n  如果 n 等于 0：\n    返回 \"0\"\n  定义 结果 等于 \"\"\n  当 n 大于 0：\n    定义 结果 等于 转字符串(n 取余 2) 加 结果\n    设 n 为 n 除以 2\n  返回 结果\n\n打印(转二进制(10))\n打印(转二进制(255))",
        "category": "字符串",
    },
    # ── 多返回值/元组 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "def min_max(arr):\n    return min(arr), max(arr)\n\nmn, mx = min_max([3, 1, 4, 1, 5, 9])\nprint(f'min={mn}, max={mx}')",
        "output": "段落 最小最大 接收 列表：\n  设 最小值 为 列表[0]\n  设 最大值 为 列表[0]\n  遍历 值 于 列表：\n    如果 值 小于 最小值：\n      设 最小值 为 值\n    如果 值 大于 最大值：\n      设 最大值 为 值\n  返回 [最小值, 最大值]\n\n设 结果 为 最小最大([3, 1, 4, 1, 5, 9])\n打印(f\"min={结果[0]}, max={结果[1]}\")",
        "category": "复合",
    },
    # ── 抛出异常 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "def divide(a, b):\n    if b == 0:\n        raise ValueError('除数不能为零')\n    return a / b\n\ntry:\n    print(divide(10, 0))\nexcept ValueError as e:\n    print(f'错误: {e}')",
        "output": "段落 除法 接收 a, b：\n  如果 b 等于 0：\n    抛出 异常 \"除数不能为零\"\n  返回 a 除以 b\n\n尝试：\n  打印(除法(10, 0))\n捕获 异常：\n  打印(\"错误: 除数不能为零\")",
        "category": "异常",
    },
    # ── 嵌套字典 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "students = {\n    '张三': {'语文': 90, '数学': 85},\n    '李四': {'语文': 88, '数学': 92}\n}\nfor name, scores in students.items():\n    total = sum(scores.values())\n    print(f'{name}: 总分{total}')",
        "output": "设 学生 为 {\n  \"张三\": {\"语文\": 90, \"数学\": 85},\n  \"李四\": {\"语文\": 88, \"数学\": 92}\n}\n遍历 姓名, 成绩 于 学生.项目()：\n  设 总分 为 0\n  遍历 分数 于 成绩.值()：\n    设 总分 为 总分 加 分数\n  打印(f\"{姓名}: 总分{总分}\")",
        "category": "字典",
    },
    # ── 导出和导入完整模块 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "# string_utils.py\ndef repeat(s, n):\n    return s * n\ndef capitalize(s):\n    return s.capitalize()\n\n# main.py\nfrom string_utils import repeat, capitalize\nprint(repeat('ab', 3))\nprint(capitalize('hello'))",
        "output": "# 字符串工具.duan\n段落 重复 接收 文本, 次数：\n  返回 文本 乘 次数\n段落 首字母大写 接收 文本：\n  返回 文本.首字母大写()\n导出 重复, 首字母大写\n\n# 主程序.duan\n从 字符串工具 导入 重复, 首字母大写\n打印(重复(\"ab\", 3))\n打印(首字母大写(\"hello\"))",
        "category": "导入",
    },
    # ── 检查素数 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nfor i in range(2, 20):\n    if is_prime(i):\n        print(i, end=' ')",
        "output": "段落 是否素数 接收 n：\n  如果 n 小于 2：\n    返回 假\n  设 根 为 转整数(n 的 0.5 次方)\n  遍历 i 于 2至 根：\n    如果 n 取余 i 等于 0：\n      返回 假\n  返回 真\n\n遍历 i 于 2至 19：\n  如果 是否素数(i)：\n    打印(i)",
        "category": "复合",
    },
    # ── 累加器段落 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "def accumulate(start, end, step=1):\n    total = 0\n    for i in range(start, end + 1, step):\n        total += i\n    return total\n\nprint(accumulate(1, 100))\nprint(accumulate(1, 100, 2))",
        "output": "段落 累加 接收 开始, 结束, 步长为1：\n  设 总和 为 0\n  遍历 i 于 开始至 结束：\n    设 总和 为 总和 加 i\n    设 i 为 i 加 步长 减 1\n  返回 总和\n\n打印(累加(1, 100))\n打印(累加(1, 100, 2))",
        "category": "段落",
    },
    # ── 暗坑：列表索引赋值 ──
    {
        "instruction": "请将以下代码翻译为段言（注意段言的列表索引赋值规则）：",
        "input": "arr = [1, 2, 3]\narr[0] = 10\narr[1] = 20\nprint(arr)",
        "output": "设 列表 为 [1, 2, 3]\n列表[0] = 10\n列表[1] = 20\n打印(列表)",
        "category": "暗坑",
    },
    # ── 暗坑：运算用中文不用符号 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码（注意运算符要用中文）：",
        "input": "a = 10\nb = 3\nprint(a + b)\nprint(a - b)\nprint(a * b)\nprint(a / b)\nprint(a % b)",
        "output": "设 a 为 10\n设 b 为 3\n打印(a 加 b)\n打印(a 减 b)\n打印(a 乘 b)\n打印(a 除以 b)\n打印(a 取余 b)",
        "category": "暗坑",
    },
    # ── 暗坑：比较运算用中文 ──
    {
        "instruction": "请将以下代码翻译为段言（比较运算符要用中文）：",
        "input": "x = 5\ny = 10\nprint(x == y)\nprint(x != y)\nprint(x > y)\nprint(x < y)\nprint(x >= 5)\nprint(x <= y)",
        "output": "设 x 为 5\n设 y 为 10\n打印(x 等于 y)\n打印(x 不等于 y)\n打印(x 大于 y)\n打印(x 小于 y)\n打印(x 大于等于 5)\n打印(x 小于等于 y)",
        "category": "暗坑",
    },
    # ── 暗坑：变量名不能用内建函数名 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码（注意变量名不能和内建函数冲突）：",
        "input": "list = [1, 2, 3]\nlen = 5\nprint(list)\nprint(len)",
        "output": "设 列表 为 [1, 2, 3]\n设 长度 为 5\n打印(列表)\n打印(长度)",
        "category": "暗坑",
    },
    # ── 字符串拼接 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "first = 'Hello'\nsecond = 'World'\nmessage = first + ', ' + second + '!'\nprint(message)\nprint(message * 2)",
        "output": "定义 首 等于 \"Hello\"\n定义 次 等于 \"World\"\n定义 消息 等于 首 加 \", \" 加 次 加 \"!\"\n打印(消息)\n打印(消息 乘 2)",
        "category": "字符串",
    },
    # ── None/空 判断 ──
    {
        "instruction": "请用段言v3.2语法编写以下功能：",
        "input": "value = None\nif value is None:\n    print('空值')\nelse:\n    print('有值')\n\nempty_list = []\nif not empty_list:\n    print('空列表')",
        "output": "设 值 为 空\n如果 值 等于 空：\n  打印(\"空值\")\n否则：\n  打印(\"有值\")\n\n设 空列表 为 []\n如果 len(空列表) 等于 0：\n  打印(\"空列表\")",
        "category": "变量",
    },
    # ── 嵌套条件 ──
    {
        "instruction": "用段言v3.2语法重写以下Python代码。",
        "input": "score = 75\nif score >= 60:\n    if score >= 80:\n        print('优秀')\n    else:\n        print('及格')\nelse:\n    if score >= 40:\n        print('不及格')\n    else:\n        print('很差')",
        "output": "设 分数 为 75\n如果 分数 大于等于 60：\n  如果 分数 大于等于 80：\n    打印(\"优秀\")\n  否则：\n    打印(\"及格\")\n否则：\n  如果 分数 大于等于 40：\n    打印(\"不及格\")\n  否则：\n    打印(\"很差\")",
        "category": "条件",
    },
    # ── 列表切片 ──
    {
        "instruction": "请将以下代码翻译为段言：",
        "input": "arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint(arr[:3])\nprint(arr[3:7])\nprint(arr[7:])\nprint(arr[-3:])\nprint(arr[::2])",
        "output": "设 列表 为 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n打印(列表[:3])\n打印(列表[3:7])\n打印(列表[7:])\n打印(列表[-3:])\n打印(列表[::2])",
        "category": "列表",
    },
    # ── 字典遍历 ──
    {
        "instruction": "将Python翻译成段言。",
        "input": "config = {'host': 'localhost', 'port': 8080, 'debug': True}\nfor key in config:\n    print(f'{key}: {config[key]}')\nprint(config.get('host'))\nprint(config.get('timeout', 30))",
        "output": "设 配置 为 {\"host\": \"localhost\", \"port\": 8080, \"debug\": 真}\n遍历 键 于 配置.键()：\n  打印(f\"{键}: {配置[键]}\")\n打印(配置[\"host\"])\n如果 \"timeout\" 在 配置：\n  打印(配置[\"timeout\"])\n否则：\n  打印(30)",
        "category": "字典",
    },
    # ── 打印三角形图案 ──
    {
        "instruction": "用段言v3.2语法表达以下Python代码：",
        "input": "n = 5\nfor i in range(1, n + 1):\n    for j in range(n - i):\n        print(' ', end='')\n    for j in range(2 * i - 1):\n        print('*', end='')\n    print()",
        "output": "设 n 为 5\n遍历 i 于 1至 n：\n  遍历 j 于 1至 n 减 i：\n    打印(\" \")\n  遍历 j 于 1至 2 乘 i 减 1：\n    打印(\"*\")\n  打印(\"\")",
        "category": "循环",
    },
]


def load_existing_dataset():
    """加载现有数据集"""
    data = []
    with open(_DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    print(f"现有数据集: {len(data)} 条")
    return data


def augment(data):
    """添加增强数据"""
    print(f"增强数据: {len(ENHANCED_PAIRS)} 条")
    
    # 随机打乱增强数据
    enhanced = ENHANCED_PAIRS.copy()
    random.seed(42)
    random.shuffle(enhanced)
    
    # 合并
    all_data = data + enhanced
    print(f"合并后总数: {len(all_data)} 条")
    
    # 统计类别
    categories = {}
    for item in all_data:
        cat = item.get("category", "未知")
        categories[cat] = categories.get(cat, 0) + 1
    print("类别分布:")
    for cat, cnt in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}")
    
    return all_data


def save_dataset(data, path):
    """保存数据集"""
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"已保存到: {path} ({len(data)} 条)")


def main():
    print("=" * 60)
    print("段言数据增强")
    print("=" * 60)
    
    # 加载现有数据
    data = load_existing_dataset()
    
    # 增强
    enhanced_data = augment(data)
    
    # 保存
    save_dataset(enhanced_data, _OUTPUT_PATH)
    
    print()
    print("增强完成！")
    print(f"  原始: {len(data)} 条")
    print(f"  增强: {len(ENHANCED_PAIRS)} 条")
    print(f"  总计: {len(enhanced_data)} 条")
    print()
    print("下一步：")
    print(f"  使用增强数据集训练:")
    print(f"  python train_cpu_lora.py --dataset {os.path.basename(_OUTPUT_PATH)}")


if __name__ == "__main__":
    main()
