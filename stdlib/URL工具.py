"""
URL工具模块 - 查询参数、编码

提供URL处理功能，包括：
- URL解析
- 参数构建
- URL编码
- URL验证
"""
import urllib.parse
from typing import Dict, Any, List, Optional


def 解析URL(URL: str) -> Dict[str, str]:
    """解析URL"""
    解析结果 = urllib.parse.urlparse(URL)
    return {
        '协议': 解析结果.scheme,
        '域名': 解析结果.hostname,
        '端口': 解析结果.port,
        '路径': 解析结果.path,
        '查询参数': 解析结果.query,
        '片段': 解析结果.fragment,
    }


def 获取域名(URL: str) -> str:
    """获取域名"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.hostname or ''


def 获取路径(URL: str) -> str:
    """获取路径"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.path


def 获取查询参数(URL: str) -> Dict[str, str]:
    """获取查询参数"""
    解析结果 = urllib.parse.urlparse(URL)
    参数 = urllib.parse.parse_qs(解析结果.query)
    return {k: v[0] for k, v in 参数.items()}


def 获取单个参数(URL: str, 参数名: str) -> Optional[str]:
    """获取单个查询参数"""
    参数 = 获取查询参数(URL)
    return 参数.get(参数名)


def 获取片段(URL: str) -> str:
    """获取片段（锚点）"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.fragment


def 获取协议(URL: str) -> str:
    """获取协议"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.scheme


def 构建URL(基础URL: str, 参数: Dict[str, Any] = None) -> str:
    """构建URL"""
    if 参数:
        查询字符串 = urllib.parse.urlencode(参数)
        if '?' in 基础URL:
            return 基础URL + '&' + 查询字符串
        else:
            return 基础URL + '?' + 查询字符串
    return 基础URL


def 构建查询字符串(参数: Dict[str, Any]) -> str:
    """构建查询字符串"""
    return urllib.parse.urlencode(参数)


def 添加参数(URL: str, 参数名: str, 参数值: Any) -> str:
    """添加参数"""
    查询字符串 = urllib.parse.urlencode({参数名: 参数值})
    if '?' in URL:
        return URL + '&' + 查询字符串
    else:
        return URL + '?' + 查询字符串


def 更新参数(URL: str, 参数名: str, 参数值: Any) -> str:
    """更新参数"""
    解析结果 = urllib.parse.urlparse(URL)
    参数 = 获取查询参数(URL)
    参数[参数名] = str(参数值)
    新查询 = urllib.parse.urlencode(参数)
    
    return urllib.parse.urlunparse((
        解析结果.scheme,
        解析结果.netloc,
        解析结果.path,
        解析结果.params,
        新查询,
        解析结果.fragment
    ))


def 删除参数(URL: str, 参数名: str) -> str:
    """删除参数"""
    解析结果 = urllib.parse.urlparse(URL)
    参数 = 获取查询参数(URL)
    if 参数名 in 参数:
        del 参数[参数名]
    新查询 = urllib.parse.urlencode(参数)
    
    return urllib.parse.urlunparse((
        解析结果.scheme,
        解析结果.netloc,
        解析结果.path,
        解析结果.params,
        新查询,
        解析结果.fragment
    ))


def URL编码(字符串: str) -> str:
    """URL编码"""
    return urllib.parse.quote(字符串)


def URL解码(字符串: str) -> str:
    """URL解码"""
    return urllib.parse.unquote(字符串)


def URL全编码(字符串: str) -> str:
    """URL全编码（包含特殊字符）"""
    return urllib.parse.quote(字符串, safe='')


def URL全解码(字符串: str) -> str:
    """URL全解码"""
    return urllib.parse.unquote_plus(字符串)


def 编码参数字典(参数: Dict[str, Any]) -> str:
    """编码参数字典"""
    return urllib.parse.urlencode(参数)


def 解码参数字符串(字符串: str) -> Dict[str, str]:
    """解码参数字符串"""
    参数 = urllib.parse.parse_qs(字符串)
    return {k: v[0] for k, v in 参数.items()}


def 合并URL(基础URL: str, 相对路径: str) -> str:
    """合并URL"""
    return urllib.parse.urljoin(基础URL, 相对路径)


def 获取绝对URL(基础URL: str, 相对路径: str) -> str:
    """获取绝对URL"""
    return urllib.parse.urljoin(基础URL, 相对路径)


def 验证URL(URL: str) -> bool:
    """验证URL格式"""
    import re
    模式 = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(模式, URL))


def 验证HTTPURL(URL: str) -> bool:
    """验证HTTP URL"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.scheme in ['http', 'https']


def 验证HTTPSURL(URL: str) -> bool:
    """验证HTTPS URL"""
    解析结果 = urllib.parse.urlparse(URL)
    return 解析结果.scheme == 'https'


def 获取端口(URL: str, 默认端口: int = None) -> int:
    """获取端口"""
    解析结果 = urllib.parse.urlparse(URL)
    if 解析结果.port:
        return 解析结果.port
    
    if 默认端口:
        return 默认端口
    
    if 解析结果.scheme == 'https':
        return 443
    elif 解析结果.scheme == 'http':
        return 80
    elif 解析结果.scheme == 'ftp':
        return 21
    else:
        return 0


def 是否是相对路径(URL: str) -> bool:
    """检查是否是相对路径"""
    解析结果 = urllib.parse.urlparse(URL)
    return not 解析结果.scheme and not 解析结果.netloc


def 是否是绝对路径(URL: str) -> bool:
    """检查是否是绝对路径"""
    解析结果 = urllib.parse.urlparse(URL)
    return bool(解析结果.scheme) or bool(解析结果.netloc)


def 获取文件名(URL: str) -> str:
    """从URL中获取文件名"""
    路径 = 获取路径(URL)
    if '/' in 路径:
        return 路径.split('/')[-1]
    return 路径


def 获取扩展名(URL: str) -> str:
    """从URL中获取扩展名"""
    文件名 = 获取文件名(URL)
    if '.' in 文件名:
        return 文件名.split('.')[-1]
    return ''


def 构建完整URL(协议: str, 域名: str, 路径: str = '', 参数: Dict[str, Any] = None,
                 片段: str = None, 端口: int = None) -> str:
    """构建完整URL"""
    if 端口:
        主机 = f'{域名}:{端口}'
    else:
        主机 = 域名
    
    查询 = urllib.parse.urlencode(参数) if 参数 else ''
    
    return urllib.parse.urlunparse((
        协议,
        主机,
        路径,
        '',
        查询,
        片段 or ''
    ))


def 标准化URL(URL: str) -> str:
    """标准化URL"""
    解析结果 = urllib.parse.urlparse(URL)
    
    # 域名小写
    主机 = 解析结果.hostname
    if 主机:
        主机 = 主机.lower()
        if 解析结果.port:
            主机 = f'{主机}:{解析结果.port}'
    
    # 路径标准化
    路径 = 解析结果.path
    if not 路径.startswith('/'):
        路径 = '/' + 路径
    
    return urllib.parse.urlunparse((
        解析结果.scheme,
        主机 or '',
        路径,
        解析结果.params,
        解析结果.query,
        解析结果.fragment
    ))


def 拼接URL路径(*路径片段) -> str:
    """拼接URL路径"""
    路径 = '/'.join(str(片段).strip('/') for 片段 in 路径片段)
    if not 路径.startswith('/'):
        路径 = '/' + 路径
    return 路径


def 提取子域名(URL: str) -> Optional[str]:
    """提取子域名"""
    域名 = 获取域名(URL)
    if 域名:
        部分 = 域名.split('.')
        if len(部分) >= 3:
            return 部分[0]
    return None


def 提取顶级域名(URL: str) -> Optional[str]:
    """提取顶级域名"""
    域名 = 获取域名(URL)
    if 域名:
        部分 = 域名.split('.')
        if len(部分) >= 2:
            return '.'.join(部分[-2:])
    return None


def 判断同域(URL1: str, URL2: str) -> bool:
    """判断两个URL是否同域"""
    域名1 = 获取域名(URL1)
    域名2 = 获取域名(URL2)
    return 域名1 == 域名2


def 获取URL哈希(URL: str) -> str:
    """获取URL哈希值"""
    import hashlib
    return hashlib.md5(URL.encode()).hexdigest()


def 比较URL(URL1: str, URL2: str, 忽略片段: bool = True) -> bool:
    """比较两个URL"""
    解析1 = urllib.parse.urlparse(URL1)
    解析2 = urllib.parse.urlparse(URL2)
    
    if 忽略片段:
        return (
            解析1.scheme == 解析2.scheme and
            解析1.hostname == 解析2.hostname and
            解析1.path == 解析2.path and
            解析1.query == 解析2.query
        )
    else:
        return URL1 == URL2


def 从URL提取路径片段(URL: str) -> List[str]:
    """从URL提取路径片段"""
    路径 = 获取路径(URL)
    片段 = 路径.split('/')
    return [片段 for 片段 in 片段 if 片段]


def 从URL提取层级(URL: str) -> int:
    """从URL提取层级"""
    片段 = 从URL提取路径片段(URL)
    return len(片段)


def 是否包含参数(URL: str, 参数名: str) -> bool:
    """检查URL是否包含参数"""
    参数 = 获取查询参数(URL)
    return 参数名 in 参数


def 替换协议(URL: str, 新协议: str) -> str:
    """替换协议"""
    解析结果 = urllib.parse.urlparse(URL)
    return urllib.parse.urlunparse((
        新协议,
        解析结果.netloc,
        解析结果.path,
        解析结果.params,
        解析结果.query,
        解析结果.fragment
    ))


def 转换为HTTPS(URL: str) -> str:
    """转换为HTTPS"""
    return 替换协议(URL, 'https')


def 转换为HTTP(URL: str) -> str:
    """转换为HTTP"""
    return 替换协议(URL, 'http')