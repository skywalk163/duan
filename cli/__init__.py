# 段言（Duan）CLI 工具包
"""
本包提供段言语言的命令行工具：
- duan.py: 主命令行入口
- duan_unified.py: 统一编译器 CLI（支持 antlr/src 双后端）
- duanc.py: 编译运行工具

用法：
    python -m cli.duan_unified <源文件> [--target antlr|src] [--output <输出>]
    python cli/duanc.py <源文件> --run
"""