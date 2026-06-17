"""调试异步段解析"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from duan_visitor import DuanParser

p = DuanParser()

# 测试异步段 - 检查预处理和解析
src = "异步段落 异步任务 接收:\n  打印(\"异步执行中\")。\n结束。\n\n异步任务()。"
print("原始:", repr(src))

pre = p._preprocess_async(src)
print("预处理后:", repr(pre))

# 测试tokenization
from duan_tokenizer import create_antlr_token_stream
from DuanLangLexer import DuanLangLexer

stream = create_antlr_token_stream(pre, DuanLangLexer)
tokens = []
token = stream.nextToken()
while token.type != -1:
    tokens.append(f"{DuanLangLexer.symbolicNames[token.type]}({token.text})")
    token = stream.nextToken()
print("Token序列:", tokens)

# 尝试解析
m = p.parse(src)
if m:
    print("解析成功!")
    for seg in m.segments:
        print(f"  段落: {seg.name}, 修饰符: {seg.modifiers}")
else:
    print("解析失败:", p.errors)