"""测试 level6_self_compiled.py 的编译功能"""
import sys
sys.path.insert(0, '.')

def 列表创建(*args): return list(args)
def 列表追加(lst, item): lst.append(item)
def 列表插入(lst, item): lst.append(item)
def 列表获取(lst, i): return lst[i]
def 列表长度(lst): return len(lst)
def 列表弹栈(lst):
    if len(lst) > 0: lst.pop()
def 字符串长度(s): return len(s)
def 字符串获取(s, i): return s[i]
def 截取(s, a, b): return s[a:b]
def 打印(*args): print(*args)
def 建(t, v): return [t, v]

ns = {
    '列表创建': 列表创建, '列表追加': 列表追加, '列表插入': 列表插入, '列表获取': 列表获取,
    '列表长度': 列表长度, '列表弹栈': 列表弹栈,
    '字符串长度': 字符串长度, '字符串获取': 字符串获取,
    '截取': 截取, '打印': 打印, '输出': 打印, '真': True, '假': False, '建': 建,
}

# 加载 level6_generated.py (正确的编译器)
with open('bootstrap/level6_generated.py', 'r', encoding='utf-8') as f:
    ref_code = f.read()
exec(ref_code, ns)
编译参考 = ns['编译']

# 测试简单编译
src = "段落 foo\n    返回 42\n"
print(f"测试编译: {repr(src)}")
result = 编译参考(src)
print(f"结果: {result}")
print(f"结果大小: {len(result)} 字节")
print()

# 加载 level6_self_compiled.py
ns2 = {k: v for k, v in ns.items()}
with open('bootstrap/level6_self_compiled.py', 'r', encoding='utf-8') as f:
    self_code = f.read()
exec(self_code, ns2)
编译自举 = ns2['编译']

# 同样的测试
print(f"测试自举编译器: {repr(src)}")
result2 = 编译自举(src)
print(f"结果: {result2}")
print(f"结果大小: {len(result2)} 字节")
print()

# 测试更复杂的例子
src2 = "段落 foo\n    设 x 为 42\n    返回 x\n"
print(f"测试2: {repr(src2)}")
r1 = 编译参考(src2)
r2 = 编译自举(src2)
print(f"参考编译器: {r1}")
print(f"自举编译器: {r2}")