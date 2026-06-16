# Generated from DuanLangParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DuanLangParser import DuanLangParser
else:
    from DuanLangParser import DuanLangParser

from typing import List, Optional, Tuple, Any, Union


# This class defines a complete listener for a parse tree produced by DuanLangParser.
class DuanLangParserListener(ParseTreeListener):

    # Enter a parse tree produced by DuanLangParser#program.
    def enterProgram(self, ctx:DuanLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by DuanLangParser#program.
    def exitProgram(self, ctx:DuanLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by DuanLangParser#moduleDecl.
    def enterModuleDecl(self, ctx:DuanLangParser.ModuleDeclContext):
        pass

    # Exit a parse tree produced by DuanLangParser#moduleDecl.
    def exitModuleDecl(self, ctx:DuanLangParser.ModuleDeclContext):
        pass


    # Enter a parse tree produced by DuanLangParser#definition.
    def enterDefinition(self, ctx:DuanLangParser.DefinitionContext):
        pass

    # Exit a parse tree produced by DuanLangParser#definition.
    def exitDefinition(self, ctx:DuanLangParser.DefinitionContext):
        pass


    # Enter a parse tree produced by DuanLangParser#paragraphDef.
    def enterParagraphDef(self, ctx:DuanLangParser.ParagraphDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#paragraphDef.
    def exitParagraphDef(self, ctx:DuanLangParser.ParagraphDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#classDef.
    def enterClassDef(self, ctx:DuanLangParser.ClassDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#classDef.
    def exitClassDef(self, ctx:DuanLangParser.ClassDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#genericParams.
    def enterGenericParams(self, ctx:DuanLangParser.GenericParamsContext):
        pass

    # Exit a parse tree produced by DuanLangParser#genericParams.
    def exitGenericParams(self, ctx:DuanLangParser.GenericParamsContext):
        pass


    # Enter a parse tree produced by DuanLangParser#classMember.
    def enterClassMember(self, ctx:DuanLangParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by DuanLangParser#classMember.
    def exitClassMember(self, ctx:DuanLangParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by DuanLangParser#methodDef.
    def enterMethodDef(self, ctx:DuanLangParser.MethodDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#methodDef.
    def exitMethodDef(self, ctx:DuanLangParser.MethodDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#constructorDef.
    def enterConstructorDef(self, ctx:DuanLangParser.ConstructorDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#constructorDef.
    def exitConstructorDef(self, ctx:DuanLangParser.ConstructorDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#attributeDecl.
    def enterAttributeDecl(self, ctx:DuanLangParser.AttributeDeclContext):
        pass

    # Exit a parse tree produced by DuanLangParser#attributeDecl.
    def exitAttributeDecl(self, ctx:DuanLangParser.AttributeDeclContext):
        pass


    # Enter a parse tree produced by DuanLangParser#interfaceDef.
    def enterInterfaceDef(self, ctx:DuanLangParser.InterfaceDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#interfaceDef.
    def exitInterfaceDef(self, ctx:DuanLangParser.InterfaceDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#interfaceMember.
    def enterInterfaceMember(self, ctx:DuanLangParser.InterfaceMemberContext):
        pass

    # Exit a parse tree produced by DuanLangParser#interfaceMember.
    def exitInterfaceMember(self, ctx:DuanLangParser.InterfaceMemberContext):
        pass


    # Enter a parse tree produced by DuanLangParser#paramList.
    def enterParamList(self, ctx:DuanLangParser.ParamListContext):
        pass

    # Exit a parse tree produced by DuanLangParser#paramList.
    def exitParamList(self, ctx:DuanLangParser.ParamListContext):
        pass


    # Enter a parse tree produced by DuanLangParser#param.
    def enterParam(self, ctx:DuanLangParser.ParamContext):
        pass

    # Exit a parse tree produced by DuanLangParser#param.
    def exitParam(self, ctx:DuanLangParser.ParamContext):
        pass


    # Enter a parse tree produced by DuanLangParser#block.
    def enterBlock(self, ctx:DuanLangParser.BlockContext):
        pass

    # Exit a parse tree produced by DuanLangParser#block.
    def exitBlock(self, ctx:DuanLangParser.BlockContext):
        pass


    # Enter a parse tree produced by DuanLangParser#dataTypeDef.
    def enterDataTypeDef(self, ctx:DuanLangParser.DataTypeDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#dataTypeDef.
    def exitDataTypeDef(self, ctx:DuanLangParser.DataTypeDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#dataTypeField.
    def enterDataTypeField(self, ctx:DuanLangParser.DataTypeFieldContext):
        pass

    # Exit a parse tree produced by DuanLangParser#dataTypeField.
    def exitDataTypeField(self, ctx:DuanLangParser.DataTypeFieldContext):
        pass


    # Enter a parse tree produced by DuanLangParser#errorTypeDef.
    def enterErrorTypeDef(self, ctx:DuanLangParser.ErrorTypeDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#errorTypeDef.
    def exitErrorTypeDef(self, ctx:DuanLangParser.ErrorTypeDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#importStmt.
    def enterImportStmt(self, ctx:DuanLangParser.ImportStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#importStmt.
    def exitImportStmt(self, ctx:DuanLangParser.ImportStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#exportStmt.
    def enterExportStmt(self, ctx:DuanLangParser.ExportStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#exportStmt.
    def exitExportStmt(self, ctx:DuanLangParser.ExportStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#path.
    def enterPath(self, ctx:DuanLangParser.PathContext):
        pass

    # Exit a parse tree produced by DuanLangParser#path.
    def exitPath(self, ctx:DuanLangParser.PathContext):
        pass


    # Enter a parse tree produced by DuanLangParser#importList.
    def enterImportList(self, ctx:DuanLangParser.ImportListContext):
        pass

    # Exit a parse tree produced by DuanLangParser#importList.
    def exitImportList(self, ctx:DuanLangParser.ImportListContext):
        pass


    # Enter a parse tree produced by DuanLangParser#importItem.
    def enterImportItem(self, ctx:DuanLangParser.ImportItemContext):
        pass

    # Exit a parse tree produced by DuanLangParser#importItem.
    def exitImportItem(self, ctx:DuanLangParser.ImportItemContext):
        pass


    # Enter a parse tree produced by DuanLangParser#stmt.
    def enterStmt(self, ctx:DuanLangParser.StmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#stmt.
    def exitStmt(self, ctx:DuanLangParser.StmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#varDecl.
    def enterVarDecl(self, ctx:DuanLangParser.VarDeclContext):
        pass

    # Exit a parse tree produced by DuanLangParser#varDecl.
    def exitVarDecl(self, ctx:DuanLangParser.VarDeclContext):
        pass


    # Enter a parse tree produced by DuanLangParser#assignStmt.
    def enterAssignStmt(self, ctx:DuanLangParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#assignStmt.
    def exitAssignStmt(self, ctx:DuanLangParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#target.
    def enterTarget(self, ctx:DuanLangParser.TargetContext):
        pass

    # Exit a parse tree produced by DuanLangParser#target.
    def exitTarget(self, ctx:DuanLangParser.TargetContext):
        pass


    # Enter a parse tree produced by DuanLangParser#ifStmt.
    def enterIfStmt(self, ctx:DuanLangParser.IfStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#ifStmt.
    def exitIfStmt(self, ctx:DuanLangParser.IfStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#foreachStmt.
    def enterForeachStmt(self, ctx:DuanLangParser.ForeachStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#foreachStmt.
    def exitForeachStmt(self, ctx:DuanLangParser.ForeachStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#foreachVar.
    def enterForeachVar(self, ctx:DuanLangParser.ForeachVarContext):
        pass

    # Exit a parse tree produced by DuanLangParser#foreachVar.
    def exitForeachVar(self, ctx:DuanLangParser.ForeachVarContext):
        pass


    # Enter a parse tree produced by DuanLangParser#whileStmt.
    def enterWhileStmt(self, ctx:DuanLangParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#whileStmt.
    def exitWhileStmt(self, ctx:DuanLangParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#returnStmt.
    def enterReturnStmt(self, ctx:DuanLangParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#returnStmt.
    def exitReturnStmt(self, ctx:DuanLangParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#breakStmt.
    def enterBreakStmt(self, ctx:DuanLangParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#breakStmt.
    def exitBreakStmt(self, ctx:DuanLangParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#continueStmt.
    def enterContinueStmt(self, ctx:DuanLangParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#continueStmt.
    def exitContinueStmt(self, ctx:DuanLangParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#tryStmt.
    def enterTryStmt(self, ctx:DuanLangParser.TryStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#tryStmt.
    def exitTryStmt(self, ctx:DuanLangParser.TryStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#throwStmt.
    def enterThrowStmt(self, ctx:DuanLangParser.ThrowStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#throwStmt.
    def exitThrowStmt(self, ctx:DuanLangParser.ThrowStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#matchStmt.
    def enterMatchStmt(self, ctx:DuanLangParser.MatchStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#matchStmt.
    def exitMatchStmt(self, ctx:DuanLangParser.MatchStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#matchCase.
    def enterMatchCase(self, ctx:DuanLangParser.MatchCaseContext):
        pass

    # Exit a parse tree produced by DuanLangParser#matchCase.
    def exitMatchCase(self, ctx:DuanLangParser.MatchCaseContext):
        pass


    # Enter a parse tree produced by DuanLangParser#matchPattern.
    def enterMatchPattern(self, ctx:DuanLangParser.MatchPatternContext):
        pass

    # Exit a parse tree produced by DuanLangParser#matchPattern.
    def exitMatchPattern(self, ctx:DuanLangParser.MatchPatternContext):
        pass


    # Enter a parse tree produced by DuanLangParser#matchPatternList.
    def enterMatchPatternList(self, ctx:DuanLangParser.MatchPatternListContext):
        pass

    # Exit a parse tree produced by DuanLangParser#matchPatternList.
    def exitMatchPatternList(self, ctx:DuanLangParser.MatchPatternListContext):
        pass


    # Enter a parse tree produced by DuanLangParser#printStmt.
    def enterPrintStmt(self, ctx:DuanLangParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#printStmt.
    def exitPrintStmt(self, ctx:DuanLangParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#withStmt.
    def enterWithStmt(self, ctx:DuanLangParser.WithStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#withStmt.
    def exitWithStmt(self, ctx:DuanLangParser.WithStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#decoratorDef.
    def enterDecoratorDef(self, ctx:DuanLangParser.DecoratorDefContext):
        pass

    # Exit a parse tree produced by DuanLangParser#decoratorDef.
    def exitDecoratorDef(self, ctx:DuanLangParser.DecoratorDefContext):
        pass


    # Enter a parse tree produced by DuanLangParser#exprStmt.
    def enterExprStmt(self, ctx:DuanLangParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by DuanLangParser#exprStmt.
    def exitExprStmt(self, ctx:DuanLangParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by DuanLangParser#expr.
    def enterExpr(self, ctx:DuanLangParser.ExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#expr.
    def exitExpr(self, ctx:DuanLangParser.ExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#pipelineExpr.
    def enterPipelineExpr(self, ctx:DuanLangParser.PipelineExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#pipelineExpr.
    def exitPipelineExpr(self, ctx:DuanLangParser.PipelineExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#andExpr.
    def enterAndExpr(self, ctx:DuanLangParser.AndExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#andExpr.
    def exitAndExpr(self, ctx:DuanLangParser.AndExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#orExpr.
    def enterOrExpr(self, ctx:DuanLangParser.OrExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#orExpr.
    def exitOrExpr(self, ctx:DuanLangParser.OrExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#comparisonExpr.
    def enterComparisonExpr(self, ctx:DuanLangParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#comparisonExpr.
    def exitComparisonExpr(self, ctx:DuanLangParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#compOp.
    def enterCompOp(self, ctx:DuanLangParser.CompOpContext):
        pass

    # Exit a parse tree produced by DuanLangParser#compOp.
    def exitCompOp(self, ctx:DuanLangParser.CompOpContext):
        pass


    # Enter a parse tree produced by DuanLangParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:DuanLangParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:DuanLangParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#addOp.
    def enterAddOp(self, ctx:DuanLangParser.AddOpContext):
        pass

    # Exit a parse tree produced by DuanLangParser#addOp.
    def exitAddOp(self, ctx:DuanLangParser.AddOpContext):
        pass


    # Enter a parse tree produced by DuanLangParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:DuanLangParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:DuanLangParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#multOp.
    def enterMultOp(self, ctx:DuanLangParser.MultOpContext):
        pass

    # Exit a parse tree produced by DuanLangParser#multOp.
    def exitMultOp(self, ctx:DuanLangParser.MultOpContext):
        pass


    # Enter a parse tree produced by DuanLangParser#unaryExpr.
    def enterUnaryExpr(self, ctx:DuanLangParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#unaryExpr.
    def exitUnaryExpr(self, ctx:DuanLangParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#postfixExpr.
    def enterPostfixExpr(self, ctx:DuanLangParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#postfixExpr.
    def exitPostfixExpr(self, ctx:DuanLangParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#primary.
    def enterPrimary(self, ctx:DuanLangParser.PrimaryContext):
        pass

    # Exit a parse tree produced by DuanLangParser#primary.
    def exitPrimary(self, ctx:DuanLangParser.PrimaryContext):
        pass


    # Enter a parse tree produced by DuanLangParser#implicitCall.
    def enterImplicitCall(self, ctx:DuanLangParser.ImplicitCallContext):
        pass

    # Exit a parse tree produced by DuanLangParser#implicitCall.
    def exitImplicitCall(self, ctx:DuanLangParser.ImplicitCallContext):
        pass


    # Enter a parse tree produced by DuanLangParser#implicitArg.
    def enterImplicitArg(self, ctx:DuanLangParser.ImplicitArgContext):
        pass

    # Exit a parse tree produced by DuanLangParser#implicitArg.
    def exitImplicitArg(self, ctx:DuanLangParser.ImplicitArgContext):
        pass


    # Enter a parse tree produced by DuanLangParser#dictLiteral.
    def enterDictLiteral(self, ctx:DuanLangParser.DictLiteralContext):
        pass

    # Exit a parse tree produced by DuanLangParser#dictLiteral.
    def exitDictLiteral(self, ctx:DuanLangParser.DictLiteralContext):
        pass


    # Enter a parse tree produced by DuanLangParser#dictEntry.
    def enterDictEntry(self, ctx:DuanLangParser.DictEntryContext):
        pass

    # Exit a parse tree produced by DuanLangParser#dictEntry.
    def exitDictEntry(self, ctx:DuanLangParser.DictEntryContext):
        pass


    # Enter a parse tree produced by DuanLangParser#listComprehension.
    def enterListComprehension(self, ctx:DuanLangParser.ListComprehensionContext):
        pass

    # Exit a parse tree produced by DuanLangParser#listComprehension.
    def exitListComprehension(self, ctx:DuanLangParser.ListComprehensionContext):
        pass


    # Enter a parse tree produced by DuanLangParser#identifier_like.
    def enterIdentifier_like(self, ctx:DuanLangParser.Identifier_likeContext):
        pass

    # Exit a parse tree produced by DuanLangParser#identifier_like.
    def exitIdentifier_like(self, ctx:DuanLangParser.Identifier_likeContext):
        pass


    # Enter a parse tree produced by DuanLangParser#typeAsIdentifier.
    def enterTypeAsIdentifier(self, ctx:DuanLangParser.TypeAsIdentifierContext):
        pass

    # Exit a parse tree produced by DuanLangParser#typeAsIdentifier.
    def exitTypeAsIdentifier(self, ctx:DuanLangParser.TypeAsIdentifierContext):
        pass


    # Enter a parse tree produced by DuanLangParser#lambdaExpr.
    def enterLambdaExpr(self, ctx:DuanLangParser.LambdaExprContext):
        pass

    # Exit a parse tree produced by DuanLangParser#lambdaExpr.
    def exitLambdaExpr(self, ctx:DuanLangParser.LambdaExprContext):
        pass


    # Enter a parse tree produced by DuanLangParser#dictComprehension.
    def enterDictComprehension(self, ctx:DuanLangParser.DictComprehensionContext):
        pass

    # Exit a parse tree produced by DuanLangParser#dictComprehension.
    def exitDictComprehension(self, ctx:DuanLangParser.DictComprehensionContext):
        pass


    # Enter a parse tree produced by DuanLangParser#typeAnnotation.
    def enterTypeAnnotation(self, ctx:DuanLangParser.TypeAnnotationContext):
        pass

    # Exit a parse tree produced by DuanLangParser#typeAnnotation.
    def exitTypeAnnotation(self, ctx:DuanLangParser.TypeAnnotationContext):
        pass


    # Enter a parse tree produced by DuanLangParser#builtinType.
    def enterBuiltinType(self, ctx:DuanLangParser.BuiltinTypeContext):
        pass

    # Exit a parse tree produced by DuanLangParser#builtinType.
    def exitBuiltinType(self, ctx:DuanLangParser.BuiltinTypeContext):
        pass


    # Enter a parse tree produced by DuanLangParser#exprList.
    def enterExprList(self, ctx:DuanLangParser.ExprListContext):
        pass

    # Exit a parse tree produced by DuanLangParser#exprList.
    def exitExprList(self, ctx:DuanLangParser.ExprListContext):
        pass



del DuanLangParser