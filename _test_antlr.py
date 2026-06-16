"""测试 ANTLR 解析器多行支持 — 分析具体错误"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'antlrparser'))

from DuanLangLexer import DuanLangLexer
from DuanLangParser import DuanLangParser
from DuanLangParserVisitor import DuanLangParserVisitor
from duan_tokenizer import create_antlr_token_stream
from duan_visitor import DuanLangErrorListener

# 多个测试用例
tests = [
    ("简单打印", '打印("你好，世界！")。'),
    ("K_SET 赋值", '设甲为10。'),
    ("K_DEFINE 赋值", '定义甲等于10。'),
    ("多行1: 变量定义", '定义甲等于10。\n定义乙等于20。'),
    ("多行2: if+打印", '定义甲等于10。\n如果甲大于5：\n打印("甲大")。\n结束。'),
    ("多行3: if+else", '定义甲等于10。\n如果甲大于5：\n打印("大")。\n否则：\n打印("小")。\n结束。'),
    ("多行4: 遍历", '遍历甲之[1,2,3]：\n打印(甲)。\n结束。'),
    ("多行5: 段落定义", '段 加一 接收 甲：\n返回甲加一。\n结束。'),
]

for desc, code in tests:
    print(f"\n{'='*60}")
    print(f"测试: {desc}")
    print(f"代码: {repr(code)}")
    
    lexer = DuanLangLexer()
    token_stream = create_antlr_token_stream(code, lexer)
    
    # Parse
    token_stream.seek(0)
    parser = DuanLangParser(token_stream)
    
    error_listener = DuanLangErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    tree = parser.program()
    
    if error_listener.has_errors():
        for e in error_listener.get_errors():
            print(f"  错误: {e}")
    else:
        print(f"  ✅ 语法通过!")
        # Show token flow for debugging
        token_stream.seek(0)
        token_stream.fill()
        for tok in token_stream.tokens:
            if tok.type != -1:
                name = lexer.symbolicNames[tok.type] if tok.type < len(lexer.symbolicNames) else 'UNKNOWN'
                print(f"    Token: {name} = '{tok.text}'")