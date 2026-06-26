# 段言 (Duan) VS Code 扩展

## 功能特性

### 🎨 语法高亮
- 完整支持段言关键字（如果、则、否则、遍历等）
- 动词高亮（加、减、乘、除等算术运算）
- 字符串、注释、数字识别
- 中文标识符支持

### 💡 代码补全
- 关键字自动补全
- 动词（函数）自动补全
- 用户定义变量/函数补全
- 智能前缀匹配

### 📖 悬停提示
- 关键字说明
- 动词元数显示
- 函数签名（参数列表）
- 变量定义位置

### 🎯 跳转到定义
- 变量定义跳转
- 函数定义跳转
- 类定义跳转

### 🐛 调试支持
- 断点设置
- 单步执行
- 变量查看
- 调用栈显示

### 📝 代码片段
- 快速生成函数定义
- 条件语句模板
- 循环语句模板
- 类定义模板

## 安装

### 方法 1: 从 VSIX 安装

```bash
cd vscode-extension
npm install
npm run compile
vsce package
code --install-extension duan-language.vsix
```

### 方法 2: 开发模式

```bash
cd vscode-extension
npm install
npm run watch
# 按 F5 在新的 VS Code 窗口中打开
```

## 配置

### LSP 服务器路径

```json
{
  "duan.serverPath": "path/to/lsp/server.py"
}
```

### 调试端口

```json
{
  "duan.debugPort": 8765
}
```

## 快捷键

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| 运行当前文件 | `Ctrl+Shift+R` | 运行当前打开的段言文件 |
| 打开 REPL | `Ctrl+Shift+P` → "段言 REPL" | 打开段言交互式解释器 |

## 命令面板

- `段言: 运行当前文件` - 运行当前文件
- `段言: 打开 REPL` - 打开交互式解释器
- `段言: 重启 LSP 服务器` - 重启语言服务器

## 调试

### 启动调试

1. 打开要调试的 `.duan` 文件
2. 按 `F9` 设置断点
3. 按 `F5` 开始调试
4. 使用调试工具栏进行单步执行

### 调试配置

```json
{
  "type": "duan",
  "request": "launch",
  "program": "${file}",
  "stopOnEntry": true
}
```

## 文件关联

扩展会自动关联 `.duan` 文件：

```json
{
  "files.associations": {
    "*.duan": "duan"
  }
}
```

## 问题反馈

如遇到问题，请提交 Issue：
https://github.com/duan-lang/duan/issues

## 许可证

MIT License
