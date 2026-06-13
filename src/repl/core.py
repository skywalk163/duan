#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
段言 REPL 核心类

提供交互式开发环境的核心功能。
"""

import sys
import os
from typing import Optional

# 添加路径
_current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _current_dir)
sys.path.insert(0, os.path.join(_current_dir, 'src'))
sys.path.insert(0, os.path.join(_current_dir, 'antlrparser'))

from .executor import Executor, Environment


# =============================================================================
# DuanREPL 核心类
# =============================================================================

class DuanREPL:
    """段言交互式开发环境核心类

    提供：
    - 代码执行
    - 环境管理
    - 历史记录
    - 自动补全（预留）
    """

    def __init__(self):
        """初始化REPL"""
        self.executor = Executor()
        self.history = []
        self._setup_welcome()

    def _setup_welcome(self):
        """设置欢迎信息"""
        self.welcome = """
=== 段言 REPL v1.0 ===
输入段言代码即可执行。
输入 帮助 获取命令列表。
输入 退出 退出REPL。
"""

    def run(self):
        """运行REPL主循环"""
        print(self.welcome)

        while True:
            try:
                # 读取输入
                code = input("段言> ").strip()

                if not code:
                    continue

                # 处理特殊命令
                if code in ['退出', 'exit', 'quit', 'q']:
                    print("再见！")
                    break

                if code in ['帮助', 'help', 'h', '?']:
                    self._show_help()
                    continue

                if code in ['历史', 'history', 'hi']:
                    self._show_history()
                    continue

                if code in ['重置', 'reset', 'clear']:
                    self.executor.reset()
                    print("环境已重置。")
                    continue

                if code in ['环境', 'env', 'e']:
                    self._show_env()
                    continue

                # 执行代码
                self.history.append(code)
                result = self.executor.execute(code)

                # 显示结果
                if result is not None:
                    print(f"=> {result}")

            except KeyboardInterrupt:
                print("\n按 Ctrl+C 退出请输入 退出。")
            except EOFError:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")

    def execute(self, code: str) -> any:
        """执行代码并返回结果

        Args:
            code: 段言代码

        Returns:
            执行结果
        """
        return self.executor.execute(code)

    def _show_help(self):
        """显示帮助信息"""
        print("""
=== 段言 REPL 帮助 ===

命令:
  帮助, help     显示此帮助信息
  退出, exit     退出REPL
  历史, history  显示历史记录
  重置, reset    重置执行环境
  环境, env      显示当前环境变量

代码示例:
  设 甲 为 3。           # 变量声明
  甲 加 5               # 简单表达式
  打印(甲)。            # 打印输出
  段落 平方 接收 数值:   # 函数定义
      返回 数值 * 数值。
  结束。
""")

    def _show_history(self):
        """显示历史记录"""
        print("=== 历史记录 ===")
        for i, cmd in enumerate(self.history, 1):
            print(f"{i}: {cmd}")

    def _show_env(self):
        """显示当前环境"""
        print("=== 当前环境 ===")
        variables = self.executor.env.variables
        functions = self.executor.env.functions

        if variables:
            print("变量:")
            for name, value in variables.items():
                print(f"  {name} = {value}")
        else:
            print("变量: (空)")

        if functions:
            print("函数:")
            for name in functions.keys():
                print(f"  {name}()")
        else:
            print("函数: (空)")


# =============================================================================
# 入口点
# =============================================================================

def main():
    """REPL入口点"""
    repl = DuanREPL()
    repl.run()


if __name__ == '__main__':
    main()
