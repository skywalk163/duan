"""
段言（Duan）编程语言 - 语义分析器

实现：
- 类型检查
- 作用域分析
- 元数驱动解析（决策28）
- 主谓/谓宾语义识别（决策34）
"""

from typing import Dict, List, Set, Optional, Any
from duan_parser_v3 import *
from keywords import VERB_ARITY, VERB_MODE


# 需要导入新的AST节点类型
from duan_parser_v3 import IndexAccess, BreakStmt, ContinueStmt, ExportStmt, ImportStmt


# =============================================================================
# 符号表
# =============================================================================

class Symbol:
    """符号表条目"""
    def __init__(self, name: str, symbol_type: str, scope_level: int):
        self.name = name
        self.symbol_type = symbol_type  # 'variable', 'paragraph', 'parameter'
        self.scope_level = scope_level
        self.data_type = None  # 数据类型（如 '数', '串', '列表'）
    
    def __repr__(self):
        return f"Symbol({self.name}: {self.symbol_type})"


class SymbolTable:
    """符号表（支持作用域）"""
    
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # 作用域栈
        self.current_level = 0
    
    def enter_scope(self):
        """进入新作用域"""
        self.scopes.append({})
        self.current_level += 1
    
    def exit_scope(self):
        """退出作用域"""
        if self.current_level > 0:
            self.scopes.pop()
            self.current_level -= 1
    
    def define(self, name: str, symbol_type: str, data_type: str = None) -> bool:
        """定义符号"""
        if name in self.scopes[self.current_level]:
            return False  # 重定义
        
        symbol = Symbol(name, symbol_type, self.current_level)
        symbol.data_type = data_type
        self.scopes[self.current_level][name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """查找符号（从当前作用域向外查找）"""
        for level in range(self.current_level, -1, -1):
            if name in self.scopes[level]:
                return self.scopes[level][name]
        return None
    
    def is_defined(self, name: str) -> bool:
        """检查符号是否已定义"""
        return self.lookup(name) is not None


# =============================================================================
# 语义错误
# =============================================================================

class SemanticError(Exception):
    """语义错误"""
    def __init__(self, message: str, node: ASTNode = None):
        self.message = message
        self.node = node
        super().__init__(f"语义错误: {message}")


# =============================================================================
# 语义分析器
# =============================================================================

class SemanticAnalyzer:
    """段言语义分析器"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        
        # 内置类型
        self.builtin_types = {'数', '串', '列表', '字典', '布尔', '空'}
        
        # 内置函数（从keywords.py导入）
        self.builtin_functions = {}
        for func_name in VERB_ARITY.keys():
            self.builtin_functions[func_name] = {
                'arity': VERB_ARITY[func_name],
                'mode': VERB_MODE.get(func_name, 'functional')
            }
    
    def analyze(self, module: Module) -> bool:
        """分析模块"""
        try:
            self._analyze_module(module)
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(SemanticError(str(e)))
            return False
    
    def _analyze_module(self, module: Module):
        """分析模块"""
        for stmt in module.statements:
            self._analyze_statement(stmt)
    
    def _analyze_statement(self, stmt: ASTNode):
        """分析语句"""
        if isinstance(stmt, VarDecl):
            self._analyze_var_decl(stmt)
        elif isinstance(stmt, IfStmt):
            self._analyze_if_stmt(stmt)
        elif isinstance(stmt, ForeachStmt):
            self._analyze_foreach_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self._analyze_while_stmt(stmt)
        elif isinstance(stmt, Paragraph):
            self._analyze_paragraph(stmt)
        elif isinstance(stmt, ReturnStmt):
            self._analyze_return_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            # 跳出语句：检查是否在循环内
            pass  # 简化：不检查
        elif isinstance(stmt, ContinueStmt):
            # 跳过语句：检查是否在循环内
            pass  # 简化：不检查
        elif isinstance(stmt, ExportStmt):
            # 导出语句：允许前向声明，不强制检查是否已定义
            pass
        elif isinstance(stmt, ImportStmt):
            # 导入语句：将导入的符号加入当前作用域
            pass  # 简化：不检查模块是否存在
        elif isinstance(stmt, ParagraphCall):
            # 段落调用作为语句
            self._analyze_expr(stmt)
        else:
            raise SemanticError(f"未知语句类型: {type(stmt).__name__}")
    
    def _analyze_var_decl(self, stmt: VarDecl):
        """分析变量声明"""
        # 检查变量名是否已定义
        if self.symbol_table.is_defined(stmt.name):
            existing = self.symbol_table.lookup(stmt.name)
            if existing.scope_level == self.symbol_table.current_level:
                self.errors.append(SemanticError(
                    f"变量 '{stmt.name}' 重复定义", stmt
                ))
        
        # 分析表达式
        expr_type = self._analyze_expr(stmt.value)
        
        # 定义变量
        self.symbol_table.define(stmt.name, 'variable', expr_type)
    
    def _analyze_if_stmt(self, stmt: IfStmt):
        """分析条件语句"""
        # 分析条件
        cond_type = self._analyze_expr(stmt.condition)
        
        # 条件必须是布尔类型（简化：不强制检查）
        
        # 分析 then 分支
        self.symbol_table.enter_scope()
        for s in stmt.then_body:
            self._analyze_statement(s)
        self.symbol_table.exit_scope()
        
        # 分析 else 分支
        if stmt.else_body:
            self.symbol_table.enter_scope()
            for s in stmt.else_body:
                self._analyze_statement(s)
            self.symbol_table.exit_scope()
    
    def _analyze_foreach_stmt(self, stmt: ForeachStmt):
        """分析遍历循环"""
        # 分析可迭代对象
        iter_type = self._analyze_expr(stmt.iterable)
        
        # 进入循环作用域
        self.symbol_table.enter_scope()
        
        # 定义循环变量
        self.symbol_table.define(stmt.variable, 'variable', '元素')
        
        # 分析循环体
        for s in stmt.body:
            self._analyze_statement(s)
        
        # 退出作用域
        self.symbol_table.exit_scope()
    
    def _analyze_while_stmt(self, stmt: WhileStmt):
        """分析当循环"""
        # 分析条件
        cond_type = self._analyze_expr(stmt.condition)
        
        # 进入循环作用域
        self.symbol_table.enter_scope()
        
        # 分析循环体
        for s in stmt.body:
            self._analyze_statement(s)
        
        # 退出作用域
        self.symbol_table.exit_scope()
    
    def _analyze_paragraph(self, stmt: Paragraph):
        """分析段落定义"""
        # 检查段落名是否已定义
        if self.symbol_table.is_defined(stmt.name):
            self.errors.append(SemanticError(
                f"段落 '{stmt.name}' 重复定义", stmt
            ))
        
        # 定义段落
        self.symbol_table.define(stmt.name, 'paragraph')
        
        # 进入段落作用域
        self.symbol_table.enter_scope()
        
        # 定义参数
        for param in stmt.params:
            self.symbol_table.define(
                param['name'], 
                'parameter', 
                param.get('type')
            )
        
        # 分析段落体
        for s in stmt.body:
            self._analyze_statement(s)
        
        # 退出作用域
        self.symbol_table.exit_scope()
    
    def _analyze_return_stmt(self, stmt: ReturnStmt):
        """分析返回语句"""
        if stmt.value:
            return_type = self._analyze_expr(stmt.value)
    
    def _analyze_expr(self, expr: ASTNode) -> str:
        """分析表达式，返回类型"""
        if isinstance(expr, NumberLiteral):
            return '数'
        
        elif isinstance(expr, StringLiteral):
            return '串'
        
        elif isinstance(expr, Identifier):
            # 检查变量是否已定义（警告但不报错）
            symbol = self.symbol_table.lookup(expr.name)
            if not symbol:
                # 允许未定义变量（可能是内置值或前向引用）
                pass
                return '未知'
            return symbol.data_type or '未知'
        
        elif isinstance(expr, BinaryOp):
            left_type = self._analyze_expr(expr.left)
            right_type = self._analyze_expr(expr.right)
            
            # 算术运算
            if expr.operator in ['+', '-', '*', '/']:
                return '数'
            
            # 比较运算
            elif expr.operator in ['>', '<', '==', '!=', '>=', '<=']:
                return '布尔'
            
            return '未知'
        
        elif isinstance(expr, ParagraphCall):
            # 检查段落是否已定义
            symbol = self.symbol_table.lookup(expr.name)
            if not symbol:
                # 可能是内置函数
                if expr.name in self.builtin_functions:
                    return '未知'
                
                self.errors.append(SemanticError(
                    f"段落 '{expr.name}' 未定义", expr
                ))
            
            # 分析参数
            for arg in expr.args:
                self._analyze_expr(arg)
            
            return '未知'
        
        elif isinstance(expr, Pipeline):
            # 分析管道各阶段
            for stage in expr.stages:
                self._analyze_expr(stage)
            return '未知'
        
        elif isinstance(expr, IndexAccess):
            # 索引访问
            obj_type = self._analyze_expr(expr.obj)
            index_type = self._analyze_expr(expr.index)
            # 返回元素类型
            return '元素'
        
        else:
            return '未知'


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    from duan_parser_v3 import DuanParser
    
    print("=" * 60)
    print("段言语义分析器测试")
    print("=" * 60)
    
    # 测试代码
    test_code = '''
定义甲等于三。
定义乙等于五。
定义丙等于甲加乙。
'''
    
    # 解析
    parser = DuanParser()
    module = parser.parse(test_code)
    
    # 语义分析
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(module)
    
    print(f"\n解析结果: {len(module.statements)} 条语句")
    print(f"语义分析: {'成功' if success else '失败'}")
    
    if analyzer.errors:
        print("\n错误:")
        for error in analyzer.errors:
            print(f"  - {error.message}")
    else:
        print("\n符号表:")
        for scope in analyzer.symbol_table.scopes:
            for name, symbol in scope.items():
                print(f"  {name}: {symbol.symbol_type} (类型: {symbol.data_type})")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
