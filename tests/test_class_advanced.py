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

class 动物:
    def 叫声(self):
        print('动物叫声')

class 狗(动物):
    def __init__(self, 名称, 品种):
        self.名称 = 名称
        self.品种 = 品种
    def 叫声(self):
        print('汪汪汪')
    def 介绍(self):
        print('我是')
        print(self.名称)
        print('品种：')
        print(self.品种)

class 猫(动物):
    def __init__(self, 名称):
        self.名称 = 名称
    def 叫声(self):
        print('喵喵喵')

小狗 = 狗('旺财', '金毛')
小狗.叫声()
小狗.介绍()
小猫 = 猫('咪咪')
小猫.叫声()
print('类定义测试完成！')