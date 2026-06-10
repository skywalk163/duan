#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试解析器 - 添加详细日志"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from duan_parser_v3 import DuanParser

# 启用调试模式
import duan_parser_v3
duan_parser_v3.DEBUG = True

source = '字典设置 字典 "名称" "测试"。'
print('Source:', source)
print()

lexer = Lexer()
tokens = lexer.tokenize(source)
print('Tokens:')
for i, tok in enumerate(tokens):
    print(f'  {i}: {tok.type.name:15} {tok.value!r}')

print('\nParsing...')
parser = DuanParser()

# 手动调用收集参数
from keywords import VERB_ARITY

tok = tokens[0]
print(f'First token: {tok.type.name} {tok.value}')
print(f'Is verb: {tok.value in VERB_ARITY}')
print(f'Arity: {VERB_ARITY.get(tok.value)}')
