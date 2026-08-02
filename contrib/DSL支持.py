"""
DSL支持模块 - 领域特定语言解析

提供DSL解析和执行功能，包括：
- 简单DSL解析器
- 表达式求值
- 语法分析
- 自定义语法
- 模板表达式
"""
import re
from typing import Any, Callable, Dict, List, Optional, Tuple


class DSL解析异常(Exception):
    """DSL解析异常"""
    pass


class 词法分析器:
    """词法分析器"""
    
    def __init__(self):
        self._token规则列表: List[Tuple[str, str]] = []
    
    def 添加规则(self, 类型: str, 模式: str):
        """添加词法规则"""
        self._token规则列表.append((类型, 模式))
    
    def 分词(self, 代码: str) -> List[Dict[str, Any]]:
        """分词"""
        token列表 = []
        位置 = 0
        行号 = 1
        列号 = 1
        
        while 位置 < len(代码):
            匹配 = None
            
            for 类型, 模式 in self._token规则列表:
                正则 = re.compile(模式)
                匹配 = 正则.match(代码, 位置)
                if 匹配:
                    值 = 匹配.group(0)
                    token列表.append({
                        '类型': 类型,
                        '值': 值,
                        '行号': 行号,
                        '列号': 列号
                    })
                    
                    for 字符 in 值:
                        if 字符 == '\n':
                            行号 += 1
                            列号 = 1
                        else:
                            列号 += 1
                    
                    位置 = 匹配.end()
                    break
            
            if not 匹配:
                raise DSL解析异常(f'无法识别的字符: {代码[位置]} (行{行号}, 列{列号})')
        
        return token列表
    
    @staticmethod
    def 创建默认词法分析器() -> '词法分析器':
        """创建默认词法分析器"""
        分析器 = 词法分析器()
        分析器.添加规则('数字', r'\d+(\.\d+)?')
        分析器.添加规则('字符串', r'"[^"]*"')
        分析器.添加规则('标识符', r'[a-zA-Z_][a-zA-Z0-9_]*')
        分析器.添加规则('运算符', r'[+\-*/=<>!&|]')
        分析器.添加规则('括号', r'[()\[\]{}]')
        分析器.添加规则('逗号', r',')
        分析器.添加规则('点号', r'\.')
        分析器.添加规则('空白', r'\s+')
        return 分析器


class 语法节点:
    """语法节点"""
    
    def __init__(self, 类型: str, 值: Any = None, 子节点: List['语法节点'] = None):
        self.类型 = 类型
        self.值 = 值
        self.子节点 = 子节点 or []
    
    def __repr__(self) -> str:
        if self.子节点:
            return f'{self.类型}({self.值})[{len(self.子节点)}个子节点]'
        return f'{self.类型}({self.值})'


class 语法分析器:
    """语法分析器"""
    
    def __init__(self):
        self._token列表: List[Dict[str, Any]] = []
        self._当前位置 = 0
    
    def 分析(self, token列表: List[Dict[str, Any]]) -> 语法节点:
        """分析token列表生成AST"""
        self._token列表 = [t for t in token列表 if t['类型'] != '空白']
        self._当前位置 = 0
        
        return self._解析表达式()
    
    def _当前token(self) -> Optional[Dict[str, Any]]:
        """获取当前token"""
        if self._当前位置 < len(self._token列表):
            return self._token列表[self._当前位置]
        return None
    
    def _消费token(self, 期望类型: str = None) -> Dict[str, Any]:
        """消费一个token"""
        token = self._当前token()
        if not token:
            raise DSL解析异常('意外的结束')
        if 期望类型 and token['类型'] != 期望类型:
            raise DSL解析异常(f'期望{期望类型}, 实际{token["类型"]}')
        self._当前位置 += 1
        return token
    
    def _解析表达式(self) -> 语法节点:
        """解析表达式"""
        return self._解析加减()
    
    def _解析加减(self) -> 语法节点:
        """解析加减表达式"""
        左节点 = self._解析乘除()
        
        while self._当前token() and self._当前token()['类型'] == '运算符' and self._当前token()['值'] in '+-':
            运算符 = self._消费token('运算符')
            右节点 = self._解析乘除()
            左节点 = 语法节点('二元运算', 运算符['值'], [左节点, 右节点])
        
        return 左节点
    
    def _解析乘除(self) -> 语法节点:
        """解析乘除表达式"""
        左节点 = self._解析基础表达式()
        
        while self._当前token() and self._当前token()['类型'] == '运算符' and self._当前token()['值'] in '*/':
            运算符 = self._消费token('运算符')
            右节点 = self._解析基础表达式()
            左节点 = 语法节点('二元运算', 运算符['值'], [左节点, 右节点])
        
        return 左节点
    
    def _解析基础表达式(self) -> 语法节点:
        """解析基础表达式"""
        token = self._当前token()
        
        if not token:
            raise DSL解析异常('意外的结束')
        
        if token['类型'] == '数字':
            self._消费token()
            return 语法节点('数字', float(token['值']))
        
        if token['类型'] == '字符串':
            self._消费token()
            return 语法节点('字符串', token['值'][1:-1])
        
        if token['类型'] == '标识符':
            self._消费token()
            
            if self._当前token() and self._当前token()['类型'] == '括号' and self._当前token()['值'] == '(':
                self._消费token()
                参数列表 = []
                
                while self._当前token() and not (self._当前token()['类型'] == '括号' and self._当前token()['值'] == ')'):
                    参数列表.append(self._解析表达式())
                    if self._当前token() and self._当前token()['类型'] == '逗号':
                        self._消费token()
                
                self._消费token()
                return 语法节点('函数调用', token['值'], 参数列表)
            
            return 语法节点('变量', token['值'])
        
        if token['类型'] == '括号' and token['值'] == '(':
            self._消费token()
            表达式 = self._解析表达式()
            self._消费token()
            return 表达式
        
        raise DSL解析异常(f'意外的token: {token}')


class 解释器:
    """DSL解释器"""
    
    def __init__(self):
        self._变量字典: Dict[str, Any] = {}
        self._函数字典: Dict[str, Callable] = {}
    
    def 设置变量(self, 名称: str, 值: Any):
        """设置变量"""
        self._变量字典[名称] = 值
    
    def 获取变量(self, 名称: str) -> Any:
        """获取变量"""
        if 名称 not in self._变量字典:
            raise DSL解析异常(f'未定义的变量: {名称}')
        return self._变量字典[名称]
    
    def 注册函数(self, 名称: str, 函数: Callable):
        """注册函数"""
        self._函数字典[名称] = 函数
    
    def 求值(self, ast: 语法节点) -> Any:
        """求值"""
        if ast.类型 == '数字':
            return ast.值
        
        if ast.类型 == '字符串':
            return ast.值
        
        if ast.类型 == '变量':
            return self.获取变量(ast.值)
        
        if ast.类型 == '二元运算':
            左值 = self.求值(ast.子节点[0])
            右值 = self.求值(ast.子节点[1])
            运算符 = ast.值
            
            if 运算符 == '+':
                return 左值 + 右值
            if 运算符 == '-':
                return 左值 - 右值
            if 运算符 == '*':
                return 左值 * 右值
            if 运算符 == '/':
                return 左值 / 右值
            if 运算符 == '==':
                return 左值 == 右值
            if 运算符 == '!=':
                return 左值 != 右值
            if 运算符 == '>':
                return 左值 > 右值
            if 运算符 == '<':
                return 左值 < 右值
            
            raise DSL解析异常(f'未知的运算符: {运算符}')
        
        if ast.类型 == '函数调用':
            if ast.值 not in self._函数字典:
                raise DSL解析异常(f'未定义的函数: {ast.值}')
            参数值 = [self.求值(p) for p in ast.子节点]
            return self._函数字典[ast.值](*参数值)
        
        raise DSL解析异常(f'未知的节点类型: {ast.类型}')
    
    def 执行(self, 代码: str) -> Any:
        """执行代码"""
        词法分析器实例 = 词法分析器.创建默认词法分析器()
        token列表 = 词法分析器实例.分词(代码)
        
        语法分析器实例 = 语法分析器()
        ast = 语法分析器实例.分析(token列表)
        
        return self.求值(ast)


class 表达式求值器:
    """简单表达式求值器"""
    
    def __init__(self):
        self._变量: Dict[str, Any] = {}
        self._函数: Dict[str, Callable] = {}
        self._初始化默认函数()
    
    def _初始化默认函数(self):
        """初始化默认函数"""
        self._函数['max'] = max
        self._函数['min'] = min
        self._函数['abs'] = abs
        self._函数['int'] = int
        self._函数['float'] = float
        self._函数['str'] = str
        self._函数['len'] = len
        self._函数['sum'] = sum
        self._函数['round'] = round
    
    def 设置变量(self, 名称: str, 值: Any):
        """设置变量"""
        self._变量[名称] = 值
    
    def 注册函数(self, 名称: str, 函数: Callable):
        """注册函数"""
        self._函数[名称] = 函数
    
    def 求值(self, 表达式: str) -> Any:
        """求值表达式"""
        解释器实例 = 解释器()
        for 名称, 值 in self._变量.items():
            解释器实例.设置变量(名称, 值)
        for 名称, 函数 in self._函数.items():
            解释器实例.注册函数(名称, 函数)
        return 解释器实例.执行(表达式)


class 模板引擎DSL:
    """模板引擎DSL"""
    
    def __init__(self):
        self._变量: Dict[str, Any] = {}
    
    def 设置变量(self, 名称: str, 值: Any):
        """设置模板变量"""
        self._变量[名称] = 值
    
    def 渲染(self, 模板: str, 变量字典: Dict[str, Any] = None) -> str:
        """渲染模板"""
        上下文 = self._变量.copy()
        if 变量字典:
            上下文.update(变量字典)
        
        def 替换变量(匹配):
            表达式 = 匹配.group(1).strip()
            try:
                求值器 = 表达式求值器()
                for 名称, 值 in 上下文.items():
                    求值器.设置变量(名称, 值)
                return str(求值器.求值(表达式))
            except Exception:
                return 匹配.group(0)
        
        结果 = re.sub(r'\{\{(.+?)\}\}', 替换变量, 模板)
        return 结果


class 简单DSL:
    """简单DSL封装"""
    
    def __init__(self):
        self._解释器 = 解释器()
        self._注册内置函数()
    
    def _注册内置函数(self):
        """注册内置函数"""
        self._解释器.注册函数('max', max)
        self._解释器.注册函数('min', min)
        self._解释器.注册函数('abs', abs)
        self._解释器.注册函数('round', round)
        self._解释器.注册函数('print', print)
    
    def 设置变量(self, 名称: str, 值: Any):
        """设置变量"""
        self._解释器.设置变量(名称, 值)
    
    def 注册函数(self, 名称: str, 函数: Callable):
        """注册函数"""
        self._解释器.注册函数(名称, 函数)
    
    def 执行(self, 代码: str) -> Any:
        """执行DSL代码"""
        return self._解释器.执行(代码)
    
    def 求值(self, 表达式: str) -> Any:
        """求值表达式"""
        return self._解释器.执行(表达式)


class 自定义语法:
    """自定义语法定义"""
    
    def __init__(self):
        self._关键字: List[str] = []
        self._运算符: Dict[str, int] = {}
        self._语法规则: List = []
    
    def 添加关键字(self, 关键字: str):
        """添加关键字"""
        self._关键字.append(关键字)
    
    def 添加运算符(self, 运算符: str, 优先级: int):
        """添加运算符"""
        self._运算符[运算符] = 优先级
    
    def 添加语法规则(self, 模式: str, 动作: Callable):
        """添加语法规则"""
        self._语法规则.append((模式, 动作))
    
    def 分析(self, 代码: str) -> Any:
        """分析代码"""
        raise NotImplementedError


# 便捷函数
def 求值表达式(表达式: str, 变量字典: Dict[str, Any] = None) -> Any:
    """求值表达式"""
    求值器 = 表达式求值器()
    if 变量字典:
        for 名称, 值 in 变量字典.items():
            求值器.设置变量(名称, 值)
    return 求值器.求值(表达式)


def 渲染模板(模板: str, 变量字典: Dict[str, Any] = None) -> str:
    """渲染模板"""
    引擎 = 模板引擎DSL()
    return 引擎.渲染(模板, 变量字典)


def 创建DSL() -> 简单DSL:
    """创建简单DSL"""
    return 简单DSL()


def 创建表达式求值器() -> 表达式求值器:
    """创建表达式求值器"""
    return 表达式求值器()


def 创建模板引擎() -> 模板引擎DSL:
    """创建模板引擎"""
    return 模板引擎DSL()


def 分词(代码: str) -> List[Dict[str, Any]]:
    """分词"""
    分析器 = 词法分析器.创建默认词法分析器()
    return 分析器.分词(代码)