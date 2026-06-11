# 测试文件解析
import sys
sys.path.insert(0, 'antlrparser')
from duan_visitor import parse_source

print("=== 简化测试 ===")
tests = [
    '''《解释》段(源码): 定义 a 等于 []. 定义 环境 等于 _典(). 定义 位置 等于 0. 定义 词数 等于 5. 当 位置 小于 词数: 定义 x 等于 a. 跳过. 结束. 返回 环境. 结束。''',
    '''《解释》段(源码): 定义 a 等于 []. 定义 环境 等于 _典(). 定义 位置 等于 0. 定义 词数 等于 5. 当 位置 小于 词数: 定义 当前项 等于 a. 跳过. 结束. 返回 环境. 结束。''',
    '''《解释》段(源码): 定义 a 等于 []. 定义 环境 等于 _典(). 定义 位置 等于 0. 定义 词数 等于 5. 当 位置 小于 词数: 定义 当前 等于 a. 跳过. 结束. 返回 环境. 结束。''',
]

for i, test in enumerate(tests):
    print(f"\n测试 {i+1}: {test[:70]}...")
    result = parse_source(test)
    if result:
        print("✓ 解析成功")
    else:
        print("✗ 解析失败")