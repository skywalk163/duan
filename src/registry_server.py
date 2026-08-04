# -*- coding: utf-8 -*-
"""
段言在线包注册表服务器 (Duan Package Registry)

提供 HTTP API 用于包的发布、搜索、安装和版本管理。

API 端点:
  GET  /api/packages                   列出所有包
  GET  /api/packages/<name>            获取包信息
  GET  /api/packages/<name>/<version>  获取指定版本
  GET  /api/packages/<name>/download   下载包（最新版本）
  POST /api/packages/publish           发布包
  GET  /api/search?q=<query>           搜索包
  GET  /api/stats                      注册表统计

用法:
  python registry_server.py                    # 启动服务器（默认端口 8080）
  python registry_server.py --port 9000        # 指定端口
  python registry_server.py --dir ./registry   # 指定存储目录
"""

import os
import sys
import json
import hashlib
import argparse
import tempfile
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional, List


# =============================================================================
# 包存储
# =============================================================================

class PackageStorage:
    """包存储管理器"""

    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.packages_dir = self.storage_dir / 'packages'
        self.index_file = self.storage_dir / 'index.json'
        self._ensure_dirs()
        self.index = self._load_index()

    def _ensure_dirs(self):
        """确保目录存在"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'packages': {}, 'updated': str(datetime.now()), 'stats': {'total_packages': 0, 'total_versions': 0}}

    def _save_index(self):
        """保存索引"""
        self.index['updated'] = str(datetime.now())
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def list_packages(self) -> List[Dict]:
        """列出所有包"""
        pkgs = []
        for name, info in self.index['packages'].items():
            pkg = {
                'name': name,
                'latest_version': info.get('latest_version', '0.0.0'),
                'description': info.get('description', ''),
                'author': info.get('author', ''),
                'versions': list(info.get('versions', {}).keys()),
                'downloads': info.get('downloads', 0),
                'updated': info.get('updated', ''),
            }
            pkgs.append(pkg)
        return pkgs

    def get_package(self, name: str, version: str = None) -> Optional[Dict]:
        """获取包信息"""
        info = self.index['packages'].get(name)
        if not info:
            return None

        if version:
            ver_info = info.get('versions', {}).get(version)
            if not ver_info:
                return None
            return {
                'name': name,
                'version': version,
                'description': info.get('description', ''),
                'author': info.get('author', ''),
                'license': info.get('license', ''),
                'dependencies': ver_info.get('dependencies', {}),
                'published': ver_info.get('published', ''),
                'size': ver_info.get('size', 0),
                'sha256': ver_info.get('sha256', ''),
            }

        return {
            'name': name,
            'latest_version': info.get('latest_version', '0.0.0'),
            'description': info.get('description', ''),
            'author': info.get('author', ''),
            'license': info.get('license', ''),
            'versions': list(info.get('versions', {}).keys()),
            'downloads': info.get('downloads', 0),
            'updated': info.get('updated', ''),
        }

    def publish_package(self, pkg_data: bytes, pkg_name: str, version: str,
                        metadata: Dict) -> Dict:
        """发布包"""
        # 更新索引
        if pkg_name not in self.index['packages']:
            self.index['packages'][pkg_name] = {
                'latest_version': version,
                'description': metadata.get('description', ''),
                'author': metadata.get('author', ''),
                'license': metadata.get('license', ''),
                'versions': {},
                'downloads': 0,
                'updated': str(datetime.now()),
            }
            self.index['stats']['total_packages'] += 1
        else:
            self.index['packages'][pkg_name]['latest_version'] = version
            self.index['packages'][pkg_name]['description'] = metadata.get('description', '')
            self.index['packages'][pkg_name]['author'] = metadata.get('author', '')
            self.index['packages'][pkg_name]['updated'] = str(datetime.now())

        # 保存包文件
        sha256 = hashlib.sha256(pkg_data).hexdigest()
        pkg_dir = self.packages_dir / pkg_name
        pkg_dir.mkdir(parents=True, exist_ok=True)
        pkg_file = pkg_dir / f'{version}.zip'
        with open(pkg_file, 'wb') as f:
            f.write(pkg_data)

        # 更新版本信息
        self.index['packages'][pkg_name]['versions'][version] = {
            'published': str(datetime.now()),
            'size': len(pkg_data),
            'sha256': sha256,
            'dependencies': metadata.get('dependencies', {}),
        }
        self.index['stats']['total_versions'] += 1

        self._save_index()
        return {'status': 'published', 'name': pkg_name, 'version': version, 'sha256': sha256}

    def download_package(self, name: str, version: str = None) -> Optional[bytes]:
        """下载包"""
        info = self.index['packages'].get(name)
        if not info:
            return None

        if version is None:
            version = info.get('latest_version', '0.0.0')

        pkg_file = self.packages_dir / name / f'{version}.zip'
        if not pkg_file.exists():
            return None

        # 更新下载计数
        info['downloads'] = info.get('downloads', 0) + 1
        self._save_index()

        with open(pkg_file, 'rb') as f:
            return f.read()

    def search_packages(self, query: str) -> List[Dict]:
        """搜索包"""
        results = []
        q = query.lower()
        for name, info in self.index['packages'].items():
            if q in name.lower() or q in info.get('description', '').lower():
                results.append({
                    'name': name,
                    'latest_version': info.get('latest_version', '0.0.0'),
                    'description': info.get('description', ''),
                    'author': info.get('author', ''),
                    'downloads': info.get('downloads', 0),
                })
        return results

    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = self.index.get('stats', {})
        stats['storage_size'] = sum(
            f.stat().st_size for f in self.packages_dir.rglob('*.zip')
        )
        return stats


# =============================================================================
# HTTP 服务器
# =============================================================================

class RegistryHandler(BaseHTTPRequestHandler):
    """注册表 HTTP 处理器"""

    storage: PackageStorage = None  # 由外部设置

    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def _send_json(self, data: Any, status: int = 200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _send_error(self, message: str, status: int = 400):
        """发送错误响应"""
        self._send_json({'error': message}, status)

    def _send_binary(self, data: bytes, filename: str = 'package.zip'):
        """发送二进制响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/zip')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        params = parse_qs(parsed.query)

        try:
            # GET /api/packages
            if path == '/api/packages':
                pkgs = self.storage.list_packages()
                self._send_json({
                    'packages': pkgs,
                    'total': len(pkgs),
                    'registry': '段言包注册表',
                    'version': '1.0.0',
                })

            # GET /api/search?q=<query>
            elif path == '/api/search':
                query = params.get('q', [''])[0]
                results = self.storage.search_packages(query)
                self._send_json({
                    'results': results,
                    'query': query,
                    'total': len(results),
                })

            # GET /api/stats
            elif path == '/api/stats':
                stats = self.storage.get_stats()
                self._send_json(stats)

            # GET /api/packages/<name>/download
            elif path.endswith('/download'):
                pkg_name = path.split('/')[3] if len(path.split('/')) > 3 else ''
                version = params.get('version', [None])[0]
                data = self.storage.download_package(pkg_name, version)
                if data:
                    self._send_binary(data, f'{pkg_name}.zip')
                else:
                    self._send_error(f'Package not found: {pkg_name}', 404)

            # GET /api/packages/<name>/<version>
            elif len(path.split('/')) == 4 and path.split('/')[3] != 'download':
                parts = path.split('/')
                pkg_name = parts[3]
                try:
                    # 检查是否是版本号
                    version = parts[4] if len(parts) > 4 else None
                except IndexError:
                    version = params.get('version', [None])[0]

                pkg = self.storage.get_package(pkg_name, version)
                if pkg:
                    self._send_json(pkg)
                else:
                    self._send_error(f'Package not found: {pkg_name}', 404)

            # GET /api/packages/<name>
            elif len(path.split('/')) == 3:
                pkg_name = path.split('/')[2]
                version = params.get('version', [None])[0]
                pkg = self.storage.get_package(pkg_name, version)
                if pkg:
                    self._send_json(pkg)
                else:
                    self._send_error(f'Package not found: {pkg_name}', 404)

            # 根路径
            elif path == '' or path == '/':
                self._send_json({
                    'name': '段言包注册表',
                    'version': '1.0.0',
                    'endpoints': [
                        'GET  /api/packages',
                        'GET  /api/packages/<name>',
                        'GET  /api/packages/<name>/<version>',
                        'GET  /api/packages/<name>/download',
                        'POST /api/packages/publish',
                        'GET  /api/search?q=<query>',
                        'GET  /api/stats',
                    ],
                })

            else:
                self._send_error('Not Found', 404)

        except Exception as e:
            self._send_error(f'Internal error: {str(e)}', 500)

    def do_POST(self):
        """处理 POST 请求"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        # POST /api/packages/publish
        if path == '/api/packages/publish':
            content_length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')

            if 'multipart/form-data' in content_type:
                # 处理文件上传
                self._send_error('multipart upload not yet supported', 400)
                return

            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                pkg_name = data.get('name')
                version = data.get('version')
                metadata = data.get('metadata', {})

                if not pkg_name or not version:
                    self._send_error('Missing required fields: name, version', 400)
                    return

                # 从 payload 或外部文件获取包内容
                pkg_content = data.get('content')
                if pkg_content:
                    import base64
                    pkg_data = base64.b64decode(pkg_content)
                else:
                    # 创建最小包内容
                    pkg_data = self._create_minimal_package(pkg_name, version, metadata)

                result = self.storage.publish_package(pkg_data, pkg_name, version, metadata)
                self._send_json(result, 201)

            except json.JSONDecodeError:
                self._send_error('Invalid JSON', 400)
            except Exception as e:
                self._send_error(f'Publish failed: {str(e)}', 500)
        else:
            self._send_error('Not Found', 404)

    def _create_minimal_package(self, name: str, version: str, metadata: Dict) -> bytes:
        """创建最小包 zip 文件"""
        import io
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            # duan.json
            pkg_json = {
                'name': name,
                'version': version,
                'description': metadata.get('description', ''),
                'author': metadata.get('author', ''),
                'license': metadata.get('license', 'MIT'),
                'dependencies': metadata.get('dependencies', {}),
            }
            zf.writestr('duan.json', json.dumps(pkg_json, indent=2, ensure_ascii=False))
            # 主模块文件
            zf.writestr(f'{name}.duan', f'# {name} v{version}\n# 段言包\n\n段 主函数()：\n  打印 "Hello from {name}!"。\n')
        return buf.getvalue()


# =============================================================================
# 入口
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='段言在线包注册表服务器')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口（默认 8080）')
    parser.add_argument('--dir', type=str, default='./registry_data', help='存储目录（默认 ./registry_data）')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='绑定地址（默认 0.0.0.0）')
    args = parser.parse_args()

    # 初始化存储
    storage = PackageStorage(args.dir)
    RegistryHandler.storage = storage

    # 启动服务器
    server = HTTPServer((args.host, args.port), RegistryHandler)
    print(f'段言包注册表服务器已启动')
    print(f'  地址: http://{args.host}:{args.port}')
    print(f'  存储: {args.dir}')
    print(f'  包数: {storage.index["stats"]["total_packages"]}')
    print(f'  按 Ctrl+C 停止服务器')
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        server.shutdown()


if __name__ == '__main__':
    main()