"""
HTTP服务端模块 - 路由、中间件、静态文件

提供HTTP服务端功能，包括：
- 路由注册
- 中间件支持
- 静态文件服务
- 请求解析
- 响应构建
"""
import http.server
import socketserver
import json
import os
import mimetypes
from typing import Dict, Any, Callable, List, Optional
from urllib.parse import parse_qs, urlparse


class HTTP请求:
    """HTTP请求类"""
    
    def __init__(self, 请求对象):
        self._请求对象 = 请求对象
        self._路径 = urlparse(请求对象.path).path
        self._查询参数 = parse_qs(urlparse(请求对象.path).query)
        self._请求头 = dict(请求对象.headers)
        self._方法 = 请求对象.command
        self._正文 = None
        self._JSON = None
    
    def 获取路径(self) -> str:
        """获取请求路径"""
        return self._路径
    
    def 获取方法(self) -> str:
        """获取请求方法"""
        return self._方法
    
    def 获取查询参数(self, 名称: str = None) -> Any:
        """获取查询参数"""
        if 名称:
            值列表 = self._查询参数.get(名称, [])
            return 值列表[0] if 值列表 else None
        return {k: v[0] for k, v in self._查询参数.items()}
    
    def 获取请求头(self, 名称: str = None) -> Any:
        """获取请求头"""
        if 名称:
            return self._请求头.get(名称)
        return self._请求头
    
    def 获取正文(self) -> bytes:
        """获取请求正文"""
        if self._正文 is None:
            长度 = int(self._请求头.get('Content-Length', 0))
            self._正文 = self._请求对象.rfile.read(长度)
        return self._正文
    
    def 获取JSON(self) -> Any:
        """获取JSON数据"""
        if self._JSON is None:
            try:
                正文 = self.获取正文()
                self._JSON = json.loads(正文.decode('utf-8'))
            except:
                self._JSON = None
        return self._JSON
    
    def 获取表单数据(self) -> Dict[str, str]:
        """获取表单数据"""
        正文 = self.获取正文().decode('utf-8')
        数据 = parse_qs(正文)
        return {k: v[0] for k, v in 数据.items()}


class HTTP响应:
    """HTTP响应类"""
    
    def __init__(self):
        self._状态码 = 200
        self._响应头 = {'Content-Type': 'text/html; charset=utf-8'}
        self._正文 = b''
    
    def 设置状态码(self, 状态码: int):
        """设置状态码"""
        self._状态码 = 状态码
    
    def 设置响应头(self, 名称: str, 值: str):
        """设置响应头"""
        self._响应头[名称] = 值
    
    def 设置正文(self, 正文: str):
        """设置正文"""
        self._正文 = 正文.encode('utf-8')
    
    def 设置JSON(self, 数据: Any):
        """设置JSON响应"""
        self._响应头['Content-Type'] = 'application/json; charset=utf-8'
        self._正文 = json.dumps(数据, ensure_ascii=False).encode('utf-8')
    
    def 设置HTML(self, HTML: str):
        """设置HTML响应"""
        self._响应头['Content-Type'] = 'text/html; charset=utf-8'
        self._正文 = HTML.encode('utf-8')
    
    def 设置文本(self, 文本: str):
        """设置文本响应"""
        self._响应头['Content-Type'] = 'text/plain; charset=utf-8'
        self._正文 = 文本.encode('utf-8')
    
    def 设置二进制(self, 数据: bytes, 类型: str = 'application/octet-stream'):
        """设置二进制响应"""
        self._响应头['Content-Type'] = 类型
        self._正文 = 数据
    
    def 重定向(self, URL: str, 状态码: int = 302):
        """重定向"""
        self._状态码 = 状态码
        self._响应头['Location'] = URL
    
    def 获取状态码(self) -> int:
        """获取状态码"""
        return self._状态码
    
    def 获取响应头(self) -> Dict[str, str]:
        """获取响应头"""
        return self._响应头
    
    def 获取正文(self) -> bytes:
        """获取正文"""
        return self._正文


class HTTP服务端:
    """HTTP服务端类"""
    
    def __init__(self, 主机: str = '127.0.0.1', 端口: int = 8080):
        self._主机 = 主机
        self._端口 = 端口
        self._路由 = {}
        self._中间件 = []
        self._静态文件目录 = None
        self._服务 = None
    
    def 路由(self, 路径: str, 方法: str = 'GET'):
        """路由装饰器"""
        def 包装(函数):
            键 = f'{方法.upper()}:{路径}'
            self._路由[键] = 函数
            return 函数
        return 包装
    
    def 注册路由(self, 路径: str, 函数: Callable, 方法: str = 'GET'):
        """注册路由"""
        键 = f'{方法.upper()}:{路径}'
        self._路由[键] = 函数
    
    def GET(self, 路径: str):
        """GET路由装饰器"""
        return self.路由(路径, 'GET')
    
    def POST(self, 路径: str):
        """POST路由装饰器"""
        return self.路由(路径, 'POST')
    
    def PUT(self, 路径: str):
        """PUT路由装饰器"""
        return self.路由(路径, 'PUT')
    
    def DELETE(self, 路径: str):
        """DELETE路由装饰器"""
        return self.路由(路径, 'DELETE')
    
    def 添加中间件(self, 函数: Callable):
        """添加中间件"""
        self._中间件.append(函数)
    
    def 设置静态文件目录(self, 目录: str):
        """设置静态文件目录"""
        self._静态文件目录 = 目录
    
    def 启动(self, 阻塞: bool = True):
        """启动服务"""
        处理器类 = self._创建处理器类()
        self._服务 = socketserver.TCPServer((self._主机, self._端口), 处理器类)
        
        if 阻塞:
            self._服务.serve_forever()
        else:
            import threading
            线程 = threading.Thread(target=self._服务.serve_forever)
            线程.start()
    
    def 停止(self):
        """停止服务"""
        if self._服务:
            self._服务.shutdown()
            self._服务.server_close()
    
    def _创建处理器类(self):
        """创建请求处理器类"""
        服务端实例 = self
        
        class 请求处理器(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self._处理请求('GET')
            
            def do_POST(self):
                self._处理请求('POST')
            
            def do_PUT(self):
                self._处理请求('PUT')
            
            def do_DELETE(self):
                self._处理请求('DELETE')
            
            def _处理请求(self, 方法):
                请求 = HTTP请求(self)
                响应 = HTTP响应()
                
                # 执行中间件
                for 中间件 in 服务端实例._中间件:
                    结果 = 中间件(请求, 响应)
                    if 结果 == False:
                        self._发送响应(响应)
                        return
                
                # 查找路由
                键 = f'{方法}:{请求.获取路径()}'
                处理函数 = 服务端实例._路由.get(键)
                
                if 处理函数:
                    try:
                        处理函数(请求, 响应)
                    except Exception as e:
                        响应.设置状态码(500)
                        响应.设置JSON({'错误': str(e)})
                elif 服务端实例._静态文件目录:
                    文件路径 = os.path.join(服务端实例._静态文件目录, 请求.获取路径().lstrip('/'))
                    if os.path.exists(文件路径) and os.path.isfile(文件路径):
                        self._发送静态文件(文件路径, 响应)
                    else:
                        响应.设置状态码(404)
                        响应.设置文本('404 Not Found')
                else:
                    响应.设置状态码(404)
                    响应.设置文本('404 Not Found')
                
                self._发送响应(响应)
            
            def _发送响应(self, 响应):
                """发送响应"""
                self.send_response(响应.获取状态码())
                for 名称, 值 in 响应.获取响应头().items():
                    self.send_header(名称, 值)
                self.end_headers()
                self.wfile.write(响应.获取正文())
            
            def _发送静态文件(self, 文件路径, 响应):
                """发送静态文件"""
                try:
                    mime类型, _ = mimetypes.guess_type(文件路径)
                    if not mime类型:
                        mime类型 = 'application/octet-stream'
                    
                    with open(文件路径, 'rb') as f:
                        内容 = f.read()
                    
                    响应.设置响应头('Content-Type', mime类型)
                    响应.设置响应头('Content-Length', str(len(内容)))
                    响应.设置二进制(内容, mime类型)
                except Exception as e:
                    响应.设置状态码(500)
                    响应.设置文本(f'500 Internal Server Error: {e}')
        
        return 请求处理器


def 创建HTTP服务端(主机: str = '127.0.0.1', 端口: int = 8080) -> HTTP服务端:
    """创建HTTP服务端实例"""
    return HTTP服务端(主机, 端口)


def 创建请求(请求对象) -> HTTP请求:
    """创建请求实例"""
    return HTTP请求(请求对象)


def 创建响应() -> HTTP响应:
    """创建响应实例"""
    return HTTP响应()


def 返回JSON(数据: Any) -> HTTP响应:
    """返回JSON响应"""
    响应 = HTTP响应()
    响应.设置JSON(数据)
    return 响应


def 返回HTML(HTML: str) -> HTTP响应:
    """返回HTML响应"""
    响应 = HTTP响应()
    响应.设置HTML(HTML)
    return 响应


def 返回文本(文本: str, 状态码: int = 200) -> HTTP响应:
    """返回文本响应"""
    响应 = HTTP响应()
    响应.设置状态码(状态码)
    响应.设置文本(文本)
    return 响应


def 返回404(消息: str = '404 Not Found') -> HTTP响应:
    """返回404响应"""
    响应 = HTTP响应()
    响应.设置状态码(404)
    响应.设置文本(消息)
    return 响应


def 返回500(消息: str = '500 Internal Server Error') -> HTTP响应:
    """返回500响应"""
    响应 = HTTP响应()
    响应.设置状态码(500)
    响应.设置文本(消息)
    return 响应


def 返回重定向(URL: str) -> HTTP响应:
    """返回重定向响应"""
    响应 = HTTP响应()
    响应.重定向(URL)
    return 响应


def CORS中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
    """CORS中间件"""
    响应.设置响应头('Access-Control-Allow-Origin', '*')
    响应.设置响应头('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    响应.设置响应头('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    if 请求.获取方法() == 'OPTIONS':
        响应.设置状态码(200)
        return False
    
    return True


def JSON中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
    """JSON中间件"""
    if 请求.获取请求头('Content-Type') == 'application/json':
        请求._JSON = 请求.获取JSON()
    return True


def 日志中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
    """日志中间件"""
    print(f'{请求.获取方法()} {请求.获取路径()}')
    return True


def 静态文件中间件(目录: str) -> Callable:
    """静态文件中间件"""
    def 中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
        路径 = 请求.获取路径().lstrip('/')
        文件路径 = os.path.join(目录, 路径)
        
        if os.path.exists(文件路径) and os.path.isfile(文件路径):
            mime类型, _ = mimetypes.guess_type(文件路径)
            if not mime类型:
                mime类型 = 'application/octet-stream'
            
            with open(文件路径, 'rb') as f:
                内容 = f.read()
            
            响应.设置响应头('Content-Type', mime类型)
            响应.设置二进制(内容, mime类型)
            return False
        
        return True
    
    return 中间件


def 基础认证中间件(用户名: str, 密码: str) -> Callable:
    """基础认证中间件"""
    def 中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
        认证头 = 请求.获取请求头('Authorization')
        
        if not 认证头:
            响应.设置状态码(401)
            响应.设置响应头('WWW-Authenticate', 'Basic realm="Login Required"')
            响应.设置文本('401 Unauthorized')
            return False
        
        try:
            import base64
            编码 = 认证头.replace('Basic ', '')
            解码 = base64.b64decode(编码).decode()
            用户, 密 = 解码.split(':')
            
            if 用户 == 用户名 and 密 == 密码:
                return True
            else:
                响应.设置状态码(401)
                响应.设置文本('401 Unauthorized')
                return False
        except:
            响应.设置状态码(401)
            响应.设置文本('401 Unauthorized')
            return False
    
    return 中间件


def 速率限制中间件(限制: int = 100, 时间窗口: int = 60) -> Callable:
    """速率限制中间件"""
    请求计数 = {}
    
    def 中间件(请求: HTTP请求, 响应: HTTP响应) -> bool:
        import time
        客户端 = 请求.获取请求头('X-Forwarded-For') or 'unknown'
        当前时间 = time.time()
        
        if 客户端 not in 请求计数:
            请求计数[客户端] = {'次数': 0, '开始时间': 当前时间}
        
        数据 = 请求计数[客户端]
        
        if 当前时间 - 数据['开始时间'] > 时间窗口:
            数据['次数'] = 0
            数据['开始时间'] = 当前时间
        
        数据['次数'] += 1
        
        if 数据['次数'] > 限制:
            响应.设置状态码(429)
            响应.设置文本('429 Too Many Requests')
            return False
        
        return True
    
    return 中间件