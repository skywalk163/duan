"""
段言（Duan）编程语言 - 模块解析器

实现功能：
1. 模块查找（搜索.duan文件）
2. 依赖图构建
3. 循环依赖检测
4. 拓扑排序（确定编译顺序）
"""

import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field

# 添加父目录到路径
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer import Lexer
from duan_parser_v3 import DuanParser, ImportStmt


# =============================================================================
# 错误类型
# =============================================================================

class ModuleError(Exception):
    """模块相关错误基类"""
    pass


class ModuleNotFoundError(ModuleError):
    """模块未找到"""
    def __init__(self, module_name: str, search_paths: List[str]):
        self.module_name = module_name
        self.search_paths = search_paths
        message = f"模块未找到: '{module_name}'\n搜索路径:\n"
        for path in search_paths:
            message += f"  - {path}\n"
        super().__init__(message)


class CircularDependencyError(ModuleError):
    """循环依赖错误"""
    def __init__(self, cycle: List[str]):
        self.cycle = cycle
        message = "检测到循环依赖:\n  " + " → ".join(cycle)
        super().__init__(message)


# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class ModuleInfo:
    """模块信息"""
    name: str                    # 模块名
    path: Path                   # 文件路径
    imports: List[ImportStmt]    # 导入的模块
    dependencies: Set[str] = field(default_factory=set)  # 依赖的模块名
    exports: List[str] = field(default_factory=list)     # 导出的符号
    
    def __repr__(self):
        return f"ModuleInfo({self.name}, deps={self.dependencies})"


@dataclass
class DependencyGraph:
    """依赖图"""
    nodes: Dict[str, ModuleInfo] = field(default_factory=dict)
    edges: Dict[str, Set[str]] = field(default_factory=dict)
    
    def add_module(self, module: ModuleInfo):
        """添加模块节点"""
        self.nodes[module.name] = module
        if module.name not in self.edges:
            self.edges[module.name] = set()
    
    def add_dependency(self, from_module: str, to_module: str):
        """添加依赖关系"""
        if from_module not in self.edges:
            self.edges[from_module] = set()
        self.edges[from_module].add(to_module)
    
    def get_dependencies(self, module_name: str) -> Set[str]:
        """获取模块的直接依赖"""
        return self.edges.get(module_name, set())
    
    def get_all_dependencies(self, module_name: str) -> Set[str]:
        """获取模块的所有依赖（递归）"""
        all_deps = set()
        to_visit = list(self.get_dependencies(module_name))
        
        while to_visit:
            dep = to_visit.pop()
            if dep not in all_deps:
                all_deps.add(dep)
                to_visit.extend(self.get_dependencies(dep))
        
        return all_deps


# =============================================================================
# 模块解析器
# =============================================================================

class ModuleResolver:
    """模块解析器"""
    
    def __init__(self, search_paths: List[str] = None):
        """
        初始化模块解析器
        
        Args:
            search_paths: 模块搜索路径列表，None表示使用默认路径
        """
        # 默认搜索路径：当前目录 + stdlib 目录
        if search_paths is None:
            stdlib_path = os.path.join(os.path.dirname(__file__), '..', 'stdlib')
            search_paths = ['.', stdlib_path]
        self.search_paths = search_paths
        self.lexer = Lexer()
        self.parser = DuanParser()
        self.module_cache: Dict[str, ModuleInfo] = {}
    
    def find_module(self, module_name: str, from_dir: str = None) -> Path:
        """
        查找模块文件
        
        Args:
            module_name: 模块名
            from_dir: 从哪个目录开始查找（用于相对导入）
        
        Returns:
            模块文件路径
        
        Raises:
            ModuleNotFoundError: 模块未找到
        """
        # 模块文件名
        module_file = f"{module_name}.duan"
        
        # 构建搜索路径
        search_dirs = []
        
        # 1. 从当前目录查找（如果有）
        if from_dir:
            search_dirs.append(from_dir)
        
        # 2. 从搜索路径查找
        search_dirs.extend(self.search_paths)
        
        # 3. 从环境变量 DUAN_PATH 查找
        duan_path = os.environ.get('DUAN_PATH', '')
        if duan_path:
            search_dirs.extend(duan_path.split(os.pathsep))
        
        # 搜索
        searched = []
        for search_dir in search_dirs:
            search_path = Path(search_dir)
            if not search_path.is_absolute():
                search_path = Path.cwd() / search_path
            
            module_path = search_path / module_file
            searched.append(str(module_path))
            
            if module_path.exists():
                return module_path.resolve()
        
        # 未找到
        raise ModuleNotFoundError(module_name, searched)
    
    def parse_module(self, module_path: Path) -> ModuleInfo:
        """
        解析模块文件
        
        Args:
            module_path: 模块文件路径
        
        Returns:
            模块信息
        """
        # 检查缓存
        module_name = module_path.stem
        if module_name in self.module_cache:
            return self.module_cache[module_name]
        
        # 读取文件
        with open(module_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 词法分析和语法解析
        tokens = self.lexer.tokenize(source)
        module_ast = self.parser.parse(source)
        
        # 提取导入语句
        imports = []
        dependencies = set()
        
        for stmt in module_ast.statements:
            if isinstance(stmt, ImportStmt):
                imports.append(stmt)
                dependencies.add(stmt.module_name)
        
        # 提取导出符号
        exports = []
        for stmt in module_ast.statements:
            if hasattr(stmt, 'symbols') and stmt.symbols:
                if stmt.symbols == ['*']:
                    # 导出全部，需要收集所有函数名
                    for s in module_ast.statements:
                        if hasattr(s, 'name') and hasattr(s, 'params'):
                            # 这是段落定义
                            exports.append(s.name)
                else:
                    exports.extend(stmt.symbols)
        
        # 创建模块信息
        module_info = ModuleInfo(
            name=module_name,
            path=module_path,
            imports=imports,
            dependencies=dependencies,
            exports=exports
        )
        
        # 缓存
        self.module_cache[module_name] = module_info
        
        return module_info
    
    def build_dependency_graph(self, main_module: str, from_dir: str = None) -> DependencyGraph:
        """
        构建依赖图
        
        Args:
            main_module: 主模块名
            from_dir: 主模块所在目录
        
        Returns:
            依赖图
        """
        graph = DependencyGraph()
        visited = set()
        
        def visit(module_name: str, module_dir: str = None):
            """访问模块并构建依赖图"""
            if module_name in visited:
                return
            
            visited.add(module_name)
            
            # 查找模块
            module_path = self.find_module(module_name, module_dir)
            
            # 解析模块
            module_info = self.parse_module(module_path)
            
            # 添加到图
            graph.add_module(module_info)
            
            # 处理依赖
            module_dir = str(module_path.parent)
            for dep_name in module_info.dependencies:
                try:
                    visit(dep_name, module_dir)
                    graph.add_dependency(module_name, dep_name)
                except ModuleNotFoundError as e:
                    print(f"警告: {e}")
        
        # 从主模块开始构建
        visit(main_module, from_dir)
        
        return graph
    
    def detect_circular_dependency(self, graph: DependencyGraph) -> Optional[List[str]]:
        """
        检测循环依赖
        
        Args:
            graph: 依赖图
        
        Returns:
            循环依赖路径，如果没有则返回 None
        """
        # 使用 DFS 检测环
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in graph.nodes}
        parent = {}
        
        def dfs(node: str) -> Optional[List[str]]:
            """深度优先搜索检测环"""
            color[node] = GRAY
            
            for neighbor in graph.get_dependencies(node):
                if color.get(neighbor, WHITE) == GRAY:
                    # 找到环，构建环路径
                    cycle = [neighbor]
                    current = node
                    while current != neighbor:
                        cycle.append(current)
                        current = parent.get(current)
                        if current is None:
                            break
                    cycle.append(neighbor)
                    return list(reversed(cycle))
                
                if color.get(neighbor, WHITE) == WHITE:
                    parent[neighbor] = node
                    result = dfs(neighbor)
                    if result:
                        return result
            
            color[node] = BLACK
            return None
        
        # 从每个未访问的节点开始
        for node in graph.nodes:
            if color[node] == WHITE:
                result = dfs(node)
                if result:
                    return result
        
        return None
    
    def topological_sort(self, graph: DependencyGraph) -> List[str]:
        """
        拓扑排序（确定编译顺序）
        
        Args:
            graph: 依赖图
        
        Returns:
            模块名列表（按编译顺序）
        """
        # 使用 Kahn 算法
        in_degree = {node: 0 for node in graph.nodes}
        
        # 计算入度
        for node in graph.nodes:
            for dep in graph.get_dependencies(node):
                if dep in in_degree:
                    in_degree[node] += 1
        
        # 找到所有入度为0的节点
        queue = [node for node, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            # 按字典序排序，保证确定性
            queue.sort()
            node = queue.pop(0)
            result.append(node)
            
            # 更新依赖此节点的模块的入度
            for other in graph.nodes:
                if node in graph.get_dependencies(other):
                    in_degree[other] -= 1
                    if in_degree[other] == 0:
                        queue.append(other)
        
        # 检查是否所有节点都已处理
        if len(result) != len(graph.nodes):
            # 有环，不应该发生（应该先检测环）
            remaining = [node for node in graph.nodes if node not in result]
            raise CircularDependencyError(remaining)
        
        return result
    
    def resolve(self, main_file: str) -> Tuple[List[ModuleInfo], DependencyGraph]:
        """
        解析主文件及其所有依赖
        
        Args:
            main_file: 主文件路径
        
        Returns:
            (模块列表（按编译顺序），依赖图)
        
        Raises:
            ModuleNotFoundError: 模块未找到
            CircularDependencyError: 循环依赖
        """
        # 获取主模块信息
        main_path = Path(main_file).resolve()
        main_dir = str(main_path.parent)
        main_name = main_path.stem
        
        # 构建依赖图
        graph = self.build_dependency_graph(main_name, main_dir)
        
        # 检测循环依赖
        cycle = self.detect_circular_dependency(graph)
        if cycle:
            raise CircularDependencyError(cycle)
        
        # 拓扑排序
        order = self.topological_sort(graph)
        
        # 按顺序获取模块信息
        modules = [graph.nodes[name] for name in order]
        
        return modules, graph


# =============================================================================
# ModuleDependencyResolver —— 从入口模块递归解析依赖 + 拓扑排序
# =============================================================================

@dataclass
class ResolvedModule:
    """已解析模块（用于 compile_project 跨模块链接）"""
    name: str
    path: Path
    imports: List[str] = field(default_factory=list)
    source: str = ""
    ast: Any = None  # duan_parser_v3.Module
    exports: List[str] = field(default_factory=list)  # 可外部可见的符号名


class CircularDependencyError(Exception):
    """循环依赖错误（与上方重名但可共存，此处保持清晰）"""

    def __init__(self, cycle: List[str]):
        self.cycle = list(cycle)
        super().__init__("检测到循环依赖: " + " -> ".join(self.cycle))


class ModuleDependencyResolver:
    """递归解析入口模块及所有 import 依赖，进行循环检测与拓扑排序。

    与模块中的 ImportStmt（`导入 模块`、`从 模块 导入 符号`）协同工作。
    """

    def __init__(self, search_paths: List[Path]):
        # 规范化搜索路径
        self.search_paths: List[Path] = [Path(p) for p in search_paths]
        self.modules: Dict[str, ResolvedModule] = {}

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------
    def resolve_all(self, entry_module_name: str, source: str
                     ) -> Dict[str, ResolvedModule]:
        """从入口模块出发，递归解析所有导入的模块。"""
        visited: Set[str] = set()
        stack: List[str] = []
        try:
            self._resolve_recursive(entry_module_name, source, visited, stack)
        except CircularDependencyError:
            raise
        return self.modules

    def topological_order(self) -> List[str]:
        """返回模块拓扑排序结果（被依赖的在前）。"""
        order: List[str] = []
        visited: Set[str] = set()
        temp: Set[str] = set()

        def visit(name: str) -> None:
            if name in visited:
                return
            if name in temp:
                cycle = list(temp) + [name]
                raise CircularDependencyError(cycle)
            temp.add(name)
            if name in self.modules:
                for imp in self.modules[name].imports:
                    visit(imp)
            temp.discard(name)
            visited.add(name)
            order.append(name)

        # 先处理入口，再处理其余
        entry_candidates = list(self.modules.keys())
        for name in entry_candidates:
            visit(name)
        return order

    # ------------------------------------------------------------------
    # 内部实现
    # ------------------------------------------------------------------
    def _resolve_recursive(self, module_name: str, source: str,
                           visited: Set[str], stack: List[str]) -> None:
        if module_name in visited:
            return
        if module_name in stack:
            idx = stack.index(module_name)
            cycle = stack[idx:] + [module_name]
            raise CircularDependencyError(cycle)

        # 解析 AST
        try:
            from duan_parser_v3 import DuanParser  # type: ignore
            parser = DuanParser()
            ast_node = parser.parse(source)
        except Exception:
            # 解析失败，跳过（由 compiler 报告错误）
            ast_node = None

        imports = self._extract_imports(ast_node)
        exports = self._extract_exports(ast_node)

        # 记录已解析模块
        default_path = self._find_module_path(module_name) or \
            Path(f"{module_name}.duan")
        self.modules[module_name] = ResolvedModule(
            name=module_name,
            path=default_path,
            imports=list(imports),
            source=source,
            ast=ast_node,
            exports=exports,
        )
        # 注意：此时 *不* 将 module_name 加入 visited，
        # 否则循环依赖检测失效。依赖处理结束后再标记 visited。

        # 递归解析导入
        new_stack = stack + [module_name]
        for imp in imports:
            if imp in visited:
                continue
            if imp in new_stack:
                raise CircularDependencyError(new_stack + [imp])
            module_path = self._find_module_path(imp)
            if module_path is None:
                # 找不到文件的模块，使用占位空模块（由 compiler 做警告）
                self.modules[imp] = ResolvedModule(
                    name=imp,
                    path=Path(f"{imp}.duan"),
                    imports=[],
                    source="",
                    ast=None,
                    exports=[],
                )
                visited.add(imp)
                continue
            try:
                sub_source = module_path.read_text(encoding="utf-8")
            except OSError:
                continue
            self._resolve_recursive(imp, sub_source, visited, new_stack)

        # 所有依赖处理完毕，再标记 visited
        visited.add(module_name)

    def _extract_imports(self, ast_node: Any) -> List[str]:
        """从 AST 中提取所有导入的模块名（支持 导入 / 使用 两种语法）。"""
        imports: List[str] = []
        if ast_node is None:
            return imports
        statements = getattr(ast_node, "statements", None) or []
        for stmt in statements:
            type_name = type(stmt).__name__
            if type_name == "ImportStmt":
                # `导入 模块` 或 `从 模块 导入 符号`
                mod_name = getattr(stmt, "module_name", None)
                if mod_name:
                    imports.append(mod_name)
            elif type_name == "UseStmt" or (hasattr(stmt, "module_name") and
                                              hasattr(stmt, "is_use")):
                # `使用 模块`（扩展形式）
                imports.append(stmt.module_name)
        return imports

    def _extract_exports(self, ast_node: Any) -> List[str]:
        """提取模块中可对外暴露的符号（段落/类 名）。

        - 若模块含显式 `导出 符号...` 语句，则只导出这些符号
        - 否则导出所有 `段 名(...)` 与 `类 名(...)`
        - 可选地支持公开的 / pub 标注前缀
        """
        names: List[str] = []
        if ast_node is None:
            return names
        statements = getattr(ast_node, "statements", None) or []

        explicit_exports: List[str] = []
        for stmt in statements:
            type_name = type(stmt).__name__
            if type_name == "ExportStmt":
                syms = getattr(stmt, "symbols", None) or []
                explicit_exports.extend(str(s) for s in syms)

        if explicit_exports:
            return list(dict.fromkeys(explicit_exports))

        # 隐式导出：收集所有段落与类定义
        for stmt in statements:
            type_name = type(stmt).__name__
            if type_name in ("Paragraph", "ParagraphDef", "FunctionDef",
                             "段定义"):
                name = getattr(stmt, "name", None)
                if name:
                    names.append(str(name))
            elif type_name in ("ClassDefinition", "ClassDef", "类定义"):
                name = getattr(stmt, "name", None)
                if name:
                    names.append(str(name))
        return list(dict.fromkeys(names))

    def _find_module_path(self, module_name: str) -> Optional[Path]:
        """根据模块名在搜索路径中寻找 .duan 文件。"""
        if not module_name:
            return None
        candidates = [
            f"{module_name}.duan",
            module_name.replace(".", os.sep) + ".duan",
            module_name.replace("/", os.sep) + ".duan",
        ]
        seen: Set[str] = set()
        for base in self.search_paths:
            if not base.exists():
                continue
            for cand in candidates:
                if cand in seen:
                    continue
                seen.add(cand)
                path = base / cand
                if path.is_file():
                    return path
        return None


# =============================================================================
# 模块加载器
# =============================================================================

class ModuleLoader:
    """模块加载器"""
    
    def __init__(self, resolver: ModuleResolver = None):
        """
        初始化模块加载器
        
        Args:
            resolver: 模块解析器
        """
        self.resolver = resolver or ModuleResolver()
        self.loaded_modules: Dict[str, ModuleInfo] = {}
    
    def load(self, module_name: str, from_dir: str = None) -> ModuleInfo:
        """
        加载模块
        
        Args:
            module_name: 模块名
            from_dir: 从哪个目录查找
        
        Returns:
            模块信息
        """
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        
        # 查找模块
        module_path = self.resolver.find_module(module_name, from_dir)
        
        # 解析模块
        module_info = self.resolver.parse_module(module_path)
        
        # 加载依赖
        module_dir = str(module_path.parent)
        for dep_name in module_info.dependencies:
            if dep_name not in self.loaded_modules:
                self.load(dep_name, module_dir)
        
        # 标记为已加载
        self.loaded_modules[module_name] = module_info
        
        return module_info
    
    def load_project(self, main_file: str) -> List[ModuleInfo]:
        """
        加载整个项目
        
        Args:
            main_file: 主文件路径
        
        Returns:
            模块列表（按依赖顺序）
        """
        modules, graph = self.resolver.resolve(main_file)
        return modules


# =============================================================================
# 测试
# =============================================================================

if __name__ == '__main__':
    print("="*60)
    print("段言模块解析器测试")
    print("="*60)
    
    # 创建测试环境
    test_dir = Path("examples/modules")
    
    # 测试1: 查找模块
    print("\n测试1: 查找模块")
    print("-"*60)
    
    resolver = ModuleResolver(search_paths=[str(test_dir)])
    
    try:
        module_path = resolver.find_module("math_utils")
        print(f"✓ 找到模块: {module_path}")
    except ModuleNotFoundError as e:
        print(f"✗ {e}")
    
    # 测试2: 解析模块
    print("\n测试2: 解析模块")
    print("-"*60)
    
    try:
        module_info = resolver.parse_module(module_path)
        print(f"✓ 模块名: {module_info.name}")
        print(f"  依赖: {module_info.dependencies}")
        print(f"  导出: {module_info.exports}")
    except Exception as e:
        print(f"✗ 解析失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试3: 构建依赖图
    print("\n测试3: 构建依赖图")
    print("-"*60)
    
    main_file = test_dir / "main.duan"
    
    if main_file.exists():
        try:
            graph = resolver.build_dependency_graph("main", str(test_dir))
            print(f"✓ 依赖图节点数: {len(graph.nodes)}")
            print("  模块列表:")
            for name, info in graph.nodes.items():
                print(f"    - {name} (依赖: {info.dependencies})")
        except Exception as e:
            print(f"✗ 构建失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 测试4: 检测循环依赖
    print("\n测试4: 检测循环依赖")
    print("-"*60)
    
    cycle = resolver.detect_circular_dependency(graph)
    if cycle:
        print(f"✗ 检测到循环依赖: {' → '.join(cycle)}")
    else:
        print("✓ 无循环依赖")
    
    # 测试5: 拓扑排序
    print("\n测试5: 拓扑排序")
    print("-"*60)
    
    try:
        order = resolver.topological_sort(graph)
        print(f"✓ 编译顺序: {' → '.join(order)}")
    except Exception as e:
        print(f"✗ 排序失败: {e}")
    
    # 测试6: 完整解析
    print("\n测试6: 完整解析")
    print("-"*60)
    
    if main_file.exists():
        try:
            modules, graph = resolver.resolve(str(main_file))
            print(f"✓ 解析成功，共 {len(modules)} 个模块")
            print("  编译顺序:")
            for i, module in enumerate(modules, 1):
                print(f"    {i}. {module.name} ({module.path.name})")
        except Exception as e:
            print(f"✗ 解析失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
