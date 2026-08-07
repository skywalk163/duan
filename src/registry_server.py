# -*- coding: utf-8 -*-
"""
段言（Duan）包注册中心服务器 — v2.0

提供 HTTP API 用于段件的搜索、发布和查询。

功能：
  - GET  /api/v1/packages              列出所有包
  - GET  /api/v1/packages/{name}       获取包详情
  - GET  /api/v1/packages/{name}/{version}  获取特定版本
  - GET  /api/v1/packages/{name}/versions   列出所有版本
  - POST /api/v1/packages              发布新包
  - DELETE /api/v1/packages/{name}     删除包
  - GET  /api/v1/search?q=关键词        搜索包
  - GET  /api/v1/stats                 注册中心统计信息

用法：
    python src/registry_server.py          # 启动服务器（默认端口 8000）
    python src/registry_server.py --port 8080  # 指定端口
"""

import os
import sys
import json
import re
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime


# ---------------------------------------------------------------------------
# 数据存储
# ---------------------------------------------------------------------------

class RegistryStore:
    """注册中心数据存储（基于文件系统 JSON）"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'registry_data')
        self.data_dir = Path(data_dir).resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._packages: Dict[str, Dict] = {}
        self._load()

    def _packages_path(self) -> Path:
        return self.data_dir / 'packages.json'

    def _load(self):
        """从磁盘加载包数据"""
        pkg_path = self._packages_path()
        if pkg_path.exists():
            try:
                with open(pkg_path, 'r', encoding='utf-8') as f:
                    self._packages = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._packages = {}
        else:
            self._packages = {}
            self._save()

    def _save(self):
        """保存包数据到磁盘"""
        with open(self._packages_path(), 'w', encoding='utf-8') as f:
            json.dump(self._packages, f, ensure_ascii=False, indent=2)

    def list_packages(self) -> List[Dict]:
        """列出所有包（摘要信息）"""
        result = []
        for name, info in self._packages.items():
            result.append({
                'name': name,
                'version': info.get('version', '0.0.0'),
                'description': info.get('description', ''),
                'keywords': info.get('keywords', []),
                'authors': info.get('authors', []),
                'updated_at': info.get('updated_at', ''),
                'download_count': info.get('download_count', 0),
            })
        return result

    def get_package(self, name: str) -> Optional[Dict]:
        """获取包详情"""
        info = self._packages.get(name)
        if info:
            info['download_count'] = info.get('download_count', 0)
        return info

    def get_package_version(self, name: str, version: str) -> Optional[Dict]:
        """获取特定版本"""
        info = self._packages.get(name)
        if info and info.get('version') == version:
            info['download_count'] = info.get('download_count', 0)
            return info
        return None

    def list_package_versions(self, name: str) -> List[Dict]:
        """列出包的所有版本（版本历史）"""
        info = self._packages.get(name)
        if not info:
            return []
        # 如果包有版本历史，返回历史；否则只返回当前版本
        version_history = info.get('version_history', [])
        if version_history:
            return version_history
        return [{
            'version': info.get('version', '0.0.0'),
            'published_at': info.get('published_at', ''),
            'description': info.get('description', ''),
        }]

    def search(self, query: str) -> List[Dict]:
        """搜索包"""
        query_lower = query.lower()
        results = []
        seen_names = set()
        for name, info in self._packages.items():
            score = 0
            # 精确匹配权重最高
            if query_lower == name.lower():
                score = 100
            elif query_lower in name.lower():
                score = 80
            # 关键词匹配
            for kw in info.get('keywords', []):
                if query_lower == kw.lower():
                    score = max(score, 70)
                elif query_lower in kw.lower():
                    score = max(score, 50)
            # 描述匹配
            if query_lower in info.get('description', '').lower():
                score = max(score, 30)
            if score > 0:
                results.append({
                    'name': name,
                    'version': info.get('version', '0.0.0'),
                    'description': info.get('description', ''),
                    'keywords': info.get('keywords', []),
                    'score': score,
                    'download_count': info.get('download_count', 0),
                })
                seen_names.add(name)
        # 按分数降序排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def publish(self, package_data: Dict) -> bool:
        """发布包"""
        name = package_data.get('name')
        if not name:
            return False

        required = ['name', 'version']
        for field in required:
            if field not in package_data:
                return False

        version = package_data['version']
        if not re.match(r'^\d+\.\d+\.\d+', version):
            return False

        now = datetime.now().isoformat()

        # 保存版本历史
        if name in self._packages:
            old_info = self._packages[name]
            old_version = old_info.get('version', '')
            version_history = old_info.get('version_history', [])
            # 如果版本不同，记录旧版本到历史
            if old_version and old_version != version:
                version_history.append({
                    'version': old_version,
                    'published_at': old_info.get('published_at', now),
                    'description': old_info.get('description', ''),
                })
            package_data['version_history'] = version_history
            package_data['download_count'] = old_info.get('download_count', 0)
            package_data['published_at'] = old_info.get(
                'published_at', now
            )
        else:
            package_data['download_count'] = 0
            package_data['version_history'] = []
            package_data['published_at'] = now

        package_data['updated_at'] = now
        self._packages[name] = package_data
        self._save()
        return True

    def delete_package(self, name: str) -> bool:
        """删除包"""
        if name in self._packages:
            del self._packages[name]
            self._save()
            return True
        return False

    def record_download(self, name: str) -> bool:
        """记录一次下载"""
        if name in self._packages:
            self._packages[name]['download_count'] = self._packages[name].get('download_count', 0) + 1
            self._save()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """获取注册中心统计信息"""
        total_packages = len(self._packages)
        total_downloads = sum(
            info.get('download_count', 0) for info in self._packages.values()
        )
        total_versions = sum(
            len(info.get('version_history', [])) + 1
            for info in self._packages.values()
        )
        return {
            'total_packages': total_packages,
            'total_downloads': total_downloads,
            'total_versions': total_versions,
            'updated_at': datetime.now().isoformat(),
        }


# ---------------------------------------------------------------------------
# HTTP 处理器
# ---------------------------------------------------------------------------

class RegistryHandler(BaseHTTPRequestHandler):
    """注册中心 HTTP 请求处理器"""

    store = RegistryStore()

    def _send_json(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _send_error(self, status: int, message: str):
        """发送错误响应"""
        self._send_json({'error': message}, status)

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        query = parse_qs(parsed.query)

        # GET /api/v1/packages
        if path == '/api/v1/packages':
            packages = self.store.list_packages()
            self._send_json({'packages': packages, 'count': len(packages)})
            return

        # GET /api/v1/stats
        if path == '/api/v1/stats':
            stats = self.store.get_stats()
            self._send_json(stats)
            return

        # GET /api/v1/search?q=...
        if path == '/api/v1/search':
            q = query.get('q', [''])[0]
            if not q:
                self._send_error(400, '缺少搜索关键词 q')
                return
            results = self.store.search(q)
            self._send_json({'results': results, 'count': len(results)})
            return

        # GET /api/v1/packages/{name}/versions
        versions_match = re.match(r'^/api/v1/packages/([^/]+)/versions$', path)
        if versions_match:
            name = unquote(versions_match.group(1))
            versions = self.store.list_package_versions(name)
            if not versions:
                self._send_error(404, f'包 {name} 未找到')
                return
            self._send_json({'name': name, 'versions': versions, 'count': len(versions)})
            return

        # GET /api/v1/packages/{name}/{version}
        pkg_match = re.match(r'^/api/v1/packages/([^/]+)/([^/]+)$', path)
        if pkg_match:
            name = unquote(pkg_match.group(1))
            version = pkg_match.group(2)
            info = self.store.get_package_version(name, version)
            if info is None:
                self._send_error(404, f'包 {name}@{version} 未找到')
                return
            # 记录下载
            self.store.record_download(name)
            self._send_json(info)
            return

        # GET /api/v1/packages/{name}
        pkg_match = re.match(r'^/api/v1/packages/([^/]+)$', path)
        if pkg_match:
            name = unquote(pkg_match.group(1))
            info = self.store.get_package(name)
            if info is None:
                self._send_error(404, f'包 {name} 未找到')
                return
            self._send_json(info)
            return

        # 健康检查
        if path == '/health':
            self._send_json({'status': 'ok', 'version': '2.0.0'})
            return

        self._send_error(404, f'未找到路由: {path}')

    def do_POST(self):
        """处理 POST 请求"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        # POST /api/v1/packages
        if path == '/api/v1/packages':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error(400, '请求体为空')
                return

            try:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self._send_error(400, f'JSON 解析错误: {e}')
                return

            if self.store.publish(data):
                self._send_json({'success': True, 'message': f"包 '{data.get('name')}' 发布成功"}, 201)
            else:
                self._send_error(400, '发布失败: 缺少必要字段或版本号格式无效')
            return

        self._send_error(404, f'未找到路由: {path}')

    def do_DELETE(self):
        """处理 DELETE 请求"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        # DELETE /api/v1/packages/{name}
        pkg_match = re.match(r'^/api/v1/packages/([^/]+)$', path)
        if pkg_match:
            name = unquote(pkg_match.group(1))
            if self.store.delete_package(name):
                self._send_json({'success': True, 'message': f"包 '{name}' 已删除"})
            else:
                self._send_error(404, f'包 {name} 未找到')
            return

        self._send_error(404, f'未找到路由: {path}')

    def log_message(self, format, *args):
        """自定义日志格式"""
        sys.stderr.write(f"[{datetime.now().isoformat()}] {args[0]} {args[1]} {args[2]}\n")


# ---------------------------------------------------------------------------
# 启动
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description='段言包注册中心服务器')
    parser.add_argument('--port', '-p', type=int, default=8000, help='监听端口（默认: 8000）')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址（默认: 0.0.0.0）')
    parser.add_argument('--data-dir', default=None, help='数据存储目录（默认: ./registry_data）')
    args = parser.parse_args()

    if args.data_dir:
        RegistryHandler.store = RegistryStore(args.data_dir)

    server = HTTPServer((args.host, args.port), RegistryHandler)
    print(f"段言包注册中心服务器启动")
    print(f"  地址: http://{args.host}:{args.port}")
    print(f"  API:  http://{args.host}:{args.port}/api/v1/packages")
    print(f"  搜索: http://{args.host}:{args.port}/api/v1/search?q=关键词")
    print(f"  统计: http://{args.host}:{args.port}/api/v1/stats")
    print(f"  数据: {RegistryHandler.store.data_dir}")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.server_close()


if __name__ == '__main__':
    main()