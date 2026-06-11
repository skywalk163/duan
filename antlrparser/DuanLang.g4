/*
 * 段言（Duan）编程语言 ANTLR4 语法定义
 *
 * 版本: v1.0
 * 依据: 段言-完整规范文档 v1.4.1
 *
 * 设计说明：
 * - 支持中文整句分词（决策29：无空格分词支持）
 * - 双字关键字优先匹配（决策27：统一双字关键字）
 * - 中英文标点双模式（决策19：符号双模式支持）
 * - 显式"结束"模式 + 缩进模式双支持（决策33）
 * - 主谓/谓宾/定语语义区分（决策34）
 * - 元数驱动解析（决策28）
 * - 三种管道操作符（决策30）
 */

grammar DuanLang;

@header {
import sys
from antlr4 import *
from typing import List, Optional, Tuple, Any, Union
}

@members {
def format_error_msg(self, msg: str) -> str:
    return f"[段言语法错误] 行{self._ctx.start.line}: {msg}"
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
    | classDef
    | interfaceDef
    | dataTypeDef
    | errorTypeDef
    ;

// ----- 类定义 -----

classDef
    : BOOK_L ID genericParams? BOOK_R K_CLASS
      ( K_INHERIT typeAnnotation ( COMMA typeAnnotation )* )?
      ( K_USE typeAnnotation ( COMMA typeAnnotation )* )?
      COLON
      classMember*
      K_END DOT?
    ;

genericParams
    : LEFT_ANGLE ID (COMMA ID)* RIGHT_ANGLE
    ;

classMember
    : varDecl
    | methodDef
    | constructorDef
    ;

methodDef
    : BOOK_L ID BOOK_R K_METHOD
      LPAREN paramList? RPAREN
      ( PIPE typeAnnotation )?
      COLON
      block
      K_END DOT?
    ;

constructorDef
    : BOOK_L ID BOOK_R
      LPAREN paramList? RPAREN
      COLON
      block
      K_END DOT?
    ;

// ----- 接口定义 -----

interfaceDef
    : BOOK_L ID BOOK_R K_INTERFACE
      ( K_INHERIT typeAnnotation ( COMMA typeAnnotation )* )?
      COLON
      interfaceMember*
      K_END DOT?
    ;

interfaceMember
    : methodSignature DOT?
    | propertySignature DOT?
    ;

methodSignature
    : BOOK_L ID BOOK_R K_METHOD
      LPAREN paramList? RPAREN
      PIPE typeAnnotation
    ;

propertySignature
    : ID COLON typeAnnotation
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
    | K_NEW ID LPAREN exprList? RPAREN                 // 新 类名() - 实例化
    ;

dictLiteral
    : dictEntry ( COMMA dictEntry )*
    ;

dictEntry
    : expr COLON expr
    ;

typeAnnotation
    : builtinType
    | genericType
    | ID
    ;

genericType
    : ID LBRACKET typeAnnotation ( COMMA typeAnnotation )* RBRACKET
    ;

builtinType
    : T_NUMBER | T_INT | T_FLOAT
    | T_STRING | T_BOOL | K_NULL | T_ANY
    | T_LIST | T_DICT | T_SET
    | T_LIST LBRACKET typeAnnotation RBRACKET
    | T_DICT LBRACKET typeAnnotation COMMA typeAnnotation RBRACKET
    | T_SET LBRACKET typeAnnotation RBRACKET
    ;

exprList
    : expr ( COMMA expr )*
    ;


// ================================================================
// LEXER RULES
// ================================================================

// ----- 注释处理 -----

COMMENT_START
    : '```' .*? '```' -> skip
    ;

// ----- 双字关键字（决策27）- 长关键字在前避免部分匹配 -----

// 条件判断（三字优先于二字）
K_ELSE_IF  : '否则若' ;
K_IF       : '如果' ;
K_THEN     : '那么' ;
K_ELSE     : '否则' ;
K_END      : '结束' ;

// 比较运算符（三字优先于二字）
K_GE       : '大于等于' ;
K_LE       : '小于等于' ;
K_NE       : '不等于' ;
K_GT       : '大于' ;
K_LT       : '小于' ;

// 定义声明
K_DEFINE   : '定义' ;
K_EQUAL    : '等于' ;    // 同时用于赋值和比较（由 Parser 上下文决定语义）
K_SEGMENT  : '段' ;
K_CLASS    : '类' ;
K_INTERFACE: '接口' ;
K_NEW      : '新' ;
K_DATA_TYPE: '数据类型' ;
K_ERROR_TYPE: '错误' ;
K_CONST    : '常量' ;
K_TYPE     : '类型' ;
K_EXPORT   : '导出' ;
K_IMPORT   : '导入' ;
K_FROM     : '从' ;

// 循环控制
K_FOREACH  : '遍历' ;
K_WHILE    : '当' ;
K_BREAK    : '跳出' ;
K_CONTINUE : '跳过' ;

// 异常处理
K_TRY      : '尝试' ;
K_CATCH    : '捕获' ;
K_THROW    : '抛出' ;

// 返回
K_RETURN   : '返回' ;

// 数据操作
K_PRINT    : '打印' ;
K_OUTPUT   : '输出' ;
K_INPUT    : '输入' ;

// 作用域控制
K_INHERIT  : '继承' ;
K_USE      : '使用' ;
K_PARENT   : '父' ;
K_SELF     : '自我' ;
K_METHOD   : '方法' ;

// 逻辑运算
K_AND      : '且' ;
K_OR       : '或' ;
K_NOT      : '非' ;

// 算术运算（中文关键字）
K_PLUS     : '加' ;
K_MINUS    : '减' ;
K_MULTIPLY : '乘' ;
K_DIVIDE   : '除' ;
K_MOD      : '模' ;
K_POW      : '幂' ;

// 连接符/管道
K_AND_WORD : '并' ;
K_OF       : '之' ;
K_DE       : '的' ;

// 特殊值
K_TRUE     : '真' ;
K_FALSE    : '假' ;
K_NULL     : '空' ;

// ----- 内置类型 -----

T_NUMBER   : '数' ;
T_INT      : '整数' ;
T_FLOAT    : '浮数' ;
T_STRING   : '串' ;
T_LIST     : '列' ;
T_DICT     : '典' ;
T_SET      : '集' ;
T_BOOL     : '布尔' ;
T_ANY      : '任意' ;

// ----- 符号运算符（英文/符号）-----

POW        : '^' ;
MODULO     : '%' ;
MULTIPLY   : '*' ;
DIVIDE     : '/' ;
PLUS       : '+' ;
MINUS      : '-' ;

// 比较符号
EQ         : '==' ;
NE         : '!=' ;
GE         : '>=' ;
LE         : '<=' ;
GT         : '>' ;
LT         : '<' ;

// 泛型角括号（使用中文角括号）
LEFT_ANGLE  : '〈' ;  // U+3008
RIGHT_ANGLE : '〉' ;  // U+3009

// 逻辑符号
NOT        : '!' ;
AND        : '&&' ;
OR         : '||' ;

// 管道/箭头
PIPE       : '->' ;

// 路径分隔符（中文反斜杠或英文斜杠的 Unicode 形式）
PATH_SEP   : '/' | '／' ;

// ----- 标点符号（中英文双模式）-----

DOT        : '。' | '.' ;        // 句号：语句结束
COMMA      : '，' | ',' ;        // 逗号：分隔符/管道
COLON      : '：' | ':' ;        // 冒号：块定义/类型注解
SEMICOLON  : '；' | ';' ;        // 分号：多语句分隔
PAUSE      : '、' ;              // 顿号：参数并列

// ----- 括号 -----

LPAREN     : '（' | '(' ;
RPAREN     : '）' | ')' ;
LBRACKET   : '【' | '[' ;
RBRACKET   : '】' | ']' ;
BOOK_L     : '《' ;
BOOK_R     : '》' ;

// ----- 字面量 -----

NUMBER
    : [0-9]+ ( '.' [0-9]+ )?
    ;

STRING
    : '"' ( '\\' . | ~["\\] )* '"'
    | '\'' ( '\\' . | ~['\\] )* '\''
    ;

// ----- 标识符（含中文字符）-----

fragment IDEOGRAPHIC
    : [\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]
    ;

fragment LETTER
    : [a-zA-Z_]
    ;

fragment DIGIT
    : [0-9]
    ;

ID
    : ( IDEOGRAPHIC | LETTER ) ( IDEOGRAPHIC | LETTER | DIGIT )*
    ;

// ----- 空白 -----

NEWLINE
    : '\r'? '\n' -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

// ----- 未知字符（捕获错误）-----

UNKNOWN
    : .
    ;