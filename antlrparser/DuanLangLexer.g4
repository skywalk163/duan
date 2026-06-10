/*
 * 段言（Duan）编程语言 ANTLR4 词法定义
 *
 * 版本: v1.0
 * 独立的 Lexer 语法，支持 lexer mode 实现代码块注释
 */

lexer grammar DuanLangLexer;

// ----- 注释（lexer mode 实现）-----

LINE_COMMENT
    : '#' ~[\r\n]* -> channel(HIDDEN)
    ;

COMMENT_START
    : '```' -> pushMode(COMMENT_MODE), channel(HIDDEN)
    ;

mode COMMENT_MODE;
COMMENT_CLOSE
    : '```' -> popMode, channel(HIDDEN)
    ;
COMMENT_CONTENT
    : . -> channel(HIDDEN)
    ;

mode DEFAULT_MODE;

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
MULTIPLY   : '*' | '×' ;
DIVIDE     : '/' | '÷' ;
PLUS       : '+' ;
MINUS      : '-' ;

// 比较符号
EQ         : '==' ;
NE         : '!=' ;
GE         : '>=' ;
LE         : '<=' ;
GT         : '>' ;
LT         : '<' ;

// 逻辑符号
NOT        : '!' ;
AND        : '&&' ;
OR         : '||' ;

// 管道/箭头
PIPE       : '->' ;

// 路径分隔符
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
LBRACE     : '{' ;
RBRACE     : '}' ;
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