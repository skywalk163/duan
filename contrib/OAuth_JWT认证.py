"""
OAuth/JWT认证模块 - 令牌生成与验证

提供身份认证功能，包括：
- JWT令牌生成与验证
- OAuth2.0简化流程
- 令牌刷新
- 密码哈希
- 会话管理
"""
import hashlib
import hmac
import base64
import json
import time
import secrets
import os
from typing import Any, Callable, Dict, List, Optional, Tuple


class JWT异常(Exception):
    """JWT异常"""
    pass


class 令牌过期异常(JWT异常):
    """令牌过期异常"""
    pass


class 令牌无效异常(JWT异常):
    """令牌无效异常"""
    pass


class 密码工具:
    """密码哈希工具"""
    
    @staticmethod
    def 哈希密码(密码: str, 盐值: str = None, 迭代次数: int = 100000) -> Tuple[str, str]:
        """哈希密码"""
        if 盐值 is None:
            盐值 = secrets.token_hex(16)
        
        哈希值 = hashlib.pbkdf2_hmac(
            'sha256',
            密码.encode('utf-8'),
            盐值.encode('utf-8'),
            迭代次数
        )
        
        return base64.b64encode(哈希值).decode('utf-8'), 盐值
    
    @staticmethod
    def 验证密码(密码: str, 哈希值: str, 盐值: str, 迭代次数: int = 100000) -> bool:
        """验证密码"""
        新哈希, _ = 密码工具.哈希密码(密码, 盐值, 迭代次数)
        return hmac.compare_digest(新哈希, 哈希值)
    
    @staticmethod
    def 生成随机密码(长度: int = 16) -> str:
        """生成随机密码"""
        字符集 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
        return ''.join(secrets.choice(字符集) for _ in range(长度))


class JWT令牌:
    """JWT令牌工具"""
    
    def __init__(self, 密钥: str, 算法: str = 'HS256', 过期时间: int = 3600):
        self._密钥 = 密钥
        self._算法 = 算法
        self._过期时间 = 过期时间
    
    def _base64url编码(self, 数据: bytes) -> str:
        """Base64URL编码"""
        return base64.urlsafe_b64encode(数据).rstrip(b'=').decode('utf-8')
    
    def _base64url解码(self, 数据: str) -> bytes:
        """Base64URL解码"""
        填充 = 4 - len(数据) % 4
        if 填充 != 4:
            数据 += '=' * 填充
        return base64.urlsafe_b64decode(数据)
    
    def _获取算法函数(self) -> str:
        """获取哈希算法名称"""
        算法映射 = {
            'HS256': 'sha256',
            'HS384': 'sha384',
            'HS512': 'sha512',
        }
        return 算法映射.get(self._算法, 'sha256')
    
    def 生成令牌(self, 载荷: Dict[str, Any]) -> str:
        """生成JWT令牌"""
        头部 = {
            'alg': self._算法,
            'typ': 'JWT'
        }
        
        当前时间 = int(time.time())
        载荷['iat'] = 当前时间
        载荷['exp'] = 当前时间 + self._过期时间
        载荷['jti'] = secrets.token_hex(8)
        
        编码头 = self._base64url编码(json.dumps(头部).encode('utf-8'))
        编码载荷 = self._base64url编码(json.dumps(载荷).encode('utf-8'))
        
        签名输入 = f'{编码头}.{编码载荷}'.encode('utf-8')
        签名 = hmac.new(
            self._密钥.encode('utf-8'),
            签名输入,
            self._获取算法函数()
        ).digest()
        
        编码签名 = self._base64url编码(签名)
        
        return f'{编码头}.{编码载荷}.{编码签名}'
    
    def 验证令牌(self, 令牌: str) -> Dict[str, Any]:
        """验证JWT令牌"""
        部分 = 令牌.split('.')
        if len(部分) != 3:
            raise 令牌无效异常('令牌格式无效')
        
        编码头, 编码载荷, 编码签名 = 部分
        
        签名输入 = f'{编码头}.{编码载荷}'.encode('utf-8')
        期望签名 = hmac.new(
            self._密钥.encode('utf-8'),
            签名输入,
            self._获取算法函数()
        ).digest()
        
        实际签名 = self._base64url解码(编码签名)
        
        if not hmac.compare_digest(期望签名, 实际签名):
            raise 令牌无效异常('令牌签名无效')
        
        载荷 = json.loads(self._base64url解码(编码载荷).decode('utf-8'))
        
        if 'exp' in 载荷:
            if time.time() > 载荷['exp']:
                raise 令牌过期异常('令牌已过期')
        
        return 载荷
    
    def 刷新令牌(self, 令牌: str, 新过期时间: int = None) -> str:
        """刷新令牌"""
        try:
            载荷 = self.验证令牌(令牌)
        except 令牌过期异常:
            部分 = 令牌.split('.')
            载荷 = json.loads(self._base64url解码(部分[1]).decode('utf-8'))
        
        if 'exp' in 载荷:
            del 载荷['exp']
        if 'iat' in 载荷:
            del 载荷['iat']
        if 'jti' in 载荷:
            del 载荷['jti']
        
        原过期时间 = self._过期时间
        if 新过期时间:
            self._过期时间 = 新过期时间
        
        新令牌 = self.生成令牌(载荷)
        self._过期时间 = 原过期时间
        
        return 新令牌
    
    def 解码令牌(self, 令牌: str) -> Dict[str, Any]:
        """解码令牌（不验证）"""
        部分 = 令牌.split('.')
        if len(部分) != 3:
            raise 令牌无效异常('令牌格式无效')
        
        头部 = json.loads(self._base64url解码(部分[0]).decode('utf-8'))
        载荷 = json.loads(self._base64url解码(部分[1]).decode('utf-8'))
        
        return {'头部': 头部, '载荷': 载荷}


class OAuth2简化流程:
    """OAuth2.0简化流程"""
    
    def __init__(self, 客户端ID: str, 客户端密钥: str, 授权服务器: str = ''):
        self._客户端ID = 客户端ID
        self._客户端密钥 = 客户端密钥
        self._授权服务器 = 授权服务器
        self._授权码存储: Dict[str, Dict[str, Any]] = {}
        self._访问令牌存储: Dict[str, Dict[str, Any]] = {}
    
    def 生成授权码(self, 用户ID: str, 重定向URI: str, 作用域: str = '') -> str:
        """生成授权码"""
        授权码 = secrets.token_urlsafe(32)
        self._授权码存储[授权码] = {
            '用户ID': 用户ID,
            '重定向URI': 重定向URI,
            '作用域': 作用域,
            '创建时间': time.time(),
            '已使用': False
        }
        return 授权码
    
    def 交换令牌(self, 授权码: str, 重定向URI: str) -> Optional[Dict[str, Any]]:
        """用授权码交换访问令牌"""
        if 授权码 not in self._授权码存储:
            return None
        
        授权信息 = self._授权码存储[授权码]
        
        if 授权信息['已使用']:
            return None
        
        if 授权信息['重定向URI'] != 重定向URI:
            return None
        
        if time.time() - 授权信息['创建时间'] > 600:
            return None
        
        授权信息['已使用'] = True
        
        访问令牌 = secrets.token_urlsafe(32)
        刷新令牌 = secrets.token_urlsafe(32)
        
        令牌信息 = {
            '访问令牌': 访问令牌,
            '刷新令牌': 刷新令牌,
            '令牌类型': 'Bearer',
            '过期时间': 3600,
            '作用域': 授权信息['作用域'],
            '用户ID': 授权信息['用户ID']
        }
        
        self._访问令牌存储[访问令牌] = 令牌信息
        
        return 令牌信息
    
    def 验证访问令牌(self, 访问令牌: str) -> Optional[Dict[str, Any]]:
        """验证访问令牌"""
        if 访问令牌 not in self._访问令牌存储:
            return None
        return self._访问令牌存储[访问令牌]
    
    def 撤销令牌(self, 访问令牌: str) -> bool:
        """撤销令牌"""
        if 访问令牌 in self._访问令牌存储:
            del self._访问令牌存储[访问令牌]
            return True
        return False


class 会话管理器:
    """会话管理器"""
    
    def __init__(self, 过期时间: int = 1800):
        self._会话字典: Dict[str, Dict[str, Any]] = {}
        self._过期时间 = 过期时间
    
    def 创建会话(self, 用户ID: str, 数据: Dict[str, Any] = None) -> str:
        """创建会话"""
        会话ID = secrets.token_urlsafe(32)
        self._会话字典[会话ID] = {
            '用户ID': 用户ID,
            '数据': 数据 or {},
            '创建时间': time.time(),
            '最后活动时间': time.time()
        }
        return 会话ID
    
    def 获取会话(self, 会话ID: str) -> Optional[Dict[str, Any]]:
        """获取会话"""
        if 会话ID not in self._会话字典:
            return None
        
        会话 = self._会话字典[会话ID]
        
        if time.time() - 会话['最后活动时间'] > self._过期时间:
            del self._会话字典[会话ID]
            return None
        
        会话['最后活动时间'] = time.time()
        return 会话
    
    def 更新会话(self, 会话ID: str, 数据: Dict[str, Any]):
        """更新会话"""
        会话 = self.获取会话(会话ID)
        if 会话:
            会话['数据'].update(数据)
    
    def 销毁会话(self, 会话ID: str) -> bool:
        """销毁会话"""
        if 会话ID in self._会话字典:
            del self._会话字典[会话ID]
            return True
        return False
    
    def 清理过期会话(self):
        """清理过期会话"""
        当前时间 = time.time()
        过期列表 = [
            sid for sid, 会话 in self._会话字典.items()
            if 当前时间 - 会话['最后活动时间'] > self._过期时间
        ]
        for sid in 过期列表:
            del self._会话字典[sid]
    
    def 活跃会话数(self) -> int:
        """获取活跃会话数"""
        self.清理过期会话()
        return len(self._会话字典)


class API密钥管理:
    """API密钥管理"""
    
    def __init__(self):
        self._密钥字典: Dict[str, Dict[str, Any]] = {}
    
    def 生成密钥(self, 名称: str, 权限列表: List[str] = None, 过期时间: int = None) -> str:
        """生成API密钥"""
        密钥 = f'sk_{secrets.token_urlsafe(32)}'
        
        self._密钥字典[密钥] = {
            '名称': 名称,
            '权限列表': 权限列表 or [],
            '创建时间': time.time(),
            '过期时间': time.time() + 过期时间 if 过期时间 else None
        }
        
        return 密钥
    
    def 验证密钥(self, 密钥: str) -> Optional[Dict[str, Any]]:
        """验证API密钥"""
        if 密钥 not in self._密钥字典:
            return None
        
        信息 = self._密钥字典[密钥]
        
        if 信息['过期时间'] and time.time() > 信息['过期时间']:
            del self._密钥字典[密钥]
            return None
        
        return 信息
    
    def 撤销密钥(self, 密钥: str) -> bool:
        """撤销API密钥"""
        if 密钥 in self._密钥字典:
            del self._密钥字典[密钥]
            return True
        return False
    
    def 检查权限(self, 密钥: str, 权限: str) -> bool:
        """检查密钥权限"""
        信息 = self.验证密钥(密钥)
        if not 信息:
            return False
        return 权限 in 信息['权限列表']


# 便捷函数
def 生成JWT(密钥: str, 载荷: Dict[str, Any], 过期时间: int = 3600) -> str:
    """生成JWT令牌"""
    jwt = JWT令牌(密钥, 过期时间=过期时间)
    return jwt.生成令牌(载荷)


def 验证JWT(密钥: str, 令牌: str) -> Dict[str, Any]:
    """验证JWT令牌"""
    jwt = JWT令牌(密钥)
    return jwt.验证令牌(令牌)


def 哈希密码(密码: str) -> Tuple[str, str]:
    """哈希密码"""
    return 密码工具.哈希密码(密码)


def 验证密码(密码: str, 哈希值: str, 盐值: str) -> bool:
    """验证密码"""
    return 密码工具.验证密码(密码, 哈希值, 盐值)