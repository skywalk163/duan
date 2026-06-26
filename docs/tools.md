# 工具链

## CLI 工具

### duan 命令

```bash
# 编译运行
duan run <file.duan>

# 编译为可执行文件
duan build <file.duan> -o output.exe

# 版本信息
duan --version

# 帮助
duan --help
```

### duan debug 调试模式

```bash
# 调试文件
duan debug <file.duan>

# 启动调试 REPL
duan debug
```

**调试命令：**

| 命令 | 说明 |
|------|------|
| `b <行号>` | 设置断点 |
| `d <行号>` | 删除断点 |
| `c` | 继续执行 |
| `n` | 单步跳过 |
| `s` | 单步进入 |
| `r` | 单步返回 |
| `p <变量>` | 打印变量 |
| `w` | 显示调用栈 |
| `l` | 显示源代码 |
| `vars` | 显示所有变量 |
| `q` | 退出调试 |

## VS Code 插件

安装 `vscode-extension/` 目录下的插件可以获得：

- **语法高亮**：段言关键字、动词、字符串等
- **代码补全**：内置函数、关键字等
- **悬停提示**：函数签名、文档
- **调试支持**：断点、单步调试

## LSP 语言服务器

段言提供 Language Server Protocol 支持：

```bash
# 启动 LSP 服务器
python -m lsp.duan_lsp

# 或通过 stdio
python -m lsp.duan_lsp --stdio
```

### 支持的功能

- ✅ 悬停提示 (Hover)
- ✅ 代码补全 (Completion)
- ✅ 跳转到定义 (Go to Definition)
- ✅ 诊断信息 (Diagnostics)
- ✅ 符号搜索 (Document Symbols)
