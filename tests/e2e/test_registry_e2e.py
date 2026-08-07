# -*- coding: utf-8 -*-
"""
段言包注册中心端到端测试

测试注册中心服务器的完整发布→搜索→安装全链路流程。
"""

import os
import sys
import json
import time
import threading
import tempfile
import shutil
import unittest
from pathlib import Path
from http.server import HTTPServer
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import quote, urlencode

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_src_dir = os.path.join(_project_root, 'src')
for _p in [_src_dir, _project_root]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from registry_server import RegistryStore, RegistryHandler


# ===========================================================================
# RegistryStore 单元测试
# ===========================================================================

class TestRegistryStore(unittest.TestCase):
    """RegistryStore 核心功能测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='duan_reg_test_')
        self.store = RegistryStore(data_dir=self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_empty_store(self):
        """空注册中心"""
        self.assertEqual(self.store.list_packages(), [])
        self.assertIsNone(self.store.get_package('nonexistent'))
        self.assertEqual(self.store.search('test'), [])

    def test_publish_and_get(self):
        """发布并获取包"""
        pkg = {
            'name': '测试包',
            'version': '1.0.0',
            'description': '一个测试包',
            'keywords': ['测试', 'demo'],
            'authors': ['测试作者'],
        }
        self.assertTrue(self.store.publish(pkg))
        info = self.store.get_package('测试包')
        self.assertIsNotNone(info)
        self.assertEqual(info['version'], '1.0.0')
        self.assertEqual(info['description'], '一个测试包')
        self.assertEqual(info['download_count'], 0)

    def test_publish_missing_fields(self):
        """缺少必填字段时发布失败"""
        self.assertFalse(self.store.publish({}))
        self.assertFalse(self.store.publish({'name': 'test'}))
        self.assertFalse(self.store.publish({'version': '1.0.0'}))

    def test_publish_invalid_version(self):
        """无效版本号时发布失败"""
        self.assertFalse(self.store.publish({'name': 'test', 'version': 'abc'}))
        self.assertFalse(self.store.publish({'name': 'test', 'version': '1'}))
        self.assertTrue(self.store.publish({'name': 'test', 'version': '1.0.0'}))

    def test_publish_version_history(self):
        """版本历史记录"""
        self.assertTrue(self.store.publish({'name': 'pkg', 'version': '1.0.0'}))
        time.sleep(0.01)  # 确保时间戳不同
        self.assertTrue(self.store.publish({'name': 'pkg', 'version': '2.0.0'}))
        versions = self.store.list_package_versions('pkg')
        self.assertEqual(len(versions), 1)  # 1个历史版本
        self.assertEqual(versions[0]['version'], '1.0.0')

    def test_search_by_name(self):
        """按名称搜索"""
        self.store.publish({'name': '网络请求', 'version': '1.0.0', 'keywords': [], 'description': ''})
        self.store.publish({'name': '网络工具', 'version': '1.0.0', 'keywords': [], 'description': ''})
        results = self.store.search('网络')
        self.assertEqual(len(results), 2)

    def test_search_by_keyword(self):
        """按关键词搜索"""
        self.store.publish({'name': '测试包', 'version': '1.0.0', 'keywords': ['测试', 'demo'], 'description': ''})
        results = self.store.search('demo')
        self.assertEqual(len(results), 1)

    def test_search_ranking(self):
        """搜索排序：精确匹配优先"""
        self.store.publish({'name': '数学', 'version': '1.0.0', 'keywords': [], 'description': ''})
        self.store.publish({'name': '数学扩展', 'version': '1.0.0', 'keywords': [], 'description': ''})
        results = self.store.search('数学')
        self.assertEqual(len(results), 2)
        # 精确匹配应该排在前面
        self.assertEqual(results[0]['name'], '数学')

    def test_delete_package(self):
        """删除包"""
        self.store.publish({'name': 'todelete', 'version': '1.0.0'})
        self.assertIsNotNone(self.store.get_package('todelete'))
        self.assertTrue(self.store.delete_package('todelete'))
        self.assertIsNone(self.store.get_package('todelete'))
        self.assertFalse(self.store.delete_package('todelete'))

    def test_download_count(self):
        """下载计数"""
        self.store.publish({'name': 'downloaded', 'version': '1.0.0'})
        for _ in range(5):
            self.store.record_download('downloaded')
        info = self.store.get_package('downloaded')
        self.assertEqual(info['download_count'], 5)

    def test_get_stats(self):
        """注册中心统计"""
        self.store.publish({'name': 'a', 'version': '1.0.0'})
        self.store.publish({'name': 'b', 'version': '2.0.0'})
        self.store.record_download('a')
        stats = self.store.get_stats()
        self.assertEqual(stats['total_packages'], 2)
        self.assertEqual(stats['total_downloads'], 1)


# ===========================================================================
# 端到端集成测试（HTTP 级别）
# ===========================================================================

class TestRegistryServerE2E(unittest.TestCase):
    """注册中心 HTTP 服务器端到端测试"""

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix='duan_reg_e2e_')
        cls._reset_store()
        cls.server = HTTPServer(('127.0.0.1', 0), RegistryHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f'http://127.0.0.1:{cls.port}'
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)  # 等待服务器启动

    @classmethod
    def _reset_store(cls):
        """重置存储状态（清空数据文件后创建新存储）"""
        pkg_path = Path(cls.tmpdir) / 'packages.json'
        if pkg_path.exists():
            pkg_path.unlink()
        cls.store = RegistryStore(data_dir=cls.tmpdir)
        RegistryHandler.store = cls.store

    def setUp(self):
        """每个测试前重置存储状态，确保测试隔离"""
        self._reset_store()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def _build_url(self, path: str) -> str:
        """构建 URL，只编码路径部分，保留查询字符串"""
        if '?' in path:
            base_path, query = path.split('?', 1)
            encoded_path = quote(base_path, safe='/')
            # 编码查询字符串中的中文等非 ASCII 字符
            from urllib.parse import urlencode, parse_qs
            query_params = parse_qs(query)
            encoded_query = urlencode(query_params, doseq=True)
            return f'{self.base_url}{encoded_path}?{encoded_query}'
        else:
            return f'{self.base_url}{quote(path, safe="/")}'

    def _get_json(self, path):
        """GET 请求，自动处理 URL 编码"""
        url = self._build_url(path)
        with urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def _post_json(self, path, data):
        """POST 请求，自动处理 URL 编码"""
        url = self._build_url(path)
        body = json.dumps(data).encode('utf-8')
        req = Request(url, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def _delete_request(self, path):
        """DELETE 请求，自动处理 URL 编码"""
        url = self._build_url(path)
        req = Request(url, method='DELETE')
        try:
            with urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except URLError as e:
            return json.loads(e.read().decode('utf-8'))

    def test_health_check(self):
        """健康检查"""
        data = self._get_json('/health')
        self.assertEqual(data['status'], 'ok')

    def test_empty_list(self):
        """空列表"""
        data = self._get_json('/api/v1/packages')
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['packages'], [])

    def test_full_publish_and_list_flow(self):
        """完整发布-列表流程"""
        # 发布
        result = self._post_json('/api/v1/packages', {
            'name': 'e2e测试包',
            'version': '1.0.0',
            'description': '端到端测试',
            'keywords': ['e2e', 'test'],
        })
        self.assertTrue(result['success'])

        # 列表
        data = self._get_json('/api/v1/packages')
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['packages'][0]['name'], 'e2e测试包')

        # 获取详情
        detail = self._get_json('/api/v1/packages/e2e测试包')
        self.assertEqual(detail['version'], '1.0.0')

    def test_search_flow(self):
        """搜索流程"""
        self._post_json('/api/v1/packages', {
            'name': '搜索测试包',
            'version': '1.0.0',
            'description': '用于搜索测试的包',
            'keywords': ['搜索', 'search'],
        })
        data = self._get_json('/api/v1/search?q=搜索')
        self.assertGreaterEqual(data['count'], 1)
        self.assertTrue(any(p['name'] == '搜索测试包' for p in data['results']))

    def test_version_management(self):
        """版本管理流程"""
        # 发布 v1
        self._post_json('/api/v1/packages', {
            'name': '版本测试',
            'version': '1.0.0',
        })
        # 发布 v2
        self._post_json('/api/v1/packages', {
            'name': '版本测试',
            'version': '2.0.0',
        })
        # 获取版本历史
        data = self._get_json('/api/v1/packages/版本测试/versions')
        self.assertGreaterEqual(data['count'], 1)

    def test_download_counting(self):
        """下载计数"""
        self._post_json('/api/v1/packages', {
            'name': '下载测试',
            'version': '1.0.0',
        })
        # 多次下载
        for _ in range(3):
            self._get_json('/api/v1/packages/下载测试/1.0.0')
        detail = self._get_json('/api/v1/packages/下载测试')
        self.assertEqual(detail['download_count'], 3)

    def test_stats(self):
        """统计信息"""
        stats = self._get_json('/api/v1/stats')
        self.assertIn('total_packages', stats)
        self.assertIn('total_downloads', stats)
        self.assertIn('total_versions', stats)

    def test_delete_flow(self):
        """删除流程"""
        self._post_json('/api/v1/packages', {
            'name': '待删除包',
            'version': '1.0.0',
        })
        data = self._delete_request('/api/v1/packages/待删除包')
        self.assertTrue(data['success'])
        # 确认已删除
        data = self._get_json('/api/v1/packages')
        names = [p['name'] for p in data['packages']]
        self.assertNotIn('待删除包', names)


if __name__ == '__main__':
    unittest.main(verbosity=2)