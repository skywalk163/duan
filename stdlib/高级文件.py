"""
段言标准库 - 高级文件模块

封装 shutil 模块，提供高级文件和目录操作功能。
"""

import shutil
import os
from typing import List, Optional


def 复制文件(源路径: str, 目标路径: str, 保留元数据: bool = True) -> str:
    """
    复制文件
    
    参数:
        源路径: 源文件路径
        目标路径: 目标路径（文件或目录）
        保留元数据: 是否保留文件元数据
    
    返回:
        目标文件路径
    """
    if 保留元数据:
        return shutil.copy2(源路径, 目标路径)
    else:
        return shutil.copy(源路径, 目标路径)


def 复制目录(源路径: str, 目标路径: str, 忽略模式: List[str] = None) -> str:
    """
    递归复制目录
    
    参数:
        源路径: 源目录路径
        目标路径: 目标目录路径（必须不存在）
        忽略模式: 忽略的文件模式列表
    
    返回:
        目标目录路径
    """
    忽略函数 = None
    if 忽略模式:
        忽略函数 = shutil.ignore_patterns(*忽略模式)
    return shutil.copytree(源路径, 目标路径, ignore=忽略函数)


def 移动(源路径: str, 目标路径: str) -> str:
    """
    移动文件或目录
    
    参数:
        源路径: 源路径
        目标路径: 目标路径
    
    返回:
        目标路径
    """
    return shutil.move(源路径, 目标路径)


def 删除目录(路径: str, 忽略错误: bool = False) -> None:
    """
    递归删除目录
    
    参数:
        路径: 目录路径
        忽略错误: 是否忽略错误
    """
    shutil.rmtree(路径, ignore_errors=忽略错误)


def 删除文件(路径: str) -> None:
    """删除文件"""
    os.remove(路径)


def 磁盘使用情况(路径: str = ".") -> dict:
    """
    获取磁盘使用情况
    
    参数:
        路径: 路径
    
    返回:
        {'总空间': 字节数, '已用空间': 字节数, '可用空间': 字节数}
    """
    用法 = shutil.disk_usage(路径)
    return {
        '总空间': 用法.total,
        '已用空间': 用法.used,
        '可用空间': 用法.free,
    }


def 磁盘总空间(路径: str = ".") -> int:
    """获取磁盘总空间（字节）"""
    return shutil.disk_usage(路径).total


def 磁盘可用空间(路径: str = ".") -> int:
    """获取磁盘可用空间（字节）"""
    return shutil.disk_usage(路径).free


def 磁盘已用空间(路径: str = ".") -> int:
    """获取磁盘已用空间（字节）"""
    return shutil.disk_usage(路径).used


def 查找命令(命令名: str) -> Optional[str]:
    """
    查找可执行文件路径
    
    参数:
        命令名: 命令名称
    
    返回:
        可执行文件路径，未找到返回None
    """
    return shutil.which(命令名)


def 命令存在(命令名: str) -> bool:
    """检查命令是否存在"""
    return shutil.which(命令名) is not None


def 归档(源路径: str, 目标路径: str = None, 格式: str = "zip") -> str:
    """
    创建归档文件
    
    参数:
        源路径: 要归档的源路径
        目标路径: 目标归档文件路径（不含扩展名）
        格式: 归档格式（zip, tar, gztar, bztar, xztar）
    
    返回:
        归档文件路径
    """
    return shutil.make_archive(目标路径 or 源路径, 格式, 源路径)


def 解压(归档路径: str, 目标目录: str = None, 格式: str = None) -> None:
    """
    解压归档文件
    
    参数:
        归档路径: 归档文件路径
        目标目录: 目标目录，默认当前目录
        格式: 归档格式，None自动检测
    """
    shutil.unpack_archive(归档路径, 目标目录, 格式)


def 支持的归档格式() -> List[str]:
    """获取支持的归档格式列表"""
    return [f[0] for f in shutil.get_archive_formats()]


def 支持的解压格式() -> List[str]:
    """获取支持的解压格式列表"""
    return [f[0] for f in shutil.get_unpack_formats()]


def 目录大小(路径: str) -> int:
    """
    计算目录总大小（字节）
    
    参数:
        路径: 目录路径
    
    返回:
        总字节数
    """
    总大小 = 0
    for 目录路径, 子目录, 文件列表 in os.walk(路径):
        for 文件名 in 文件列表:
            文件路径 = os.path.join(目录路径, 文件名)
            if os.path.isfile(文件路径):
                总大小 += os.path.getsize(文件路径)
    return 总大小


def 文件树(路径: str, 前缀: str = "", 显示大小: bool = True) -> str:
    """
    生成目录树状结构字符串
    
    参数:
        路径: 目录路径
        前缀: 行前缀
        显示大小: 是否显示文件大小
    
    返回:
        树状结构字符串
    """
    行列表 = []
    行列表.append(f"{前缀}{os.path.basename(路径) or 路径}/")
    
    try:
        项目列表 = sorted(os.listdir(路径))
    except PermissionError:
        行列表.append(f"{前缀}  [权限不足]")
        return "\n".join(行列表)
    
    文件列表 = [f for f in 项目列表 if os.path.isfile(os.path.join(路径, f))]
    目录列表 = [d for d in 项目列表 if os.path.isdir(os.path.join(路径, d))]
    
    # 显示目录
    for i, 目录 in enumerate(目录列表):
        是最后 = i == len(目录列表) - 1 and len(文件列表) == 0
        连接器 = "└── " if 是最后 else "├── "
        子前缀 = 前缀 + ("    " if 是最后 else "│   ")
        子路径 = os.path.join(路径, 目录)
        行列表.append(f"{前缀}{连接器}{目录}/")
        
        # 递归（限制深度，避免无限递归）
        子树 = 文件树(子路径, 子前缀, 显示大小)
        子行 = 子树.split("\n")
        行列表.extend(子行[1:])  # 跳过第一行（已由父级显示）
    
    # 显示文件
    for i, 文件 in enumerate(文件列表):
        是最后 = i == len(文件列表) - 1
        连接器 = "└── " if 是最后 else "├── "
        if 显示大小:
            try:
                大小 = os.path.getsize(os.path.join(路径, 文件))
                大小文本 = f" ({大小}字节)"
            except:
                大小文本 = ""
            行列表.append(f"{前缀}{连接器}{文件}{大小文本}")
        else:
            行列表.append(f"{前缀}{连接器}{文件}")
    
    return "\n".join(行列表)


__all__ = [
    '复制文件',
    '复制目录',
    '移动',
    '删除目录',
    '删除文件',
    '磁盘使用情况',
    '磁盘总空间',
    '磁盘可用空间',
    '磁盘已用空间',
    '查找命令',
    '命令存在',
    '归档',
    '解压',
    '支持的归档格式',
    '支持的解压格式',
    '目录大小',
    '文件树',
]
