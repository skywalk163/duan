# 段言（Duan）开发指南

## 项目概述

段言（Duan）是一款以中文为基础的编程语言，旨在为中文用户提供更自然、更直观的编程体验。

## 目录结构

```
duan/
├── antlrparser/          # ANTLR4 解析器实现
│   ├── duan_parser/      # 生成的解析器代码
│   ├── runtime/          # C 语言运行时库
│   ├── scripts/          # 构建脚本
│   ├── test/             # 测试用例
│   ├── web_playground/   # Web 在线编辑器
│   └── self_hosted/      # 自举测试代码
├── bootstrap/            # 自举相关代码
├── docs/                 # 文档
├── examples/             # 示例代码
├── src/                  # 核心源代码
└── tests/                # 测试套件
```

## 开发环境设置

### 1. 安装 Python

确保安装 Python 3.10 或更高版本：

```bash
python --version
```

### 2. 创建虚拟环境

```bash
cd duan
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements-dev.txt
```

### 4. 安装 LLVM（编译支持）

下载并安装 LLVM 16.0+：
- Windows: https://github.com/llvm/llvm-project/releases
- macOS: `brew install llvm`
- Linux: `sudo apt install llvm`

设置环境变量（Windows）：
```bash
set LLVM_BIN=E:\Program Files\LLVM\bin
```

## 生成解析器

修改语法文件 `antlrparser/DuanLang.g4` 后，运行生成脚本：

```bash
cd antlrparser
.\scripts\generate.ps1
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_parser.py -v

# 运行性能测试
python tests/performance_benchmark.py
```

## 使用命令行工具

```bash
# 解析并显示 AST
python antlrparser/duan_cli.py parse test.duan

# 解释执行
python antlrparser/duan_cli.py run test.duan

# 编译为可执行文件
python antlrparser/duan_cli.py compile test.duan -o output
```

## 代码规范

### Python 代码规范

- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 使用 `isort` 进行导入排序

```bash
black antlrparser/
flake8 antlrparser/
isort antlrparser/
```

### 命名规范

- Python 文件：小写加下划线，如 `duan_ast.py`
- 类名：大驼峰，如 `DuanVisitor`
- 函数/方法：小写加下划线，如 `visit_class_def`
- 变量：小写加下划线，如 `segment_name`

## 调试技巧

### 1. 调试解析器

```python
from antlrparser.duan_visitor import parse_source

source = """
定义 x 等于 10。
打印(x)。
"""

module = parse_source(source)
print(module)
```

### 2. 调试解释器

```python
from antlrparser.duan_interpreter import run_source

result = run_source("定义 x 等于 5 加 3。打印(x)。")
print(result.get_output())
```

### 3. 调试编译器

```python
from antlrparser.duan_llvm import LLVMCodeGen, parse_source

module = parse_source("打印(100)。")
gen = LLVMCodeGen()
ir = gen.generate(module)
print(ir)
```

## 开发流程

1. **修改语法** → 更新 `DuanLang.g4`
2. **生成解析器** → 运行 `scripts/generate.ps1`
3. **更新 AST** → 修改 `duan_ast.py`
4. **更新访问器** → 修改 `duan_visitor.py`
5. **更新解释器** → 修改 `duan_interpreter.py`
6. **更新编译器** → 修改 `duan_llvm.py`
7. **编写测试** → 在 `tests/` 或 `antlrparser/test/` 添加测试
8. **运行测试** → `pytest`

## 发布流程

```bash
# 构建包
python -m build

# 发布到 PyPI
twine upload dist/*
```

## 常见问题

### Q: 解析器生成失败

**A:** 确保已安装 `antlr4-tools`：
```bash
pip install antlr4-tools
```

### Q: 编译失败

**A:** 检查 LLVM 路径是否正确配置，确保 `clang.exe` 可访问。

### Q: 中文显示乱码

**A:** 确保终端编码为 UTF-8：
```bash
chcp 65001  # Windows
export LC_ALL=en_US.UTF-8  # Linux/macOS
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件