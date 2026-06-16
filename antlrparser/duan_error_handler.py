#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言（Duan）编程语言 - 中文错误处理器

将ANTLR原始错误信息转换为友好的中文提示
"""

import sys
from typing import List, Optional
from antlr4.error.ErrorListener import ErrorListener


class ChineseErrorListener(ErrorListener):
    """中文错误监听器"""
    
    def __init__(self):
        super().__init__()
        self.errors: List[str] = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """语法错误处理"""
        error_msg = self._translate_error(msg, line, column, offendingSymbol)
        self.errors.append(error_msg)
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[str]:
        """获取所有错误"""
        return self.errors
    
    def _translate_error(self, msg: str, line: int, column: int, offendingSymbol) -> str:
        """翻译错误信息"""
        # 获取错误符号文本
        symbol_text = offendingSymbol.text if offendingSymbol else "未知"
        
        # 常见错误模式匹配
        if "mismatched input" in msg:
            expected = self._extract_expected(msg)
            return f"[语法错误] 第{line}行，第{column}列：意外的符号 '{symbol_text}'，期望 {expected}"
        
        elif "missing" in msg:
            missing = self._extract_missing(msg)
            return f"[语法错误] 第{line}行，第{column}列：缺少符号 '{missing}'"
        
        elif "extraneous input" in msg:
            return f"[语法错误] 第{line}行，第{column}列：多余的符号 '{symbol_text}'"
        
        elif "no viable alternative" in msg:
            return f"[语法错误] 第{line}行，第{column}列：无法识别的语法结构，符号 '{symbol_text}'"
        
        elif "token recognition error" in msg:
            return f"[词法错误] 第{line}行，第{column}列：无法识别的字符 '{symbol_text}'"
        
        else:
            # 默认格式
            return f"[错误] 第{line}行，第{column}列：{self._clean_msg(msg)}"
    
    def _extract_expected(self, msg: str) -> str:
        """提取期望的符号"""
        if "expecting" in msg:
            parts = msg.split("expecting")
            if len(parts) > 1:
                expected = parts[1].strip().strip('{}')
                # 翻译常见符号
                expected = self._translate_symbols(expected)
                return expected
        return "有效符号"
    
    def _extract_missing(self, msg: str) -> str:
        """提取缺失的符号"""
        if "missing" in msg:
            parts = msg.split("missing")
            if len(parts) > 1:
                missing = parts[1].split("at")[0].strip()
                return self._translate_symbols(missing)
        return "符号"
    
    def _translate_symbols(self, symbols: str) -> str:
        """翻译符号名称"""
        translations = {
            'ID': '标识符',
            'NUMBER': '数字',
            'STRING': '字符串',
            'LPAREN': '(',
            'RPAREN': ')',
            'LBRACKET': '[',
            'RBRACKET': ']',
            'COLON': '：',
            'PERIOD': '。',
            'COMMA': '，',
            'K_SET': '设',
            'K_AS': '为',
            'K_SEGMENT': '段落',
            'K_RECEIVE': '接收',
            'K_RETURN': '返回',
            'K_IF': '如果',
            'K_ELSE': '否则',
            'K_WHILE': '当',
            'K_FOREACH': '遍历',
            'K_CLASS': '类',
            'K_NEW': '新建',
            'K_PRINT': '打印',
        }
        
        for eng, chn in translations.items():
            symbols = symbols.replace(eng, chn)
        
        return symbols
    
    def _clean_msg(self, msg: str) -> str:
        """清理错误消息"""
        # 移除技术细节
        msg = msg.replace("at input", "在输入")
        msg = msg.replace("mismatched input", "不匹配的输入")
        msg = msg.replace("expecting", "期望")
        return msg


class DuanError(Exception):
    """段言错误基类"""
    
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """格式化错误消息"""
        if self.line is not None and self.column is not None:
            return f"{self.message}（第{self.line}行，第{self.column}列）"
        return self.message


class LexerError(DuanError):
    """词法错误"""
    pass


class ParserError(DuanError):
    """语法错误"""
    pass


class SemanticError(DuanError):
    """语义错误"""
    pass


class CodeGenError(DuanError):
    """代码生成错误"""
    pass


class RuntimeError(DuanError):
    """运行时错误"""
    pass


def format_error_context(source: str, line: int, column: int, context_lines: int = 2) -> str:
    """
    格式化错误上下文
    
    Args:
        source: 源代码
        line: 错误行号（从1开始）
        column: 错误列号（从0开始）
        context_lines: 显示的上下文行数
    
    Returns:
        格式化的错误上下文字符串
    """
    lines = source.split('\n')
    start = max(0, line - context_lines - 1)
    end = min(len(lines), line + context_lines)
    
    result = []
    for i in range(start, end):
        line_num = i + 1
        prefix = "→ " if line_num == line else "  "
        result.append(f"{prefix}{line_num:4d} | {lines[i]}")
        
        if line_num == line:
            # 添加错误指示
            pointer = " " * (len(prefix) + 7 + column) + "^"
            result.append(pointer)
    
    return '\n'.join(result)


def suggest_fix(error_type: str, symbol: str, context: str = "") -> Optional[str]:
    """
    根据错误类型提供修复建议
    
    Args:
        error_type: 错误类型
        symbol: 错误符号
        context: 上下文
    
    Returns:
        修复建议字符串
    """
    suggestions = {
        'missing_LPAREN': f"提示：函数调用需要括号，尝试改为 {symbol}()",
        'missing_RPAREN': f"提示：缺少右括号，检查括号是否配对",
        'missing_COLON': f"提示：代码块开始需要冒号 '：'",
        'missing_PERIOD': f"提示：语句结束需要句号 '。'",
        'mismatched_ID': f"提示：期望标识符，'{symbol}' 可能是关键字",
        'unexpected_symbol': f"提示：符号 '{symbol}' 在此处不合法",
    }
    
    key = f"{error_type}_{symbol}" if symbol else error_type
    return suggestions.get(key) or suggestions.get(error_type)
