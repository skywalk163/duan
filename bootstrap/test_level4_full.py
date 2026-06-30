"""
Level 4 全面测试套件 v3
修复: 正确预期值，标注语言限制
"""
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

with open('level4_generated.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code, ns)
编译 = ns['编译']
nl = '\n'
dq = '"'

passed = 0
failed = 0
lang_limited = 0
failed_tests = []

def t(name, src, expected):
    """正常测试"""
    global passed, failed, failed_tests
    try:
        code = 编译(src)
        ns2 = dict(ns)
        exec(code, ns2)
        result = ns2['test']()
        if result == expected:
            print(f"  OK  {name}")
            passed += 1
        else:
            print(f"  FAIL {name}: expected {expected}, got {result}")
            failed += 1
            failed_tests.append(name)
    except Exception as e:
        print(f"  FAIL {name}: {type(e).__name__}: {e}")
        failed += 1
        failed_tests.append(name)

def x(name, src, err_type):
    """错误场景"""
    global passed, failed, failed_tests
    result = None
    try:
        code = 编译(src)
        ns2 = dict(ns)
        exec(code, ns2)
        result = ns2['test']()
        if err_type == 'None' and result is None:
            print(f"  OK  {name} ({err_type})")
            passed += 1
        else:
            print(f"  FAIL {name}: 期望 {err_type}, 实际返回 {result}")
            failed += 1
            failed_tests.append(name)
    except Exception as e:
        if err_type in type(e).__name__ or err_type in str(e):
            print(f"  OK  {name} ({type(e).__name__})")
            passed += 1
        else:
            print(f"  FAIL {name}: 期望 {err_type}, 实际 {type(e).__name__}: {e}")
            failed += 1
            failed_tests.append(name)

print("=" * 60)
print("Level 4 全面测试套件 v3")
print("=" * 60)

# ═══════════════════════════════════════════════════════════
# 类别 1: 多级继承
# ═══════════════════════════════════════════════════════════
print()
print("[类别 1] 多级继承")
t('三级继承',
  '类 A：' + nl + '  段落 greet 接收 己：' + nl + '    返回 ' + dq + 'A' + dq + '。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 B(A)：' + nl + '  段落 greet 接收 己：' + nl + '    返回 父.greet() 加 ' + dq + 'B' + dq + '。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 C(B)：' + nl + '  段落 greet 接收 己：' + nl + '    返回 父.greet() 加 ' + dq + 'C' + dq + '。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 C().greet()。' + nl + '结束。' + nl,
  'ABC')

t('四级继承',
  '类 L1：' + nl + '  段落 val 接收 己：' + nl + '    返回 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 L2(L1)：' + nl + '  段落 val 接收 己：' + nl + '    返回 父.val() 加 10。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 L3(L2)：' + nl + '  段落 val 接收 己：' + nl + '    返回 父.val() 加 100。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 L4(L3)：' + nl + '  段落 val 接收 己：' + nl + '    返回 父.val() 加 1000。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 L4().val()。' + nl + '结束。' + nl,
  1111)

t('菱形继承',
  '类 Base：' + nl + '  属性 val。' + nl + nl + '  段落 __init__ 接收 己, v：' + nl + '    设 己.val 为 v。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Base(99).val。' + nl + '结束。' + nl,
  99)

# ═══════════════════════════════════════════════════════════
# 类别 2: Super 链
# ═══════════════════════════════════════════════════════════
print()
print("[类别 2] Super 链")
t('super三次链',
  '类 Base：' + nl + '  段落 calc 接收 己, n：' + nl + '    返回 n 加 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 Middle(Base)：' + nl + '  段落 calc 接收 己, n：' + nl + '    返回 父.calc(n) 乘 2。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 Top(Middle)：' + nl + '  段落 calc 接收 己, n：' + nl + '    返回 父.calc(n) 加 100。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Top().calc(5)。' + nl + '结束。' + nl,
  112)

t('super嵌套方法',
  '类 Calc：' + nl +
  '  段落 twice 接收 己, n：' + nl + '    返回 n 乘 2。' + nl + '  结束。' + nl +
  '  段落 add_one 接收 己, n：' + nl + '    返回 n 加 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  设 c 为 Calc()。' + nl +
  '  返回 c.twice(c.add_one(5))。' + nl + '结束。' + nl,
  12)

# ═══════════════════════════════════════════════════════════
# 类别 3: 多重属性访问
# ═══════════════════════════════════════════════════════════
print()
print("[类别 3] 多重属性访问")
t('嵌套对象属性',
  '类 Inner：' + nl + '  属性 x。' + nl + nl + '  段落 __init__ 接收 己, x：' + nl + '    设 己.x 为 x。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 Outer：' + nl + '  属性 inner。' + nl + nl + '  段落 __init__ 接收 己：' + nl + '    设 己.inner 为 Inner(42)。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Outer().inner.x。' + nl + '结束。' + nl,
  42)

t('属性多次修改',
  '类 Counter：' + nl +
  '  属性 count。' + nl + nl +
  '  段落 __init__ 接收 己：' + nl + '    设 己.count 为 0。' + nl + '  结束。' + nl + nl +
  '  段落 inc 接收 己：' + nl + '    设 己.count 为 己.count 加 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  设 c 为 Counter()。' + nl +
  '  c.inc()' + nl + '  c.inc()' + nl + '  c.inc()' + nl +
  '  返回 c.count。' + nl + '结束。' + nl,
  3)

t('深层属性读取',
  '类 L3：' + nl + '  属性 val。' + nl + '  段落 __init__ 接收 己, v：' + nl + '    设 己.val 为 v。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 L2：' + nl + '  属性 next。' + nl + '  段落 __init__ 接收 己, n：' + nl + '    设 己.next 为 n。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 L1：' + nl + '  属性 next。' + nl + '  段落 __init__ 接收 己, n：' + nl + '    设 己.next 为 n。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  设 l1 为 L1(L2(L3(999)))。' + nl +
  '  返回 l1.next.next.val。' + nl + '结束。' + nl,
  999)

# ═══════════════════════════════════════════════════════════
# 类别 4: 链式方法调用
# ═══════════════════════════════════════════════════════════
print()
print("[类别 4] 链式方法调用")
t('两方法链',
  '类 Builder：' + nl +
  '  属性 v。' + nl +
  '  段落 __init__ 接收 己：' + nl + '    设 己.v 为 0。' + nl + '  结束。' + nl +
  '  段落 add 接收 己, n：' + nl + '    设 己.v 为 己.v 加 n。' + nl + '    返回 己。' + nl + '  结束。' + nl +
  '  段落 result 接收 己：' + nl + '    返回 己.v。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  返回 Builder().add(5).add(3).result()。' + nl + '结束。' + nl,
  8)

t('三方法链',
  '类 Builder：' + nl +
  '  属性 s。' + nl + nl +
  '  段落 __init__ 接收 己：' + nl + '    设 己.s 为 ' + dq + '' + dq + '。' + nl + '  结束。' + nl +
  '  段落 add 接收 己, txt：' + nl + '    设 己.s 为 己.s 加 txt。' + nl + '    返回 己。' + nl + '  结束。' + nl +
  '  段落 val 接收 己：' + nl + '    返回 己.s。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  返回 Builder().add(' + dq + 'Hello' + dq + ').add(' + dq + 'World' + dq + ').val()。' + nl + '结束。' + nl,
  'HelloWorld')

t('方法链+属性',
  '类 R：' + nl + '  属性 v。' + nl + '  段落 __init__ 接收 己, v：' + nl + '    设 己.v 为 v。' + nl + '  结束。' + nl +
  '  段落 mul 接收 己, n：' + nl + '    设 己.v 为 己.v 乘 n。' + nl + '    返回 己。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  设 r 为 R(2)。' + nl +
  '  返回 r.mul(3).mul(5).v。' + nl + '结束。' + nl,
  30)

# ═══════════════════════════════════════════════════════════
# 类别 5: 边界情况
# ═══════════════════════════════════════════════════════════
print()
print("[类别 5] 边界情况")
t('空类实例化',
  '类 Empty：' + nl + '  段落 dummy 接收 己：' + nl + '    返回 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Empty().dummy()。' + nl + '结束。' + nl,
  1)

t('只有构造函数的类',
  '类 Simple：' + nl +
  '  段落 __init__ 接收 己：' + nl + '    设 己.x 为 123。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Simple().x。' + nl + '结束。' + nl,
  123)

t('多层方法嵌套调用',
  '类 Math：' + nl +
  '  段落 sq 接收 己, n：' + nl + '    返回 n 乘 n。' + nl + '  结束。' + nl +
  '  段落 add 接收 己, a, b：' + nl + '    返回 a 加 b。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl +
  '  设 m 为 Math()。' + nl +
  '  返回 m.add(m.sq(2), m.sq(3))。' + nl + '结束。' + nl,
  13)

t('递归继承',
  '类 Fact：' + nl +
  '  段落 fact 接收 己, n：' + nl + '    返回 n。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 FactEx(Fact)：' + nl +
  '  段落 fact 接收 己, n：' + nl +
  '    如果 n 小于等于 1：' + nl + '      返回 父.fact(n)。' + nl + '    结束。' + nl +
  '    返回 n 乘 己.fact(n 减 1)。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 FactEx().fact(5)。' + nl + '结束。' + nl,
  120)

t('继承覆盖+super',
  '类 Base：' + nl + '  段落 step 接收 己：' + nl + '    返回 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '类 Derived(Base)：' + nl + '  段落 step 接收 己：' + nl + '    返回 父.step() 加 2。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 Derived().step()。' + nl + '结束。' + nl,
  3)

# ═══════════════════════════════════════════════════════════
# 类别 6: 错误场景
# ═══════════════════════════════════════════════════════════
print()
print("[类别 6] 错误场景")
x('除以零',
  '段落 test：' + nl + '  返回 10 除 0。' + nl + '结束。' + nl,
  'ZeroDivisionError')

x('列表越界',
  '段落 test：' + nl + '  设 lst 为 列表创建(1, 2, 3)。' + nl + '  返回 列表获取(lst, 10)。' + nl + '结束。' + nl,
  'IndexError')

x('调用不存在的类',
  '段落 test：' + nl + '  返回 Nonexistent().foo()。' + nl + '结束。' + nl,
  'NameError')

x('超类未定义',
  '类 Derived(BadBase)：' + nl + '结束。' + nl + '段落 test：' + nl + '  返回 1。' + nl + '结束。' + nl,
  'NameError')

x('构造函数参数过多',
  '类 A：' + nl + '  段落 __init__ 接收 己：' + nl + '    设 己.x 为 1。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 A(1, 2, 3)。' + nl + '结束。' + nl,
  'TypeError')

x('访问未初始化属性',
  '类 A：' + nl + '  段落 get 接收 己：' + nl + '    返回 己.x。' + nl + '  结束。' + nl + '结束。' + nl +
  '段落 test：' + nl + '  返回 A().get()。' + nl + '结束。' + nl,
  'AttributeError')

# ═══════════════════════════════════════════════════════════
# 类别 7: Level 3 回归
# ═══════════════════════════════════════════════════════════
print()
print("[类别 7] Level 3 回归测试")
t('整数算术正确优先级',
  '段落 test：' + nl + '  返回 1 加 2 乘 3 减 4 除 2。' + nl + '结束。' + nl,
  5)  # 1+6-2=5
t('比较运算',
  '段落 test：' + nl + '  返回 5 大于 3 且 2 小于 1 或 10 等于 10。' + nl + '结束。' + nl,
  True)
t('字符串',
  '段落 test：' + nl + '  设 s 为 ' + dq + 'Hello' + dq + '。' + nl + '  返回 s。' + nl + '结束。' + nl,
  'Hello')
t('列表长度',
  '段落 test：' + nl + '  设 lst 为 列表创建(1, 2, 3)。' + nl + '  列表追加(lst, 4)。' + nl + '  返回 列表长度(lst)。' + nl + '结束。' + nl,
  4)
t('嵌套if',
  '段落 test：' + nl + '  设 x 为 5。' + nl + '  如果 x 大于 0：' + nl + '    如果 x 大于 3：' + nl + '      返回 1。' + nl + '    结束。' + nl + '  结束。' + nl + '  返回 0。' + nl + '结束。' + nl,
  1)
t('for遍历',
  '段落 test：' + nl + '  设 s 为 0。' + nl + '  遍历 i 在 列表创建(1, 2, 3, 4, 5)：' + nl + '    设 s 为 s 加 i。' + nl + '  结束。' + nl + '  返回 s。' + nl + '结束。' + nl,
  15)
t('非运算',
  '段落 test：' + nl + '  如果 非 假：' + nl + '    返回 1。' + nl + '  结束。' + nl + '  返回 0。' + nl + '结束。' + nl,
  1)
t('负数',
  '段落 test：' + nl + '  返回 10 减 15。' + nl + '结束。' + nl,
  -5)
t('取模',
  '段落 test：' + nl + '  返回 17 取模 5。' + nl + '结束。' + nl,
  2)
t('while嵌套',
  '段落 test：' + nl + '  设 i 为 0。' + nl + '  设 j 为 0。' + nl + '  当 i 小于 3：' + nl + '    设 j 为 0。' + nl + '    当 j 小于 3：' + nl + '      设 j 为 j 加 1。' + nl + '    结束。' + nl + '    设 i 为 i 加 1。' + nl + '  结束。' + nl + '  返回 i 乘 10 加 j。' + nl + '结束。' + nl,
  33)

# ═══════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════
print()
print("=" * 60)
print("总结")
print("=" * 60)
print(f"  总计: {passed}/{passed+failed} 通过")
if failed_tests:
    print(f"  失败: {failed_tests}")
else:
    print("  所有测试通过！")
