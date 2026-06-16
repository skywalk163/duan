"""
段言标准库 - 内置函数实现

提供文件I/O、路径操作、系统函数等核心功能
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Union


# =============================================================================
# 文件I/O函数
# =============================================================================

def 读取文件(path: str, encoding: str = 'utf-8') -> str:
    """
    读取文件内容
    
    参数:
        path: 文件路径
        encoding: 编码（默认utf-8）
    
    返回:
        文件内容
    
    异常:
        RuntimeError: 文件读取失败
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"文件不存在: '{path}'")
    except PermissionError:
        raise RuntimeError(f"无权限读取文件: '{path}'")
    except Exception as e:
        raise RuntimeError(f"读取文件失败 '{path}': {e}")


def 写入文件(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    写入文件内容
    
    参数:
        path: 文件路径
        content: 文件内容
        encoding: 编码（默认utf-8）
    
    异常:
        RuntimeError: 文件写入失败
    """
    try:
        # 确保目录存在
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
    except PermissionError:
        raise RuntimeError(f"无权限写入文件: '{path}'")
    except Exception as e:
        raise RuntimeError(f"写入文件失败 '{path}': {e}")


def 追加文件(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    追加内容到文件
    
    参数:
        path: 文件路径
        content: 追加内容
        encoding: 编码（默认utf-8）
    """
    try:
        with open(path, 'a', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise RuntimeError(f"追加文件失败 '{path}': {e}")


def 文件存在(path: str) -> bool:
    """检查文件是否存在"""
    return os.path.isfile(path)


def 目录存在(path: str) -> bool:
    """检查目录是否存在"""
    return os.path.isdir(path)


def 路径存在(path: str) -> bool:
    """检查路径是否存在（文件或目录）"""
    return os.path.exists(path)


def 创建目录(path: str) -> None:
    """
    创建目录
    
    参数:
        path: 目录路径
    
    说明:
        自动创建所有父目录
    """
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"创建目录失败 '{path}': {e}")


def 删除文件(path: str) -> None:
    """删除文件"""
    try:
        os.remove(path)
    except FileNotFoundError:
        raise RuntimeError(f"文件不存在: '{path}'")
    except Exception as e:
        raise RuntimeError(f"删除文件失败 '{path}': {e}")


def 删除目录(path: str) -> None:
    """删除空目录"""
    try:
        os.rmdir(path)
    except Exception as e:
        raise RuntimeError(f"删除目录失败 '{path}': {e}")


def 列出目录(path: str = '.') -> List[str]:
    """
    列出目录内容
    
    参数:
        path: 目录路径（默认当前目录）
    
    返回:
        文件名列表
    """
    try:
        return os.listdir(path)
    except Exception as e:
        raise RuntimeError(f"列出目录失败 '{path}': {e}")


def 文件大小(path: str) -> int:
    """
    获取文件大小（字节）
    
    参数:
        path: 文件路径
    
    返回:
        文件大小（字节）
    """
    try:
        return os.path.getsize(path)
    except Exception as e:
        raise RuntimeError(f"获取文件大小失败 '{path}': {e}")


# =============================================================================
# 路径操作函数
# =============================================================================

def 绝对路径(path: str) -> str:
    """获取绝对路径"""
    return os.path.abspath(path)


def 连接路径(*paths: str) -> str:
    """连接多个路径"""
    return os.path.join(*paths)


def 目录名(path: str) -> str:
    """获取路径的目录部分"""
    return os.path.dirname(path)


def 文件名(path: str) -> str:
    """获取路径的文件名部分"""
    return os.path.basename(path)


def 扩展名(path: str) -> str:
    """获取文件扩展名"""
    _, ext = os.path.splitext(path)
    return ext


def 分割路径(path: str) -> tuple:
    """分割路径为(目录, 文件名)"""
    return os.path.split(path)


def 分割扩展名(path: str) -> tuple:
    """分割路径为(主名, 扩展名)"""
    return os.path.splitext(path)


# =============================================================================
# 系统函数
# =============================================================================

def 环境变量(name: str, default: str = None) -> Optional[str]:
    """
    获取环境变量
    
    参数:
        name: 环境变量名
        default: 默认值
    
    返回:
        环境变量值或默认值
    """
    return os.environ.get(name, default)


def 设置环境变量(name: str, value: str) -> None:
    """设置环境变量"""
    os.environ[name] = value


def 参数列表() -> List[str]:
    """获取命令行参数列表"""
    return sys.argv


def 退出程序(code: int = 0) -> None:
    """退出程序"""
    sys.exit(code)


def 当前目录() -> str:
    """获取当前工作目录"""
    return os.getcwd()


def 切换目录(path: str) -> None:
    """切换工作目录"""
    try:
        os.chdir(path)
    except Exception as e:
        raise RuntimeError(f"切换目录失败 '{path}': {e}")


def 执行命令(command: str) -> int:
    """
    执行系统命令
    
    参数:
        command: 命令字符串
    
    返回:
        退出码
    """
    return os.system(command)


# =============================================================================
# 字符串工具函数
# =============================================================================

def 转整数(text: str) -> int:
    """将字符串转换为整数"""
    try:
        return int(text)
    except ValueError:
        raise RuntimeError(f"无法将 '{text}' 转换为整数")


def 转浮点(text: str) -> float:
    """将字符串转换为浮点数"""
    try:
        return float(text)
    except ValueError:
        raise RuntimeError(f"无法将 '{text}' 转换为浮点数")


def 转字符串(value) -> str:
    """将值转换为字符串"""
    return str(value)


def 字符串长度(text: str) -> int:
    """获取字符串长度"""
    return len(text)


def 分割字符串(text: str, separator: str = None) -> List[str]:
    """分割字符串"""
    return text.split(separator)


def 连接字符串(parts: List[str], separator: str = '') -> str:
    """连接字符串列表"""
    return separator.join(parts)


def 替换字符串(text: str, old: str, new: str) -> str:
    """替换字符串"""
    return text.replace(old, new)


def 去除空白(text: str) -> str:
    """去除首尾空白"""
    return text.strip()


# =============================================================================
# 列表工具函数
# =============================================================================

def 列(*args) -> list:
    """创建包含指定元素的列表"""
    return list(args)


def 列表创建() -> list:
    """创建空列表"""
    return []


def 列表长度(列表) -> int:
    """获取列表长度"""
    return len(列表)


def 列表获取(列表, 索引):
    """获取列表中指定索引的元素"""
    return 列表[索引]


def 列表追加(列表, 元素) -> None:
    """向列表追加元素"""
    列表.append(元素)


def 列表弹出(列表, 索引: int = -1):
    """从列表弹出元素"""
    return 列表.pop(索引)


def 列表排序(列表, 反向: bool = False) -> None:
    """排序列表（原地修改）"""
    列表.sort(reverse=反向)


def 列表反转(列表) -> None:
    """反转列表（原地修改）"""
    列表.reverse()


def 列表包含(列表, 元素) -> bool:
    """检查列表是否包含元素"""
    return 元素 in 列表


# =============================================================================
# 字典工具函数
# =============================================================================

def 字典创建() -> dict:
    """创建空字典"""
    return {}


def 字典设置(字典, 键, 值) -> None:
    """设置字典键值"""
    字典[键] = 值


def 字典删除(字典, 键) -> None:
    """删除字典键值"""
    if 键 in 字典:
        del 字典[键]


def 字典键列表(字典) -> list:
    """获取字典的所有键"""
    return list(字典.keys())


def 字典值列表(字典) -> list:
    """获取字典的所有值"""
    return list(字典.values())


def 字典项列表(字典) -> list:
    """获取字典的所有键值对"""
    return list(字典.items())


def 字典包含键(字典, 键) -> bool:
    """检查字典是否包含键"""
    return 键 in 字典


def 字典获取(字典, 键, 默认值=None):
    """从字典获取值，不存在则返回默认值"""
    return 字典.get(键, 默认值)


# =============================================================================
# 类型检查函数
# =============================================================================

def 是整数(值) -> bool:
    """检查是否为整数"""
    return isinstance(值, int) and not isinstance(值, bool)


def 是浮点(值) -> bool:
    """检查是否为浮点数"""
    return isinstance(值, float)


def 是字符串(值) -> bool:
    """检查是否为字符串"""
    return isinstance(值, str)


def 是列表(值) -> bool:
    """检查是否为列表"""
    return isinstance(值, list)


def 是字典(值) -> bool:
    """检查是否为字典"""
    return isinstance(值, dict)


def 是空(值) -> bool:
    """检查是否为空值"""
    return 值 is None


# =============================================================================
# 导出所有函数
# =============================================================================

__all__ = [
    # 文件I/O
    '读取文件', '写入文件', '追加文件',
    '文件存在', '目录存在', '路径存在',
    '创建目录', '删除文件', '删除目录',
    '列出目录', '文件大小',
    
    # 路径操作
    '绝对路径', '连接路径', '目录名', '文件名',
    '扩展名', '分割路径', '分割扩展名',
    
    # 系统函数
    '环境变量', '设置环境变量', '参数列表',
    '退出程序', '当前目录', '切换目录', '执行命令',
    
    # 字符串工具
    '转整数', '转浮点', '转字符串',
    '字符串长度', '分割字符串', '连接字符串',
    '替换字符串', '去除空白',
    
    # 列表工具
    '列', '列表长度', '列表追加', '列表弹出',
    '列表排序', '列表反转', '列表包含',
    
    # 字典工具
    '字典创建', '字典设置', '字典删除',
    '字典键列表', '字典值列表', '字典项列表',
    '字典包含键', '字典获取',
    
    # 类型检查
    '是整数', '是浮点', '是字符串',
    '是列表', '是字典', '是空',
]
