# 段言（DuanLang）编程语言

**段言**是一门基于中文的编程语言，采用中文关键字，让编程更加直观易懂。

## ✨ 核心特性

- 🀄 **中文语法**：全中文关键字，符合中文思维习惯
- 🚀 **自举编译**：编译器本身用段言编写（bootstrap_v3.duan，95 个段落），可自举编译
- ⚡ **LLVM 原生编译**：支持编译为原生机器码（EXE），无需 Python 运行时
- 📦 **双后端架构**：Python 解释执行 + LLVM 原生编译，灵活切换
- 🔧 **丰富标准库**：数学工具、字符串工具、列表工具、JSON、CSV、文件系统等

## 📊 里程碑

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| v3.2 语法 | ✅ | 成熟稳定的中文编程语言 |
| 自举编译器 | ✅ | 用段言编写的段言编译器（62KB / 95 段） |
| LLVM 后端 | ✅ | 支持编译为原生 EXE（clang 零错误） |
| 自举编译 | ✅ | 自举编译器可通过 LLVM 编译为原生 EXE（525KB） |

## 快速开始（3 步跑通）

### 第 1 步：安装 Python

段言需要 **Python 3.10+**。检查你的版本：

```bash
python --version
# 输出应为 Python 3.10.x 或更高
```

> 没装 Python？去 [python.org](https://www.python.org/downloads/) 下载安装。
> Windows 用户安装时请勾选 **Add Python to PATH**。

### 第 2 步：安装段言

**方式 A：从源码安装（推荐，开发者适用）**

```bash
git clone https://gitcode.com/skywalk163/duan.git
cd duan
pip install -e .
```

**方式 B：从 PyPI 安装（仅使用）**

```bash
pip install duan
```

安装完成后验证：

```bash
duan --version
# 输出：段言编译器 v1.9.0
```

### 第 3 步：运行你的第一个程序

创建文件 `hello.duan`，写入以下内容：

```段言
打印 "你好，世界！"
```

运行它：

```bash
duan run hello.duan
# 输出：你好，世界！
```

就这么简单！无需安装任何额外依赖。

## 示例程序

项目自带示例文件，可以直接运行：

```bash
# 运行 Hello World 示例（阶乘、循环）
duan run examples/hello.duan

# 输出：
# 你好，世界！
# 5的阶乘是：
# 120
# 1到10的和：
# 55
# 程序运行完成！
```

## 语法入门

### 变量

```段言
定义 姓名 等于 "张三"
定义 年龄 等于 25
打印 姓名
打印 年龄
```

### 函数（段落）

```段言
段落 加法 接收 a, b：
  返回 a 加 b

打印 加法(3, 5)    # 输出：8
```

### 条件语句

```段言
定义 分数 等于 85

如果 分数 大于等于 90：
  打印 "优秀"
否则如果 分数 大于等于 60：
  打印 "及格"
否则：
  打印 "不及格"
```

### 循环

```段言
# 当循环
定义 计数 等于 0
当 计数 小于 5：
  打印 计数
  计数 等于 计数 加 1

# 遍历循环
遍历 项 于 1至5：
  打印 项
```

### 字符串

```段言
定义 名字 等于 "段言"
打印 "你好，" 加 名字 加 "！"
```

## 命令行工具

```bash
# 运行段言程序（默认使用 SRC 后端，无需额外依赖）
duan run hello.duan

# 编译为 Python 文件
duan compile hello.duan -o hello.py

# 语法检查
duan check hello.duan

# 查看 Token 流
duan tokens hello.duan

# 查看 AST
duan ast hello.duan

# 初始化新项目
duan init myproject
```

### 后端选择

段言支持多种编译后端：

| 后端 | 命令 | 说明 | 额外依赖 |
|------|------|------|---------|
| **SRC**（默认） | `duan run hello.duan` | 手写解析器，v3.2 语法，Python 解释执行 | **无** |
| ANTLR | `duan run hello.duan --backend antlr` | ANTLR 解析器，兼容模式 | `pip install antlr4-python3-runtime` |
| LLVM | `duan compile hello.duan --backend llvm-typed -o hello.exe` | 原生编译为 EXE | 安装 LLVM/Clang |

**新手建议**：直接用默认的 SRC 后端即可，无需任何额外安装。

### 编译为 EXE

如需编译为 Windows 可执行文件：

```bash
# 方式1：使用 PyInstaller（简单，但文件较大）
pip install pyinstaller
duan compile hello.duan -o hello.exe

# 方式2：使用 LLVM 原生编译（需要安装 LLVM）
duan compile hello.duan --backend llvm-typed -o hello.exe
```

## 标准库

段言提供中文标准库，位于 `stdlib/` 目录：

```段言
从 数学工具 导入 阶乘
打印 阶乘(10)
```

常用模块：数学工具、字符串工具、列表工具、JSON、CSV、文件系统、日志、日期时间等。

## 语法参考（v3.2）

| 语法 | 说明 | 示例 |
|------|------|------|
| `定义 X 等于 Y` | 变量声明 | `定义 年龄 等于 25` |
| `X 等于 Y` | 变量赋值 | `年龄 等于 26` |
| `段落 名 接收 参数：` | 函数定义 | `段落 加法 接收 a, b：` |
| `如果 条件：` | 条件语句 | `如果 年龄 大于 18：` |
| `否则如果 条件：` | 否则如果 | `否则如果 年龄 大于 12：` |
| `否则：` | 否则 | `否则：` |
| `当 条件：` | 当循环 | `当 计数 小于 10：` |
| `遍历 变量 于 列表：` | 遍历循环 | `遍历 i 于 1至10：` |
| `返回 X` | 返回值 | `返回 a 加 b` |
| `打印 X` | 打印输出 | `打印 "你好"` |
| `从 模块 导入 符号` | 从模块导入 | `从 数学工具 导入 阶乘` |
| `导入 模块` | 导入整个模块 | `导入 数学工具` |
| `导出 符号列表` | 导出符号 | `导出 加法, 减法` |
| `跳出` | 跳出循环 | `跳出` |
| `跳过` | 跳过本次循环 | `跳过` |

### 运算符

| 运算符 | 说明 |
|--------|------|
| `加` | 加法 |
| `减` | 减法 |
| `乘` | 乘法 |
| `除以` | 除法 |
| `取余` | 取模 |
| `等于` | 相等比较 |
| `不等于` | 不等比较 |
| `大于` / `小于` | 大小比较 |
| `大于等于` / `小于等于` | 带等号比较 |
| `且` / `或` / `非` | 逻辑运算 |

### 类与面向对象

```段言
类 动物：
  属性 名字
  构造 接收 名字：
    己名字 为 名字
  段落 介绍：
    打印 "我叫" 加 己名字

类 狗 继承 动物：
  段落 叫声：
    打印 "汪汪汪"

定义 小狗 等于 新建 狗("旺财")
小狗.介绍()
小狗.叫声()
```

## 项目结构

```
duan/
├── src/                 # 核心编译器（活跃维护）
│   ├── lexer.py         # 词法分析器
│   ├── parser_core.py   # 解析器核心
│   ├── parser_stmt.py   # 语句解析
│   ├── parser_expr.py   # 表达式解析
│   ├── ast_nodes_v3.py  # AST 节点定义
│   ├── code_generator.py     # Python 代码生成
│   ├── code_generator_unified.py  # 统一代码生成
│   ├── compiler.py      # 编译器主体
│   ├── llvm/            # LLVM 后端
│   │   ├── codegen_typed.py  # LLVM 代码生成（typed 模式）
│   │   └── compiler.py       # LLVM 编译入口
│   └── optimizer/       # 代码优化器
├── cli/                 # 命令行工具
│   ├── duan.py          # 主入口（duan 命令）
│   └── duanc.py         # SRC 后端入口（duanc 命令）
├── stdlib/              # 标准库（27 个模块）
├── stdlib_v3/           # v3.2 标准库
├── antlrparser/         # ANTLR 后端（可选，需安装 antlr4-python3-runtime）
├── examples/            # 示例程序
├── tests/               # 测试
│   ├── unit/            # 单元测试
│   ├── integration/     # 集成测试
│   └── e2e/            # 端到端测试
└── docs/                # 文档
```

## 开发

### 环境准备

```bash
# 克隆项目
git clone https://gitcode.com/skywalk163/duan.git
cd duan

# 安装（开发模式）
pip install -e .

# 安装开发工具（可选）
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有核心测试
python -m pytest tests/test_parser.py tests/test_lexer.py tests/test_async.py -v

# 运行单元测试
python -m pytest tests/unit/ -v

# 运行全部测试
python -m pytest tests/ -v
```

### 代码格式

项目使用 UTF-8 编码和中文注释。

## 常见问题

### Q: 运行时报 `No module named 'antlr4'`

**A:** 这是 ANTLR 后端的依赖。两种解决方案：

1. **用默认 SRC 后端**（推荐，无需额外安装）：
   ```bash
   duan run hello.duan
   ```

2. **安装 ANTLR 运行时**（如需使用 `--backend antlr`）：
   ```bash
   pip install antlr4-python3-runtime
   ```

### Q: `pip install antlr4` 报错

**A:** 正确的包名是 `antlr4-python3-runtime`，不是 `antlr4`：
```bash
pip install antlr4-python3-runtime
```

### Q: 编译为 EXE 失败

**A:** 两种方式：

1. **PyInstaller 方式**（简单）：
   ```bash
   pip install pyinstaller
   duan compile hello.duan -o hello.exe
   ```

2. **LLVM 方式**（原生编译，需安装 LLVM）：
   ```bash
   duan compile hello.duan --backend llvm-typed -o hello.exe
   ```

### Q: Python 版本要求

**A:** 段言需要 Python 3.10 或更高版本。检查版本：
```bash
python --version
```

## 文档

- [语法规范 v3.2](docs/统一语法规范_v3.2.md)
- [快速开始](docs/getting-started.md)
- [架构设计](docs/architecture.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [用户手册](docs/USER_MANUAL.md)

## 许可证

本项目采用 MIT 许可证。
