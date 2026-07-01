import sys
sys.path.insert(0, '.')

def 列表创建(*args): return list(args)
def 列表追加(lst, item): lst.append(item)
def 列表获取(lst, i): return lst[i]
def 列表长度(lst): return len(lst)
def 字符串长度(s): return len(s)
def 字符串获取(s, i): return s[i]
def 截取(s, a, b): return s[a:b]
def 打印(*args): print(*args)
def 建(t, v): return [t, v]

ns = {
    '列表创建': 列表创建, '列表追加': 列表追加, '列表获取': 列表获取,
    '列表长度': 列表长度, '字符串长度': 字符串长度, '字符串获取': 字符串获取,
    '截取': 截取, '打印': 打印, '真': True, '假': False, '建': 建,
}

with open('bootstrap/level5_generated.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code, ns)
词法 = ns['词法']

def run_test(name, code, expected_output, should_raise=False):
    # 编译并运行 Duan 代码，检查输出
    pass

def test_keywords():
    # 测试关键字识别
    toks = 词法("尝试 捕获 最终 抛出")
    kw_count = sum(1 for t in toks if t[0] == 'KW')
    assert kw_count == 4, f"期望 4 个关键字，实际 {kw_count}"
    print("✅ 关键字识别测试通过")

def test_throw_string():
    with open('bootstrap/level5_generated.py', 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code, ns)
    编译 = ns['编译']
    code = '抛出 "测试错误"'
    result = 编译(code)
    assert 'raise' in result, f"生成代码应包含 raise: {result}"
    print("✅ 抛出字符串测试通过")

def test_try_catch_basic():
    exec(open('bootstrap/level5_generated.py', 'r', encoding='utf-8').read(), ns)
    编译 = ns['编译']
    code = """尝试：
    输出("测试")
捕获：
    输出("捕获错误")
结束。
"""
    result = 编译(code)
    assert 'try:' in result, f"应生成 try: {result}"
    assert 'except:' in result, f"应生成 except: {result}"
    print("✅ 基础尝试-捕获测试通过")

if __name__ == '__main__':
    print("Level 5 异常处理测试")
    print("=" * 50)
    test_keywords()
    test_throw_string()
    test_try_catch_basic()