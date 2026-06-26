# 快速开始

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install duan
```

### 从源码安装

```bash
git clone https://github.com/skywalk163/duan.git
cd duan
pip install -e .
```

## 运行方式

### 1. 使用 CLI 编译运行

```bash
# 编译运行
duan run examples/hello.duan

# 编译为可执行文件
duan build examples/hello.duan -o hello.exe
```

### 2. 使用统一 CLI

```bash
# ANTLR 后端（兼容旧语法）
python -m cli.duan_unified examples/hello.duan --backend antlr

# SRC 后端（3.x 纯缩进语法）
python -m cli.duan_unified examples/hello.duan --backend src
```

## Hello World

创建 `hello.duan`：

```段言
打印 "你好，世界！"
```

运行：

```bash
duan run hello.duan
```

## REPL 交互式解释器

```bash
duan repl
```

## 调试模式

```bash
duan debug hello.duan
```

## 验证安装

```bash
duan --version
duan --help
```
