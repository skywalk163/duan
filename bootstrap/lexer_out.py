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

__all__ = ['词法分析']
from 字符串处理 import 截取
def 创建关键字列表():
    列表 = _duan_builtin.列表创建()
    _duan_builtin.列表追加(列表, "定义")
    _duan_builtin.列表追加(列表, "等于")
    _duan_builtin.列表追加(列表, "如果")
    _duan_builtin.列表追加(列表, "那么")
    _duan_builtin.列表追加(列表, "否则")
    _duan_builtin.列表追加(列表, "返回")
    _duan_builtin.列表追加(列表, "段")
    _duan_builtin.列表追加(列表, "结束")
    _duan_builtin.列表追加(列表, "当")
    _duan_builtin.列表追加(列表, "遍历")
    _duan_builtin.列表追加(列表, "跳过")
    _duan_builtin.列表追加(列表, "跳出")
    _duan_builtin.列表追加(列表, "打印")
    _duan_builtin.列表追加(列表, "导入")
    _duan_builtin.列表追加(列表, "导出")
    _duan_builtin.列表追加(列表, "设")
    _duan_builtin.列表追加(列表, "为")
    _duan_builtin.列表追加(列表, "尝试")
    _duan_builtin.列表追加(列表, "捕获")
    _duan_builtin.列表追加(列表, "抛出")
    _duan_builtin.列表追加(列表, "从")
    _duan_builtin.列表追加(列表, "中的")
    _duan_builtin.列表追加(列表, "类")
    _duan_builtin.列表追加(列表, "接口")
    _duan_builtin.列表追加(列表, "加上")
    _duan_builtin.列表追加(列表, "减去")
    _duan_builtin.列表追加(列表, "乘以")
    _duan_builtin.列表追加(列表, "除以")
    _duan_builtin.列表追加(列表, "模以")
    _duan_builtin.列表追加(列表, "幂以")
    _duan_builtin.列表追加(列表, "真")
    _duan_builtin.列表追加(列表, "假")
    _duan_builtin.列表追加(列表, "空")
    _duan_builtin.列表追加(列表, "且")
    _duan_builtin.列表追加(列表, "或")
    _duan_builtin.列表追加(列表, "不")
    return 列表

def 创建符号映射():
    映射 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(映射, "。", "句号")
    _duan_builtin.字典设置(映射, "，", "逗号")
    _duan_builtin.字典设置(映射, "：", "冒号")
    _duan_builtin.字典设置(映射, "（", "左括号")
    _duan_builtin.字典设置(映射, "）", "右括号")
    _duan_builtin.字典设置(映射, "【", "左方括号")
    _duan_builtin.字典设置(映射, "】", "右方括号")
    _duan_builtin.字典设置(映射, "《", "左书名号")
    _duan_builtin.字典设置(映射, "》", "右书名号")
    _duan_builtin.字典设置(映射, "「", "左引号")
    _duan_builtin.字典设置(映射, "」", "右引号")
    _duan_builtin.字典设置(映射, "『", "左单引号")
    _duan_builtin.字典设置(映射, "』", "右单引号")
    _duan_builtin.字典设置(映射, ".", "点")
    _duan_builtin.字典设置(映射, ",", "逗号")
    _duan_builtin.字典设置(映射, ":", "冒号")
    _duan_builtin.字典设置(映射, "(", "左括号")
    _duan_builtin.字典设置(映射, ")", "右括号")
    _duan_builtin.字典设置(映射, "[", "左方括号")
    _duan_builtin.字典设置(映射, "]", "右方括号")
    _duan_builtin.字典设置(映射, "<", "左书名号")
    _duan_builtin.字典设置(映射, ">", "右书名号")
    _duan_builtin.字典设置(映射, "\\", "反斜杠")
    _duan_builtin.字典设置(映射, "=", "等号")
    _duan_builtin.字典设置(映射, "@", "at")
    _duan_builtin.字典设置(映射, "+", "加号")
    return 映射

def 是空白(字符):
    return (((字符 == " ") or (字符 == "	")) or (字符 == ""))

def 是数字(字符):
    return ((字符 >= "0") and (字符 <= "9"))

def 是字母(字符):
    return ((((字符 >= "a") and (字符 <= "z")) or ((字符 >= "A") and (字符 <= "Z"))) or (字符 == "_"))

def 是标识符字符(字符, 符号字典):
    if 是空白(字符):
        return False
    if (字符 == "
"):
        return False
    if ((字符 == "\"") or (字符 == "'")):
        return False
    if _duan_builtin.字典包含键(符号字典, 字符):
        return False
    return True

def 匹配关键字(文本, 关键字列表):
    最佳关键字 = None
    索引 = 0
    列表长度 = _duan_builtin.列表长度(关键字列表)
    while (索引 < 列表长度):
        关键字 = _duan_builtin.列表获取(关键字列表, 索引)
        关键字长度 = _duan_builtin.字符串长度(关键字)
        文本长度 = _duan_builtin.字符串长度(文本)
        if ((关键字长度 > 0) and (关键字长度 <= 文本长度)):
            if (截取(文本, 0, 关键字长度) == 关键字):
                if ((最佳关键字 == None) or (关键字长度 > _duan_builtin.字符串长度(最佳关键字))):
                    最佳关键字 = 关键字
                    索引 = (索引 + 1)
                    return 最佳关键字
                def 收集标识符文本(源码, 位置, 符号字典):
                    结果 = ""
                    源码长度 = _duan_builtin.字符串长度(源码)
                    while (位置 < 源码长度):
                        字符 = 字符串获取(源码, 位置)
                        if 是标识符字符(字符, 符号字典):
                            结果 = (结果 + 字符)
                            位置 = (位置 + 1)
                        else:
                            break
                            return 结果
                        def 标识符分词(文本, 关键字列表, 行, 列):
                            结果 = _duan_builtin.列表创建()
                            剩余文本 = 文本
                            当前列 = 列
                            while (_duan_builtin.字符串长度(剩余文本) > 0):
                                找到关键字 = 匹配关键字(剩余文本, 关键字列表)
                                if (找到关键字 != None):
                                    找到长度 = _duan_builtin.字符串长度(找到关键字)
                                    _duan_builtin.列表追加(结果, 创建令牌("关键字", 找到关键字, 行, 当前列))
                                    当前列 = (当前列 + 找到长度)
                                    剩余文本 = 截取(剩余文本, 找到长度, _duan_builtin.字符串长度(剩余文本))
                                else:
                                    _duan_builtin.列表追加(结果, 创建令牌("标识符", 剩余文本, 行, 当前列))
                                    剩余文本 = ""
                                    return 结果
                                def 跳到行尾(源码, 位置):
                                    源码长度 = _duan_builtin.字符串长度(源码)
                                    while (位置 < 源码长度):
                                        字符 = 字符串获取(源码, 位置)
                                        if (字符 == "
"):
                                            return 位置
                                            位置 = (位置 + 1)
                                            return 位置
                                        def 词法分析(源码):
                                            令牌列表 = _duan_builtin.列表创建()
                                            源码长度 = _duan_builtin.字符串长度(源码)
                                            位置 = 0
                                            行 = 1
                                            列 = 1
                                            缩进栈 = _duan_builtin.列表创建()
                                            _duan_builtin.列表追加(缩进栈, 0)
                                            关键字列表 = 创建关键字列表()
                                            符号映射 = 创建符号映射()
                                            while (位置 < 源码长度):
                                                字符 = 字符串获取(源码, 位置)
                                                if (字符 == "
"):
                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("换行", "
", 行, 列))
                                                    行 = (行 + 1)
                                                    列 = 1
                                                    位置 = (位置 + 1)
                                                    缩进 = 0
                                                    while (位置 < 源码长度):
                                                        下一个 = 字符串获取(源码, 位置)
                                                        if (下一个 == " "):
                                                            缩进 = (缩进 + 1)
                                                            位置 = (位置 + 1)
                                                        else:
                                                            if (下一个 == "	"):
                                                                缩进 = (缩进 + 4)
                                                                位置 = (位置 + 1)
                                                            else:
                                                                break
                                                                列 = (缩进 + 1)
                                                                栈顶 = _duan_builtin.列表获取(缩进栈, (_duan_builtin.列表长度(缩进栈) - 1))
                                                                if (缩进 > 栈顶):
                                                                    _duan_builtin.列表追加(缩进栈, 缩进)
                                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("缩进", 缩进, 行, 1))
                                                                else:
                                                                    if (缩进 < 栈顶):
                                                                        while (_duan_builtin.列表获取(缩进栈, (_duan_builtin.列表长度(缩进栈) - 1)) > 缩进):
                                                                            _duan_builtin.列表弹出(缩进栈)
                                                                            _duan_builtin.列表追加(令牌列表, 创建令牌("反缩进", _duan_builtin.列表获取(缩进栈, (_duan_builtin.列表长度(缩进栈) - 1)), 行, 1))
                                                                            continue
                                                                            if 是空白(字符):
                                                                                列 = (列 + 1)
                                                                                位置 = (位置 + 1)
                                                                                continue
                                                                                if (字符 == "#"):
                                                                                    位置 = 跳到行尾(源码, 位置)
                                                                                    continue
                                                                                    if ((字符 == "/") and ((位置 + 1) < 源码长度)):
                                                                                        下一个字符 = 字符串获取(源码, (位置 + 1))
                                                                                        if (下一个字符 == "/"):
                                                                                            位置 = 跳到行尾(源码, 位置)
                                                                                            continue
                                                                                            if (字符 == "注"):
                                                                                                位置备份 = 位置
                                                                                                位置 = 跳到行尾(源码, 位置)
                                                                                                消耗 = (位置 - 位置备份)
                                                                                                if (消耗 == 1):
                                                                                                    位置 = 位置备份
                                                                                                else:
                                                                                                    continue
                                                                                                    if (字符 == "-"):
                                                                                                        if (((位置 + 1) < 源码长度) and (字符串获取(源码, (位置 + 1)) == ">")):
                                                                                                            _duan_builtin.列表追加(令牌列表, 创建令牌("箭头", "->", 行, 列))
                                                                                                            列 = (列 + 2)
                                                                                                            位置 = (位置 + 2)
                                                                                                            continue
                                                                                                            if (字符 == "《"):
                                                                                                                _duan_builtin.列表追加(令牌列表, 创建令牌("左书名号", "《", 行, 列))
                                                                                                                列 = (列 + 1)
                                                                                                                位置 = (位置 + 1)
                                                                                                                名称 = ""
                                                                                                                while (位置 < 源码长度):
                                                                                                                    名称字符 = 字符串获取(源码, 位置)
                                                                                                                    if (名称字符 == "》"):
                                                                                                                        break
                                                                                                                        名称 = (名称 + 名称字符)
                                                                                                                        位置 = (位置 + 1)
                                                                                                                        列 = (列 + 1)
                                                                                                                        _duan_builtin.列表追加(令牌列表, 创建令牌("标识符", 名称, 行, 列))
                                                                                                                        if (位置 < 源码长度):
                                                                                                                            列 = (列 + 1)
                                                                                                                            位置 = (位置 + 1)
                                                                                                                            _duan_builtin.列表追加(令牌列表, 创建令牌("右书名号", "》", 行, 列))
                                                                                                                            continue
                                                                                                                            if _duan_builtin.字典包含键(符号映射, 字符):
                                                                                                                                符号种别 = _duan_builtin.字典获取(符号映射, 字符)
                                                                                                                                _duan_builtin.列表追加(令牌列表, 创建令牌(符号种别, 字符, 行, 列))
                                                                                                                                列 = (列 + 1)
                                                                                                                                位置 = (位置 + 1)
                                                                                                                                continue
                                                                                                                                if ((字符 == "\"") or (字符 == "'")):
                                                                                                                                    字符串结果 = ""
                                                                                                                                    起始位置 = 位置
                                                                                                                                    位置 = (位置 + 1)
                                                                                                                                    while (位置 < 源码长度):
                                                                                                                                        字符串字符 = 字符串获取(源码, 位置)
                                                                                                                                        if (字符串字符 == 字符):
                                                                                                                                            位置 = (位置 + 1)
                                                                                                                                            break
                                                                                                                                        else:
                                                                                                                                            if (字符串字符 == "\\"):
                                                                                                                                                位置 = (位置 + 1)
                                                                                                                                                if (位置 < 源码长度):
                                                                                                                                                    转义字符 = 字符串获取(源码, 位置)
                                                                                                                                                    if (转义字符 == "n"):
                                                                                                                                                        字符串结果 = (字符串结果 + "
")
                                                                                                                                                    else:
                                                                                                                                                        if (转义字符 == "t"):
                                                                                                                                                            字符串结果 = (字符串结果 + "	")
                                                                                                                                                        else:
                                                                                                                                                            字符串结果 = (字符串结果 + 转义字符)
                                                                                                                                                            位置 = (位置 + 1)
                                                                                                                                                else:
                                                                                                                                                    字符串结果 = (字符串结果 + 字符串字符)
                                                                                                                                                    位置 = (位置 + 1)
                                                                                                                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("字符串", 字符串结果, 行, 列))
                                                                                                                                                    列 = (列 + (位置 - 起始位置))
                                                                                                                                                    continue
                                                                                                                                                    if (是数字(字符) or (((字符 == "-") and ((位置 + 1) < 源码长度)) and 是数字(字符串获取(源码, (位置 + 1))))):
                                                                                                                                                        数字开始 = 位置
                                                                                                                                                        是负数 = False
                                                                                                                                                        if (字符 == "-"):
                                                                                                                                                            是负数 = True
                                                                                                                                                            位置 = (位置 + 1)
                                                                                                                                                            数字字符串 = ""
                                                                                                                                                            if 是负数:
                                                                                                                                                                数字字符串 = "-"
                                                                                                                                                                while (位置 < 源码长度):
                                                                                                                                                                    数字字符 = 字符串获取(源码, 位置)
                                                                                                                                                                    if 是数字(数字字符):
                                                                                                                                                                        数字字符串 = (数字字符串 + 数字字符)
                                                                                                                                                                        位置 = (位置 + 1)
                                                                                                                                                                    else:
                                                                                                                                                                        break
                                                                                                                                                                        if ((位置 < 源码长度) and (字符串获取(源码, 位置) == ".")):
                                                                                                                                                                            下一个下一个 = (位置 + 1)
                                                                                                                                                                            if ((下一个下一个 < 源码长度) and 是数字(字符串获取(源码, 下一个下一个))):
                                                                                                                                                                                数字字符串 = (数字字符串 + ".")
                                                                                                                                                                                位置 = (位置 + 1)
                                                                                                                                                                                while (位置 < 源码长度):
                                                                                                                                                                                    数字字符 = 字符串获取(源码, 位置)
                                                                                                                                                                                    if 是数字(数字字符):
                                                                                                                                                                                        数字字符串 = (数字字符串 + 数字字符)
                                                                                                                                                                                        位置 = (位置 + 1)
                                                                                                                                                                                    else:
                                                                                                                                                                                        break
                                                                                                                                                                                        _duan_builtin.列表追加(令牌列表, 创建令牌("数字", 数字字符串, 行, 列))
                                                                                                                                                                                        列 = (列 + (位置 - 数字开始))
                                                                                                                                                                                        continue
                                                                                                                                                                                        if ((字符 > "x7F") or 是字母(字符)):
                                                                                                                                                                                            标识符文本 = 收集标识符文本(源码, 位置, 符号映射)
                                                                                                                                                                                            标识符长度 = _duan_builtin.字符串长度(标识符文本)
                                                                                                                                                                                            if (标识符长度 > 0):
                                                                                                                                                                                                分词结果 = 标识符分词(标识符文本, 关键字列表, 行, 列)
                                                                                                                                                                                                分词索引 = 0
                                                                                                                                                                                                while (分词索引 < _duan_builtin.列表长度(分词结果)):
                                                                                                                                                                                                    _duan_builtin.列表追加(令牌列表, _duan_builtin.列表获取(分词结果, 分词索引))
                                                                                                                                                                                                    分词索引 = (分词索引 + 1)
                                                                                                                                                                                                    位置 = (位置 + 标识符长度)
                                                                                                                                                                                                    列 = (列 + 标识符长度)
                                                                                                                                                                                                    continue
                                                                                                                                                                                                    错误消息 = "未知字符"
                                                                                                                                                                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("错误", 错误消息, 行, 列))
                                                                                                                                                                                                    位置 = (位置 + 1)
                                                                                                                                                                                                    列 = (列 + 1)
                                                                                                                                                                                                while (_duan_builtin.列表长度(缩进栈) > 1):
                                                                                                                                                                                                    _duan_builtin.列表弹出(缩进栈)
                                                                                                                                                                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("反缩进", _duan_builtin.列表获取(缩进栈, (_duan_builtin.列表长度(缩进栈) - 1)), 行, 列))
                                                                                                                                                                                                    _duan_builtin.列表追加(令牌列表, 创建令牌("结束", None, 行, 列))
                                                                                                                                                                                                    return 令牌列表




