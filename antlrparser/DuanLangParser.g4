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
    | classDef
    | interfaceDef
    | dataTypeDef
    | errorTypeDef
    ;

// ----- 段落定义（统一语法）-----

paragraphDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON
      block
      K_END PERIOD?
    ;

// ----- 类定义（统一语法）-----

classDef
    : K_CLASS ID genericParams?
      ( K_INHERIT typeAnnotation ( COMMA typeAnnotation )* )?
      ( K_IMPLEMENTS typeAnnotation ( COMMA typeAnnotation )* )?
      COLON
      classMember*
      K_END PERIOD?
    ;

genericParams
    : LBRACKET ID ( COMMA ID )* RBRACKET
    ;

classMember
    : methodDef
    | constructorDef
    | attributeDecl
    | stmt
    ;

methodDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

constructorDef
    : K_CONSTRUCTOR ( LPAREN paramList? RPAREN | K_RECEIVE paramList )? COLON block K_END PERIOD?
    ;

attributeDecl
    : K_ATTRIBUTE ID ( K_AS typeAnnotation )? ( K_EQUAL expr )? PERIOD?
    ;

// ----- 接口定义（统一语法）-----

interfaceDef
    : K_INTERFACE ID
      ( K_INHERIT typeAnnotation ( COMMA typeAnnotation )* )?
      COLON
      interfaceMember*
      K_END PERIOD?
    ;

interfaceMember
    : K_METHOD ID LPAREN paramList? RPAREN ( K_RETURN typeAnnotation )? PERIOD?
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
      K_END PERIOD?
    ;

dataTypeField
    : ID COLON typeAnnotation PERIOD?
    ;

errorTypeDef
    : BOOK_L ID BOOK_R K_ERROR_TYPE COLON
      dataTypeField+
      K_END PERIOD?
    ;

// ----- 导入/导出 -----

importStmt
    : K_FROM path K_IMPORT importList PERIOD?
    | K_IMPORT importList PERIOD?
    ;

exportStmt
    : K_EXPORT ( ID | BOOK_L ID BOOK_R ) PERIOD?
    ;

path
    : ID ( PATH_SEP ID )*
    | BOOK_L ID BOOK_R
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
    : K_SET ID K_AS expr PERIOD ( K_TYPE typeAnnotation )?    // 统一语法：设 甲 为 三
    | K_DEFINE ID ( K_EQUAL expr PERIOD )?                    // 兼容旧语法
    ;

assignStmt
    : target ( ASSIGN | K_EQUAL | K_AS ) expr PERIOD?            // 支持 =、等于、为 三种赋值
    ;

target
    : ID
    | expr K_OF ID
    | primary DOT ID                                          // 属性访问作为赋值目标
    ;

ifStmt
    : K_IF expr COLON block
      ( K_ELSE_IF expr COLON block )*
      ( K_ELSE COLON block )?
      K_END PERIOD?
    ;

foreachStmt
    : K_FOREACH ID ( K_OF | K_AT ) expr
      COLON block
      K_END PERIOD?
    ;

foreachVar
    : ID
    | ID K_OF ID
    | ID K_OF ID COMMA ID
    ;

whileStmt
    : K_WHILE expr
      ( COLON block )?
      K_END PERIOD?
    ;

returnStmt
    : K_RETURN expr? PERIOD?
    ;

breakStmt
    : K_BREAK PERIOD?
    ;

continueStmt
    : K_CONTINUE PERIOD?
    ;

tryStmt
    : K_TRY COLON block
      K_CATCH ID COLON block
      K_END PERIOD?
    ;

throwStmt
    : K_THROW expr PERIOD?
    ;

printStmt
    : ( K_PRINT | K_OUTPUT ) expr PERIOD?
    ;

exprStmt
    : expr PERIOD
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
      | DOT ID                                         // 属性访问: 对象.属性
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
    | K_SELF                                              // 己（self引用）
    | K_NEW ID LPAREN exprList? RPAREN                  // 新建 对象()
    | ID
    | LPAREN expr RPAREN
    | LBRACKET dictLiteral RBRACKET
    | LBRACKET exprList? RBRACKET
    | BOOK_L ID BOOK_R                                 // 《段落名》
    // 动词调用（支持动词白名单中的动词）
    | K_FIRST LPAREN expr RPAREN                       // 首(列表)
    | K_LAST LPAREN expr RPAREN                        // 末(列表)
    | K_REST LPAREN expr RPAREN                        // 余(列表)
    | K_LENGTH LPAREN expr RPAREN                      // 长(列表)
    | K_SORT LPAREN expr RPAREN                        // 排序(列表)
    | K_REVERSE LPAREN expr RPAREN                     // 反转(列表)
    | K_SUM LPAREN expr RPAREN                         // 求和(列表)
    | K_MAX LPAREN expr RPAREN                         // 求最大(列表)
    | K_MIN LPAREN expr RPAREN                         // 求最小(列表)
    | K_UNIQUE LPAREN expr RPAREN                      // 去重(列表)
    | K_FILTER LPAREN expr COMMA expr RPAREN           // 筛选(列表, 条件)
    | K_MAP LPAREN expr COMMA expr RPAREN              // 映射(列表, 函数)
    // 字符串操作动词
    | K_TO_INT LPAREN expr RPAREN                      // 转整数(值)
    | K_TO_FLOAT LPAREN expr RPAREN                    // 转浮点(值)
    | K_TO_STR LPAREN expr RPAREN                      // 转字符串(值)
    | K_STR_LEN LPAREN expr RPAREN                     // 字符串长度(文本)
    | K_STR_SPLIT LPAREN expr COMMA expr RPAREN        // 分割字符串(文本, 分隔符)
    | K_STR_JOIN LPAREN expr COMMA expr RPAREN         // 连接字符串(列表, 分隔符)
    | K_STR_REPLACE LPAREN expr COMMA expr COMMA expr RPAREN  // 替换字符串(文本, 旧, 新)
    | K_STR_TRIM LPAREN expr RPAREN                    // 去除空白(文本)
    // 文件操作动词
    | K_READ_FILE LPAREN expr RPAREN                   // 读取文件(路径)
    | K_WRITE_FILE LPAREN expr COMMA expr RPAREN       // 写入文件(路径, 内容)
    | K_APPEND_FILE LPAREN expr COMMA expr RPAREN      // 追加文件(路径, 内容)
    | K_FILE_EXISTS LPAREN expr RPAREN                 // 文件存在(路径)
    | K_DIR_EXISTS LPAREN expr RPAREN                  // 目录存在(路径)
    | K_MAKE_DIR LPAREN expr RPAREN                    // 创建目录(路径)
    | K_REMOVE_FILE LPAREN expr RPAREN                 // 删除文件(路径)
    | K_REMOVE_DIR LPAREN expr RPAREN                  // 删除目录(路径)
    // 系统操作动词
    | K_ENV LPAREN expr RPAREN                         // 环境变量(名称)
    | K_SET_ENV LPAREN expr COMMA expr RPAREN          // 设置环境变量(名称, 值)
    | K_ARGS LPAREN RPAREN                             // 参数列表()
    | K_EXIT LPAREN expr? RPAREN                       // 退出程序(状态码)
    | K_CWD LPAREN RPAREN                              // 当前目录()
    | K_CD LPAREN expr RPAREN                          // 切换目录(路径)
    | K_EXEC LPAREN expr RPAREN                        // 执行命令(命令)
    // I/O操作动词
    | K_PRINT LPAREN exprList? RPAREN                  // 打印(...)
    | K_OUTPUT LPAREN exprList? RPAREN                 // 输出(...)
    | K_INPUT LPAREN expr? RPAREN                      // 输入(提示)
    | K_READ LPAREN expr? RPAREN                       // 读取(提示)
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