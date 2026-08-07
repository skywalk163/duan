#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言离线轻量级小模型方案

提供离线环境下的小模型代码生成能力。核心思路：
  1. 优先加载本地小模型（如 Qwen2.5-0.5B 等）
  2. 模型不可用时回退到基于规则的代码生成
  3. 支持代码生成、语法修正、代码补全三种模式

模型下载与设置：
    # 使用 Hugging Face transformers 加载模型
    pip install transformers torch

    # 推荐模型（按体积排序）：
    #   Qwen/Qwen2.5-0.5B-Instruct    ~1GB  [推荐]
    #   Qwen/Qwen2.5-1.5B-Instruct    ~3GB
    #   microsoft/Phi-3-mini-4k-instruct ~4GB
    #   google/gemma-2-2b-it          ~3GB

    # 下载模型（自动缓存）：
    python -c "from transformers import AutoModelForCausalLM, AutoTokenizer;
    AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct');
    AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')"

用法：
    from offline_model import OfflineModel

    model = OfflineModel()
    code = model.generate("写一个二分查找函数")
    fixed = model.fix_syntax("段落 加法 接收 a, b：\n    返回 a 加 错误")
    completed = model.complete("段落 斐波那契 接收 n：\n    ")
"""

import os
import sys
import json
import re
import logging
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 规则引擎：当模型不可用时的回退方案
# ═══════════════════════════════════════════════════════════════════

# 段言关键字
DUAN_KEYWORDS = {
    '定义', '常量', '类型', '导入', '导出', '从', '为', '设',
    '如果', '否则', '否则若', '若', '则',
    '遍历', '当', '跳出', '跳过', '在', '于', '对', '中的',
    '函数', '段落', '段', '接收', '返回',
    '尝试', '捕获', '抛出', '最终',
    '类', '继承', '属性', '构造', '新建',
    '匹配', '情况',
    '使用', '标注',
    '异步', '等待', '作用域',
    '生成',
    '打印', '读取',
    '真', '假', '空',
    '己', '父',
    '加', '减', '乘', '除', '模', '幂',
    '加上', '减去', '乘以', '除以', '整除', '取余',
    '等于', '不等于', '大于', '小于', '大于等于', '小于等于',
    '且', '或', '非',
    '私有', '公有', '保护', '静态', '类方法', '特性',
    '打包', '筛选', '映射', '排序', '反转', '求和',
    '整数', '浮数', '串', '布尔', '列', '典', '集',
    '追加', '弹出', '删除', '清空', '插入',
    '字符串去空白', '字符串分割', '字符串替换', '字符串查找',
}


class RuleBasedGenerator:
    """基于规则的代码生成器（模型不可用时的回退）"""

    SNIPPETS = {
        "二分查找": """段落 二分查找 接收 arr, target：
    设 left 为 0
    设 right 为 len(arr) 减 1
    当 left 小于等于 right：
        设 mid 为 (left 加 right) 除以 2
        如果 arr[mid] 等于 target：
            返回 mid
        否则如果 arr[mid] 小于 target：
            left 为 mid 加 1
        否则：
            right 为 mid 减 1
    返回 -1""",

        "快速排序": """段落 快速排序 接收 arr：
    如果 len(arr) 小于等于 1：
        返回 arr
    设 基准 为 arr[0]
    设 左 为 []
    设 右 为 []
    遍历 x 于 arr[1:]：
        如果 x 小于 基准：
            左.append(x)
        否则：
            右.append(x)
    返回 快速排序(左) 加 [基准] 加 快速排序(右)""",

        "斐波那契": """段落 斐波那契 接收 n：
    如果 n 小于等于 0：
        返回 0
    如果 n 等于 1：
        返回 1
    返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)""",

        "阶乘": """段落 阶乘 接收 n：
    如果 n 小于等于 1：
        返回 1
    返回 n 乘 阶乘(n 减 1)""",

        "冒泡排序": """段落 冒泡排序 接收 arr：
    设 n 为 len(arr)
    遍历 i 于 range(n)：
        遍历 j 于 range(0, n 减 i 减 1)：
            如果 arr[j] 大于 arr[j 加 1]：
                设 tmp 为 arr[j]
                arr[j] 为 arr[j 加 1]
                arr[j 加 1] 为 tmp
    返回 arr""",

        "线性查找": """段落 线性查找 接收 arr, target：
    遍历 i 于 range(len(arr))：
        如果 arr[i] 等于 target：
            返回 i
    返回 -1""",

        "求和": """段落 求和 接收 arr：
    设 结果 为 0
    遍历 x 于 arr：
        结果 加上 x
    返回 结果""",

        "最大值": """段落 最大值 接收 arr：
    设 最大值 为 arr[0]
    遍历 x 于 arr：
        如果 x 大于 最大值：
            最大值 为 x
    返回 最大值""",

        "反转字符串": """段落 反转字符串 接收 s：
    返回 s[::-1]""",

        "素数判断": """段落 素数判断 接收 n：
    如果 n 小于 2：
        返回 假
    遍历 i 于 range(2, int(n ** 0.5) 加 1)：
        如果 n 模 i 等于 0：
            返回 假
    返回 真""",

        "类-学生": """类 学生：
    属性 姓名
    属性 年龄
    构造 接收 姓名, 年龄：
        己姓名 为 姓名
        己年龄 为 年龄
    段落 介绍：
        打印(f"我叫{己姓名}，今年{己年龄}岁")""",

        "类-矩形": """类 矩形：
    属性 宽
    属性 高
    构造 接收 宽, 高：
        己宽 为 宽
        己高 为 高
    段落 面积：
        返回 己宽 乘 己高
    段落 周长：
        返回 2 乘 (己宽 加 己高)""",

        "文件读取": """使用 读取文件("data.txt") 为 f：
    设 内容 为 f.read()
    打印(内容)""",

        "文件写入": """使用 打开文件("output.txt", "w") 为 f：
    f.write("hello world")""",

        "异常处理": """尝试：
    设 结果 为 10 除以 0
捕获 异常：
    打印("发生错误")
    设 结果 为 0""",

        "遍历数组": """遍历 i 于 range(0, 10)：
    打印(i)""",

        "遍历列表": """遍历 项 于 列表：
    打印(项)""",

        "模式匹配": """匹配 值：
    情况 1：
        打印("一")
    情况 2：
        打印("二")
    情况 _：
        打印("其他")""",

        "异步任务": """异步 作用域：
    等待 任务1()
    等待 任务2()""",
    }

    FIX_PATTERNS = [
        # 修复缺少冒号
        (r'(如果|当|遍历|否则若|否则|情况|捕获|使用|尝试|最终|匹配|异步)\s+(.+?)(?:\n|$)(?!：)', r'\1 \2：'),
        # 修复中文运算符混用英文
        (r'(\d+)\s*\+\s*(\d+)', r'\1 加 \2'),
        (r'(\d+)\s*\-\s*(\d+)', r'\1 减 \2'),
        (r'(\d+)\s*\*\s*(\d+)', r'\1 乘 \2'),
        (r'(\d+)\s*/\s*(\d+)', r'\1 除以 \2'),
        # 修复==
        (r'(\w+)\s*==\s*(\w+)', r'\1 等于 \2'),
        (r'(\w+)\s*!=\s*(\w+)', r'\1 不等于 \2'),
        (r'(\w+)\s*>=\s*(\w+)', r'\1 大于等于 \2'),
        (r'(\w+)\s*<=\s*(\w+)', r'\1 小于等于 \2'),
        (r'(\w+)\s*>\s*(\w+)', r'\1 大于 \2'),
        (r'(\w+)\s*<\s*(\w+)', r'\1 小于 \2'),
        # 修复 && 和 ||
        (r'(\w+)\s*&&\s*(\w+)', r'\1 且 \2'),
        (r'(\w+)\s*\|\|\s*(\w+)', r'\1 或 \2'),
        # 修复 ! 非
        (r'!(\w+)', r'非 \1'),
        # 修复 def 定义
        (r'def\s+(\w+)\s*\(([^)]*)\)\s*:', r'段落 \1 接收 \2：'),
        # 修复 for 循环
        (r'for\s+(\w+)\s+in\s+(.+?)\s*:', r'遍历 \1 于 \2：'),
        # 修复 while 循环
        (r'while\s+(.+?)\s*:', r'当 \1：'),
        # 修复 if/elif/else
        (r'if\s+(.+?)\s*:', r'如果 \1：'),
        (r'elif\s+(.+?)\s*:', r'否则若 \1：'),
        (r'else\s*:', r'否则：'),
        # 修复 try/except
        (r'try\s*:', r'尝试：'),
        (r'except\s+(\w+)\s+as\s+(\w+)\s*:', r'捕获 \1 \2：'),
        (r'except\s+(\w+)\s*:', r'捕获 \1：'),
        (r'except\s*:', r'捕获：'),
        (r'finally\s*:', r'最终：'),
        # 修复 return
        (r'return\s+(.+?)$', r'返回 \1'),
        (r'^return$', r'返回'),
        # 修复 True/False/None
        (r'\bTrue\b', '真'),
        (r'\bFalse\b', '假'),
        (r'\bNone\b', '空'),
        (r'\bself\b', '己'),
        (r'\bsuper\b', '父'),
        # 修复 print
        (r'print\((.+?)\)', r'打印(\1)'),
        # 修复 class
        (r'class\s+(\w+)\s*\(([^)]*)\)\s*:', r'类 \1 继承 \2：'),
        (r'class\s+(\w+)\s*:', r'类 \1：'),
        (r'def __init__\(self', r'构造 接收'),
        # 修复 += -= *= /=
        (r'(\w+)\s*\+=(\s*\w+)', r'\1 加上 \2'),
        (r'(\w+)\s*-=(\s*\w+)', r'\1 减去 \2'),
        (r'(\w+)\s*\*=(\s*\w+)', r'\1 乘以 \2'),
        (r'(\w+)\s*/=(\s*\w+)', r'\1 除以 \2'),
    ]

    def generate(self, query: str) -> str:
        """根据关键词匹配生成代码"""
        query_lower = query.lower()

        # 尝试精确匹配片段名
        for name, code in self.SNIPPETS.items():
            if name in query:
                return code

        # 关键词匹配
        if any(kw in query_lower for kw in ['二分', 'binary', '搜索', 'search']):
            return self.SNIPPETS["二分查找"]
        elif any(kw in query_lower for kw in ['排序', 'sort', '快速']):
            return self.SNIPPETS["快速排序"]
        elif any(kw in query_lower for kw in ['斐波那契', 'fibonacci', 'fib']):
            return self.SNIPPETS["斐波那契"]
        elif any(kw in query_lower for kw in ['阶乘', 'factorial', 'fact']):
            return self.SNIPPETS["阶乘"]
        elif any(kw in query_lower for kw in ['冒泡', 'bubble']):
            return self.SNIPPETS["冒泡排序"]
        elif any(kw in query_lower for kw in ['查找', '线性', 'linear']):
            return self.SNIPPETS["线性查找"]
        elif any(kw in query_lower for kw in ['求和', 'sum', '累加']):
            return self.SNIPPETS["求和"]
        elif any(kw in query_lower for kw in ['最大', 'max', '最小值']):
            return self.SNIPPETS["最大值"]
        elif any(kw in query_lower for kw in ['反转', 'reverse', '字符串']):
            return self.SNIPPETS["反转字符串"]
        elif any(kw in query_lower for kw in ['素数', '质数', 'prime']):
            return self.SNIPPETS["素数判断"]
        elif any(kw in query_lower for kw in ['类', '学生', 'student']):
            return self.SNIPPETS["类-学生"]
        elif any(kw in query_lower for kw in ['矩形', 'rectangle', '面积']):
            return self.SNIPPETS["类-矩形"]
        elif any(kw in query_lower for kw in ['文件', '读取', 'file', 'read']):
            return self.SNIPPETS["文件读取"]
        elif any(kw in query_lower for kw in ['写入', 'write', '保存']):
            return self.SNIPPETS["文件写入"]
        elif any(kw in query_lower for kw in ['异常', 'try', '捕获', '错误']):
            return self.SNIPPETS["异常处理"]
        elif any(kw in query_lower for kw in ['遍历', '循环', 'for', '迭代']):
            return self.SNIPPETS["遍历列表"]
        elif any(kw in query_lower for kw in ['匹配', 'match', '模式']):
            return self.SNIPPETS["模式匹配"]
        elif any(kw in query_lower for kw in ['异步', 'async', '等待']):
            return self.SNIPPETS["异步任务"]

        return "# 无法识别需求，请使用更具体的描述\n# 支持：排序、查找、斐波那契、阶乘、类定义、文件操作等"

    def fix_syntax(self, code: str) -> str:
        """修复常见的语法错误"""
        fixed = code
        for pattern, replacement in self.FIX_PATTERNS:
            fixed = re.sub(pattern, replacement, fixed)
        return fixed

    def complete(self, partial: str) -> str:
        """补全不完整的代码片段"""
        partial_stripped = partial.strip()

        # 段落定义补全
        m = re.match(r'段落\s+(\w+)\s+接收\s+(.+?)$', partial_stripped)
        if m:
            name = m.group(1)
            params = m.group(2)
            return f"{partial_stripped}：\n    返回 None"

        # 如果
        m = re.match(r'如果\s+(.+?)$', partial_stripped)
        if m:
            return f"{partial_stripped}：\n    跳过"

        # 遍历
        m = re.match(r'遍历\s+(\w+)\s+于\s+(.+?)$', partial_stripped)
        if m:
            return f"{partial_stripped}：\n    跳过"

        # 当
        m = re.match(r'当\s+(.+?)$', partial_stripped)
        if m:
            return f"{partial_stripped}：\n    跳过"

        # 尝试
        if partial_stripped == '尝试':
            return "尝试：\n    跳过"

        # 类
        m = re.match(r'类\s+(\w+)$', partial_stripped)
        if m:
            return f"{partial_stripped}：\n    属性 名称\n    构造 接收 名称：\n        己名称 为 名称"

        # 使用
        m = re.match(r'使用\s+(.+?)$', partial_stripped)
        if m:
            return f"{partial_stripped} 为 f：\n    跳过"

        return f"{partial_stripped}：\n    跳过"


# ═══════════════════════════════════════════════════════════════════
# 离线模型封装
# ═══════════════════════════════════════════════════════════════════

class OfflineModel:
    """离线轻量级段言代码生成模型

    使用本地小模型（如 Qwen2.5-0.5B）进行代码生成。
    当模型不可用时，自动回退到基于规则的生成器。

    Attributes:
        model_name: 模型名称
        model_available: 模型是否可用
        max_length: 生成的最大长度
        temperature: 生成温度
    """

    # 推荐模型列表（按推荐度排序）
    RECOMMENDED_MODELS = [
        "Qwen/Qwen2.5-0.5B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
        "microsoft/Phi-3-mini-4k-instruct",
        "google/gemma-2-2b-it",
    ]

    _SYSTEM_PROMPT = """你是一个段言（DuanLang）代码生成器。段言是一门中文编程语言。
关键语法规则：
- 段落定义：段落 名 接收 参数：  (缩进体)
- 变量：设 变量名 为 值
- 条件：如果 条件： / 否则： / 否则若 条件：
- 循环：遍历 变量 于 范围： / 当 条件：
- 返回：返回 表达式
- 运算符：加/减/乘/除以/模/幂；等于/不等于/大于/小于/大于等于/小于等于
- 且/或/非（逻辑运算符）
- 真/假/空/己/父（字面量）
- 类：类 名 继承 父类：/ 构造 接收 参数：/ 属性 字段
- 异常：尝试：/ 捕获 类型：/ 抛出 值/ 最终：
- 匹配：匹配 值：/ 情况 模式：
- 异步：异步 作用域：/ 等待 表达式
- 上下文：使用 表达式 为 变量：
- 装饰器：@标注 名
- f-string：f"文本{表达式}"

只输出段言代码，不要解释。"""

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        device: str = "auto",
        max_length: int = 512,
        temperature: float = 0.7,
        use_rule_fallback: bool = True,
    ):
        self.model_name = model_name
        self.device = device
        self.max_length = max_length
        self.temperature = temperature
        self.use_rule_fallback = use_rule_fallback

        self._model = None
        self._tokenizer = None
        self.model_available = False
        self._rule_engine = RuleBasedGenerator() if use_rule_fallback else None

        # 尝试加载模型
        self._try_load_model()

    def _try_load_model(self):
        """尝试加载本地模型"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch

            logger.info(f"正在加载模型: {self.model_name}")
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map=self.device if self.device != "auto" else "auto",
            )
            self.model_available = True
            logger.info(f"模型加载成功: {self.model_name}")
        except ImportError:
            logger.warning("transformers/torch 未安装，回退到规则引擎")
            self.model_available = False
        except Exception as e:
            logger.warning(f"模型加载失败: {e}，回退到规则引擎")
            self.model_available = False

    def generate(self, query: str, max_length: Optional[int] = None) -> str:
        """根据自然语言描述生成段言代码"""
        if self.model_available and self._model is not None:
            return self._model_generate(query, max_length)
        elif self._rule_engine:
            return self._rule_engine.generate(query)
        return "# 错误：模型不可用且规则引擎未初始化"

    def fix_syntax(self, code: str) -> str:
        """修正段言代码中的语法错误"""
        if self._rule_engine:
            return self._rule_engine.fix_syntax(code)
        return code

    def complete(self, partial: str, max_length: Optional[int] = None) -> str:
        """补全不完整的段言代码"""
        if self.model_available and self._model is not None:
            return self._model_complete(partial, max_length)
        elif self._rule_engine:
            return self._rule_engine.complete(partial)
        return "# 错误：模型不可用且规则引擎未初始化"

    def _model_generate(self, query: str, max_length: Optional[int] = None) -> str:
        """使用模型生成代码"""
        try:
            import torch

            messages = [
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": f"请用段言写一段代码：{query}"},
            ]

            prompt = self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )

            inputs = self._tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    max_new_tokens=max_length or self.max_length,
                    temperature=self.temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self._tokenizer.eos_token_id,
                )

            response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            # 提取模型生成的部分（去掉 prompt）
            if prompt in response:
                response = response[len(prompt):]
            return response.strip()

        except Exception as e:
            logger.error(f"模型生成失败: {e}")
            if self._rule_engine:
                return self._rule_engine.generate(query)
            return f"# 生成失败: {e}"

    def _model_complete(self, partial: str, max_length: Optional[int] = None) -> str:
        """使用模型补全代码"""
        try:
            import torch

            messages = [
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": f"请补全以下段言代码：\n{partial}"},
            ]

            prompt = self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )

            inputs = self._tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    max_new_tokens=max_length or min(self.max_length, 256),
                    temperature=0.5,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self._tokenizer.eos_token_id,
                )

            response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            if prompt in response:
                response = response[len(prompt):]
            return response.strip()

        except Exception as e:
            logger.error(f"模型补全失败: {e}")
            if self._rule_engine:
                return self._rule_engine.complete(partial)
            return f"# 补全失败: {e}"

    def get_status(self) -> Dict:
        """获取模型状态信息"""
        return {
            "model_name": self.model_name,
            "model_available": self.model_available,
            "max_length": self.max_length,
            "temperature": self.temperature,
            "rule_fallback": self.use_rule_fallback,
            "recommended_models": self.RECOMMENDED_MODELS,
        }


# ═══════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════

def cli_generate(args=None):
    """命令行生成代码"""
    import argparse
    parser = argparse.ArgumentParser(description="离线模型代码生成")
    parser.add_argument("query", nargs="?", help="生成需求描述")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct", help="模型名称")
    parser.add_argument("--fix", action="store_true", help="语法修正模式")
    parser.add_argument("--complete", action="store_true", help="代码补全模式")
    parser.add_argument("--status", action="store_true", help="查看模型状态")
    parser.add_argument("--max-length", type=int, default=512, help="最大生成长度")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成温度")

    args = parser.parse_args(args)

    model = OfflineModel(
        model_name=args.model,
        max_length=args.max_length,
        temperature=args.temperature,
    )

    if args.status:
        status = model.get_status()
        print("=== 离线模型状态 ===")
        for k, v in status.items():
            print(f"  {k}: {v}")
        print()
        print("推荐模型下载命令：")
        for m in model.RECOMMENDED_MODELS:
            print(f"  pip install transformers torch")
            print(f"  python -c \"from transformers import AutoModel, AutoTokenizer; "
                  f"AutoTokenizer.from_pretrained('{m}'); "
                  f"AutoModel.from_pretrained('{m}')\"")
        return

    if args.fix:
        code = sys.stdin.read() if not args.query else args.query
        if code:
            print(model.fix_syntax(code))
        else:
            print("请输入要修正的代码（通过参数或管道）")
        return

    if args.complete:
        partial = sys.stdin.read() if not args.query else args.query
        if partial:
            print(model.complete(partial))
        else:
            print("请输入要补全的代码片段（通过参数或管道）")
        return

    if args.query:
        print(model.generate(args.query))
    else:
        parser.print_help()


if __name__ == "__main__":
    cli_generate()