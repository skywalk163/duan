# 快速开始

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install duan
```

安装后即可使用 `duan` 命令：
```bash
duan --version
duan --help
```

### 从源码安装

```bash
git clone https://github.com/skywalk163/duan.git
cd duan
pip install -e .
```

## 3 步跑起来

### 第1步：安装

```bash
pip install duan
```

### 第2步：创建程序

创建文件 `hello.duan`：

```段言
打印 "你好，段言！"
```

### 第3步：运行

```bash
duan run hello.duan
```

或直接用 Python 运行：

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from compiler import DuanCompiler
code = open('hello.duan').read()
result = DuanCompiler().compile(code)
from code_generator_unified import UnifiedCodeGenerator
code_gen = UnifiedCodeGenerator()
py_code = code_gen.generate(result['ast'])
exec(py_code)
"
```

## CLI 命令

### 常用命令

```bash
duan run hello.duan         # 解释执行
duan compile hello.duan     # 编译为 Python
duan ast hello.duan         # 显示 AST
duan tokens hello.duan      # 显示 Token 流
```

### 后端选择

```bash
# ANTLR 后端（兼容旧语法）
duan run hello.duan --backend antlr

# SRC 后端（3.x 纯缩进语法，推荐）
duan run hello.duan --backend src
```

## 示例程序

项目包含多个示例程序：

```bash
# 运行示例
duan run examples/hello.duan
duan run examples/basic.duan
duan run examples/class_example.duan
```

示例列表：
- `examples/hello.duan` - Hello World
- `examples/basic.duan` - 基础语法
- `examples/class_example.duan` - 类示例
- `examples/hanoi.duan` - 汉诺塔算法
- `examples/calculator.duan` - 计算器

## REPL 交互式解释器

```bash
duan repl
```

## 验证安装

```bash
duan --version
duan --help
duan run examples/hello.duan
```

如果看到输出 `你好，世界！`，说明安装成功！
