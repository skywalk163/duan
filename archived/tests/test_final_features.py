# 由段言编译器生成
# 源文件: 段言代码

# 导入段言标准库
import sys
import importlib.util
try:
    # 尝试从src/stdlib导入
    spec = importlib.util.spec_from_file_location('duan_builtins', 'src/stdlib/builtins.py')
    _duan_builtin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_duan_builtin)
except:
    # 如果无法导入，使用内置函数占位
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

def 计算平方(数值):
    return (数值 * 数值)

def 计算阶乘(数值):
    if (数值 < 2):
        return 1
    前值 = (数值 - 1)
    递归结果 = 计算阶乘(前值)
    return (数值 * 递归结果)

def 判断正负(数值):
    if (数值 > 0):
        print(正数)
        return 1
    if (数值 < 0):
        print(负数)
        return 负一
    print(0)
    return 0

def 计算累加(限制):
    计数器 = 0
    总和 = 0
    while (计数器 < 限制):
        总和 = (总和 + 计数器)
        计数器 = (计数器 + 1)
    return 总和

def 测试列表功能():
    数字数据 = _duan_builtin.列表创建()
    _duan_builtin.列表追加(数字数据, 1)
    _duan_builtin.列表追加(数字数据, 2)
    _duan_builtin.列表追加(数字数据, 3)
    _duan_builtin.列表追加(数字数据, 4)
    _duan_builtin.列表追加(数字数据, 5)
    数据长度 = _duan_builtin.字符串长度(数字数据)
    print(列表长度)
    print(数据长度)
    索引值 = 0
    while (索引值 < 数据长度):
        元素内容 = _duan_builtin.列表获取(数字数据, 索引值)
        print(元素内容)
        索引值 = (索引值 + 1)
    return 数据长度

def 测试字典功能():
    分数数据 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(分数数据, 张三, 9)
