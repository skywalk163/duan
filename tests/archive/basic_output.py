# 由段言编译器生成
# 源文件: 段言代码

import sys
import os

try:
    import importlib.util
except ImportError:
    importlib = None

try:
    _duan_stdlib = os.path.join(os.path.dirname(__file__), 'stdlib')
except NameError:
    _duan_stdlib = os.path.join(os.getcwd(), 'stdlib')
    if not os.path.isdir(_duan_stdlib):
        # 尝试父目录（当从子目录运行时）
        parent_stdlib = os.path.normpath(os.path.join(os.getcwd(), '..', 'stdlib'))
        if os.path.isdir(parent_stdlib):
            _duan_stdlib = parent_stdlib

if os.path.isdir(_duan_stdlib) and _duan_stdlib not in sys.path:
    sys.path.insert(0, _duan_stdlib)

if importlib:
    try:
        _duan_builtin_path = os.path.join(_duan_stdlib, 'builtins.py')
        if os.path.isfile(_duan_builtin_path):
            spec = importlib.util.spec_from_file_location('duan_builtins', _duan_builtin_path)
            _duan_builtin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_duan_builtin)
        else:
            raise ImportError()
    except:
        import types
        _duan_builtin = types.ModuleType('_duan_builtin')
        _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()
        _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None
        _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)
        _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)
        _duan_builtin.打印 = print
        _duan_builtin.列表创建 = list
        _duan_builtin.列 = lambda *args: list(args)
        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
        _duan_builtin.列表包含 = lambda lst, item: item in lst
        _duan_builtin.字符串长度 = len
        _duan_builtin.字典创建 = dict
        _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
        _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)
else:
    import types
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.打印 = print

甲 = 123
乙 = _3加五
print("变量声明：")
print(甲)
print(乙)
结果 = (甲(加乙) * 2)
print("算术运算：")
print(结果)
print("条件语句：")
if (甲 > 乙):
    print("甲大于乙")
else:
    print("甲小于等于乙")
def 加法(甲, 乙):
    return 甲(加乙)

和 = 加法(3(5))
print("函数调用：")
print(和)
def 阶乘(数):
    if (数 <= 1):
        return 1
    return (数 * 阶乘((数 - 1)))

阶乘结果 = 阶乘(5)
print("递归函数（阶乘）：")
print(阶乘结果)
print("循环示例：")
计数 = 1
(当计数 <= 5)