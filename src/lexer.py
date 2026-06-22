"""
段言（Duan）编程语言 - 词法分析器

实现决策29的三层分词机制：
1. 类型切换自动分词 - 甲加1 → [甲] [加] [1]
2. 双字关键词优先匹配 - 定义甲 → [定义] [甲]
3. 元数驱动参数收集 - 打印 甲 -（元数=1）→ [打印] [甲]

参考：newlisp/yan 的无空格分词实现
"""

from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Tuple
from enum import Enum

from tokens import Token, TokenType
from keywords import (
    ALL_KEYWORDS, KEYWORDS_DOUBLE, KEYWORDS_LOGIC, KEYWORDS_SPECIAL,
    VERB_ARITY, BUILTIN_TYPES, SYMBOL_MAP, BLOCKING_SYMBOLS
)

# 运算符动词集合（用于分词时识别运算符）
OPERATOR_VERBS = frozenset({
    '加', '减', '乘', '除', '加上', '减去', '乘以', '除以', 
    '大于', '小于', '等于', '不等于', '大于等于', '小于等于',
    '模', '幂'
})

# 常见复合词保护列表（这些词包含运算符动词，但应该作为整体识别）
COMMON_COMPOUND_WORDS = frozenset({
    '追加', '加入', '减少', '减去', '乘法', '除法', '模式', '幂次',
    '当前', '当然', '应当', '当选', '当家',
    '加入', '加快', '加强', '加减',
    '减少', '减弱', '减速',
    '乘法', '乘积', '乘客', '乘除',
    '除法', '除非', '去除',
})


class LexerError(Exception):
    """词法分析错误"""
    def __init__(self, message: str, line: int, col: int, source_context: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.source_context = source_context
        msg = f"词法错误 (行{line}, 列{col}): {message}"
        if source_context:
            msg += f"\n  附近代码: ...{source_context}..."
        super().__init__(msg)


class Lexer:
    """段言词法分析器：无空格分词 + 三层机制"""
    
    # CJK 汉字范围
    HAN_START = 0x4E00
    HAN_END = 0x9FFF
    
    # 中文数字
    CHINESE_DIGITS = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '万': 10000,
    }
    
    # 简单中文数字（零到十）
    SIMPLE_CHINESE_NUMBERS = {
        '零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
    }
    
    def __init__(self, source: str = None):
        """初始化词法分析器
        
        支持两种调用方式：
        - Lexer(source).tokenize()
        - Lexer().tokenize(source)
        
        Args:
            source: 可选的源码字符串
        """
        self._source = source
        
        # 预计算关键字长度分组（优化匹配速度）
        self.keywords_by_length: Dict[int, Set[str]] = {}
        self.max_keyword_len = 0
        
        for kw in ALL_KEYWORDS:
            length = len(kw)
            if length not in self.keywords_by_length:
                self.keywords_by_length[length] = set()
            self.keywords_by_length[length].add(kw)
            if length > self.max_keyword_len:
                self.max_keyword_len = length
        
        # 添加动词到关键字集合（用于分词）
        self.all_keywords_with_verbs = ALL_KEYWORDS | set(VERB_ARITY.keys())
        
        # 重新计算包含动词的长度分组
        self.all_keywords_by_length: Dict[int, Set[str]] = {}
        self.all_max_keyword_len = 0
        
        for kw in self.all_keywords_with_verbs:
            length = len(kw)
            if length not in self.all_keywords_by_length:
                self.all_keywords_by_length[length] = set()
            self.all_keywords_by_length[length].add(kw)
            if length > self.all_max_keyword_len:
                self.all_max_keyword_len = length
        
        # 复合词安全：这些单字关键字在复合词中常见（如"对象"中的"对"），
        # 当后接CJK字符时应跳过，避免拆分复合词
        # 注意：算术运算符（加、减、乘、除、模、幂）和循环关键字"当"现在在此列，
        # 因为它们经常出现在复合词中（如"当前"、"追加"）
        self.compound_safe_single_keywords: Set[str] = {
            '数', '列', '串', '典', '集',   # 类型
            '从',                             # 导入
            '段',                             # 段落
            '空', '真', '假',                 # 特殊值（常见复合词如 空间、真实、假设）
            '父',                             # 作用域（常见复合词如 父类、父级）
            '的',                             # 助词
            '若',                             # 条件（常见复合词如 若干、若非）
            '则',                             # 条件（常见复合词如 规则、法则）
            '对',                             # 遍历别名（常见复合词如 对象、对于、对比）
            '长',                             # 长度（常见复合词如 长度、成长、延长）
        }
        
        # 预计算符号映射到 TokenType（优化符号匹配）
        self._symbol_token_map: Dict[str, TokenType] = {
            '.': TokenType.DOT,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '<': TokenType.LBOOK,
            '>': TokenType.RBOOK,
            '\\': TokenType.COMMA,
            '=': TokenType.EQUALS,
            '@': TokenType.AT,
            '+': TokenType.PLUS,
            '!': TokenType.BANG,
            '\uff01': TokenType.BANG,  # 中文感叹号 ！
        }
    
    def tokenize(self, source: str = None) -> List[Token]:
        """将源码转为 Token 流
        
        支持两种调用方式：
        - lexer.tokenize()  # 使用构造时传入的 source
        - lexer.tokenize(source)  # 使用传入的 source
        
        Args:
            source: 要分析的源码字符串（可选，默认使用构造时传入的）
        """
        if source is None:
            source = self._source
        if source is None:
            raise LexerError("没有提供源码", 0, 0)
        
        tokens = []
        i = 0
        line = 1
        col = 1
        n = len(source)

        # 预扫描：收集用户定义的标识符
        user_definitions = self._scan_user_definitions(source)

        # 处理缩进
        indent_stack = [0]

        # 安全计数器（防止意外死循环）
        _main_loop_safety = 0

        while i < n:
            # 安全计数器（防止意外死循环）
            _main_loop_safety += 1
            if _main_loop_safety > 50000:
                raise RuntimeError(f"词法分析主循环超出安全上限 ({_main_loop_safety}次迭代), 位置: {i}, 字符: {repr(source[i:i+30])}")
            
            # 处理换行
            if source[i] == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', line, col))
                line += 1
                col = 1
                i += 1
                
                # 计算下一行的缩进
                indent = 0
                while i < n and source[i] in ' \t':
                    if source[i] == '\t':
                        indent += 4
                    else:
                        indent += 1
                    col += 1
                    i += 1
                
                # 处理缩进变化
                if indent > indent_stack[-1]:
                    tokens.append(Token(TokenType.INDENT, indent, line, 1))
                    indent_stack.append(indent)
                elif indent < indent_stack[-1]:
                    while indent_stack[-1] > indent:
                        indent_stack.pop()
                        tokens.append(Token(TokenType.DEDENT, indent_stack[-1], line, 1))
                continue
            
            # 跳过空白
            if source[i] in ' \t\r':
                col += 1
                i += 1
                continue
            
            # 处理注释（# 开头）
            if source[i] == '#':
                while i < n and source[i] != '\n':
                    i += 1
                continue
            
            # 处理注释（// 开头）
            if i + 1 < n and source[i:i+2] == '//':
                while i < n and source[i] != '\n':
                    i += 1
                continue
            
            # 处理注释（注 开头）
            if source[i] == '注':
                while i < n and source[i] != '\n':
                    i += 1
                continue
            
            # 处理符号
            token, consumed = self._try_match_symbol(source, i, line, col)
            if token:
                # 特殊处理：书名号《》内的段落名
                if token.type == TokenType.LBOOK:
                    # 收集段落名
                    j = i + 1
                    name_chars = []
                    while j < n and source[j] != '》':
                        name_chars.append(source[j])
                        j += 1
                    
                    if j >= n:
                        raise LexerError(f"书名号《》未闭合: 段落名 '{''.join(name_chars)}' 缺少右书名号》", line, col)
                    
                    # 添加左书名号
                    tokens.append(token)
                    col += 1
                    i += 1
                    
                    # 添加段落名（作为标识符）
                    para_name = ''.join(name_chars)
                    tokens.append(Token(TokenType.IDENTIFIER, para_name, line, col))
                    col += len(name_chars)
                    i += len(name_chars)
                    
                    # 添加右书名号
                    tokens.append(Token(TokenType.RBOOK, '》', line, col))
                    col += 1
                    i += 1
                    continue
                else:
                    tokens.append(token)
                    col += consumed
                    i += consumed
                    continue
            
            # 处理字符串
            if source[i] in '"\'「『':
                token, consumed = self._tokenize_string(source, i, line, col)
                tokens.append(token)
                col += consumed
                i += consumed
                continue
            
            # 处理数字
            if source[i].isdigit() or (source[i] == '-' and i + 1 < n and source[i+1].isdigit()):
                token, consumed = self._tokenize_number(source, i, line, col)
                tokens.append(token)
                col += consumed
                i += consumed
                continue
            
            # 处理中文数字（不在此处拦截单个字符，而是交给 _tokenize_chinese_sequence 处理复合数字）
            # 注释：SIMPLE_CHINESE_NUMBERS 单个字符拦截会破坏复合数字（如"零点一"、"一百"）
            # 以及以数字开头的函数名（如"四舍五入"）的解析
            # 所有汉字统一由 _tokenize_identifier_or_keyword → _tokenize_chinese_sequence 处理
            
            # 处理中文数字（注释：不在此处处理，而是在标识符处理中判断）
            # 因为 "甲加三" 中的 "三" 需要根据上下文判断
            
            # 处理标识符和关键字（核心：无空格分词）
            if self._is_han(source[i]) or source[i].isalpha() or source[i] == '_':
                new_tokens, consumed = self._tokenize_identifier_or_keyword(source, i, line, col, user_definitions)
                tokens.extend(new_tokens)
                col += consumed
                i += consumed
                continue
            
            # 未知字符
            raise LexerError(f"未知字符: '{source[i]}' (0x{ord(source[i]):04X})", line, col)
        
        # 文件结束，处理剩余的 DEDENT
        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, indent_stack[-1], line, col))
        
        tokens.append(Token(TokenType.EOF, None, line, col))
        return tokens
    
    def _is_han(self, ch: str) -> bool:
        """判断是否为汉字"""
        if not ch:
            return False
        cp = ord(ch)
        return self.HAN_START <= cp <= self.HAN_END
    
    def _is_same_type(self, ch1: str, ch2: str) -> bool:
        """判断两个字符是否属于同一类型（用于分词边界检测）"""
        if not ch1 or not ch2:
            return False
        
        # 汉字只能和汉字连续
        if self._is_han(ch1):
            return self._is_han(ch2)
        
        # 字母、数字、下划线可以连续（但汉字应该分开）
        if self._is_han(ch2):
            return False
        
        if ch1 == '_' or ch1.isalnum():
            return ch2 == '_' or ch2.isalnum()
        
        return False
    
    def _try_parse_chinese_number(self, source: str, pos: int):
        """
        尝试从指定位置解析完整的中文数字
        返回 (数值, 消耗长度) 或 (None, 0)
        """
        n = len(source)
        start = pos
        
        # 收集连续的汉字
        chars = []
        while pos < n and self._is_han(source[pos]):
            ch = source[pos]
            # 只收集中文数字相关的字符
            if ch in self.CHINESE_DIGITS or ch == '点':
                chars.append(ch)
                pos += 1
            else:
                break
        
        if not chars:
            return None, 0
        
        text = ''.join(chars)
        
        # 尝试解析为中文数字
        value = self._convert_chinese_number(text)
        if value is not None:
            return value, len(text)
        
        return None, 0

    def _convert_chinese_number(self, text: str):
        """
        将中文数字字符串转换为数值
        
        支持格式：
        - 整数：一、十二、三百二十一、一千零一
        - 小数：三点一四一五九、零点一
        """
        if not text:
            return None
        
        digits = self.CHINESE_DIGITS
        
        # 处理小数：X点Y
        if '点' in text:
            parts = text.split('点', 1)
            if len(parts) != 2:
                return None
            # 整数部分
            int_part = self._convert_chinese_integer(parts[0])
            if int_part is None:
                return None
            # 小数部分
            frac = 0
            frac_len = 0
            for ch in parts[1]:
                if ch in digits and digits[ch] < 10:  # 只取0-9的数字
                    frac = frac * 10 + digits[ch]
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
        
        digits = self.CHINESE_DIGITS
        
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
                    if temp > 0:
                        temp = temp * 10 + d  # 连续数字组成多位数（如"八五"→85）
                    else:
                        temp = d
            else:
                return None
        
        result += temp
        return result
    
    def _match_keyword(self, text: str, pos: int) -> Tuple[Optional[str], int]:
        """
        最长匹配关键字
        
        注意：compound_safe_single 中的单字关键字（如"典"）不应在独立上下文中匹配，
        仅当它们是更长关键字的组成部分时才使用。
        递归调用 _skip_compound_safe_and_match 处理这种情况。
        
        Returns:
            (匹配到的关键字, 匹配长度) 或 (None, 0)
        """
        return self._skip_compound_safe_and_match(text, pos)
    
    def _skip_compound_safe_and_match(self, text: str, pos: int) -> Tuple[Optional[str], int]:
        """尝试匹配关键字，遇到 compound_safe 关键字时跳过并继续匹配后续内容"""
        max_possible = min(self.all_max_keyword_len, len(text) - pos)
        
        # 从最长到最短尝试匹配
        for length in range(max_possible, 0, -1):
            candidates = self.all_keywords_by_length.get(length)
            if candidates:
                candidate = text[pos:pos+length]
                if candidate in candidates:
                    # 检查是否是 compound_safe_single 中的单字关键字
                    if (length == 1 and candidate in self.compound_safe_single_keywords
                            and pos + length < len(text)):
                        # 单字 compound_safe 关键字（如"典"），后面还有内容，
                        # 跳过它，尝试匹配后续内容
                        kw, l = self._skip_compound_safe_and_match(text, pos + 1)
                        if kw:
                            return kw, l
                        # 后续无法形成关键字，继续使用当前关键字
                    return candidate, length
        
        return None, 0
    
    def _try_match_symbol(self, source: str, i: int, line: int, col: int) -> Tuple[Optional[Token], int]:
        """尝试匹配符号"""
        ch = source[i]
        
        # 中文符号映射
        if ch in SYMBOL_MAP:
            mapped = SYMBOL_MAP[ch]
            token_type = self._symbol_token_map.get(mapped)
            if token_type:
                return Token(token_type, ch, line, col), 1
            # 其他符号
            return Token(TokenType.COMMA, ch, line, col), 1
        
        # 英文符号
        token_type = self._symbol_token_map.get(ch)
        if token_type:
            return Token(token_type, ch, line, col), 1
        
        # 管道操作符 ->
        if ch == '-' and i + 1 < len(source) and source[i+1] == '>':
            return Token(TokenType.ARROW, '->', line, col), 2
        
        return None, 0
    
    def _tokenize_string(self, source: str, i: int, line: int, col: int) -> Tuple[Token, int]:
        """处理字符串"""
        start_col = col
        quote_char = source[i]
        
        # 中文引号映射
        quote_map = {
            '「': '"', '」': '"',
            '『': "'", '』': "'",
        }
        
        if quote_char in quote_map:
            # 中文引号
            close_quote = {'「': '」', '『': '』'}.get(quote_char)
            
            j = i + 1
            chars = []
            while j < len(source) and source[j] != close_quote:
                chars.append(source[j])
                j += 1
            
            if j >= len(source):
                raise LexerError(f"字符串未闭合: 以 '{quote_char}' 开头的字符串缺少匹配的 '{close_quote}'", line, start_col)
            
            value = ''.join(chars)
            return Token(TokenType.STRING, value, line, start_col), j - i + 1
        else:
            # 英文引号
            j = i + 1
            chars = []
            while j < len(source) and source[j] != quote_char:
                if source[j] == '\\' and j + 1 < len(source):
                    next_ch = source[j + 1]
                    if next_ch == 'n':
                        chars.append('\n')
                    elif next_ch == 't':
                        chars.append('\t')
                    elif next_ch == 'r':
                        chars.append('\r')
                    elif next_ch == '\\':
                        chars.append('\\')
                    elif next_ch == quote_char:
                        chars.append(quote_char)
                    else:
                        chars.append(next_ch)
                    j += 2
                else:
                    chars.append(source[j])
                    j += 1
            
            if j >= len(source):
                raise LexerError(f"字符串未闭合: 以 '{quote_char}' 开头的字符串缺少匹配的引号", line, start_col)
            
            value = ''.join(chars)
            return Token(TokenType.STRING, value, line, start_col), j - i + 1
    
    def _tokenize_number(self, source: str, i: int, line: int, col: int) -> Tuple[Token, int]:
        """处理数字"""
        start = i
        j = i
        
        # 负号
        if source[j] == '-':
            j += 1
        
        # 整数部分
        while j < len(source) and source[j].isdigit():
            j += 1
        
        # 小数部分
        if j < len(source) and source[j] == '.':
            j += 1
            while j < len(source) and source[j].isdigit():
                j += 1
        
        num_str = source[start:j]
        if '.' in num_str:
            value = float(num_str)
        else:
            value = int(num_str)
        
        return Token(TokenType.NUMBER, value, line, col), j - start
    
    def _tokenize_chinese_number(self, source: str, i: int, line: int, col: int) -> Tuple[Token, int]:
        """处理中文数字（简单版：只处理一到十）"""
        ch = source[i]
        value = self.CHINESE_DIGITS.get(ch)
        
        if value is None:
            raise LexerError(f"无效的中文数字: {ch}", line, col)
        
        return Token(TokenType.CHINESE_NUM, value, line, col), 1
    
    def _tokenize_identifier_or_keyword(self, source: str, i: int, line: int, col: int, user_definitions: Set[str] = None) -> Tuple[List[Token], int]:
        """
        处理标识符和关键字（核心：三层分词机制）

        决策29：
        1. 类型切换自动分词 - 甲加1 → [甲] [加] [1]
        2. 双字关键词优先匹配 - 定义甲 → [定义] [甲]
        3. 元数驱动参数收集 - 打印 甲 → [打印] [甲]
        """
        if user_definitions is None:
            user_definitions = set()

        tokens = []
        start = i
        n = len(source)

        # 收集连续的汉字（或英文标识符）
        if self._is_han(source[i]):
            # 汉字处理：实现三层分词
            consumed = self._tokenize_chinese_sequence(source, i, line, col, tokens, user_definitions)
            
            # 处理汉字后紧跟ASCII字母/数字的情况（如"计算器1"）
            next_pos = i + consumed
            if next_pos < n:
                next_ch = source[next_pos]
                if next_ch.isascii() and (next_ch.isalnum() or next_ch == '_'):
                    j = next_pos
                    while j < n:
                        ch = source[j]
                        if ch.isascii() and (ch.isalnum() or ch == '_'):
                            j += 1
                        else:
                            break
                    suffix = source[next_pos:j]
                    # 将后缀合并到最后一个token（如果是标识符）
                    if tokens and tokens[-1].type == TokenType.IDENTIFIER:
                        tokens[-1] = Token(TokenType.IDENTIFIER, tokens[-1].value + suffix, tokens[-1].line, tokens[-1].col)
                        consumed += len(suffix)
            
            return tokens, consumed
        else:
            # 英文标识符：收集连续的字母、数字、下划线
            j = i + 1
            while j < n and (source[j].isalnum() or source[j] == '_'):
                j += 1
            
            word = source[i:j]
            if word in ALL_KEYWORDS:
                tokens.append(Token(TokenType.KEYWORD, word, line, col))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, word, line, col))
            
            return tokens, j - i
    
    def _tokenize_chinese_sequence(self, source: str, i: int, line: int, col: int, tokens: List[Token], user_definitions: Set[str] = None) -> int:
        """
        处理连续的汉字序列（实现三层分词）

        这是核心方法，实现决策29的三层机制
        """
        if user_definitions is None:
            user_definitions = set()

        n = len(source)
        consumed = 0
        current_col = col
        
        # 安全计数器，防止无限循环
        _loop_safety = 0

        while i + consumed < n:
            _loop_safety += 1
            if _loop_safety > 100:
                raise RuntimeError(f"词法分析内部错误: 汉字序列分词超出安全上限 ({_loop_safety}次迭代), 当前位置: {i + consumed}")

            pos = i + consumed
            ch = source[pos]

            # 遇到非汉字，结束
            if not self._is_han(ch):
                break

            # 遇到符号，结束
            if ch in SYMBOL_MAP or ch in '。：；，（）【】':
                break

            # 检查是否是简单中文数字（一～十）
            if ch in self.SIMPLE_CHINESE_NUMBERS:
                # 检查下一个位置是否是关键字或符号
                next_pos = pos + 1

                # 情况1：下一个字符不是汉字（如 "三。" 中的 "。"）
                # 情况2：下一个字符是关键字（如 "三加" 中的 "加"）
                # 情况3：下一个字符是符号
                # 在这些情况下，当前中文数字应该独立输出

                is_standalone_num = False

                if next_pos >= n:
                    # 到达字符串末尾
                    is_standalone_num = True
                elif not self._is_han(source[next_pos]):
                    # 下一个字符不是汉字
                    is_standalone_num = True
                else:
                    # 检查下一个位置是否能匹配关键字
                    next_keyword, _ = self._match_keyword(source, next_pos)
                    if next_keyword:
                        # 下一个是关键字，当前数字独立
                        is_standalone_num = True
                    elif source[next_pos] in SYMBOL_MAP or source[next_pos] in '。：；，（）【】':
                        # 下一个是符号
                        is_standalone_num = True

                if is_standalone_num:
                    # 单独的中文数字，输出为数字
                    value = self.CHINESE_DIGITS[ch]
                    tokens.append(Token(TokenType.CHINESE_NUM, value, line, current_col))
                    consumed += 1
                    current_col += 1
                    continue

            # 先收集完整的汉字序列
            j = pos
            while j < n and self._is_han(source[j]):
                # 遇到符号停止
                if source[j] in SYMBOL_MAP or source[j] in '。：；，（）【】':
                    break
                j += 1
            
            full_identifier = source[pos:j]
            
            # 检查是否是中文数字（如三点一四一五九、一百零一）
            if full_identifier:
                num_value, num_len = self._try_parse_chinese_number(source, pos)
                if num_value is not None and num_len == len(full_identifier):
                    # 整个标识符是中文数字
                    tokens.append(Token(TokenType.CHINESE_NUM, num_value, line, current_col))
                    consumed += num_len
                    current_col += num_len
                    continue
                elif num_value is not None and num_len > 0:
                    # 前缀是中文数字（如"九十那么"中的"九十"）
                    # 输出CHINESE_NUM，剩余部分由后续循环处理
                    tokens.append(Token(TokenType.CHINESE_NUM, num_value, line, current_col))
                    consumed += num_len
                    current_col += num_len
                    continue
            
            # 检查完整标识符是否是常见复合词
            if full_identifier in COMMON_COMPOUND_WORDS:
                # 常见复合词，作为整体标识符，不拆分
                tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                consumed += len(full_identifier)
                current_col += len(full_identifier)
                continue
            
            # 检查完整标识符是否在用户定义中
            if full_identifier in user_definitions:
                # 完整标识符在用户定义中，优先作为标识符，不拆分
                tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                consumed += len(full_identifier)
                current_col += len(full_identifier)
                continue
            
            # 检查前缀是否在用户定义中（如"阶乘结果"在定义中，当前标识符为"阶乘结果等于"）
            if user_definitions:
                prefix_matched = None
                for plen in range(len(full_identifier) - 1, 0, -1):
                    prefix = full_identifier[:plen]
                    if prefix in user_definitions:
                        prefix_matched = prefix
                        break
                if prefix_matched:
                    # 输出用户定义的前缀部分作为标识符，剩余部分由后续循环处理
                    tokens.append(Token(TokenType.IDENTIFIER, prefix_matched, line, current_col))
                    consumed += len(prefix_matched)
                    current_col += len(prefix_matched)
                    continue
            
            # 第一层：尝试最长匹配关键字
            keyword, length = self._match_keyword(source, pos)
            
            # 再次检查单个关键字是否在用户定义中
            if keyword and keyword in user_definitions:
                # 用户定义的标识符，不作为关键字
                keyword = None

            if keyword:
                # 单字动词在词首且词长>1时不直接匹配，避免拆开复合词
                # 例如"列表"(len=2)不应拆为 列(动词)+表
                # 但独立出现的"加"(len=1)仍应匹配为关键字
                # 例外：后续字符是中文数字（如"加五"），应拆分为 加(动词)+五(数字)
                # 另外：只有当关键字在词首位置时才跳过，词中出现的运算符应正常识别
                skip_verb = False
                if length == 1 and keyword in self.compound_safe_single_keywords and len(full_identifier) > 1:
                    # 检查是否在词首位置（相对于 full_identifier）
                    in_word_start = (pos == i + consumed)  # 当前位置是当前处理的起始位置
                    if in_word_start:
                        # 检查后续字符是否构成中文数字
                        remaining = full_identifier[1:]
                        is_chinese_num = False
                        if len(remaining) == 1 and remaining[0] in self.SIMPLE_CHINESE_NUMBERS:
                            is_chinese_num = True
                        else:
                            num_val, num_len = self._try_parse_chinese_number(remaining, 0)
                            if num_val is not None and num_len >= len(remaining):
                                is_chinese_num = True
                        if not is_chinese_num:
                            skip_verb = True
                
                # 特殊处理："当"关键字只在后面跟着冒号或在标识符开头时才作为关键字
                # 否则作为复合词的一部分（如"当前时间戳"中的"当"）
                if length == 1 and keyword == '当':
                    # 检查整个汉字序列后面的字符
                    word_end_pos = i + consumed + len(full_identifier)
                    if word_end_pos < len(source):
                        word_next_char = source[word_end_pos]
                        # 如果整个汉字序列后面是冒号，"当"作为关键字
                        if word_next_char == ':':
                            # 作为关键字处理，不跳过
                            pass
                        else:
                            # 检查"当"后面是否紧跟非汉字字符（如空格、符号等）
                            next_pos = pos + length
                            if next_pos < len(source):
                                next_char = source[next_pos]
                                # 如果"当"后面是冒号或空格，作为关键字
                                if next_char == ':' or next_char.isspace():
                                    pass
                                else:
                                    # 否则作为复合词的一部分
                                    skip_verb = True
                
                if skip_verb:
                    # 单字动词在多字词词首，跳过主匹配，让嵌入式检测处理
                    keyword = None
                else:
                    # 匹配到关键字（非单字动词或不在词首）
                    tokens.append(Token(TokenType.KEYWORD, keyword, line, current_col))
                    consumed += length
                    current_col += length
            
            if not keyword:
                # 未匹配到关键字（或单字动词被跳过），检查是否内嵌有关键字
                # 例如"初始值加数值"中的"加"应该被识别为关键字
                embedded_found = False
                scan_pos = 0
                while scan_pos < len(full_identifier):
                    sub_kw, sub_len = self._match_keyword(source, i + consumed + scan_pos)
                    if sub_kw and sub_kw not in user_definitions:
                        embedded_found = True
                        break
                    scan_pos += 1
                
                if embedded_found:
                    # 有内嵌关键字，分段输出
                    scan_pos = 0
                    while scan_pos < len(full_identifier):
                        abs_pos = i + consumed + scan_pos
                        sub_kw, sub_len = self._match_keyword(source, abs_pos)
                        if sub_kw and sub_kw not in user_definitions:
                            # 跳过 compound_safe_single 的单字关键字（如"典"），继续扫描
                            # 这允许"字典创建"中的"典"被跳过，从而识别"创建"为关键字
                            # 对于运算符动词（加、减、乘、除、模、幂）：
                            # - 如果后面跟着普通汉字，作为复合词的一部分，跳过
                            # - 如果后面跟着数字或符号，作为运算符识别
                            # 特殊处理："当"关键字只在后面跟着冒号时才作为关键字
                            if sub_len == 1 and sub_kw == '当':
                                # 检查后面是否是冒号
                                next_pos = abs_pos + sub_len
                                if next_pos < len(source):
                                    next_char = source[next_pos]
                                    # 只有当后面是冒号或空格时，才作为关键字
                                    if next_char != ':' and not next_char.isspace():
                                        scan_pos += sub_len
                                        continue
                            elif sub_len == 1 and sub_kw in self.compound_safe_single_keywords:
                                # 检查是否是运算符动词
                                if sub_kw in OPERATOR_VERBS:
                                    # 检查后面是否是普通汉字（不是数字或符号）
                                    next_pos = abs_pos + sub_len
                                    if next_pos < len(source):
                                        next_char = source[next_pos]
                                        # 如果后面是普通汉字，作为复合词一部分，跳过
                                        if self._is_han(next_char) and next_char not in self.SIMPLE_CHINESE_NUMBERS:
                                            scan_pos += sub_len
                                            continue
                                    # 否则作为运算符识别，不跳过
                                else:
                                    scan_pos += sub_len
                                    continue
                            # 输出关键字前的标识符部分
                            if scan_pos > 0:
                                id_part = full_identifier[:scan_pos]
                                num_value = self._convert_chinese_number(id_part)
                                if num_value is not None:
                                    tokens.append(Token(TokenType.CHINESE_NUM, num_value, line, current_col))
                                else:
                                    tokens.append(Token(TokenType.IDENTIFIER, id_part, line, current_col))
                                consumed += scan_pos
                                current_col += scan_pos
                                full_identifier = full_identifier[scan_pos:]
                                scan_pos = 0
                                abs_pos = i + consumed
                                sub_kw, sub_len = self._match_keyword(source, abs_pos)
                                if not (sub_kw and sub_kw not in user_definitions):
                                    break
                                if sub_len == 1 and sub_kw in self.compound_safe_single_keywords:
                                    scan_pos += sub_len
                                    continue
                            # 输出关键字
                            tokens.append(Token(TokenType.KEYWORD, sub_kw, line, current_col))
                            consumed += sub_len
                            current_col += sub_len
                            full_identifier = full_identifier[sub_len:]
                            scan_pos = 0
                        else:
                            scan_pos += 1
                    # 输出剩余标识符部分
                    if full_identifier:
                        num_value, num_len = self._try_parse_chinese_number(source, i + consumed)
                        if num_value is not None and num_len == len(full_identifier):
                            tokens.append(Token(TokenType.CHINESE_NUM, num_value, line, current_col))
                            consumed += num_len
                            current_col += num_len
                        else:
                            tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                            consumed += len(full_identifier)
                            current_col += len(full_identifier)
                else:
                    # 无嵌入关键字，使用前面收集的完整标识符
                    if full_identifier:
                        # 尝试解析为中文数字（支持多位如"四十二"、"一百"）
                        num_value, num_len = self._try_parse_chinese_number(source, i + consumed)
                        if num_value is not None and num_len == len(full_identifier):
                            tokens.append(Token(TokenType.CHINESE_NUM, num_value, line, current_col))
                            consumed += num_len
                            current_col += num_len
                        else:
                            tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                            consumed += len(full_identifier)
                            current_col += len(full_identifier)
                    else:
                        # 单个非关键字汉字，检查是否为中文数字
                        if ch in self.SIMPLE_CHINESE_NUMBERS:
                            value = self.CHINESE_DIGITS[ch]
                            tokens.append(Token(TokenType.CHINESE_NUM, value, line, current_col))
                        else:
                            tokens.append(Token(TokenType.IDENTIFIER, ch, line, current_col))
                        consumed += 1
                        current_col += 1
        
        return consumed
    
    def _scan_user_definitions(self, source: str) -> Set[str]:
        """
        预扫描：收集用户定义的变量名和函数名

        用于避免将用户定义的标识符错误拆分为关键字
        """
        definitions = set()
        i = 0
        n = len(source)

        # 安全计数器（防止意外死循环）
        _scan_safety = 0

        while i < n:
            _scan_safety += 1
            if _scan_safety > 50000:
                raise RuntimeError(f"_scan_user_definitions 超出安全上限 ({_scan_safety}次迭代), i={i}, n={n}")
            
            # 查找段落定义：《段名》段 或 《类名》类 或 《方法名》方法(参数)
            if source[i] == '《':
                j = i + 1
                # 收集段名/类名/方法名
                k = j
                while k < n and source[k] != '》':
                    k += 1
                if k < n and k > j:
                    name = source[j:k]
                    # 《Name》段 或 《Name》类
                    next_start = k + 1
                    if next_start < n:
                        # 检查后跟"方法("：收集括号内的参数名，并注册方法名
                        if source[next_start:next_start+2] == '方法' and next_start+2 < n and source[next_start+2] == '(':
                            # 注册方法名（如"添加成绩"、"打印信息"）
                            if name not in ALL_KEYWORDS and name not in VERB_ARITY:
                                definitions.add(name)
                            # 收集括号内的参数
                            p = next_start + 3  # 跳过 方法(
                            while p < n and source[p] != ')':
                                # 跳过空白
                                if source[p] in ' \t':
                                    p += 1
                                    continue
                                # 跳过逗号
                                if source[p] == ',' or source[p] == '，':
                                    p += 1
                                    continue
                                # 收集参数名
                                param_start = p
                                while p < n and self._is_han(source[p]) and source[p] not in '，, )）':
                                    p += 1
                                if p > param_start:
                                    param_name = source[param_start:p]
                                    if param_name not in ALL_KEYWORDS:
                                        definitions.add(param_name)
                                else:
                                    # 非汉字的参数（如ASCII字符'x'），向前移动一位避免死循环
                                    p += 1
                        elif name not in ALL_KEYWORDS and name not in VERB_ARITY:
                            definitions.add(name)
                i = k + 1
                continue
            
            # 查找 "段落 段名 参数 参数名" 格式
            if source[i:i+2] == '段落':
                j = i + 2
                # 跳过空白
                while j < n and source[j] in ' \t':
                    j += 1
                # 收集段名
                k = j
                while k < n and self._is_han(source[k]):
                    k += 1
                if k > j:
                    segment_name = source[j:k]
                    # 收集段落名（允许覆盖动词名称）
                    if segment_name not in ALL_KEYWORDS:
                        definitions.add(segment_name)
                
                # 检查是否有 "参数" 关键字
                j = k
                while j < n and source[j] in ' \t':
                    j += 1
                if source[j:j+2] == '参数':
                    j += 2
                    # 跳过空白
                    while j < n and source[j] in ' \t':
                        j += 1
                    # 收集参数名（可能多个参数）
                    while j < n:
                        k = j
                        while k < n and self._is_han(source[k]) and source[k] not in '。：':
                            k += 1
                        if k > j:
                            param_name = source[j:k]
                            # 排除关键字和动词
                            if param_name not in ALL_KEYWORDS and param_name not in VERB_ARITY:
                                definitions.add(param_name)
                        j = k
                        # 跳过空白
                        while j < n and source[j] in ' \t':
                            j += 1
                        # 检查是否结束（句号、冒号或换行）
                        if j >= n or source[j] in '。：\n':
                            break
                i = j
                continue
            
            # 查找 "定义" 或 "设" 开头的定义语句
            if source[i:i+2] == '定义':
                j = i + 2
                # 跳过空白
                while j < n and source[j] in ' \t':
                    j += 1
                # 收集标识符（收集到赋值关键字"等于"/"为"为止，动词允许在变量名内）
                k = j
                # we just started at k, scan until we find the breakpoint
                start_k = k
                while k < n and self._is_han(source[k]):
                    # check if current position has a keyword that should break
                    next_kw, length = self._match_keyword(source, k)
                    if next_kw:
                        if next_kw in ALL_KEYWORDS:
                            # 真正的关键字（如"定义"），作为断点
                            break
                        if next_kw in ('等于', '为'):
                            # 赋值运算符，作为断点
                            break
                    # If we get here, the keyword doesn't break us
                    # so advance normally
                    if next_kw:
                        k += length
                    else:
                        k += 1
                if k > j:
                    name = source[j:k]
                    # 只排除真正的关键字，动词可以作为变量名的一部分
                    if name not in ALL_KEYWORDS:
                        definitions.add(name)
                i = k
            elif source[i] == '设':
                j = i + 1
                # 跳过空白
                while j < n and source[j] in ' \t':
                    j += 1
                # 收集标识符（设 甲 为 值）
                k = j
                collected_something = False
                while k < n and self._is_han(source[k]):
                    # 只检查是否遇到"为"关键字（跳过空格），动词在开头时可跳过
                    lookahead = k
                    while lookahead < n and source[lookahead] in ' \t':
                        lookahead += 1
                    if lookahead < n and source[lookahead] == '为':
                        break
                    # 在开头遇到动词（如"设阶乘结果为五"），跳过
                    next_kw, length = self._match_keyword(source, k)
                    if next_kw and next_kw in VERB_ARITY and not collected_something:
                        k += length
                        continue
                    k += 1
                    collected_something = True
                if k > j:
                    name = source[j:k]
                    # 只排除真正的关键字，动词可以作为变量名的一部分
                    if name not in ALL_KEYWORDS:
                        definitions.add(name)
                i = k
            else:
                i += 1

        return definitions
