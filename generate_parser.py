#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys

# 检查 Java 是否可用
try:
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("错误: Java 不可用，请安装 Java 11+")
        sys.exit(1)
    print("Java 已安装")
except FileNotFoundError:
    print("错误: Java 不可用，请安装 Java 11+")
    sys.exit(1)

# 检查 ANTLR jar 文件是否存在
antlr_jar = "antlr-4.13.2-complete.jar"
if not os.path.exists(antlr_jar):
    print(f"正在下载 ANTLR jar 文件...")
    try:
        # 使用 curl 或 wget 下载
        import urllib.request
        url = "https://www.antlr.org/download/antlr-4.13.2-complete.jar"
        urllib.request.urlretrieve(url, antlr_jar)
        print(f"ANTLR jar 下载成功")
    except Exception as e:
        print(f"下载 ANTLR jar 失败: {e}")
        sys.exit(1)

# 生成解析器
print("正在生成解析器...")

# Lexer 文件
lexer_file = "antlrparser/DuanLangLexer.g4"
# Parser 文件  
parser_file = "antlrparser/DuanLangParser.g4"
# 输出目录
output_dir = "antlrparser/duan_parser"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 生成命令
cmd = [
    'java', '-jar', antlr_jar,
    '-Dlanguage=Python3',
    '-o', output_dir,
    lexer_file,
    parser_file
]

print(f"执行命令: {' '.join(cmd)}")

try:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
    if result.returncode == 0:
        print("解析器生成成功!")
        print("生成的文件:")
        for f in os.listdir(output_dir):
            print(f"  - {f}")
    else:
        print(f"生成失败!")
        print(f"标准输出:\n{result.stdout}")
        print(f"错误输出:\n{result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"执行命令失败: {e}")
    sys.exit(1)
