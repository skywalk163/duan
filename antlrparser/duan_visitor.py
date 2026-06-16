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
    ConditionalExpression,
    StringInterpolation, ListComprehension, LambdaExpression,
    MatchStatement, MatchCase, MatchPattern,
    DictComprehension, DecoratorDefinition, DestructuringAssignment, WithStatement,
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
    """段言语法错误监听器 — 中文提示+修复建议"""

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        chinese_msg = self._translate_error(msg)
        suggestion = self._get_suggestion(msg)
        if suggestion:
            error_msg = f"第{line}行, 第{column}列: {chinese_msg}\n  建议: {suggestion}"
        else:
            error_msg = f"第{line}行, 第{column}列: {chinese_msg}"
        self.errors.append(error_msg)

    @staticmethod
    def _decode_unicode(msg: str) -> str:
        """解码消息中的 \\uXXXX 转义序列"""
        import re
        def replace_unicode(match):
            return chr(int(match.group(1), 16))
        return re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, msg)

    @staticmethod
    def _translate_error(msg: str) -> str:
        """将 ANTLR 英文错误翻译为中文"""
        # 先解码 Unicode 转义
        msg = DuanLangErrorListener._decode_unicode(msg)

        # mismatched input
        if msg.startswith("mismatched input"):
            # mismatched input 'X' expecting {'Y', 'Z'}
            parts = msg.split("expecting")
            if len(parts) == 2:
                found = parts[0].replace("mismatched input", "").strip().strip("'")
                expected = parts[1].strip()
                # 展开期望列表
                expected = expected.replace("{", "").replace("}", "")
                expected_list = [e.strip().strip("'") for e in expected.split(",")]
                if len(expected_list) == 1:
                    return f"期望 {expected_list[0]}，却遇到了 '{found}'"
                elif len(expected_list) <= 3:
                    expect_text = "、".join(expected_list)
                    return f"期望 {expect_text}，却遇到了 '{found}'"
                else:
                    expect_text = "、".join(expected_list[:3])
                    return f"语法不匹配: 遇到了 '{found}'，期望 {expect_text} 等"
            return f"语法不匹配: {msg}"

        # missing
        if msg.startswith("missing"):
            # missing 'X' at 'Y'
            parts = msg.split("at")
            if len(parts) == 2:
                missing = parts[0].replace("missing", "").strip().strip("'")
                location = parts[1].strip().strip("'")
                if location == '<EOF>':
                    return f"缺少 '{missing}'（文件末尾）"
                return f"在 '{location}' 处缺少 '{missing}'"
            return f"缺少语法元素: {msg}"

        # extraneous input
        if msg.startswith("extraneous input"):
            # extraneous input 'X' expecting {'Y', 'Z'}
            parts = msg.split("expecting")
            if len(parts) == 2:
                found = parts[0].replace("extraneous input", "").strip().strip("'")
                expected = parts[1].strip().replace("{", "").replace("}", "")
                expected_list = [e.strip().strip("'") for e in expected.split(",")]
                if len(expected_list) == 1:
                    return f"多余的 '{found}'，此处应为 {expected_list[0]}"
                expect_text = "、".join(expected_list[:3])
                return f"多余的 '{found}'，此处应为 {expect_text} 等"
            return f"多余输入: {msg}"

        # no viable alternative
        if msg.startswith("no viable alternative"):
            return "语法错误，无法解析此处的输入"

        # token recognition
        if msg.startswith("token recognition"):
            return f"无法识别的字符: {msg.split('at:')[1].strip() if 'at:' in msg else msg}"

        # 其他错误
        return msg

    @staticmethod
    def _get_suggestion(msg: str) -> str:
        """根据错误给出中文修复建议"""
        msg_lower = msg.lower()

        # 缺少句号
        if msg.startswith("missing") and ("PERIOD" in msg or "。'" in msg):
            return "每条语句末尾需要加中文句号「。」"

        # 缺少冒号
        if msg.startswith("missing") and "COLON" in msg:
            return "段定义或条件语句末尾需要加中文冒号「：」"

        # 多余结束
        if "K_END" in msg and ("extraneous" in msg_lower or "mismatched" in msg_lower):
            return "可能缺少「结束」标记，或层级缩进有误"

        # 括号不匹配
        if "mismatched" in msg_lower and ("LPAREN" in msg or "RPAREN" in msg):
            return "检查括号是否匹配，是否缺少左括号「（」或右括号「）」"

        # 中括号不匹配
        if "mismatched" in msg_lower and ("LBRACKET" in msg or "RBRACKET" in msg):
            return "检查中括号是否匹配，是否缺少「【」或「】」"

        # 语法结构错误
        if "no viable" in msg_lower:
            return "请检查此行的语法结构，是否有拼写错误或缺少关键字"

        # 结束标记错误
        if msg.startswith("missing") and "K_END" in msg:
            return "段落缺少结束标记「结束」，或层级缩进有误"

        return ""

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

    # ----- 中文数字转换 -----
    
    _CN_DIGITS = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '万': 10000,
    }

    def _is_chinese_number(self, text: str):
        """检查文本是否为中文数字，若是则返回数值，否则返回 None"""
        if not text:
            return None
        
        # 检查所有字符是否都是中文数字相关
        for ch in text:
            if ch not in self._CN_DIGITS and ch != '点':
                return None
        
        # 处理小数
        if '点' in text:
            parts = text.split('点', 1)
            if len(parts) != 2:
                return None
            int_part = self._convert_chinese_integer(parts[0])
            if int_part is None:
                return None
            frac = 0.0
            frac_len = 0
            for ch in parts[1]:
                if ch in self._CN_DIGITS and self._CN_DIGITS[ch] < 10:
                    frac = frac * 10 + self._CN_DIGITS[ch]
                    frac_len += 1
                else:
                    return None
            if frac_len == 0:
                return float(int_part)
            return float(int_part) + frac / (10 ** frac_len)
        
        # 处理整数
        return self._convert_chinese_integer(text)
    
    def _convert_chinese_integer(self, text: str):
        """将中文整数转换为数值"""
        if not text:
            return None
        
        digits = self._CN_DIGITS
        
        # 简单数字
        if text in digits:
            return digits[text]
        
        # 处理复合数字（如十六、一百零一、三百二十一）
        result = 0
        temp = 0
        for ch in text:
            if ch in digits:
                d = digits[ch]
                if d >= 10:  # 十、百、千、万是进位单位
                    if temp == 0:
                        temp = 1  # "十"在开头表示1*10
                    temp *= d
                    result += temp
                    temp = 0
                elif d == 0:  # 零表示空位
                    temp = 0
                else:  # 0-9的数字
                    temp = d
            else:
                return None
        
        result += temp
        return result

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
        name = self._get_identifier_like_name(ctx.identifier_like())
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

    def _get_identifier_like_name(self, ctx):
        """从 identifier_like 规则中提取名称文本"""
        if ctx is None:
            return ''
        if ctx.ID():
            return ctx.ID().getText()
        # 内置类型token也可以作为标识符名
        if ctx.T_NUMBER():
            return ctx.T_NUMBER().getText()
        if ctx.T_INT():
            return ctx.T_INT().getText()
        if ctx.T_FLOAT():
            return ctx.T_FLOAT().getText()
        if ctx.T_STRING():
            return ctx.T_STRING().getText()
        if ctx.T_LIST():
            return ctx.T_LIST().getText()
        if ctx.T_DICT():
            return ctx.T_DICT().getText()
        if ctx.T_SET():
            return ctx.T_SET().getText()
        if ctx.T_BOOL():
            return ctx.T_BOOL().getText()
        if ctx.T_ANY():
            return ctx.T_ANY().getText()
        if ctx.K_TRUE():
            return ctx.K_TRUE().getText()
        if ctx.K_FALSE():
            return ctx.K_FALSE().getText()
        if ctx.K_NULL():
            return ctx.K_NULL().getText()
        # fallback
        return ctx.getText()

    def _get_type_as_identifier_name(self, ctx):
        """从 typeAsIdentifier 规则中提取名称文本"""
        if ctx is None:
            return ''
        if ctx.T_NUMBER():
            return ctx.T_NUMBER().getText()
        if ctx.T_INT():
            return ctx.T_INT().getText()
        if ctx.T_FLOAT():
            return ctx.T_FLOAT().getText()
        if ctx.T_STRING():
            return ctx.T_STRING().getText()
        if ctx.T_LIST():
            return ctx.T_LIST().getText()
        if ctx.T_DICT():
            return ctx.T_DICT().getText()
        if ctx.T_SET():
            return ctx.T_SET().getText()
        if ctx.T_BOOL():
            return ctx.T_BOOL().getText()
        if ctx.T_ANY():
            return ctx.T_ANY().getText()
        return ctx.getText()

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
        elif ctx.decoratorDef():
            return self.visitDecoratorDef(ctx.decoratorDef())
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
        elif ctx.matchStmt():
            return self.visitMatchStmt(ctx.matchStmt())
        elif ctx.withStmt():
            return self.visitWithStmt(ctx.withStmt())
        elif ctx.printStmt():
            return self.visitPrintStmt(ctx.printStmt())
        elif ctx.exprStmt():
            return self.visitExprStmt(ctx.exprStmt())
        return None

    def visitVarDecl(self, ctx: DuanLangParser.VarDeclContext):
        """变量声明"""
        line = ctx.start.line
        col = ctx.start.column

        # 解构赋值：设 (甲, 乙) 为 元组 — 有 LPAREN
        if ctx.LPAREN():
            variables = [self._get_identifier_like_name(il) for il in ctx.identifier_like()]
            value = self.visitExpr(ctx.expr())
            return DestructuringAssignment(line=line, column=col,
                                           variables=variables, value=value)

        # 己属性赋值：设 己属性名 为 值 — 有 K_SELF
        if ctx.K_SELF():
            prop = ctx.ID(0).getText() if ctx.ID() else ''
            if prop:
                target = PropertyAccess(line=line, column=col,
                                        obj=SelfReference(line=line, column=col),
                                        property_name=prop)
                value = self.visitExpr(ctx.expr()) if ctx.expr() else None
                return Assignment(line=line, column=col, target=target, value=value)

        # 普通变量声明：设 甲 为 值 — 用 identifier_like 获取变量名
        if ctx.identifier_like():
            name = self._get_identifier_like_name(ctx.identifier_like(0))
            value = self.visitExpr(ctx.expr()) if ctx.expr() else None

            # 特殊处理：以"己"开头的变量名 -> 转换为属性赋值
            if name.startswith('己'):
                prop_name = name[1:]  # 去掉"己"前缀
                if prop_name:  # 确保有属性名
                    target = PropertyAccess(line=line, column=col,
                                            obj=SelfReference(line=line, column=col),
                                            property_name=prop_name)
                    return Assignment(line=line, column=col, target=target, value=value)

            return VariableDeclaration(line=line, column=col, name=name, value=value)

        return None

    def visitAssignStmt(self, ctx: DuanLangParser.AssignStmtContext):
        """赋值语句"""
        line = ctx.start.line
        col = ctx.start.column
        value = self.visitExpr(ctx.expr())

        # 己属性赋值：己属性名 = 值
        if ctx.K_SELF():
            prop = ctx.ID().getText() if ctx.ID() else ''
            target = PropertyAccess(line=line, column=col,
                                    obj=SelfReference(line=line, column=col),
                                    property_name=prop)
            return Assignment(line=line, column=col, target=target, value=value)

        # 属性赋值：primary . ID = 值
        if ctx.primary() and ctx.DOT():
            expr = self.visitPrimary(ctx.primary())
            prop = ctx.ID().getText()
            target = PropertyAccess(line=line, column=col,
                                    obj=expr, property_name=prop)
            return Assignment(line=line, column=col, target=target, value=value)

        # 简单变量赋值：甲 = 值（使用 identifier_like）
        if ctx.identifier_like():
            name = self._get_identifier_like_name(ctx.identifier_like(0))
        elif ctx.ID():
            name = ctx.ID().getText()
        else:
            name = ''
        # 特殊处理：以"己"开头的变量名
        if name.startswith('己'):
            prop_name = name[1:]
            if prop_name:
                target = PropertyAccess(line=line, column=col,
                                        obj=SelfReference(line=line, column=col),
                                        property_name=prop_name)
                return Assignment(line=line, column=col, target=target, value=value)

        target = Identifier(line=line, column=col, name=name)
        return Assignment(line=line, column=col, target=target, value=value)

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

    def visitMatchStmt(self, ctx: DuanLangParser.MatchStmtContext):
        """模式匹配语句"""
        line = ctx.start.line
        col = ctx.start.column
        subject = self.visitExpr(ctx.expr())
        cases = []
        for case_ctx in ctx.matchCase():
            cases.append(self.visitMatchCase(case_ctx))
        return MatchStatement(line=line, column=col, subject=subject, cases=cases)

    def visitMatchCase(self, ctx: DuanLangParser.MatchCaseContext):
        """匹配分支"""
        line = ctx.start.line
        col = ctx.start.column
        pattern = self.visitMatchPattern(ctx.matchPattern())
        guard = None
        if ctx.K_IF():
            # 从expr中找守卫条件
            exprs = ctx.expr()
            if exprs:
                guard = self.visitExpr(exprs[0])
        body = self.visitBlock(ctx.block()) if ctx.block() else []
        return MatchCase(line=line, column=col, pattern=pattern, guard=guard, body=body)

    def visitMatchPattern(self, ctx: DuanLangParser.MatchPatternContext):
        """匹配模式"""
        line = ctx.start.line
        col = ctx.start.column

        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            value = float(text) if '.' in text else int(text)
            return MatchPattern(line=line, column=col, kind='number',
                                value=NumberLiteral(line=line, column=col, value=value))
        if ctx.STRING():
            text = ctx.STRING().getText()
            raw = text[1:-1]
            value = self._unescape_string(raw)
            return MatchPattern(line=line, column=col, kind='string',
                                value=StringLiteral(line=line, column=col, value=value))
        if ctx.K_TRUE():
            return MatchPattern(line=line, column=col, kind='bool',
                                value=BooleanLiteral(line=line, column=col, value=True))
        if ctx.K_FALSE():
            return MatchPattern(line=line, column=col, kind='bool',
                                value=BooleanLiteral(line=line, column=col, value=False))
        if ctx.K_NULL():
            return MatchPattern(line=line, column=col, kind='null')
        if ctx.UNDERSCORE():
            return MatchPattern(line=line, column=col, kind='wildcard')

        # 列表模式
        if ctx.LBRACKET():
            elements = []
            if ctx.matchPatternList():
                elements = [self.visitMatchPattern(p) for p in ctx.matchPatternList().matchPattern()]
            return MatchPattern(line=line, column=col, kind='list', elements=elements)

        # 类型检查模式：类名 之 变量
        if ctx.K_OF():
            type_name = ctx.ID(0).getText() if ctx.ID(0) else ""
            binding = ctx.ID(1).getText() if len(ctx.ID()) > 1 else ""
            return MatchPattern(line=line, column=col, kind='type_check',
                                type_name=type_name, binding=binding)

        # 变量绑定或标识符
        if ctx.ID():
            name = ctx.ID().getText()
            # 小写/中文标识符视为变量绑定，大写标识符视为枚举匹配
            return MatchPattern(line=line, column=col, kind='variable', binding=name)

        return MatchPattern(line=line, column=col, kind='wildcard')

    def visitWithStmt(self, ctx: DuanLangParser.WithStmtContext):
        """上下文管理器语句：使用 表达式 作为 变量：...结束。"""
        line = ctx.start.line
        col = ctx.start.column
        context_expr = self.visitExpr(ctx.expr())
        variable = ctx.ID().getText() if ctx.ID() else None
        body = self.visitBlock(ctx.block()) if ctx.block() else []
        return WithStatement(line=line, column=col,
                             context_expr=context_expr, variable=variable, body=body)

    def visitDecoratorDef(self, ctx: DuanLangParser.DecoratorDefContext):
        """装饰器定义：@段落名 标注 段落 ..."""
        line = ctx.start.line
        col = ctx.start.column
        decorator_name = ctx.ID().getText()
        paragraph = self.visitParagraphDef(ctx.paragraphDef())
        return DecoratorDefinition(line=line, column=col,
                                   decorator_name=decorator_name, paragraph=paragraph)

    def visitDictComprehension(self, ctx: DuanLangParser.DictComprehensionContext):
        """字典推导：{键: 值 遍历 变量 之 列表}"""
        line = ctx.start.line
        col = ctx.start.column
        key_expr = self.visitExpr(ctx.expr(0))
        value_expr = self.visitExpr(ctx.expr(1))
        variable = self._get_identifier_like_name(ctx.identifier_like())
        iterable = self.visitExpr(ctx.expr(2))
        condition = None
        if ctx.K_IF():
            condition = self.visitExpr(ctx.expr(3))
        return DictComprehension(line=line, column=col,
                                 key_expr=key_expr, value_expr=value_expr,
                                 variable=variable, iterable=iterable,
                                 condition=condition)

    def visitBracketContent(self, ctx: DuanLangParser.BracketContentContext):
        """方括号内容：消除列表/字典/推导歧义"""
        line = ctx.start.line
        col = ctx.start.column

        # 1. 字典推导：键: 值 遍历 ...
        if ctx.dictComprehension():
            return self.visitDictComprehension(ctx.dictComprehension())

        # 2. 字典字面量：键: 值, ...
        if ctx.dictLiteral():
            from duan_ast import DictEntry
            entries = []
            for entry_ctx in ctx.dictLiteral().dictEntry():
                key = self.visitExpr(entry_ctx.expr(0))
                value = self.visitExpr(entry_ctx.expr(1))
                entries.append(DictEntry(line=key.line, column=key.column, key=key, value=value))
            return DictLiteral(line=line, column=col, entries=entries)

        # 3. 列表推导：表达式 遍历 变量 之 ...
        if ctx.K_FOREACH():
            expression = self.visitExpr(ctx.expr(0))
            variable = self._get_identifier_like_name(ctx.identifier_like())
            iterable = self.visitExpr(ctx.expr(1))
            condition = None
            if ctx.K_IF():
                condition = self.visitExpr(ctx.expr(2))
            return ListComprehension(line=line, column=col,
                                     expression=expression, variable=variable,
                                     iterable=iterable, condition=condition)

        # 4. 列表字面量
        if ctx.exprList():
            elements = self.visitExprList(ctx.exprList())
            return ListLiteral(line=line, column=col, elements=elements)

        # 空列表
        return ListLiteral(line=line, column=col, elements=[])

    @staticmethod
    def _unescape_string(raw: str) -> str:
        """解析字符串转义序列"""
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
        return ''.join(escaped)

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
        # 独立的标识符作为表达式语句时，视为无参数函数调用
        # 例如：问候。 → FunctionCall(问候, [])
        if isinstance(expr, Identifier):
            expr = FunctionCall(line=expr.line, column=expr.column,
                                name=expr, arguments=[])
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
                              left=result, operator='or', right=exprs[i])
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
            # 检测是否包含插值表达式 {xxx}
            interpolated = self._parse_string_interpolation(raw, line, col)
            if interpolated is not None:
                return interpolated
            # 普通字符串
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

        # 三元条件表达式：如果 条件 那么 值1 否则 值2
        if ctx.conditionalExpr():
            return self.visitConditionalExpr(ctx.conditionalExpr())

        # 实例化表达式：新 类名() - 必须在 ID 检查之前
        if ctx.K_NEW():
            class_name = ctx.ID().getText()
            arguments = []
            if ctx.exprList():
                arguments = self.visitExprList(ctx.exprList())
            return NewExpression(line=line, column=col, class_name=class_name, arguments=arguments)

        # 列表推导：[表达式 遍历 变量 之 列表]
        if ctx.listComprehension():
            return self.visitListComprehension(ctx.listComprehension())

        # 匿名函数：接收 甲：返回 甲 乘 甲。
        if ctx.lambdaExpr():
            return self.visitLambdaExpr(ctx.lambdaExpr())

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
            # 检查是否为中文数字（如 四十二、三点一四）
            cn_value = self._is_chinese_number(name)
            if cn_value is not None:
                if isinstance(cn_value, float):
                    return NumberLiteral(line=line, column=col, value=cn_value)
                return NumberLiteral(line=line, column=col, value=cn_value)
            # 特殊处理：以"己"开头的标识符 -> 己.属性
            if name.startswith('己'):
                # 拆分为 self.属性
                prop_name = name[1:]  # 去掉"己"前缀
                if prop_name:  # 确保有属性名
                    return PropertyAccess(line=line, column=col,
                                          obj=SelfReference(line=line, column=col),
                                          property_name=prop_name)
            # 检查是否有隐式函数调用（无括号参数列表）
            if ctx.implicitCall():
                arguments = self.visitImplicitCall(ctx.implicitCall())
                return FunctionCall(line=line, column=col,
                                    name=Identifier(line=line, column=col, name=name),
                                    arguments=arguments)
            return Identifier(line=line, column=col, name=name)

        # 类型关键字用作标识符（如变量名"数"）
        if ctx.typeAsIdentifier():
            type_id = ctx.typeAsIdentifier()
            name = self._get_type_as_identifier_name(type_id)
            return Identifier(line=line, column=col, name=name)

        if ctx.LPAREN():
            exprs = ctx.expr()
            if exprs:
                return self.visitExpr(exprs[0])
            return None

        if ctx.LBRACKET():
            # 统一通过 bracketContent 处理
            if ctx.bracketContent():
                return self.visitBracketContent(ctx.bracketContent())
            # 空列表
            return ListLiteral(line=line, column=col, elements=[])

        if ctx.BOOK_L() and ctx.BOOK_R():
            return SegmentName(line=line, column=col, name=ctx.ID().getText())

        # Fallback
        return None

    def visitConditionalExpr(self, ctx: DuanLangParser.ConditionalExprContext):
        """三元条件表达式：如果 条件 那么 值1 否则 值2"""
        line = ctx.start.line
        col = ctx.start.column
        # conditionalExpr 规则：K_IF expr K_THEN expr ( K_ELSE expr )?
        # 子规则索引：K_IF(0), expr(0), K_THEN(1), expr(1), K_ELSE(2)?, expr(2)?
        condition = self.visitExpr(ctx.expr(0))
        then_expr = self.visitExpr(ctx.expr(1))
        else_expr = None
        if ctx.K_ELSE():
            else_expr = self.visitExpr(ctx.expr(2))
        return ConditionalExpression(
            line=line, column=col,
            condition=condition,
            then_expr=then_expr,
            else_expr=else_expr,
        )

    def visitImplicitCall(self, ctx: DuanLangParser.ImplicitCallContext):
        """隐式函数调用参数列表"""
        args = []
        for i in range(len(ctx.implicitArg())):
            arg_ctx = ctx.implicitArg(i)
            arg = self.visitImplicitArg(arg_ctx)
            if arg is not None:
                args.append(arg)
        return args

    def visitImplicitArg(self, ctx: DuanLangParser.ImplicitArgContext):
        """隐式函数调用的单个参数"""
        line = ctx.start.line
        col = ctx.start.column

        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            if '.' in text:
                return NumberLiteral(line=line, column=col, value=float(text))
            return NumberLiteral(line=line, column=col, value=int(text))

        if ctx.STRING():
            text = ctx.STRING().getText()
            raw = text[1:-1]
            # 解析转义序列
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
        if ctx.K_SELF():
            return SelfReference(line=line, column=col)

        if ctx.ID():
            name = ctx.ID().getText()
            # 检查是否为中文数字
            cn_value = self._is_chinese_number(name)
            if cn_value is not None:
                if isinstance(cn_value, float):
                    return NumberLiteral(line=line, column=col, value=cn_value)
                return NumberLiteral(line=line, column=col, value=cn_value)
            return Identifier(line=line, column=col, name=name)

        return None

    def visitExprList(self, ctx: DuanLangParser.ExprListContext):
        """表达式列表"""
        return [self.visitExpr(e) for e in ctx.expr()]

    def _parse_string_interpolation(self, raw: str, line: int, col: int):
        """检测字符串中是否包含 {表达式} 插值，若有则返回StringInterpolation节点"""
        import re
        # 匹配 {expr} 模式（非转义的 { }）
        # 先检查是否有未转义的 {
        has_interpolation = False
        i = 0
        while i < len(raw):
            if raw[i] == '\\' and i + 1 < len(raw):
                i += 2  # 跳过转义字符
                continue
            if raw[i] == '{':
                has_interpolation = True
                break
            i += 1

        if not has_interpolation:
            return None

        # 拆分为交替的字符串片段和表达式
        parts = []
        current_str = []
        i = 0
        while i < len(raw):
            if raw[i] == '\\' and i + 1 < len(raw):
                nxt = raw[i + 1]
                if nxt == 'n':
                    current_str.append('\n')
                elif nxt == 't':
                    current_str.append('\t')
                elif nxt == 'r':
                    current_str.append('\r')
                elif nxt == '\\':
                    current_str.append('\\')
                elif nxt == '{':
                    current_str.append('{')
                elif nxt == '}':
                    current_str.append('}')
                else:
                    current_str.append(raw[i])
                    current_str.append(nxt)
                i += 2
                continue
            if raw[i] == '{':
                # 保存前面的字符串部分
                if current_str:
                    parts.append(''.join(current_str))
                    current_str = []
                # 找到匹配的 }
                j = i + 1
                depth = 1
                while j < len(raw) and depth > 0:
                    if raw[j] == '{':
                        depth += 1
                    elif raw[j] == '}':
                        depth -= 1
                    j += 1
                if depth == 0:
                    expr_text = raw[i+1:j-1].strip()
                    # 解析插值表达式
                    try:
                        expr_ast = self._parse_interpolation_expr(expr_text, line, col)
                        parts.append(expr_ast)
                    except Exception:
                        # 如果解析失败，当作普通文本
                        parts.append('{' + expr_text + '}')
                    i = j
                else:
                    current_str.append(raw[i])
                    i += 1
            else:
                current_str.append(raw[i])
                i += 1

        # 保存最后的字符串部分
        if current_str:
            parts.append(''.join(current_str))

        return StringInterpolation(line=line, column=col, parts=parts)

    def _parse_interpolation_expr(self, expr_text: str, line: int, col: int):
        """解析字符串插值中的表达式文本为AST节点"""
        # 使用ANTLR解析器解析表达式
        from duan_tokenizer import create_antlr_token_stream
        from DuanLangLexer import DuanLangLexer
        from DuanLangParser import DuanLangParser

        token_stream = create_antlr_token_stream(expr_text, DuanLangLexer)
        parser = DuanLangParser(token_stream)
        parser.removeErrorListeners()
        tree = parser.expr()
        return self.visitExpr(tree)

    def visitListComprehension(self, ctx: DuanLangParser.ListComprehensionContext):
        """列表推导：[表达式 遍历 变量 之 列表]"""
        line = ctx.start.line
        col = ctx.start.column
        expression = self.visitExpr(ctx.expr(0))  # 第一个expr是输出表达式
        variable = self._get_identifier_like_name(ctx.identifier_like())
        iterable = self.visitExpr(ctx.expr(1))  # 第二个expr是可迭代对象
        condition = None
        if ctx.K_IF():
            condition = self.visitExpr(ctx.expr(2))  # 第三个expr是条件（如果有）
        return ListComprehension(line=line, column=col,
                                 expression=expression, variable=variable,
                                 iterable=iterable, condition=condition)

    def visitLambdaExpr(self, ctx: DuanLangParser.LambdaExprContext):
        """匿名函数：接收 甲：返回 甲 乘 甲。"""
        line = ctx.start.line
        col = ctx.start.column
        params = []
        if ctx.paramList():
            params = self.visitParamList(ctx.paramList())
        # 函数体：如果有 返回 关键字则取expr，否则取expr
        body_expr = self.visitExpr(ctx.expr()) if ctx.expr() else None
        return LambdaExpression(line=line, column=col, parameters=params, body=body_expr)

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
        """解析源代码为 AST（使用自定义中文分词器 + ANTLR 解析器）"""
        # ANTLR Parser 已原生支持列表推导、匿名函数、模式匹配
        # 不再需要预处理转换

        # 使用自定义中文分词器
        token_stream = create_antlr_token_stream(source, DuanLangLexer)
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

    def _preprocess_source(self, source: str) -> str:
        """预处理源代码：将新语法转换为ANTLR可解析的等效语法

        转换规则：
        1. 列表推导 [expr 遍历 var 之 list] → __列表推导__(expr, var, list)
        2. 匿名函数 接收 x：返回 expr。 → __匿名函数__(x, expr)
        3. 模式匹配 匹配 val：情况 ... 结束。 → __模式匹配__(val, ...)
        """
        import re

        # 1. 处理模式匹配
        source = self._preprocess_match(source)

        # 2. 处理列表推导
        source = self._preprocess_list_comprehension(source)

        # 3. 处理匿名函数
        source = self._preprocess_lambda(source)

        return source

    def _preprocess_match(self, source: str) -> str:
        """预处理模式匹配语句

        匹配 值：
          情况 1：打印("一")。
          情况 2：打印("二")。
          情况 _：打印("其他")。
        结束。

        转换为：
        设 __匹配值__ 为 值。
        如果 __匹配值__ 等于 1：打印("一")。
        否则若 __匹配值__ 等于 2：打印("二")。
        否则：打印("其他")。
        结束。
        """
        import re
        # 匹配 "匹配" 开始，到 "结束。" 为止的块
        pattern = re.compile(
            r'匹配\s+(.+?)\s*[：:]\s*\n(.*?)\n\s*结束[。.]?',
            re.DOTALL
        )

        def replace_match(m):
            subject = m.group(1).strip()
            body = m.group(2).strip()
            var_name = '__匹配值__'

            # 解析情况分支
            case_pattern = re.compile(
                r'情况\s+(.+?)\s*[：:]\s*(.*?)(?=\n\s*情况|\s*$)',
                re.DOTALL
            )
            cases = case_pattern.findall(body)

            if not cases:
                return m.group(0)  # 无法解析，保持原样

            lines = [f'设 {var_name} 为 {subject}。']
            first = True
            for pattern_val, case_body in cases:
                pattern_val = pattern_val.strip()
                case_body = case_body.strip().rstrip('。').rstrip('.')
                if pattern_val == '_':
                    # 通配符 -> else
                    lines.append(f'否则：{case_body}。')
                elif first:
                    lines.append(f'如果 {var_name} 等于 {pattern_val}：{case_body}。')
                    first = False
                else:
                    lines.append(f'否则若 {var_name} 等于 {pattern_val}：{case_body}。')
            lines.append('结束。')
            return '\n'.join(lines)

        return pattern.sub(replace_match, source)

    def _preprocess_list_comprehension(self, source: str) -> str:
        """预处理列表推导

        [表达式 遍历 变量 之 列表]
        [表达式 遍历 变量 之 列表 如果 条件]

        转换为：
        __列表推导__(表达式, 变量, 列表)
        __列表推导筛选__(表达式, 变量, 列表, 条件)
        """
        import re
        # 匹配 [expr 遍历 var 之 iterable] 或 [... 遍历 var 之 iterable 如果 cond]
        pattern = re.compile(
            r'\[\s*(.+?)\s+遍历\s+(\S+)\s+之\s+(.+?)(?:\s+如果\s+(.+?))?\s*\]'
        )

        def replace_comp(m):
            expr = m.group(1).strip()
            var = m.group(2).strip()
            iterable = m.group(3).strip()
            condition = m.group(4)
            if condition:
                condition = condition.strip()
                return f'__列表推导筛选__({iterable}, 接收 {var}：返回 {expr}。, 接收 {var}：返回 {condition}。)'
            return f'__列表推导__({iterable}, 接收 {var}：返回 {expr}。)'

        return pattern.sub(replace_comp, source)

    def _preprocess_lambda(self, source: str) -> str:
        """预处理匿名函数

        接收 参数列表：返回 表达式。
        接收 x, y：返回 x 加 y。

        注意：只有当"接收"出现在表达式位置时才转换
        （段落定义中也有"接收"，但后面跟的是参数声明不是冒号）

        转换为：__匿名函数__(参数列表, 表达式)
        """
        import re
        # 匹配 接收 params：返回 expr。 或 接收 params：expr。
        # 注意：段落定义中 "段落 名称 接收 参数：" 后面是代码块不是单行表达式
        # 匿名函数的特点是 接收 后面直接跟参数名和冒号，且冒号后是单行表达式
        # 安全策略：只匹配括号内或赋值值中的匿名函数
        pattern = re.compile(
            r'接收\s+([^：:]+?)\s*[：:]\s*返回?\s*(.+?)[。.]'
        )

        def replace_lambda(m):
            params = m.group(1).strip()
            body = m.group(2).strip()
            return f'__匿名函数__({params}, {body})'

        return pattern.sub(replace_lambda, source)

    def _postprocess_ast(self, module: Module) -> Module:
        """后处理AST：将预处理标记还原为真实AST节点"""
        # 处理 __列表推导__、__列表推导筛选__、__匿名函数__ 函数调用
        # 转换为 ListComprehension / LambdaExpression AST 节点
        new_stmts = []
        for stmt in module.statements:
            result = self._transform_stmt(stmt)
            if result is not None:
                new_stmts.append(result)
            else:
                new_stmts.append(stmt)
        module.statements = new_stmts

        # 处理段落体中的语句
        for seg in module.segments:
            new_body = []
            for stmt in seg.body:
                result = self._transform_stmt(stmt)
                new_body.append(result if result else stmt)
            seg.body = new_body

        return module

    def _transform_stmt(self, stmt):
        """转换单个语句中的预处理标记"""
        # 处理表达式语句中的函数调用
        if isinstance(stmt, ExpressionStatement):
            expr = self._transform_expr(stmt.expression)
            if expr is not None:
                stmt.expression = expr
                return stmt

        # 处理变量声明
        if isinstance(stmt, VariableDeclaration):
            expr = self._transform_expr(stmt.value)
            if expr is not None:
                stmt.value = expr
                return stmt

        # 处理赋值
        if isinstance(stmt, Assignment):
            expr = self._transform_expr(stmt.value)
            if expr is not None:
                stmt.value = expr
                return stmt

        # 处理打印
        if isinstance(stmt, PrintStatement):
            expr = self._transform_expr(stmt.value)
            if expr is not None:
                stmt.value = expr
                return stmt

        # 处理返回
        if isinstance(stmt, ReturnStatement) and stmt.value:
            expr = self._transform_expr(stmt.value)
            if expr is not None:
                stmt.value = expr
                return stmt

        return None

    def _transform_expr(self, expr):
        """转换表达式中的预处理标记"""
        if expr is None:
            return None

        # 检查是否是 __列表推导__ 或 __列表推导筛选__ 函数调用
        if isinstance(expr, FunctionCall):
            func_name = None
            if isinstance(expr.name, Identifier):
                func_name = expr.name.name

            if func_name == '__列表推导__':
                # __列表推导__(iterable, lambda)
                if len(expr.arguments) >= 2:
                    iterable = expr.arguments[0]
                    lambda_expr = expr.arguments[1]
                    if isinstance(lambda_expr, FunctionCall) and isinstance(lambda_expr.name, Identifier) and lambda_expr.name.name == '__匿名函数__':
                        return self._build_list_comprehension(lambda_expr, iterable, None)
                    # 如果lambda_expr本身已经是LambdaExpression
                    if isinstance(lambda_expr, LambdaExpression):
                        var = lambda_expr.parameters[0].name if lambda_expr.parameters else '当前项'
                        return ListComprehension(
                            line=expr.line, column=expr.column,
                            expression=lambda_expr.body, variable=var,
                            iterable=iterable, condition=None
                        )

            elif func_name == '__列表推导筛选__':
                # __列表推导筛选__(iterable, lambda, cond_lambda)
                if len(expr.arguments) >= 3:
                    iterable = expr.arguments[0]
                    lambda_expr = expr.arguments[1]
                    cond_lambda = expr.arguments[2]
                    var = '当前项'
                    body_expr = lambda_expr
                    cond_expr = cond_lambda
                    if isinstance(lambda_expr, FunctionCall) and isinstance(lambda_expr.name, Identifier) and lambda_expr.name.name == '__匿名函数__':
                        result = self._build_list_comprehension(lambda_expr, iterable, cond_lambda)
                        return result
                    if isinstance(lambda_expr, LambdaExpression):
                        var = lambda_expr.parameters[0].name if lambda_expr.parameters else '当前项'
                        body_expr = lambda_expr.body
                        cond_expr = cond_lambda.body if isinstance(cond_lambda, LambdaExpression) else cond_lambda
                        return ListComprehension(
                            line=expr.line, column=expr.column,
                            expression=body_expr, variable=var,
                            iterable=iterable, condition=cond_expr
                        )

            elif func_name == '__匿名函数__':
                return self._build_lambda(expr)

            # 递归处理函数参数
            new_args = []
            changed = False
            for arg in expr.arguments:
                transformed = self._transform_expr(arg)
                if transformed is not None:
                    new_args.append(transformed)
                    changed = True
                else:
                    new_args.append(arg)
            if changed:
                expr.arguments = new_args
                return expr

        # 递归处理二元运算
        if isinstance(expr, BinaryOp):
            left = self._transform_expr(expr.left)
            right = self._transform_expr(expr.right)
            if left is not None:
                expr.left = left
            if right is not None:
                expr.right = right
            if left is not None or right is not None:
                return expr

        # 递归处理列表字面量
        if isinstance(expr, ListLiteral):
            new_elements = []
            changed = False
            for e in expr.elements:
                transformed = self._transform_expr(e)
                if transformed is not None:
                    new_elements.append(transformed)
                    changed = True
                else:
                    new_elements.append(e)
            if changed:
                expr.elements = new_elements
                return expr

        return None

    def _build_list_comprehension(self, lambda_call: FunctionCall, iterable, cond_lambda=None):
        """从 __匿名函数__ 调用构建 ListComprehension"""
        if len(lambda_call.arguments) >= 2:
            # 参数1是参数名（ID），参数2是表达式
            params = []
            first_arg = lambda_call.arguments[0]
            if isinstance(first_arg, Identifier):
                var = first_arg.name
            else:
                var = str(first_arg)
            body_expr = lambda_call.arguments[1]
            condition = None
            if cond_lambda:
                if isinstance(cond_lambda, FunctionCall) and isinstance(cond_lambda.name, Identifier) and cond_lambda.name.name == '__匿名函数__':
                    condition = cond_lambda.arguments[1] if len(cond_lambda.arguments) >= 2 else None
                elif isinstance(cond_lambda, LambdaExpression):
                    condition = cond_lambda.body
                else:
                    condition = cond_lambda
            return ListComprehension(
                line=lambda_call.line, column=lambda_call.column,
                expression=body_expr, variable=var,
                iterable=iterable, condition=condition
            )
        return None

    def _build_lambda(self, func_call: FunctionCall):
        """从 __匿名函数__ 调用构建 LambdaExpression"""
        from duan_ast import Parameter
        if len(func_call.arguments) >= 2:
            # 参数列表：可能是单个ID或逗号分隔的多个ID
            params = []
            first_arg = func_call.arguments[0]
            if isinstance(first_arg, Identifier):
                params.append(Parameter(line=first_arg.line, column=first_arg.column, name=first_arg.name))
            elif isinstance(first_arg, FunctionCall):
                # 多个参数被解析为函数调用
                for arg in first_arg.arguments:
                    if isinstance(arg, Identifier):
                        params.append(Parameter(line=arg.line, column=arg.column, name=arg.name))
            body = func_call.arguments[1]
            return LambdaExpression(
                line=func_call.line, column=func_call.column,
                parameters=params, body=body
            )
        return None


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