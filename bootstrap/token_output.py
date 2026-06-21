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
        _duan_builtin.转字符串 = str
        _duan_builtin.列表创建 = list
        _duan_builtin.列表长度 = len
        _duan_builtin.列 = lambda *args: list(args)
        _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
        _duan_builtin.列表包含 = lambda lst, item: item in lst
        _duan_builtin.字符串长度 = len
        _duan_builtin.字典创建 = dict
        _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
        _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)
        _duan_builtin.字典键列表 = lambda d: list(d.keys())
        _duan_builtin.字典包含键 = lambda d, k: k in d
else:
    import types
    _duan_builtin = types.ModuleType('_duan_builtin')
    _duan_builtin.打印 = print
    _duan_builtin.转字符串 = str
    _duan_builtin.列表创建 = list
    _duan_builtin.列表长度 = len
    _duan_builtin.列 = lambda *args: list(args)
    _duan_builtin.列表追加 = lambda lst, item: lst.append(item)
    _duan_builtin.列表包含 = lambda lst, item: item in lst
    _duan_builtin.字符串长度 = len
    _duan_builtin.字典创建 = dict
    _duan_builtin.字典设置 = lambda d, k, v: d.update({k: v})
    _duan_builtin.字典获取 = lambda d, k, default=None: d.get(k, default)
    _duan_builtin.字典键列表 = lambda d: list(d.keys())
    _duan_builtin.字典包含键 = lambda d, k: k in d

__all__ = ['创建令牌', '令牌种别集', '是关键字']
def 创建令牌(种别, 值, 横, 纵):
    令牌 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(令牌, "种别", 种别)
    _duan_builtin.字典设置(令牌, "值", 值)
    _duan_builtin.字典设置(令牌, "横", 横)
    _duan_builtin.字典设置(令牌, "纵", 纵)
    return 令牌

def 令牌种别集():
    种别字典 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(种别字典, "关键字", "关键字")
    _duan_builtin.字典设置(种别字典, "标识符", "标识符")
    _duan_builtin.字典设置(种别字典, "数字", "数字")
    _duan_builtin.字典设置(种别字典, "字符串", "字符串")
    _duan_builtin.字典设置(种别字典, "符号", "符号")
    _duan_builtin.字典设置(种别字典, "结束", "结束")
    return 种别字典

def 是关键字(文本):
    关键字列表 = _duan_builtin.列表创建()
    _duan_builtin.列表追加(关键字列表, "定义")
    _duan_builtin.列表追加(关键字列表, "等于")
    _duan_builtin.列表追加(关键字列表, "如果")
    _duan_builtin.列表追加(关键字列表, "那么")
    _duan_builtin.列表追加(关键字列表, "否则")
    _duan_builtin.列表追加(关键字列表, "返回")
    _duan_builtin.列表追加(关键字列表, "段")
    _duan_builtin.列表追加(关键字列表, "结束")
    _duan_builtin.列表追加(关键字列表, "当")
    _duan_builtin.列表追加(关键字列表, "遍历")
    _duan_builtin.列表追加(关键字列表, "跳过")
    _duan_builtin.列表追加(关键字列表, "跳出")
    _duan_builtin.列表追加(关键字列表, "打印")
    _duan_builtin.列表追加(关键字列表, "导入")
    _duan_builtin.列表追加(关键字列表, "导出")
    _duan_builtin.列表追加(关键字列表, "设")
    _duan_builtin.列表追加(关键字列表, "为")
    _duan_builtin.列表追加(关键字列表, "尝试")
    _duan_builtin.列表追加(关键字列表, "捕获")
    _duan_builtin.列表追加(关键字列表, "抛出")
    _duan_builtin.列表追加(关键字列表, "从")
    _duan_builtin.列表追加(关键字列表, "中的")
    _duan_builtin.列表追加(关键字列表, "类")
    _duan_builtin.列表追加(关键字列表, "接口")
    return _duan_builtin.列表包含(关键字列表, 文本)

def 符号种别():
    符号字典 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(符号字典, "。", "句号")
    _duan_builtin.字典设置(符号字典, "，", "逗号")
    _duan_builtin.字典设置(符号字典, "：", "冒号")
    _duan_builtin.字典设置(符号字典, "（", "左括号")
    _duan_builtin.字典设置(符号字典, "）", "右括号")
    _duan_builtin.字典设置(符号字典, "【", "左方括号")
    _duan_builtin.字典设置(符号字典, "】", "右方括号")
    _duan_builtin.字典设置(符号字典, "《", "左书名号")
    _duan_builtin.字典设置(符号字典, "》", "右书名号")
    return 符号字典
