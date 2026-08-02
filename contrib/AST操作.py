"""
AST操作模块 - 解析、修改、生成代码

提供抽象语法树操作功能，包括：
- 代码解析为AST
- AST遍历与修改
- 代码生成
- 模式匹配
- 代码转换
"""
import ast
import inspect
from typing import Any, Callable, Dict, List, Optional, Type


class AST节点类型:
    """AST节点类型常量"""
    模块 = ast.Module
    函数定义 = ast.FunctionDef
    类定义 = ast.ClassDef
    赋值 = ast.Assign
    表达式 = ast.Expr
    调用 = ast.Call
    名称 = ast.Name
    常量 = ast.Constant
    属性 = ast.Attribute
    返回 = ast.Return
    导入 = ast.Import
    导入从 = ast.ImportFrom
    二元运算 = ast.BinOp
    比较 = ast.Compare
    If = ast.If
    For = ast.For
    While = ast.While
    列表 = ast.List
    字典 = ast.Dict
    元组 = ast.Tuple
    Lambda = ast.Lambda


class AST工具:
    """AST工具类"""
    
    @staticmethod
    def 解析代码(代码: str) -> ast.Module:
        """解析代码字符串为AST"""
        return ast.parse(代码)
    
    @staticmethod
    def 解析文件(文件路径: str) -> ast.Module:
        """解析文件为AST"""
        with open(文件路径, 'r', encoding='utf-8') as f:
            代码 = f.read()
        return ast.parse(代码)
    
    @staticmethod
    def 生成代码(树: ast.AST, 缩进: int = 4) -> str:
        """从AST生成代码字符串"""
        return ast.unparse(树)
    
    @staticmethod
    def 美化输出(树: ast.AST, 缩进: int = 2) -> str:
        """美化AST输出"""
        return ast.dump(树, indent=缩进)
    
    @staticmethod
    def 获取函数节点(树: ast.AST, 函数名: str) -> Optional[ast.FunctionDef]:
        """获取指定函数的AST节点"""
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.FunctionDef) and 节点.name == 函数名:
                return 节点
        return None
    
    @staticmethod
    def 获取类节点(树: ast.AST, 类名: str) -> Optional[ast.ClassDef]:
        """获取指定类的AST节点"""
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.ClassDef) and 节点.name == 类名:
                return 节点
        return None
    
    @staticmethod
    def 获取所有函数(树: ast.AST) -> List[ast.FunctionDef]:
        """获取所有函数定义"""
        return [n for n in ast.walk(树) if isinstance(n, ast.FunctionDef)]
    
    @staticmethod
    def 获取所有类(树: ast.AST) -> List[ast.ClassDef]:
        """获取所有类定义"""
        return [n for n in ast.walk(树) if isinstance(n, ast.ClassDef)]
    
    @staticmethod
    def 获取所有调用(树: ast.AST, 函数名: str = None) -> List[ast.Call]:
        """获取所有函数调用"""
        调用列表 = [n for n in ast.walk(树) if isinstance(n, ast.Call)]
        if 函数名:
            return [c for c in 调用列表 if getattr(c.func, 'id', None) == 函数名]
        return 调用列表
    
    @staticmethod
    def 获取所有导入(树: ast.AST) -> List:
        """获取所有导入语句"""
        return [n for n in ast.walk(树) if isinstance(n, (ast.Import, ast.ImportFrom))]


class AST访问者(ast.NodeVisitor):
    """AST访问者基类"""
    
    def __init__(self):
        self.节点统计: Dict[str, int] = {}
    
    def 访问(self, 节点: ast.AST):
        """访问节点"""
        类型名 = type(节点).__name__
        self.节点统计[类型名] = self.节点统计.get(类型名, 0) + 1
        self.generic_visit(节点)
    
    def 统计信息(self) -> Dict[str, int]:
        """获取统计信息"""
        return self.节点统计


class AST转换器(ast.NodeTransformer):
    """AST转换器基类"""
    
    def __init__(self):
        self.修改计数 = 0
    
    def 替换函数名(self, 树: ast.AST, 旧名称: str, 新名称: str) -> ast.AST:
        """替换函数名"""
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.FunctionDef) and 节点.name == 旧名称:
                节点.name = 新名称
                self.修改计数 += 1
            if isinstance(节点, ast.Call) and getattr(节点.func, 'id', None) == 旧名称:
                节点.func.id = 新名称
                self.修改计数 += 1
        return 树
    
    def 插入函数开头(self, 函数节点: ast.FunctionDef, 语句: ast.stmt) -> ast.FunctionDef:
        """在函数开头插入语句"""
        函数节点.body.insert(0, 语句)
        self.修改计数 += 1
        return 函数节点
    
    def 添加日志语句(self, 树: ast.AST, 函数名: str = None) -> ast.AST:
        """为函数添加日志语句"""
        打印语句 = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='print', ctx=ast.Load()),
                args=[ast.Constant(value=f'进入函数: {函数名}')],
                keywords=[]
            )
        )
        
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.FunctionDef):
                if 函数名 is None or 节点.name == 函数名:
                    self.插入函数开头(节点, ast.parse(
                        f'print("进入函数: {节点.name}")'
                    ).body[0])
        return 树
    
    def 添加装饰器(self, 函数节点: ast.FunctionDef, 装饰器名: str) -> ast.FunctionDef:
        """为函数添加装饰器"""
        装饰器 = ast.Name(id=装饰器名, ctx=ast.Load())
        函数节点.decorator_list.append(装饰器)
        self.修改计数 += 1
        return 函数节点
    
    def 重命名变量(self, 树: ast.AST, 旧名称: str, 新名称: str) -> ast.AST:
        """重命名变量"""
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.Name) and 节点.id == 旧名称:
                节点.id = 新名称
                self.修改计数 += 1
        return 树


class 代码生成器:
    """代码生成器"""
    
    @staticmethod
    def 生成函数(函数名: str, 参数列表: List[str] = None, 函数体: str = 'pass', 
                   返回类型: str = None) -> str:
        """生成函数定义代码"""
        参数 = ', '.join(参数列表) if 参数列表 else ''
        返回注解 = f' -> {返回类型}' if 返回类型 else ''
        
        函数体缩进 = '\n    '.join(函数体.strip().split('\n'))
        
        return f'''def {函数名}({参数}){返回注解}:
    {函数体缩进}
'''
    
    @staticmethod
    def 生成类(类名: str, 父类列表: List[str] = None, 属性字典: Dict[str, Any] = None,
                  方法字典: Dict[str, str] = None) -> str:
        """生成类定义代码"""
        父类 = ', '.join(父类列表) if 父类列表 else ''
        类头部 = f'class {类名}({父类}):' if 父类 else f'class {类名}:'
        
        类体 = []
        
        if 属性字典:
            for 属性名, 属性值 in 属性字典.items():
                类体.append(f'    {属性名} = {repr(属性值)}')
        
        if 方法字典:
            for 方法名, 方法体 in 方法字典.items():
                缩进方法体 = '\n    '.join(方法体.strip().split('\n'))
                类体.append(f'    def {方法名}(self):\n        {缩进方法体}')
        
        if not 类体:
            类体.append('    pass')
        
        return 类头部 + '\n' + '\n'.join(类体) + '\n'
    
    @staticmethod
    def 生成GetterSetter(属性名: str, 类型名: str = None) -> str:
        """生成getter和setter方法"""
        类型注解 = f': {类型名}' if 类型名 else ''
        
        return f'''    @property
    def {属性名}(self){类型注解}:
        return self._{属性名}
    
    @{属性名}.setter
    def {属性名}(self, 值{类型注解}):
        self._{属性名} = 值
'''
    
    @staticmethod
    def 生成单例(类名: str) -> str:
        """生成单例模式类"""
        return f'''class {类名}:
    _实例 = None
    
    def __new__(cls):
        if cls._实例 is None:
            cls._实例 = super().__new__(cls)
        return cls._实例
'''


class 代码分析器:
    """代码分析器"""
    
    def __init__(self, 代码: str = None, 文件路径: str = None):
        if 代码:
            self.AST = AST工具.解析代码(代码)
        elif 文件路径:
            self.AST = AST工具.解析文件(文件路径)
        else:
            raise ValueError('必须提供代码或文件路径')
    
    def 函数数量(self) -> int:
        """统计函数数量"""
        return len(AST工具.获取所有函数(self.AST))
    
    def 类数量(self) -> int:
        """统计类数量"""
        return len(AST工具.获取所有类(self.AST))
    
    def 行数量(self, 代码: str) -> int:
        """统计行数"""
        return len(代码.strip().split('\n'))
    
    def 获取复杂度(self) -> int:
        """计算圈复杂度"""
        复杂度 = 0
        for 节点 in ast.walk(self.AST):
            if isinstance(节点, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                复杂度 += 1
            elif isinstance(节点, ast.BoolOp):
                复杂度 += len(节点.values) - 1
            elif isinstance(节点, ast.Compare):
                复杂度 += len(节点.ops) - 1
        return 复杂度 + 1
    
    def 获取导入列表(self) -> List[str]:
        """获取导入列表"""
        导入列表 = []
        for 节点 in AST工具.获取所有导入(self.AST):
            if isinstance(节点, ast.Import):
                for 别名 in 节点.names:
                    导入列表.append(别名.name)
            elif isinstance(节点, ast.ImportFrom):
                for 别名 in 节点.names:
                    导入列表.append(f'{节点.module}.{别名.name}')
        return 导入列表
    
    def 生成报告(self) -> Dict[str, Any]:
        """生成代码分析报告"""
        return {
            '函数数量': self.函数数量(),
            '类数量': self.类数量(),
            '圈复杂度': self.获取复杂度(),
            '导入列表': self.获取导入列表(),
        }


class 装饰器生成器:
    """装饰器生成器"""
    
    @staticmethod
    def 生成计时装饰器() -> str:
        """生成计时装饰器"""
        return '''import time

def 计时装饰器(函数):
    def 包装(*参数, **关键字参数):
        开始时间 = time.time()
        结果 = 函数(*参数, **关键字参数)
        耗时 = time.time() - 开始时间
        print(f"函数 {函数.__name__} 执行耗时: {耗时:.6f}秒")
        return 结果
    return 包装
'''
    
    @staticmethod
    def 生成缓存装饰器() -> str:
        """生成缓存装饰器"""
        return '''def 缓存装饰器(函数):
    缓存字典 = {}
    def 包装(*参数):
        if 参数 in 缓存字典:
            return 缓存字典[参数]
        结果 = 函数(*参数)
        缓存字典[参数] = 结果
        return 结果
    return 包装
'''
    
    @staticmethod
    def 生成日志装饰器() -> str:
        """生成日志装饰器"""
        return '''import logging

def 日志装饰器(函数):
    def 包装(*参数, **关键字参数):
        logging.info(f"调用函数: {函数.__name__}")
        结果 = 函数(*参数, **关键字参数)
        logging.info(f"函数 {函数.__name__} 执行完成")
        return 结果
    return 包装
'''


class 模式匹配器:
    """AST模式匹配器"""
    
    @staticmethod
    def 查找模式(树: ast.AST, 模式函数: Callable[[ast.AST], bool]) -> List[ast.AST]:
        """查找匹配模式的节点"""
        return [节点 for 节点 in ast.walk(树) if 模式函数(节点)]
    
    @staticmethod
    def 查找空函数(树: ast.AST) -> List[ast.FunctionDef]:
        """查找空函数"""
        def 是空函数(节点):
            if not isinstance(节点, ast.FunctionDef):
                return False
            if len(节点.body) == 0:
                return True
            if len(节点.body) == 1 and isinstance(节点.body[0], ast.Pass):
                return True
            return False
        
        return 模式匹配器.查找模式(树, 是空函数)
    
    @staticmethod
    def 查找未使用变量(树: ast.AST) -> List[str]:
        """查找未使用的变量（简化版）"""
        赋值变量 = set()
        使用变量 = set()
        
        for 节点 in ast.walk(树):
            if isinstance(节点, ast.Assign):
                for 目标 in 节点.targets:
                    if isinstance(目标, ast.Name):
                        赋值变量.add(目标.id)
            elif isinstance(节点, ast.Name) and isinstance(节点.ctx, ast.Load):
                使用变量.add(节点.id)
        
        return list(赋值变量 - 使用变量)
    
    @staticmethod
    def 查找魔法数字(树: ast.AST) -> List[ast.Constant]:
        """查找魔法数字"""
        def 是魔法数字(节点):
            if not isinstance(节点, ast.Constant):
                return False
            if not isinstance(节点.value, (int, float)):
                return False
            if 节点.value in (0, 1, -1):
                return False
            return True
        
        return 模式匹配器.查找模式(树, 是魔法数字)


# 便捷函数
def 解析代码(代码: str) -> ast.Module:
    """解析代码"""
    return AST工具.解析代码(代码)


def 生成代码(树: ast.AST) -> str:
    """生成代码"""
    return AST工具.生成代码(树)


def 美化AST(树: ast.AST) -> str:
    """美化AST输出"""
    return AST工具.美化输出(树)


def 分析代码(代码: str) -> Dict[str, Any]:
    """分析代码"""
    分析器 = 代码分析器(代码)
    return 分析器.生成报告()


def 生成函数(函数名: str, 参数列表: List[str] = None, 函数体: str = 'pass') -> str:
    """生成函数代码"""
    return 代码生成器.生成函数(函数名, 参数列表, 函数体)


def 生成类(类名: str, 父类列表: List[str] = None, 属性字典: Dict[str, Any] = None,
            方法字典: Dict[str, str] = None) -> str:
    """生成类代码"""
    return 代码生成器.生成类(类名, 父类列表, 属性字典, 方法字典)


def 重写代码(代码: str, 转换函数: Callable[[ast.AST], ast.AST]) -> str:
    """重写代码"""
    树 = AST工具.解析代码(代码)
    转换后的树 = 转换函数(树)
    ast.fix_missing_locations(转换后的树)
    return AST工具.生成代码(转换后的树)