"""
段言（Duan）编程语言 - 语义分析器

实现：
- 类型检查（利用类型注解）
- 作用域分析
- 类型兼容性检查
"""

from typing import Dict, List, Set, Optional, Any
from duan_parser_v3 import *
from keywords import VERB_ARITY, VERB_MODE


# 需要导入新的AST节点类型
from duan_parser_v3 import IndexAccess, BreakStmt, ContinueStmt, ExportStmt, ImportStmt


# =============================================================================
# 类型兼容性映射
# =============================================================================

TYPE_COMPATIBILITY = {
    # (注解类型, 表达式类型) → 是否兼容
    '数': {'数', '整数', '浮点'},
    '串': {'串', '字符串'},
    '布尔': {'布尔'},
    '列表': {'列表', '列表[]'},
    '字典': {'字典'},
    '空': {'空', 'None'},
}


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
    """段言语义分析器（增强版：支持类型注解检查）"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        
        # 内置类型
        self.builtin_types = {'数', '串', '列表', '字典', '布尔', '空', '整数', '浮点', '字符串'}
        
        # 当前段落返回类型（用于返回语句检查）
        self._current_return_type: Optional[str] = None
        self._current_paragraph_name: Optional[str] = None
        
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
    
    def _is_type_compatible(self, annotated_type: str, actual_type: str) -> bool:
        """检查类型是否兼容"""
        if not annotated_type or not actual_type:
            return True  # 未知类型总是兼容
        if actual_type == '未知':
            return True  # 无法推断的类型视为兼容
        if annotated_type == actual_type:
            return True
        # 检查兼容性映射
        compatible_set = TYPE_COMPATIBILITY.get(annotated_type, set())
        if actual_type in compatible_set:
            return True
        # 数字兼容性（整数和浮点互相兼容）
        if annotated_type in ('数', '整数', '浮点') and actual_type in ('数', '整数', '浮点'):
            return True
        return False
    
    def _check_type_compatible(self, annotated_type: str, actual_type: str, context: str = ""):
        """检查类型兼容性，不兼容时添加错误"""
        if not self._is_type_compatible(annotated_type, actual_type):
            msg = f"类型不匹配"
            if context:
                msg += f" {context}"
            msg += f": 期望 '{annotated_type}'，实际为 '{actual_type}'"
            self.errors.append(SemanticError(msg))
    
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
            pass
        elif isinstance(stmt, ContinueStmt):
            pass
        elif isinstance(stmt, ExportStmt):
            pass
        elif isinstance(stmt, ImportStmt):
            pass
        elif isinstance(stmt, ParagraphCall):
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
        
        # 类型注解优先（如果存在）
        data_type = stmt.type_annotation or expr_type
        
        # 如果类型注解存在，检查类型兼容性
        if stmt.type_annotation and expr_type != '未知':
            self._check_type_compatible(
                stmt.type_annotation, expr_type,
                f"变量 '{stmt.name}' 赋值"
            )
        
        # 定义变量
        self.symbol_table.define(stmt.name, 'variable', data_type)
    
    def _analyze_if_stmt(self, stmt: IfStmt):
        """分析条件语句"""
        cond_type = self._analyze_expr(stmt.condition)
        
        self.symbol_table.enter_scope()
        for s in stmt.then_body:
            self._analyze_statement(s)
        self.symbol_table.exit_scope()
        
        if stmt.else_body:
            self.symbol_table.enter_scope()
            for s in stmt.else_body:
                self._analyze_statement(s)
            self.symbol_table.exit_scope()
    
    def _analyze_foreach_stmt(self, stmt: ForeachStmt):
        """分析遍历循环"""
        iter_type = self._analyze_expr(stmt.iterable)
        
        self.symbol_table.enter_scope()
        self.symbol_table.define(stmt.variable, 'variable', '元素')
        
        for s in stmt.body:
            self._analyze_statement(s)
        
        self.symbol_table.exit_scope()
    
    def _analyze_while_stmt(self, stmt: WhileStmt):
        """分析当循环"""
        cond_type = self._analyze_expr(stmt.condition)
        
        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._analyze_statement(s)
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
        
        # 记录当前段落返回类型
        old_return_type = self._current_return_type
        old_paragraph_name = self._current_paragraph_name
        self._current_return_type = stmt.return_type
        self._current_paragraph_name = stmt.name
        
        # 进入段落作用域
        self.symbol_table.enter_scope()
        
        # 定义参数（带类型信息）
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
        
        # 恢复返回类型
        self._current_return_type = old_return_type
        self._current_paragraph_name = old_paragraph_name
    
    def _analyze_return_stmt(self, stmt: ReturnStmt):
        """分析返回语句"""
        if stmt.value:
            return_type = self._analyze_expr(stmt.value)
            
            # 检查返回类型是否与段落声明匹配
            if self._current_return_type and return_type != '未知':
                self._check_type_compatible(
                    self._current_return_type, return_type,
                    f"段落 '{self._current_paragraph_name}' 的返回语句"
                )
    
    def _analyze_expr(self, expr: ASTNode) -> str:
        """分析表达式，返回类型"""
        if isinstance(expr, NumberLiteral):
            return '数'
        
        elif isinstance(expr, StringLiteral):
            return '串'
        
        elif isinstance(expr, Identifier):
            symbol = self.symbol_table.lookup(expr.name)
            if not symbol:
                # 内置值：True, False, None
                if expr.name in ('True', 'False', 'None'):
                    return '布尔' if expr.name in ('True', 'False') else '空'
                return '未知'
            return symbol.data_type or '未知'
        
        elif isinstance(expr, BinaryOp):
            left_type = self._analyze_expr(expr.left)
            right_type = self._analyze_expr(expr.right)
            
            # 算术运算
            if expr.operator in ('加', '减', '乘', '除', '模', '幂',
                                  '+', '-', '*', '/', '%', '**'):
                return '数'
            
            # 比较运算
            elif expr.operator in ('大于', '小于', '等于', '不等于', 
                                    '大于等于', '小于等于',
                                    '>', '<', '==', '!=', '>=', '<='):
                return '布尔'
            
            elif expr.operator in ('且', '与', '或', 'and', 'or'):
                return '布尔'
            
            return '数'
        
        elif isinstance(expr, ParagraphCall):
            # 检查段落是否已定义
            symbol = self.symbol_table.lookup(expr.name)
            if not symbol:
                if expr.name in self.builtin_functions:
                    return '未知'
                self.errors.append(SemanticError(
                    f"段落 '{expr.name}' 未定义", expr
                ))
            
            # 分析参数
            arg_types = []
            for arg in expr.args:
                arg_type = self._analyze_expr(arg)
                arg_types.append(arg_type)
            
            return '未知'
        
        elif isinstance(expr, Pipeline):
            for stage in expr.stages:
                self._analyze_expr(stage)
            return '未知'
        
        elif isinstance(expr, IndexAccess):
            obj_type = self._analyze_expr(expr.obj)
            index_type = self._analyze_expr(expr.index)
            return '元素'
        
        elif isinstance(expr, ConditionalExpression):
            self._analyze_expr(expr.condition)
            then_type = self._analyze_expr(expr.then_expr)
            if expr.else_expr:
                self._analyze_expr(expr.else_expr)
            return then_type
        
        elif isinstance(expr, ListLiteral):
            for elem in expr.elements:
                self._analyze_expr(elem)
            return '列表'
        
        elif isinstance(expr, DictLiteral):
            for entry in expr.entries:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    self._analyze_expr(entry[0])
                    self._analyze_expr(entry[1])
            return '字典'
        
        else:
            return '未知'


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    from duan_parser_v3 import DuanParser
    
    print("=" * 60)
    print("段言语义分析器测试（增强版）")
    print("=" * 60)
    
    # 测试类型注解
    test_cases = [
        ("变量类型注解", '''
设 甲: 数 = 三。
设 乙: 串 = "你好"。
设 丙 = 五。
'''),
        ("段落类型注解", '''
段落 加法 接收 甲: 数, 乙: 数 返回 数:
  返回 甲 加 乙。
结束。
'''),
        ("类型不匹配", '''
设 甲: 数 = "这不是数字"。
'''),
    ]
    
    for name, code in test_cases:
        print(f"\n--- {name} ---")
        print(f"代码: {code.strip()[:50]}...")
        
        parser = DuanParser()
        try:
            module = parser.parse(code)
            analyzer = SemanticAnalyzer()
            success = analyzer.analyze(module)
            
            if analyzer.errors:
                print(f"[类型错误]")
                for err in analyzer.errors:
                    print(f"  - {err.message}")
            else:
                print(f"[OK] 语义分析通过")
                
            print("\n符号表:")
            for scope in analyzer.symbol_table.scopes:
                for name, symbol in scope.items():
                    print(f"  {name}: {symbol.symbol_type} (类型: {symbol.data_type})")
                    
        except Exception as e:
            print(f"[解析错误] {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)