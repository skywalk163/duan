"""段言 REPL 命令处理器"""

from typing import Any, Dict, List, Optional


class CommandHandler:
    """段言 REPL 命令处理器"""

    # 命令映射（主命令 -> 中文别名）
    COMMANDS = {
        'help': ['帮助', 'h'],
        'exit': ['退出', 'quit', 'q'],
        'clear': ['清除', 'cls'],
        'reset': ['重置'],
        'vars': ['变量', 'var'],
        'funcs': ['段落', 'func', 'functions'],
        'classes': ['类', 'class'],
        'history': ['历史'],
        'load': ['加载'],
        'save': ['保存'],
        'debug': ['调试'],
        'step': ['单步'],
        'break': ['断点'],
    }

    def __init__(self, env: Dict = None, executor=None):
        """初始化命令处理器

        Args:
            env: 环境变量字典
            executor: 执行器实例
        """
        self.env = env if env is not None else {}
        self.executor = executor
        self._history: List[str] = []
        self._debug_enabled = False

    def handle(self, input: str) -> Any:
        """处理命令输入

        Args:
            input: 命令字符串（已去除前导冒号）

        Returns:
            'EXIT' - 退出REPL
            'CLEAR' - 清屏
            'RESET' - 重置环境
            其他字符串 - 显示给用户
        """
        input = input.strip()
        if not input:
            return ''

        # 去除前导冒号
        if input.startswith(':'):
            input = input[1:]

        # 解析命令和参数
        parts = input.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ''

        # 查找命令（支持别名）
        actual_cmd = self._resolve_command(cmd)
        if actual_cmd is None:
            return f"未知命令: {cmd}"

        return self._execute(actual_cmd, args)

    def _resolve_command(self, cmd: str) -> Optional[str]:
        """解析命令，支持别名

        Args:
            cmd: 命令或别名

        Returns:
            主命令名称，如果未找到返回None
        """
        # 先检查是否已经是主命令
        if cmd in self.COMMANDS:
            return cmd

        # 搜索别名
        for main_cmd, aliases in self.COMMANDS.items():
            if cmd in aliases:
                return main_cmd

        return None

    def _execute(self, cmd: str, args: str) -> Any:
        """执行命令

        Args:
            cmd: 命令名称
            args: 命令参数

        Returns:
            命令执行结果
        """
        handlers = {
            'help': self._help,
            'exit': lambda: 'EXIT',
            'clear': lambda: 'CLEAR',
            'reset': lambda: 'RESET',
            'vars': self._show_vars,
            'funcs': self._show_funcs,
            'classes': self._show_classes,
            'history': self._show_history,
            'load': lambda: self._load_file(args),
            'save': lambda: self._save_session(args),
            'debug': lambda: self._toggle_debug(args),
        }

        handler = handlers.get(cmd)
        if handler:
            return handler()

        return f"未知命令: {cmd}"

    def _help(self) -> str:
        """显示帮助信息"""
        return """段言 REPL 帮助

命令:
  :help / :帮助     - 显示此帮助
  :exit / :退出     - 退出 REPL
  :clear / :清除    - 清屏
  :reset / :重置    - 重置环境
  :vars / :变量     - 显示所有变量
  :funcs / :段落    - 显示所有段落
  :classes / :类    - 显示所有类
  :history / :历史  - 显示命令历史
  :load <file>      - 加载文件
  :save <file>      - 保存会话
  :debug on/off     - 开启/关闭调试"""

    def _show_vars(self) -> str:
        """显示所有变量"""
        if not self.env:
            return "无变量"

        lines = []
        for name, value in self.env.items():
            lines.append(f"  {name} = {value}")
        return "变量:\n" + "\n".join(lines)

    def _show_funcs(self) -> str:
        """显示所有段落（函数）"""
        if not self.executor:
            return "无段落"

        funcs = getattr(self.executor, 'funcs', {})
        if not funcs:
            return "无段落"

        lines = []
        for name in funcs:
            lines.append(f"  {name}")
        return "段落:\n" + "\n".join(lines)

    def _show_classes(self) -> str:
        """显示所有类"""
        if not self.executor:
            return "无类"

        classes = getattr(self.executor, 'classes', {})
        if not classes:
            return "无类"

        lines = []
        for name in classes:
            lines.append(f"  {name}")
        return "类:\n" + "\n".join(lines)

    def _show_history(self) -> str:
        """显示命令历史"""
        if not self._history:
            return "无历史"

        lines = []
        for i, cmd in enumerate(self._history, 1):
            lines.append(f"  {i}. {cmd}")
        return "历史:\n" + "\n".join(lines)

    def _load_file(self, filename: str) -> str:
        """加载文件"""
        if not filename:
            return "请指定文件名: :load <file>"

        return f"加载文件: {filename}"

    def _save_session(self, filename: str) -> str:
        """保存会话"""
        if not filename:
            return "请指定文件名: :save <file>"

        return f"保存会话: {filename}"

    def _toggle_debug(self, args: str) -> str:
        """切换调试模式"""
        args = args.strip().lower()

        if args == 'on':
            self._debug_enabled = True
            return "调试模式已开启"
        elif args == 'off':
            self._debug_enabled = False
            return "调试模式已关闭"
        else:
            return "用法: :debug on/off"

    def add_history(self, cmd: str) -> None:
        """添加命令到历史记录

        Args:
            cmd: 命令字符串
        """
        self._history.append(cmd)
