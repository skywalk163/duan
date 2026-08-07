# -*- coding: utf-8 -*-
"""
段言编译器 - 美化的错误和 traceback 处理

提供中文错误信息、源代码上下文显示、栈追踪美化等功能。
"""

import sys
import traceback
import os


# =============================================================================
# D05: 全量中文错误名称映射表（20 种标准异常类型）
# =============================================================================
CHINESE_ERROR_NAMES = {
    'SyntaxError': '语法解析错误',
    'TypeError': '类型错误',
    'ValueError': '值错误',
    'NameError': '名称错误',
    'IndexError': '索引错误',
    'KeyError': '键错误',
    'AttributeError': '属性错误',
    'ImportError': '导入错误',
    'RuntimeError': '运行时错误',
    'ZeroDivisionError': '除零错误',
    'FileNotFoundError': '文件未找到',
    'IOError': '输入输出错误',
    'MemoryError': '内存错误',
    'RecursionError': '递归错误',
    'StopIteration': '迭代停止',
    'AssertionError': '断言错误',
    'NotImplementedError': '未实现错误',
    'OverflowError': '溢出错误',
    'ArithmeticError': '算术错误',
    'LookupError': '查找错误',
    # 额外常见异常
    'ModuleNotFoundError': '模块未找到',
    'PermissionError': '权限错误',
    'IndentationError': '缩进错误',
    'TabError': '制表符错误',
    'UnicodeError': 'Unicode 错误',
    'EOFError': '输入结束错误',
    'KeyboardInterrupt': '用户中断',
    'SystemExit': '系统退出',
    'ConnectionError': '连接错误',
    'TimeoutError': '超时错误',
    'OSError': '系统错误',
    'UnicodeDecodeError': 'Unicode解码错误',
    'UnicodeEncodeError': 'Unicode编码错误',
    'FloatingPointError': '浮点运算错误',
    'ReferenceError': '引用错误',
    'SystemError': '系统内部错误',
}

# =============================================================================
# D06: 中文错误附带修改指引
# =============================================================================
CHINESE_ERROR_HINTS = {
    'SyntaxError': '请检查代码语法是否正确，确保所有括号、引号、冒号等符号已正确配对。',
    'TypeError': '请检查操作数类型是否匹配，段言中文本和数字不能直接进行运算。',
    'ValueError': '请检查传入的值是否在有效范围内，可能需要先进行类型转换。',
    'NameError': '请检查变量名是否拼写正确，使用前需先通过「设」关键字定义变量。',
    'IndexError': '请检查索引是否在有效范围内，段言列表索引从 0 开始。',
    'KeyError': '请检查字典键是否存在，可以使用「字典包含键」方法先判断。',
    'AttributeError': '请检查对象是否拥有该属性或方法，需确认类定义中已声明。',
    'ImportError': '请检查模块名是否拼写正确，确认模块已安装或在标准库路径中。',
    'RuntimeError': '程序运行时出现异常，请根据具体错误信息排查。',
    'ZeroDivisionError': '除数不能为零，请在除法前添加条件判断。',
    'FileNotFoundError': '请检查文件路径是否正确，确认文件是否存在。',
    'IOError': '输入输出操作失败，请检查文件状态和权限。',
    'MemoryError': '内存不足，请尝试优化代码或增加系统内存。',
    'RecursionError': '递归过深，请检查函数是否存在无限递归，增加递归终止条件。',
    'StopIteration': '迭代器已无更多元素，请检查循环逻辑或使用默认值。',
    'AssertionError': '断言条件不满足，请检查断言表达式是否正确。',
    'NotImplementedError': '该方法尚未实现，请补充实现代码。',
    'OverflowError': '数值运算结果超出范围，请使用更大的数据类型。',
    'ArithmeticError': '算术运算出错，请检查操作数和运算符是否正确。',
    'LookupError': '查找操作失败，请检查索引或键是否存在。',
}

# 段言特有错误修改指引
CHINESE_DUAN_ERROR_HINTS = {
    '设': '缺少「设」关键字后的变量名，例如：设 甲 为 10',
    '接收': '段落定义缺少「接收」关键字，例如：段落 计算 接收 参数：',
    '如果': '条件表达式缺少冒号结尾，例如：如果 甲 大于 0：',
    '冒号': '块语句后必须使用中文冒号「：」结尾，例如：如果 条件：',
    '缩进': '请检查缩进是否一致，段言使用 4 空格缩进，例如：段落 测试：',
    '引号': '字符串引号未闭合，请检查引号是否成对出现，例如：打印("hello")',
    '括号': '括号不匹配，请检查所有括号是否成对，例如：打印(长度(列表))',
    '返回': '段落缺少「返回」语句或返回值类型不匹配，例如：返回 值',
    '定义': '变量定义格式应为：设 变量名 为 值，例如：设 甲 为 10',
    '遍历': '遍历循环格式应为：遍历 变量 之 集合，例如：遍历 项 之 列表',
}


def get_chinese_error_name(exc_name: str) -> str:
    """获取异常的完整中文名称"""
    return CHINESE_ERROR_NAMES.get(exc_name, exc_name)


def get_chinese_error_hint(exc_name: str) -> str:
    """获取异常的中文修改指引"""
    hint = CHINESE_ERROR_HINTS.get(exc_name)
    if hint:
        return f"💡 修改建议：{hint}"
    return ""


def get_duan_error_hint(error_msg: str) -> str:
    """根据错误消息内容，返回段言特有的中文修改指引"""
    for keyword, hint in CHINESE_DUAN_ERROR_HINTS.items():
        if keyword in error_msg:
            return f"💡 修改建议：{hint}"
    return ""


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
    
    # 异常类型（使用全量中文映射）
    exc_name = exc_type.__name__
    chinese_name = get_chinese_error_name(exc_name)
    lines.append(f"║  错误类型: {chinese_name:<45}║")
    
    # 错误信息
    error_msg = str(exc_value)
    if len(error_msg) > 45:
        error_msg = error_msg[:42] + "..."
    lines.append(f"║  错误信息: {error_msg:<45}║")
    
    # D06: 添加中文修改指引
    hint = get_chinese_error_hint(exc_name)
    if hint:
        hint_short = hint.replace("💡 修改建议：", "")
        if len(hint_short) > 45:
            hint_short = hint_short[:42] + "..."
        lines.append(f"║  修改建议: {hint_short:<45}║")
    
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
        
        # D06: 自动从段言错误提示中匹配关键字补充指引
        duan_hint = get_duan_error_hint(message)
        if hint is None and duan_hint:
            hint = duan_hint
        
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
