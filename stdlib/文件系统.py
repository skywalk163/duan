"""
段言标准库 - 文件系统模块

提供文件 I/O 和路径操作函数
"""

import os
import shutil
import tempfile
import time
from typing import List, Optional, Union, Dict, Any


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


def 绝对路径(path: str) -> str:
    """获取绝对路径"""
    return os.path.abspath(path)


def 规范化路径(path: str) -> str:
    """规范化路径（去除多余分隔符和引用）"""
    return os.path.normpath(path)


def 真实路径(path: str) -> str:
    """获取真实路径（解析符号链接）"""
    return os.path.realpath(path)


def 路径分割(path: str) -> tuple:
    """分割路径为(目录, 文件名)"""
    return os.path.split(path)


def 扩展名分割(path: str) -> tuple:
    """分割路径为(主名, 扩展名)"""
    return os.path.splitext(path)


def 获取文件名不含扩展名(path: str) -> str:
    """获取文件名（不含扩展名）"""
    name, _ = os.path.splitext(os.path.basename(path))
    return name


def 路径存在(path: str) -> bool:
    """检查路径是否存在（文件或目录）"""
    return os.path.exists(path)


def 是否符号链接(path: str) -> bool:
    """检查是否为符号链接"""
    return os.path.islink(path)


def 是否可执行(path: str) -> bool:
    """检查是否可执行"""
    return os.access(path, os.X_OK)


def 是否可读(path: str) -> bool:
    """检查是否可读"""
    return os.access(path, os.R_OK)


def 是否可写(path: str) -> bool:
    """检查是否可写"""
    return os.access(path, os.W_OK)


def 文件修改时间(path: str) -> float:
    """获取文件修改时间（时间戳）"""
    return os.path.getmtime(path)


def 文件访问时间(path: str) -> float:
    """获取文件访问时间（时间戳）"""
    return os.path.getatime(path)


def 文件创建时间(path: str) -> float:
    """获取文件创建时间（时间戳）"""
    return os.path.getctime(path)


def 文件修改时间字符串(path: str, 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取文件修改时间（格式化字符串）"""
    return time.strftime(格式, time.localtime(os.path.getmtime(path)))


def 文件访问时间字符串(path: str, 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取文件访问时间（格式化字符串）"""
    return time.strftime(格式, time.localtime(os.path.getatime(path)))


def 文件创建时间字符串(path: str, 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取文件创建时间（格式化字符串）"""
    return time.strftime(格式, time.localtime(os.path.getctime(path)))


def 文件属性(path: str) -> Dict[str, Any]:
    """获取文件属性"""
    stat = os.stat(path)
    return {
        '大小': stat.st_size,
        '修改时间': stat.st_mtime,
        '访问时间': stat.st_atime,
        '创建时间': stat.st_ctime,
        '权限': oct(stat.st_mode)[-4:],
        'inode': stat.st_ino,
        '链接数': stat.st_nlink,
        '用户ID': stat.st_uid,
        '组ID': stat.st_gid,
    }


def 遍历目录(dir_path: str, 递归: bool = False) -> List[str]:
    """遍历目录，返回文件路径列表"""
    result = []
    if 递归:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                result.append(os.path.join(root, file))
    else:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            if os.path.isfile(full_path):
                result.append(full_path)
    return result


def 遍历目录树(dir_path: str) -> List[str]:
    """遍历目录树（递归，包含所有文件）"""
    return 遍历目录(dir_path, 递归=True)


def 目录列表(dir_path: str) -> List[str]:
    """列出目录中的所有项（文件和目录）"""
    return os.listdir(dir_path)


def 子目录列表(dir_path: str) -> List[str]:
    """列出目录中的子目录"""
    result = []
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            result.append(full_path)
    return result


def 文件列表(dir_path: str) -> List[str]:
    """列出目录中的文件（完整路径）"""
    result = []
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isfile(full_path):
            result.append(full_path)
    return result


def 按扩展名筛选(dir_path: str, 扩展名: str) -> List[str]:
    """按扩展名筛选文件"""
    result = []
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isfile(full_path) and item.endswith(扩展名):
            result.append(full_path)
    return result


def 复制目录(src: str, dst: str) -> None:
    """复制目录"""
    shutil.copytree(src, dst)


def 重命名(src: str, dst: str) -> None:
    """重命名文件或目录"""
    os.rename(src, dst)


def 删除空目录(path: str) -> None:
    """删除空目录"""
    os.rmdir(path)


def 移动目录(src: str, dst: str) -> None:
    """移动目录"""
    shutil.move(src, dst)


def 创建符号链接(target: str, link_path: str) -> None:
    """创建符号链接"""
    os.symlink(target, link_path)


def 读取符号链接(link_path: str) -> str:
    """读取符号链接目标"""
    return os.readlink(link_path)


def 创建临时文件(suffix: str = '', prefix: str = 'tmp', dir: str = None) -> str:
    """创建临时文件，返回文件名"""
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(fd)
    return path


def 创建临时目录(suffix: str = '', prefix: str = 'tmp', dir: str = None) -> str:
    """创建临时目录，返回目录名"""
    return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)


def 删除临时文件(path: str) -> None:
    """删除临时文件"""
    os.remove(path)


def 删除临时目录(path: str) -> None:
    """删除临时目录"""
    shutil.rmtree(path)


def 读取二进制文件(path: str) -> bytes:
    """读取二进制文件"""
    with open(path, 'rb') as f:
        return f.read()


def 写入二进制文件(path: str, content: bytes) -> None:
    """写入二进制文件"""
    with open(path, 'wb') as f:
        f.write(content)


def 追加二进制文件(path: str, content: bytes) -> None:
    """追加二进制内容到文件"""
    with open(path, 'ab') as f:
        f.write(content)


def 文件行列表(path: str, encoding: str = 'utf-8') -> List[str]:
    """读取文件为行列表"""
    with open(path, 'r', encoding=encoding) as f:
        return f.readlines()


def 写入行列表(path: str, 行列表: List[str], encoding: str = 'utf-8') -> None:
    """写入行列表到文件"""
    with open(path, 'w', encoding=encoding) as f:
        f.writelines(行列表)


def 读取文件块(path: str, 块大小: int = 4096, encoding: str = 'utf-8') -> List[str]:
    """按块读取文件"""
    blocks = []
    with open(path, 'r', encoding=encoding) as f:
        while True:
            block = f.read(块大小)
            if not block:
                break
            blocks.append(block)
    return blocks


def 当前工作目录() -> str:
    """获取当前工作目录"""
    return os.getcwd()


def 切换工作目录(path: str) -> None:
    """切换工作目录"""
    os.chdir(path)


def 获取环境变量(name: str, 默认值: str = None) -> Optional[str]:
    """获取环境变量"""
    return os.environ.get(name, 默认值)


def 设置环境变量(name: str, value: str) -> None:
    """设置环境变量"""
    os.environ[name] = value


def 目录大小(path: str) -> int:
    """计算目录大小（字节）"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    return total


def 文件扩展名匹配(path: str, 扩展名: str) -> bool:
    """检查文件扩展名是否匹配"""
    return os.path.splitext(path)[1] == 扩展名


def 路径比较(path1: str, path2: str) -> bool:
    """比较两个路径是否相同"""
    return os.path.samefile(path1, path2)


def 获取磁盘使用情况(path: str = '/') -> Dict[str, Any]:
    """获取磁盘使用情况"""
    usage = shutil.disk_usage(path)
    return {
        '总空间': usage.total,
        '已用空间': usage.used,
        '可用空间': usage.free,
        '使用率': usage.used / usage.total * 100,
    }


def 创建文件(path: str) -> None:
    """创建空文件"""
    with open(path, 'w') as f:
        pass


def 触摸文件(path: str) -> None:
    """更新文件时间戳（不存在则创建）"""
    if os.path.exists(path):
        os.utime(path)
    else:
        创建文件(path)


def 批量重命名(dir_path: str, 前缀: str, 起始编号: int = 1, 扩展名: str = '') -> None:
    """批量重命名文件"""
    files = 文件列表(dir_path)
    for i, filepath in enumerate(files, 起始编号):
        _, ext = os.path.splitext(filepath)
        new_name = f"{前缀}{i}{ext}" if not 扩展名 else f"{前缀}{i}{扩展名}"
        os.rename(filepath, os.path.join(dir_path, new_name))


def 文件编码检测(path: str) -> str:
    """检测文件编码（简化版）"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            f.read()
        return 'utf-8'
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='gbk') as f:
                f.read()
            return 'gbk'
        except UnicodeDecodeError:
            return '未知'