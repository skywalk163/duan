# 段言（DuanLang）编程语言

**段言**是一门基于中文的现代化编程语言，采用中文关键字，让编程更加直观易懂。

## 特性

- **中文关键字**：使用中文关键字如`遍历`、`如果`、`那么`等
- **纯缩进语法**：v3.x 中文关键字，类似 Python 的缩进风格，无"结束"关键字
- **统一编译器**：手写递归下降解析器 + Python 代码生成
- **LLVM 后端**：支持原生编译为 EXE，typed 模式性能优异
- **标准库**：23 个中文命名模块（日志、表格、CSV、JSON 等）
- **泛型系统**：泛型函数、泛型类、泛型方法
- **模块系统**：导入/导出、包管理、跨模块继承
- **类与对象**：面向对象编程，支持继承、构造函数
- **异常处理**：抛出、尝试、捕获、最终
- **开发工具链**：REPL、调试器、LSP 语言服务器、VS Code 插件
- **性能优化**：常量折叠、死代码消除、循环不变量外提

## 安装

```bash
# 方式1: 从 PyPI 安装（推荐）
pip install duan

# 方式2: 从源码安装
git clone https://github.com/skywalk163/duan.git
cd duan
pip install -e .
```

## 快速开始

### 3 步跑起来

**第1步：安装**
```bash
pip install duan
```

**第2步：创建程序**
```段言
# hello.duan
打印 "你好，段言！"
```

**第3步：运行**
```bash
duan run hello.duan
```

### Hello World

```段言
打印 "你好，世界！"
```

### 变量和函数

```段言
段落 加一 接收 数：
    返回 数 加 1
```

### 条件语句

```段言
如果 年龄 大于 18 那么：
    打印 "成年人"
否则：
    打印 "未成年人"
```

### 循环

```段言
遍历 项 在 列表：
    打印 项
```

## 编译运行

```bash
# 解释执行（推荐）
duan run hello.duan

# 编译为 Python 文件
duan compile hello.duan -o hello.py

# 编译为 Windows EXE（需安装 pyinstaller）
pip install pyinstaller
duan compile hello.duan -o hello.exe

# LLVM 原生编译（需安装 clang/LLVM）
duan compile hello.duan --backend llvm-typed -o hello.exe
```

后端选择：
```bash
# SRC 后端（3.x 纯缩进语法，推荐，Python 解释执行）
duan run hello.duan --backend src

# ANTLR 后端（兼容模式，支持 v3 纯缩进语法）
duan run hello.duan --backend antlr

# LLVM string 模式（原生编译，字符串类型系统）
duan compile hello.duan --backend llvm -o hello.exe

# LLVM typed 模式（原生编译，DuanValue 类型系统，推荐）
duan compile hello.duan --backend llvm-typed -o hello.exe
```

## 项目结构

```
duan/
├── src/                 # 核心编译器
│   ├── lexer.py        # 词法分析器
│   ├── parser_stmt.py  # 语法分析器
│   ├── ast_nodes.py    # AST 节点定义
│   ├── compiler.py     # 编译器主体
│   ├── llvm/           # LLVM 后端
│   │   ├── codegen.py       # LLVM 代码生成（string 模式）
│   │   ├── codegen_typed.py # LLVM 代码生成（typed 模式）
│   │   ├── runtime_typed.c  # typed 模式运行时库
│   │   ├── compiler.py      # LLVM 编译入口
│   │   └── core.py          # 代码生成核心
│   ├── optimizer/      # 代码优化器（常量折叠、死代码消除等）
│   └── ...
├── cli/                 # 命令行工具
│   └── duan.py         # CLI 入口
├── stdlib/              # 标准库（23 个模块）
│   ├── 日志.duan/py
│   ├── 表格.duan/py
│   ├── JSON.duan/py
│   └── ...
├── antlrparser/         # ANTLR 后端
│   ├── indent_preprocessor.py  # v3 缩进语法预处理
│   └── ...
├── lsp/                 # LSP 语言服务器
├── benchmarks/          # 性能基准测试
├── examples/            # 示例程序
├── tests/               # 测试（unit / integration / e2e）
└── docs/                # 文档
```

## 编译器架构

| 组件 | 说明 |
|------|------|
| 词法分析 | 手写词法分析器，支持 Unicode 中文关键字 |
| 语法分析 | 递归下降解析器，v3.x 纯缩进语法 |
| 类型检查 | Hindley-Milner 全局类型推断 |
| 代码生成（Python） | Python 代码生成（类型擦除策略） |
| 代码生成（LLVM） | LLVM IR 生成，DuanValue 类型化后端 |
| 运行时（C） | typed 模式运行时库，提供基础操作实现 |
| 优化器 | 常量折叠、死代码消除、循环不变量外提 |

## 语法参考（3.x）

| 段言 | 说明 |
|------|------|
| `定义 X 等于 Y` 或 `X 等于 Y` | 变量声明 |
| `段落 名 接收 参数：` | 函数定义 |
| `如果 条件 那么：` | 条件语句 |
| `遍历 X 在 列表：` | 遍历循环 |
| `当 条件：` | 当循环 |
| `返回 X` | 返回值 |
| `打印 X` | 打印输出 |
| `类 名称：` | 类定义 |
| `类 子类 继承 父类：` | 类继承 |
| `属性 名称` | 类属性声明 |
| `构造 接收 参数：` | 构造函数 |
| `己属性名` | 访问自身属性（对应 self.属性名） |
| `新建 类名(参数)` | 实例化对象 |
| `从 模块 导入 符号` | 从模块导入 |
| `导入 模块` | 导入整个模块 |
| `导出 符号列表` | 导出符号 |

### 类示例

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

设 小狗 为 新建 狗("旺财")
小狗.介绍()
小狗.叫声()
```

### 模块示例

```段言
// math_utils.duan
段落 加法 接收 a, b：
  返回 a 加 b
导出 加法

// main.duan
从 math_utils 导入 加法
打印 加法(3, 5)
```

## 文档

更多文档请参考：

- [快速开始](docs/getting-started.md)
- [语法参考](docs/syntax.md)
- [架构设计](docs/architecture.md)
- [标准库](docs/stdlib.md)
- [完整语法规范 v3.1](docs/统一语法规范_v3.1.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [API 参考](docs/API_REFERENCE.md)
- [工具链](docs/tools.md)

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 代码格式

项目使用中文注释和 UTF-8 编码。

## 许可证

本项目采用 MIT 许可证。
