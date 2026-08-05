# -*- coding: utf-8 -*-
"""
段言（Duan）Level 6 类型注解系统测试

覆盖：
  1. TypeAnnotation AST 节点（创建、to_dict、_fields、__repr__、__slots__）
  2. 基本类型名映射（整数→int, 文本→str, 布尔→bool, 小数→float, 空→None）
  3. 可选类型包装（整数? → Optional[int]）
  4. 列表类型记法（[整数] → List[int]）
  5. 字典类型记法（{文本: 整数} → Dict[str, int]）
  6. 函数类型记法（接收 整数, 文本 返回 布尔 → Callable[[int, str], bool]）
  7. 类型注解零成本（不影响代码生成的运行时语义）
  8. type_checker 与带注解变量协同工作
  9. type_system.py 既有类型类（is_subtype_of / unify / TypeParser 等）
"""

import sys
import os
import types

# conftest.py 已将 src 与项目根加入 sys.path，这里保持与同级测试一致的显式保险
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest

from ast_nodes_v3 import (
    TypeAnnotation, VarDecl, NumberLiteral, StringLiteral, ASTNode,
)
from type_system import (
    Type, NumberType, StringType, BooleanType, NullType, AnyType, UnknownType,
    OptionalTypeWrapper, ListType, DictType, TupleType, SetType, FunctionType,
    TypeVar, GenericTypeInstance, ClassType, InterfaceType,
    TypeSubstitution, UnificationError, unify, TypeParser,
    TypeSymbolTable, TypeErrorInference,
    TYPE_NUMBER, TYPE_STRING, TYPE_BOOLEAN, TYPE_NULL, TYPE_ANY, TYPE_UNKNOWN,
)
from type_checker import (
    TypeChecker, TypeCheckerConfig, TypeErrorSeverity,
)
from core.config import TypeCheckLevel, SegmentTypeMode


# =============================================================================
# 1. TypeAnnotation 节点创建与序列化
# =============================================================================

class TestTypeAnnotationNode:
    """TypeAnnotation AST 节点基础行为"""

    def test_inherits_from_astnode(self):
        node = TypeAnnotation(base_type='整数')
        assert isinstance(node, ASTNode)

    def test_basic_creation_defaults(self):
        node = TypeAnnotation(base_type='整数')
        assert node.base_type == '整数'
        assert node.is_optional is False
        assert node.is_list is False
        assert node.is_dict is False
        assert node.key_type is None
        assert node.value_type is None
        assert node.params == []
        assert node.return_type is None

    def test_slots_does_not_allow_arbitrary_attrs(self):
        """__slots__ 限制：不能添加额外属性"""
        node = TypeAnnotation(base_type='整数')
        assert not hasattr(node, '__dict__')
        with pytest.raises(AttributeError):
            node.some_random_field = 1

    def test_slots_contains_all_declared_fields(self):
        expected = {
            'base_type', 'is_optional', 'is_list', 'is_dict',
            'key_type', 'value_type', 'params', 'return_type',
            # ASTNode 基类的 slots
            'line', 'col',
        }
        declared = set(TypeAnnotation.__slots__) | set(ASTNode.__slots__)
        assert expected.issubset(declared)

    def test_line_col_propagated_from_base(self):
        node = TypeAnnotation(base_type='整数', line=12, col=5)
        assert node.line == 12
        assert node.col == 5

    def test_to_dict_basic(self):
        node = TypeAnnotation(base_type='文本')
        d = node.to_dict()
        assert d['node'] == 'TypeAnnotation'
        assert d['base_type'] == '文本'
        assert d['is_optional'] is False
        assert d['is_list'] is False
        assert d['is_dict'] is False
        assert d['key_type'] is None
        assert d['value_type'] is None
        assert d['params'] == []
        assert d['return_type'] is None

    def test_to_dict_list(self):
        node = TypeAnnotation(base_type='整数', is_list=True)
        d = node.to_dict()
        assert d['is_list'] is True
        assert d['base_type'] == '整数'

    def test_to_dict_dict(self):
        node = TypeAnnotation(is_dict=True, key_type='文本', value_type='整数')
        d = node.to_dict()
        assert d['is_dict'] is True
        assert d['key_type'] == '文本'
        assert d['value_type'] == '整数'

    def test_to_dict_optional(self):
        node = TypeAnnotation(base_type='整数', is_optional=True)
        d = node.to_dict()
        assert d['is_optional'] is True

    def test_to_dict_function(self):
        node = TypeAnnotation(params=['整数', '文本'], return_type='布尔')
        d = node.to_dict()
        assert d['params'] == ['整数', '文本']
        assert d['return_type'] == '布尔'

    def test_to_dict_returns_independent_copy_of_params(self):
        """to_dict 返回的 params 列表应独立于内部状态"""
        src_params = ['整数', '文本']
        node = TypeAnnotation(params=src_params, return_type='布尔')
        d = node.to_dict()
        d['params'].append('被篡改')
        assert node.params == ['整数', '文本']  # 内部未受影响

    def test_fields_returns_tuple(self):
        node = TypeAnnotation(base_type='整数', is_optional=True)
        f = node._fields()
        assert isinstance(f, tuple)
        # 顺序：base_type, is_optional, is_list, is_dict, key_type, value_type, params, return_type
        assert f[0] == '整数'
        assert f[1] is True
        assert f[6] == ()  # 空 params 转为元组

    def test_fields_distinguishes_equal_nodes(self):
        a = TypeAnnotation(base_type='整数')
        b = TypeAnnotation(base_type='整数')
        c = TypeAnnotation(base_type='文本')
        assert a._fields() == b._fields()
        assert a._fields() != c._fields()

    def test_repr_basic(self):
        assert repr(TypeAnnotation(base_type='整数')) == 'TypeAnnotation(整数)'

    def test_repr_list(self):
        assert repr(TypeAnnotation(base_type='整数', is_list=True)) == 'TypeAnnotation([整数])'

    def test_repr_dict(self):
        node = TypeAnnotation(is_dict=True, key_type='文本', value_type='整数')
        assert repr(node) == 'TypeAnnotation({文本: 整数})'

    def test_repr_optional(self):
        assert repr(TypeAnnotation(base_type='整数', is_optional=True)) == 'TypeAnnotation(整数?)'

    def test_repr_function(self):
        node = TypeAnnotation(params=['整数', '文本'], return_type='布尔')
        assert repr(node) == 'TypeAnnotation(接收 整数, 文本 返回 布尔)'


# =============================================================================
# 2. 基本类型名映射
# =============================================================================

class TestBasicTypeMapping:
    """段言基本类型名 → Python 类型名"""

    @pytest.mark.parametrize('duan,py', [
        ('整数', 'int'),
        ('文本', 'str'),
        ('布尔', 'bool'),
        ('小数', 'float'),
        ('空', 'None'),
    ])
    def test_required_mapping(self, duan, py):
        """任务指定五组映射必须成立"""
        assert TypeAnnotation._map_basic(duan) == py

    @pytest.mark.parametrize('duan,py', [
        ('整数', 'int'),
        ('小数', 'float'),
        ('浮数', 'float'),
        ('数', 'float'),
        ('文本', 'str'),
        ('串', 'str'),
        ('布尔', 'bool'),
        ('空', 'None'),
        ('任意', 'Any'),
        ('列表', 'list'),
        ('列', 'list'),
        ('字典', 'dict'),
        ('典', 'dict'),
        ('集合', 'set'),
        ('集', 'set'),
    ])
    def test_full_mapping_table(self, duan, py):
        assert TypeAnnotation._DUAN_TO_PYTHON[duan] == py

    def test_unknown_type_passthrough(self):
        """未在映射表中的类型名原样返回（自定义类型）"""
        assert TypeAnnotation._map_basic('自定义类型') == '自定义类型'

    def test_to_python_type_basic(self):
        assert TypeAnnotation(base_type='整数').to_python_type() == 'int'
        assert TypeAnnotation(base_type='文本').to_python_type() == 'str'
        assert TypeAnnotation(base_type='布尔').to_python_type() == 'bool'
        assert TypeAnnotation(base_type='小数').to_python_type() == 'float'
        assert TypeAnnotation(base_type='空').to_python_type() == 'None'

    def test_mapping_consistent_with_code_generator(self):
        """TypeAnnotation 的类型映射应与 code_generator._map_type 一致"""
        from code_generator import PythonCodeGenerator
        gen = PythonCodeGenerator()
        for duan, py in TypeAnnotation._DUAN_TO_PYTHON.items():
            assert gen._map_type(duan) == py, f"映射不一致: {duan}"


# =============================================================================
# 3. 可选类型包装
# =============================================================================

class TestOptionalType:
    """整数? 形式的可选类型"""

    def test_optional_flag(self):
        node = TypeAnnotation(base_type='整数', is_optional=True)
        assert node.is_optional is True

    def test_to_python_type_optional(self):
        node = TypeAnnotation(base_type='整数', is_optional=True)
        assert node.to_python_type() == 'Optional[int]'

    def test_to_python_type_optional_text(self):
        node = TypeAnnotation(base_type='文本', is_optional=True)
        assert node.to_python_type() == 'Optional[str]'

    def test_optional_does_not_imply_list_or_dict(self):
        node = TypeAnnotation(base_type='整数', is_optional=True)
        assert node.is_list is False
        assert node.is_dict is False


# =============================================================================
# 4. 列表类型记法
# =============================================================================

class TestListType:
    """[整数] 形式的列表类型"""

    def test_list_flag_and_base_type(self):
        node = TypeAnnotation(base_type='整数', is_list=True)
        assert node.is_list is True
        assert node.base_type == '整数'

    def test_to_python_type_list(self):
        node = TypeAnnotation(base_type='整数', is_list=True)
        assert node.to_python_type() == 'List[int]'

    def test_to_python_type_list_text(self):
        node = TypeAnnotation(base_type='文本', is_list=True)
        assert node.to_python_type() == 'List[str]'

    def test_to_python_type_list_empty_base(self):
        """无元素类型的列表 → List[Any]"""
        node = TypeAnnotation(is_list=True)
        assert node.to_python_type() == 'List[Any]'

    def test_list_with_optional(self):
        """[整数]? → Optional[List[int]]"""
        node = TypeAnnotation(base_type='整数', is_list=True, is_optional=True)
        assert node.to_python_type() == 'Optional[List[int]]'


# =============================================================================
# 5. 字典类型记法
# =============================================================================

class TestDictType:
    """{文本: 整数} 形式的字典类型"""

    def test_dict_flags_and_kv(self):
        node = TypeAnnotation(is_dict=True, key_type='文本', value_type='整数')
        assert node.is_dict is True
        assert node.key_type == '文本'
        assert node.value_type == '整数'

    def test_to_python_type_dict(self):
        node = TypeAnnotation(is_dict=True, key_type='文本', value_type='整数')
        assert node.to_python_type() == 'Dict[str, int]'

    def test_to_python_type_dict_optional_value(self):
        node = TypeAnnotation(is_dict=True, key_type='文本', value_type='整数')
        # 字典本身可选
        node.is_optional = True
        assert node.to_python_type() == 'Optional[Dict[str, int]]'

    def test_to_python_type_dict_missing_kv(self):
        """缺少键/值类型 → Any 兜底"""
        node = TypeAnnotation(is_dict=True)
        assert node.to_python_type() == 'Dict[Any, Any]'

    def test_dict_takes_precedence_over_base_type(self):
        """is_dict=True 时优先按字典渲染，忽略 base_type"""
        node = TypeAnnotation(base_type='整数', is_dict=True, key_type='文本', value_type='小数')
        assert node.to_python_type() == 'Dict[str, float]'


# =============================================================================
# 6. 函数类型记法
# =============================================================================

class TestFunctionType:
    """接收 整数, 文本 返回 布尔 形式的函数类型"""

    def test_function_fields(self):
        node = TypeAnnotation(params=['整数', '文本'], return_type='布尔')
        assert node.params == ['整数', '文本']
        assert node.return_type == '布尔'

    def test_to_python_type_function(self):
        node = TypeAnnotation(params=['整数', '文本'], return_type='布尔')
        assert node.to_python_type() == 'Callable[[int, str], bool]'

    def test_to_python_type_function_single_param(self):
        node = TypeAnnotation(params=['小数'], return_type='小数')
        assert node.to_python_type() == 'Callable[[float], float]'

    def test_function_with_optional(self):
        node = TypeAnnotation(params=['整数'], return_type='布尔', is_optional=True)
        assert node.to_python_type() == 'Optional[Callable[[int], bool]]'

    def test_function_without_params_falls_back_to_basic(self):
        """仅有 return_type 而无 params 时，不视作函数类型"""
        node = TypeAnnotation(base_type='整数', return_type='布尔')
        assert node.to_python_type() == 'int'


# =============================================================================
# 7. 类型注解零成本（不影响代码生成的运行时语义）
# =============================================================================

class TestZeroCost:
    """类型注解为零成本：生成的代码运行时语义不变"""

    def _gen_var_decl(self, type_annotation):
        from code_generator import PythonCodeGenerator
        gen = PythonCodeGenerator()
        gen._generate_var_decl(
            VarDecl('x', NumberLiteral(10), type_annotation=type_annotation)
        )
        return gen.output_lines

    def test_annotated_and_unannotated_produce_same_runtime_value(self):
        lines_with = self._gen_var_decl('整数')
        lines_without = self._gen_var_decl(None)

        ns_with = {}
        ns_without = {}
        exec('\n'.join(lines_with), ns_with)
        exec('\n'.join(lines_without), ns_without)

        # 运行时值完全一致 —— 注解不改变语义
        assert ns_with['x'] == ns_without['x'] == 10

    def test_annotation_appears_in_generated_code(self):
        """类型注解确实被渲染为 Python 注解（: int）"""
        lines_with = self._gen_var_decl('整数')
        assert any(': int' in line for line in lines_with)

    def test_no_annotation_when_absent(self):
        lines_without = self._gen_var_decl(None)
        assert not any(': int' in line for line in lines_without)

    def test_runtime_type_check_off_by_default(self):
        """代码生成器默认关闭运行时类型检查（零开销）"""
        from code_generator import PythonCodeGenerator
        gen = PythonCodeGenerator()
        assert gen._runtime_type_check is False

    def test_no_runtime_check_inserted_when_disabled(self):
        """默认配置下不应注入 _duan_check_type 调用"""
        lines = self._gen_var_decl('整数')
        assert not any('_duan_check_type' in line for line in lines)

    def test_typeannotation_node_does_not_break_code_generator(self):
        """TypeAnnotation 节点对象本身不参与 code_generator 流程
        （code_generator 仅识别字符串形式 type_annotation）。
        将 TypeAnnotation 节点作为结构化表示独立于 codegen，互不干扰。
        """
        # TypeAnnotation 是结构化节点，与 codegen 用的字符串注解解耦
        node = TypeAnnotation(base_type='整数', is_list=True)
        # 它能独立产出 Python 类型表达式
        assert node.to_python_type() == 'List[int]'
        # 而 code_generator 仍使用字符串注解路径正常工作
        lines = self._gen_var_decl('整数')
        assert any('x' in line for line in lines)


# =============================================================================
# 8. type_checker 与带注解变量协同工作
# =============================================================================

def _make_module(segment):
    """构造一个最小模块对象，包含 segments 列表"""
    return types.SimpleNamespace(statements=[], segments=[segment])


def _make_segment(name, body, parameters=None, return_type=None, modifiers=None):
    """构造一个最小段落对象"""
    return types.SimpleNamespace(
        name=name,
        body=body,
        parameters=parameters or [],
        return_type=return_type,
        modifiers=modifiers or [],
    )


class TestTypeCheckerWithAnnotations:
    """分级类型检查器与变量类型注解"""

    def test_variable_level_warns_on_missing_annotation(self):
        """VARIABLE 级别下，缺少类型注解的变量应产生 WARNING"""
        body = [VarDecl('未注解变量', NumberLiteral(1), type_annotation=None)]
        seg = _make_segment('段落一', body)
        module = _make_module(seg)

        config = TypeCheckerConfig(
            check_level=TypeCheckLevel.VARIABLE,
            default_segment_mode=SegmentTypeMode.LOOSE,
        )
        checker = TypeChecker(config)
        results = checker.check(module, inferencer=None)

        warnings = [r for r in results if r.severity == TypeErrorSeverity.WARNING]
        assert len(warnings) == 1
        assert '未注解变量' in warnings[0].message

    def test_variable_level_no_warning_with_annotation(self):
        """VARIABLE 级别下，带类型注解的变量不应产生 WARNING"""
        body = [VarDecl('已注解变量', NumberLiteral(1), type_annotation='整数')]
        seg = _make_segment('段落一', body)
        module = _make_module(seg)

        config = TypeCheckerConfig(
            check_level=TypeCheckLevel.VARIABLE,
            default_segment_mode=SegmentTypeMode.LOOSE,
        )
        checker = TypeChecker(config)
        results = checker.check(module, inferencer=None)

        warnings = [r for r in results if r.severity == TypeErrorSeverity.WARNING]
        assert warnings == []

    def test_none_level_skips_checking(self):
        """NONE 级别下不产生任何结果"""
        body = [VarDecl('未注解变量', NumberLiteral(1), type_annotation=None)]
        seg = _make_segment('段落一', body)
        module = _make_module(seg)

        config = TypeCheckerConfig(check_level=TypeCheckLevel.NONE)
        checker = TypeChecker(config)
        results = checker.check(module, inferencer=None)
        assert results == []

    def test_signature_level_does_not_check_variables(self):
        """SIGNATURE 级别（低于 VARIABLE）不检查变量注解缺失"""
        body = [VarDecl('未注解变量', NumberLiteral(1), type_annotation=None)]
        seg = _make_segment('段落一', body)
        module = _make_module(seg)

        config = TypeCheckerConfig(
            check_level=TypeCheckLevel.SIGNATURE,
            default_segment_mode=SegmentTypeMode.LOOSE,
        )
        checker = TypeChecker(config)
        results = checker.check(module, inferencer=None)

        # SIGNATURE 级别不会触发变量级检查
        variable_warnings = [
            r for r in results
            if r.severity == TypeErrorSeverity.WARNING and '未注解变量' in r.message
        ]
        assert variable_warnings == []

    def test_mixed_annotated_and_unannotated(self):
        """混合场景：只对未注解变量产生警告"""
        body = [
            VarDecl('有注解', NumberLiteral(1), type_annotation='整数'),
            VarDecl('无注解', NumberLiteral(2), type_annotation=None),
        ]
        seg = _make_segment('段落一', body)
        module = _make_module(seg)

        config = TypeCheckerConfig(
            check_level=TypeCheckLevel.VARIABLE,
            default_segment_mode=SegmentTypeMode.LOOSE,
        )
        checker = TypeChecker(config)
        results = checker.check(module, inferencer=None)

        warnings = [r for r in results if r.severity == TypeErrorSeverity.WARNING]
        assert len(warnings) == 1
        assert '无注解' in warnings[0].message


# =============================================================================
# 9. type_system.py 既有类型类
# =============================================================================

class TestBasicTypes:
    """基本类型行为"""

    def test_singletons(self):
        """基本类型为单例"""
        assert NumberType() is NumberType()
        assert StringType() is StringType()
        assert BooleanType() is BooleanType()
        assert NullType() is NullType()
        assert AnyType() is AnyType()

    def test_type_id_constants(self):
        assert NumberType()._type_id == 1
        assert StringType()._type_id == 2
        assert BooleanType()._type_id == 3
        assert NullType()._type_id == 4
        assert AnyType()._type_id == 5

    def test_repr_uses_chinese_display_name(self):
        assert repr(NumberType()) == '数'
        assert repr(StringType()) == '串'
        assert repr(BooleanType()) == '布尔'
        assert repr(NullType()) == '空'
        assert repr(AnyType()) == '任意'


class TestIsSubtypeOf:
    """is_subtype_of 关系"""

    def test_same_type_is_subtype(self):
        assert NumberType().is_subtype_of(NumberType())
        assert StringType().is_subtype_of(StringType())

    def test_different_basic_not_subtype(self):
        assert not NumberType().is_subtype_of(StringType())
        assert not StringType().is_subtype_of(BooleanType())

    def test_any_is_supertype_of_all(self):
        """任意类型是所有类型的超类型"""
        assert NumberType().is_subtype_of(AnyType())
        assert StringType().is_subtype_of(AnyType())
        assert BooleanType().is_subtype_of(AnyType())
        assert NullType().is_subtype_of(AnyType())

    def test_any_is_subtype_of_any(self):
        assert AnyType().is_subtype_of(AnyType())

    def test_null_assignable_to_optional_and_any(self):
        """空值可赋给可空类型或任意类型"""
        assert NullType().is_subtype_of(AnyType())
        assert NullType().is_subtype_of(OptionalTypeWrapper(NumberType()))
        assert NullType().is_subtype_of(NullType())
        # 空值不能赋给非空的具体类型
        assert not NullType().is_subtype_of(NumberType())

    def test_unknown_compatible_with_all(self):
        """未知类型与所有类型兼容（渐进式推断）"""
        assert UnknownType().is_subtype_of(NumberType())
        assert UnknownType().is_subtype_of(AnyType())


class TestOptionalTypeWrapper:
    """OptionalTypeWrapper 行为"""

    def test_repr(self):
        opt = OptionalTypeWrapper(NumberType())
        assert repr(opt) == '数|空'

    def test_unwrap(self):
        inner = NumberType()
        opt = OptionalTypeWrapper(inner)
        assert opt.unwrap() is inner

    def test_optional_subtype_of_optional(self):
        assert OptionalTypeWrapper(NumberType()).is_subtype_of(
            OptionalTypeWrapper(NumberType())
        )

    def test_optional_not_subtype_of_concrete(self):
        """可空类型不是具体类型的子类型"""
        assert not OptionalTypeWrapper(NumberType()).is_subtype_of(NumberType())

    def test_optional_subtype_of_any(self):
        assert OptionalTypeWrapper(NumberType()).is_subtype_of(AnyType())


class TestListType:
    """ListType 行为"""

    def test_repr_with_element(self):
        assert repr(ListType(NumberType())) == '列表[数]'

    def test_repr_without_element(self):
        assert repr(ListType()) == '列表'

    def test_list_subtype_covariant(self):
        """列表元素协变：List[数] <: List[数]"""
        assert ListType(NumberType()).is_subtype_of(ListType(NumberType()))

    def test_list_with_unknown_element_compatible(self):
        assert ListType(NumberType()).is_subtype_of(ListType(None))

    def test_list_not_subtype_of_dict(self):
        assert not ListType(NumberType()).is_subtype_of(DictType())


class TestDictType:
    """DictType 行为"""

    def test_repr_with_kv(self):
        d = DictType(StringType(), NumberType())
        assert repr(d) == '字典[串: 数]'

    def test_repr_without_kv(self):
        assert repr(DictType()) == '字典'

    def test_dict_subtype_same_kv(self):
        d1 = DictType(StringType(), NumberType())
        d2 = DictType(StringType(), NumberType())
        assert d1.is_subtype_of(d2)

    def test_dict_not_subtype_of_list(self):
        assert not DictType(StringType(), NumberType()).is_subtype_of(ListType())


class TestFunctionType:
    """FunctionType 行为"""

    def test_repr(self):
        ft = FunctionType([NumberType(), StringType()], BooleanType())
        assert repr(ft) == '(数, 串) -> 布尔'

    def test_function_subtype_same_signature(self):
        f1 = FunctionType([NumberType()], BooleanType())
        f2 = FunctionType([NumberType()], BooleanType())
        assert f1.is_subtype_of(f2)

    def test_function_arity_mismatch_not_subtype(self):
        f1 = FunctionType([NumberType()], BooleanType())
        f2 = FunctionType([NumberType(), StringType()], BooleanType())
        assert not f1.is_subtype_of(f2)


class TestUnification:
    """类型合一（unify）"""

    def test_unify_same_basic(self):
        subs = unify(NumberType(), NumberType())
        assert isinstance(subs, TypeSubstitution)

    def test_unify_with_any_succeeds(self):
        subs = unify(NumberType(), AnyType())
        assert isinstance(subs, TypeSubstitution)

    def test_unify_type_var_binds(self):
        tv = TypeVar('T')
        subs = unify(tv, NumberType())
        assert subs['T'] == NumberType() or subs['T'] is NumberType()

    def test_unify_incompatible_raises(self):
        with pytest.raises(UnificationError):
            unify(NumberType(), StringType())

    def test_unify_lists(self):
        subs = unify(ListType(NumberType()), ListType(NumberType()))
        assert isinstance(subs, TypeSubstitution)

    def test_unify_functions(self):
        f1 = FunctionType([NumberType()], BooleanType())
        f2 = FunctionType([NumberType()], BooleanType())
        subs = unify(f1, f2)
        assert isinstance(subs, TypeSubstitution)

    def test_unification_error_message(self):
        try:
            unify(NumberType(), StringType())
        except UnificationError as e:
            assert '类型合一失败' in str(e)


class TestTypeParser:
    """TypeParser 字符串 → Type 解析"""

    def setup_method(self):
        self.parser = TypeParser()

    def test_parse_basic_number(self):
        t = self.parser.parse('数')
        assert t._type_id == TYPE_NUMBER._type_id

    def test_parse_alias_integers(self):
        """整数是 数 的别名"""
        t = self.parser.parse('整数')
        assert t._type_id == TYPE_NUMBER._type_id

    def test_parse_alias_text(self):
        """文本是 串 的别名"""
        t = self.parser.parse('文本')
        assert t._type_id == TYPE_STRING._type_id

    def test_parse_boolean(self):
        t = self.parser.parse('布尔')
        assert t._type_id == TYPE_BOOLEAN._type_id

    def test_parse_null(self):
        t = self.parser.parse('空')
        assert t._type_id == TYPE_NULL._type_id

    def test_parse_any(self):
        t = self.parser.parse('任意')
        assert t._type_id == TYPE_ANY._type_id

    def test_parse_list(self):
        t = self.parser.parse('列表[数]')
        assert t._type_id == 8  # TYPE_ID_LIST
        assert t.element_type._type_id == TYPE_NUMBER._type_id

    def test_parse_dict(self):
        t = self.parser.parse('字典[串: 数]')
        assert t._type_id == 9  # TYPE_ID_DICT
        assert t.key_type._type_id == TYPE_STRING._type_id
        assert t.value_type._type_id == TYPE_NUMBER._type_id

    def test_parse_optional(self):
        t = self.parser.parse('数|空')
        assert t._type_id == 7  # TYPE_ID_OPTIONAL

    def test_parse_function_with_parens_is_single_tuple_param(self):
        """带括号的 (数, 串) -> 布尔：括号触发元组规则，等价于单参数（元组）函数

        这是 TypeParser 既有行为：params_part 仍带括号时，
        _split_top_level 不会在括号内切分，整体被解析为 TupleType。
        """
        t = self.parser.parse('(数, 串) -> 布尔')
        assert t._type_id == 12  # TYPE_ID_FUNCTION
        assert len(t.param_types) == 1
        assert t.param_types[0]._type_id == 10  # TYPE_ID_TUPLE
        assert t.return_type._type_id == TYPE_BOOLEAN._type_id

    def test_parse_function_multiple_params(self):
        """数, 串 -> 布尔：无括号时按逗号切分得到多参数函数"""
        t = self.parser.parse('数, 串 -> 布尔')
        assert t._type_id == 12  # TYPE_ID_FUNCTION
        assert len(t.param_types) == 2
        assert t.param_types[0]._type_id == TYPE_NUMBER._type_id
        assert t.param_types[1]._type_id == TYPE_STRING._type_id
        assert t.return_type._type_id == TYPE_BOOLEAN._type_id

    def test_parse_type_sugar_list(self):
        """中文语法糖：整数列表 → ListType(数)"""
        t = self.parser.parse('整数列表')
        assert t._type_id == 8
        assert t.element_type._type_id == TYPE_NUMBER._type_id

    def test_parse_type_sugar_dict(self):
        """中文语法糖：文本到整数字典 → DictType(串, 数)"""
        t = self.parser.parse('文本到整数字典')
        assert t._type_id == 9
        assert t.key_type._type_id == TYPE_STRING._type_id
        assert t.value_type._type_id == TYPE_NUMBER._type_id

    def test_parse_unknown_class_fallback(self):
        """未识别名称回退为 ClassType"""
        t = self.parser.parse('某自定义类')
        assert t._type_id == 16  # TYPE_ID_CLASS


class TestTypeSymbolTable:
    """类型符号表作用域与泛型参数"""

    def test_define_and_lookup(self):
        st = TypeSymbolTable()
        assert st.define('x', 'variable', NumberType()) is True
        sym = st.lookup('x')
        assert sym is not None
        assert sym.name == 'x'

    def test_define_duplicate_in_same_scope_fails(self):
        st = TypeSymbolTable()
        assert st.define('x', 'variable', NumberType()) is True
        assert st.define('x', 'variable', StringType()) is False

    def test_scope_nesting(self):
        st = TypeSymbolTable()
        st.define('外层', 'variable', NumberType())
        st.enter_scope()
        st.define('内层', 'variable', StringType())
        # 内层可看到外层
        assert st.lookup('外层') is not None
        assert st.lookup('内层') is not None
        st.exit_scope()
        # 退出后看不到内层
        assert st.lookup('内层') is None
        assert st.lookup('外层') is not None

    def test_generic_param(self):
        st = TypeSymbolTable()
        st.define_generic_param('T')
        resolved = st.resolve_type_param('T')
        assert resolved is not None
        assert resolved._type_id == 13  # TYPE_ID_TVAR


class TestTypeErrorInference:
    """类型推断异常"""

    def test_error_carries_message(self):
        err = TypeErrorInference('类型不匹配')
        assert '类型不匹配' in str(err)

    def test_error_with_line(self):
        err = TypeErrorInference('错误', line=42)
        assert '42' in str(err)
