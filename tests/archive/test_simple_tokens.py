import sys, traceback
sys.path.insert(0, 'src')
sys.path.insert(0, '.')
from lexer import Lexer

tests = [
    '方法',          # Just 方法
    '方法(x)',       # 方法 with parens  
    '方法:',         # 方法 with colon
    '方法(x):',      # 方法 with parens and colon
    '方法:\n    结果', # 方法 with body
    '）方法',        # ) followed by 方法
    '》方法',        # 》 followed by 方法
]

l = Lexer()

for test in tests:
    print(f"\n--- {repr(test)} ---")
    sys.stdout.flush()
    try:
        tokens = l.tokenize(test)
        for t in tokens:
            print(f"  {t}")
        sys.stdout.flush()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        sys.stdout.flush()