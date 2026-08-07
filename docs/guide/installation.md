# 安装说明

## 系统要求

- Python 3.10+
- 操作系统：Windows / macOS / Linux

## 通过 pip 安装

```bash
pip install duan4
```

## 从源码安装

```bash
git clone https://github.com/duan-lang/duan.git
cd duan
pip install -e .
```

## 验证安装

```bash
duan --version
```

## 可选依赖

```bash
# LLVM 后端支持
pip install llvmlite

# L3 领域嵌入支持
pip install numpy sympy pandas

# L4 Python 引用额外依赖
pip install matplotlib requests scikit-learn
```

## 开发环境

```bash
pip install pytest pytest-cov
pip install flake8
```