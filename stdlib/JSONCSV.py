"""
段言标准库 - JSON/CSV 数据格式模块

提供 JSON 和 CSV 格式的解析与生成函数
"""

import json
import csv
from typing import Any, Dict, List, Optional
import io


def JSON解析(text: str) -> Any:
    """解析 JSON 字符串"""
    return json.loads(text)


def JSON生成(obj: Any, 缩进: Optional[int] = None) -> str:
    """生成 JSON 字符串"""
    if 缩进 is not None:
        return json.dumps(obj, ensure_ascii=False, indent=缩进)
    return json.dumps(obj, ensure_ascii=False)


def CSV解析(text: str, 分隔符: str = ',') -> List[List[str]]:
    """解析 CSV 字符串"""
    reader = csv.reader(text.splitlines(), delimiter=分隔符)
    return [row for row in reader]


def CSV生成(rows: List[List[str]], 分隔符: str = ',') -> str:
    """生成 CSV 字符串"""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=分隔符)
    writer.writerows(rows)
    return output.getvalue().rstrip('\r\n')


def CSV解析到列表(text: str, 分隔符: str = ',') -> List[Dict[str, str]]:
    """解析 CSV 字符串为字典列表（首行为表头）"""
    reader = csv.DictReader(text.splitlines(), delimiter=分隔符)
    return [row for row in reader]


def CSV从列表生成(rows: List[Dict[str, str]], 分隔符: str = ',') -> str:
    """从字典列表生成 CSV（键名为表头）"""
    if not rows:
        return ''
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys(), delimiter=分隔符)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().rstrip('\r\n')