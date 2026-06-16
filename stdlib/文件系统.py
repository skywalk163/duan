"""
段言标准库 - 文件系统模块

提供文件 I/O 和路径操作函数
"""

import os
import shutil
from typing import List, Optional, Union


def 读取文件(path: str, encoding: str = 'utf-8') -> str:
    """读取文件内容"""
    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def 写入文件(path: str, content: str, encoding: str = 'utf-8') -> None:
    """写入文件"""
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)


def 追加文件(path: str, content: str, encoding: str = 'utf-8') -> None:
    """追加内容到文件"""
    with open(path, 'a', encoding=encoding) as f:
        f.write(content)


def 文件存在(path: str) -> bool:
    """检查文件是否存在"""
    return os.path.isfile(path)


def 删除文件(path: str) -> None:
    """删除文件"""
    os.remove(path)


def 复制文件(src: str, dst: str) -> None:
    """复制文件"""
    shutil.copy2(src, dst)


def 移动文件(src: str, dst: str) -> None:
    """移动文件"""
    shutil.move(src, dst)


def 创建目录(path: str) -> None:
    """创建目录（包括父目录）"""
    os.makedirs(path, exist_ok=True)


def 删除目录(path: str) -> None:
    """删除目录"""
    shutil.rmtree(path)


def 目录存在(path: str) -> bool:
    """检查目录是否存在"""
    return os.path.isdir(path)


def 获取文件名(path: str) -> str:
    """获取文件名（含扩展名）"""
    return os.path.basename(path)


def 获取扩展名(path: str) -> str:
    """获取文件扩展名"""
    _, ext = os.path.splitext(path)
    return ext


def 获取目录名(path: str) -> str:
    """获取目录路径"""
    return os.path.dirname(path)


def 文件大小(path: str) -> int:
    """获取文件大小（字节）"""
    return os.path.getsize(path)


def 文件列表(dir_path: str) -> List[str]:
    """列出目录中的文件名"""
    return os.listdir(dir_path)


def 路径连接(*parts: str) -> str:
    """连接路径组件"""
    return os.path.join(*parts)