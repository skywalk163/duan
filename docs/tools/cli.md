# CLI 使用指南

## 基本用法

```bash
duan [选项] <文件>
```

## 选项

| 选项 | 说明 |
|------|------|
| `--version` | 显示版本信息 |
| `--help` | 显示帮助信息 |
| `--ast` | 输出 AST 解析树 |
| `--tokens` | 输出词法分析结果 |
| `--compile` | 编译为 Python 代码 |
| `--llvm` | 编译为 LLVM IR |
| `--check` | 仅检查语法，不执行 |
| `--format` | 格式化代码 |
| `--watch` | 监视文件变化并自动重跑 |

## 示例

```bash
# 运行文件
duan hello.duan

# 查看 AST
duan hello.duan --ast

# 编译为 Python
duan hello.duan --compile

# 语法检查
duan hello.duan --check
```

## REPL

```bash
duan
```

进入交互式 REPL 环境，支持：
- 逐行执行段言代码
- 自动补全
- 语法高亮
- 历史记录