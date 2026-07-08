"""
JSON解析器模块 - JSON序列化与反序列化

提供JSON数据处理功能，包括：
- JSON序列化（对象转JSON字符串）
- JSON反序列化（JSON字符串转对象）
- JSON文件读写
- JSON格式化与压缩
"""
import json
from typing import Dict, List, Any, Optional


def 解析JSON(字符串: str) -> Any:
    """解析JSON字符串"""
    return json.loads(字符串)


def 生成JSON(对象: Any, 缩进: int = None, 确保ASCII: bool = True) -> str:
    """生成JSON字符串"""
    return json.dumps(对象, indent=缩进, ensure_ascii=确保ASCII)


def 读取JSON文件(文件路径: str) -> Any:
    """读取JSON文件"""
    with open(文件路径, 'r', encoding='utf-8') as f:
        return json.load(f)


def 写入JSON文件(文件路径: str, 对象: Any, 缩进: int = 2, 确保ASCII: bool = False):
    """写入JSON文件"""
    with open(文件路径, 'w', encoding='utf-8') as f:
        json.dump(对象, f, indent=缩进, ensure_ascii=确保ASCII)


def JSON转字典(字符串: str) -> Dict[str, Any]:
    """JSON字符串转字典"""
    return json.loads(字符串)


def 字典转JSON(字典: Dict[str, Any], 缩进: int = None) -> str:
    """字典转JSON字符串"""
    return json.dumps(字典, indent=缩进, ensure_ascii=False)


def JSON转列表(字符串: str) -> List[Any]:
    """JSON字符串转列表"""
    return json.loads(字符串)


def 列表转JSON(列表: List[Any], 缩进: int = None) -> str:
    """列表转JSON字符串"""
    return json.dumps(列表, indent=缩进, ensure_ascii=False)


def JSON格式化(字符串: str, 缩进: int = 2) -> str:
    """格式化JSON字符串"""
    对象 = json.loads(字符串)
    return json.dumps(对象, indent=缩进, ensure_ascii=False)


def JSON压缩(字符串: str) -> str:
    """压缩JSON字符串"""
    对象 = json.loads(字符串)
    return json.dumps(对象, separators=(',', ':'), ensure_ascii=False)


def JSON验证(字符串: str) -> bool:
    """验证JSON格式是否正确"""
    try:
        json.loads(字符串)
        return True
    except ValueError:
        return False


def JSON合并(*对象列表: Any) -> Dict[str, Any]:
    """合并多个JSON对象"""
    结果 = {}
    for obj in 对象列表:
        if isinstance(obj, dict):
            结果.update(obj)
    return 结果


def JSON深拷贝(对象: Any) -> Any:
    """深拷贝JSON对象"""
    return json.loads(json.dumps(对象))


def JSON提取值(字符串: str, 路径: str) -> Any:
    """提取JSON中的值（支持点分隔路径）"""
    对象 = json.loads(字符串)
    当前 = 对象
    for 键 in 路径.split('.'):
        if isinstance(当前, dict) and 键 in 当前:
            当前 = 当前[键]
        elif isinstance(当前, list) and 键.isdigit():
            当前 = 当前[int(键)]
        else:
            return None
    return 当前


def JSON设置值(字符串: str, 路径: str, 值: Any) -> str:
    """设置JSON中的值（支持点分隔路径）"""
    对象 = json.loads(字符串)
    当前 = 对象
    键列表 = 路径.split('.')
    
    for i, 键 in enumerate(键列表[:-1]):
        if isinstance(当前, dict) and 键 in 当前:
            当前 = 当前[键]
        elif isinstance(当前, list) and 键.isdigit():
            当前 = 当前[int(键)]
        else:
            return 字符串
    
    最后键 = 键列表[-1]
    if isinstance(当前, dict):
        当前[最后键] = 值
    elif isinstance(当前, list) and 最后键.isdigit():
        当前[int(最后键)] = 值
    
    return json.dumps(对象, indent=2, ensure_ascii=False)


def JSON删除键(字符串: str, 路径: str) -> str:
    """删除JSON中的键（支持点分隔路径）"""
    对象 = json.loads(字符串)
    当前 = 对象
    键列表 = 路径.split('.')
    
    for i, 键 in enumerate(键列表[:-1]):
        if isinstance(当前, dict) and 键 in 当前:
            当前 = 当前[键]
        elif isinstance(当前, list) and 键.isdigit():
            当前 = 当前[int(键)]
        else:
            return 字符串
    
    最后键 = 键列表[-1]
    if isinstance(当前, dict) and 最后键 in 当前:
        del 当前[最后键]
    elif isinstance(当前, list) and 最后键.isdigit():
        del 当前[int(最后键)]
    
    return json.dumps(对象, indent=2, ensure_ascii=False)


def JSON遍历(字符串: str, 回调函数: callable):
    """遍历JSON对象"""
    对象 = json.loads(字符串)
    
    def 递归遍历(当前, 路径=''):
        if isinstance(当前, dict):
            for 键, 值 in 当前.items():
                回调函数(f'{路径}.{键}' if 路径 else 键, 值)
                递归遍历(值, f'{路径}.{键}' if 路径 else 键)
        elif isinstance(当前, list):
            for i, 值 in enumerate(当前):
                回调函数(f'{路径}[{i}]', 值)
                递归遍历(值, f'{路径}[{i}]')
    
    递归遍历(对象)


def JSON查找(字符串: str, 键: str) -> List[Any]:
    """查找JSON中所有指定键的值"""
    结果 = []
    对象 = json.loads(字符串)
    
    def 递归查找(当前):
        if isinstance(当前, dict):
            if 键 in 当前:
                结果.append(当前[键])
            for 值 in 当前.values():
                递归查找(值)
        elif isinstance(当前, list):
            for 值 in 当前:
                递归查找(值)
    
    递归查找(对象)
    return 结果


def JSON计数(字符串: str) -> Dict[str, int]:
    """统计JSON中各类型的数量"""
    对象 = json.loads(字符串)
    计数 = {'dict': 0, 'list': 0, 'str': 0, 'int': 0, 'float': 0, 'bool': 0, 'null': 0}
    
    def 递归计数(当前):
        if isinstance(当前, dict):
            计数['dict'] += 1
            for 值 in 当前.values():
                递归计数(值)
        elif isinstance(当前, list):
            计数['list'] += 1
            for 值 in 当前:
                递归计数(值)
        elif isinstance(当前, str):
            计数['str'] += 1
        elif isinstance(当前, int):
            计数['int'] += 1
        elif isinstance(当前, float):
            计数['float'] += 1
        elif isinstance(当前, bool):
            计数['bool'] += 1
        elif 当前 is None:
            计数['null'] += 1
    
    递归计数(对象)
    return 计数


def JSON转换XML(字符串: str, 根节点: str = 'root') -> str:
    """将JSON转换为XML"""
    对象 = json.loads(字符串)
    
    def 转换(数据, 父标签):
        if isinstance(数据, dict):
            结果 = []
            for 键, 值 in 数据.items():
                结果.append(f'<{键}>')
                结果.append(转换(值, 键))
                结果.append(f'</{键}>')
            return '\n'.join(结果)
        elif isinstance(数据, list):
            结果 = []
            for i, 项 in enumerate(数据):
                结果.append(f'<item index="{i}">')
                结果.append(转换(项, 'item'))
                结果.append('</item>')
            return '\n'.join(结果)
        else:
            return str(data)
    
    return f'<{根节点}>\n{转换(对象, 根节点)}\n</{根节点}>'


def JSON转Python对象(字符串: str, 类映射: Dict[str, type] = None) -> Any:
    """JSON转Python对象（支持自定义类）"""
    对象 = json.loads(字符串)
    
    if 类映射 and isinstance(对象, dict) and '__class__' in 对象:
        类名 = 对象['__class__']
        if 类名 in 类映射:
            实例 = 类映射[类名].__new__(类映射[类名])
            实例.__dict__.update(对象['__data__'])
            return 实例
    
    return 对象


def Python对象转JSON(对象: Any) -> str:
    """Python对象转JSON（支持自定义类）"""
    def 默认处理(obj):
        if hasattr(obj, '__dict__'):
            return {'__class__': obj.__class__.__name__, '__data__': obj.__dict__}
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    
    return json.dumps(对象, default=默认处理, indent=2, ensure_ascii=False)


def JSON转CSV(字符串: str, 输出文件: str = None) -> str:
    """将JSON数组转换为CSV"""
    对象 = json.loads(字符串)
    
    if not isinstance(对象, list):
        raise ValueError('JSON必须是数组格式')
    
    if not 对象:
        return ''
    
    表头 = set()
    for 项 in 对象:
        if isinstance(项, dict):
            表头.update(项.keys())
    表头 = list(表头)
    
    行 = [','.join(表头)]
    for 项 in 对象:
        单元格 = []
        for 列 in 表头:
            值 = 项.get(列, '')
            if isinstance(值, str):
                值 = 值.replace('"', '""')
                单元格.append(f'"{值}"')
            else:
                单元格.append(str(值))
        行.append(','.join(单元格))
    
    CSV内容 = '\n'.join(行)
    
    if 输出文件:
        with open(输出文件, 'w', encoding='utf-8') as f:
            f.write(CSV内容)
    
    return CSV内容


def JSON格式化美化(字符串: str) -> str:
    """美化JSON字符串（带语法高亮）"""
    对象 = json.loads(字符串)
    
    颜色 = {
        'key': '\033[94m',
        'string': '\033[92m',
        'number': '\033[93m',
        'bool': '\033[95m',
        'null': '\033[91m',
        'end': '\033[0m'
    }
    
    def 美化(数据, 缩进=0):
        if isinstance(数据, dict):
            结果 = ['{']
            缩进 += 2
            项 = []
            for 键, 值 in 数据.items():
                项.append(f'{" " * 缩进}{颜色["key"]}"{键}"{颜色["end"]}: {美化(值, 缩进)}')
            结果.append(',\n'.join(项))
            缩进 -= 2
            结果.append(f'{" " * 缩进}}}',)
            return '\n'.join(结果)
        elif isinstance(数据, list):
            结果 = ['[']
            缩进 += 2
            项 = [f'{" " * 缩进}{美化(值, 缩进)}' for 值 in 数据]
            结果.append(',\n'.join(项))
            缩进 -= 2
            结果.append(f'{" " * 缩进}]')
            return '\n'.join(结果)
        elif isinstance(数据, str):
            return f'{颜色["string"]}"{数据}"{颜色["end"]}'
        elif isinstance(数据, (int, float)):
            return f'{颜色["number"]}{数据}{颜色["end"]}'
        elif isinstance(数据, bool):
            return f'{颜色["bool"]}{数据}{颜色["end"]}'
        elif 数据 is None:
            return f'{颜色["null"]}null{颜色["end"]}'
    
    return 美化(对象)


def JSON获取大小(字符串: str) -> int:
    """获取JSON字符串大小（字节数）"""
    return len(字符串.encode('utf-8'))


def JSON版本() -> str:
    """获取JSON模块版本"""
    return json.__name__


def JSON编码器(对象: Any) -> str:
    """JSON编码器"""
    return json.dumps(对象)


def JSON解码器(字符串: str) -> Any:
    """JSON解码器"""
    return json.loads(字符串)