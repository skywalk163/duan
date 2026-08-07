# 段言（DuanLang）编程语言

**段言**是一门基于中文的编程语言，采用中文关键字，让编程更加直观易懂。

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-2129%20passed-brightgreen.svg)](https://github.com/skywalk163/duan)
[![Version](https://img.shields.io/badge/version-6.0.0-blue.svg)](https://github.com/skywalk163/duan)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-duan-orange.svg)](https://pypi.org/project/duan/)

## ✨ 核心特性

- 🀄 **中文语法**：全中文关键字，符合中文思维习惯
- 🚀 **自举编译**：编译器本身用段言编写（bootstrap_v3.duan，95 个函数），可自举编译
- ⚡ **LLVM 原生编译**：支持编译为原生机器码（EXE），无需 Python 运行时
- 📦 **双后端架构**：Python 解释执行 + LLVM 原生编译，灵活切换
- 🔧 **丰富标准库**：60+ 模块，涵盖数学、字符串、文件、网络、加密、Web 开发等
- 🔗 **C FFI 绑定**：支持调用 C 动态库，枚举/联合体/变长参数/回调/位域/函数指针
- 🧩 **异常处理**：完整的 try-catch-finally 异常机制，支持异常类型层级和异常链
- 🔄 **模式匹配**：结构化模式匹配、解构赋值、守卫条件
- ⚡ **异步/协程**：async/await 关键字，事件循环集成，异步 I/O
- 🎨 **装饰器**：@decorator 语法糖，装饰器链，参数化装饰器
- 📋 **上下文管理器**：with 语句，资源自动管理，异步上下文管理器
- 🌐 **Web 框架**：内置 Web 框架，路由/中间件/模板引擎/请求处理
- 🤖 **AI Copilot**：LoRA 微调模型辅助生成段言代码

## 里程碑

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| v6.0 正式发布 | ✅ | 生产就绪，社区启航 |
| 自举编译器 | ✅ | 用段言编写的段言编译器（62KB / 95 函数） |
| LLVM 后端 | ✅ | 支持编译为原生 EXE（clang 零错误） |
| Web 框架 | ✅ | 路由/中间件/模板引擎/请求处理 50+ 测试通过 |
| 示例项目 | ✅ | 30+ 示例，5 个完整应用（CLI/博客/数据管道/游戏/算法） |
| 包注册中心 | ✅ | 全链路包发布→搜索→安装 |
| 英文文档 | ✅ | 覆盖 v6.0 全部特性 |
| AI Copilot | ✅ | 算力不足场景下的段言代码生成工具链 + LoRA 微调 |
| C FFI 绑定 | ✅ | 四阶段实现 + @C 语法标记 |

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
git clone https://github.com/skywalk163/duan.git
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
# 输出：段言编译器 v6.0.0
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
设 姓名 为 "张三"
设 年龄 为 25
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
设 分数 为 85

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
设 计数 为 0
当 计数 小于 5：
    打印 计数
    设 计数 为 计数 加 1

# 遍历循环
遍历 项 于 1至5：
    打印 项
```

### 异常处理

```段言
尝试：
    设 结果 为 10 除以 0
捕获 错误 为 e：
    打印 "发生错误：" + 转字符串(e)
最终：
    打印 "清理完成"
```

### 异步编程

```段言
异步 段落 获取数据 接收 网址：
    设 响应 为 等待 请求(网址)
    返回 响应

异步 段落 主程序：
    设 数据 为 等待 获取数据("https://api.example.com")
    打印 数据

等待 主程序()
```

### 装饰器

```段言
@日志
段落 计算 接收 甲, 乙：
    返回 甲 加 乙
```

### 上下文管理器

```段言
使用 打开("文件.txt", "读取") 为 文件：
    设 内容 为 文件.读取()
    打印 内容
```

## 📖 教程

- [**30 分钟入门段言**](docs/30分钟入门段言.md) — 零基础入门教程
- [**端到端实战教程**](docs/端到端实战教程.md) — 从零构建天气查询程序
- [**入门教程**](docs/tutorials/入门教程.md) — 面向初学者的交互式教程
- [**进阶教程**](docs/tutorials/进阶教程.md) — 面向有经验的开发者的进阶教程

## 命令行工具

```bash
# 运行段言程序（默认使用 SRC 后端，无需额外依赖）
duan run hello.duan

# 编译为 Python 文件
duan compile hello.duan -o hello.py

# 语法检查
duan check hello.duan

# 类型检查（三级：签名/变量/表达式）
duan check hello.duan --type-check 表达式

# 独立类型检查
duan type-check hello.duan --level 变量

# 查看 Token 流
duan tokens hello.duan

# 查看 AST
duan ast hello.duan

# 初始化新项目
duan init myproject
```

### 包管理

```bash
# 初始化新包（创建 package.toml 与 主.duan）
duan pkg init myproject

# 编译项目
duan pkg -p myproject build

# 运行项目
duan pkg -p myproject run

# LLVM 原生编译
duan pkg -p myproject native -o output.exe

# 搜索包
duan pkg search 关键词

# 远程搜索包
duan pkg search 关键词 --remote

# 查看包详情
duan pkg info 包名

# 更新包
duan pkg update 包名

# 发布包
duan pkg publish
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

## Web 框架

段言内置 Web 框架（duanpub/Web框架），支持完整的 Web 开发：

```段言
从 Web框架 导入 创建应用, 路由, 启动

设 应用 为 创建应用()

@路由(应用, "/", "GET")
段落 首页 接收 请求：
    返回 "欢迎使用段言！"

@路由(应用, "/api/数据", "GET")
段落 获取数据 接收 请求：
    返回 {"消息": "你好，世界！"}

启动(应用, 端口=8080)
```

### 示例项目

段言提供 30+ 示例程序，包含 5 个完整应用：

| 项目 | 类型 | 说明 |
|------|------|------|
| CLI 待办管理器 | CLI | 完整 CRUD，命令行界面 |
| 博客系统 | Web | 基于 Web 框架的简易博客 |
| 数据管道 | 数据处理 | CSV→JSON→SQLite 数据流水线 |
| 贪吃蛇游戏 | 终端游戏 | 终端贪吃蛇，方向控制 |
| 算法库 20+ | 算法 | 排序/搜索/图/动态规划 |

## AI Copilot（算力不足时让 AI 写段言代码）

段言提供完整的 AI 辅助工具链，即使只有小模型（7B 以下），也能帮你写出正确的段言代码。

> **模型已上线**：训练好的段言翻译器模型已发布到 Ollama 官网，可直接拉取使用：
> ```bash
> ollama pull airoot/duan-translator
> ```
> 模型主页：[https://ollama.com/airoot/duan-translator](https://ollama.com/airoot/duan-translator)

### 核心思路

```
用户需求 → AI 生成 Python → 微调模型翻译为段言 → duan ai check 验证
```

### 使用方式

```bash
# 一键生成段言代码
duan ai generate "写一个二分查找函数"
duan ai generate "排序算法" --model-size small
duan ai generate "文件读写" --model-size large

# 修复出错的段言代码
duan ai fix hello.duan "第3行语法错误"

# 查看语法速查卡（复制给 AI 当参考）
duan ai card

# 查看代码片段模板
duan ai snippets

# 后端感知检测
duan ai check hello.duan
```

## 标准库

段言提供丰富的中文标准库，位于 `stdlib/` 目录，包含 **14个阶段**、**60+个模块**：

```段言
从 数学 导入 阶乘
打印 阶乘(10)
```

### 核心模块

| 模块 | 说明 |
|------|------|
| 数学 | 绝对值、三角函数、阶乘、统计函数 |
| 字符串处理 | 分割、拼接、替换、查找、截取 |
| 文件系统 | 读写文件、目录操作、路径处理 |
| 日期时间 | 日期解析/格式化、时区转换 |
| JSON | 解析与序列化 |
| 加密 | 对称/非对称加密、哈希 |
| 正则表达式 | 正则匹配、捕获、替换 |
| 网络请求 | HTTP 请求（GET/POST） |
| 线程 | 线程创建与管理、锁、信号量 |
| 装饰器 | 缓存、重试、计时、日志等 11 种装饰器 |
| 上下文管理器 | 临时文件、资源管理等 13 种上下文管理器 |

### Web 框架

| 模块 | 说明 |
|------|------|
| HTTP客户端 | GET/POST、Cookie、重定向 |
| HTTP服务端 | 路由、中间件、静态文件 |
| Web框架 | 完整 Web 框架（路由/中间件/模板/请求处理） |
| WebSocket | 长连接、双向通信 |

### duanpub 生态

段言拥有 53+ 桥接模块、109 包索引，涵盖：

- 开发工具（代码格式化、构建工具、静态分析）
- 网络通信（HTTP、WebSocket、RPC、消息队列）
- 数据库（SQLite、NoSQL 连接器、Redis 绑定）
- 安全加密（JWT、OAuth、数字签名、证书）
- 媒体处理（图像处理、音频处理、视频处理）
- 数据科学（科学计算、统计分析、数据可视化）

## 语法参考（v6.0）

| 语法 | 说明 | 示例 |
|------|------|------|
| `设 X 为 Y` | 变量声明 | `设 年龄 为 25` |
| `段落 名 接收 参数：` | 函数定义 | `段落 加法 接收 a, b：` |
| `如果 条件：` | 条件语句 | `如果 年龄 大于 18：` |
| `遍历 变量 于 列表：` | 遍历循环 | `遍历 i 于 1至10：` |
| `当 条件：` | 当循环 | `当 计数 小于 10：` |
| `尝试：...捕获 错误 为 e：` | 异常处理 | `尝试：捕获 错误 为 e：` |
| `异步 段落 名 接收 参数：` | 异步函数 | `异步 段落 获取 接收 网址：` |
| `@装饰器` | 装饰器 | `@日志` |
| `使用 表达式 为 变量：` | 上下文管理器 | `使用 文件 为 f：` |
| `返回 X` | 返回值 | `返回 a + b` |
| `打印 X` | 打印输出 | `打印 "你好"` |
| `从 模块 导入 符号` | 从模块导入 | `从 数学 导入 阶乘` |
| `导入 模块` | 导入整个模块 | `导入 数学` |

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
│   ├── compiler.py      # 编译器主体
│   ├── type_checker.py  # 三级类型检查器
│   ├── type_inferencer.py   # HM 类型推断
│   ├── package_manager.py   # 包管理器
│   ├── module_resolver.py   # 模块解析器
│   ├── llvm/            # LLVM 后端
│   └── optimizer/       # 代码优化器
├── cli/                 # 命令行工具
├── stdlib/              # 标准库（60+ 模块）
│   ├── duanpub/         # duanpub 桥接模块（53+ 包）
│   └── ...
├── lsp/                 # LSP 语言服务器
├── bootstrap/           # 自举编译器
├── contrib/             # 社区贡献库
├── examples/            # 示例程序（30+）
├── tests/               # 测试（2129+ 通过）
├── playground/          # Web Playground
└── docs/                # 文档
```

## 开发

### 环境准备

```bash
# 克隆项目
git clone https://github.com/skywalk163/duan.git
cd duan

# 安装（开发模式）
pip install -e .

# 安装开发工具（可选）
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有核心测试
python -m pytest tests/ -q
```

### 代码格式

项目使用 UTF-8 编码和中文注释。

## 迁移指南

从 v5.x 迁移到 v6.0？请参阅 [迁移指南 v5→v6](docs/迁移指南_v5到v6.md)。

## 文档

- [语法规范 v3.2](docs/统一语法规范_v3.2.md)
- [快速开始](docs/getting-started.md)
- [架构设计](docs/architecture.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [用户手册](docs/USER_MANUAL.md)
- [工具链](docs/tools.md)（CLI、调试器、LSP、AI Copilot）
- [API 参考](docs/API_REFERENCE.md)
- [标准库文档](docs/stdlib.md)
- [安全审计报告](docs/security_audit_report.md)
- [性能基准 vs Python](docs/性能基准_vs_Python.md)

## 许可证

本项目采用 MIT 许可证。