# -*- coding: utf-8 -*-
"""
段言词法分析器单元测试

测试 src/lexer.py 的词法分析功能
"""

import sys
import os
import unittest

# 添加项目路径
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
sys.path.insert(0, _src_dir)


class TestLexer(unittest.TestCase):
    """词法分析器测试"""

    @classmethod
    def setUpClass(cls):
        try:
            from lexer import Lexer
            from tokens import TokenType
            cls.Lexer = Lexer
            cls.TokenType = TokenType
        except ImportError as e:
            raise unittest.SkipTest(f"Lexer 模块不可用: {e}")

    def test_simple_tokenize(self):
        """测试简单语句词法分析"""
        lexer = self.Lexer('定义甲等于三。')
        tokens = lexer.tokenize()
        self.assertGreater(len(tokens), 0)
        # 验证生成了预期的 token 类型
        token_types = [t.type for t in tokens]
        self.assertIn(self.TokenType.KEYWORD, token_types)
        self.assertIn(self.TokenType.IDENTIFIER, token_types)
        self.assertIn(self.TokenType.CHINESE_NUM, token_types)
        # 验证关键字值
        token_values = [t.value for t in tokens if t.type == self.TokenType.KEYWORD]
        self.assertIn('定义', token_values)
        self.assertIn('等于', token_values)

    def test_number_literal(self):
        """测试数字字面量"""
        lexer = self.Lexer('打印 123')
        tokens = lexer.tokenize()
        number_tokens = [t for t in tokens if t.type == self.TokenType.NUMBER]
        self.assertGreater(len(number_tokens), 0)
        self.assertEqual(number_tokens[0].value, 123)

    def test_string_literal(self):
        """测试字符串字面量"""
        lexer = self.Lexer('打印"你好"。')
        tokens = lexer.tokenize()
        string_tokens = [t for t in tokens if t.type == self.TokenType.STRING]
        self.assertGreater(len(string_tokens), 0)
        self.assertIn('你好', [t.value for t in string_tokens])

    def test_chinese_number(self):
        """测试中文数字"""
        lexer = self.Lexer('三加五')
        tokens = lexer.tokenize()
        cn_num_tokens = [t for t in tokens if t.type == self.TokenType.CHINESE_NUM]
        self.assertEqual(len(cn_num_tokens), 2)

    def test_list_literal(self):
        """测试列表字面量"""
        lexer = self.Lexer('定义列表等于[1, 2, 3]。')
        tokens = lexer.tokenize()
        token_types = [t.type for t in tokens]
        self.assertIn(self.TokenType.LBRACKET, token_types)
        self.assertIn(self.TokenType.RBRACKET, token_types)

    def test_keywords(self):
        """测试关键字识别"""
        test_cases = [
            ('如果', '如果'),
            ('那么', '那么'),
            ('否则', '否则'),
            ('遍历', '遍历'),
            ('返回', '返回'),
            ('打印', '打印'),
        ]
        for keyword, expected in test_cases:
            with self.subTest(keyword=keyword):
                lexer = self.Lexer(keyword + ' x')
                tokens = lexer.tokenize()
                keyword_tokens = [t for t in tokens if t.type == self.TokenType.KEYWORD and t.value == expected]
                self.assertGreater(len(keyword_tokens), 0,
                                 f"关键字 {keyword} 未被正确识别")

    def test_eof_token(self):
        """测试 EOF token"""
        lexer = self.Lexer('x')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[-1].type, self.TokenType.EOF)

    def test_empty_source(self):
        """测试空源文件"""
        lexer = self.Lexer('')
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, self.TokenType.EOF)


if __name__ == '__main__':
    unittest.main()
