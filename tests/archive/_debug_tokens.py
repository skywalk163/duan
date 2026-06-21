import sys
sys.path.insert(0, 'src')
sys.path.insert(0, 'G:\\dumategithub\\duan\\src')
from duan_parser_v3 import DuanParser
from tokens import Token, TokenType
from lexer import Lexer

lexer = Lexer()
parser = DuanParser()

with open('examples/student_management.duan', 'r', encoding='utf-8') as f:
    content = f.read()

# Try parsing and catch the error
try:
    tokens = lexer.tokenize(content)
    ast = parser.parse(tokens)
    print("Parse successful!")
except Exception as e:
    print(f"Error: {e}")
    
    # Try to parse line by line to find the problem
    print("\n--- Line by line analysis ---")
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip() and not line.strip().startswith('#'):
            try:
                ltokens = lexer.tokenize(line + '\n')
                # Just check if lexing works
            except Exception as le:
                print(f"Line {i} LEX ERROR: {le}")
                continue
            
            # Try to see what happens when we parse expressions in this line
            # Check for method calls with ()
            if '(' in line and '方法' not in line:
                print(f"Line {i}: {line.strip()}")
                # Show tokens for this line
                for t in ltokens:
                    if t.type.name in ('IDENTIFIER', 'KEYWORD', 'LPAREN', 'RPAREN', 'NUMBER', 'CHINESE_NUM', 'STRING', 'PLUS', 'DOT'):
                        print(f"  {t.type.name:15s} {repr(t.value)}")