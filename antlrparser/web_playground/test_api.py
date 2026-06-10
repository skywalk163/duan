"""测试 Web Playground API"""
import urllib.request
import json

BASE = 'http://localhost:5000'

def test_examples():
    resp = urllib.request.urlopen(f'{BASE}/api/examples')
    data = json.loads(resp.read())
    print(f'[GET /api/examples] 示例数: {len(data["examples"])}')
    for e in data['examples']:
        print(f'    {e["id"]}: {e["title"]}')
    assert len(data['examples']) > 0

def test_execute():
    body = json.dumps({'code': '打印("你好，段言！")。\n定义甲等于42。\n打印(甲加8)。'}).encode()
    req = urllib.request.Request(f'{BASE}/api/execute', data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f'[POST /api/execute] 成功: {result["success"]}')
    print(f'    输出: {result["output"]}')
    assert result['success']
    assert '50' in result['output']

def test_parse():
    body = json.dumps({'code': '《平方》段(n):\n  返回n乘n。\n结束。\n《双倍》段(n):\n  返回n乘2。\n结束。'}).encode()
    req = urllib.request.Request(f'{BASE}/api/parse', data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f'[POST /api/parse] 成功: {result["success"]}')
    print(f'    段落: {[s["name"] for s in result.get("segments", [])]}')
    assert result['success'], f'解析失败: {result.get("error", "unknown")}'
    assert len(result['segments']) == 2

def test_tokenize():
    body = json.dumps({'code': '定义甲等于10。'}).encode()
    req = urllib.request.Request(f'{BASE}/api/tokenize', data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f'[POST /api/tokenize] 成功: {result["success"]}')
    print(f'    Token数: {result["token_count"]}')
    for t in result['tokens'][:3]:
        print(f'      {t["type"]}: {t["text"]}')
    assert result['success']
    assert result['token_count'] >= 5

def test_share():
    # 分享
    body = json.dumps({'code': '打印("分享测试")。'}).encode()
    req = urllib.request.Request(f'{BASE}/api/share', data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    share_id = result['share_id']
    print(f'[POST /api/share] 成功: {result["success"]}')
    print(f'    分享ID: {share_id}')
    assert result['success']

    # 获取分享
    resp = urllib.request.urlopen(f'{BASE}/api/share/{share_id}')
    data = json.loads(resp.read())
    print(f'[GET /api/share/{share_id}] 代码: {data["code"][:20]}...')
    assert data['code'] == '打印("分享测试")。'

if __name__ == '__main__':
    print('=== 测试 Web Playground API ===\n')
    test_examples()
    test_execute()
    test_parse()
    test_tokenize()
    test_share()
    print('\n✅ 所有测试通过！')