# 由段言编译器生成
# 源文件: 段言代码

# 导入段言标准库
try:
    from stdlib import builtins as _duan_builtin
except ImportError:
    # 如果无法导入，使用内置函数占位
    import types
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.读取文件 = lambda path: open(path, 'r', encoding='utf-8').read()
    _duan_builtin.写入文件 = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or None
    _duan_builtin.文件存在 = lambda path: __import__('os').path.isfile(path)
    _duan_builtin.目录存在 = lambda path: __import__('os').path.isdir(path)
    _duan_builtin.打印 = print

__all__ = ['测试函数']
def 测试函数():
    字典 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(字典, "名称", "测试")
    print("测试完成")
    return True
