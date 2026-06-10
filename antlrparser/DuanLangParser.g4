/*
 * 段言（Duan）编程语言 ANTLR4 语法定义
 *
 * 版本: v1.0
 * 独立的 Parser 语法，配合 DuanLangLexer 使用
 */

parser grammar DuanLangParser;

options { tokenVocab = DuanLangLexer; }

@header {
from typing import List, Optional, Tuple, Any, Union
}


// ================================================================
// PARSER RULES
// ================================================================

// ----- 程序入口 -----

program
    : ( moduleDecl
      | importStmt
      | exportStmt
      | definition
      | stmt
      )* EOF
    ;

moduleDecl
    : LBRACKET ID RBRACKET
    ;

definition
    : paragraphDef
    | dataTypeDef
    | errorTypeDef
    ;

// ----- 段落定义 -----

paragraphDef
    : BOOK_L ID BOOK_R K_SEGMENT
      LPAREN paramList? RPAREN
      ( PIPE typeAnnotation )?
      COLON
      block
      K_END DOT?
    ;

paramList
    : param ( COMMA param )*
    ;

param
    : ID ( COLON typeAnnotation )? ( K_EQUAL expr )?
    ;

block
    : stmt*
    ;

// ----- 类型定义 -----

dataTypeDef
    : BOOK_L ID BOOK_R K_DATA_TYPE COLON
      dataTypeField+
      K_END DOT?
    ;

dataTypeField
    : ID COLON typeAnnotation DOT?
    ;

errorTypeDef
    : BOOK_L ID BOOK_R K_ERROR_TYPE COLON
      dataTypeField+
      K_END DOT?
    ;

// ----- 导入/导出 -----

importStmt
    : K_FROM path K_IMPORT importList DOT?
    | K_IMPORT importList DOT?
    ;

exportStmt
    : K_EXPORT ( ID | BOOK_L ID BOOK_R ) DOT?
    ;

path
    : ID ( PATH_SEP ID )*
    ;

importList
    : importItem ( COMMA importItem )*
    ;

importItem
    : BOOK_L ID BOOK_R
    | ID
    ;

// ----- 语句 -----

stmt
    : varDecl
    | assignStmt
    | ifStmt
    | foreachStmt
    | whileStmt
    | returnStmt
    | breakStmt
    | continueStmt
    | tryStmt
    | throwStmt
    | printStmt
    | exprStmt
    ;

varDecl
    : K_DEFINE ID ( K_EQUAL expr )? DOT?
    ;

assignStmt
    : target K_EQUAL expr DOT?
    ;

target
    : ID
    | expr K_OF ID
    ;

ifStmt
    : K_IF expr K_THEN
      ( COLON block )?
      ( K_ELSE_IF expr K_THEN COLON block )*
      ( K_ELSE COLON block )?
      K_END DOT?
    ;

foreachStmt
    : K_FOREACH foreachVar expr
      ( COLON block )?
      K_END DOT?
    ;

foreachVar
    : ID
    | ID K_OF ID
    | ID K_OF ID COMMA ID
    ;

whileStmt
    : K_WHILE expr
      ( COLON block )?
      K_END DOT?
    ;

returnStmt
    : K_RETURN expr? DOT?
    ;

breakStmt
    : K_BREAK DOT?
    ;

continueStmt
    : K_CONTINUE DOT?
    ;

tryStmt
    : K_TRY COLON block
      K_CATCH ID COLON block
      K_END DOT?
    ;

throwStmt
    : K_THROW expr DOT?
    ;

printStmt
    : ( K_PRINT | K_OUTPUT ) expr DOT?
    ;

exprStmt
    : expr DOT?
    ;

// ----- 表达式 -----

expr
    : pipelineExpr
    ;

pipelineExpr
    : andExpr ( ( PIPE | K_AND_WORD ) andExpr )*
    ;

andExpr
    : orExpr ( K_AND orExpr )*
    ;

orExpr
    : comparisonExpr ( K_OR comparisonExpr )*
    ;

comparisonExpr
    : additiveExpr ( compOp additiveExpr )*
    ;

compOp
    : K_GE | K_LE | K_GT | K_LT | K_NE | K_EQUAL
    | GE | LE | GT | LT | NE | EQ
    ;

additiveExpr
    : multiplicativeExpr ( addOp multiplicativeExpr )*
    ;

addOp
    : K_PLUS | K_MINUS
    | PLUS | MINUS
    ;

multiplicativeExpr
    : unaryExpr ( multOp unaryExpr )*
    ;

multOp
    : K_MULTIPLY | K_DIVIDE | K_MOD | K_POW
    | MULTIPLY | DIVIDE | MODULO | POW
    ;

unaryExpr
    : ( K_NOT | NOT ) unaryExpr
    | ( MINUS | K_MINUS ) unaryExpr
    | postfixExpr
    ;

postfixExpr
    : primary
      ( BOOK_L ID BOOK_R LPAREN exprList? RPAREN     // 《段名》(参数)
      | LPAREN exprList? RPAREN                        // (参数)
      | K_OF ID                                        // 之字结构: 对象之属性
      | LBRACKET expr RBRACKET                         // 索引: 对象[索引]
      )*
    ;

primary
    : NUMBER
    | STRING
    | K_TRUE
    | K_FALSE
    | K_NULL
    | ID
    | LPAREN expr RPAREN
    | LBRACKET dictLiteral RBRACKET
    | LBRACKET exprList? RBRACKET
    | BOOK_L ID BOOK_R                                 // 《段落名》
    ;

dictLiteral
    : dictEntry ( COMMA dictEntry )*
    ;

dictEntry
    : expr COLON expr
    ;

typeAnnotation
    : builtinType
    | ID
    ;

builtinType
    : T_NUMBER | T_INT | T_FLOAT
    | T_STRING | T_LIST | T_DICT | T_SET
    | T_BOOL | K_NULL | T_ANY
    ;

exprList
    : expr ( COMMA expr )*
    ;