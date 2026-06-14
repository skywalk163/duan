# 由段言编译器生成
# 源文件: 段言代码

# 导入段言标准库
import sys
import importlib.util
try:
    spec = importlib.util.spec_from_file_location('duan_builtins', 'src/stdlib/builtins.py')
    _duan_builtin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_duan_builtin)
except:
    import types
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()
    _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None
    _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)
    _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)
    _duan_builtin.打印 = print
    _duan_builtin.列表创建 = list
    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
    _duan_builtin.列表包含 = lambda lst, item: item in lst
    _duan_builtin.字符串长度 = len
    _duan_builtin.字典创建 = dict
    _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
    _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)

def 平方(数值):
    return (数值 * 数值)

def 求和(甲, 乙):
    return (甲 + 乙)

def 三倍(数值):
    return (数值 * 3)

def 九倍(数值):
    return 三倍(三倍(数值))

def 阶乘(数值):
    if (数值 <= 1):
        return 1
    else:
        return (数值 * 阶乘((数值 - 1)))

甲 = 10
乙 = 20
结果 = (甲 + 乙)
print(结果)
平方值 = 平方(5)
print(平方值)
和值 = 求和(10, 20)
print(和值)
分数 = 85
if (分数 > 60):
    print('及格')
else:
    print('不及格')
计数 = 0
while (计数 < 3):
    print(计数)
    计数 = (计数 + 1)
水果 = ['苹果', '香蕉', '橙子']
for 水果项 in 水果:
    print(水果项)
数字列表 = [1, 2, 3, 4, 5]
print(数字列表[0])
print(数字列表[2])
学生信息 = {'姓名': '张三', '年龄': 18, '分数': 95}
print(学生信息['姓名'])
print(学生信息['分数'])
print(九倍(2))
print(阶乘(5))
try:
    错误值 = 10
    0
    print(错误值)
except Exception as 异常信息:
    print('捕获到异常：')
    print(异常信息)
print('所有测试完成！')