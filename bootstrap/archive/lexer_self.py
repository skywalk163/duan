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

def 数字转整数(数字字符):
    if (数字字符 == 0):
        return 0
    if (数字字符 == 1):
        return 1
    if (数字字符 == 2):
        return 2
    if (数字字符 == 3):
        return 3
    if (数字字符 == 4):
        return 4
    if (数字字符 == 5):
        return 5
    if (数字字符 == 6):
        return 6
    if (数字字符 == 7):
        return 7
    if (数字字符 == 8):
        return 8
    if (数字字符 == 9):
        return 9
    if (数字字符 == 10):
        return 10
    return 0

def 是数字字符(字符):
    数字列表 = _duan_builtin.列表创建()
    _duan_builtin.列表追加(数字列表, 0)
    _duan_builtin.列表追加(数字列表, 1)
    _duan_builtin.列表追加(数字列表, 2)
    _duan_builtin.列表追加(数字列表, 3)
    _duan_builtin.列表追加(数字列表, 4)
    _duan_builtin.列表追加(数字列表, 5)
    _duan_builtin.列表追加(数字列表, 6)
    _duan_builtin.列表追加(数字列表, 7)
    _duan_builtin.列表追加(数字列表, 8)
    _duan_builtin.列表追加(数字列表, 9)
    _duan_builtin.列表追加(数字列表, 10)
    return _duan_builtin.列表包含(数字列表, 字符)

def 主():
    print(测试词法分析器核心功能)
    测试数字 = 数字转整数(5)
    print(数字五的值)
    print(测试数字)
    测试结果 = 是数字字符(3)
    print(3)
    是数字字符
    print(测试结果)
    测试结果二 = 是数字字符(甲)
    print(甲是数字字符)
    print(测试结果二)
    return 0
