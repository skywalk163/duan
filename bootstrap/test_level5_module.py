import sys
sys.path.insert(0, 'bootstrap')

# 基础运行时函数
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

def test_import_export_keywords():
    词法 = ns['词法']
    toks = 词法("导入 导出 math_utils")
    kw_count = sum(1 for t in toks if t[0] == 'KW')
    assert kw_count >= 2, f"期望至少 2 个关键字，实际 {kw_count}"
    print("✅ 导入/导出关键字识别测试通过")

if __name__ == '__main__':
    print("Level 5 模块系统测试")
    print("=" * 50)
    test_import_export_keywords()