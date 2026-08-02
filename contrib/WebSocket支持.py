"""
WebSocket支持模块 - 长连接、双向通信

提供WebSocket功能，包括：
- 客户端连接
- 服务端支持
- 消息发送接收
- 连接管理
"""
import socket
import hashlib
import base64
import struct
import json
from typing import Dict, Any, Callable, Optional, List, Tuple
import threading


class WebSocket客户端:
    """WebSocket客户端类"""
    
    def __init__(self, URL: str):
        self._URL = URL
        self._连接 = None
        self._已连接 = False
        self._消息处理器 = None
        self._接收线程 = None
    
    def 连接(self):
        """建立连接"""
        from urllib.parse import urlparse
        
        解析 = urlparse(self._URL)
        主机 = 解析.hostname
        端口 = 解析.port or (443 if 解析.scheme == 'wss' else 80)
        
        self._连接 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._连接.connect((主机, 端口))
        
        # 发送握手请求
        键 = base64.b64encode(hashlib.sha1().hexdigest().encode()).decode()
        路径 = 解析.path or '/'
        if 解析.query:
            路径 += '?' + 解析.query
        
        握手请求 = (
            f'GET {路径} HTTP/1.1\r\n'
            f'Host: {主机}\r\n'
            f'Upgrade: websocket\r\n'
            f'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {键}\r\n'
            f'Sec-WebSocket-Version: 13\r\n'
            f'\r\n'
        )
        self._连接.send(握手请求.encode())
        
        # 接收握手响应
        响应 = self._连接.recv(4096).decode()
        if '101' in 响应.split('\n')[0] and 'Switching Protocols' in 响应:
            self._已连接 = True
            return True
        return False
    
    def 发送文本(self, 文本: str):
        """发送文本消息"""
        self._发送帧(文本.encode('utf-8'), opcode=1)
    
    def 发送JSON(self, 数据: Any):
        """发送JSON消息"""
        self._发送帧(json.dumps(数据).encode('utf-8'), opcode=1)
    
    def 发送二进制(self, 数据: bytes):
        """发送二进制消息"""
        self._发送帧(数据, opcode=2)
    
    def 接收(self) -> Optional[str]:
        """接收消息"""
        if not self._已连接:
            return None
        
        try:
            帧 = self._接收帧()
            if 帧:
                opcode, 数据 = 帧
                if opcode == 1:
                    return 数据.decode('utf-8')
                elif opcode == 2:
                    return 数据
            return None
        except:
            return None
    
    def 接收JSON(self) -> Any:
        """接收JSON消息"""
        消息 = self.接收()
        if 消息:
            try:
                return json.loads(消息)
            except:
                return None
        return None
    
    def 设置消息处理器(self, 处理器: Callable):
        """设置消息处理器"""
        self._消息处理器 = 处理器
    
    def 开始接收(self):
        """开始接收消息"""
        def 接收循环():
            while self._已连接:
                消息 = self.接收()
                if 消息 and self._消息处理器:
                    self._消息处理器(消息)
        
        self._接收线程 = threading.Thread(target=接收循环)
        self._接收线程.start()
    
    def 关闭(self):
        """关闭连接"""
        if self._已连接:
            self._发送帧(b'', opcode=8)
            self._已连接 = False
        if self._连接:
            self._连接.close()
    
    def 是否连接(self) -> bool:
        """检查是否已连接"""
        return self._已连接
    
    def _发送帧(self, 数据: bytes, opcode: int = 1):
        """发送WebSocket帧"""
        if not self._连接:
            return
        
        长度 = len(数据)
        
        if 长度 <= 125:
            头 = struct.pack('BB', 0x80 | opcode, 长度)
        elif 长度 <= 65535:
            头 = struct.pack('BBH', 0x80 | opcode, 126, 长度)
        else:
            头 = struct.pack('BBQ', 0x80 | opcode, 127, 长度)
        
        self._连接.send(头 + 数据)
    
    def _接收帧(self) -> Optional[Tuple[int, bytes]]:
        """接收WebSocket帧"""
        if not self._连接:
            return None
        
        头 = self._连接.recv(2)
        if not 头:
            return None
        
        opcode = 头[0] & 0x0f
        长度 = 头[1] & 0x7f
        
        if 长度 == 126:
            长度 = struct.unpack('>H', self._连接.recv(2))[0]
        elif 长度 == 127:
            长度 = struct.unpack('>Q', self._连接.recv(8))[0]
        
        if 头[1] & 0x80:
            mask = self._连接.recv(4)
        
        数据 = self._连接.recv(长度)
        
        if 头[1] & 0x80:
            数据 = bytes([数据[i] ^ mask[i % 4] for i in range(len(数据))])
        
        return opcode, 数据


class WebSocket服务端:
    """WebSocket服务端类"""
    
    def __init__(self, 主机: str = '127.0.0.1', 端口: int = 8765):
        self._主机 = 主机
        self._端口 = 端口
        self._服务socket = None
        self._客户端列表 = []
        self._消息处理器 = None
        self._连接处理器 = None
        self._运行中 = False
    
    def 设置消息处理器(self, 处理器: Callable):
        """设置消息处理器"""
        self._消息处理器 = 处理器
    
    def 设置连接处理器(self, 处理器: Callable):
        """设置连接处理器"""
        self._连接处理器 = 处理器
    
    def 启动(self):
        """启动服务"""
        self._服务socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._服务socket.bind((self._主机, self._端口))
        self._服务socket.listen(5)
        self._运行中 = True
        
        while self._运行中:
            客户端socket, 地址 = self._服务socket.accept()
            
            # 处理WebSocket握手
            请求 = 客户端socket.recv(4096).decode()
            
            if 'Upgrade: websocket' in 请求:
                键 = self._提取WebSocketKey(请求)
                接受键 = base64.b64encode(
                    hashlib.sha1((键 + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()
                ).decode()
                
                响应 = (
                    f'HTTP/1.1 101 Switching Protocols\r\n'
                    f'Upgrade: websocket\r\n'
                    f'Connection: Upgrade\r\n'
                    f'Sec-WebSocket-Accept: {接受键}\r\n'
                    f'\r\n'
                )
                客户端socket.send(响应.encode())
                
                客户端 = WebSocket客户端连接(客户端socket, 地址)
                self._客户端列表.append(客户端)
                
                if self._连接处理器:
                    self._连接处理器(客户端)
                
                threading.Thread(target=self._处理客户端, args=(客户端,)).start()
    
    def 停止(self):
        """停止服务"""
        self._运行中 = False
        for 客户端 in self._客户端列表:
            客户端.关闭()
        if self._服务socket:
            self._服务socket.close()
    
    def 广播(self, 消息: str):
        """广播消息给所有客户端"""
        for 客户端 in self._客户端列表:
            if 客户端.是否连接():
                客户端.发送文本(消息)
    
    def 广播JSON(self, 数据: Any):
        """广播JSON消息"""
        for 客户端 in self._客户端列表:
            if 客户端.是否连接():
                客户端.发送JSON(数据)
    
    def 发送给客户端(self, 客户端ID: str, 消息: str):
        """发送消息给指定客户端"""
        for 客户端 in self._客户端列表:
            if 客户端.获取ID() == 客户端ID:
                客户端.发送文本(消息)
                break
    
    def 获取客户端列表(self) -> List:
        """获取所有客户端"""
        return self._客户端列表
    
    def 获取客户端数量(self) -> int:
        """获取客户端数量"""
        return len(self._客户端列表)
    
    def _处理客户端(self, 客户端):
        """处理客户端消息"""
        while self._运行中 and 客户端.是否连接():
            消息 = 客户端.接收()
            if 消息:
                if self._消息处理器:
                    self._消息处理器(客户端, 消息)
    
    def _提取WebSocketKey(self, 请求: str) -> str:
        """提取WebSocket Key"""
        for 行 in 请求.split('\n'):
            if 'Sec-WebSocket-Key:' in 行:
                return 行.split(':')[1].strip()
        return ''


class WebSocket客户端连接:
    """WebSocket客户端连接类"""
    
    def __init__(self, socket, 地址):
        self._socket = socket
        self._地址 = 地址
        self._ID = str(hash(str(地址)))
        self._已连接 = True
    
    def 获取ID(self) -> str:
        """获取客户端ID"""
        return self._ID
    
    def 获取地址(self) -> tuple:
        """获取客户端地址"""
        return self._地址
    
    def 发送文本(self, 文本: str):
        """发送文本消息"""
        self._发送帧(文本.encode('utf-8'), opcode=1)
    
    def 发送JSON(self, 数据: Any):
        """发送JSON消息"""
        self._发送帧(json.dumps(数据).encode('utf-8'), opcode=1)
    
    def 发送二进制(self, 数据: bytes):
        """发送二进制消息"""
        self._发送帧(数据, opcode=2)
    
    def 接收(self) -> Optional[str]:
        """接收消息"""
        try:
            帧 = self._接收帧()
            if 帧:
                opcode, 数据 = 帧
                if opcode == 1:
                    return 数据.decode('utf-8')
                elif opcode == 2:
                    return 数据
            return None
        except:
            self._已连接 = False
            return None
    
    def 关闭(self):
        """关闭连接"""
        self._发送帧(b'', opcode=8)
        self._已连接 = False
        self._socket.close()
    
    def 是否连接(self) -> bool:
        """检查是否已连接"""
        return self._已连接
    
    def _发送帧(self, 数据: bytes, opcode: int = 1):
        """发送WebSocket帧"""
        长度 = len(数据)
        
        if 长度 <= 125:
            头 = struct.pack('BB', 0x80 | opcode, 长度)
        elif 长度 <= 65535:
            头 = struct.pack('BBH', 0x80 | opcode, 126, 长度)
        else:
            头 = struct.pack('BBQ', 0x80 | opcode, 127, 长度)
        
        self._socket.send(头 + 数据)
    
    def _接收帧(self) -> Optional[Tuple[int, bytes]]:
        """接收WebSocket帧"""
        头 = self._socket.recv(2)
        if not 头:
            return None
        
        opcode = 头[0] & 0x0f
        长度 = 头[1] & 0x7f
        
        if 长度 == 126:
            长度 = struct.unpack('>H', self._socket.recv(2))[0]
        elif 长度 == 127:
            长度 = struct.unpack('>Q', self._socket.recv(8))[0]
        
        数据 = self._socket.recv(长度)
        return opcode, 数据


def 创建WebSocket客户端(URL: str) -> WebSocket客户端:
    """创建WebSocket客户端实例"""
    return WebSocket客户端(URL)


def 创建WebSocket服务端(主机: str = '127.0.0.1', 端口: int = 8765) -> WebSocket服务端:
    """创建WebSocket服务端实例"""
    return WebSocket服务端(主机, 端口)


def WebSocket连接(URL: str) -> WebSocket客户端:
    """创建并连接WebSocket"""
    客户端 = WebSocket客户端(URL)
    客户端.连接()
    return 客户端


def 发送WebSocket消息(URL: str, 消息: str) -> bool:
    """发送WebSocket消息"""
    客户端 = WebSocket连接(URL)
    if 客户端.是否连接():
        客户端.发送文本(消息)
        客户端.关闭()
        return True
    return False


def 接收WebSocket消息(URL: str) -> Optional[str]:
    """接收WebSocket消息"""
    客户端 = WebSocket连接(URL)
    if 客户端.是否连接():
        消息 = 客户端.接收()
        客户端.关闭()
        return 消息
    return None