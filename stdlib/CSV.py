"""段言标准库 - CSV模块"""

import csv
from typing import List, Dict, Any, Optional


def 读取CSV(文件路径: str, 分隔符: str = ',', 编码: str = 'utf-8') -> List[Dict[str, str]]:
    """读取 CSV 文件，返回字典列表
    
    参数：
        文件路径: CSV文件路径
        分隔符: 列分隔符，默认为逗号
        编码: 文件编码，默认为 utf-8
    
    返回：
        字典列表，每个字典代表一行，键为表头名称
    """
    with open(文件路径, 'r', encoding=编码, newline='') as f:
        reader = csv.DictReader(f, delimiter=分隔符)
        return list(reader)


def 写入CSV(文件路径: str, 数据: List[Dict[str, Any]], 表头: List[str] = None, 分隔符: str = ',', 编码: str = 'utf-8') -> None:
    """写入 CSV 文件
    
    参数：
        文件路径: CSV文件路径
        数据: 字典列表，每个字典代表一行
        表头: 列名列表，如果为None则使用第一个字典的键
        分隔符: 列分隔符，默认为逗号
        编码: 文件编码，默认为 utf-8
    """
    if not 数据:
        with open(文件路径, 'w', encoding=编码, newline='') as f:
            return
    
    if 表头 is None:
        表头 = list(数据[0].keys())
    
    with open(文件路径, 'w', encoding=编码, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=表头, delimiter=分隔符)
        writer.writeheader()
        for 行 in 数据:
            writer.writerow(行)


def 读取TSV(文件路径: str, 编码: str = 'utf-8') -> List[Dict[str, str]]:
    """读取 TSV 文件，返回字典列表
    
    参数：
        文件路径: TSV文件路径
        编码: 文件编码，默认为 utf-8
    
    返回：
        字典列表，每个字典代表一行，键为表头名称
    """
    return 读取CSV(文件路径, 分隔符='\t', 编码=编码)


def 写入TSV(文件路径: str, 数据: List[Dict[str, Any]], 表头: List[str] = None, 编码: str = 'utf-8') -> None:
    """写入 TSV 文件
    
    参数：
        文件路径: TSV文件路径
        数据: 字典列表，每个字典代表一行
        表头: 列名列表，如果为None则使用第一个字典的键
        编码: 文件编码，默认为 utf-8
    """
    写入CSV(文件路径, 数据, 表头=表头, 分隔符='\t', 编码=编码)
