#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')
sys.path.insert(0, 'antlrparser')

from antlrparser.duan_tokenizer import create_antlr_token_stream
from antlrparser.DuanLangLexer import DuanLangLexer
from antlrparser.DuanLangParser import DuanLangParser

code = '设 甲 为 3。'
print('Testing code:', repr(code))

# 创建 token stream
token_stream = create_antlr_token_stream(code, DuanLangLexer)
print('Token stream created')

# 创建 parser
parser = DuanLangParser(token_stream)
print('Parser created')

# 设置错误监听器
from antlr4.error.ErrorListener import ErrorListener
class MyErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        error_msg = f"行{line}, 列{column}: {msg}"
        self.errors.append(error_msg)
        print(f"Syntax error: {error_msg}")

error_listener = MyErrorListener()
parser.removeErrorListeners()
parser.addErrorListener(error_listener)

# 尝试解析
try:
    tree = parser.program()
    print('Parse successful!')
    print('Tree:', tree.toStringTree(recog=parser))
except Exception as e:
    print(f'Parse failed: {e}')

if error_listener.errors:
    print('Errors:', error_listener.errors)