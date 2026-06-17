# 段言编程语言 - 示例项目

本目录包含段言编程语言的示例代码，帮助您快速学习和理解段言语言的各种特性。

## 示例列表

| 文件 | 描述 | 主要特性 |
|------|------|----------|
| [hello.duan](hello.duan) | Hello World | 基础输出 |
| [calculator.duan](calculator.duan) | 计算器 | 类定义、方法、条件语句 |
| [student_management.duan](student_management.duan) | 学生管理系统 | 类、列表操作、方法调用 |
| [module_demo.duan](module_demo.duan) | 模块使用演示 | 模块导入、标准库使用 |

## 运行示例

### 方法1: 使用命令行工具

```bash
# 运行单个示例
python duan_cli.py run examples/hello.duan

# 运行计算器示例
python duan_cli.py run examples/calculator.duan

# 运行学生管理系统
python duan_cli.py run examples/student_management.duan

# 运行模块演示（需要指定搜索路径）
python duan_cli.py run examples/module_demo.duan --path modules
```

### 方法2: 使用 Python API

```python
import sys
sys.path.insert(0, 'antlrparser')

from duan_visitor import parse_source
from duan_interpreter import Interpreter

# 读取示例文件
with open('examples/hello.duan', 'r', encoding='utf-8') as f:
    source = f.read()

# 解析并执行
module = parse_source(source)
interpreter = Interpreter()
interpreter.interpret_module(module)
```

### 方法3: 使用 REPL

```bash
# 启动 REPL
python duan_repl.py

# 在 REPL 中逐行输入代码
段言> 定义 x 等于 10。
段言> 打印(x)。
10
段言> 退出
```

## 示例详解

### 1. Hello World (hello.duan)

最简单的段言程序，演示基本的输出功能。

```段言
打印("你好，世界！")。
```

### 2. 计算器 (calculator.duan)

演示类定义、方法、条件语句等特性。

主要概念：
- 类定义 (`《计算器》类`)
- 方法定义 (`《加》方法`)
- 条件语句 (`如果...那么...否则...结束`)
- 对象实例化 (`新 计算器()`)
- 方法调用 (`计算器1之加(10)`)

### 3. 学生管理系统 (student_management.duan)

演示更复杂的类设计、列表操作和数据管理。

主要概念：
- 多属性类
- 列表操作 (`listAppend`, `listLen`)
- 循环语句 (`当...结束`)
- 多对象管理

### 4. 模块使用演示 (module_demo.duan)

演示模块系统和标准库的使用。

主要概念：
- 模块导入 (`从 math_utils 导入`)
- 标准库函数调用
- 多模块组合使用

## 创建自己的示例

1. 创建新的 `.duan` 文件
2. 编写段言代码
3. 使用命令行工具或 REPL 运行

## 提示

- 所有语句以 `。` 结尾
- 块语句以 `:` 开始，`结束。` 结尾
- 段落名和方法名使用 `《》` 包裹
- 属性和方法访问使用 `之` 连接

祝您学习愉快！