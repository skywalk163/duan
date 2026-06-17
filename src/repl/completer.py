#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
段言 REPL 自动补全

提供关键字、动词、变量名补全。
"""

from typing import List, Dict

# 关键字列表
KEYWORDS_LIST = [
    '设', '为', '段落', '接收', '返回', '类', '继承', '实现',
    '属性', '构造', '新建', '己', '如果', '那么', '否则', '结束',
    '遍历', '当', '跳出', '跳过', '尝试', '捕获', '抛出',
    '导入', '导出', '从', '真', '假', '空',
]

# 动词白名单
try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from keywords import VERB_ARITY
    VERBS_LIST = list(VERB_ARITY.keys())
except Exception:
    VERBS_LIST = [
        '打印', '长', '首', '末', '排序', '反转', '求和',
        '求最大', '求最小', '去重', '筛选', '映射',
        '转整数', '转浮点', '转字符串', '字符串长度',
        '分割字符串', '连接字符串', '替换字符串', '去除空白',
        '读取文件', '写入文件', '文件存在', '目录存在',
    ]

# 内置类型
TYPES_LIST = ['数', '串', '列', '典', '布尔', '任意', '整数', '浮数']


class DuanCompleter:
    """段言自动补全器"""
    
    def __init__(self, env: Dict = None):
        """初始化
        
        Args:
            env: 当前环境变量字典
        """
        self.env = env or {}
    
    def get_completions(self, text: str, cursor_pos: int = None) -> List[str]:
        """获取补全建议
        
        Args:
            text: 当前输入文本
            cursor_pos: 光标位置（可选）
            
        Returns:
            补全建议列表
        """
        if cursor_pos is None:
            cursor_pos = len(text)
        
        # 提取最后一个词
        words = text[:cursor_pos].split()
        if not words:
            return KEYWORDS_LIST[:10]
        
        last_word = words[-1]
        
        # 收集所有可能的补全
        candidates = []
        
        # 关键字
        candidates.extend(self._match(last_word, KEYWORDS_LIST))
        
        # 动词
        candidates.extend(self._match(last_word, VERBS_LIST))
        
        # 类型
        candidates.extend(self._match(last_word, TYPES_LIST))
        
        # 环境变量
        if self.env:
            candidates.extend(self._match(last_word, list(self.env.keys())))
        
        return candidates[:20]
    
    def _match(self, prefix: str, candidates: List[str]) -> List[str]:
        """匹配前缀"""
        if not prefix:
            return candidates[:10]
        return [c for c in candidates if c.startswith(prefix)]
    
    def update_env(self, env: Dict):
        """更新环境"""
        self.env = env


# prompt_toolkit 补全器（可选）
try:
    from prompt_toolkit.completion import Completer, Completion
    
    class PromptToolkitCompleter(Completer):
        """prompt_toolkit 补全器"""
        
        def __init__(self, duan_completer: DuanCompleter):
            self.completer = duan_completer
        
        def get_completions(self, document, complete_event):
            text = document.text
            cursor_pos = document.cursor_position
            
            completions = self.completer.get_completions(text, cursor_pos)
            
            for c in completions:
                # 计算起始位置（替换最后一个词）
                words = text[:cursor_pos].split()
                if words:
                    start_pos = cursor_pos - len(words[-1])
                else:
                    start_pos = cursor_pos
                
                yield Completion(c, start_position=-len(words[-1]) if words else 0)
    
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False
    PromptToolkitCompleter = None
