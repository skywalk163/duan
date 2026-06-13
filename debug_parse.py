#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')
sys.path.insert(0, 'antlrparser')

from antlrparser.duan_tokenizer import create_antlr_token_stream, DuanLangTokenizer
from antlrparser.DuanLangLexer import DuanLangLexer
from antlrparser.DuanLangParser import DuanLangParser

# 测试分词器
code = '设 甲 为 3。'
print('Testing code:', repr(code))

# 1. 直接使用分词器
tokenizer = DuanLangTokenizer()
tokens = tokenizer.tokenize(code)
print('Tokens:')
for t in tokens:
    print(f'  {t}')

# 2. 使用 create_antlr_token_stream
print('\nCreating ANTLR token stream...')
try:
    token_stream = create_antlr_token_stream(code, DuanLangLexer)
    print('Token stream created successfully')
    
    # 打印所有 tokens
    token_stream.fill()
    print('Tokens in stream:')
    for t in token_stream.tokens:
        if t.type != -1:  # 跳过 EOF
            print(f'  {t}')
except Exception as e:
    print(f'Error creating token stream: {e}')
    import traceback
    traceback.print_exc()