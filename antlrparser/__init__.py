"""
段言（Duan）编程语言 - ANTLR 解析器包

确保包内模块间的扁平导入（from duan_ast import xxx）在作为 pip 包安装后也能正常工作。
"""
import sys
import os

# 将包目录加入 sys.path，使 flat imports 在包内有效
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)