"""
段言（Duan）编程语言 - 语法解析器核心框架

提供基础解析框架：
- 词法分析集成
- Token 流管理
- 辅助方法（_current, _consume, _match, _peek）
- 操作符映射表
"""

from typing import List, Any, Optional, Dict, Union
from lexer import Lexer, LexerError
from tokens import Token, TokenType
from keywords import VERB_ARITY, KEYWORDS_DOUBLE, KEYWORDS_SPECIAL
from ast_nodes_v3 import *
import sys


# =============================================================================
# 解析错误类
# =============================================================================

class ParseError(Exception):
    """语法解析错误"""
    def __init__(self, message: str, line: int = 0, col: int = 0, token_value: str = None, source_lines: list = None):
        self.message = message
        self.line = line
        self.col = col
        self.token_value = token_value
        self.source_lines = source_lines or []
        
        parts = []
        
        # 错误类型（带颜色标记）
        parts.append("\n┌─ 语法错误")
        
        # 位置信息
        if line:
            pos_info = f"行 {line}"
            if col:
                pos_info += f", 列 {col}"
            parts.append(f"│ 位置: {pos_info}")
        
        # 源代码上下文
        if line and self.source_lines:
            parts.append("│")
            for i in range(max(0, line - 2), min(len(self.source_lines), line + 1)):
                line_num = i + 1
                line_content = self.source_lines[i].rstrip()
                prefix = "│ " if line_num != line else "│→"
                parts.append(f"{prefix} {line_num:4d} │ {line_content}")
                # 在错误列位置添加指示符
                if line_num == line and col:
                    parts.append(f"│       │ {' ' * (min(col, 60) - 1)}^ 错误在这里")
        
        # 错误信息
        parts.append(f"│ 原因: {message}")
        if token_value:
            parts.append(f"│ 附近: '{token_value}'")
        
        parts.append("└─")
        
        super().__init__('\n'.join(parts))


# =============================================================================
# 递归下降解析器 - 核心基类
# =============================================================================

class DuanParserCore:
    """段言完整语法解析器核心基类"""
    
    # 运算符动词集合（类常量，避免重复创建）
    OPERATOR_VERBS = frozenset({'加', '减', '乘', '除', '加上', '减去', '乘以', '除以', 
                                '大于', '小于', '等于', '不等于', '大于等于', '小于等于',
                                '不小于', '不大于',  # P2-3：比较运算符短形式
                                '模', '幂', '为'})
    
    # 操作符映射表（类常量）
    COMPARISON_OP_MAP = {
        '大于': '>', '小于': '<', '等于': '==',
        '不等于': '!=', '大于等于': '>=', '小于等于': '<=',
        '不小于': '>=', '不大于': '<=',  # P2-3：比较运算符短形式
        '为': '==',
    }
    ADD_OP_MAP = {'加': '+', '减': '-', '加上': '+', '减去': '-'}
    MUL_OP_MAP = {'乘': '*', '除': '/', '模': '%', '乘以': '*', '除以': '/', '模以': '%', '取余': '%', '整除': '//'}
    POWER_OP_MAP = {'幂': '**', '幂以': '**'}
    LOGICAL_OP_MAP = {'且': 'and', '与': 'and', '或': 'or'}
    
    def __init__(self):
        self.lexer = Lexer()
        self.tokens: List[Token] = []
        self.pos = 0

    def _error(self, message: str, line: int = 0, col: int = 0, token_value: str = None):
        """报告解析错误（抛出 ParseError）"""
        raise ParseError(message, line, col, token_value)
    
    def parse(self, source: str) -> Module:
        """解析段言代码"""
        # 词法分析
        tokens = self.lexer.tokenize(source)
        
        # 过滤掉 EOF，保留 NEWLINE、INDENT/DEDENT 用于块结构解析
        self.tokens = [t for t in tokens if t.type != TokenType.EOF]
        self.pos = 0
        
        # 解析模块
        return self._parse_module()
    
    def _current(self) -> Optional[Token]:
        """获取当前 Token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _peek(self, offset: int = 0) -> Optional[Token]:
        """查看指定位置的 Token"""
        idx = self.pos + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def _consume(self, expected_type=None, expected_value=None) -> Token:
        """消耗并返回当前 Token"""
        tok = self._current()
        if tok is None:
            last_tok = self.tokens[-1] if self.tokens else None
            line = last_tok.line if last_tok else 0
            col = last_tok.col if last_tok else 0
            hint = ""
            if expected_type:
                hint = f" (期望 {expected_type}"
                if expected_value:
                    hint += f" = '{expected_value}'"
                hint += ")"
            raise ParseError(f"输入意外结束{hint}（建议检查是否缺少表达式或语句）", line, col)
        
        if expected_type and tok.type != expected_type:
            raise ParseError(f"期望 {expected_type}，但得到 {tok.type}（附近: '{tok.value}'）", tok.line, tok.col, tok.value)
        
        if expected_value and tok.value != expected_value:
            raise ParseError(f"期望'{expected_value}'，但得到'{tok.value}'（附近: '{tok.value}'）", tok.line, tok.col)
        
        self.pos += 1
        return tok
    
    def _match(self, token_type, value=None) -> bool:
        """检查当前 Token 是否匹配"""
        tok = self._current()
        if tok is None:
            return False
        if tok.type != token_type:
            return False
        if value is not None and tok.value != value:
            return False
        return True
    
    # =========================================================================
    # 段落/函数 关键字兼容辅助方法
    # '函数' 是首选关键字，'段落' 和 '段' 是向后兼容别名
    # =========================================================================
    
    PARAGRAPH_KEYWORDS = frozenset({'函数', '段落', '段'})
    
    def _is_paragraph_kw(self, tok: Optional[Token]) -> bool:
        """检查 token 是否是段落/函数定义关键字（函数/段落/段）"""
        return tok is not None and tok.type == TokenType.KEYWORD and tok.value in self.PARAGRAPH_KEYWORDS
    
    def _match_paragraph_kw(self) -> bool:
        """检查当前 token 是否是段落/函数定义关键字（函数/段落/段）"""
        return self._is_paragraph_kw(self._current())
    
    def _consume_paragraph_kw(self) -> Token:
        """消耗段落/函数定义关键字（函数/段落/段），返回该 token"""
        tok = self._current()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in self.PARAGRAPH_KEYWORDS:
            self.pos += 1
            return tok
        raise ParseError(
            f"期望'函数'（或兼容写法'段落'/'段'），但得到 {tok.type if tok else '输入结束'}"
            f"（附近: '{tok.value if tok else ''}'）",
            tok.line if tok else 0, tok.col if tok else 0, tok.value if tok else None
        )