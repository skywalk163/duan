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

    # 中文变量名模式到类型的映射（按语义匹配）
    CHINESE_TYPE_PATTERNS: Dict[str, str] = {
        # 整数类型
        "总数": "整数", "数量": "整数", "个数": "整数", "次数": "整数",
        "年龄": "整数", "序号": "整数", "索引": "整数", "长度": "整数",
        "大小": "整数", "计数": "整数", "编号": "整数", "年份": "整数",
        "月份": "整数", "日期": "整数", "天数": "整数", "小时": "整数",
        "分钟": "整数", "秒数": "整数", "行数": "整数", "列数": "整数",
        "页码": "整数", "版本": "整数", "层级": "整数", "级别": "整数",
        "步数": "整数", "人数": "整数", "数量级": "整数",
        # 浮点数类型
        "价格": "浮数", "金额": "浮数", "费用": "浮数", "工资": "浮数",
        "温度": "浮数", "利率": "浮数", "比率": "浮数", "比例": "浮数",
        "概率": "浮数", "速度": "浮数", "距离": "浮数", "面积": "浮数",
        "体积": "浮数", "重量": "浮数", "密度": "浮数", "利润": "浮数",
        "折扣": "浮数", "税率": "浮数", "分数": "浮数", "评分": "浮数",
        # 字符串类型
        "名称": "串", "名字": "串", "姓名": "串", "标题": "串",
        "描述": "串", "说明": "串", "备注": "串", "注释": "串",
        "地址": "串", "路径": "串", "网址": "串", "邮箱": "串",
        "电话": "串", "手机": "串", "密码": "串", "密钥": "串",
        "内容": "串", "消息": "串", "文本": "串", "摘要": "串",
        "标签": "串", "颜色": "串", "编码": "串", "格式": "串",
        "前缀": "串", "后缀": "串", "关键字": "串", "关键词": "串",
        "单位": "串", "状态": "串", "类型": "串", "类别": "串",
        "代码": "串", "消息体": "串", "错误信息": "串",
        # 布尔类型
        "是否": "布尔", "是": "布尔", "有": "布尔", "可用": "布尔",
        "启用": "布尔", "禁用": "布尔", "激活": "布尔", "可见": "布尔",
        "完成": "布尔", "成功": "布尔", "失败": "布尔", "通过": "布尔",
        "有效": "布尔", "过期": "布尔", "匹配": "布尔", "包含": "布尔",
        "存在": "布尔", "选中": "布尔", "展开": "布尔", "加载": "布尔",
        "就绪": "布尔", "繁忙": "布尔", "空": "布尔",
        # 列表类型
        "列表": "列", "数组": "列", "集合": "列", "清单": "列",
        "队列": "列", "堆栈": "列", "序列": "列", "列表项": "列",
        "结果集": "列", "数据列表": "列",
        # 字典类型
        "字典": "典", "映射": "典", "配置": "典", "设置": "典",
        "选项": "典", "参数表": "典", "属性表": "典", "键值对": "典",
        "环境变量": "典",
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
        value = getattr(stmt, 'value', None)
        line = getattr(stmt, 'line', 0)

        # 中文变量名类型推断
        chinese_type = self._infer_chinese_variable_type(name, value)
        if chinese_type:
            self._add_result(
                TypeErrorSeverity.WARNING,
                f"中文变量 '{name}'（在 '{context}' 中）语义推断为 '{chinese_type}' 类型"
                + (f"，当前类型标注为 '{type_annotation}'" if type_annotation and type_annotation != chinese_type else ""),
                line=line,
            )

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
    # 中文变量名类型推导
    # ------------------------------------------------------------------

    def _infer_chinese_variable_type(self, name: str, value_node=None) -> Optional[str]:
        """根据中文变量名语义推断类型

        通过匹配中文变量名中的语义关键词，推断变量应具有的类型。
        支持整数、浮点数、字符串、布尔、列表、字典类型的推断。

        Args:
            name: 变量名（中文或混合）
            value_node: 可选的初始值节点，用于辅助推断

        Returns:
            推断出的类型名称（如 "整数"、"浮数"、"串"、"布尔"、"列"、"典"），
            如果无法推断则返回 None
        """
        if not name or not isinstance(name, str):
            return None

        # 尝试精确匹配整个变量名
        if name in self.CHINESE_TYPE_PATTERNS:
            return self.CHINESE_TYPE_PATTERNS[name]

        # 尝试后缀匹配（中文变量名通常以语义词结尾）
        # 按长度降序匹配，优先匹配更长的模式
        sorted_patterns = sorted(self.CHINESE_TYPE_PATTERNS.items(), key=lambda x: -len(x[0]))
        for pattern, inferred_type in sorted_patterns:
            if name.endswith(pattern):
                return inferred_type

        # 尝试前缀匹配（仅对长度 >= 2 的模式进行前缀匹配，避免单字误匹配）
        for pattern, inferred_type in sorted_patterns:
            if len(pattern) >= 2 and name.startswith(pattern):
                return inferred_type

        # 如果变量名包含中文，尝试按语义规则推断
        if re.search(r'[\u4e00-\u9fff]', name):
            # 以"数"结尾的通常是整数
            if name.endswith("数"):
                return "整数"
            # 以"率"、"比"结尾的通常是浮点数
            if name.endswith("率") or name.endswith("比"):
                return "浮数"
            # 以"法"、"器"结尾的通常是某种对象，不确定类型
            if name.endswith("法") or name.endswith("器"):
                return None

        return None

    def _check_chinese_naming_convention(self, name: str, line: int = 0) -> None:
        """检查中文变量名是否符合类型命名约定

        根据 CHINESE_TYPE_PATTERNS 中的映射关系，检查变量名是否暗示了类型信息。
        如果变量名包含类型语义但未标注类型，给出建议。

        Args:
            name: 变量名
            line: 行号
        """
        if not name or not isinstance(name, str):
            return

        # 检查是否包含中文
        if not re.search(r'[\u4e00-\u9fff]', name):
            return

        inferred = self._infer_chinese_variable_type(name)
        if inferred:
            self._add_result(
                TypeErrorSeverity.WARNING,
                f"中文变量 '{name}' 语义暗示类型为 '{inferred}'，"
                f"建议添加类型标注以增强代码可读性",
                line=line,
            )

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

    def get_errors_with_chinese_type_info(self) -> List[TypeCheckResult]:
        """获取包含中文类型信息的错误列表

        在原有错误信息基础上，对涉及中文变量名的错误附加类型推断信息。

        Returns:
            包含中文类型推断信息的错误结果列表
        """
        enriched: List[TypeCheckResult] = []
        for r in self.results:
            if not r.is_error():
                continue
            # 检查消息中是否包含中文变量名并附加推断信息
            chinese_vars = re.findall(r"['\"]?([\u4e00-\u9fff]+)['\"]?", r.message)
            for var_name in chinese_vars:
                inferred = self._infer_chinese_variable_type(var_name)
                if inferred:
                    enriched.append(TypeCheckResult(
                        severity=r.severity,
                        message=f"{r.message}（中文变量名 '{var_name}' 推断类型为 '{inferred}'）",
                        line=r.line,
                        column=r.column,
                    ))
                    break
            else:
                enriched.append(r)
        return enriched

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