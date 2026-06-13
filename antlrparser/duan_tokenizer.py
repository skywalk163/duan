"""
段言（Duan）编程语言 - 中文分词器

实现决策29：无空格分词支持
- 双字关键词优先匹配
- 类型切换自动分词
- 元数驱动参数收集

使用 Python 实现自定义分词，然后将 tokens 喂给 ANTLR 解析器
"""

import re
from typing import List, Optional, Tuple
from antlr4 import *
from antlr4 import Token as AntlrToken
from antlr4.CommonTokenFactory import CommonTokenFactory
from antlr4.Lexer import TokenSource
from antlr4.Token import CommonToken


# =============================================================================
# 关键词表（按长度降序排列，优先匹配长关键词）
# =============================================================================

# 所有关键字（长关键字在前）
KEYWORDS = [
    # 条件判断（三字）
    '否则若', '大于等于', '小于等于',
    # 定义声明（二字）
    '数据类型', '错误', '定义', '等于', '导入', '导出', '常量', '类型', '继承', '使用', '方法', '自我', '段落', '实现', '构造',
    # 条件判断（二字）
    '如果', '那么', '否则', '结束',
    # 比较（二字）
    '大于', '小于', '不等于',
    # 循环控制（二字）
    '遍历', '跳出', '跳过',
    # 异常处理（二字）
    '尝试', '捕获', '抛出',
    # 返回（二字）
    '返回',
    # 数据操作（二字）
    '打印', '输出', '输入',
    # 单字
    '段', '从', '当', '父', '类', '接口', '新', '己', '设', '为', '于',
    # 逻辑（单字）
    '且', '或', '非',
    # 算术（单字）
    '加', '减', '乘', '除', '模', '幂',
    # 连接/属性（单字）
    '并', '之', '的',
    # 特殊值（单字）
    '真', '假', '空',
    # 内置类型（单字/二字）
    '整数', '浮数', '布尔', '任意',
    '数', '列', '串', '典', '集',
]

# 关键词到其类型的映射
KEYWORD_TOKEN_MAP = {
    # 条件判断
    '否则若': 'K_ELSE_IF',
    '如果': 'K_IF',
    '那么': 'K_THEN',
    '否则': 'K_ELSE',
    '结束': 'K_END',
    # 比较
    '大于等于': 'K_GE',
    '小于等于': 'K_LE',
    '不等于': 'K_NE',
    '大于': 'K_GT',
    '小于': 'K_LT',
    # 定义声明
    '定义': 'K_DEFINE',
    '等于': 'K_EQUAL',
    '段': 'K_SEGMENT',
    '段落': 'K_SEGMENT',
    '接收': 'K_RECEIVE',
    '类': 'K_CLASS',
    '接口': 'K_INTERFACE',
    '新': 'K_NEW',
    '新建': 'K_NEW',
    '数据类型': 'K_DATA_TYPE',
    '错误': 'K_ERROR_TYPE',
    '常量': 'K_CONST',
    '类型': 'K_TYPE',
    '导出': 'K_EXPORT',
    '导入': 'K_IMPORT',
    '从': 'K_FROM',
    '遍历': 'K_FOREACH',
    '当': 'K_WHILE',
    '跳出': 'K_BREAK',
    '跳过': 'K_CONTINUE',
    '尝试': 'K_TRY',
    '捕获': 'K_CATCH',
    '抛出': 'K_THROW',
    '返回': 'K_RETURN',
    '打印': 'K_PRINT',
    '输出': 'K_OUTPUT',
    '输入': 'K_INPUT',
    '继承': 'K_INHERIT',
    '实现': 'K_IMPLEMENTS',
    '使用': 'K_USE',
    '父': 'K_PARENT',
    '己': 'K_SELF',
    '方法': 'K_METHOD',
    '属性': 'K_ATTRIBUTE',
    '构造': 'K_CONSTRUCTOR',
    '设': 'K_SET',
    '为': 'K_AS',
    '于': 'K_AT',
    '错误': 'K_ERROR_TYPE',
    '常量': 'K_CONST',
    '类型': 'K_TYPE',
    '导出': 'K_EXPORT',
    '导入': 'K_IMPORT',
    '从': 'K_FROM',
    # 循环控制
    '遍历': 'K_FOREACH',
    '当': 'K_WHILE',
    '跳出': 'K_BREAK',
    '跳过': 'K_CONTINUE',
    # 异常处理
    '尝试': 'K_TRY',
    '捕获': 'K_CATCH',
    '抛出': 'K_THROW',
    # 返回
    '返回': 'K_RETURN',
    # 数据操作
    '打印': 'K_PRINT',
    '输出': 'K_OUTPUT',
    '输入': 'K_INPUT',
    # 作用域
    '继承': 'K_INHERIT',
    '使用': 'K_USE',
    '父': 'K_PARENT',
    '自我': 'K_SELF',
    '方法': 'K_METHOD',
    # 逻辑运算
    '且': 'K_AND',
    '或': 'K_OR',
    '非': 'K_NOT',
    # 算术运算
    '加': 'K_PLUS',
    '减': 'K_MINUS',
    '乘': 'K_MULTIPLY',
    '除': 'K_DIVIDE',
    '模': 'K_MOD',
    '幂': 'K_POW',
    # 连接符/属性
    '并': 'K_AND_WORD',
    '之': 'K_OF',
    '的': 'K_DE',
    # 特殊值
    '真': 'K_TRUE',
    '假': 'K_FALSE',
    '空': 'K_NULL',
    # 内置类型
    '数': 'T_NUMBER',
    '整数': 'T_INT',
    '浮数': 'T_FLOAT',
    '串': 'T_STRING',
    '列': 'T_LIST',
    '典': 'T_DICT',
    '集': 'T_SET',
    '布尔': 'T_BOOL',
    '任意': 'T_ANY',
}

# 构建关键词集合（用于快速查找）
KEYWORD_SET = set(KEYWORDS)
KEYWORD_MAX_LEN = max(len(k) for k in KEYWORDS)

# 单字关键词集合（用于复合词冲突检测）
SINGLE_CHAR_KEYWORDS = {kw for kw in KEYWORDS if len(kw) == 1}

# 复合词安全关键词：这些单字关键词在复合词中很常见（如"列表"中的"列"），
# 后接CJK字符时应该跳过，允许收集为标识符
COMPOUND_SAFE_SINGLE_KEYWORDS = {
    '数', '列', '串', '典', '集',   # 类型
    '从',                             # 导入
    '段', '段落',                        # 段落（统一语法）
    '空', '真', '假',                 # 特殊值（常见复合词如 空间、真实、假设）
    '父',                             # 作用域（常见复合词如 父类、父级）
    '的',                             # 助词（常见复合词如 的确、的话）
}

# 符号 Token 映射
SYMBOL_TOKEN_MAP = {
    '。': 'DOT', '.': 'DOT',
    '，': 'COMMA', ',': 'COMMA',
    '：': 'COLON', ':': 'COLON',
    '；': 'SEMICOLON', ';': 'SEMICOLON',
    '、': 'PAUSE',
    '（': 'LPAREN', '(': 'LPAREN',
    '）': 'RPAREN', ')': 'RPAREN',
    '【': 'LBRACKET', '[': 'LBRACKET',
    '】': 'RBRACKET', ']': 'RBRACKET',
    '{': 'LBRACE', '}': 'RBRACE',
    '＼': 'PATH_SEP', '/': 'PATH_SEP',
    '^': 'POW', '%': 'MODULO',
    '*': 'MULTIPLY', '×': 'MULTIPLY',
    '÷': 'DIVIDE',
    '+': 'PLUS',
    # '-' 作为连字符，需要特殊处理（-> 是 PIPE）
}

# 多字符符号
MULTI_CHAR_SYMBOLS = {
    '->': 'PIPE',
    '==': 'EQ',
    '!=': 'NE',
    '>=': 'GE',
    '<=': 'LE',
    '&&': 'AND',
    '||': 'OR',
}

# 单字符符号
SINGLE_CHAR_SYMBOLS = {
    '>': 'GT',
    '<': 'LT',
    '!': 'NOT',
    '-': 'MINUS',
    '=': 'EQ',  # 赋值/相等比较
}


# Unicode 范围
def is_cjk_char(ch: str) -> bool:
    """判断是否为中文字符"""
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0xF900 <= cp <= 0xFAFF)


def is_letter(ch: str) -> bool:
    """判断是否为英文字母"""
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch: str) -> bool:
    """判断是否为数字"""
    return '0' <= ch <= '9'


def char_type(ch: str) -> str:
    """获取字符类型（用于类型切换分词）"""
    if is_cjk_char(ch):
        return 'CJK'
    elif is_letter(ch):
        return 'LETTER'
    elif is_digit(ch):
        return 'DIGIT'
    else:
        return 'SYMBOL'


# =============================================================================
# Token 数据类
# =============================================================================

class Token:
    """段言 Token"""

    def __init__(self, type_name: str, text: str, line: int, column: int):
        self.type_name = type_name
        self.text = text
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type_name}, '{self.text}', line={self.line}, col={self.column})"


# =============================================================================
# 中文分词器
# =============================================================================

class DuanLangTokenizer:
    """段言中文分词器

    实现决策29的三层分词机制：
    第1层：类型切换自动分词
    第2层：双字关键词优先匹配
    第3层：元数驱动参数收集（可选，在 Visitor 中实现）
    """

    def __init__(self):
        self.errors = []

    def tokenize(self, source: str) -> List[Token]:
        """将段言源代码分词"""
        tokens = []
        line = 1
        col = 1
        i = 0
        source_len = len(source)

        def advance(n: int = 1):
            nonlocal i, line, col
            for _ in range(n):
                if i < source_len and source[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1

        def peek(n: int = 0) -> str:
            pos = i + n
            return source[pos] if pos < source_len else ''

        while i < source_len:
            ch = source[i]

            # ---------- 空白字符 ----------
            if ch in ' \t\r\n':
                advance()
                continue

            # ---------- 单行注释（#）----------
            if ch == '#':
                while i < source_len and source[i] != '\n':
                    advance()
                continue

            # ---------- 代码块注释 ```...``` ----------
            if ch == '`' and source[i:i+3] == '```':
                advance(3)  # 跳过开启的```
                # 跳过注释标签行（如 `注释` 或 `python`）
                while i < source_len and source[i] != '\n':
                    advance()
                if i < source_len:
                    advance()  # 跳过换行
                # 跳过注释内容直到关闭的```
                while i < source_len:
                    if source[i:i+3] == '```':
                        advance(3)
                        break
                    advance()
                continue

            # ---------- 多字符符号（如 ->, ==, != 等）----------
            for sym_len in [2, 3]:
                if i + sym_len <= source_len:
                    text = source[i:i+sym_len]
                    if text in MULTI_CHAR_SYMBOLS:
                        token_type = MULTI_CHAR_SYMBOLS[text]
                        tokens.append(Token(token_type, text, line, col))
                        advance(sym_len)
                        break
            else:
                # ---------- 单字符符号 ----------
                if ch in SINGLE_CHAR_SYMBOLS:
                    token_type = SINGLE_CHAR_SYMBOLS[ch]
                    tokens.append(Token(token_type, ch, line, col))
                    advance()
                    continue

                # ---------- 《》书名号（收集内部文本作为单个 ID）----------
                if ch == '《':
                    tokens.append(Token('BOOK_L', ch, line, col))
                    advance()  # 跳过《
                    id_text = ''
                    start_line, start_col = line, col
                    while i < source_len and source[i] != '》':
                        id_text += source[i]
                        advance()
                    if i < source_len and source[i] == '》':
                        tokens.append(Token('ID', id_text, start_line, start_col))
                        tokens.append(Token('BOOK_R', source[i], line, col))
                        advance()  # 跳过》
                    continue

                # ---------- 中英文标点 ----------
                if ch in SYMBOL_TOKEN_MAP:
                    if ch in SYMBOL_TOKEN_MAP:
                        token_type = SYMBOL_TOKEN_MAP[ch]
                        tokens.append(Token(token_type, ch, line, col))
                        advance()
                        continue

                # ---------- 字符串 ----------
                if ch in ('"', "'"):
                    quote = ch
                    start_line, start_col = line, col
                    advance()  # 跳过开引号
                    text = quote
                    while i < source_len and source[i] != quote:
                        if source[i] == '\\':
                            advance()
                            if i < source_len:
                                text += '\\' + source[i]
                                advance()
                        else:
                            text += source[i]
                            advance()
                    if i < source_len:
                        text += source[i]
                        advance()  # 跳过闭引号
                    else:
                        self.errors.append(f"行{start_line}: 字符串未闭合")
                    tokens.append(Token('STRING', text, start_line, start_col))
                    continue

                # ---------- 关键字/标识符（中文连续书写分词）----------
                if is_cjk_char(ch) or is_letter(ch):

                    # 尝试匹配最长关键词
                    if is_cjk_char(ch):
                        matched_keyword = None
                        for kw_len in range(KEYWORD_MAX_LEN, 0, -1):
                            if i + kw_len <= source_len:
                                text = source[i:i+kw_len]
                                if text in KEYWORD_SET:
                                    matched_keyword = text
                                    break

                        if matched_keyword:
                            # 复合词安全：部分单字关键词在后接CJK时跳过（避免"列表"被拆分为"列"+"表"）
                            if (len(matched_keyword) == 1
                                and matched_keyword in COMPOUND_SAFE_SINGLE_KEYWORDS
                                and i + 1 < source_len
                                and is_cjk_char(source[i+1])):
                                matched_keyword = None
                            else:
                                token_type = KEYWORD_TOKEN_MAP[matched_keyword]
                                tokens.append(Token(token_type, matched_keyword, line, col))
                                advance(len(matched_keyword))
                                continue

                    # 不是关键字，则收集连续字符作为标识符（支持CJK/字母/数字混合）
                    start_line, start_col = line, col
                    text = ''
                    has_alphanumeric = False  # 标记是否已经收集了字母或数字

                    while i < source_len:
                        c = source[i]
                        if is_cjk_char(c):
                            # 检查是否是关键词的开头
                            keyword_found = False
                            for kw_len in range(KEYWORD_MAX_LEN, 0, -1):
                                if i + kw_len <= source_len:
                                    kw_text = source[i:i+kw_len]
                                    if kw_text in KEYWORD_SET:
                                        # 复合词安全关键词：永不阻断标识符收集
                                        # （如"计数"中的"数"，"列表"中的"列"）
                                        if kw_len == 1 and kw_text in COMPOUND_SAFE_SINGLE_KEYWORDS:
                                            continue
                                        # 只有当已经收集了字母/数字时，才让关键词阻断标识符收集
                                        # 这样可以正确处理：
                                        # - n减1 -> n 减 1（减是关键词，前面有字母）
                                        # - 阶乘 -> 阶乘（乘是关键词，但前面没有字母/数字）
                                        if has_alphanumeric:
                                            keyword_found = True
                                            break
                            if keyword_found:
                                break
                            text += c
                            advance()
                        elif is_letter(c):
                            text += c
                            has_alphanumeric = True
                            advance()
                        elif is_digit(c):
                            text += c
                            has_alphanumeric = True
                            advance()
                        else:
                            break

                    if text:
                        # 检查是否是内置类型
                        if text in KEYWORD_TOKEN_MAP:
                            tokens.append(Token(KEYWORD_TOKEN_MAP[text], text, start_line, start_col))
                        else:
                            tokens.append(Token('ID', text, start_line, start_col))
                    continue

                # ---------- 数字 ----------
                if is_digit(ch):
                    start_line, start_col = line, col
                    text = ''
                    is_float = False
                    while i < source_len and is_digit(source[i]):
                        text += source[i]
                        advance()
                    if i < source_len and source[i] == '.':
                        # 检查是否是数字的一部分（后面还有数字）
                        if i + 1 < source_len and is_digit(source[i+1]):
                            is_float = True
                            text += '.'
                            advance()
                            while i < source_len and is_digit(source[i]):
                                text += source[i]
                                advance()
                    tokens.append(Token('NUMBER', text, start_line, start_col))
                    continue

                # ---------- 未知字符（错误捕获）----------
                self.errors.append(f"行{line}, 列{col}: 无法识别的字符 '{ch}'")
                advance()

        # 不再在这里添加 EOF，让 nextToken 方法处理
        return tokens


# =============================================================================
# ANTLR 适配器：将段言 Token 转换为 ANTLR Token 流
# =============================================================================

class DuanLangTokenSource(TokenSource):
    """将自定义 Token 转换为 ANTLR Token 流"""

    def __init__(self, tokens: List[Token], lexer):
        self.tokens = tokens
        self.lexer = lexer
        self.pos = 0
        self._token_type_map = self._build_token_type_map(lexer)
        self._factory = CommonTokenFactory.DEFAULT

    def _build_token_type_map(self, lexer) -> dict:
        """构建 Token 名称到 ANTLR Token 类型的映射（使用 symbolicNames）"""
        mapping = {}
        for i, name in enumerate(lexer.symbolicNames):
            if name and name != '<INVALID>':
                mapping[name] = i
        # 添加 EOF
        mapping['EOF'] = AntlrToken.EOF
        return mapping

    def nextToken(self):
        """获取下一个 Token"""
        if self.pos >= len(self.tokens):
            # 返回 EOF token
            ct = CommonToken(
                source=CommonToken.EMPTY_SOURCE,
                type=AntlrToken.EOF,
                channel=AntlrToken.DEFAULT_CHANNEL,
            )
            ct.line = 0
            ct.column = 0
            ct.text = ''
            return ct

        token = self.tokens[self.pos]
        self.pos += 1

        antlr_type = self._token_type_map.get(token.type_name, AntlrToken.INVALID_TYPE)

        ct = CommonToken(
            source=CommonToken.EMPTY_SOURCE,
            type=antlr_type,
            channel=AntlrToken.DEFAULT_CHANNEL,
            start=token.column - 1,
            stop=token.column - 1 + len(token.text) - 1,
        )
        ct.line = token.line
        ct.column = token.column - 1
        ct.text = token.text

        return ct

    def getSourceName(self):
        return "段言自定义分词器"


def create_antlr_token_stream(source: str, lexer) -> CommonTokenStream:
    """创建 ANTLR Token 流（使用自定义分词器）"""
    tokenizer = DuanLangTokenizer()
    tokens = tokenizer.tokenize(source)
    token_source = DuanLangTokenSource(tokens, lexer)
    return CommonTokenStream(token_source)