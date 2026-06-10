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


class LexerError(Exception):
    """词法分析错误"""
    def __init__(self, message: str, line: int, col: int):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"词法错误 (行{line}, 列{col}): {message}")


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
    
    # 简单中文数字（一到十）
    SIMPLE_CHINESE_NUMBERS = {'一', '二', '三', '四', '五', '六', '七', '八', '九', '十'}
    
    def __init__(self):
        """初始化词法分析器"""
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
    
    def tokenize(self, source: str) -> List[Token]:
        """将源码转为 Token 流"""
        tokens = []
        i = 0
        line = 1
        col = 1
        n = len(source)

        # 预扫描：收集用户定义的标识符
        user_definitions = self._scan_user_definitions(source)

        # 处理缩进
        indent_stack = [0]

        while i < n:
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
                        raise LexerError("段落名未闭合", line, col)
                    
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
            
            # 处理中文数字
            if source[i] in self.SIMPLE_CHINESE_NUMBERS:
                token, consumed = self._tokenize_chinese_number(source, i, line, col)
                tokens.append(token)
                col += consumed
                i += consumed
                continue
            
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
            raise LexerError(f"未知字符: {source[i]}", line, col)
        
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
    
    def _match_keyword(self, text: str, pos: int) -> Tuple[Optional[str], int]:
        """
        最长匹配关键字
        
        Returns:
            (匹配到的关键字, 匹配长度) 或 (None, 0)
        """
        max_possible = min(self.all_max_keyword_len, len(text) - pos)
        
        # 从最长到最短尝试匹配
        for length in range(max_possible, 0, -1):
            if length in self.all_keywords_by_length:
                candidate = text[pos:pos+length]
                if candidate in self.all_keywords_by_length[length]:
                    return candidate, length
        
        return None, 0
    
    def _try_match_symbol(self, source: str, i: int, line: int, col: int) -> Tuple[Optional[Token], int]:
        """尝试匹配符号"""
        ch = source[i]
        
        # 中文符号映射
        if ch in SYMBOL_MAP:
            mapped = SYMBOL_MAP[ch]
            if mapped == '.':
                return Token(TokenType.DOT, ch, line, col), 1
            elif mapped == ',':
                return Token(TokenType.COMMA, ch, line, col), 1
            elif mapped == ';':
                return Token(TokenType.SEMICOLON, ch, line, col), 1
            elif mapped == ':':
                return Token(TokenType.COLON, ch, line, col), 1
            elif mapped == '(':
                return Token(TokenType.LPAREN, ch, line, col), 1
            elif mapped == ')':
                return Token(TokenType.RPAREN, ch, line, col), 1
            elif mapped == '[':
                return Token(TokenType.LBRACKET, ch, line, col), 1
            elif mapped == ']':
                return Token(TokenType.RBRACKET, ch, line, col), 1
            elif mapped == '<':
                # 左书名号 《
                return Token(TokenType.LBOOK, ch, line, col), 1
            elif mapped == '>':
                # 右书名号 》
                return Token(TokenType.RBOOK, ch, line, col), 1
        
        # 英文符号
        if ch == '.':
            return Token(TokenType.DOT, ch, line, col), 1
        elif ch == ',':
            return Token(TokenType.COMMA, ch, line, col), 1
        elif ch == ';':
            return Token(TokenType.SEMICOLON, ch, line, col), 1
        elif ch == ':':
            return Token(TokenType.COLON, ch, line, col), 1
        elif ch == '(':
            return Token(TokenType.LPAREN, ch, line, col), 1
        elif ch == ')':
            return Token(TokenType.RPAREN, ch, line, col), 1
        elif ch == '[':
            return Token(TokenType.LBRACKET, ch, line, col), 1
        elif ch == ']':
            return Token(TokenType.RBRACKET, ch, line, col), 1
        elif ch == '=':
            return Token(TokenType.EQUALS, ch, line, col), 1
        
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
            if not close_quote:
                raise LexerError(f"未闭合的引号: {quote_char}", line, col)
            
            j = i + 1
            chars = []
            while j < len(source) and source[j] != close_quote:
                chars.append(source[j])
                j += 1
            
            if j >= len(source):
                raise LexerError(f"字符串未闭合", line, start_col)
            
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
                raise LexerError("字符串未闭合", line, start_col)
            
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

        while i + consumed < n:
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
            
            # 检查完整标识符是否在用户定义中
            if full_identifier in user_definitions:
                # 完整标识符在用户定义中，优先作为标识符，不拆分
                tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                consumed += len(full_identifier)
                current_col += len(full_identifier)
                continue
            
            # 第一层：尝试最长匹配关键字
            keyword, length = self._match_keyword(source, pos)
            
            # 再次检查单个关键字是否在用户定义中
            if keyword and keyword in user_definitions:
                # 用户定义的标识符，不作为关键字
                keyword = None

            if keyword:
                # 匹配到关键字
                tokens.append(Token(TokenType.KEYWORD, keyword, line, current_col))
                consumed += length
                current_col += length
            else:
                # 未匹配到关键字，收集标识符
                # 使用前面收集的完整标识符
                if full_identifier:
                    tokens.append(Token(TokenType.IDENTIFIER, full_identifier, line, current_col))
                    consumed += len(full_identifier)
                    current_col += len(full_identifier)
                else:
                    # 单个非关键字汉字
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

        while i < n:
            # 查找段落定义：《段名》段 或 "段落 段名 参数 参数名"
            if source[i] == '《':
                j = i + 1
                # 收集段名
                k = j
                while k < n and source[k] != '》':
                    k += 1
                if k < n and k > j:
                    definitions.add(source[j:k])
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
                    definitions.add(source[j:k])
                
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
                        while k < n and self._is_han(source[k]) and source[k] not in '。':
                            k += 1
                        if k > j:
                            param_name = source[j:k]
                            definitions.add(param_name)
                        j = k
                        # 跳过空白
                        while j < n and source[j] in ' \t':
                            j += 1
                        # 检查是否结束
                        if j >= n or source[j] == '。':
                            break
                i = j
                continue
            
            # 查找 "定义" 或 "设" 开头的定义语句
            if source[i:i+2] == '定义':
                j = i + 2
                # 跳过空白
                while j < n and source[j] in ' \t':
                    j += 1
                # 收集标识符（只收集到下一个关键字或符号）
                k = j
                while k < n and self._is_han(source[k]):
                    # 检查是否遇到关键字
                    next_kw, length = self._match_keyword(source, k)
                    if next_kw and next_kw in ALL_KEYWORDS:
                        # 遇到关键字，停止
                        break
                    k += 1
                if k > j:
                    definitions.add(source[j:k])
                i = k
            elif source[i] == '设':
                j = i + 1
                # 收集标识符（设甲为三）
                while j < n and self._is_han(source[j]):
                    # 检查是否遇到关键字
                    if source[j:j+2] == '为':
                        break
                    j += 1
                if j > i + 1:
                    definitions.add(source[i+1:j])
                i = j
            else:
                i += 1

        return definitions
