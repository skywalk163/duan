"""
第七阶段测试用例 - 文本处理与解析模块
"""
import unittest
import os
import json
import tempfile


class Test正则表达式(unittest.TestCase):
    
    def test_匹配(self):
        from stdlib.正则表达式 import 匹配
        self.assertTrue(匹配(r'\d+', 'abc123def'))
        self.assertFalse(匹配(r'\d+', 'abcdef'))
    
    def test_完全匹配(self):
        from stdlib.正则表达式 import 完全匹配
        self.assertTrue(完全匹配(r'^\d+$', '12345'))
        self.assertFalse(完全匹配(r'^\d+$', 'abc123'))
    
    def test_查找(self):
        from stdlib.正则表达式 import 查找
        self.assertEqual(查找(r'\d+', 'abc123def456'), '123')
    
    def test_查找所有(self):
        from stdlib.正则表达式 import 查找所有
        self.assertEqual(查找所有(r'\d+', 'abc123def456'), ['123', '456'])
    
    def test_替换(self):
        from stdlib.正则表达式 import 替换
        self.assertEqual(替换(r'\d+', 'abc123def', '***'), 'abc***def')
    
    def test_分割(self):
        from stdlib.正则表达式 import 分割
        self.assertEqual(分割(r'\s+', 'a b  c   d'), ['a', 'b', 'c', 'd'])
    
    def test_验证邮箱(self):
        from stdlib.正则表达式 import 验证邮箱
        self.assertTrue(验证邮箱('test@example.com'))
        self.assertFalse(验证邮箱('invalid-email'))
    
    def test_验证手机号(self):
        from stdlib.正则表达式 import 验证手机号
        self.assertTrue(验证手机号('13812345678'))
        self.assertFalse(验证手机号('12345678901'))
    
    def test_验证URL(self):
        from stdlib.正则表达式 import 验证URL
        self.assertTrue(验证URL('https://www.example.com'))
        self.assertFalse(验证URL('invalid-url'))
    
    def test_去除HTML标签(self):
        from stdlib.正则表达式 import 去除HTML标签
        self.assertEqual(去除HTML标签('<div>hello</div>'), 'hello')


class Test模板引擎(unittest.TestCase):
    
    def test_变量替换(self):
        from stdlib.模板引擎 import 简单模板
        模板 = 简单模板('Hello, {{name}}!')
        self.assertEqual(模板.渲染({'name': 'World'}), 'Hello, World!')
    
    def test_条件渲染(self):
        from stdlib.模板引擎 import 模板引擎
        模板 = 模板引擎()
        内容 = '{% if name %}Hello, {{name}}!{% endif %}'
        self.assertEqual(模板.渲染(内容, name='World'), 'Hello, World!')
        self.assertEqual(模板.渲染(内容), '')
    
    def test_循环渲染(self):
        from stdlib.模板引擎 import 模板引擎
        模板 = 模板引擎()
        内容 = '{% for item in items %}{{item}}{% endfor %}'
        self.assertEqual(模板.渲染(内容, items=['a', 'b', 'c']), 'abc')
    
    def test_HTML转义(self):
        from stdlib.模板引擎 import HTML转义
        self.assertEqual(HTML转义('<script>alert("xss")</script>'), '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;')


class TestJSON解析器(unittest.TestCase):
    
    def test_解析JSON(self):
        from stdlib.JSON解析器 import 解析JSON
        数据 = 解析JSON('{"name": "test", "value": 123}')
        self.assertEqual(数据['name'], 'test')
        self.assertEqual(数据['value'], 123)
    
    def test_生成JSON(self):
        from stdlib.JSON解析器 import 生成JSON
        数据 = {'name': 'test', 'value': 123}
        结果 = 生成JSON(数据)
        self.assertIn('"name": "test"', 结果)
    
    def test_JSON提取值(self):
        from stdlib.JSON解析器 import JSON提取值
        JSON字符串 = '{"a": {"b": {"c": 123}}}'
        self.assertEqual(JSON提取值(JSON字符串, 'a.b.c'), 123)
    
    def test_JSON转CSV(self):
        from stdlib.JSON解析器 import JSON转CSV
        JSON字符串 = '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
        CSV结果 = JSON转CSV(JSON字符串)
        self.assertIn('name,age', CSV结果)


class TestCSV读写器(unittest.TestCase):
    
    def setUp(self):
        self.临时文件 = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.临时文件.write('name,age,city\nAlice,25,Beijing\nBob,30,Shanghai\n')
        self.临时文件.close()
    
    def tearDown(self):
        os.unlink(self.临时文件.name)
    
    def test_读取CSV(self):
        from stdlib.CSV读写器 import 读取CSV
        数据 = 读取CSV(self.临时文件.name)
        self.assertEqual(len(数据), 2)
        self.assertEqual(数据[0]['name'], 'Alice')
    
    def test_字典转CSV(self):
        from stdlib.CSV读写器 import 字典转CSV
        数据 = [{'name': 'Alice', 'age': 25}]
        CSV结果 = 字典转CSV(数据)
        self.assertIn('name,age', CSV结果)
    
    def test_CSV转字典(self):
        from stdlib.CSV读写器 import CSV转字典
        CSV文本 = 'name,age\nAlice,25'
        结果 = CSV转字典(CSV文本)
        self.assertEqual(len(结果), 1)
        self.assertEqual(结果[0]['name'], 'Alice')
    
    def test_CSV转HTML表格(self):
        from stdlib.CSV读写器 import CSV转HTML表格
        HTML结果 = CSV转HTML表格(self.临时文件.name)
        self.assertIn('<table>', HTML结果)
    
    def test_CSV转Markdown表格(self):
        from stdlib.CSV读写器 import CSV转Markdown表格
        Markdown结果 = CSV转Markdown表格(self.临时文件.name)
        self.assertIn('|name|age|city|', Markdown结果)


class Test字符串工具(unittest.TestCase):
    
    def test_转大写(self):
        from stdlib.字符串工具 import 转大写
        self.assertEqual(转大写('hello'), 'HELLO')
    
    def test_转小写(self):
        from stdlib.字符串工具 import 转小写
        self.assertEqual(转小写('HELLO'), 'hello')
    
    def test_首字母大写(self):
        from stdlib.字符串工具 import 首字母大写
        self.assertEqual(首字母大写('hello'), 'Hello')
    
    def test_反转字符串(self):
        from stdlib.字符串工具 import 反转字符串
        self.assertEqual(反转字符串('hello'), 'olleh')
    
    def test_去除首尾空白(self):
        from stdlib.字符串工具 import 去除首尾空白
        self.assertEqual(去除首尾空白('  hello  '), 'hello')
    
    def test_子串查找(self):
        from stdlib.字符串工具 import 子串查找
        self.assertEqual(子串查找('hello world', 'world'), 6)
    
    def test_包含子串(self):
        from stdlib.字符串工具 import 包含子串
        self.assertTrue(包含子串('hello world', 'world'))
        self.assertFalse(包含子串('hello world', 'python'))
    
    def test_以子串开头(self):
        from stdlib.字符串工具 import 以子串开头
        self.assertTrue(以子串开头('hello world', 'hello'))
    
    def test_以子串结尾(self):
        from stdlib.字符串工具 import 以子串结尾
        self.assertTrue(以子串结尾('hello world', 'world'))
    
    def test_Base64编码解码(self):
        from stdlib.字符串工具 import Base64编码, Base64解码
        原始 = 'hello world'
        编码 = Base64编码(原始)
        解码 = Base64解码(编码)
        self.assertEqual(解码, 原始)
    
    def test_URL编码解码(self):
        from stdlib.字符串工具 import URL编码, URL解码
        原始 = 'hello world'
        编码 = URL编码(原始)
        解码 = URL解码(编码)
        self.assertEqual(解码, 原始)
    
    def test_HTML编码解码(self):
        from stdlib.字符串工具 import HTML编码, HTML解码
        原始 = '<script>alert("xss")</script>'
        编码 = HTML编码(原始)
        解码 = HTML解码(编码)
        self.assertEqual(解码, 原始)
    
    def test_MD5哈希(self):
        from stdlib.字符串工具 import MD5哈希
        哈希 = MD5哈希('hello')
        self.assertEqual(len(哈希), 32)
    
    def test_SHA256哈希(self):
        from stdlib.字符串工具 import SHA256哈希
        哈希 = SHA256哈希('hello')
        self.assertEqual(len(哈希), 64)
    
    def test_验证邮箱(self):
        from stdlib.字符串工具 import 验证邮箱
        self.assertTrue(验证邮箱('test@example.com'))
    
    def test_验证手机号(self):
        from stdlib.字符串工具 import 验证手机号
        self.assertTrue(验证手机号('13812345678'))
    
    def test_去除HTML标签(self):
        from stdlib.字符串工具 import 去除HTML标签
        self.assertEqual(去除HTML标签('<div>hello</div>'), 'hello')
    
    def test_文本清洗(self):
        from stdlib.字符串工具 import 文本清洗
        self.assertEqual(文本清洗('  hello   world!  '), 'hello world')
    
    def test_格式化金额(self):
        from stdlib.字符串工具 import 格式化金额
        self.assertEqual(格式化金额(12345.67), '12,345.67')
    
    def test_格式化百分比(self):
        from stdlib.字符串工具 import 格式化百分比
        self.assertEqual(格式化百分比(0.25), '25.00%')


if __name__ == '__main__':
    unittest.main()
