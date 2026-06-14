"""
段言（Duan）编程语言 ANTLR 访问器

将 ANTLR 解析树转换为段言 AST 节点
"""

import sys
import os
from typing import List, Optional, Union

# 添加当前目录到路径，以便导入生成的解析器
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parser_dir = os.path.join(_current_dir, 'duan_parser')
sys.path.insert(0, _parser_dir)

# ANTLR imports
from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorListener import ErrorListener

# 导入 ANTLR 生成的解析器（从 duan_parser 目录）
from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from DuanLangParserVisitor import DuanLangParserVisitor

# 导入 AST 节点
from duan_ast import (
    ASTNode, NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Identifier, SegmentName, ModuleName, BinaryOp, UnaryOp, FunctionCall,
    PipeExpression, PropertyAccess, IndexAccess, ListLiteral, DictLiteral, NewExpression,
    VariableDeclaration, Assignment, IfStatement, ForeachStatement,
    WhileStatement, BreakStatement, ContinueStatement, ReturnStatement,
    TryStatement, ThrowStatement, PrintStatement, ExpressionStatement,
    Parameter, SegmentDefinition, DataTypeField, DataTypeDefinition,
    ErrorTypeDefinition, ImportStatement, ExportStatement, Module,
    ClassDefinition, InterfaceDefinition, MethodDefinition, ConstructorDefinition,
    InterfaceMethod, InterfaceProperty, SelfReference,
)

# 导入自定义分词器
from duan_tokenizer import create_antlr_token_stream


# =============================================================================
# 自定义错误监听器
# =============================================================================

class DuanLangErrorListener(ErrorListener):
    """段言语法错误监听器"""

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        error_msg = f"行{line}, 列{column}: {msg}"
        self.errors.append(error_msg)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self) -> List[str]:
        return self.errors


# =============================================================================
# 访问器：ANTLR 解析树 → 段言 AST
# =============================================================================

class DuanLangASTBuilder(DuanLangParserVisitor):
    """将 ANTLR 解析树转换为段言 AST"""

    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []

    def _add_warning(self, message: str, line: int, column: int):
        """添加警告信息"""
        self.warnings.append(f"警告 [行{line}:{column}]: {message}")

    # ----- 程序 -----

    def visitProgram(self, ctx: DuanLangParser.ProgramContext):
        """程序入口"""
        module = Module(line=1, column=1)

        for child in ctx.getChildren():
            if isinstance(child, DuanLangParser.ModuleDeclContext):
                module.name = self.visitModuleDecl(child)
            elif isinstance(child, DuanLangParser.ImportStmtContext):
                module.imports.append(self.visitImportStmt(child))
            elif isinstance(child, DuanLangParser.ExportStmtContext):
                module.exports.append(self.visitExportStmt(child))
            elif isinstance(child, DuanLangParser.DefinitionContext):
                defn = self.visitDefinition(child)
                if isinstance(defn, SegmentDefinition):
                    module.segments.append(defn)
                elif isinstance(defn, ClassDefinition):
                    module.classes.append(defn)
                elif isinstance(defn, InterfaceDefinition):
                    module.interfaces.append(defn)
                elif isinstance(defn, DataTypeDefinition):
                    module.data_types.append(defn)
                elif isinstance(defn, ErrorTypeDefinition):
                    module.error_types.append(defn)
            elif isinstance(child, DuanLangParser.StmtContext):
                stmt = self.visitStmt(child)
                if stmt:
                    module.statements.append(stmt)

        return module

    def visitModuleDecl(self, ctx: DuanLangParser.ModuleDeclContext):
        """模块声明 【名称】"""
        return ctx.ID().getText()

    # ----- 段落定义 -----

    def visitParagraphDef(self, ctx: DuanLangParser.ParagraphDefContext):
        """段落定义"""
        # 新语法：段落 名称 接收 参数列表:
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column
        
        # 参数列表
        params = []
        if ctx.paramList():
            params = self.visitParamList(ctx.paramList())
        
        # 返回类型
        return_type = None
        if ctx.typeAnnotation():
            return_type = self.visitTypeAnnotation(ctx.typeAnnotation())
        
        # 段落体
        body = []
        if ctx.block():
            body = self.visitBlock(ctx.block())
        
        return SegmentDefinition(
            line=line, column=col,
            name=name,
            parameters=params,
            body=body,
            return_type=return_type,
            modifiers=[],
        )

    def visitClassDef(self, ctx: DuanLangParser.ClassDefContext):
        """类定义"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column
        
        # 提取泛型参数
        generic_params = []
        if ctx.genericParams():
            for id_ctx in ctx.genericParams().ID():
                generic_params.append(id_ctx.getText())

        superclasses = []
        interfaces = []
        
        # 处理继承和实现
        child_list = list(ctx.getChildren())
        inherit_found = False
        use_found = False
        
        for child in child_list:
            if hasattr(child, 'getText'):
                txt = child.getText()
                if txt == '继承':
                    inherit_found = True
                    use_found = False
                elif txt == '使用':
                    use_found = True
                    inherit_found = False
                elif inherit_found and isinstance(child, DuanLangParser.TypeAnnotationContext):
                    superclasses.append(self.visitTypeAnnotation(child))
                elif use_found and isinstance(child, DuanLangParser.TypeAnnotationContext):
                    interfaces.append(self.visitTypeAnnotation(child))

        fields = []
        methods = []
        constructor = None

        for member in ctx.classMember():
            if member.attributeDecl():
                # 属性声明：属性 名字。
                attr_ctx = member.attributeDecl()
                field_name = attr_ctx.ID().getText()
                field = DataTypeField(
                    name=field_name,
                    type_annotation=""
                )
                fields.append(field)
            elif member.methodDef():
                method = self.visitMethodDef(member.methodDef())
                # 如果方法名为"初始化"，则作为构造函数
                if method.name == '初始化':
                    constructor = ConstructorDefinition(
                        line=method.line,
                        column=method.column,
                        parameters=method.parameters,
                        body=method.body
                    )
                else:
                    methods.append(method)
            elif member.constructorDef():
                constructor = self.visitConstructorDef(member.constructorDef())

        return ClassDefinition(
            line=line, column=col,
            name=name,
            generic_params=generic_params,
            superclasses=superclasses,
            interfaces=interfaces,
            fields=fields,
            methods=methods,
            constructor=constructor,
        )

    def visitMethodDef(self, ctx: DuanLangParser.MethodDefContext):
        """方法定义"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column

        params = []
        if ctx.paramList():
            params = self.visitParamList(ctx.paramList())

        return_type = None
        if ctx.typeAnnotation():
            return_type = self.visitTypeAnnotation(ctx.typeAnnotation())

        body = []
        if ctx.block():
            body = self.visitBlock(ctx.block())

        return MethodDefinition(
            line=line, column=col,
            name=name,
            parameters=params,
            body=body,
            return_type=return_type,
            is_static=False,
        )

    def visitConstructorDef(self, ctx: DuanLangParser.ConstructorDefContext):
        """构造函数定义"""
        name = "构造"  # 构造函数名固定为"构造"
        line = ctx.start.line
        col = ctx.start.column

        params = []
        if ctx.paramList():
            params = self.visitParamList(ctx.paramList())

        body = []
        if ctx.block():
            body = self.visitBlock(ctx.block())

        return ConstructorDefinition(
            line=line, column=col,
            name=name,
            parameters=params,
            body=body,
        )

    def visitInterfaceDef(self, ctx: DuanLangParser.InterfaceDefContext):
        """接口定义"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column

        superinterfaces = []
        inherit_found = False
        
        for child in ctx.getChildren():
            if hasattr(child, 'getText') and child.getText() == '继承':
                inherit_found = True
            elif inherit_found and isinstance(child, DuanLangParser.TypeAnnotationContext):
                superinterfaces.append(self.visitTypeAnnotation(child))

        methods = []
        properties = []

        for member in ctx.interfaceMember():
            if member.methodSignature():
                ms = member.methodSignature()
                method_name = ms.ID().getText()
                params = []
                if ms.paramList():
                    params = self.visitParamList(ms.paramList())
                return_type = self.visitTypeAnnotation(ms.typeAnnotation())
                methods.append(InterfaceMethod(
                    line=ms.start.line, column=ms.start.column,
                    name=method_name,
                    parameters=params,
                    return_type=return_type,
                ))
            elif member.propertySignature():
                ps = member.propertySignature()
                prop_name = ps.ID().getText()
                prop_type = ps.typeAnnotation().getText()
                properties.append(InterfaceProperty(
                    line=ps.start.line, column=ps.start.column,
                    name=prop_name,
                    type_annotation=prop_type,
                ))

        return InterfaceDefinition(
            line=line, column=col,
            name=name,
            superinterfaces=superinterfaces,
            methods=methods,
            properties=properties,
        )

    def visitParamList(self, ctx: DuanLangParser.ParamListContext):
        """参数列表"""
        return [self.visitParam(p) for p in ctx.param()]

    def visitParam(self, ctx: DuanLangParser.ParamContext):
        """单个参数"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column

        typ = None
        if ctx.typeAnnotation():
            typ = self.visitTypeAnnotation(ctx.typeAnnotation())

        default = None
        if ctx.expr():
            default = self.visitExpr(ctx.expr())

        return Parameter(line=line, column=col, name=name,
                         type_annotation=typ, default_value=default)

    def visitBlock(self, ctx: DuanLangParser.BlockContext):
        """代码块（语句列表）"""
        stmts = []
        for child in ctx.getChildren():
            if isinstance(child, DuanLangParser.StmtContext):
                stmt = self.visitStmt(child)
                if stmt:
                    stmts.append(stmt)
            elif isinstance(child, DuanLangParser.DefinitionContext):
                # 块内嵌套定义
                defn = self.visitDefinition(child)
                if defn:
                    stmts.append(defn)
        return stmts

    def visitDefinition(self, ctx: DuanLangParser.DefinitionContext):
        """定义分发"""
        if ctx.paragraphDef():
            return self.visitParagraphDef(ctx.paragraphDef())
        elif ctx.classDef():
            return self.visitClassDef(ctx.classDef())
        elif ctx.interfaceDef():
            return self.visitInterfaceDef(ctx.interfaceDef())
        elif ctx.dataTypeDef():
            return self.visitDataTypeDef(ctx.dataTypeDef())
        elif ctx.errorTypeDef():
            return self.visitErrorTypeDef(ctx.errorTypeDef())
        return None

    # ----- 类型定义 -----

    def visitDataTypeDef(self, ctx: DuanLangParser.DataTypeDefContext):
        """数据类型定义"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column
        fields = [self.visitDataTypeField(f) for f in ctx.dataTypeField()]
        return DataTypeDefinition(line=line, column=col, name=name, fields=fields)

    def visitErrorTypeDef(self, ctx: DuanLangParser.ErrorTypeDefContext):
        """错误类型定义"""
        name = ctx.ID().getText()
        line = ctx.start.line
        col = ctx.start.column
        fields = [self.visitDataTypeField(f) for f in ctx.dataTypeField()]
        return ErrorTypeDefinition(line=line, column=col, name=name, fields=fields)

    def visitDataTypeField(self, ctx: DuanLangParser.DataTypeFieldContext):
        """类型字段"""
        name = ctx.ID().getText()
        typ = self.visitTypeAnnotation(ctx.typeAnnotation())
        line = ctx.start.line
        col = ctx.start.column
        return DataTypeField(line=line, column=col, name=name, type_annotation=typ)

    # ----- 导入/导出 -----

    def visitImportStmt(self, ctx: DuanLangParser.ImportStmtContext):
        """导入语句"""
        line = ctx.start.line
        col = ctx.start.column

        # 从...导入 格式
        if ctx.K_FROM():
            path_ctx = ctx.path()
            module = "".join(t.getText() for t in path_ctx.getChildren())
            names = [self.visitImportItem(item) for item in ctx.importList().importItem()]
            return ImportStatement(line=line, column=col, module=module, names=names)

        # 直接导入
        names = [self.visitImportItem(item) for item in ctx.importList().importItem()]
        return ImportStatement(line=line, column=col, module="", names=names)

    def visitImportItem(self, ctx: DuanLangParser.ImportItemContext):
        """导入项"""
        return ctx.ID().getText()

    def visitExportStmt(self, ctx: DuanLangParser.ExportStmtContext):
        """导出语句"""
        line = ctx.start.line
        col = ctx.start.column
        name = ctx.ID().getText()
        return ExportStatement(line=line, column=col, name=name)

    # ----- 语句 -----

    def visitStmt(self, ctx: DuanLangParser.StmtContext):
        """语句分发"""
        if ctx.varDecl():
            return self.visitVarDecl(ctx.varDecl())
        elif ctx.assignStmt():
            return self.visitAssignStmt(ctx.assignStmt())
        elif ctx.ifStmt():
            return self.visitIfStmt(ctx.ifStmt())
        elif ctx.foreachStmt():
            return self.visitForeachStmt(ctx.foreachStmt())
        elif ctx.whileStmt():
            return self.visitWhileStmt(ctx.whileStmt())
        elif ctx.returnStmt():
            return self.visitReturnStmt(ctx.returnStmt())
        elif ctx.breakStmt():
            return self.visitBreakStmt(ctx.breakStmt())
        elif ctx.continueStmt():
            return self.visitContinueStmt(ctx.continueStmt())
        elif ctx.tryStmt():
            return self.visitTryStmt(ctx.tryStmt())
        elif ctx.throwStmt():
            return self.visitThrowStmt(ctx.throwStmt())
        elif ctx.printStmt():
            return self.visitPrintStmt(ctx.printStmt())
        elif ctx.exprStmt():
            return self.visitExprStmt(ctx.exprStmt())
        return None

    def visitVarDecl(self, ctx: DuanLangParser.VarDeclContext):
        """变量声明"""
        line = ctx.start.line
        col = ctx.start.column

        # 支持target（可以是ID或己属性）
        if ctx.target():
            target = self.visitTarget(ctx.target())
            value = None
            if ctx.expr():
                value = self.visitExpr(ctx.expr())
            
            # 如果target是PropertyAccess（己属性），返回Assignment
            if isinstance(target, PropertyAccess):
                return Assignment(line=line, column=col, target=target, value=value)
            
            # 否则返回VariableDeclaration
            return VariableDeclaration(line=line, column=col, name=target.name, value=value)
        
        # 兼容旧的ID语法
        name = ctx.ID().getText()
        value = None
        if ctx.expr():
            value = self.visitExpr(ctx.expr())

        # 特殊处理：以"己"开头的变量名 -> 转换为属性赋值
        if name.startswith('己'):
            prop_name = name[1:]  # 去掉"己"前缀
            if prop_name:  # 确保有属性名
                target = PropertyAccess(line=line, column=col,
                                        obj=SelfReference(line=line, column=col),
                                        property_name=prop_name)
                return Assignment(line=line, column=col, target=target, value=value)

        return VariableDeclaration(line=line, column=col, name=name, value=value)

    def visitAssignStmt(self, ctx: DuanLangParser.AssignStmtContext):
        """赋值语句"""
        line = ctx.start.line
        col = ctx.start.column
        target = self.visitTarget(ctx.target())
        value = self.visitExpr(ctx.expr())
        return Assignment(line=line, column=col, target=target, value=value)

    def visitTarget(self, ctx: DuanLangParser.TargetContext):
        """赋值目标"""
        if ctx.expr():
            # 属性赋值：expr 之 ID
            expr = self.visitExpr(ctx.expr())
            prop = ctx.ID().getText()
            return PropertyAccess(line=ctx.start.line, column=ctx.start.column,
                                   obj=expr, property_name=prop)
        elif ctx.primary() and ctx.DOT():
            # 属性访问作为赋值目标：primary . ID
            expr = self.visitPrimary(ctx.primary())
            prop = ctx.ID().getText()
            return PropertyAccess(line=ctx.start.line, column=ctx.start.column,
                                   obj=expr, property_name=prop)
        elif ctx.K_SELF():
            # 己属性赋值：己属性名
            prop = ctx.ID().getText()
            return PropertyAccess(line=ctx.start.line, column=ctx.start.column,
                                   obj=SelfReference(line=ctx.start.line, column=ctx.start.column),
                                   property_name=prop)
        # 简单变量赋值 - 但要检查是否以"己"开头
        name = ctx.ID().getText()
        if name.startswith('己'):
            prop_name = name[1:]  # 去掉"己"前缀
            if prop_name:  # 确保有属性名
                return PropertyAccess(line=ctx.start.line, column=ctx.start.column,
                                       obj=SelfReference(line=ctx.start.line, column=ctx.start.column),
                                       property_name=prop_name)
        
        return Identifier(line=ctx.start.line, column=ctx.start.column, name=name)

    def visitIfStmt(self, ctx: DuanLangParser.IfStmtContext):
        """条件语句"""
        line = ctx.start.line
        col = ctx.start.column

        condition = self.visitExpr(ctx.expr(0))

        then_body = []
        if ctx.block(0):
            then_body = self.visitBlock(ctx.block(0))

        else_body = None
        num_elseif = len(ctx.K_ELSE_IF())
        if ctx.K_ELSE():
            # else 体在最后一个 block（索引 = elseif 数量 + 1）
            else_body = self.visitBlock(ctx.block(num_elseif + 1))

        # elseif 子句
        elseif_conditions = []
        elseif_bodies = []
        if num_elseif > 0:
            for i in range(num_elseif):
                # elseif 条件
                cond_idx = i + 1
                elseif_conditions.append(self.visitExpr(ctx.expr(cond_idx)))
                # elseif 体
                elseif_bodies.append(self.visitBlock(ctx.block(i + 1)))

        return IfStatement(
            line=line, column=col,
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            elseif_conditions=elseif_conditions,
            elseif_bodies=elseif_bodies,
        )

    def visitForeachStmt(self, ctx: DuanLangParser.ForeachStmtContext):
        """遍历循环"""
        line = ctx.start.line
        col = ctx.start.column

        # 遍历变量（直接从foreachStmt获取）
        variable = ctx.ID().getText() if ctx.ID() else "当前项"

        iterable = self.visitExpr(ctx.expr())

        body = []
        if ctx.block():
            body = self.visitBlock(ctx.block())

        return ForeachStatement(line=line, column=col, variable=variable,
                                iterable=iterable, body=body)

    def visitWhileStmt(self, ctx: DuanLangParser.WhileStmtContext):
        """当循环"""
        line = ctx.start.line
        col = ctx.start.column
        condition = self.visitExpr(ctx.expr())
        body = []
        if ctx.block():
            body = self.visitBlock(ctx.block())
        return WhileStatement(line=line, column=col, condition=condition, body=body)

    def visitReturnStmt(self, ctx: DuanLangParser.ReturnStmtContext):
        """返回语句"""
        line = ctx.start.line
        col = ctx.start.column
        value = None
        if ctx.expr():
            value = self.visitExpr(ctx.expr())
        return ReturnStatement(line=line, column=col, value=value)

    def visitBreakStmt(self, ctx: DuanLangParser.BreakStmtContext):
        """跳出语句"""
        return BreakStatement(line=ctx.start.line, column=ctx.start.column)

    def visitContinueStmt(self, ctx: DuanLangParser.ContinueStmtContext):
        """跳过语句"""
        return ContinueStatement(line=ctx.start.line, column=ctx.start.column)

    def visitTryStmt(self, ctx: DuanLangParser.TryStmtContext):
        """异常捕获"""
        line = ctx.start.line
        col = ctx.start.column
        try_body = self.visitBlock(ctx.block(0))
        catch_var = ctx.ID().getText()
        catch_body = self.visitBlock(ctx.block(1))
        return TryStatement(line=line, column=col, try_body=try_body,
                            catch_var=catch_var, catch_body=catch_body)

    def visitThrowStmt(self, ctx: DuanLangParser.ThrowStmtContext):
        """抛出异常"""
        line = ctx.start.line
        col = ctx.start.column
        value = self.visitExpr(ctx.expr())
        return ThrowStatement(line=line, column=col, value=value)

    def visitPrintStmt(self, ctx: DuanLangParser.PrintStmtContext):
        """打印语句"""
        line = ctx.start.line
        col = ctx.start.column
        value = self.visitExpr(ctx.expr())
        return PrintStatement(line=line, column=col, value=value)

    def visitExprStmt(self, ctx: DuanLangParser.ExprStmtContext):
        """表达式语句"""
        line = ctx.start.line
        col = ctx.start.column
        expr = self.visitExpr(ctx.expr())
        return ExpressionStatement(line=line, column=col, expression=expr)

    # ----- 表达式 -----

    def visitExpr(self, ctx: DuanLangParser.ExprContext):
        """表达式入口"""
        child = ctx.getChild(0)
        if isinstance(child, DuanLangParser.PipelineExprContext):
            return self.visitPipelineExpr(child)
        elif isinstance(child, DuanLangParser.AndExprContext):
            return self.visitAndExpr(child)
        elif isinstance(child, DuanLangParser.OrExprContext):
            return self.visitOrExpr(child)
        elif isinstance(child, DuanLangParser.ComparisonExprContext):
            return self.visitComparisonExpr(child)
        elif isinstance(child, DuanLangParser.AdditiveExprContext):
            return self.visitAdditiveExpr(child)
        elif isinstance(child, DuanLangParser.MultiplicativeExprContext):
            return self.visitMultiplicativeExpr(child)
        elif isinstance(child, DuanLangParser.UnaryExprContext):
            return self.visitUnaryExpr(child)
        elif isinstance(child, DuanLangParser.PostfixExprContext):
            return self.visitPostfixExpr(child)
        elif isinstance(child, DuanLangParser.PrimaryContext):
            return self.visitPrimary(child)
        return self.visit(child)

    def visitPipelineExpr(self, ctx: DuanLangParser.PipelineExprContext):
        """管道表达式"""
        # 使用 getTypedRuleContexts 获取 AndExpr 子节点
        exprs = [self.visitAndExpr(c)
                 for c in ctx.getTypedRuleContexts(DuanLangParser.AndExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        line = ctx.start.line
        col = ctx.start.column
        return PipeExpression(line=line, column=col, expressions=exprs)

    def visitAndExpr(self, ctx: DuanLangParser.AndExprContext):
        """逻辑与表达式"""
        exprs = [self.visitOrExpr(c)
                 for c in ctx.getTypedRuleContexts(DuanLangParser.OrExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        # 从左到右构建 BinaryOp
        result = exprs[0]
        for i in range(1, len(exprs)):
            result = BinaryOp(line=result.line, column=result.column,
                              left=result, operator='且', right=exprs[i])
        return result

    def visitOrExpr(self, ctx: DuanLangParser.OrExprContext):
        """逻辑或表达式"""
        exprs = [self.visitComparisonExpr(c)
                 for c in ctx.getTypedRuleContexts(DuanLangParser.ComparisonExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        result = exprs[0]
        for i in range(1, len(exprs)):
            result = BinaryOp(line=result.line, column=result.column,
                              left=result, operator='或', right=exprs[i])
        return result

    def visitComparisonExpr(self, ctx: DuanLangParser.ComparisonExprContext):
        """比较表达式"""
        exprs = [self.visitAdditiveExpr(a)
                 for a in ctx.getTypedRuleContexts(DuanLangParser.AdditiveExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        ops = [c.getText() for c in ctx.compOp()]
        result = exprs[0]
        for i, op in enumerate(ops):
            result = BinaryOp(line=result.line, column=result.column,
                              left=result, operator=op, right=exprs[i+1])
        return result

    def visitAdditiveExpr(self, ctx: DuanLangParser.AdditiveExprContext):
        """加减表达式"""
        exprs = [self.visitMultiplicativeExpr(m)
                 for m in ctx.getTypedRuleContexts(DuanLangParser.MultiplicativeExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        ops = [c.getText() for c in ctx.addOp()]
        result = exprs[0]
        for i, op in enumerate(ops):
            result = BinaryOp(line=result.line, column=result.column,
                              left=result, operator=op, right=exprs[i+1])
        return result

    def visitMultiplicativeExpr(self, ctx: DuanLangParser.MultiplicativeExprContext):
        """乘除表达式（将 ×/÷ 符号归一化为 乘/除 中文关键字）"""
        exprs = [self.visitUnaryExpr(u)
                 for u in ctx.getTypedRuleContexts(DuanLangParser.UnaryExprContext)]
        if len(exprs) == 1:
            return exprs[0]
        ops = [c.getText() for c in ctx.multOp()]
        result = exprs[0]
        for i, op in enumerate(ops):
            # 归一化符号运算符
            normalized_op = op
            if op == '×':
                normalized_op = '乘'
            elif op == '÷':
                normalized_op = '除'
            result = BinaryOp(line=result.line, column=result.column,
                              left=result, operator=normalized_op, right=exprs[i+1])
        return result

    def visitUnaryExpr(self, ctx: DuanLangParser.UnaryExprContext):
        """一元表达式"""
        if ctx.K_NOT() or ctx.NOT():
            op = ctx.K_NOT().getText() if ctx.K_NOT() else ctx.NOT().getText()
            operand = self.visitUnaryExpr(ctx.unaryExpr())
            return UnaryOp(line=ctx.start.line, column=ctx.start.column,
                           operator=op, operand=operand)
        if ctx.MINUS() or ctx.K_MINUS():
            operand = self.visitUnaryExpr(ctx.unaryExpr())
            return UnaryOp(line=ctx.start.line, column=ctx.start.column,
                           operator='-', operand=operand)
        return self.visitPostfixExpr(ctx.postfixExpr())

    def visitPostfixExpr(self, ctx: DuanLangParser.PostfixExprContext):
        """后缀表达式：处理索引访问、属性访问、函数调用"""
        base = self.visitPrimary(ctx.primary())

        # 如果已经是 NewExpression，直接返回（避免被包装成 FunctionCall）
        if isinstance(base, NewExpression):
            return base

        # 顺序处理后缀操作（按子节点位置）
        child_idx = 1  # 0 是 primary
        while child_idx < ctx.getChildCount():
            child = ctx.getChild(child_idx)

            if isinstance(child, TerminalNode):
                ttype = child.symbol.type

                # 属性访问：对象之属性
                if ttype == DuanLangParser.K_OF:
                    child_idx += 1
                    prop_name = ctx.getChild(child_idx).getText()
                    child_idx += 1
                    base = PropertyAccess(line=base.line, column=base.column,
                                          obj=base, property_name=prop_name)

                # 属性访问：对象.属性
                elif ttype == DuanLangParser.DOT:
                    child_idx += 1
                    prop_name = ctx.getChild(child_idx).getText()
                    child_idx += 1
                    base = PropertyAccess(line=base.line, column=base.column,
                                          obj=base, property_name=prop_name)

                # 索引访问：对象[索引]
                elif ttype == DuanLangParser.LBRACKET:
                    child_idx += 1
                    idx_expr = self.visit(ctx.getChild(child_idx))
                    child_idx += 1  # 跳过 expr
                    child_idx += 1  # 跳过 RBRACKET
                    base = IndexAccess(line=base.line, column=base.column,
                                       obj=base, index=idx_expr)

                # 函数调用：(参数)
                elif ttype == DuanLangParser.LPAREN:
                    child_idx += 1  # 跳过 LPAREN
                    args = []
                    if (child_idx < ctx.getChildCount() and
                            isinstance(ctx.getChild(child_idx),
                                       DuanLangParser.ExprListContext)):
                        args = self.visitExprList(ctx.getChild(child_idx))
                        child_idx += 1
                    child_idx += 1  # 跳过 RPAREN
                    base = FunctionCall(line=base.line, column=base.column,
                                        name=base, arguments=args)

                # 《段名》(参数) 调用
                elif ttype == DuanLangParser.BOOK_L:
                    child_idx += 1
                    seg_name = ctx.getChild(child_idx).getText()  # ID
                    child_idx += 1  # 跳过 ID
                    child_idx += 1  # 跳过 BOOK_R
                    child_idx += 1  # 跳过 LPAREN
                    args = []
                    if (child_idx < ctx.getChildCount() and
                            isinstance(ctx.getChild(child_idx),
                                       DuanLangParser.ExprListContext)):
                        args = self.visitExprList(ctx.getChild(child_idx))
                        child_idx += 1
                    child_idx += 1  # 跳过 RPAREN
                    seg = SegmentName(line=base.line, column=base.column, name=seg_name)
                    base = FunctionCall(line=base.line, column=base.column,
                                        name=seg, arguments=args)
                # ID(参数) - 直接调用（无书名号）
                elif ttype == DuanLangParser.ID and child_idx + 1 < ctx.getChildCount():
                    next_child = ctx.getChild(child_idx + 1)
                    if isinstance(next_child, TerminalNode) and next_child.symbol.type == DuanLangParser.LPAREN:
                        seg_name = child.getText()
                        child_idx += 1  # 跳过 ID
                        child_idx += 1  # 跳过 LPAREN
                        args = []
                        if (child_idx < ctx.getChildCount() and
                                isinstance(ctx.getChild(child_idx),
                                           DuanLangParser.ExprListContext)):
                            args = self.visitExprList(ctx.getChild(child_idx))
                            child_idx += 1
                        child_idx += 1  # 跳过 RPAREN
                        seg = SegmentName(line=base.line, column=base.column, name=seg_name)
                        base = FunctionCall(line=base.line, column=base.column,
                                            name=seg, arguments=args)
                    else:
                        child_idx += 1
                else:
                    child_idx += 1
            else:
                child_idx += 1

        return base

    def visitPrimary(self, ctx: DuanLangParser.PrimaryContext):
        """基本表达式"""
        line = ctx.start.line
        col = ctx.start.column

        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            if '.' in text:
                return NumberLiteral(line=line, column=col, value=float(text))
            return NumberLiteral(line=line, column=col, value=int(text))

        if ctx.STRING():
            text = ctx.STRING().getText()
            # 去掉引号并解析转义序列
            raw = text[1:-1]
            # 解析常见转义序列
            escaped = []
            i = 0
            while i < len(raw):
                if raw[i] == '\\' and i + 1 < len(raw):
                    nxt = raw[i + 1]
                    if nxt == 'n':
                        escaped.append('\n')
                    elif nxt == 't':
                        escaped.append('\t')
                    elif nxt == 'r':
                        escaped.append('\r')
                    elif nxt == '\\':
                        escaped.append('\\')
                    elif nxt == '"':
                        escaped.append('"')
                    elif nxt == "'":
                        escaped.append("'")
                    else:
                        escaped.append(raw[i])
                        escaped.append(nxt)
                    i += 2
                else:
                    escaped.append(raw[i])
                    i += 1
            return StringLiteral(line=line, column=col, value=''.join(escaped))

        if ctx.K_TRUE():
            return BooleanLiteral(line=line, column=col, value=True)
        if ctx.K_FALSE():
            return BooleanLiteral(line=line, column=col, value=False)
        if ctx.K_NULL():
            return NullLiteral(line=line, column=col)
        
        # self引用：己（通过检查子节点）
        for child in ctx.getChildren():
            if hasattr(child, 'symbol') and hasattr(child.symbol, 'type'):
                if child.symbol.type == DuanLangParser.K_SELF:
                    return SelfReference(line=line, column=col)

        # 实例化表达式：新 类名() - 必须在 ID 检查之前
        if ctx.K_NEW():
            class_name = ctx.ID().getText()
            arguments = []
            if ctx.exprList():
                arguments = self.visitExprList(ctx.exprList())
            return NewExpression(line=line, column=col, class_name=class_name, arguments=arguments)

        # 动词调用处理（基于Parser语法规则）
        # 列表操作动词
        if ctx.K_FIRST():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='首'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_LAST():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='末'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_REST():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='余'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_LENGTH():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='长'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_SORT():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='排序'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_REVERSE():
            return FunctionCall(line=line, column=col,
                                name=Identifier(line=line, column=col, name='反转'),
                                arguments=[self.visitExpr(ctx.expr(0))])
        # K_SUM, K_MAX, K_MIN 已移除
        if ctx.K_UNIQUE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='去重'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_FILTER():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='筛选'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_MAP():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='映射'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        
        # 字符串操作动词
        if ctx.K_TO_INT():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='转整数'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_TO_FLOAT():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='转浮点'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_TO_STR():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='转字符串'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_STR_LEN():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='字符串长度'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_STR_SPLIT():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='分割字符串'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_STR_JOIN():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='连接字符串'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_STR_REPLACE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='替换字符串'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1)), self.visitExpr(ctx.expr(2))])
        if ctx.K_STR_TRIM():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='去除空白'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        
        # 文件操作动词
        if ctx.K_READ_FILE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='读取文件'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_WRITE_FILE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='写入文件'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_APPEND_FILE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='追加文件'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_FILE_EXISTS():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='文件存在'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_DIR_EXISTS():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='目录存在'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_MAKE_DIR():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='创建目录'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_REMOVE_FILE():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='删除文件'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_REMOVE_DIR():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='删除目录'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        
        # 系统操作动词
        if ctx.K_ENV():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='环境变量'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_SET_ENV():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='设置环境变量'),
                               arguments=[self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1))])
        if ctx.K_ARGS():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='参数列表'),
                               arguments=[])
        if ctx.K_EXIT():
            args = []
            if ctx.expr():
                args = [self.visitExpr(ctx.expr(0))]
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='退出程序'),
                               arguments=args)
        if ctx.K_CWD():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='当前目录'),
                               arguments=[])
        if ctx.K_CD():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='切换目录'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        if ctx.K_EXEC():
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='执行命令'),
                               arguments=[self.visitExpr(ctx.expr(0))])
        
        # I/O操作动词
        if ctx.K_PRINT():
            args = []
            if ctx.exprList():
                args = self.visitExprList(ctx.exprList())
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='打印'),
                               arguments=args)
        if ctx.K_OUTPUT():
            args = []
            if ctx.exprList():
                args = self.visitExprList(ctx.exprList())
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='输出'),
                               arguments=args)
        if ctx.K_INPUT():
            args = []
            if ctx.expr():
                args = [self.visitExpr(ctx.expr(0))]
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='输入'),
                               arguments=args)
        if ctx.K_READ():
            args = []
            if ctx.expr():
                args = [self.visitExpr(ctx.expr(0))]
            return FunctionCall(line=line, column=col,
                               name=Identifier(line=line, column=col, name='读取'),
                               arguments=args)

        if ctx.ID():
            name = ctx.ID().getText()
            # 特殊处理：以"己"开头的标识符 -> 己.属性
            if name.startswith('己'):
                # 拆分为 self.属性
                prop_name = name[1:]  # 去掉"己"前缀
                if prop_name:  # 确保有属性名
                    return PropertyAccess(line=line, column=col,
                                          obj=SelfReference(line=line, column=col),
                                          property_name=prop_name)
            return Identifier(line=line, column=col, name=name)

        if ctx.LPAREN():
            exprs = ctx.expr()
            if exprs:
                return self.visitExpr(exprs[0])
            return None

        if ctx.LBRACKET():
            # 优先检查是否为字典字面量
            if ctx.dictLiteral():
                from duan_ast import DictEntry
                entries = []
                for entry_ctx in ctx.dictLiteral().dictEntry():
                    key = self.visitExpr(entry_ctx.expr(0))
                    value = self.visitExpr(entry_ctx.expr(1))
                    entries.append(DictEntry(line=key.line, column=key.column, key=key, value=value))
                return DictLiteral(line=line, column=col, entries=entries)
            # 否则为列表字面量
            elements = []
            if ctx.exprList():
                elements = self.visitExprList(ctx.exprList())
            return ListLiteral(line=line, column=col, elements=elements)

        if ctx.BOOK_L() and ctx.BOOK_R():
            return SegmentName(line=line, column=col, name=ctx.ID().getText())

        # Fallback
        return None

    def visitExprList(self, ctx: DuanLangParser.ExprListContext):
        """表达式列表"""
        return [self.visitExpr(e) for e in ctx.expr()]

    def visitTypeAnnotation(self, ctx: DuanLangParser.TypeAnnotationContext):
        """类型注解"""
        if ctx.ID():
            return ctx.ID().getText()
        if ctx.builtinType():
            return ctx.builtinType().getText()
        return "任意"


# =============================================================================
# 词法分析器包装
# =============================================================================

class DuanLexer:
    """段言词法分析器包装"""

    def __init__(self):
        self.errors = []

    def tokenize(self, source: str) -> List:
        """将源代码分词为 Token 列表（使用自定义中文分词器）"""
        from duan_tokenizer import DuanLangTokenizer

        tokenizer = DuanLangTokenizer()
        tokens = tokenizer.tokenize(source)

        if tokenizer.errors:
            self.errors = tokenizer.errors

        return tokens


# =============================================================================
# 语法解析器包装
# =============================================================================

class DuanParser:
    """段言语法解析器包装"""

    def __init__(self):
        self.errors = []

    def parse(self, source: str) -> Optional[Module]:
        """解析源代码为 AST（使用标准ANTLR词法分析器）"""
        # 创建 ANTLR lexer 和 parser
        input_stream = InputStream(source)
        lexer = DuanLangLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = DuanLangParser(token_stream)
        
        # 设置错误监听器
        error_listener = DuanLangErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        # 解析
        tree = parser.program()

        if error_listener.has_errors():
            self.errors = error_listener.get_errors()
            return None

        # 构建 AST
        builder = DuanLangASTBuilder()
        module = builder.visitProgram(tree)
        self.errors = builder.errors
        return module


# =============================================================================
# 高层解析接口
# =============================================================================

def parse_source(source: str) -> Module:
    """解析段言源代码，返回 AST"""
    parser = DuanParser()
    module = parser.parse(source)
    if parser.errors:
        for err in parser.errors:
            print(f"[语法错误] {err}", file=sys.stderr)
    return module


def parse_file(filepath: str) -> Module:
    """从文件读取段言源代码并解析"""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    return parse_source(source)