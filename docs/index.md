# 段言 (Duan) 文档

> **当前版本：** v6.0
> **最后更新：** 2026-08-07

**段言**是一门基于中文的现代化编程语言，采用中文关键字，让编程更加直观易懂。

## 特性

- 🀄 **中文语法**：全中文关键字，符合中文思维习惯
- 🚀 **自举编译**：编译器本身用段言编写，可自举编译
- ⚡ **LLVM 原生编译**：支持编译为原生机器码（EXE），无需 Python 运行时
- 📦 **双后端架构**：Python 解释执行 + LLVM 原生编译，灵活切换
- 🔧 **丰富标准库**：60+ 标准库模块，覆盖数学、文件、JSON、HTTP、加密、FFI 等
- 🔗 **C FFI 绑定**：支持调用 C 动态库，完整的 C 语言互操作
- 🧠 **HM 类型推断**：Hindley-Milner 全局类型推断，支持泛型
- 🛡️ **空安全系统**：可空类型注解与安全展开
- 📦 **duanpub 包管理器**：包索引、安装、依赖管理、发布流程
- 🤖 **AI 工具链 2.0**：AI Copilot 代码生成、微调模型、语法速查卡
- 💻 **完整 LSP 支持**：悬停提示、代码补全、跳转定义、诊断、重构、格式化
- 🐛 **DAP 调试器**：VS Code 断点调试支持
- 📚 **交互式教程**：10 节完整教程，支持 `--repl` 和 `--step` 模式

## 安装

```bash
pip install duan
```

## 快速开始

```段言
打印 "你好，世界！"

段落 加法 接收 甲, 乙：
    返回 甲 + 乙

设 结果 为 加法(3, 5)
打印 结果  # 输出：8
```

## 文档导航

### 入门指南

- [快速开始](getting-started.md) — 安装和运行
- [30 分钟入门段言](30分钟入门段言.md) — 零基础入门教程
- [语法规范](syntax.md) — 语言语法参考
- [用户手册](USER_MANUAL.md) — 完整用户手册

### 核心文档

- [标准库](stdlib.md) — 内置模块说明
- [工具链](tools.md) — CLI、调试器、LSP、AI Copilot
- [案例](examples.md) — 示例代码
- [架构设计](architecture.md) — 编译器架构详解
- [编译器内部设计](编译器内部设计.md) — 编译器管线与实现
- [包管理器使用指南](包管理器使用指南.md) — duanpub 包管理
- [LLVM 后端设计](llvm_backend_design.md) — 原生编译实现

### 博客

- [段言 v6.0 正式发布](blog/段言v6.0正式发布.md) — 中文编程语言的新里程碑
- [用段言构建 Web 应用](blog/用段言构建Web应用.md) — 从零到一的实战指南
- [段言自举编译器架构解析](blog/段言自举编译器架构解析.md) — 自举编译器的实现之路
- [段言入门指南](blog/段言入门指南.md) — 用中文自然语言编程
- [段言编译器架构解析](blog/段言编译器架构解析.md) — 从中文到机器码
- [中文编程语言的未来](blog/中文编程语言的未来.md) — 设计哲学与愿景

### 项目规划

- [项目路线图](ROADMAP.md) — 版本规划与愿景
- [开发指南](DEVELOPMENT_GUIDE.md) — 开发者参与指南
- [API 参考](API_REFERENCE.md) — 完整 API 文档

### 视频教程

- [视频教程脚本](video_scripts/) — 视频教程脚本

## 版本

当前版本：**v6.0**

## 社区

- [社区入口](community/README.md) — 社区渠道、交流方式和项目资源
- [反馈收集指南](community/feedback.md) — 如何提交有价值的反馈

## 如何贡献

- 💬 **讨论**：在 [GitHub Discussions](https://github.com/skywalk163/duan/discussions) 发起讨论
- 🐛 **报告 Bug**：提交 [Bug Report](https://github.com/skywalk163/duan/issues/new?template=bug_report.md)
- 💡 **建议功能**：提交 [Feature Request](https://github.com/skywalk163/duan/issues/new?template=feature_request.md)
- 🔧 **贡献代码**：参考 [CONTRIBUTING.md](../CONTRIBUTING.md) 和 [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)