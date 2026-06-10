# Generated from g:/dumategithub/duan/antlrparser/DuanLangParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DuanLangParser import DuanLangParser
else:
    from DuanLangParser import DuanLangParser

from typing import List, Optional, Tuple, Any, Union


# This class defines a complete generic visitor for a parse tree produced by DuanLangParser.

class DuanLangParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DuanLangParser#program.
    def visitProgram(self, ctx:DuanLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#moduleDecl.
    def visitModuleDecl(self, ctx:DuanLangParser.ModuleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#definition.
    def visitDefinition(self, ctx:DuanLangParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#paragraphDef.
    def visitParagraphDef(self, ctx:DuanLangParser.ParagraphDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#paramList.
    def visitParamList(self, ctx:DuanLangParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#param.
    def visitParam(self, ctx:DuanLangParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#block.
    def visitBlock(self, ctx:DuanLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#dataTypeDef.
    def visitDataTypeDef(self, ctx:DuanLangParser.DataTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#dataTypeField.
    def visitDataTypeField(self, ctx:DuanLangParser.DataTypeFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#errorTypeDef.
    def visitErrorTypeDef(self, ctx:DuanLangParser.ErrorTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#importStmt.
    def visitImportStmt(self, ctx:DuanLangParser.ImportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#exportStmt.
    def visitExportStmt(self, ctx:DuanLangParser.ExportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#path.
    def visitPath(self, ctx:DuanLangParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#importList.
    def visitImportList(self, ctx:DuanLangParser.ImportListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#importItem.
    def visitImportItem(self, ctx:DuanLangParser.ImportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#stmt.
    def visitStmt(self, ctx:DuanLangParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#varDecl.
    def visitVarDecl(self, ctx:DuanLangParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#assignStmt.
    def visitAssignStmt(self, ctx:DuanLangParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#target.
    def visitTarget(self, ctx:DuanLangParser.TargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#ifStmt.
    def visitIfStmt(self, ctx:DuanLangParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#foreachStmt.
    def visitForeachStmt(self, ctx:DuanLangParser.ForeachStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#foreachVar.
    def visitForeachVar(self, ctx:DuanLangParser.ForeachVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#whileStmt.
    def visitWhileStmt(self, ctx:DuanLangParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#returnStmt.
    def visitReturnStmt(self, ctx:DuanLangParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#breakStmt.
    def visitBreakStmt(self, ctx:DuanLangParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#continueStmt.
    def visitContinueStmt(self, ctx:DuanLangParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#tryStmt.
    def visitTryStmt(self, ctx:DuanLangParser.TryStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#throwStmt.
    def visitThrowStmt(self, ctx:DuanLangParser.ThrowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#printStmt.
    def visitPrintStmt(self, ctx:DuanLangParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#exprStmt.
    def visitExprStmt(self, ctx:DuanLangParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#expr.
    def visitExpr(self, ctx:DuanLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#pipelineExpr.
    def visitPipelineExpr(self, ctx:DuanLangParser.PipelineExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#andExpr.
    def visitAndExpr(self, ctx:DuanLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#orExpr.
    def visitOrExpr(self, ctx:DuanLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#comparisonExpr.
    def visitComparisonExpr(self, ctx:DuanLangParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#compOp.
    def visitCompOp(self, ctx:DuanLangParser.CompOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:DuanLangParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#addOp.
    def visitAddOp(self, ctx:DuanLangParser.AddOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:DuanLangParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#multOp.
    def visitMultOp(self, ctx:DuanLangParser.MultOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#unaryExpr.
    def visitUnaryExpr(self, ctx:DuanLangParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#postfixExpr.
    def visitPostfixExpr(self, ctx:DuanLangParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#primary.
    def visitPrimary(self, ctx:DuanLangParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#typeAnnotation.
    def visitTypeAnnotation(self, ctx:DuanLangParser.TypeAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#builtinType.
    def visitBuiltinType(self, ctx:DuanLangParser.BuiltinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DuanLangParser#exprList.
    def visitExprList(self, ctx:DuanLangParser.ExprListContext):
        return self.visitChildren(ctx)



del DuanLangParser