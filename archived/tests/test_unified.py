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

def 问候(姓名):
    return (('你好，' + 姓名) + '！')

def 求和(甲, 乙):
    return (甲 + 乙)

class 狗:
    def __init__(self, 名字):
        super().__init__()
        self.名字 = 名字
    def 叫(self):
        print((self.名字 + ' 汪汪叫！'))

名字 = '世界'
print(问候(名字))
结果 = 求和(3, 5)
print(('3 + 5 = ' + 结果))
旺财 = 狗('旺财')
旺财.叫()