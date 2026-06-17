#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
段言 REPL 核心类

提供交互式开发环境的核心功能。
"""

import sys
import os
from typing import List, Optional

# 添加路径
_current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _current_dir)
sys.path.insert(0, os.path.join(_current_dir, 'src'))
sys.path.insert(0, os.path.join(_current_dir, 'antlrparser'))

from .executor import Executor, Environment
from .commands import CommandHandler


# =============================================================================
# DuanREPL 核心类
# =============================================================================

class DuanREPL:
    """段言交互式开发环境核心类

    提供：
    - 代码执行
    - 环境管理
    - 历史记录
    - 多行支持
    - 命令处理
    """

    def __init__(self, enhanced: bool = False):
        """初始化REPL

        Args:
            enhanced: 是否使用增强模式（prompt_toolkit）
        """
        self.executor = Executor()
        self.command_handler = CommandHandler(
            env=self.executor.env.variables,
            executor=self.executor
        )
        self.buffer: List[str] = []
        self.history: List[str] = []
        self.debug_mode = False
        self.enhanced = enhanced

        # 尝试加载增强模式
        if enhanced:
            try:
                from .enhanced import EnhancedREPL, HAS_PROMPT_TOOLKIT
                if HAS_PROMPT_TOOLKIT:
                    self._enhanced_impl = EnhancedREPL(self)
                    self._use_enhanced = True
                else:
                    self._use_enhanced = False
            except ImportError:
                self._use_enhanced = False
        else:
            self._use_enhanced = False

    def _is_multiline_start(self, line: str) -> bool:
        """判断是否是多行开始"""
        starters = ['段落', '类', '接口', '如果', '当', '遍历', '尝试']
        for s in starters:
            if line.startswith(s) and (line.endswith(':') or line.endswith('：')):
                return True
        return False

    def _is_multiline_end(self, line: str) -> bool:
        """判断是否是多行结束"""
        return line.strip() in ['结束。', '结束', '结束。', '否则', '否则：', '否则:']

    def execute_buffer(self) -> Optional[str]:
        """执行缓冲区代码"""
        code = '\n'.join(self.buffer)
        self.buffer = []
        self.history.append(code)

        try:
            self.executor.execute(code)
            return "执行完成"
        except Exception as e:
            return f"错误: {e}"

    def process_input(self, line: str) -> Optional[str]:
        """处理输入"""
        line = line.strip()

        # 空行
        if not line:
            if self.buffer:
                return self.execute_buffer()
            return None

        # 注释
        if line.startswith('#'):
            return None

        # 命令（以 : 开头）
        if line.startswith(':'):
            result = self.command_handler.handle(line)
            self.history.append(line)

            if result == 'CLEAR':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_banner()
                return None
            elif result == 'RESET':
                self.executor.reset()
                return "环境已重置"

            return result

        # 多行检测
        if self._is_multiline_start(line):
            self.buffer.append(line)
            return None

        # 添加到缓冲区
        if self.buffer:
            self.buffer.append(line)
            if self._is_multiline_end(line):
                return self.execute_buffer()
            return None

        # 单行执行
        return self.execute_line(line)

    def print_banner(self):
        """打印欢迎信息"""
        print("""
╔══════════════════════════════════════════════╗
║           段言 (DuanLang) REPL              ║
║           版本: 1.0.0                        ║
║                                              ║
║  输入段言代码，按 Enter 执行                  ║
║  输入 :help 获取帮助                         ║
║  输入 :exit 或按 Ctrl+D 退出                 ║
╚══════════════════════════════════════════════╝
""")

    def run(self):
        """启动REPL主循环"""
        self.print_banner()

        while True:
            try:
                # 读取输入
                if self.buffer:
                    prompt = "...   "
                else:
                    prompt = "段言> "

                line = self.read_input(prompt)

                if line is None:
                    break

                # 处理输入
                result = self.process_input(line)

                # 显示结果
                if result and result != 'EXIT':
                    print(result)

                if result == 'EXIT':
                    print("再见！")
                    break

            except KeyboardInterrupt:
                print("\n^C")
                self.buffer = []
            except EOFError:
                print("\n再见！")
                break

    def read_input(self, prompt: str) -> Optional[str]:
        """读取用户输入"""
        try:
            return input(prompt)
        except EOFError:
            return None

    def execute_line(self, line: str) -> Optional[str]:
        """执行单行代码"""
        self.history.append(line)

        try:
            result = self.executor.execute(line)

            if result is not None:
                return str(result)

            return None
        except Exception as e:
            return f"错误: {e}"

    def execute(self, code: str):
        """执行代码并返回结果

        Args:
            code: 段言代码

        Returns:
            执行结果
        """
        return self.executor.execute(code)


# =============================================================================
# 入口点
# =============================================================================

def main():
    """REPL入口点"""
    repl = DuanREPL()
    repl.run()


if __name__ == '__main__':
    main()
