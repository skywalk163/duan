"""
输入校验与净化模块 - SQL注入防护、XSS过滤

提供安全防御功能，包括：
- SQL注入防护
- XSS过滤
- 输入校验
- 输出编码
- 安全转换
"""
import re
import html
from typing import Any, Callable, Dict, List, Optional


class SQL注入防护:
    """SQL注入防护"""
    
    _危险模式 = [
        r"(\b(OR|AND)\b\s+.+\s*=\s*)",
        r"(--\s*$)",
        r"(;\s*(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE)\b)",
        r"(\bUNION\b\s+\bSELECT\b)",
        r"(\bEXEC\b\s*\()",
        r"(\bEXECUTE\b\s*\()",
        r"(1\s*=\s*1)",
        r"('\s*(OR|AND)\s+')",
        r"(\bCHAR\b\s*\()",
        r"(\bCONCAT\b\s*\()",
    ]
    
    @staticmethod
    def 检测(输入: str) -> bool:
        """检测SQL注入"""
        输入大写 = 输入.upper()
        for 模式 in SQL注入防护._危险模式:
            if re.search(模式, 输入大写, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def 净化(输入: str) -> str:
        """净化SQL输入"""
        危险字符 = ["'", '"', ';', '--', '/*', '*/', '\\']
        结果 = 输入
        for 字符 in 危险字符:
            结果 = 结果.replace(字符, '')
        return 结果
    
    @staticmethod
    def 参数化转义(值: Any) -> str:
        """参数化转义"""
        if isinstance(值, str):
            return 值.replace("'", "''").replace('\\', '\\\\')
        if isinstance(值, (int, float)):
            return str(值)
        if isinstance(值, bool):
            return '1' if 值 else '0'
        if 值 is None:
            return 'NULL'
        return str(值)
    
    @staticmethod
    def 安全查询(查询模板: str, 参数: Dict[str, Any]) -> str:
        """安全查询构建"""
        for 键, 值 in 参数.items():
            占位符 = f':{键}'
            转义值 = SQL注入防护.参数化转义(值)
            if isinstance(值, str):
                转义值 = f"'{转义值}'"
            查询模板 = 查询模板.replace(占位符, 转义值)
        return 查询模板


class XSS防护:
    """XSS防护"""
    
    _危险标签 = ['script', 'iframe', 'object', 'embed', 'applet', 'form', 'input']
    _危险属性 = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onblur']
    
    @staticmethod
    def 检测(输入: str) -> bool:
        """检测XSS"""
        危险模式 = [
            r'<\s*script',
            r'javascript\s*:',
            r'on\w+\s*=',
            r'<\s*iframe',
            r'<\s*object',
            r'<\s*embed',
            r'eval\s*\(',
            r'expression\s*\(',
        ]
        for 模式 in 危险模式:
            if re.search(模式, 输入, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def 净化(输入: str) -> str:
        """净化HTML输入"""
        结果 = html.escape(输入)
        return 结果
    
    @staticmethod
    def 剥离标签(输入: str, 允许标签: List[str] = None) -> str:
        """剥离HTML标签"""
        if 允许标签:
            允许模式 = '|'.join(允许标签)
            模式 = rf'<(?!/?({允许模式})\b)[^>]*>'
            return re.sub(模式, '', 输入)
        
        return re.sub(r'<[^>]*>', '', 输入)
    
    @staticmethod
    def 编码属性值(值: str) -> str:
        """编码HTML属性值"""
        return html.escape(值, quote=True)


class 输入校验器:
    """输入校验器"""
    
    @staticmethod
    def 校验长度(值: str, 最小: int = 0, 最大: int = None) -> bool:
        """校验长度"""
        长度 = len(值)
        if 长度 < 最小:
            return False
        if 最大 is not None and 长度 > 最大:
            return False
        return True
    
    @staticmethod
    def 校验范围(值: float, 最小: float, 最大: float) -> bool:
        """校验范围"""
        return 最小 <= 值 <= 最大
    
    @staticmethod
    def 校验格式(值: str, 模式: str) -> bool:
        """校验格式"""
        return bool(re.match(模式, 值))
    
    @staticmethod
    def 校验邮箱(值: str) -> bool:
        """校验邮箱"""
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 值))
    
    @staticmethod
    def 校验手机号(值: str) -> bool:
        """校验手机号"""
        return bool(re.match(r'^1[3-9]\d{9}$', 值))
    
    @staticmethod
    def 校验URL(值: str) -> bool:
        """校验URL"""
        return bool(re.match(r'^https?://[^\s/$.?#].[^\s]*$', 值))
    
    @staticmethod
    def 校验IP地址(值: str) -> bool:
        """校验IP地址"""
        return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', 值))
    
    @staticmethod
    def 校验身份证(值: str) -> bool:
        """校验身份证"""
        return bool(re.match(r'^\d{17}[\dXx]$', 值))
    
    @staticmethod
    def 校验纯数字(值: str) -> bool:
        """校验纯数字"""
        return 值.isdigit()
    
    @staticmethod
    def 校验纯字母(值: str) -> bool:
        """校验纯字母"""
        return 值.isalpha()
    
    @staticmethod
    def 校验字母数字(值: str) -> bool:
        """校验字母数字"""
        return 值.isalnum()
    
    @staticmethod
    def 校验强密码(值: str) -> bool:
        """校验强密码"""
        if len(值) < 8:
            return False
        有小写 = any(c.islower() for c in 值)
        有大写 = any(c.isupper() for c in 值)
        有数字 = any(c.isdigit() for c in 值)
        有特殊 = any(not c.isalnum() for c in 值)
        return 有小写 and 有大写 and 有数字 and 有特殊


class 安全转换:
    """安全类型转换"""
    
    @staticmethod
    def 安全整数(值: Any, 默认值: int = 0) -> int:
        """安全转整数"""
        try:
            return int(值)
        except (ValueError, TypeError):
            return 默认值
    
    @staticmethod
    def 安全浮点数(值: Any, 默认值: float = 0.0) -> float:
        """安全转浮点数"""
        try:
            return float(值)
        except (ValueError, TypeError):
            return 默认值
    
    @staticmethod
    def 安全字符串(值: Any, 默认值: str = '') -> str:
        """安全转字符串"""
        if 值 is None:
            return 默认值
        return str(值)
    
    @staticmethod
    def 安全布尔值(值: Any, 默认值: bool = False) -> bool:
        """安全转布尔值"""
        if isinstance(值, bool):
            return 值
        if isinstance(值, str):
            return 值.lower() in ('true', '1', 'yes', '是')
        if isinstance(值, (int, float)):
            return bool(值)
        return 默认值
    
    @staticmethod
    def 安全列表(值: Any, 默认值: list = None) -> list:
        """安全转列表"""
        if isinstance(值, list):
            return 值
        if isinstance(值, (tuple, set)):
            return list(值)
        if isinstance(值, str):
            return 值.split(',')
        return 默认值 or []


class 路径安全:
    """路径安全工具"""
    
    @staticmethod
    def 检测路径遍历(路径: str) -> bool:
        """检测路径遍历攻击"""
        危险模式 = ['../', '..\\', '..%2f', '..%5c', '%2e%2e']
        路径小写 = 路径.lower()
        return any(模式 in 路径小写 for 模式 in 危险模式)
    
    @staticmethod
    def 净化路径(路径: str) -> str:
        """净化路径"""
        路径 = 路径.replace('../', '').replace('..\\', '')
        while '../' in 路径 or '..\\' in 路径:
            路径 = 路径.replace('../', '').replace('..\\', '')
        return 路径
    
    @staticmethod
    def 安全文件名(文件名: str) -> str:
        """安全文件名"""
        文件名 = re.sub(r'[^\w\s.-]', '', 文件名)
        文件名 = 文件名.strip('. ')
        return 文件名 or 'unnamed'


class 文件上传安全:
    """文件上传安全"""
    
    _危险扩展名 = {'.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.msi', '.com', '.scr'}
    _危险MIME类型 = {'application/x-executable', 'application/x-msdos-program'}
    
    @staticmethod
    def 检查文件扩展名(文件名: str, 允许扩展名: List[str] = None) -> bool:
        """检查文件扩展名"""
        _, 扩展名 = os.path.splitext(文件名)
        扩展名 = 扩展名.lower()
        
        if 扩展名 in 文件上传安全._危险扩展名:
            return False
        
        if 允许扩展名:
            return 扩展名 in [e.lower() for e in 允许扩展名]
        
        return True
    
    @staticmethod
    def 检查文件大小(大小: int, 最大大小: int = 10 * 1024 * 1024) -> bool:
        """检查文件大小"""
        return 0 < 大小 <= 最大大小
    
    @staticmethod
    def 生成安全文件名(原始文件名: str) -> str:
        """生成安全文件名"""
        import uuid
        名称, 扩展名 = os.path.splitext(原始文件名)
        安全扩展名 = 扩展名.lower() if 扩展名.lower() not in 文件上传安全._危险扩展名 else '.txt'
        return f'{uuid.uuid4().hex}{安全扩展名}'


# 便捷函数
def 净化SQL(输入: str) -> str:
    """净化SQL输入"""
    return SQL注入防护.净化(输入)


def 净化HTML(输入: str) -> str:
    """净化HTML输入"""
    return XSS防护.净化(输入)


def 检测SQL注入(输入: str) -> bool:
    """检测SQL注入"""
    return SQL注入防护.检测(输入)


def 检测XSS(输入: str) -> bool:
    """检测XSS"""
    return XSS防护.检测(输入)


def 校验输入(值: str, 规则: Callable[[str], bool]) -> bool:
    """校验输入"""
    return 规则(值)