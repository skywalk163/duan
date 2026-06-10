"""
段言（Duan）Web Playground - 后端 API 服务

提供代码执行、示例库、代码分享功能。
"""

import os
import sys
import json
import uuid
import hashlib
import time
import io

# 添加上级目录到路径（引入解释器）
_script_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_script_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from duan_interpreter import run_source
from duan_visitor import parse_source
from duan_tokenizer import DuanLangTokenizer

app = Flask(__name__, static_folder='static')
CORS(app)

# =============================================================================
# 配置
# =============================================================================

SHARED_DIR = os.path.join(_script_dir, 'shared')
EXAMPLES_FILE = os.path.join(_script_dir, 'examples.json')
os.makedirs(SHARED_DIR, exist_ok=True)


# =============================================================================
# 内置示例
# =============================================================================

BUILTIN_EXAMPLES = [
    {
        "id": "hello",
        "title": "你好，段言",
        "description": "最基础的段言程序",
        "code": '打印("你好，段言！")。\n打印("欢迎来到中文编程的世界。")。'
    },
    {
        "id": "variables",
        "title": "变量与运算",
        "description": "变量定义和基本算术运算",
        "code": '定义甲等于10。\n定义乙等于20。\n定义丙等于真。\n定义丁等于空。\n\n打印(甲加乙)。\n打印(甲乘乙)。\n\n定义_最大值等于甲。\n如果乙大于甲那么:\n  定义_最大值等于乙。\n结束。\n打印(_最大值)。'
    },
    {
        "id": "types",
        "title": "数据类型",
        "description": "数字、字符串、列表、字典的使用",
        "code": '# 数字运算\n定义结果等于10加5乘2。\n打印("10 + 5 × 2 = "加结果)。\n\n# 字符串\n定义_问候等于"你好，世界！"。\n打印(_问候)。\n\n# 列表\n定义_数字列等于【1, 2, 3, 4, 5】。\n打印(_数字列)。\n打印("长度："加_数字列之长度)。\n打印("第一个元素："加_数字列[0])。\n\n# 嵌套列表\n定义_矩阵等于【【1, 2】, 【3, 4】】。\n打印(_矩阵[0][1])。'
    },
    {
        "id": "controlflow",
        "title": "控制流",
        "description": "条件判断和循环语句",
        "code": '# 条件判断\n定义分数等于85。\n\n如果分数大于等于90那么:\n  打印(\'优秀\')。\n否则若分数大于等于80那么:\n  打印(\'良好\')。\n否则若分数大于等于60那么:\n  打印(\'及格\')。\n否则:\n  打印(\'不及格\')。\n结束。\n\n# 遍历循环\n定义列表等于【10, 20, 30】。\n遍历 项 列表:\n  打印(项)。\n结束。\n\n# 当循环\n定义计数等于3。\n当计数大于0:\n  打印(计数)。\n  定义计数等于计数减1。\n结束。'
    },
    {
        "id": "function",
        "title": "段落（函数）",
        "description": "段落定义和调用",
        "code": '# 定义段落\n《平方》段(数值):\n  返回数值乘数值。\n结束。\n\n《双倍》段(数值):\n  返回数值乘2。\n结束。\n\n《阶乘》段(数值):\n  如果数值小于等于1那么:\n    返回1。\n  结束。\n  定义结果等于1。\n  定义i等于数值。\n  当i大于1:\n    结果等于结果乘i。\n    i等于i减1。\n  结束。\n  返回结果。\n结束。\n\n# 调用段落\n打印("5 的平方："加《平方》(5))。\n打印("双倍 21："加《双倍》(21))。\n打印("6 的阶乘："加《阶乘》(6))。'
    },
    {
        "id": "fibonacci",
        "title": "斐波那契数列",
        "description": "递归计算斐波那契数列",
        "code": '# 递归斐波那契\n《斐波那契》段(n):\n  如果n小于等于1那么:\n    返回n。\n  结束。\n  返回《斐波那契》(n减1)加《斐波那契》(n减2)。\n结束。\n\n# 输出前 10 项\n定义i等于0。\n当i小于10:\n  打印("F("加i加") = "加《斐波那契》(i))。\n  i等于i加1。\n结束。'
    },
    {
        "id": "quicksort",
        "title": "快速排序",
        "description": "经典的快速排序算法",
        "code": '# 找最大值\n《找最大值》段(列表):\n  定义_最大值等于列表[0]。\n  遍历 项 列表:\n    如果项大于_最大值那么:\n      定义_最大值等于项。\n    结束。\n  结束。\n  返回_最大值。\n结束。\n\n定义数据等于【5, 3, 8, 1, 9, 2】。\n定义_最大等于《找最大值》(数据)。\n打印("列表："加数据)。\n打印("最大值："加_最大)。\n\n# 用同样的方式找最小值\n《找最小值》段(列表):\n  定义_最小值等于列表[0]。\n  遍历 项 列表:\n    如果项小于_最小值那么:\n      定义_最小值等于项。\n    结束。\n  结束。\n  返回_最小值。\n结束。\n\n定义_最小等于《找最小值》(数据)。\n打印("最小值："加_最小)。'
    },
    {
        "id": "grades",
        "title": "成绩统计",
        "description": "学生成绩统计和等级评定",
        "code": '# 计算平均分\n《计算平均分》段(成绩列表):\n  定义总分等于0。\n  遍历 项 成绩列表:\n    总分等于总分加项。\n  结束。\n  返回总分除成绩列表之长度。\n结束。\n\n# 等级评定\n《统计等级》段(分数):\n  如果分数大于等于90那么:\n    返回\'优秀\'。\n  否则若分数大于等于80那么:\n    返回\'良好\'。\n  否则若分数大于等于60那么:\n    返回\'及格\'。\n  否则:\n    返回\'不及格\'。\n  结束。\n结束。\n\n定义成绩等于【85, 92, 78, 63, 58, 95】。\n定义平均分等于《计算平均分》(成绩)。\n打印("平均分："加平均分)。\n\n遍历 项 成绩:\n  定义_等级等于《统计等级》(项)。\n  打印(项加"："加_等级)。\n结束。'
    },
    {
        "id": "module_demo",
        "title": "模块导入",
        "description": "演示模块导入和导出功能",
        "code": '# 段落定义 — 函数式编程示例\n\n《平方》段(数值):\n  返回数值乘数值。\n结束。\n\n《立方》段(数值):\n  返回数值乘数值乘数值。\n结束。\n\n打印("5 的平方："加《平方》(5))。\n打印("3 的立方："加《立方》(3))。\n\n# 管道式调用\n定义_双倍等于《平方》(3)加1。\n打印("3² + 1 = "加_双倍)。'
    }
]


# =============================================================================
# API 路由
# =============================================================================

@app.route('/')
def index():
    """提供主页面"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/execute', methods=['POST'])
def execute():
    """执行段言代码"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'success': False, 'error': '代码不能为空'})

    try:
        interp = run_source(code)
        output = interp.get_output()
        if not output:
            output = '(无输出)'

        return jsonify({
            'success': True,
            'output': output,
            'execution_time': 0
        })
    except SyntaxError as e:
        return jsonify({'success': False, 'error': f'语法错误: {e}'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'运行时错误: {type(e).__name__}: {e}'})


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """获取内置示例列表"""
    return jsonify({'examples': BUILTIN_EXAMPLES})


@app.route('/api/examples/<example_id>', methods=['GET'])
def get_example(example_id):
    """获取单个示例详情"""
    for ex in BUILTIN_EXAMPLES:
        if ex['id'] == example_id:
            return jsonify(ex)
    return jsonify({'error': '示例未找到'}), 404


@app.route('/api/share', methods=['POST'])
def share_code():
    """分享代码（返回唯一 ID）"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'success': False, 'error': '代码不能为空'})

    # 生成唯一 ID（基于内容和时间戳）
    content_hash = hashlib.md5(code.encode('utf-8')).hexdigest()[:8]
    timestamp = int(time.time())
    share_id = f"{content_hash}-{timestamp}"

    # 保存到文件
    share_file = os.path.join(SHARED_DIR, f"{share_id}.json")
    if not os.path.exists(share_file):
        with open(share_file, 'w', encoding='utf-8') as f:
            json.dump({
                'id': share_id,
                'code': code,
                'created_at': timestamp
            }, f, ensure_ascii=False, indent=2)

    return jsonify({
        'success': True,
        'share_id': share_id,
        'share_url': f"/?share={share_id}"
    })


@app.route('/api/share/<share_id>', methods=['GET'])
def get_shared_code(share_id):
    """获取已分享的代码"""
    share_file = os.path.join(SHARED_DIR, f"{share_id}.json")
    if not os.path.exists(share_file):
        return jsonify({'error': '分享内容未找到或已过期'}), 404

    with open(share_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/api/parse', methods=['POST'])
def parse_code():
    """解析代码并返回 AST 信息"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'success': False, 'error': '代码不能为空'})

    try:
        module = parse_source(code)
        if module is None:
            return jsonify({'success': False, 'error': '解析失败'})

        segments = []
        for seg in module.segments:
            segments.append({
                'name': seg.name,
                'parameters': [p.name for p in seg.parameters],
                'return_type': seg.return_type
            })

        return jsonify({
            'success': True,
            'segments': segments,
            'statement_count': len(module.statements),
            'import_count': len(module.imports),
            'export_count': len(module.exports)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'解析错误: {e}'})


@app.route('/api/tokenize', methods=['POST'])
def tokenize_code():
    """词法分析并返回 Token 列表"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'success': False, 'error': '代码不能为空'})

    try:
        tokenizer = DuanLangTokenizer()
        tokens = tokenizer.tokenize(code)

        token_list = []
        for t in tokens:
            if t.type_name == 'EOF':
                continue
            token_list.append({
                'type': t.type_name,
                'text': t.text,
                'line': t.line,
                'column': t.column
            })

        has_errors = len(tokenizer.errors) > 0
        return jsonify({
            'success': not has_errors,
            'tokens': token_list,
            'errors': [str(e) for e in tokenizer.errors],
            'token_count': len(token_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'词法分析错误: {e}'})


# =============================================================================
# 启动
# =============================================================================

if __name__ == '__main__':
    print(f"段言 Web Playground 启动中...")
    print(f"  静态文件目录: {app.static_folder}")
    print(f"  分享存储目录: {SHARED_DIR}")
    print(f"  访问地址: http://localhost:5000")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)