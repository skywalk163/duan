"""
第四阶段标准库测试
测试：加密、编码解码
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'stdlib'))


class Test加密(unittest.TestCase):
    """测试加密模块"""
    
    def test_MD5(self):
        """测试MD5哈希"""
        from 加密 import MD5, MD5二进制
        
        result = MD5('hello')
        self.assertEqual(len(result), 32)
        self.assertEqual(result, '5d41402abc4b2a76b9719d911017c592')
        
        result_bin = MD5二进制(b'hello')
        self.assertEqual(len(result_bin), 16)
    
    def test_SHA1(self):
        """测试SHA1哈希"""
        from 加密 import SHA1, SHA1二进制
        
        result = SHA1('hello')
        self.assertEqual(len(result), 40)
        
        result_bin = SHA1二进制(b'hello')
        self.assertEqual(len(result_bin), 20)
    
    def test_SHA256(self):
        """测试SHA256哈希"""
        from 加密 import SHA256, SHA256二进制
        
        result = SHA256('hello')
        self.assertEqual(len(result), 64)
        
        result_bin = SHA256二进制(b'hello')
        self.assertEqual(len(result_bin), 32)
    
    def test_SHA512(self):
        """测试SHA512哈希"""
        from 加密 import SHA512, SHA512二进制
        
        result = SHA512('hello')
        self.assertEqual(len(result), 128)
        
        result_bin = SHA512二进制(b'hello')
        self.assertEqual(len(result_bin), 64)
    
    def test_SHA224(self):
        """测试SHA224哈希"""
        from 加密 import SHA224, SHA224二进制
        
        result = SHA224('hello')
        self.assertEqual(len(result), 56)
        
        result_bin = SHA224二进制(b'hello')
        self.assertEqual(len(result_bin), 28)
    
    def test_SHA384(self):
        """测试SHA384哈希"""
        from 加密 import SHA384, SHA384二进制
        
        result = SHA384('hello')
        self.assertEqual(len(result), 96)
        
        result_bin = SHA384二进制(b'hello')
        self.assertEqual(len(result_bin), 48)
    
    def test_HMAC(self):
        """测试HMAC"""
        from 加密 import HMAC_MD5, HMAC_SHA1, HMAC_SHA256, HMAC_SHA512, HMAC
        
        key = 'secret'
        data = 'hello'
        
        md5_result = HMAC_MD5(data, key)
        self.assertEqual(len(md5_result), 32)
        
        sha1_result = HMAC_SHA1(data, key)
        self.assertEqual(len(sha1_result), 40)
        
        sha256_result = HMAC_SHA256(data, key)
        self.assertEqual(len(sha256_result), 64)
        
        sha512_result = HMAC_SHA512(data, key)
        self.assertEqual(len(sha512_result), 128)
        
        generic_result = HMAC(data, key, 'sha256')
        self.assertEqual(generic_result, sha256_result)
    
    def test_计算文件哈希(self):
        """测试计算文件哈希"""
        from 加密 import 计算文件哈希
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('hello world')
            temp_file = f.name
        
        try:
            result = 计算文件哈希(temp_file)
            self.assertEqual(len(result), 64)
        finally:
            os.remove(temp_file)
    
    def test_生成随机密钥(self):
        """测试生成随机密钥"""
        from 加密 import 生成随机密钥, 生成随机IV
        
        key16 = 生成随机密钥(16)
        self.assertEqual(len(key16), 16)
        
        key24 = 生成随机密钥(24)
        self.assertEqual(len(key24), 24)
        
        key32 = 生成随机密钥(32)
        self.assertEqual(len(key32), 32)
        
        iv = 生成随机IV()
        self.assertEqual(len(iv), 16)
    
    def test_密码派生密钥(self):
        """测试密码派生密钥"""
        from 加密 import 密码派生密钥
        
        password = 'mypassword'
        key, salt = 密码派生密钥(password)
        self.assertEqual(len(key), 32)
        self.assertEqual(len(salt), 16)
        
        key2, salt2 = 密码派生密钥(password, salt=salt)
        self.assertEqual(key, key2)
    
    def test_AES(self):
        """测试AES加密（如果有加密库）"""
        from 加密 import AES, 生成随机密钥, 生成随机IV
        
        try:
            key = 生成随机密钥(16)
            aes = AES(key)
            
            plaintext = b'hello world 1234567890'
            ciphertext, iv = aes.加密(plaintext)
            
            self.assertNotEqual(ciphertext, plaintext)
            self.assertEqual(len(iv), 16)
            
            decrypted = aes.解密(ciphertext, iv)
            self.assertEqual(decrypted, plaintext)
        except RuntimeError as e:
            self.skipTest(f"AES测试跳过：{e}")
    
    def test_RSA(self):
        """测试RSA加密（如果有加密库）"""
        from 加密 import RSA
        
        try:
            rsa = RSA()
            private_key, public_key = rsa.生成密钥对(1024)
            
            self.assertIsInstance(private_key, bytes)
            self.assertIsInstance(public_key, bytes)
            self.assertIn(b'PRIVATE KEY', private_key)
            self.assertIn(b'PUBLIC KEY', public_key)
            
            plaintext = b'hello'
            ciphertext = rsa.加密(plaintext)
            self.assertNotEqual(ciphertext, plaintext)
            
            decrypted = rsa.解密(ciphertext)
            self.assertEqual(decrypted, plaintext)
            
            data = b'test data'
            signature = rsa.签名(data)
            self.assertTrue(rsa.验证签名(data, signature))
            self.assertFalse(rsa.验证签名(b'wrong data', signature))
        except RuntimeError as e:
            self.skipTest(f"RSA测试跳过：{e}")


class Test编码解码(unittest.TestCase):
    """测试编码解码模块"""
    
    def test_Base64(self):
        """测试Base64编码解码"""
        from 编码解码 import Base64编码, Base64解码, Base64编码二进制, Base64解码二进制
        
        data = 'hello world'
        encoded = Base64编码(data)
        decoded = Base64解码(encoded)
        self.assertEqual(decoded, data)
        
        bin_encoded = Base64编码二进制(b'hello')
        bin_decoded = Base64解码二进制(bin_encoded)
        self.assertEqual(bin_decoded, b'hello')
    
    def test_Base64URL(self):
        """测试Base64URL编码解码"""
        from 编码解码 import Base64URL编码, Base64URL解码
        
        data = 'hello world!'
        encoded = Base64URL编码(data)
        decoded = Base64URL解码(encoded)
        self.assertEqual(decoded, data)
    
    def test_Base32(self):
        """测试Base32编码解码"""
        from 编码解码 import Base32编码, Base32解码
        
        data = 'hello'
        encoded = Base32编码(data)
        decoded = Base32解码(encoded)
        self.assertEqual(decoded, data)
    
    def test_Base16(self):
        """测试Base16编码解码"""
        from 编码解码 import Base16编码, Base16解码
        
        data = 'hello'
        encoded = Base16编码(data)
        decoded = Base16解码(encoded)
        self.assertEqual(decoded, data)
    
    def test_十六进制(self):
        """测试十六进制编码解码"""
        from 编码解码 import 十六进制编码, 十六进制解码, 十六进制编码大写
        
        data = 'hello'
        encoded = 十六进制编码(data)
        decoded = 十六进制解码(encoded)
        self.assertEqual(decoded, data)
        
        encoded_upper = 十六进制编码大写(data)
        self.assertTrue(encoded_upper.isupper())
        self.assertEqual(十六进制解码(encoded_upper), data)
    
    def test_二进制十六进制转换(self):
        """测试二进制与十六进制转换"""
        from 编码解码 import 二进制转十六进制, 十六进制转二进制
        
        data = b'hello'
        hex_str = 二进制转十六进制(data)
        back_data = 十六进制转二进制(hex_str)
        self.assertEqual(back_data, data)
    
    def test_URL编码解码(self):
        """测试URL编码解码"""
        from 编码解码 import URL编码, URL解码, URL编码全字符
        
        data = '你好 world!'
        encoded = URL编码(data)
        decoded = URL解码(encoded)
        self.assertEqual(decoded, data)
        
        encoded_full = URL编码全字符(data)
        decoded_full = URL解码(encoded_full)
        self.assertEqual(decoded_full, data)
    
    def test_URL查询串(self):
        """测试URL查询串编码解码"""
        from 编码解码 import URL查询串编码, URL查询串解码
        
        params = {'a': '1', 'b': '2', 'c': '你好'}
        encoded = URL查询串编码(params)
        decoded = URL查询串解码(encoded)
        self.assertEqual(decoded['a'], '1')
        self.assertEqual(decoded['b'], '2')
        self.assertEqual(decoded['c'], '你好')
    
    def test_字符集转换(self):
        """测试字符集转换"""
        from 编码解码 import 字符集转换, 字符集转换为字符串, 检测编码
        
        utf8_data = '你好'.encode('utf-8')
        gbk_data = utf8_data.decode('utf-8').encode('gbk')
        
        converted = 字符集转换(gbk_data, 'gbk', 'utf-8')
        self.assertEqual(converted.decode('utf-8'), '你好')
        
        converted_str = 字符集转换为字符串(gbk_data, 'gbk', 'utf-8')
        self.assertEqual(converted_str, '你好')
        
        detected = 检测编码(utf8_data)
        self.assertEqual(detected, 'utf-8')
    
    def test_HTML实体(self):
        """测试HTML实体编码解码"""
        from 编码解码 import HTML实体编码, HTML实体解码
        
        data = '<script>alert("test")</script>'
        encoded = HTML实体编码(data)
        self.assertNotIn('<', encoded)
        self.assertNotIn('>', encoded)
        
        decoded = HTML实体解码(encoded)
        self.assertEqual(decoded, data)
    
    def test_Unicode转换(self):
        """测试Unicode转换"""
        from 编码解码 import Unicode转中文, 中文转Unicode
        
        chinese = '你好'
        unicode_escaped = 中文转Unicode(chinese)
        self.assertIn('\\u', unicode_escaped)
        
        back = Unicode转中文(unicode_escaped)
        self.assertEqual(back, chinese)
    
    def test_字节字符串转换(self):
        """测试字节与字符串转换"""
        from 编码解码 import 字节转字符串, 字符串转字节
        
        data = 'hello'
        b = 字符串转字节(data)
        self.assertIsInstance(b, bytes)
        
        s = 字节转字符串(b)
        self.assertEqual(s, data)
    
    def test_文本十六进制转换(self):
        """测试文本与十六进制转换"""
        from 编码解码 import 文本转十六进制, 十六进制转文本
        
        data = 'hello'
        hex_str = 文本转十六进制(data)
        back = 十六进制转文本(hex_str)
        self.assertEqual(back, data)


if __name__ == '__main__':
    unittest.main()
