# -*- coding: utf-8 -*-
"""
段言编译器 - 美化的错误和 traceback 处理

提供中文错误信息、源代码上下文显示、栈追踪美化等功能。
"""

import sys
import traceback
import os


def format_exception(exc_type, exc_value, exc_tb, source_lines=None):
    """格式化异常为美化的中文输出"""
    if source_lines is None:
        source_lines = []
    
    # 词法/语法错误
    if hasattr(exc_value, 'source_lines'):
        return str(exc_value)
    
    # 普通异常
    lines = []
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║                      段言运行错误                         ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    # 异常类型
    exc_name = exc_type.__name__
    chinese_names = {
        'SyntaxError': '语法错误',
        'NameError': '名称错误',
        'TypeError': '类型错误',
        'ValueError': '值错误',
        'IndexError': '索引错误',
        'KeyError': '键错误',
        'AttributeError': '属性错误',
        'ZeroDivisionError': '除零错误',
        'OverflowError': '溢出错误',
        'RecursionError': '递归错误',
        'ImportError': '导入错误',
        'ModuleNotFoundError': '模块未找到',
        'FileNotFoundError': '文件未找到',
        'PermissionError': '权限错误',
        'RuntimeError': '运行时错误',
        'StopIteration': '迭代停止',
        'AssertionError': '断言错误',
        'IndentationError': '缩进错误',
        'TabError': '制表符错误',
        'UnicodeError': 'Unicode 错误',
        'EOFError': '输入结束错误',
        'KeyboardInterrupt': '用户中断',
        'SystemExit': '系统退出',
    }
    chinese_name = chinese_names.get(exc_name, exc_name)
    lines.append(f"║  错误类型: {chinese_name:<45}║")
    
    # 错误信息
    error_msg = str(exc_value)
    if len(error_msg) > 45:
        error_msg = error_msg[:42] + "..."
    lines.append(f"║  错误信息: {error_msg:<45}║")
    
    lines.append("╚══════════════════════════════════════════════════════════╝")
    lines.append("")
    
    # 栈追踪
    tb_list = traceback.format_tb(exc_tb)
    if len(tb_list) > 1:
        lines.append("调用栈:")
        lines.append("─" * 60)
        
        for i, tb_entry in enumerate(tb_list):
            # 解析栈追踪条目
            for line in tb_entry.strip().split('\n'):
                if 'File' in line:
                    # 解析文件路径
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        file_part = parts[0].replace('File ', '').strip('"')
                        location_part = parts[1].strip() if len(parts) > 1 else ''
                        # 只显示项目内的文件
                        if 'duan' in file_part.lower() or 'src' in file_part.lower():
                            lines.append(f"  → {file_part} {location_part}")
            if i > 0:  # 跳过第一个（用户代码）
                break
    
    lines.append("")
    return '\n'.join(lines)


def install_excepthook():
    """安装自定义的异常处理器"""
    old_excepthook = sys.excepthook
    
    def custom_excepthook(exc_type, exc_value, exc_tb):
        # 如果是段言相关的错误，使用美化格式
        if 'duan' in str(exc_type).lower() or hasattr(exc_value, 'source_lines'):
            print(format_exception(exc_type, exc_value, exc_tb), file=sys.stderr)
        else:
            # 其他错误使用原始格式
            old_excepthook(exc_type, exc_value, exc_tb)
    
    sys.excepthook = custom_excepthook


def format_source_context(source, line, col=None, context_lines=3):
    """格式化源代码上下文"""
    if not source:
        return ""
    
    lines = source.split('\n')
    if line < 1 or line > len(lines):
        return ""
    
    result = []
    start = max(0, line - context_lines - 1)
    end = min(len(lines), line + context_lines)
    
    for i in range(start, end):
        line_num = i + 1
        line_content = lines[i].rstrip()
        prefix = "→ " if line_num == line else "  "
        result.append(f"{prefix}{line_num:4d} │ {line_content}")
        
        if line_num == line and col:
            # 添加列指示符
            indent = len(str(line_num)) + 5
            arrow = " " * (indent + min(col, len(line_content)) - 1) + "^"
            result.append(arrow)
    
    return '\n'.join(result)


class DuanError(Exception):
    """段言基础错误类"""
    def __init__(self, message: str, line: int = 0, col: int = 0, hint: str = None):
        self.message = message
        self.line = line
        self.col = col
        self.hint = hint
        
        parts = []
        parts.append("\n┌─ 段言错误")
        
        if line:
            pos_info = f"行 {line}"
            if col:
                pos_info += f", 列 {col}"
            parts.append(f"│ 位置: {pos_info}")
        
        parts.append(f"│ 原因: {message}")
        
        if hint:
            parts.append(f"│ 提示: {hint}")
        
        parts.append("└─")
        super().__init__('\n'.join(parts))


class LexerError(DuanError):
    """词法分析错误"""
    def __init__(self, message: str, line: int = 0, col: int = 0, hint: str = None):
        message = f"词法分析错误: {message}"
        super().__init__(message, line, col, hint)


class SemanticError(DuanError):
    """语义分析错误"""
    def __init__(self, message: str, line: int = 0, col: int = 0, hint: str = None):
        message = f"语义错误: {message}"
        super().__init__(message, line, col, hint)


# 安装默认的异常处理器
install_excepthook()
