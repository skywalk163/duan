"""
段言（Duan）编程语言 - 分级类型检查器

实现三级类型检查系统：
  Level 1 (签名级): 检查段落参数和返回值的类型标注
  Level 2 (变量级): 签名级 + 变量声明类型检查
  Level 3 (表达式级): 变量级 + 表达式运算类型检查

错误分级处理：
  - 参数类型缺失/不匹配 → 硬性报错（编译失败）
  - 变量类型标注缺失/不匹配 → 警告（编译继续）
  - 表达式运算类型不匹配 → 运行时检查（编译通过，运行时报错）

配置优先级：段落修饰符 > 文件级声明 > 全局配置
"""

import re
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum

from core.config import TypeCheckLevel, SegmentTypeMode


class TypeErrorSeverity(Enum):
    """类型错误严重级别"""
    ERROR = 'error'       # 硬性报错，编译失败
    WARNING = 'warning'   # 警告，编译继续
    RUNTIME = 'runtime'   # 运行时检查，编译通过


class TypeCheckResult:
    """类型检查结果"""
    __slots__ = ('severity', 'message', 'line', 'column', 'source_context')

    def __init__(self, severity: TypeErrorSeverity, message: str,
                 line: int = 0, column: int = 0, source_context: str = ''):
        self.severity = severity
        self.message = message
        self.line = line
        self.column = column
        self.source_context = source_context

    def __repr__(self):
        return f'[{self.severity.value}] {self.message}'

    def is_error(self) -> bool:
        return self.severity == TypeErrorSeverity.ERROR


class TypeCheckerConfig:
    """类型检查器配置（整合全局配置 + 文件级声明）"""

    __slots__ = ('check_level', 'default_segment_mode', 'inference_mode')

    def __init__(self, check_level: TypeCheckLevel = TypeCheckLevel.NONE,
                 default_segment_mode: SegmentTypeMode = SegmentTypeMode.LOOSE,
                 inference_mode: str = '渐进'):
        self.check_level = check_level
        self.default_segment_mode = default_segment_mode
        self.inference_mode = inference_mode

    @classmethod
    def from_duan_config(cls, config) -> 'TypeCheckerConfig':
        """从 DuanConfig 创建"""
        from core.config import DuanConfig
        return cls(
            check_level=getattr(config, 'type_check_level', TypeCheckLevel.NONE),
            default_segment_mode=getattr(config, 'default_segment_mode', SegmentTypeMode.LOOSE),
            inference_mode=getattr(config, 'type_inference_mode', '渐进'),
        )

    def apply_file_directives(self, source: str) -> 'TypeCheckerConfig':
        """从源代码中提取文件级类型声明指令并更新配置"""
        directives = _extract_type_directives(source)
        new_config = TypeCheckerConfig(
            check_level=self.check_level,
            default_segment_mode=self.default_segment_mode,
            inference_mode=self.inference_mode,
        )
        if '类型检查级别' in directives:
            level_str = directives['类型检查级别'].lower()
            level_map = {
                '签名': TypeCheckLevel.SIGNATURE,
                'signature': TypeCheckLevel.SIGNATURE, '1': TypeCheckLevel.SIGNATURE,
                '变量': TypeCheckLevel.VARIABLE,
                'variable': TypeCheckLevel.VARIABLE, '2': TypeCheckLevel.VARIABLE,
                '表达式': TypeCheckLevel.EXPRESSION,
                'expression': TypeCheckLevel.EXPRESSION, '3': TypeCheckLevel.EXPRESSION,
                '无': TypeCheckLevel.NONE, 'none': TypeCheckLevel.NONE, '0': TypeCheckLevel.NONE,
            }
            if level_str in level_map:
                new_config.check_level = level_map[level_str]
        if '类型模式' in directives:
            mode_str = directives['类型模式']
            if mode_str in ('严格', 'strict'):
                new_config.default_segment_mode = SegmentTypeMode.STRICT
            elif mode_str in ('松散', 'loose'):
                new_config.default_segment_mode = SegmentTypeMode.LOOSE
        return new_config

    def get_segment_check_level(self, modifiers: List[str]) -> TypeCheckLevel:
        """根据段落修饰符和配置确定该段落的检查级别"""
        if '严格' in modifiers:
            return TypeCheckLevel.EXPRESSION
        if '松散' in modifiers:
            return TypeCheckLevel.NONE
        if self.default_segment_mode == SegmentTypeMode.STRICT:
            return self.check_level if self.check_level != TypeCheckLevel.NONE else TypeCheckLevel.SIGNATURE
        return self.check_level


def _extract_type_directives(source: str) -> Dict[str, str]:
    """从源代码中提取文件级类型指令

    支持的指令格式：
      # 类型检查级别: 签名
      # 类型检查级别: 变量
      # 类型检查级别: 表达式
      # 类型检查级别: 无
      # 类型模式: 严格
      # 类型模式: 松散
    """
    directives: Dict[str, str] = {}
    for line in source.split('\n'):
        line = line.strip()
        m = re.match(r'^#\s*类型检查级别\s*[:：]\s*(.+?)\s*$', line)
        if m:
            directives['类型检查级别'] = m.group(1).strip()
            continue
        m = re.match(r'^#\s*类型模式\s*[:：]\s*(.+?)\s*$', line)
        if m:
            directives['类型模式'] = m.group(1).strip()
            continue
        # 非注释行后停止扫描
        if line and not line.startswith('#'):
            break
    return directives


# =============================================================================
# 类型检查器
# =============================================================================

class TypeChecker:
    """分级类型检查器

    使用方式：
        checker = TypeChecker(config)
        results = checker.check(module, inferencer)
        errors = [r for r in results if r.is_error()]
    """

    BUILTIN_TYPE_NAMES = {
        '数', '整数', '浮数', '串', '列', '典', '集',
        '布尔', '空', '任意', '文本', '小数',
        'int', 'float', 'str', 'bool', 'list', 'dict', 'set',
        'None', 'null',
    }

    def __init__(self, config: TypeCheckerConfig):
        self.config = config
        self.results: List[TypeCheckResult] = []
        self._inferencer = None
        self._checked_segments: Set[str] = set()

    def check(self, module, inferencer) -> List[TypeCheckResult]:
        """对模块进行分级类型检查"""
        self.results = []
        self._inferencer = inferencer
        self._checked_segments = set()

        if self.config.check_level == TypeCheckLevel.NONE:
            return self.results

        # 收集所有语句
        statements = getattr(module, 'statements', []) or []
        segments = getattr(module, 'segments', []) or []

        # 检查每个段落
        for seg in segments:
            self._check_segment(seg)

        # 检查顶层语句中的段落定义
        for stmt in statements:
            if hasattr(stmt, 'name') and hasattr(stmt, 'parameters'):
                self._check_segment(stmt)

        return self.results

    # ------------------------------------------------------------------
    # 段落检查
    # ------------------------------------------------------------------

    def _check_segment(self, seg) -> None:
        """对单个段落进行分级类型检查"""
        seg_name = getattr(seg, 'name', '?')
        modifiers = getattr(seg, 'modifiers', []) or []
        check_level = self.config.get_segment_check_level(modifiers)

        if check_level == TypeCheckLevel.NONE:
            return

        self._checked_segments.add(seg_name)

        # Level 1: 签名级检查（所有级别都包含）
        self._check_segment_signature(seg, check_level)

        # Level 2: 变量级检查
        if check_level.value >= TypeCheckLevel.VARIABLE.value:
            self._check_segment_variables(seg)

        # Level 3: 表达式级检查
        if check_level.value >= TypeCheckLevel.EXPRESSION.value:
            self._check_segment_expressions(seg)

    def _check_segment_signature(self, seg, check_level: TypeCheckLevel) -> None:
        """签名级检查：参数类型标注 + 返回值类型"""
        params = getattr(seg, 'parameters', []) or []
        return_type = getattr(seg, 'return_type', None)
        line = getattr(seg, 'line', 0)

        for param in params:
            if isinstance(param, dict):
                param_name = param.get('name', '?')
                param_type = param.get('type')
            elif hasattr(param, 'name'):
                param_name = param.name
                param_type = getattr(param, 'type_annotation', None)
            else:
                continue

            if param_type is None:
                if check_level.value >= TypeCheckLevel.EXPRESSION.value:
                    self._add_result(
                        TypeErrorSeverity.ERROR,
                        f"严格段落 '{seg.name}' 的参数 '{param_name}' 缺少类型标注",
                        line=line,
                    )
                else:
                    self._add_result(
                        TypeErrorSeverity.WARNING,
                        f"段落 '{seg.name}' 的参数 '{param_name}' 建议添加类型标注",
                        line=line,
                    )

        if return_type is None:
            if check_level.value >= TypeCheckLevel.EXPRESSION.value:
                pass  # 严格模式下返回值缺失只是警告，不阻塞编译

    def _check_segment_variables(self, seg) -> None:
        """变量级检查：检查段落内的变量声明"""
        body = getattr(seg, 'body', []) or []
        self._check_body_variables(body, seg.name)

    def _check_body_variables(self, body: List[Any], context: str) -> None:
        """递归检查代码块中的变量声明"""
        for stmt in body:
            if stmt is None:
                continue
            stmt_type = type(stmt).__name__

            if stmt_type == 'VarDecl':
                self._check_var_decl(stmt, context)
            elif stmt_type == 'VariableDeclaration':
                self._check_var_decl(stmt, context)
            elif stmt_type == 'IfStmt':
                self._check_body_variables(getattr(stmt, 'then_body', []) or [], context)
                self._check_body_variables(getattr(stmt, 'else_body', []) or [], context)
                for elseif_body in getattr(stmt, 'elseif_bodies', []) or []:
                    self._check_body_variables(elseif_body, context)
            elif stmt_type == 'WhileStmt':
                self._check_body_variables(getattr(stmt, 'body', []) or [], context)
            elif stmt_type == 'ForeachStmt':
                self._check_body_variables(getattr(stmt, 'body', []) or [], context)

    def _check_var_decl(self, stmt, context: str) -> None:
        """检查变量声明是否有类型标注"""
        name = getattr(stmt, 'name', '?')
        type_annotation = getattr(stmt, 'type_annotation', None)
        line = getattr(stmt, 'line', 0)

        if type_annotation is None:
            check_level = self.config.check_level
            if check_level.value >= TypeCheckLevel.VARIABLE.value:
                self._add_result(
                    TypeErrorSeverity.WARNING,
                    f"变量 '{name}'（在 '{context}' 中）建议添加类型标注",
                    line=line,
                )
        elif isinstance(type_annotation, str):
            if type_annotation not in self.BUILTIN_TYPE_NAMES:
                pass  # 可能是自定义类型，不在这里判断

    def _check_segment_expressions(self, seg) -> None:
        """表达式级检查：检查段落内的表达式类型兼容性"""
        body = getattr(seg, 'body', []) or []
        self._check_body_expressions(body, seg.name)

    def _check_body_expressions(self, body: List[Any], context: str) -> None:
        """递归检查代码块中的表达式类型"""
        for stmt in body:
            if stmt is None:
                continue
            stmt_type = type(stmt).__name__

            if stmt_type == 'VarDecl':
                self._check_expr_type(stmt, context)
            elif stmt_type == 'VariableDeclaration':
                self._check_expr_type(stmt, context)
            elif stmt_type == 'Assignment':
                self._check_expr_type(stmt, context)
            elif stmt_type == 'ReturnStmt':
                self._check_return_expr(stmt, context)
            elif stmt_type == 'IfStmt':
                self._check_body_expressions(getattr(stmt, 'then_body', []) or [], context)
                self._check_body_expressions(getattr(stmt, 'else_body', []) or [], context)
                for elseif_body in getattr(stmt, 'elseif_bodies', []) or []:
                    self._check_body_expressions(elseif_body, context)
            elif stmt_type == 'WhileStmt':
                self._check_body_expressions(getattr(stmt, 'body', []) or [], context)
            elif stmt_type == 'ForeachStmt':
                self._check_body_expressions(getattr(stmt, 'body', []) or [], context)
            elif stmt_type == 'ExpressionStatement':
                self._check_expr_type(stmt, context)

    def _check_expr_type(self, stmt, context: str) -> None:
        """检查表达式的类型兼容性（运行时检查级别）"""
        type_annotation = getattr(stmt, 'type_annotation', None)
        value = getattr(stmt, 'value', None)
        line = getattr(stmt, 'line', 0)

        if type_annotation and value and self._inferencer:
            try:
                inferred = self._inferencer.type_cache.get(id(value))
                if inferred:
                    from type_system import TypeParser
                    parser = TypeParser(self._inferencer.symbol_table)
                    expected = parser.parse(type_annotation)
                    if not inferred.is_subtype_of(expected):
                        self._add_result(
                            TypeErrorSeverity.RUNTIME,
                            f"类型不匹配: 期望 {type_annotation}，实际为 {inferred}",
                            line=line,
                        )
            except Exception:
                pass

    def _check_return_expr(self, stmt, context: str) -> None:
        """检查返回语句的类型兼容性"""
        line = getattr(stmt, 'line', 0)
        value = getattr(stmt, 'value', None)
        if value and self._inferencer:
            try:
                inferred = self._inferencer.type_cache.get(id(value))
                current_return = getattr(self._inferencer, '_current_return_type', None)
                if inferred and current_return:
                    if not inferred.is_subtype_of(current_return):
                        self._add_result(
                            TypeErrorSeverity.RUNTIME,
                            f"返回类型不匹配: 期望 {current_return}，实际为 {inferred}",
                            line=line,
                        )
            except Exception:
                pass

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _add_result(self, severity: TypeErrorSeverity, message: str,
                    line: int = 0, column: int = 0) -> None:
        self.results.append(TypeCheckResult(severity, message, line, column))

    def get_errors(self) -> List[TypeCheckResult]:
        return [r for r in self.results if r.is_error()]

    def get_warnings(self) -> List[TypeCheckResult]:
        return [r for r in self.results if r.severity == TypeErrorSeverity.WARNING]

    def get_runtime_checks(self) -> List[TypeCheckResult]:
        return [r for r in self.results if r.severity == TypeErrorSeverity.RUNTIME]

    def has_errors(self) -> bool:
        return any(r.is_error() for r in self.results)


# =============================================================================
# 便捷函数
# =============================================================================

def create_checker_from_config(duan_config) -> TypeChecker:
    """从 DuanConfig 创建类型检查器"""
    tc_config = TypeCheckerConfig.from_duan_config(duan_config)
    return TypeChecker(tc_config)


def create_checker_from_source(source: str, duan_config) -> TypeChecker:
    """从源代码和 DuanConfig 创建类型检查器（含文件级指令）"""
    tc_config = TypeCheckerConfig.from_duan_config(duan_config)
    tc_config = tc_config.apply_file_directives(source)
    return TypeChecker(tc_config)