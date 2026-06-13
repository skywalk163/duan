"""
段言（Duan）编程语言 - 类型推断器

实现基于AST的类型推断，支持：
- 基本类型推断（数字、字符串、布尔、空值）
- 变量类型追踪
- 二元运算类型推断（特别是加法/连接操作）
- 函数调用类型推断
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import sys
import os

# 优先尝试导入ANTLR生成的AST（用于编译流程）
try:
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(_current_dir, '..', 'antlrparser'))
    from duan_ast import *
    _USE_DUAN_AST = True
except ImportError:
    # 回退到统一AST（用于测试）
    from ast_unified import *
    _USE_DUAN_AST = False


# =============================================================================
# 类型系统定义
# =============================================================================

class Type:
    """类型基类"""
    pass


class NumberType(Type):
    """数字类型"""
    def __repr__(self):
        return "数"


class StringType(Type):
    """字符串类型"""
    def __repr__(self):
        return "串"


class BooleanType(Type):
    """布尔类型"""
    def __repr__(self):
        return "布尔"


class NullType(Type):
    """空值类型"""
    def __repr__(self):
        return "空"


class ListType(Type):
    """列表类型"""
    def __init__(self, element_type: Optional['Type'] = None):
        self.element_type = element_type
    
    def __repr__(self):
        return f"列表[{self.element_type}]" if self.element_type else "列表"


class DictType(Type):
    """字典类型"""
    def __init__(self, key_type: Optional['Type'] = None, value_type: Optional['Type'] = None):
        self.key_type = key_type
        self.value_type = value_type
    
    def __repr__(self):
        return f"字典[{self.key_type}: {self.value_type}]" if self.key_type else "字典"


class ClassType(Type):
    """类类型"""
    def __init__(self, class_name: str):
        self.class_name = class_name
    
    def __repr__(self):
        return self.class_name


class UnknownType(Type):
    """未知类型"""
    def __repr__(self):
        return "未知"


# 类型常量
TYPE_NUMBER = NumberType()
TYPE_STRING = StringType()
TYPE_BOOLEAN = BooleanType()
TYPE_NULL = NullType()
TYPE_UNKNOWN = UnknownType()


# =============================================================================
# 符号表（带类型信息）
# =============================================================================

@dataclass
class TypedSymbol:
    """带类型信息的符号"""
    name: str
    symbol_type: str  # 'variable', 'function', 'class', 'parameter'
    data_type: Type
    scope_level: int


class TypeSymbolTable:
    """带类型信息的符号表"""
    
    def __init__(self):
        self.scopes: List[Dict[str, TypedSymbol]] = [{}]
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
    
    def define(self, name: str, symbol_type: str, data_type: Type) -> bool:
        """定义符号"""
        if name in self.scopes[self.current_level]:
            return False
        
        symbol = TypedSymbol(name, symbol_type, data_type, self.current_level)
        self.scopes[self.current_level][name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[TypedSymbol]:
        """查找符号"""
        for level in range(self.current_level, -1, -1):
            if name in self.scopes[level]:
                return self.scopes[level][name]
        return None
    
    def update_type(self, name: str, data_type: Type):
        """更新符号类型"""
        symbol = self.lookup(name)
        if symbol:
            symbol.data_type = data_type


# =============================================================================
# 类型推断器
# =============================================================================

class TypeInferencer:
    """段言类型推断器"""
    
    def __init__(self):
        self.symbol_table = TypeSymbolTable()
        self.type_cache: Dict[int, Type] = {}  # AST节点ID → 类型
    
    def infer(self, module: Module) -> Dict[int, Type]:
        """对整个模块进行类型推断"""
        self.type_cache = {}
        self.symbol_table = TypeSymbolTable()
        
        # 先处理类和函数定义（建立符号表）
        self._scan_definitions(module)
        
        # 再处理语句
        self._infer_module(module)
        
        return self.type_cache
    
    def _scan_definitions(self, module: Module):
        """扫描定义（建立符号表）"""
        # 处理类定义
        if hasattr(module, 'classes'):
            for cls in module.classes:
                self.symbol_table.define(cls.name, 'class', ClassType(cls.name))
        
        # 处理段落定义
        if hasattr(module, 'segments'):
            for segment in module.segments:
                self.symbol_table.define(segment.name, 'function', TYPE_UNKNOWN)
    
    def _infer_module(self, module: Module):
        """推断模块"""
        # 处理类定义（推断方法类型）
        if hasattr(module, 'classes'):
            for cls in module.classes:
                self._infer_class(cls)
        
        # 处理段落定义
        if hasattr(module, 'segments'):
            for segment in module.segments:
                self._infer_segment(segment)
        
        # 处理语句
        if hasattr(module, 'statements'):
            for stmt in module.statements:
                self._infer_statement(stmt)
    
    def _infer_class(self, cls: ClassDefinition):
        """推断类"""
        self.symbol_table.enter_scope()
        
        # 处理构造函数
        if cls.constructor:
            self._infer_constructor(cls.constructor)
        
        # 处理方法
        for method in cls.methods:
            self._infer_method(method)
        
        self.symbol_table.exit_scope()
    
    def _infer_constructor(self, constructor: ConstructorDefinition):
        """推断构造函数"""
        self.symbol_table.enter_scope()
        
        # 定义参数
        for param in constructor.parameters:
            self.symbol_table.define(param.name, 'parameter', TYPE_UNKNOWN)
        
        # 推断构造函数体
        for stmt in constructor.body:
            self._infer_statement(stmt)
        
        self.symbol_table.exit_scope()
    
    def _infer_method(self, method: MethodDefinition):
        """推断方法"""
        self.symbol_table.enter_scope()
        
        # 定义参数
        for param in method.parameters:
            self.symbol_table.define(param.name, 'parameter', TYPE_UNKNOWN)
        
        # 推断方法体
        for stmt in method.body:
            self._infer_statement(stmt)
        
        self.symbol_table.exit_scope()
    
    def _infer_segment(self, segment: SegmentDefinition):
        """推断段落（函数）"""
        self.symbol_table.enter_scope()
        
        # 定义参数
        for param in segment.parameters:
            self.symbol_table.define(param.name, 'parameter', TYPE_UNKNOWN)
        
        # 推断段落体
        for stmt in segment.body:
            self._infer_statement(stmt)
        
        self.symbol_table.exit_scope()
    
    def _infer_statement(self, stmt: ASTNode):
        """推断语句类型"""
        if stmt is None:
            return
        
        node_type = type(stmt).__name__
        
        # 变量声明
        if is_instance(stmt, 'VariableDeclaration'):
            self._infer_var_decl(stmt)
        
        # 赋值语句
        elif is_instance(stmt, 'Assignment'):
            self._infer_assignment(stmt)
        
        # 条件语句
        elif is_instance(stmt, 'IfStatement'):
            self._infer_if_stmt(stmt)
        
        # 循环语句
        elif is_instance(stmt, 'ForeachStatement'):
            self._infer_foreach_stmt(stmt)
        
        elif is_instance(stmt, 'WhileStatement'):
            self._infer_while_stmt(stmt)
        
        # 返回语句
        elif is_instance(stmt, 'ReturnStatement'):
            self._infer_return_stmt(stmt)
        
        # 表达式语句
        elif is_instance(stmt, 'ExpressionStatement'):
            self._infer_expr(stmt.expression)
        
        # 打印语句
        elif is_instance(stmt, 'PrintStatement'):
            if hasattr(stmt, 'value'):
                self._infer_expr(stmt.value)
        
        # 函数调用作为语句
        elif is_instance(stmt, 'FunctionCall'):
            self._infer_expr(stmt)
    
    def _infer_var_decl(self, stmt):
        """推断变量声明"""
        expr_type = self._infer_expr(stmt.value)
        self.symbol_table.define(stmt.name, 'variable', expr_type)
        self.type_cache[id(stmt)] = expr_type
        self.type_cache[id(stmt.value)] = expr_type  # 同时缓存表达式类型
        #print(f"DEBUG: 定义变量 '{stmt.name}' 类型为 {expr_type}")
    
    def _infer_assignment(self, stmt):
        """推断赋值语句"""
        value_type = self._infer_expr(stmt.value)
        
        # 更新目标变量的类型
        if is_instance(stmt.target, 'Identifier'):
            self.symbol_table.update_type(stmt.target.name, value_type)
        elif is_instance(stmt.target, 'PropertyAccess'):
            self._infer_expr(stmt.target)
        
        self.type_cache[id(stmt)] = value_type
    
    def _infer_if_stmt(self, stmt):
        """推断条件语句"""
        self._infer_expr(stmt.condition)
        
        self.symbol_table.enter_scope()
        for s in stmt.then_body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
        
        if stmt.else_body:
            self.symbol_table.enter_scope()
            for s in stmt.else_body:
                self._infer_statement(s)
            self.symbol_table.exit_scope()
    
    def _infer_foreach_stmt(self, stmt):
        """推断遍历循环"""
        self._infer_expr(stmt.iterable)
        
        self.symbol_table.enter_scope()
        self.symbol_table.define(stmt.variable, 'variable', TYPE_UNKNOWN)
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
    
    def _infer_while_stmt(self, stmt):
        """推断当循环"""
        self._infer_expr(stmt.condition)
        
        self.symbol_table.enter_scope()
        for s in stmt.body:
            self._infer_statement(s)
        self.symbol_table.exit_scope()
    
    def _infer_return_stmt(self, stmt):
        """推断返回语句"""
        if stmt.value:
            return_type = self._infer_expr(stmt.value)
            self.type_cache[id(stmt)] = return_type
    
    def _infer_expr(self, expr: ASTNode) -> Type:
        """推断表达式类型"""
        if expr is None:
            return TYPE_NULL
        
        # 检查缓存
        if id(expr) in self.type_cache:
            cached_type = self.type_cache[id(expr)]
            #print(f"DEBUG: 缓存命中 id={id(expr)}, 类型={cached_type}")
            return cached_type
        
        node_type = type(expr).__name__
        result_type: Type
        
        # 字面量
        if is_instance(expr, 'NumberLiteral'):
            result_type = TYPE_NUMBER
        
        elif is_instance(expr, 'StringLiteral'):
            result_type = TYPE_STRING
        
        elif is_instance(expr, 'BooleanLiteral'):
            result_type = TYPE_BOOLEAN
        
        elif is_instance(expr, 'NullLiteral'):
            result_type = TYPE_NULL
        
        # 标识符
        elif is_instance(expr, 'Identifier'):
            symbol = self.symbol_table.lookup(expr.name)
            if symbol:
                result_type = symbol.data_type
            else:
                # 未定义的标识符，可能是内置函数或变量
                result_type = TYPE_UNKNOWN
        
        # 二元运算
        elif is_instance(expr, 'BinaryOp'):
            left_type = self._infer_expr(expr.left)
            right_type = self._infer_expr(expr.right)
            
            if expr.operator in ['+', '加']:
                # 加法/连接：如果任一操作数是字符串，则结果为字符串
                if isinstance(left_type, StringType) or isinstance(right_type, StringType):
                    result_type = TYPE_STRING
                else:
                    result_type = TYPE_NUMBER
            
            elif expr.operator in ['-', '减', '*', '乘', '/', '除']:
                result_type = TYPE_NUMBER
            
            elif expr.operator in ['>', '<', '>=', '<=', '==', '!=', '等于', '不等于', '大于', '小于', '大于等于', '小于等于']:
                result_type = TYPE_BOOLEAN
            
            else:
                result_type = TYPE_UNKNOWN
        
        # 一元运算
        elif is_instance(expr, 'UnaryOp'):
            operand_type = self._infer_expr(expr.operand)
            
            if expr.operator in ['-', 'not', '否']:
                if isinstance(operand_type, BooleanType):
                    result_type = TYPE_BOOLEAN
                else:
                    result_type = TYPE_NUMBER
            else:
                result_type = TYPE_UNKNOWN
        
        # 函数调用
        elif is_instance(expr, 'FunctionCall'):
            # 分析参数（确保参数表达式的类型被缓存）
            arg_types = []
            for i, arg in enumerate(expr.arguments):
                arg_type = self._infer_expr(arg)
                arg_types.append(arg_type)
                #print(f"DEBUG: 参数{i} id={id(arg)}, 类型={arg_type}")
            
            # 尝试推断返回类型
            func_name = None
            if is_instance(expr.name, 'Identifier'):
                func_name = expr.name.name
            elif hasattr(expr.name, 'name'):
                func_name = expr.name.name
            
            # 内置函数类型推断
            if func_name in ['打印', '显示']:
                result_type = TYPE_NULL
            elif func_name in ['长', '长度', '字符串长度', '列表长度']:
                result_type = TYPE_NUMBER
            elif func_name in ['转整数', '转为整数']:
                result_type = TYPE_NUMBER
            elif func_name in ['转浮点', '转为浮点']:
                result_type = TYPE_NUMBER
            elif func_name in ['转字符串', '转为字符串']:
                result_type = TYPE_STRING
            elif func_name in ['首', '末']:
                result_type = TYPE_UNKNOWN  # 取决于输入类型
            else:
                result_type = TYPE_UNKNOWN
        
        # 属性访问
        elif is_instance(expr, 'PropertyAccess'):
            obj_type = self._infer_expr(expr.obj)
            result_type = TYPE_UNKNOWN
        
        # 索引访问
        elif is_instance(expr, 'IndexAccess'):
            self._infer_expr(expr.obj)
            self._infer_expr(expr.index)
            result_type = TYPE_UNKNOWN  # 元素类型取决于容器
        
        # 列表字面量
        elif is_instance(expr, 'ListLiteral'):
            element_types = [self._infer_expr(e) for e in expr.elements]
            if element_types:
                # 如果所有元素类型相同，则推断为该类型的列表
                first_type = element_types[0]
                if all(t == first_type for t in element_types):
                    result_type = ListType(first_type)
                else:
                    result_type = ListType()
            else:
                result_type = ListType()
        
        # 字典字面量
        elif is_instance(expr, 'DictLiteral'):
            for entry in expr.entries:
                self._infer_expr(entry.key)
                self._infer_expr(entry.value)
            result_type = DictType()
        
        # 类实例化
        elif is_instance(expr, 'NewExpression'):
            for arg in expr.arguments:
                self._infer_expr(arg)
            result_type = ClassType(expr.class_name)
        
        # Self引用
        elif is_instance(expr, 'SelfReference'):
            result_type = TYPE_UNKNOWN  # 需要更多上下文
        
        else:
            result_type = TYPE_UNKNOWN
        
        # 缓存结果
        self.type_cache[id(expr)] = result_type
        return result_type


# =============================================================================
# 辅助函数
# =============================================================================

def is_instance(node, class_name):
    """检查节点类型"""
    if node is None:
        return False
    return type(node).__name__ == class_name


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("段言类型推断器测试")
    print("=" * 60)
    
    # 创建测试AST
    test_module = Module(
        statements=[
            VariableDeclaration(
                name='结果',
                value=BinaryOp(
                    left=NumberLiteral(value=3),
                    operator='+',
                    right=NumberLiteral(value=5)
                )
            ),
            ExpressionStatement(
                expression=BinaryOp(
                    left=StringLiteral(value='3 + 5 = '),
                    operator='+',
                    right=Identifier(name='结果')
                )
            )
        ]
    )
    
    # 类型推断
    inferencer = TypeInferencer()
    types = inferencer.infer(test_module)
    
    print("\n推断结果:")
    for node_id, node_type in types.items():
        print(f"  节点 {node_id}: {node_type}")
    
    # 测试表达式类型
    expr = test_module.statements[1].expression
    expr_type = inferencer._infer_expr(expr)
    print(f"\n表达式类型: {expr_type}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)