# 段言（DuanLang）—— 中文优先的编程语言

**段言**是一门以中文为第一公民的现代化编程语言。全中文关键字、中文标准库、中文文档，让你用母语思维写代码，降低认知负担，提升开发效率。

[![Version](https://img.shields.io/badge/version-6.1.0-blue.svg)](https://github.com/skywalk163/duan)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/skywalk163/duan)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-duan-orange.svg)](https://pypi.org/project/duan/)

---

## 🚀 快速开始（3 条命令）

```bash
pip install duan                  # 安装
echo '打印 "你好，世界！"' > hello.duan  # 写代码
duan run hello.duan               # 运行
```

输出：`你好，世界！`

无需配置、无需额外依赖，装完即用。

---

## ❓ 为什么选择段言？

| 痛点 | 段言的解法 |
|------|-----------|
| **英文关键字门槛** | 全中文关键字，`设`/`如果`/`遍历`/`段落`，零英文基础也能上手 |
| **Python 运行时依赖** | 可选 LLVM 原生编译，编译为独立 EXE，无需任何运行时 |
| **类型安全缺失** | 三级类型检查 + HM 全局类型推断，编译期捕获类型错误 |
| **C 互操作复杂** | `@C` 语法标记 + 自动 FFI 生成，调用 C 库像调用本地函数 |
| **新手入门困难** | 交互式教程（`--repl`/`--step`）、中文错误提示、AI Copilot 辅助 |
| **生态割裂** | 内置包管理器（duanpub）、Web 框架、LSP、DAP 调试器，开箱即用 |

---

## 📊 特性对比：段言 vs Python

| 维度 | 段言 | Python |
|------|------|--------|
| **关键字** | 全中文 | 英文 |
| **类型系统** | 三级类型检查 + HM 全局推断 | 可选类型注解（PEP 484） |
| **原生编译** | ✅ LLVM 后端，编译为独立 EXE | ❌ 需 PyInstaller/Nuitka |
| **C FFI** | `@C` 语法标记，自动绑定 | `ctypes`/`cffi` 手动绑定 |
| **包管理器** | 内置（duanpub） | pip + venv（需额外安装） |
| **Web 框架** | 内置 Web 框架 | 需 Flask/FastAPI 等第三方库 |
| **异步编程** | `异步`/`等待` 中文关键字 | `async`/`await` 英文关键字 |
| **模式匹配** | 结构化匹配 + 守卫条件 + 解构赋值 | 3.10+ 匹配（有限） |
| **异常处理** | 中文异常类型层级 + 异常链 | 英文异常类型 |
| **LSP/DAP** | 内置支持 | 需安装 pylance/pyright 等扩展 |
| **中文文档** | 完整中文文档 + 中文教程 | 中文文档多为社区翻译 |
| **AI 辅助** | 内置 AI Copilot + 微调模型 | 需第三方工具 |

---

## 💡 示例

### 一句话说清楚

```段言
打印 "你好，世界！"
```

### 经典算法：二分查找

```段言
段落 二分查找 接收 数组, 目标：
    设 左 为 0
    设 右 为 数组.长度 减 1
    
    当 左 小于等于 右：
        设 中 为 (左 加 右) 除以 2 取整
        如果 数组[中] 等于 目标：
            返回 中
        否则如果 数组[中] 小于 目标：
            设 左 为 中 加 1
        否则：
            设 右 为 中 减 1
    
    返回 -1

设 结果 为 二分查找([1, 3, 5, 7, 9, 11], 7)
打印 结果  # 输出：3
```

### Web 应用

```段言
从 Web框架 导入 创建应用, 路由, 启动

设 应用 为 创建应用()

@路由(应用, "/", "GET")
段落 首页 接收 请求：
    返回 "欢迎使用段言！"

@路由(应用, "/api/用户/{id}", "GET")
段落 获取用户 接收 请求, id：
    返回 {"用户ID": id, "姓名": "张三"}

启动(应用, 端口=8080)
```

### 更多示例

| 项目 | 类型 | 说明 |
|------|------|------|
| CLI 待办管理器 | CLI | 完整 CRUD，命令行界面 |
| 博客系统 | Web | 基于 Web 框架的简易博客 |
| 数据管道 | 数据处理 | CSV→JSON→SQLite 数据流水线 |
| 贪吃蛇游戏 | 终端游戏 | 终端贪吃蛇，方向控制 |
| 算法库 20+ | 算法 | 排序/搜索/图/动态规划 |

运行所有示例：`duan run examples/hello.duan`

---

## 🌍 社区

| 渠道 | 地址 |
|------|------|
| 💬 **GitHub Discussions** | [讨论区](https://github.com/skywalk163/duan/discussions) — 提问、分享、交流 |
| 🐛 **问题反馈** | [Issues](https://github.com/skywalk163/duan/issues) — 报告 Bug 与建议 |
| 📖 **文档站** | [docs/](docs/index.md) — 完整文档与教程 |
| 📝 **技术博客** | [docs/blog/](docs/blog/) — 版本发布、技术解析 |
| 🤖 **AI 模型** | [Ollama: airoot/duan-translator](https://ollama.com/airoot/duan-translator) — 段言代码生成模型 |
| 📦 **包注册中心** | [duanpub](https://github.com/skywalk163/duan) — 社区包索引 |

---

## 📚 教程

- [**30 分钟入门段言**](docs/30分钟入门段言.md) — 零基础入门
- [**端到端实战教程**](docs/端到端实战教程.md) — 从零构建天气查询程序
- [**入门教程**](docs/tutorials/入门教程.md) — 面向初学者的交互式教程
- [**进阶教程**](docs/tutorials/进阶教程.md) — 面向有经验的开发者

---

## 🔧 命令行工具

```bash
duan run hello.duan            # 运行段言程序
duan compile hello.duan -o hello.py   # 编译为 Python
duan check hello.duan          # 语法检查
duan type-check hello.duan --level 变量  # 类型检查
duan pkg init myproject        # 初始化新项目
duan pkg search 关键词 --remote # 搜索社区包
duan pkg publish               # 发布包
duan ai generate "二分查找"    # AI 生成代码
duan ai fix hello.duan "语法错误"  # AI 修复代码
```

---

## 📖 文档

- [语法规范 v3.2](docs/统一语法规范_v3.2.md)
- [快速开始](docs/getting-started.md)
- [架构设计](docs/architecture.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [用户手册](docs/USER_MANUAL.md)
- [工具链](docs/tools.md)
- [API 参考](docs/API_REFERENCE.md)
- [标准库文档](docs/stdlib.md)
- [性能基准 vs Python](docs/性能基准_vs_Python.md)
- [迁移指南 v5→v6](docs/迁移指南_v5到v6.md)

---

## 📋 项目状态

| 里程碑 | 状态 |
|--------|------|
| v6.1 正式发布 | ✅ 生态建设全面升级 |
| v6.0 正式发布 | ✅ 生产就绪 |
| 自举编译器 | ✅ 62KB / 95 函数，可自举编译 |
| LLVM 后端 | ✅ 原生 EXE 编译 + 增量编译加速 |
| Web 框架 | ✅ 50+ 测试通过 |
| 测试覆盖 | ✅ 全量回归测试通过 |
| 包注册中心 | ✅ 全链路发布→搜索→安装 + Web 界面 |
| 英文文档 | ✅ 覆盖 v6.0 全部特性 |
| AI Copilot | ✅ 离线轻量模型 + 多语言代码转换 |

---

## 许可证

本项目采用 MIT 许可证。