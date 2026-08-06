"""
段言（Duan）编程语言 - 增量编译系统

基于文件变更检测和依赖图追踪，实现仅重新编译变更文件及其依赖链。

核心机制：
1. 文件变更检测：基于 mtime + SHA256 内容哈希
2. 依赖图追踪：利用 module_resolver 的依赖图
3. 增量编译：仅重新编译变更文件及其下游依赖
4. 构建缓存：.duan_build_cache.json 持久化构建状态
"""

import os
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Set, List, Optional, Tuple
from dataclasses import dataclass, field, asdict


# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class FileState:
    """文件构建状态"""
    mtime: float          # 文件修改时间
    content_hash: str     # 文件内容 SHA256 哈希
    output_mtime: float   # 输出文件修改时间（0 表示不存在）

    def is_valid(self) -> bool:
        """检查缓存是否有效：输出文件存在"""
        return self.output_mtime > 0


@dataclass
class BuildCache:
    """构建缓存"""
    version: str = "1.0"
    created_at: float = 0.0
    updated_at: float = 0.0
    files: Dict[str, FileState] = field(default_factory=dict)
    # 依赖图快照：{模块名: [依赖模块名]}
    dep_graph: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'version': self.version,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'files': {k: asdict(v) for k, v in self.files.items()},
            'dep_graph': self.dep_graph,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BuildCache':
        cache = cls()
        cache.version = data.get('version', '1.0')
        cache.created_at = data.get('created_at', 0.0)
        cache.updated_at = data.get('updated_at', 0.0)
        for k, v in data.get('files', {}).items():
            cache.files[k] = FileState(**v)
        cache.dep_graph = data.get('dep_graph', {})
        return cache


# =============================================================================
# 增量构建器
# =============================================================================

class IncrementalBuilder:
    """增量编译构建器

    用法:
        builder = IncrementalBuilder(project_dir)
        changed_files = builder.detect_changes()
        builder.build(changed_files)
    """

    CACHE_FILENAME = '.duan_build_cache.json'

    def __init__(self, project_dir: str = '.'):
        self.project_dir = Path(project_dir).resolve()
        self.cache_path = self.project_dir / self.CACHE_FILENAME
        self.cache = self._load_cache()

        # 延迟导入 module_resolver（避免循环依赖）
        self._resolver = None

    @property
    def resolver(self):
        if self._resolver is None:
            from module_resolver import ModuleResolver
            self._resolver = ModuleResolver()
        return self._resolver

    # ------------------------------------------------------------------
    # 缓存管理
    # ------------------------------------------------------------------

    def _load_cache(self) -> BuildCache:
        """加载构建缓存"""
        if self.cache_path.exists():
            try:
                data = json.loads(self.cache_path.read_text(encoding='utf-8'))
                return BuildCache.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        cache = BuildCache()
        cache.created_at = time.time()
        cache.updated_at = time.time()
        return cache

    def _save_cache(self):
        """保存构建缓存"""
        self.cache.updated_at = time.time()
        self.cache_path.write_text(
            json.dumps(self.cache.to_dict(), ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    # ------------------------------------------------------------------
    # 文件变更检测
    # ------------------------------------------------------------------

    @staticmethod
    def _content_hash(file_path: Path) -> str:
        """计算文件内容哈希"""
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def _get_mtime(self, file_path: Path) -> float:
        """获取文件修改时间"""
        try:
            return file_path.stat().st_mtime
        except OSError:
            return 0.0

    def _get_output_mtime(self, source_path: Path) -> float:
        """获取输出文件修改时间"""
        output_path = source_path.with_suffix('.py')
        if output_path.exists():
            return self._get_mtime(output_path)
        return 0.0

    def detect_changes(self, duan_files: List[Path]) -> Tuple[Set[str], Set[str]]:
        """检测文件变更

        Args:
            duan_files: 项目中的 .duan 文件列表

        Returns:
            (changed_files, unchanged_files): 变更和未变更的文件路径集合
        """
        changed: Set[str] = set()
        unchanged: Set[str] = set()

        for f in duan_files:
            fpath = str(f.resolve())
            current_mtime = self._get_mtime(f)
            current_hash = self._content_hash(f)

            cached = self.cache.files.get(fpath)
            if cached is None:
                # 新文件：需要编译
                changed.add(fpath)
            elif cached.content_hash != current_hash:
                # 内容变更：需要编译
                changed.add(fpath)
            elif not cached.is_valid():
                # 输出文件不存在：需要编译
                changed.add(fpath)
            elif cached.mtime != current_mtime:
                # mtime 变更但内容未变（如 touch）：不需要编译，但更新缓存
                unchanged.add(fpath)
            else:
                # 完全未变更
                unchanged.add(fpath)

        return changed, unchanged

    def _build_dep_graph(self, main_file: Path) -> Dict[str, List[str]]:
        """构建依赖图

        Args:
            main_file: 入口文件路径

        Returns:
            依赖图字典：{模块名: [依赖模块名]}
        """
        try:
            result = self.resolver.resolve_module(main_file)
            graph = {}
            for mod_name, mod_info in result.items():
                if hasattr(mod_info, 'dependencies'):
                    graph[mod_name] = list(mod_info.dependencies)
                else:
                    graph[mod_name] = []
            return graph
        except Exception:
            return {}

    def _get_dependent_files(self, changed_files: Set[str], dep_graph: Dict[str, List[str]]) -> Set[str]:
        """获取需要重新编译的所有文件（变更文件 + 下游依赖）

        Args:
            changed_files: 变更的文件路径集合
            dep_graph: 依赖图

        Returns:
            需要重新编译的全部文件路径集合
        """
        # 构建反向依赖图：{模块: [依赖此模块的模块]}
        reverse_deps: Dict[str, Set[str]] = {}
        for module, deps in dep_graph.items():
            if module not in reverse_deps:
                reverse_deps[module] = set()
            for dep in deps:
                if dep not in reverse_deps:
                    reverse_deps[dep] = set()
                reverse_deps[dep].add(module)

        # BFS 收集所有受影响的下游
        affected: Set[str] = set(changed_files)
        queue = list(changed_files)
        visited: Set[str] = set(queue)

        # 将文件路径转换为模块名
        file_to_module: Dict[str, str] = {}
        for fpath in self.cache.files:
            module_name = Path(fpath).stem
            file_to_module[fpath] = module_name

        while queue:
            current = queue.pop(0)
            current_module = file_to_module.get(current)
            if current_module and current_module in reverse_deps:
                for downstream in reverse_deps[current_module]:
                    # 找到下游模块对应的文件路径
                    for fpath, mod_name in file_to_module.items():
                        if mod_name == downstream and fpath not in visited:
                            visited.add(fpath)
                            queue.append(fpath)
                            affected.add(fpath)

        # 同时包含变更文件自身
        return affected

    def build(self, duan_files: List[Path], main_file: Optional[Path] = None,
              force: bool = False, verbose: bool = True) -> int:
        """执行增量编译

        Args:
            duan_files: 项目中的 .duan 文件列表
            main_file: 入口文件（用于构建依赖图）
            force: 强制全量编译
            verbose: 是否输出详细信息

        Returns:
            编译成功数
        """
        if force:
            if verbose:
                print("[增量编译] 强制全量编译")
            return self._full_build(duan_files, verbose)

        # 1. 检测变更
        changed, unchanged = self.detect_changes(duan_files)

        if not changed:
            if verbose:
                print(f"[增量编译] 所有文件均未变更，跳过编译")
            return len(duan_files)

        # 2. 构建依赖图，计算受影响范围
        if main_file and main_file.exists():
            dep_graph = self._build_dep_graph(main_file)
            affected = self._get_dependent_files(changed, dep_graph)
        else:
            affected = changed

        if verbose:
            print(f"[增量编译] 变更文件: {len(changed)}, 受影响文件: {len(affected)}, 跳过: {len(unchanged)}")

        # 3. 仅编译受影响文件
        files_to_build = [f for f in duan_files if str(f.resolve()) in affected]
        return self._compile_files(files_to_build, verbose)

    def _full_build(self, duan_files: List[Path], verbose: bool = True) -> int:
        """全量编译（不使用增量缓存）"""
        return self._compile_files(duan_files, verbose)

    def _compile_files(self, files: List[Path], verbose: bool = True) -> int:
        """编译指定文件列表

        Args:
            files: 要编译的 .duan 文件列表
            verbose: 是否输出详细信息

        Returns:
            编译成功数
        """
        success_count = 0

        for f in files:
            try:
                source = f.read_text(encoding='utf-8')
                output_file = f.with_suffix('.py')

                # 使用 src 后端编译
                from duan_parser_v3 import DuanParser
                from code_generator import PythonCodeGenerator
                parser = DuanParser()
                module = parser.parse(source)
                if module is None:
                    if verbose:
                        print(f"[跳过] 解析失败: {f.name}", file=__import__('sys').stderr)
                    continue

                generator = PythonCodeGenerator()
                py_code = generator.generate(module)
                output_file.write_text(py_code, encoding='utf-8')

                # 更新缓存
                fpath = str(f.resolve())
                self.cache.files[fpath] = FileState(
                    mtime=self._get_mtime(f),
                    content_hash=self._content_hash(f),
                    output_mtime=self._get_output_mtime(f),
                )

                if verbose:
                    print(f"[编译] {f.name} -> {output_file.name}")
                success_count += 1

            except Exception as e:
                if verbose:
                    print(f"[错误] 编译 {f.name} 失败: {e}", file=__import__('sys').stderr)
                continue

        # 保存缓存
        self._save_cache()

        if verbose:
            print(f"\n[摘要] 成功: {success_count}/{len(files)}")

        return success_count

    def clear_cache(self):
        """清除构建缓存"""
        if self.cache_path.exists():
            self.cache_path.unlink()
        self.cache = BuildCache()
        self.cache.created_at = time.time()
        self.cache.updated_at = time.time()

    def get_stats(self) -> dict:
        """获取构建统计信息"""
        return {
            'cached_files': len(self.cache.files),
            'cache_created': self.cache.created_at,
            'cache_updated': self.cache.updated_at,
            'cache_path': str(self.cache_path),
            'dep_graph_nodes': len(self.cache.dep_graph),
        }


# =============================================================================
# CLI 工具函数
# =============================================================================

def incremental_build_cli(project_dir: str = '.', force: bool = False,
                           verbose: bool = True) -> int:
    """增量编译 CLI 入口

    Args:
        project_dir: 项目目录
        force: 强制全量编译
        verbose: 是否输出详细信息

    Returns:
        0 = 成功, 1 = 失败
    """
    root = Path(project_dir).resolve()
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}", file=__import__('sys').stderr)
        return 1

    duan_files = list(root.glob('*.duan'))
    if not duan_files:
        print(f"[错误] 未找到 .duan 文件: {root}", file=__import__('sys').stderr)
        return 1

    main_file = root / 'main.duan'
    if not main_file.exists():
        main_file = duan_files[0]

    builder = IncrementalBuilder(project_dir)
    result = builder.build(duan_files, main_file=main_file, force=force, verbose=verbose)

    return 0 if result > 0 else 1


if __name__ == '__main__':
    import sys
    force = '--force' in sys.argv or '-f' in sys.argv
    project = sys.argv[sys.argv.index('--dir') + 1] if '--dir' in sys.argv else '.'
    sys.exit(incremental_build_cli(project, force=force))