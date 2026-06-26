"""段言解释器 - 内置函数混入模块"""

from typing import List

from interpreter_core import InterpreterCore, DuanValue, DuanBuiltinFunction


class BuiltinsMixin:
    """内置函数混入类"""

    def _register_builtins(self):
        """注册内置函数"""
        builtins = [
            # I/O操作
            DuanBuiltinFunction('打印', self._builtin_print, min_args=1),
            DuanBuiltinFunction('输出', self._builtin_print, min_args=1),
            # 典操作
            DuanBuiltinFunction('_典', self._builtin_dict, min_args=0),
            # 类型转换
            DuanBuiltinFunction('转字符串', self._builtin_to_string, min_args=1, max_args=1),
            DuanBuiltinFunction('_串化', self._builtin_to_string, min_args=1, max_args=1),
            DuanBuiltinFunction('_数化', self._builtin_to_number, min_args=1, max_args=1),
            DuanBuiltinFunction('_布尔化', self._builtin_to_bool, min_args=1, max_args=1),
            # 字符分类
            DuanBuiltinFunction('_是中文', self._builtin_is_cjk, min_args=1, max_args=1),
            DuanBuiltinFunction('_是字母', self._builtin_is_letter, min_args=1, max_args=1),
            DuanBuiltinFunction('_是数字', self._builtin_is_digit, min_args=1, max_args=1),
            # 文件IO
            DuanBuiltinFunction('_读文件', self._builtin_read_file, min_args=1, max_args=1),
            DuanBuiltinFunction('_写文件', self._builtin_write_file, min_args=2, max_args=2),
            DuanBuiltinFunction('_文件存在', self._builtin_file_exists, min_args=1, max_args=1),
            # 数学函数
            DuanBuiltinFunction('abs', self._builtin_abs, min_args=1, max_args=1),
            DuanBuiltinFunction('max', self._builtin_max, min_args=2),
            DuanBuiltinFunction('min', self._builtin_min, min_args=2),
            DuanBuiltinFunction('sqrt', self._builtin_sqrt, min_args=1, max_args=1),
            DuanBuiltinFunction('pow', self._builtin_pow, min_args=2, max_args=2),
            DuanBuiltinFunction('round', self._builtin_round, min_args=1, max_args=1),
            DuanBuiltinFunction('sin', self._builtin_sin, min_args=1, max_args=1),
            DuanBuiltinFunction('cos', self._builtin_cos, min_args=1, max_args=1),
            DuanBuiltinFunction('tan', self._builtin_tan, min_args=1, max_args=1),
            DuanBuiltinFunction('log', self._builtin_log, min_args=1, max_args=1),
            DuanBuiltinFunction('exp', self._builtin_exp, min_args=1, max_args=1),
            DuanBuiltinFunction('floor', self._builtin_floor, min_args=1, max_args=1),
            DuanBuiltinFunction('ceil', self._builtin_ceil, min_args=1, max_args=1),
            # 字符串函数
            DuanBuiltinFunction('len', self._builtin_len, min_args=1, max_args=1),
            DuanBuiltinFunction('trim', self._builtin_trim, min_args=1, max_args=1),
            DuanBuiltinFunction('substring', self._builtin_substring, min_args=3, max_args=3),
            DuanBuiltinFunction('lower', self._builtin_lower, min_args=1, max_args=1),
            DuanBuiltinFunction('upper', self._builtin_upper, min_args=1, max_args=1),
            DuanBuiltinFunction('replace', self._builtin_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('split', self._builtin_split, min_args=2, max_args=2),
            DuanBuiltinFunction('join', self._builtin_join, min_args=2, max_args=2),
            DuanBuiltinFunction('indexOf', self._builtin_index_of, min_args=2, max_args=2),
            DuanBuiltinFunction('contains', self._builtin_contains, min_args=2, max_args=2),
            # 列表函数
            DuanBuiltinFunction('列表长度', self._builtin_list_len, min_args=1, max_args=1),
            DuanBuiltinFunction('listLen', self._builtin_list_len, min_args=1, max_args=1),
            DuanBuiltinFunction('listAppend', self._builtin_list_append, min_args=2, max_args=2),
            DuanBuiltinFunction('listReverse', self._builtin_list_reverse, min_args=1, max_args=1),
            DuanBuiltinFunction('listIndexOf', self._builtin_list_index_of, min_args=2, max_args=2),
            DuanBuiltinFunction('listContains', self._builtin_list_contains, min_args=2, max_args=2),
            DuanBuiltinFunction('listSlice', self._builtin_list_slice, min_args=3, max_args=3),
            DuanBuiltinFunction('listConcat', self._builtin_list_concat, min_args=2, max_args=2),
            DuanBuiltinFunction('listSort', self._builtin_list_sort, min_args=1, max_args=1),
            DuanBuiltinFunction('listInsert', self._builtin_list_insert, min_args=3, max_args=3),
            DuanBuiltinFunction('listRemove', self._builtin_list_remove, min_args=2, max_args=2),
            DuanBuiltinFunction('listPop', self._builtin_list_pop, min_args=1, max_args=2),
            # 时间函数
            DuanBuiltinFunction('now', self._builtin_now, min_args=0, max_args=0),
            DuanBuiltinFunction('sleep', self._builtin_sleep, min_args=1, max_args=1),
            # 其他实用函数
            DuanBuiltinFunction('range', self._builtin_range, min_args=1, max_args=3),
            DuanBuiltinFunction('type', self._builtin_type, min_args=1, max_args=1),
            DuanBuiltinFunction('id', self._builtin_id, min_args=1, max_args=1),
            # 调试函数
            DuanBuiltinFunction('printDebug', self._builtin_print_debug, min_args=2, max_args=2),
            DuanBuiltinFunction('assert', self._builtin_assert, min_args=2, max_args=2),
            # 新数学函数
            DuanBuiltinFunction('随机整数', self._builtin_random_int, min_args=2, max_args=2),
            DuanBuiltinFunction('randomInt', self._builtin_random_int, min_args=2, max_args=2),
            DuanBuiltinFunction('随机浮点', self._builtin_random_float, min_args=0, max_args=0),
            DuanBuiltinFunction('randomFloat', self._builtin_random_float, min_args=0, max_args=0),
            DuanBuiltinFunction('阶乘', self._builtin_factorial, min_args=1, max_args=1),
            DuanBuiltinFunction('factorial', self._builtin_factorial, min_args=1, max_args=1),
            DuanBuiltinFunction('平均数', self._builtin_mean, min_args=1, max_args=1),
            DuanBuiltinFunction('mean', self._builtin_mean, min_args=1, max_args=1),
            DuanBuiltinFunction('中位数', self._builtin_median, min_args=1, max_args=1),
            DuanBuiltinFunction('median', self._builtin_median, min_args=1, max_args=1),
            DuanBuiltinFunction('求和', self._builtin_sum, min_args=1, max_args=1),
            DuanBuiltinFunction('sum', self._builtin_sum, min_args=1, max_args=1),
            DuanBuiltinFunction('圆周率', self._builtin_pi, min_args=0, max_args=0),
            DuanBuiltinFunction('pi', self._builtin_pi, min_args=0, max_args=0),
            DuanBuiltinFunction('自然常数', self._builtin_e, min_args=0, max_args=0),
            DuanBuiltinFunction('e', self._builtin_e, min_args=0, max_args=0),
            # JSON 函数
            DuanBuiltinFunction('解析JSON', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('解析字典', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('parseJSON', self._builtin_parse_json, min_args=1, max_args=1),
            DuanBuiltinFunction('序列化JSON', self._builtin_stringify_json, min_args=1, max_args=2),
            DuanBuiltinFunction('序列化字典', self._builtin_stringify_json, min_args=1, max_args=2),
            DuanBuiltinFunction('stringifyJSON', self._builtin_stringify_json, min_args=1, max_args=2),
            # 日期时间函数
            DuanBuiltinFunction('当前时间', self._builtin_current_time, min_args=0, max_args=1),
            DuanBuiltinFunction('formatTime', self._builtin_current_time, min_args=0, max_args=1),
            DuanBuiltinFunction('当前日期', self._builtin_current_date, min_args=0, max_args=1),
            DuanBuiltinFunction('formatDate', self._builtin_current_date, min_args=0, max_args=1),
            DuanBuiltinFunction('时间戳', self._builtin_timestamp, min_args=0, max_args=0),
            DuanBuiltinFunction('timestamp', self._builtin_timestamp, min_args=0, max_args=0),
            DuanBuiltinFunction('格式化时间', self._builtin_format_time, min_args=2, max_args=2),
            DuanBuiltinFunction('formatTime', self._builtin_format_time, min_args=2, max_args=2),
            DuanBuiltinFunction('日期差', self._builtin_date_diff, min_args=2, max_args=2),
            DuanBuiltinFunction('dateDiff', self._builtin_date_diff, min_args=2, max_args=2),
            # 哈希函数
            DuanBuiltinFunction('MD5', self._builtin_md5, min_args=1, max_args=1),
            DuanBuiltinFunction('md5', self._builtin_md5, min_args=1, max_args=1),
            DuanBuiltinFunction('SHA256', self._builtin_sha256, min_args=1, max_args=1),
            DuanBuiltinFunction('sha256', self._builtin_sha256, min_args=1, max_args=1),
            DuanBuiltinFunction('Base64编码', self._builtin_base64_encode, min_args=1, max_args=1),
            DuanBuiltinFunction('base64Encode', self._builtin_base64_encode, min_args=1, max_args=1),
            DuanBuiltinFunction('Base64解码', self._builtin_base64_decode, min_args=1, max_args=1),
            DuanBuiltinFunction('base64Decode', self._builtin_base64_decode, min_args=1, max_args=1),
            # 正则表达式函数
            DuanBuiltinFunction('匹配', self._builtin_regex_match, min_args=2, max_args=2),
            DuanBuiltinFunction('regexMatch', self._builtin_regex_match, min_args=2, max_args=2),
            DuanBuiltinFunction('搜索', self._builtin_regex_search, min_args=2, max_args=2),
            DuanBuiltinFunction('regexSearch', self._builtin_regex_search, min_args=2, max_args=2),
            DuanBuiltinFunction('查找所有', self._builtin_regex_find_all, min_args=2, max_args=2),
            DuanBuiltinFunction('regexFindAll', self._builtin_regex_find_all, min_args=2, max_args=2),
            DuanBuiltinFunction('替换', self._builtin_regex_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('regexReplace', self._builtin_regex_replace, min_args=3, max_args=3),
            DuanBuiltinFunction('分割', self._builtin_regex_split, min_args=2, max_args=2),
            DuanBuiltinFunction('regexSplit', self._builtin_regex_split, min_args=2, max_args=2),
        ]
        for b in builtins:
            self.global_env.define(b.name, DuanValue(b, '内置段'))
    
    # ----- 内置函数实现 -----

    def _builtin_print(self, args: List[DuanValue]) -> DuanValue:
        """打印输出"""
        text = ' '.join(str(a) for a in args)
        self.output_lines.append(text)
        print(text)
        return DuanValue(None, '空')

    def _builtin_dict(self, args: List[DuanValue]) -> DuanValue:
        """创建典：_典(键1, 值1, 键2, 值2, ...)"""
        result = {}
        for i in range(0, len(args), 2):
            if i + 1 >= len(args):
                raise RuntimeError("_典 需要偶数个参数（键值对）")
            key = args[i]
            if key.type_name not in ('串', '数', '布尔'):
                raise RuntimeError(f"典键不支持类型: '{key.type_name}'")
            result[key.value] = args[i + 1]
        return DuanValue(result, '典')
    
    def _builtin_to_string(self, args: List[DuanValue]) -> DuanValue:
        """转换为字符串"""
        return DuanValue(str(args[0]), '串')
    
    def _builtin_to_number(self, args: List[DuanValue]) -> DuanValue:
        """转换为数字"""
        try:
            val = args[0].value
            if isinstance(val, str):
                if '.' in val:
                    return DuanValue(float(val), '数')
                return DuanValue(int(val), '数')
            if isinstance(val, bool):
                return DuanValue(1 if val else 0, '数')
            if isinstance(val, (int, float)):
                return DuanValue(val, '数')
            raise ValueError()
        except (ValueError, TypeError):
            raise RuntimeError(f"无法转换为数字: '{args[0].value}'")
    
    def _builtin_is_cjk(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为中文字符"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        cp = ord(s)
        return DuanValue(
            0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0xF900 <= cp <= 0xFAFF,
            '布尔'
        )
    
    def _builtin_is_letter(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为英文字母"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        return DuanValue(('a' <= s <= 'z') or ('A' <= s <= 'Z') or s == '_', '布尔')
    
    def _builtin_is_digit(self, args: List[DuanValue]) -> DuanValue:
        """判断是否为数字字符"""
        s = str(args[0])
        if len(s) != 1:
            return DuanValue(False, '布尔')
        return DuanValue('0' <= s <= '9', '布尔')
    
    def _builtin_read_file(self, args: List[DuanValue]) -> DuanValue:
        """读取文件内容"""
        path = str(args[0])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return DuanValue(content, '串')
        except Exception as e:
            raise RuntimeError(f"读取文件失败: {e}")
    
    def _builtin_write_file(self, args: List[DuanValue]) -> DuanValue:
        """写入文件内容"""
        path = str(args[0])
        content = str(args[1])
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return DuanValue(None, '空')
        except Exception as e:
            raise RuntimeError(f"写入文件失败: {e}")
    
    def _builtin_file_exists(self, args: List[DuanValue]) -> DuanValue:
        """检查文件是否存在"""
        path = str(args[0])
        import os
        return DuanValue(os.path.exists(path), '布尔')
    
    def _builtin_to_bool(self, args: List[DuanValue]) -> DuanValue:
        """转换为布尔值"""
        val = args[0].value
        if val is None:
            return DuanValue(False, '布尔')
        if isinstance(val, bool):
            return DuanValue(val, '布尔')
        if isinstance(val, (int, float)):
            return DuanValue(val != 0, '布尔')
        if isinstance(val, str):
            return DuanValue(len(val) > 0, '布尔')
        if isinstance(val, (list, dict)):
            return DuanValue(len(val) > 0, '布尔')
        return DuanValue(bool(val), '布尔')
    
    # ----- 数学函数 -----
    
    def _builtin_abs(self, args: List[DuanValue]) -> DuanValue:
        """绝对值"""
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(abs(val), '数')
        raise RuntimeError("abs 需要数字参数")
    
    def _builtin_max(self, args: List[DuanValue]) -> DuanValue:
        """最大值"""
        max_val = None
        for arg in args:
            val = arg.value
            if not isinstance(val, (int, float)):
                raise RuntimeError("max 需要数字参数")
            if max_val is None or val > max_val:
                max_val = val
        return DuanValue(max_val, '数')
    
    def _builtin_min(self, args: List[DuanValue]) -> DuanValue:
        """最小值"""
        min_val = None
        for arg in args:
            val = arg.value
            if not isinstance(val, (int, float)):
                raise RuntimeError("min 需要数字参数")
            if min_val is None or val < min_val:
                min_val = val
        return DuanValue(min_val, '数')
    
    def _builtin_sqrt(self, args: List[DuanValue]) -> DuanValue:
        """平方根"""
        val = args[0].value
        if isinstance(val, (int, float)):
            if val < 0:
                raise RuntimeError("sqrt 参数不能为负数")
            return DuanValue(val ** 0.5, '数')
        raise RuntimeError("sqrt 需要数字参数")
    
    def _builtin_pow(self, args: List[DuanValue]) -> DuanValue:
        """幂运算"""
        base = args[0].value
        exp = args[1].value
        if isinstance(base, (int, float)) and isinstance(exp, (int, float)):
            return DuanValue(base ** exp, '数')
        raise RuntimeError("pow 需要数字参数")
    
    def _builtin_round(self, args: List[DuanValue]) -> DuanValue:
        """四舍五入"""
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(round(val), '数')
        raise RuntimeError("round 需要数字参数")
    
    def _builtin_sin(self, args: List[DuanValue]) -> DuanValue:
        """正弦函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.sin(val), '数')
        raise RuntimeError("sin 需要数字参数")
    
    def _builtin_cos(self, args: List[DuanValue]) -> DuanValue:
        """余弦函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.cos(val), '数')
        raise RuntimeError("cos 需要数字参数")
    
    def _builtin_tan(self, args: List[DuanValue]) -> DuanValue:
        """正切函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.tan(val), '数')
        raise RuntimeError("tan 需要数字参数")
    
    def _builtin_log(self, args: List[DuanValue]) -> DuanValue:
        """自然对数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            if val <= 0:
                raise RuntimeError("log 参数必须大于0")
            return DuanValue(math.log(val), '数')
        raise RuntimeError("log 需要数字参数")
    
    def _builtin_exp(self, args: List[DuanValue]) -> DuanValue:
        """指数函数"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.exp(val), '数')
        raise RuntimeError("exp 需要数字参数")
    
    def _builtin_floor(self, args: List[DuanValue]) -> DuanValue:
        """向下取整"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.floor(val), '数')
        raise RuntimeError("floor 需要数字参数")
    
    def _builtin_ceil(self, args: List[DuanValue]) -> DuanValue:
        """向上取整"""
        import math
        val = args[0].value
        if isinstance(val, (int, float)):
            return DuanValue(math.ceil(val), '数')
        raise RuntimeError("ceil 需要数字参数")
    
    # ----- 字符串函数 -----
    
    def _builtin_len(self, args: List[DuanValue]) -> DuanValue:
        """长度"""
        val = args[0].value
        if isinstance(val, str):
            return DuanValue(len(val), '数')
        if isinstance(val, list):
            return DuanValue(len(val), '数')
        raise RuntimeError("len 需要字符串或列表参数")
    
    def _builtin_trim(self, args: List[DuanValue]) -> DuanValue:
        """去除首尾空白"""
        val = args[0].value
        if isinstance(val, str):
            return DuanValue(val.strip(), '串')
        raise RuntimeError("trim 需要字符串参数")
    
    def _builtin_substring(self, args: List[DuanValue]) -> DuanValue:
        """子串"""
        s = args[0].value
        start = args[1].value
        end = args[2].value
        if isinstance(s, str) and isinstance(start, int) and isinstance(end, int):
            return DuanValue(s[start:end], '串')
        raise RuntimeError("substring 参数类型错误")
    
    def _builtin_lower(self, args: List[DuanValue]) -> DuanValue:
        """转换为小写"""
        s = args[0].value
        if isinstance(s, str):
            return DuanValue(s.lower(), '串')
        raise RuntimeError("lower 需要字符串参数")
    
    def _builtin_upper(self, args: List[DuanValue]) -> DuanValue:
        """转换为大写"""
        s = args[0].value
        if isinstance(s, str):
            return DuanValue(s.upper(), '串')
        raise RuntimeError("upper 需要字符串参数")
    
    def _builtin_replace(self, args: List[DuanValue]) -> DuanValue:
        """字符串替换"""
        s = args[0].value
        old = args[1].value
        new = args[2].value
        if isinstance(s, str) and isinstance(old, str) and isinstance(new, str):
            return DuanValue(s.replace(old, new), '串')
        raise RuntimeError("replace 参数类型错误")
    
    def _builtin_split(self, args: List[DuanValue]) -> DuanValue:
        """字符串分割"""
        s = args[0].value
        sep = args[1].value
        if isinstance(s, str) and isinstance(sep, str):
            return DuanValue(s.split(sep), '列')
        raise RuntimeError("split 参数类型错误")
    
    def _builtin_join(self, args: List[DuanValue]) -> DuanValue:
        """列表拼接为字符串"""
        lst = args[0].value
        sep = args[1].value
        if isinstance(lst, list) and isinstance(sep, str):
            str_list = []
            for item in lst:
                if isinstance(item, DuanValue):
                    str_list.append(str(item.value))
                else:
                    str_list.append(str(item))
            return DuanValue(sep.join(str_list), '串')
        raise RuntimeError("join 参数类型错误")
    
    def _builtin_index_of(self, args: List[DuanValue]) -> DuanValue:
        """字符串索引查找"""
        s = args[0].value
        substr = args[1].value
        if isinstance(s, str) and isinstance(substr, str):
            return DuanValue(s.find(substr), '数')
        raise RuntimeError("indexOf 参数类型错误")
    
    def _builtin_contains(self, args: List[DuanValue]) -> DuanValue:
        """字符串包含检查"""
        s = args[0].value
        substr = args[1].value
        if isinstance(s, str) and isinstance(substr, str):
            return DuanValue(substr in s, '布尔')
        raise RuntimeError("contains 参数类型错误")
    
    # ----- 列表函数 -----
    
    def _builtin_list_len(self, args: List[DuanValue]) -> DuanValue:
        """列表长度"""
        val = args[0].value
        if isinstance(val, list):
            return DuanValue(len(val), '数')
        raise RuntimeError("listLen 需要列表参数")
    
    def _builtin_list_append(self, args: List[DuanValue]) -> DuanValue:
        """列表追加"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            lst.append(item)
            return DuanValue(None, '空')
        raise RuntimeError("listAppend 需要列表参数")
    
    def _builtin_list_reverse(self, args: List[DuanValue]) -> DuanValue:
        """列表反转"""
        lst = args[0].value
        if isinstance(lst, list):
            lst.reverse()
            return DuanValue(None, '空')
        raise RuntimeError("listReverse 需要列表参数")
    
    def _builtin_list_index_of(self, args: List[DuanValue]) -> DuanValue:
        """列表索引查找"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            for i, val in enumerate(lst):
                # 比较值而非对象引用
                val_val = val.value if isinstance(val, DuanValue) else val
                item_val = item.value if isinstance(item, DuanValue) else item
                if val_val == item_val:
                    return DuanValue(i, '数')
            return DuanValue(-1, '数')
        raise RuntimeError("listIndexOf 需要列表参数")
    
    def _builtin_list_contains(self, args: List[DuanValue]) -> DuanValue:
        """列表包含检查"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            item_val = item.value if isinstance(item, DuanValue) else item
            for val in lst:
                val_val = val.value if isinstance(val, DuanValue) else val
                if val_val == item_val:
                    return DuanValue(True, '布尔')
            return DuanValue(False, '布尔')
        raise RuntimeError("listContains 需要列表参数")
    
    def _builtin_list_slice(self, args: List[DuanValue]) -> DuanValue:
        """列表切片"""
        lst = args[0].value
        start = args[1].value
        end = args[2].value
        if isinstance(lst, list) and isinstance(start, int) and isinstance(end, int):
            return DuanValue(lst[start:end], '列')
        raise RuntimeError("listSlice 参数类型错误")
    
    def _builtin_list_concat(self, args: List[DuanValue]) -> DuanValue:
        """列表拼接"""
        lst1 = args[0].value
        lst2 = args[1].value
        if isinstance(lst1, list) and isinstance(lst2, list):
            return DuanValue(lst1 + lst2, '列')
        raise RuntimeError("listConcat 需要两个列表参数")
    
    def _builtin_list_sort(self, args: List[DuanValue]) -> DuanValue:
        """列表排序"""
        lst = args[0].value
        if isinstance(lst, list):
            lst.sort(key=lambda x: x.value if isinstance(x, DuanValue) else x)
            return DuanValue(None, '空')
        raise RuntimeError("listSort 需要列表参数")
    
    def _builtin_list_insert(self, args: List[DuanValue]) -> DuanValue:
        """列表插入"""
        lst = args[0].value
        index = args[1].value
        item = args[2]
        if isinstance(lst, list) and isinstance(index, int):
            lst.insert(index, item)
            return DuanValue(None, '空')
        raise RuntimeError("listInsert 参数类型错误")
    
    def _builtin_list_remove(self, args: List[DuanValue]) -> DuanValue:
        """列表移除元素"""
        lst = args[0].value
        item = args[1]
        if isinstance(lst, list):
            item_val = item.value if isinstance(item, DuanValue) else item
            for i, val in enumerate(lst):
                val_val = val.value if isinstance(val, DuanValue) else val
                if val_val == item_val:
                    del lst[i]
                    return DuanValue(None, '空')
            raise RuntimeError("元素不在列表中")
        raise RuntimeError("listRemove 需要列表参数")
    
    def _builtin_list_pop(self, args: List[DuanValue]) -> DuanValue:
        """列表弹出元素"""
        lst = args[0].value
        if isinstance(lst, list):
            if len(args) > 1:
                index = args[1].value
                if isinstance(index, int):
                    return lst.pop(index)
                raise RuntimeError("pop 索引必须是整数")
            return lst.pop()
        raise RuntimeError("listPop 需要列表参数")
    
    # ----- 时间函数 -----
    
    def _builtin_now(self, args: List[DuanValue]) -> DuanValue:
        """获取当前时间戳"""
        import time
        return DuanValue(time.time(), '数')
    
    def _builtin_sleep(self, args: List[DuanValue]) -> DuanValue:
        """暂停执行"""
        import time
        val = args[0].value
        if isinstance(val, (int, float)):
            time.sleep(val)
            return DuanValue(None, '空')
        raise RuntimeError("sleep 需要数字参数")
    
    # ----- 其他函数 -----
    
    def _builtin_range(self, args: List[DuanValue]) -> DuanValue:
        """生成范围列表"""
        if len(args) == 1:
            end = args[0].value
            if isinstance(end, int):
                return DuanValue(list(range(end)), '列')
        elif len(args) == 2:
            start = args[0].value
            end = args[1].value
            if isinstance(start, int) and isinstance(end, int):
                return DuanValue(list(range(start, end)), '列')
        elif len(args) == 3:
            start = args[0].value
            end = args[1].value
            step = args[2].value
            if isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
                return DuanValue(list(range(start, end, step)), '列')
        raise RuntimeError("range 参数类型错误")
    
    def _builtin_type(self, args: List[DuanValue]) -> DuanValue:
        """获取类型名称"""
        val = args[0]
        return DuanValue(val.type_name, '串')
    
    def _builtin_id(self, args: List[DuanValue]) -> DuanValue:
        """获取对象ID"""
        val = args[0].value
        return DuanValue(id(val), '数')
    
    # ----- 调试函数 -----
    
    def _builtin_print_debug(self, args: List[DuanValue]) -> DuanValue:
        """调试打印"""
        msg = str(args[0].value)
        val = str(args[1].value)
        self.output_lines.append(f"DEBUG: {msg} = {val}")
        print(f"DEBUG: {msg} = {val}")
        return DuanValue(None, '空')
    
    def _builtin_assert(self, args: List[DuanValue]) -> DuanValue:
        """断言"""
        condition = args[0].value
        msg = str(args[1].value)
        if not condition:
            self.output_lines.append(f"断言失败: {msg}")
            print(f"断言失败: {msg}")
            raise RuntimeError(f"断言失败: {msg}")
        return DuanValue(None, '空')
    
    # ----- 新数学函数 -----
    
    def _builtin_random_int(self, args: List[DuanValue]) -> DuanValue:
        """随机整数"""
        import random
        lo = int(args[0].value)
        hi = int(args[1].value)
        return DuanValue(random.randint(lo, hi), '数')
    
    def _builtin_random_float(self, args: List[DuanValue]) -> DuanValue:
        """随机浮点 [0,1)"""
        import random
        return DuanValue(random.random(), '数')
    
    def _builtin_factorial(self, args: List[DuanValue]) -> DuanValue:
        """阶乘"""
        n = int(args[0].value)
        if n < 0:
            raise RuntimeError("阶乘参数不能为负数")
        import math
        return DuanValue(math.factorial(n), '数')
    
    def _builtin_mean(self, args: List[DuanValue]) -> DuanValue:
        """平均数"""
        data = args[0].value
        if not isinstance(data, list) or len(data) == 0:
            raise RuntimeError("数据列表为空")
        import statistics
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(statistics.mean(values), '数')
    
    def _builtin_median(self, args: List[DuanValue]) -> DuanValue:
        """中位数"""
        data = args[0].value
        if not isinstance(data, list) or len(data) == 0:
            raise RuntimeError("数据列表为空")
        import statistics
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(statistics.median(values), '数')
    
    def _builtin_sum(self, args: List[DuanValue]) -> DuanValue:
        """求和"""
        data = args[0].value
        if not isinstance(data, list):
            raise RuntimeError("参数必须是列表")
        values = [x.value if isinstance(x, DuanValue) else x for x in data]
        return DuanValue(sum(values), '数')
    
    def _builtin_pi(self, args: List[DuanValue]) -> DuanValue:
        """圆周率"""
        import math
        return DuanValue(math.pi, '数')
    
    def _builtin_e(self, args: List[DuanValue]) -> DuanValue:
        """自然常数"""
        import math
        return DuanValue(math.e, '数')
    
    # ----- JSON 函数 -----
    
    def _builtin_parse_json(self, args: List[DuanValue]) -> DuanValue:
        """解析JSON字符串"""
        import json
        text = str(args[0].value)
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return DuanValue(result, '典')
            elif isinstance(result, list):
                return DuanValue(result, '列')
            elif isinstance(result, str):
                return DuanValue(result, '串')
            elif isinstance(result, bool):
                return DuanValue(result, '布尔')
            elif isinstance(result, (int, float)):
                return DuanValue(result, '数')
            elif result is None:
                return DuanValue(None, '空')
            return DuanValue(result)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON解析失败: {e}")
    
    def _builtin_stringify_json(self, args: List[DuanValue]) -> DuanValue:
        """序列化为JSON字符串"""
        import json
        val = args[0].value
        indent = None
        if len(args) >= 2 and args[1].value is not None:
            indent = int(args[1].value)
        try:
            result = json.dumps(val, ensure_ascii=False, indent=indent)
            return DuanValue(result, '串')
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"JSON序列化失败: {e}")
    
    # ----- 日期时间函数 -----
    
    def _builtin_current_time(self, args: List[DuanValue]) -> DuanValue:
        """当前时间字符串"""
        from datetime import datetime
        fmt = '%Y-%m-%d %H:%M:%S'
        if args:
            fmt = str(args[0].value)
        return DuanValue(datetime.now().strftime(fmt), '串')
    
    def _builtin_current_date(self, args: List[DuanValue]) -> DuanValue:
        """当前日期字符串"""
        from datetime import date
        fmt = '%Y-%m-%d'
        if args:
            fmt = str(args[0].value)
        return DuanValue(date.today().strftime(fmt), '串')
    
    def _builtin_timestamp(self, args: List[DuanValue]) -> DuanValue:
        """当前时间戳"""
        import time
        return DuanValue(time.time(), '数')
    
    def _builtin_format_time(self, args: List[DuanValue]) -> DuanValue:
        """格式化时间"""
        from datetime import datetime
        time_str = str(args[0].value)
        fmt = str(args[1].value)
        try:
            dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            return DuanValue(dt.strftime(fmt), '串')
        except ValueError:
            try:
                dt = datetime.strptime(time_str, '%Y-%m-%d')
                return DuanValue(dt.strftime(fmt), '串')
            except ValueError:
                raise RuntimeError(f"无法解析时间: '{time_str}'")
    
    def _builtin_date_diff(self, args: List[DuanValue]) -> DuanValue:
        """日期差"""
        from datetime import datetime
        d1 = str(args[0].value)
        d2 = str(args[1].value)
        try:
            dt1 = datetime.strptime(d1, '%Y-%m-%d')
            dt2 = datetime.strptime(d2, '%Y-%m-%d')
            diff = (dt2 - dt1).days
            return DuanValue(diff, '数')
        except ValueError as e:
            raise RuntimeError(f"日期格式无效: {e}")
    
    # ----- 哈希函数 -----
    
    def _builtin_md5(self, args: List[DuanValue]) -> DuanValue:
        """MD5哈希"""
        import hashlib
        text = str(args[0].value)
        return DuanValue(hashlib.md5(text.encode('utf-8')).hexdigest(), '串')
    
    def _builtin_sha256(self, args: List[DuanValue]) -> DuanValue:
        """SHA256哈希"""
        import hashlib
        text = str(args[0].value)
        return DuanValue(hashlib.sha256(text.encode('utf-8')).hexdigest(), '串')
    
    def _builtin_base64_encode(self, args: List[DuanValue]) -> DuanValue:
        """Base64编码"""
        import base64
        text = str(args[0].value)
        return DuanValue(base64.b64encode(text.encode('utf-8')).decode('ascii'), '串')
    
    def _builtin_base64_decode(self, args: List[DuanValue]) -> DuanValue:
        """Base64解码"""
        import base64
        text = str(args[0].value)
        try:
            return DuanValue(base64.b64decode(text).decode('utf-8'), '串')
        except Exception as e:
            raise RuntimeError(f"Base64解码失败: {e}")
    
    # ----- 正则表达式函数 -----
    
    def _builtin_regex_match(self, args: List[DuanValue]) -> DuanValue:
        """正则匹配（开头匹配）"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        m = re.match(pattern, text)
        if m:
            return DuanValue(m.group(0), '串')
        return DuanValue(None, '空')
    
    def _builtin_regex_search(self, args: List[DuanValue]) -> DuanValue:
        """正则搜索（第一个匹配）"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        m = re.search(pattern, text)
        if m:
            return DuanValue(m.group(0), '串')
        return DuanValue(None, '空')
    
    def _builtin_regex_find_all(self, args: List[DuanValue]) -> DuanValue:
        """查找所有正则匹配"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        result = re.findall(pattern, text)
        return DuanValue(result, '列')
    
    def _builtin_regex_replace(self, args: List[DuanValue]) -> DuanValue:
        """正则替换"""
        import re
        pattern = str(args[0].value)
        repl = str(args[1].value)
        text = str(args[2].value)
        try:
            result = re.sub(pattern, repl, text)
            return DuanValue(result, '串')
        except re.error as e:
            raise RuntimeError(f"正则替换失败: {e}")
    
    def _builtin_regex_split(self, args: List[DuanValue]) -> DuanValue:
        """正则分割"""
        import re
        pattern = str(args[0].value)
        text = str(args[1].value)
        result = re.split(pattern, text)
        return DuanValue(result, '列')