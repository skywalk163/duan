# 由段言编译器生成
# 源文件: 段言代码

import sys
import os

try:
    import importlib.util
except ImportError:
    importlib = None

# 解析 stdlib 路径（依次尝试多种可能）
_duan_stdlib = None
for _try_path in [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdlib'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stdlib'),
    os.path.join(os.getcwd(), 'stdlib'),
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'stdlib')),
]:
    if os.path.isdir(_try_path):
        _duan_stdlib = _try_path
        break

if _duan_stdlib and _duan_stdlib not in sys.path:
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
        _duan_builtin.读取行 = lambda: sys.stdin.readline().rstrip('\r\n')
        _duan_builtin.读取N字节 = lambda n: sys.stdin.read(n)
        _duan_builtin.写入输出 = lambda t: (sys.stdout.write(t), sys.stdout.flush()) and None
        _duan_builtin.打印输出 = lambda t: print(t, flush=True)
        _duan_builtin.刷新输出 = lambda: sys.stdout.flush()
        _duan_builtin.写入错误 = lambda t: (sys.stderr.write(t), sys.stderr.flush()) and None
        _duan_builtin.打印错误 = lambda t: print(t, file=sys.stderr, flush=True)
        _duan_builtin.解析JSON = lambda t: __import__('json').loads(t)
        _duan_builtin.序列化JSON = lambda v, i=None: (__import__('json').dumps(v, ensure_ascii=False, indent=i) if i is not None else __import__('json').dumps(v, ensure_ascii=False))
        _duan_builtin.美化JSON = lambda v: __import__('json').dumps(v, ensure_ascii=False, indent=2)
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
    _duan_builtin.读取行 = lambda: sys.stdin.readline().rstrip('\n')
    _duan_builtin.读取N字节 = lambda n: sys.stdin.read(n)
    _duan_builtin.写入输出 = lambda t: (sys.stdout.write(t), sys.stdout.flush()) and None
    _duan_builtin.打印输出 = lambda t: print(t, flush=True)
    _duan_builtin.刷新输出 = lambda: sys.stdout.flush()
    _duan_builtin.写入错误 = lambda t: (sys.stderr.write(t), sys.stderr.flush()) and None
    _duan_builtin.打印错误 = lambda t: print(t, file=sys.stderr, flush=True)
    _duan_builtin.解析JSON = lambda t: __import__('json').loads(t)
    _duan_builtin.序列化JSON = lambda v, i=None: (__import__('json').dumps(v, ensure_ascii=False, indent=i) if i is not None else __import__('json').dumps(v, ensure_ascii=False))
    _duan_builtin.美化JSON = lambda v: __import__('json').dumps(v, ensure_ascii=False, indent=2)
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

# 可空类型解包辅助函数
def _duan_unwrap(_x):
    assert _x is not None, "尝试解包空值"
    return _x

def 读取LSP消息():
    content_length = -1
    继续读取 = 1
    while (继续读取 == 1):
        行 = _duan_builtin.读取行()
        if (行 == ""):
            继续读取 = 0
        if (content_length == -1):
            部分 = _duan_builtin.分割字符串(行, ":")
            if (_duan_builtin.列表长度(部分) > 1):
                头 = _duan_builtin.列表获取(部分, 0)
                if (头 == "Content-Length"):
                    值字符串 = _duan_builtin.列表获取(部分, 1)
                    content_length = _duan_builtin.转整数(_duan_builtin.去除空白(值字符串))
    if (content_length > 0):
        body = _duan_builtin.读取N字节(content_length)
        消息 = _duan_builtin.解析JSON(body)
        return 消息
    else:
        return None

def 发送LSP响应(id, result):
    响应字典 = _duan_builtin.字典创建()
    _duan_builtin.字典设置(响应字典, "jsonrpc", "2.0")
    _duan_builtin.字典设置(响应字典, "id", id)
    _duan_builtin.字典设置(响应字典, "result", result)
    body = _duan_builtin.序列化JSON(响应字典)
    长度 = _duan_builtin.字符串长度(body)
    header = (("Content-Length: " + _duan_builtin.转字符串(长度)) + "\r\n\r\n")
    _duan_builtin.写入输出(header)
    _duan_builtin.写入输出(body)
    _duan_builtin.刷新输出()

def 获取诊断(文本):
    结果 = _duan_builtin.列表创建()
    行号 = 0
    行列表 = _duan_builtin.分割字符串(文本, "\n")
    索引 = 0
    while (索引 < _duan_builtin.列表长度(行列表)):
        本行内容 = _duan_builtin.列表获取(行列表, 索引)
        字符索引 = 0
        while (字符索引 < _duan_builtin.字符串长度(本行内容)):
            ch = _duan_builtin.字符串获取(本行内容, 字符索引)
            if (ch == "?"):
                诊断 = _duan_builtin.字典创建()
                _duan_builtin.字典设置(诊断, "range", _duan_builtin.字典创建())
                _duan_builtin.字典设置(_duan_builtin.字典获取(诊断, "range"), "start", _duan_builtin.字典创建())
                _duan_builtin.字典设置(_duan_builtin.字典获取(_duan_builtin.字典获取(诊断, "range"), "start"), "line", 索引)
                _duan_builtin.字典设置(_duan_builtin.字典获取(_duan_builtin.字典获取(诊断, "range"), "start"), "character", 字符索引)
                _duan_builtin.字典设置(_duan_builtin.字典获取(诊断, "range"), "end", _duan_builtin.字典创建())
                _duan_builtin.字典设置(_duan_builtin.字典获取(_duan_builtin.字典获取(诊断, "range"), "end"), "line", 索引)
                _duan_builtin.字典设置(_duan_builtin.字典获取(_duan_builtin.字典获取(诊断, "range"), "end"), "character", (字符索引 + 1))
                _duan_builtin.字典设置(诊断, "severity", 2)
                _duan_builtin.字典设置(诊断, "source", "duan-lsp")
                _duan_builtin.字典设置(诊断, "message", "发现可疑字符")
                _duan_builtin.列表追加(结果, 诊断)
            字符索引 = (字符索引 + 1)
        索引 = (索引 + 1)
    return 结果

def 获取补全(行, 字符位置):
    结果 = _duan_builtin.列表创建()
    关键词列表 = _duan_builtin.列表创建()
    _duan_builtin.列表追加(关键词列表, "段落")
    _duan_builtin.列表追加(关键词列表, "定义")
    _duan_builtin.列表追加(关键词列表, "等于")
    _duan_builtin.列表追加(关键词列表, "如果")
    _duan_builtin.列表追加(关键词列表, "那么")
    _duan_builtin.列表追加(关键词列表, "否则")
    _duan_builtin.列表追加(关键词列表, "当")
    _duan_builtin.列表追加(关键词列表, "结束")
    _duan_builtin.列表追加(关键词列表, "返回")
    _duan_builtin.列表追加(关键词列表, "打印输出")
    _duan_builtin.列表追加(关键词列表, "读取行")
    _duan_builtin.列表追加(关键词列表, "字典创建")
    _duan_builtin.列表追加(关键词列表, "列表创建")
    _duan_builtin.列表追加(关键词列表, "字典设置")
    _duan_builtin.列表追加(关键词列表, "字典获取")
    _duan_builtin.列表追加(关键词列表, "列表追加")
    _duan_builtin.列表追加(关键词列表, "解析JSON")
    _duan_builtin.列表追加(关键词列表, "序列化JSON")
    i = 0
    while (i < _duan_builtin.列表长度(关键词列表)):
        项 = _duan_builtin.字典创建()
        _duan_builtin.字典设置(项, "label", _duan_builtin.列表获取(关键词列表, i))
        _duan_builtin.字典设置(项, "kind", 14)
        _duan_builtin.列表追加(结果, 项)
        i = (i + 1)
    return 结果

def 主():
    _duan_builtin.打印错误("段言 LSP 服务器启动")
    运行中 = 1
    while (运行中 == 1):
        请求 = 读取LSP消息()
        if (请求 == None):
            _duan_builtin.打印错误("收到空消息，退出")
            运行中 = 0
        else:
            方法 = _duan_builtin.字典获取(请求, "method")
            请求id = _duan_builtin.字典获取(请求, "id")
            _duan_builtin.打印错误(("收到方法: " + _duan_builtin.转字符串(方法)))
            if (方法 == "initialize"):
                能力 = _duan_builtin.字典创建()
                _duan_builtin.字典设置(能力, "textDocumentSync", 1)
                _duan_builtin.字典设置(能力, "completionProvider", _duan_builtin.字典创建())
                _duan_builtin.字典设置(_duan_builtin.字典获取(能力, "completionProvider"), "triggerCharacters", _duan_builtin.列表创建())
                _duan_builtin.字典设置(能力, "hoverProvider", True)
                服务器信息 = _duan_builtin.字典创建()
                _duan_builtin.字典设置(服务器信息, "name", "duan-lsp")
                _duan_builtin.字典设置(服务器信息, "version", "1.0.0")
                初始化结果 = _duan_builtin.字典创建()
                _duan_builtin.字典设置(初始化结果, "capabilities", 能力)
                _duan_builtin.字典设置(初始化结果, "serverInfo", 服务器信息)
                发送LSP响应(请求id, 初始化结果)
            else:
                if (方法 == "textDocument/didChange"):
                    文档 = _duan_builtin.字典获取(请求, "params")
                    内容 = _duan_builtin.字典获取(_duan_builtin.字典获取(文档, "contentChanges"), 0)
                    文本 = _duan_builtin.字典获取(内容, "text")
                    诊断列表 = 获取诊断(文本)
                    pub_params = _duan_builtin.字典创建()
                    uri = _duan_builtin.字典获取(_duan_builtin.字典获取(文档, "textDocument"), "uri")
                    _duan_builtin.字典设置(pub_params, "uri", uri)
                    _duan_builtin.字典设置(pub_params, "diagnostics", 诊断列表)
                    完整通知 = _duan_builtin.字典创建()
                    _duan_builtin.字典设置(完整通知, "method", "textDocument/publishDiagnostics")
                    _duan_builtin.字典设置(完整通知, "params", pub_params)
                    body = _duan_builtin.序列化JSON(完整通知)
                    长度 = _duan_builtin.字符串长度(body)
                    header = (("Content-Length: " + _duan_builtin.转字符串(长度)) + "\r\n\r\n")
                    _duan_builtin.写入输出(header)
                    _duan_builtin.写入输出(body)
                    _duan_builtin.刷新输出()
                else:
                    if (方法 == "textDocument/didOpen"):
                        文档 = _duan_builtin.字典获取(请求, "params")
                        doc = _duan_builtin.字典获取(文档, "textDocument")
                        文本 = _duan_builtin.字典获取(doc, "text")
                        诊断列表 = 获取诊断(文本)
                        pub_params = _duan_builtin.字典创建()
                        _duan_builtin.字典设置(pub_params, "uri", _duan_builtin.字典获取(doc, "uri"))
                        _duan_builtin.字典设置(pub_params, "diagnostics", 诊断列表)
                        完整通知 = _duan_builtin.字典创建()
                        _duan_builtin.字典设置(完整通知, "method", "textDocument/publishDiagnostics")
                        _duan_builtin.字典设置(完整通知, "params", pub_params)
                        body = _duan_builtin.序列化JSON(完整通知)
                        长度 = _duan_builtin.字符串长度(body)
                        header = (("Content-Length: " + _duan_builtin.转字符串(长度)) + "\r\n\r\n")
                        _duan_builtin.写入输出(header)
                        _duan_builtin.写入输出(body)
                        _duan_builtin.刷新输出()
                    else:
                        if (方法 == "textDocument/completion"):
                            补全列表 = 获取补全("", 0)
                            发送LSP响应(请求id, 补全列表)
                        else:
                            if (方法 == "shutdown"):
                                发送LSP响应(请求id, None)
                                _duan_builtin.打印错误("收到 shutdown，准备退出")
                            else:
                                if (方法 == "exit"):
                                    运行中 = 0
                                    _duan_builtin.打印错误("LSP 服务器退出")
                                else:
                                    默认结果 = _duan_builtin.字典创建()
                                    _duan_builtin.字典设置(默认结果, "status", "ok")
                                    _duan_builtin.字典设置(默认结果, "method", 方法)
                                    发送LSP响应(请求id, 默认结果)


主()
