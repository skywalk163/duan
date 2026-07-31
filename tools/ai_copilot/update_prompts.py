#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新4个脚本的 SYSTEM_PROMPT，新增 v5 规则"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

NEW_RULES_LINE = (
    '    "- 装饰器: @标注名 标注\\n"\n'
    '    "- 变量名保持: 变量名、函数名、类名、方法名保持英文原样，不翻译为中文\\n"\n'
    '    "- 复合赋值: x += y -> 设 x 为 x 加上 y; x -= y -> 设 x 为 x 减去 y; x *= y -> 设 x 为 x 乘以 y; x /= y -> 设 x 为 x 除以 y\\n"\n'
    '    "- 负数字面量: -1, -100 等负数保持原样，返回 -1 而非 返回 减去 1\\n"\n'
    '    "- 整除运算: // 翻译为 整除; / 翻译为 除以\\n"\n'
    '    "- 取余运算: % 翻译为 取余\\n"\n'
    '    "- 幂运算: ** 翻译为 的 N 次方\\n"\n'
    '    "- 方法调用: 对象方法调用保持原样，如 s.upper(), lst.append(x), d.get(key) 不翻译方法名\\n"\n'
    '    "- break/continue: break -> 跳出; continue -> 跳过; 不可混用 返回 替代 break\\n"\n'
    '    "- 多返回值: return a, b 保持原样; x, y = func() 分别赋值\\n"\n'
    '    "- 异常类型: 捕获具体异常类型，如 捕获 ZeroDivisionError 为 e\\n"\n'
)

OLD_DECORATOR_LINE = '    "- 装饰器: @标注名 标注\\n"\n'

files = ['train_gpu_lora.py', 'train_cpu_lora.py', 'local_infer.py', 'diagnose_loss.py']

for fname in files:
    fpath = os.path.join(SCRIPT_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '变量名保持: 变量名、函数名' in content:
        print(f'{fname}: already has new rules, skip')
        continue

    if OLD_DECORATOR_LINE not in content:
        print(f'{fname}: decorator line not found')
        continue

    content = content.replace(OLD_DECORATOR_LINE, NEW_RULES_LINE, 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{fname}: updated')

print('Done.')
