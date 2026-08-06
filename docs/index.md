# 段言 (Duan) 文档

**段言**是一门基于中文的现代化编程语言，采用中文关键字，让编程更加直观易懂。

## 特性

- **中文关键字**：使用中文关键字如 `遍历`、`如果`、`那么` 等
- **双后端架构**：ANTLR 解析器 + 手写递归下降解析器
- **原生编译**：通过 LLVM IR 生成跨平台原生可执行文件
- **自举编译器**：段言语言使用自身实现编译器

## 安装

```bash
pip install duan
```

## 快速开始

```段言
打印 "你好，世界！"

函数 加一(数):
    返回 数 + 1

如果 年龄 > 18:
    打印 "成年人"
```

## 文档导航

- [快速开始](getting-started.md) - 安装和运行
- [语法规范](syntax.md) - 语言语法参考
- [标准库](stdlib.md) - 内置模块说明
- [工具链](tools.md) - CLI、调试器、LSP、AI Copilot
- [案例](examples.md) - 示例代码

## AI Copilot

算力不足时让 AI 帮你写段言代码：

- [LoRA 微调指南](superpowers/plans/2026-07-01-level6-type-annotation.md) — Qwen 模型微调训练
- [ERNIE 微调指南](superpowers/specs/2026-07-01-level5-module-exception-design.md) — ERNIE 轻量级翻译器

## 版本

当前版本：**v5.0.0-dev**
