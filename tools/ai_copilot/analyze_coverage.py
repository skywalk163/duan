#!/usr/bin/env python3
"""Analyze dataset coverage for classes, long code, complex patterns."""
import json
import ast
import sys

DATASET = 'sft_dataset.jsonl'

with open(DATASET, 'r', encoding='utf-8') as f:
    samples = [json.loads(line) for line in f]

total = len(samples)

stats = {
    'total': total,
    'by_line_count': {'1': 0, '2-3': 0, '4-8': 0, '9-15': 0, '16+': 0},
    'by_category': {},
    'classes': 0,
    'functions': 0,
    'nested_functions': 0,
    'try_except': 0,
    'decorators': 0,
    'with_stmt': 0,
    'list_comprehension': 0,
    'dict_comprehension': 0,
    'lambda': 0,
    'generators': 0,
    'nested_loops': 0,
    'multi_return': 0,
    'walrus': 0,
    'match_case': 0,
    'global_nonlocal': 0,
    'raise_from': 0,
    'yield_from': 0,
    'async_await': 0,
    'nested_classes': 0,
}

class_details = {
    'simple_class': 0,
    'inheritance': 0,
    'multi_method': 0,
    'property_decorator': 0,
    'staticmethod': 0,
    'classmethod': 0,
    'magic_methods': 0,
}

func_details = {
    'simple_func': 0,
    'medium_func': 0,
    'long_func': 0,
    'recursive': 0,
    'closures': 0,
    'default_args': 0,
    'kwargs': 0,
    'varargs': 0,
    'type_hints': 0,
}

for s in samples:
    py = s['input']
    lines = py.strip().split('\n')
    nlines = len(lines)

    if nlines == 1:
        stats['by_line_count']['1'] += 1
    elif nlines <= 3:
        stats['by_line_count']['2-3'] += 1
    elif nlines <= 8:
        stats['by_line_count']['4-8'] += 1
    elif nlines <= 15:
        stats['by_line_count']['9-15'] += 1
    else:
        stats['by_line_count']['16+'] += 1

    cat = s.get('category', 'unknown')
    stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1

    try:
        tree = ast.parse(py)
    except:
        continue

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            stats['classes'] += 1
            methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if len(methods) >= 3:
                class_details['multi_method'] += 1
            if node.bases:
                class_details['inheritance'] += 1
            for m in methods:
                for dec in m.decorator_list:
                    dec_name = ast.dump(dec)
                    if 'property' in dec_name:
                        class_details['property_decorator'] += 1
                    if 'staticmethod' in dec_name:
                        class_details['staticmethod'] += 1
                    if 'classmethod' in dec_name:
                        class_details['classmethod'] += 1
                if m.name.startswith('__') and m.name.endswith('__'):
                    class_details['magic_methods'] += 1
            if len(methods) <= 1:
                class_details['simple_class'] += 1
            for item in node.body:
                if isinstance(item, ast.ClassDef):
                    stats['nested_classes'] += 1

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stats['functions'] += 1
            func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
            if func_lines <= 3:
                func_details['simple_func'] += 1
            elif func_lines <= 8:
                func_details['medium_func'] += 1
            else:
                func_details['long_func'] += 1

            func_name = node.name
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name) and child.func.id == func_name:
                        func_details['recursive'] += 1
                        break

            args = node.args
            if args.defaults:
                func_details['default_args'] += 1
            if args.kwarg and args.kwarg.arg == 'kwargs':
                func_details['kwargs'] += 1
            if args.vararg and args.vararg.arg == 'args':
                func_details['varargs'] += 1
            if node.returns:
                func_details['type_hints'] += 1

        elif isinstance(node, ast.Try):
            stats['try_except'] += 1
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.decorator_list:
            stats['decorators'] += 1
        elif isinstance(node, ast.With):
            stats['with_stmt'] += 1
        elif isinstance(node, ast.ListComp):
            stats['list_comprehension'] += 1
        elif isinstance(node, ast.DictComp):
            stats['dict_comprehension'] += 1
        elif isinstance(node, ast.Lambda):
            stats['lambda'] += 1
        elif isinstance(node, ast.GeneratorExp):
            stats['generators'] += 1
        elif isinstance(node, ast.Match):
            stats['match_case'] += 1
        elif isinstance(node, ast.Global):
            stats['global_nonlocal'] += 1
        elif isinstance(node, ast.Nonlocal):
            stats['global_nonlocal'] += 1

    # Nested loops
    try:
        tree2 = ast.parse(py)
        for node in ast.walk(tree2):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if child is not node and isinstance(child, (ast.For, ast.While)):
                        stats['nested_loops'] += 1
                        break
    except:
        pass

    # Nested functions
    try:
        tree3 = ast.parse(py)
        for node in ast.walk(tree3):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in ast.walk(node):
                    if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        stats['nested_functions'] += 1
                        func_details['closures'] += 1
                        break
    except:
        pass

    # Multi-return
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('return ') and ',' in stripped and '(' not in stripped.split(',', 1)[0]:
            stats['multi_return'] += 1
            break

    # Walrus
    if ':=' in py:
        stats['walrus'] += 1

    # raise from
    if 'raise' in py and ' from ' in py:
        stats['raise_from'] += 1

    # yield from
    if 'yield from' in py:
        stats['yield_from'] += 1

    # async/await
    if 'async ' in py or 'await ' in py:
        stats['async_await'] += 1


print("=" * 70)
print(f"数据集覆盖度分析 (总样本数: {total})")
print("=" * 70)

print("\n### 按行数分布 ###")
for k in ['1', '2-3', '4-8', '9-15', '16+']:
    v = stats['by_line_count'][k]
    pct = v / total * 100
    bar = '#' * int(pct / 2)
    print(f"  {k:8s} lines: {v:4d} ({pct:5.1f}%) {bar}")

print("\n### 按类别分布 (Top 20) ###")
for k, v in sorted(stats['by_category'].items(), key=lambda x: -x[1])[:20]:
    pct = v / total * 100
    print(f"  {k:20s}: {v:4d} ({pct:5.1f}%)")

print("\n### 语法结构覆盖 ###")
syntax_items = [
    ('classes', stats['classes']),
    ('functions', stats['functions']),
    ('try_except', stats['try_except']),
    ('list_comprehension', stats['list_comprehension']),
    ('decorators', stats['decorators']),
    ('with_stmt', stats['with_stmt']),
    ('lambda', stats['lambda']),
    ('dict_comprehension', stats['dict_comprehension']),
    ('nested_loops', stats['nested_loops']),
    ('generators', stats['generators']),
    ('nested_functions', stats['nested_functions']),
    ('multi_return', stats['multi_return']),
    ('global_nonlocal', stats['global_nonlocal']),
    ('match_case', stats['match_case']),
    ('walrus', stats['walrus']),
    ('yield_from', stats['yield_from']),
    ('raise_from', stats['raise_from']),
    ('async_await', stats['async_await']),
    ('nested_classes', stats['nested_classes']),
]
for name, count in syntax_items:
    pct = count / total * 100 if total > 0 else 0
    if count >= 20:
        status = 'OK'
    elif count >= 5:
        status = 'LOW'
    else:
        status = 'MISSING'
    print(f"  {name:25s}: {count:4d} ({pct:5.1f}%) [{status}]")

print("\n### 函数复杂度分布 ###")
func_items = [
    ('simple_func(1-3L)', func_details['simple_func']),
    ('medium_func(4-8L)', func_details['medium_func']),
    ('long_func(9+L)', func_details['long_func']),
    ('recursive', func_details['recursive']),
    ('closures', func_details['closures']),
    ('default_args', func_details['default_args']),
    ('varargs(*args)', func_details['varargs']),
    ('kwargs(**kwargs)', func_details['kwargs']),
    ('type_hints', func_details['type_hints']),
]
for name, count in func_items:
    pct = count / total * 100 if total > 0 else 0
    if count >= 15:
        status = 'OK'
    elif count >= 5:
        status = 'LOW'
    else:
        status = 'MISSING'
    print(f"  {name:25s}: {count:4d} ({pct:5.1f}%) [{status}]")

print("\n### 类复杂度分布 ###")
class_items = [
    ('simple_class(0-1m)', class_details['simple_class']),
    ('multi_method(3+)', class_details['multi_method']),
    ('inheritance', class_details['inheritance']),
    ('property', class_details['property_decorator']),
    ('staticmethod', class_details['staticmethod']),
    ('classmethod', class_details['classmethod']),
    ('magic_methods', class_details['magic_methods']),
]
for name, count in class_items:
    pct = count / total * 100 if total > 0 else 0
    if count >= 10:
        status = 'OK'
    elif count >= 3:
        status = 'LOW'
    else:
        status = 'MISSING'
    print(f"  {name:25s}: {count:4d} ({pct:5.1f}%) [{status}]")

print("\n" + "=" * 70)
print("### 缺口汇总 ###")
print("=" * 70)

all_items = syntax_items + func_items + class_items
critical = [(n, c) for n, c in all_items if c < 5]
low = [(n, c) for n, c in all_items if 5 <= c < 15]

print(f"\nCRITICAL (< 5):")
for name, count in sorted(critical, key=lambda x: x[1]):
    print(f"  {name:25s}: {count}")
print(f"\nLOW (< 15):")
for name, count in sorted(low, key=lambda x: x[1]):
    print(f"  {name:25s}: {count}")

# Long code analysis
print("\n### 长代码行数分布详情 ###")
long_samples = []
for i, s in enumerate(samples):
    lines = s['input'].strip().split('\n')
    if len(lines) >= 9:
        long_samples.append((i, len(lines), s.get('category', ''), s['input'][:80]))

print(f"9+ 行样本: {len(long_samples)} 条")
for idx, nlines, cat, preview in long_samples[:10]:
    print(f"  [{idx}] {nlines}L cat={cat}: {preview}...")
if len(long_samples) > 10:
    print(f"  ... 还有 {len(long_samples) - 10} 条")
