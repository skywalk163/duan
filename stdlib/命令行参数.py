"""段言标准库 - 命令行参数模块"""

import sys
from typing import Any, List, Dict


def 解析参数(参数列表: List[str]) -> Dict[str, Any]:
    """解析命令行参数，支持 -name value 和 --name value 格式"""
    结果 = {}
    i = 0
    while i < len(参数列表):
        参数 = 参数列表[i]
        if 参数.startswith('--'):
            名称 = 参数[2:]
            if i + 1 < len(参数列表) and not 参数列表[i + 1].startswith('-'):
                结果[名称] = 参数列表[i + 1]
                i += 2
            else:
                结果[名称] = True
                i += 1
        elif 参数.startswith('-'):
            名称 = 参数[1:]
            if i + 1 < len(参数列表) and not 参数列表[i + 1].startswith('-'):
                结果[名称] = 参数列表[i + 1]
                i += 2
            else:
                结果[名称] = True
                i += 1
        else:
            i += 1
    return 结果


def 获取参数(参数: Dict[str, Any], 名称: str, 默认值: Any = None) -> Any:
    """获取参数值"""
    return 参数.get(名称, 默认值)


def 检查参数(参数: Dict[str, Any], 名称: str) -> bool:
    """检查参数是否存在"""
    return 名称 in 参数
