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

def 创建Token(类型, 值):
    Token = _duan_builtin.字典创建()
    _duan_builtin.字典设置(Token("类型"), 类型)
    _duan_builtin.字典设置(Token("值", 值))
    return Token

符号表 = _duan_builtin.字典创建()
_duan_builtin.字典设置(符号表("。", "DOT"))
_duan_builtin.字典设置(符号表("：", "COLON"))
_duan_builtin.字典设置(符号表("（", "LPAREN"))
_duan_builtin.字典设置(符号表("）", "RPAREN"))
双字关键 = _duan_builtin.列表创建()
_duan_builtin.列表追加(双字关键("定义"))
_duan_builtin.列表追加(双字关键("等于"))
_duan_builtin.列表追加(双字关键("如果"))
_duan_builtin.列表追加(双字关键("那么"))
_duan_builtin.列表追加(双字关键("否则"))
_duan_builtin.列表追加(双字关键("返回"))
_duan_builtin.列表追加(双字关键("遍历"))
_duan_builtin.列表追加(双字关键("当"))
_duan_builtin.列表追加(双字关键("导入"))
_duan_builtin.列表追加(双字关键("导出"))
简单数字 = _duan_builtin.列表创建()
_duan_builtin.列表追加(简单数字("一"))
_duan_builtin.列表追加(简单数字("二"))
_duan_builtin.列表追加(简单数字("三"))
_duan_builtin.列表追加(简单数字("四"))
_duan_builtin.列表追加(简单数字("五"))
_duan_builtin.列表追加(简单数字("六"))
_duan_builtin.列表追加(简单数字("七"))
_duan_builtin.列表追加(简单数字("八"))
_duan_builtin.列表追加(简单数字("九"))
_duan_builtin.列表追加(简单数字("十"))
中文数字 = _duan_builtin.字典创建()
_duan_builtin.字典设置(中文数字("零", 0))
_duan_builtin.字典设置(中文数字("一", 1))
_duan_builtin.字典设置(中文数字("二", 2))
_duan_builtin.字典设置(中文数字("三", 3))
_duan_builtin.字典设置(中文数字("四", 4))
_duan_builtin.字典设置(中文数字("五", 5))
_duan_builtin.字典设置(中文数字("六", 6))
_duan_builtin.字典设置(中文数字("七", 7))
_duan_builtin.字典设置(中文数字("八", 8))
_duan_builtin.字典设置(中文数字("九", 9))
_duan_builtin.字典设置(中文数字("十", 10))
def 分析词法(源码):
    结果 = _duan_builtin.列表创建()
    位置 = 0
    总字符数 = _duan_builtin.字符串长度(源码)
    while 位置(小于(总字符数)):
        字符 = 源码[位置]
        if 字符(等于(" ")):
            位置 = 位置(加(1))
            continue
            if 字符(等于("
")):
                位置 = 位置(加(1))
                continue
                if 字符(等于("#")):
                    while 位置(小于(总字符数)):
                        if (源码[位置] == "
"):
                            break
                            位置 = 位置(加(1))
                            continue
                            符号
