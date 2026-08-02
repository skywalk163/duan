"""
模板引擎模块 - 变量替换、条件渲染

提供轻量级模板引擎功能，包括：
- 变量替换
- 条件判断
- 循环渲染
- 模板继承
- 过滤器
"""
import re
from typing import Dict, Any, List, Callable


class 模板引擎:
    """模板引擎类"""
    
    def __init__(self):
        self._过滤器 = {}
        self._全局变量 = {}
        self._模板缓存 = {}
    
    def 注册过滤器(self, 名称: str, 函数: Callable):
        """注册过滤器函数"""
        self._过滤器[名称] = 函数
    
    def 设置全局变量(self, **变量):
        """设置全局变量"""
        self._全局变量.update(变量)
    
    def 渲染(self, 模板内容: str, **变量) -> str:
        """渲染模板"""
        上下文 = dict(self._全局变量)
        上下文.update(变量)
        return self._解析模板(模板内容, 上下文)
    
    def 渲染文件(self, 文件路径: str, **变量) -> str:
        """渲染模板文件"""
        if 文件路径 not in self._模板缓存:
            with open(文件路径, 'r', encoding='utf-8') as f:
                self._模板缓存[文件路径] = f.read()
        return self.渲染(self._模板缓存[文件路径], **变量)
    
    def _解析模板(self, 内容: str, 上下文: Dict[str, Any]) -> str:
        """解析模板内容"""
        内容 = self._处理条件判断(内容, 上下文)
        内容 = self._处理循环(内容, 上下文)
        内容 = self._处理变量替换(内容, 上下文)
        内容 = self._处理过滤器(内容, 上下文)
        return 内容
    
    def _处理变量替换(self, 内容: str, 上下文: Dict[str, Any]) -> str:
        """处理变量替换 {{变量名}}"""
        模式 = r'\{\{(\w+)\}\}'
        
        def 替换(match):
            变量名 = match.group(1)
            if 变量名 in 上下文:
                return str(上下文[变量名])
            return ''
        
        return re.sub(模式, 替换, 内容)
    
    def _处理条件判断(self, 内容: str, 上下文: Dict[str, Any]) -> str:
        """处理条件判断 {% if %} {% endif %}"""
        模式 = r'{% if (\w+) %}(.*?){% endif %}'
        
        def 替换(match):
            变量名 = match.group(1)
            内容块 = match.group(2)
            if 变量名 in 上下文 and 上下文[变量名]:
                return self._解析模板(内容块, 上下文)
            return ''
        
        return re.sub(模式, 替换, 内容, flags=re.DOTALL)
    
    def _处理循环(self, 内容: str, 上下文: Dict[str, Any]) -> str:
        """处理循环 {% for %} {% endfor %}"""
        模式 = r'{% for (\w+) in (\w+) %}(.*?){% endfor %}'
        
        def 替换(match):
            元素名 = match.group(1)
            列表名 = match.group(2)
            内容块 = match.group(3)
            
            if 列表名 not in 上下文:
                return ''
            
            列表 = 上下文[列表名]
            if not isinstance(列表, (list, tuple)):
                return ''
            
            结果 = []
            for 元素 in 列表:
                新上下文 = dict(上下文)
                新上下文[元素名] = 元素
                结果.append(self._解析模板(内容块, 新上下文))
            return ''.join(结果)
        
        return re.sub(模式, 替换, 内容, flags=re.DOTALL)
    
    def _处理过滤器(self, 内容: str, 上下文: Dict[str, Any]) -> str:
        """处理过滤器 {{变量|过滤器}}"""
        模式 = r'\{\{(\w+)\|(\w+)\}\}'
        
        def 替换(match):
            变量名 = match.group(1)
            过滤器名 = match.group(2)
            
            if 变量名 not in 上下文:
                return ''
            
            值 = 上下文[变量名]
            
            if 过滤器名 in self._过滤器:
                return str(self._过滤器[过滤器名](值))
            
            if hasattr(self, f'_过滤器_{过滤器名}'):
                return str(getattr(self, f'_过滤器_{过滤器名}')(值))
            
            return str(值)
        
        return re.sub(模式, 替换, 内容)
    
    def _过滤器_大写(self, 值: str) -> str:
        """转大写"""
        return str(值).upper()
    
    def _过滤器_小写(self, 值: str) -> str:
        """转小写"""
        return str(值).lower()
    
    def _过滤器_首字母大写(self, 值: str) -> str:
        """首字母大写"""
        return str(值).capitalize()
    
    def _过滤器_长度(self, 值) -> int:
        """获取长度"""
        return len(str(值))
    
    def _过滤器_截断(self, 值: str, 长度: int = 100) -> str:
        """截断字符串"""
        文本 = str(值)
        if len(文本) <= 长度:
            return 文本
        return 文本[:长度] + '...'
    
    def _过滤器_安全(self, 值: str) -> str:
        """标记为安全（不转义）"""
        return str(值)
    
    def _过滤器_日期格式化(self, 值, 格式: str = '%Y-%m-%d') -> str:
        """日期格式化"""
        if hasattr(值, 'strftime'):
            return 值.strftime(格式)
        return str(值)


def 渲染模板(模板内容: str, **变量) -> str:
    """渲染模板（便捷函数）"""
    引擎 = 模板引擎()
    return 引擎.渲染(模板内容, **变量)


def 渲染模板文件(文件路径: str, **变量) -> str:
    """渲染模板文件（便捷函数）"""
    引擎 = 模板引擎()
    return 引擎.渲染文件(文件路径, **变量)


def 创建模板引擎() -> 模板引擎:
    """创建模板引擎实例"""
    return 模板引擎()


def 变量替换(文本: str, **变量) -> str:
    """简单变量替换"""
    引擎 = 模板引擎()
    return 引擎._处理变量替换(文本, 变量)


def 条件渲染(文本: str, **变量) -> str:
    """条件渲染"""
    引擎 = 模板引擎()
    return 引擎._处理条件判断(文本, 变量)


def 循环渲染(文本: str, **变量) -> str:
    """循环渲染"""
    引擎 = 模板引擎()
    return 引擎._处理循环(文本, 变量)


class 简单模板:
    """简单模板类（简化版）"""
    
    def __init__(self, 模板内容: str):
        self._模板内容 = 模板内容
        self._变量 = {}
    
    def 设置变量(self, **变量):
        """设置变量"""
        self._变量.update(变量)
    
    def 渲染(self, 变量: dict = None, **额外变量) -> str:
        """渲染模板"""
        if 变量:
            self._变量.update(变量)
        self._变量.update(额外变量)
        结果 = self._模板内容
        for 名称, 值 in self._变量.items():
            结果 = 结果.replace(f'{{{{{名称}}}}}', str(值))
        return 结果
    
    def __str__(self) -> str:
        return self._模板内容


class 字符串模板:
    """字符串模板类（类似 str.format）"""
    
    def __init__(self, 模板: str):
        self._模板 = 模板
    
    def 格式化(self, **变量) -> str:
        """格式化模板"""
        return self._模板.format(**变量)
    
    def 安全格式化(self, **变量) -> str:
        """安全格式化（转义特殊字符）"""
        转义变量 = {k: str(v).replace('{', '{{').replace('}', '}}') for k, v in 变量.items()}
        return self._模板.format(**转义变量)


def 格式化字符串(模板: str, **变量) -> str:
    """格式化字符串"""
    return 模板.format(**变量)


def 安全格式化(模板: str, **变量) -> str:
    """安全格式化字符串"""
    转义变量 = {k: str(v).replace('{', '{{').replace('}', '}}') for k, v in 变量.items()}
    return 模板.format(**转义变量)


def HTML转义(文本: str) -> str:
    """HTML转义"""
    映射 = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    return ''.join(映射.get(c, c) for c in 文本)


def HTML反转义(文本: str) -> str:
    """HTML反转义"""
    映射 = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
    }
    for 转义, 原始 in 映射.items():
        文本 = 文本.replace(转义, 原始)
    return 文本


def 模板替换(文本: str, 变量: Dict[str, Any]) -> str:
    """模板替换（使用 $变量名 语法）"""
    for 名称, 值 in 变量.items():
        文本 = 文本.replace(f'${名称}', str(值))
    return 文本


def 模板替换花括号(文本: str, 变量: Dict[str, Any]) -> str:
    """模板替换（使用 {变量名} 语法）"""
    for 名称, 值 in 变量.items():
        文本 = 文本.replace(f'{{{名称}}}', str(值))
    return 文本


def 生成HTML列表(项目列表: List[str], 有序: bool = False) -> str:
    """生成HTML列表"""
    标签 = 'ol' if 有序 else 'ul'
    项目 = '\n'.join(f'  <li>{HTML转义(item)}</li>' for item in 项目列表)
    return f'<{标签}>\n{项目}\n</{标签}>'


def 生成HTML表格(数据: List[List[str]], 表头: List[str] = None) -> str:
    """生成HTML表格"""
    表头行 = ''
    if 表头:
        表头单元格 = ''.join(f'<th>{HTML转义(h)}</th>' for h in 表头)
        表头行 = f'<thead><tr>{表头单元格}</tr></thead>\n'
    
    行内容 = []
    for 行 in 数据:
        单元格 = ''.join(f'<td>{HTML转义(str(cell))}</td>' for cell in 行)
        行内容.append(f'<tr>{单元格}</tr>')
    
    return f'<table>\n{表头行}<tbody>\n{"".join(行内容)}\n</tbody>\n</table>'


def 生成邮件模板(收件人: str, 主题: str, 内容: str) -> str:
    """生成邮件模板"""
    return f"""To: {收件人}
Subject: {主题}

{内容}"""


def 生成JSON模板(数据: Dict[str, Any]) -> str:
    """生成JSON模板"""
    import json
    return json.dumps(数据, indent=2, ensure_ascii=False)