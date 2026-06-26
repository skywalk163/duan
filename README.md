# 段言（DuanLang）编程语言

**段言**是一门基于中文的现代化编程语言，采用中文关键字，让编程更加直观易懂。

## 特性

- **中文关键字**：使用中文关键字如`遍历`、`如果`、`那么`等
- **双后端架构**：支持 ANTLR 解析器（兼容旧语法）和手写递归下降解析器（3.x 纯缩进语法）
- **原生编译**：通过 LLVM IR 生成跨平台原生可执行文件
- **自举编译器**：段言语言使用自身实现编译器（bootstrap/）

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
python -c "
import sys
sys.path.insert(0, 'src')
from compiler import DuanCompiler
code = open('hello.duan').read()
compiler = DuanCompiler()
exec(compiler.compile(code).get('ast', {}))
"
```

或使用内置解释器：
```bash
python -m src.compiler hello.duan
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

### 方式1：统一 CLI（推荐）

```bash
# 使用 ANTLR 后端编译
python -m cli.duan_unified project/记账.duan --target antlr -o 记账.exe

# 使用 SRC 后端编译（仅支持 3.x 语法）
python -m cli.duan_unified project/记账.duan --target src -o 记账.exe
```

### 方式2：ANTLR 专用 CLI

```bash
python antlrparser/duan_llvm.py project/你的程序.duan
```

### 方式3：Python 解释器运行

```bash
python bootstrap/bootstrap_v3_compiled.py project/你的程序.duan
```

## 项目结构

```
duan/
├── antlrparser/          # ANTLR 后端（支持 1.x/2.x/3.x 语法）
│   ├── duan_llvm.py    # LLVM 编译流程入口
│   ├── llvm_codegen.py  # LLVM IR 代码生成
│   └── *.g4             # ANTLR 语法文件
├── src/                 # 手写递归下降后端（仅支持 3.x 语法）
│   ├── lexer.py        # 词法分析器
│   ├── parser_stmt.py  # 语法分析器
│   ├── ast_nodes.py    # AST 节点定义
│   └── compiler.py     # 编译器主体（包含 AST 适配器）
├── bootstrap/           # 自举编译器（段言实现）
├── cli/                 # 命令行工具
│   └── duan_unified.py # 统一 CLI（支持 --target antlr|src）
├── project/             # 示例程序
│   └── 记账.duan       # 记账程序
├── tests/               # 测试
└── docs/                # 文档
```

## 双后端说明

| 后端 | 路径 | 支持语法 | 特点 |
|------|------|----------|------|
| ANTLR | antlrparser/ | 1.x/2.x/3.x | 功能完整，支持旧语法 |
| SRC | src/ | 3.x 纯缩进 | 轻量级，无外部依赖 |

推荐新项目使用 **3.x 纯缩进语法**，通过 SRC 后端或 ANTLR 后端编译均可。

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

- [架构设计](docs/architecture.md)
- [完整规范文档](docs/段言-完整规范文档.md)
- [API 参考](docs/API_REFERENCE.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 代码格式

项目使用中文注释和 UTF-8 编码。

## 许可证

本项目采用 MIT 许可证。
