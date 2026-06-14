# 段言 (DuanLang)

**段言**是一种面向中文用户的编程语言，采用中文关键字和自然语言风格的语法设计，让中文用户能够更自然地学习和使用编程。

## 特性

- 🀄 **中文语法** - 使用中文关键字（`设`、`段落`、`如果`、`当`、`类` 等），读起来像中文
- 📝 **无空格分词** - 支持无空格连续书写，自动识别标识符和关键字边界
- 🔄 **迭代器驱动** - 元数驱动解析（动词声明参数数量），支持无括号函数调用
- 🧩 **面向对象** - 支持类、继承、属性、方法等完整面向对象特性
- 📦 **模块系统** - 支持导入/导出、依赖图构建、循环依赖检测
- 🔥 **双后端** - Python 后端（解释执行）和 LLVM 后端（编译为原生可执行文件）
- 🎯 **自举探索** - 包含自举编译器的实验性实现
- 🧪 **完整测试** - 33 项边界测试全部通过（变量、函数、条件、循环、递归、类、继承）
- 🔥 **健壮错误处理** - 结构化错误提示（`LexerError`/`ParseError`/`SemanticError`/`CodeGenError`），带行号、列号和上下文信息

## 快速开始

### 安装依赖

```bash
pip install antlr4-python3-runtime
```

### 运行示例

```bash
python cli/duanc.py examples/basic.duan --run
```

或使用 Python 后端：

```python
from src.duan_parser_v3 import DuanParser
from src.code_generator import PythonCodeGenerator

source = """
设 问候 为 "你好，世界！"。
打印 问候。
"""

parser = DuanParser()
module = parser.parse(source)
generator = PythonCodeGenerator()
python_code = generator.generate(module)
exec(python_code)
```

输出：
```
你好，世界！
```

## 语法示例

### 变量声明

支持两种语法风格：

```段言
# v1.6 语法：段落式（推荐）
设 年龄 为 25。
设 姓名 为 "张三"。
设 身高 为 1.75。

# v1.5 语法：定义式（向下兼容）
定义 年龄 等于 25。
定义 姓名 等于 "张三"。
```

### 段落定义（函数）

```段言
段落 平方 接收 数值：
  返回 数值 乘 数值。
结束。

段落 求和 接收 甲, 乙：
  返回 甲 加 乙。
结束。

段落 问候：
  打印 "你好，世界！"。
结束。
```

### 条件语句

```段言
设 分数 为 85。
如果 分数 大于等于 60：
  打印 "及格"。
否则：
  打印 "不及格"。
结束。
```

### 循环

```段言
# 当循环
设 计数 为 0。
当 计数 小于 5：
  打印 计数。
  设 计数 为 计数 加 1。
结束。

# 遍历循环
设 水果 为 ["苹果", "香蕉", "橙子"]。
遍历 水果项 之 水果：
  打印 水果项。
结束。
```

### 类和对象

```段言
类 动物：
  段落 叫声：
    打印 "动物叫声"。
  结束。
结束。

类 狗 继承 动物：
  属性 名称。
  属性 品种。
  
  构造 接收 名称, 品种：
    己名称 为 名称。
    己品种 为 品种。
  结束。
  
  段落 叫声：
    打印 "汪汪汪"。
  结束。
  
  段落 介绍：
    打印 "我是"。
    打印 己名称。
  结束。
结束。

设 小狗 为 新建 狗 "旺财", "金毛"。
小狗.叫声()。
小狗.介绍()。
```

### 运算符

```段言
# 算术运算符
甲 加 乙     # 加法
甲 减 乙     # 减法
甲 乘 乙     # 乘法
甲 除 乙     # 除法

# 比较运算符
甲 大于 乙       # >
甲 小于 乙       # <
甲 等于 乙       # ==
甲 不等于 乙     # !=
甲 大于等于 乙   # >=
甲 小于等于 乙   # <=
```

### 特殊值

```段言
定义 是 等于 真。    # True
定义 否 等于 假。    # False
定义 无 等于 空。    # None
```

## 项目结构

```
duan/
├── src/                  # 核心编译器源代码
│   ├── lexer.py          # 词法分析器（三层分词机制）
│   ├── tokens.py         # Token 类型定义
│   ├── keywords.py       # 关键字和动词元数定义
│   ├── duan_parser_v3.py # 递归下降语法解析器（含30+AST节点）
│   ├── ast_nodes.py      # AST 节点定义（旧版）
│   ├── ast_unified.py    # AST 节点定义（统一版）
│   ├── code_generator.py # Python 代码生成器
│   ├── code_generator_unified.py # 统一版代码生成器
│   ├── semantic_analyzer.py  # 语义分析器（符号表、作用域）
│   ├── semantic_identifier.py # 语义标识符
│   ├── type_inferencer.py    # 类型推断器
│   ├── module_resolver.py    # 模块解析器
│   ├── class_parser.py       # 类定义解析器扩展
│   ├── verb_info.py          # 动词信息模块
│   ├── arity_parser.py       # 元数驱动解析器
│   ├── core/                  # 核心配置和接口
│   │   ├── config.py         # 编译器配置
│   │   ├── errors.py         # 错误类型定义
│   │   └── interfaces.py     # 编译器接口抽象
│   ├── repl/                  # REPL 交互环境
│   │   ├── core.py           # REPL 核心
│   │   ├── executor.py       # 执行器
│   │   ├── commands.py       # 命令处理器
│   │   ├── completer.py      # 自动补全
│   │   └── highlighter.py    # 语法高亮
│   └── stdlib/               # 标准库
│       └── builtins.py       # 内置函数实现
├── antlrparser/          # ANTLR4 解析器（用于编译流程）
│   ├── DuanLang.g4       # ANTLR 语法定义
│   ├── duan_parser/      # 生成的解析器代码
│   ├── duan_interpreter.py # 解释器
│   ├── duan_llvm.py      # LLVM 代码生成器
│   ├── duan_visitor.py   # AST 访问器
│   └── duan_cli.py       # 命令行工具
├── cli/                  # 命令行入口
│   └── duanc.py          # 段言编译器 CLI
├── tests/                # 测试套件
│   ├── test_comprehensive.py   # 综合测试
│   ├── test_parser.py         # 解析器测试
│   ├── test_lexer.py          # 词法分析器测试
│   ├── test_class_definition.py # 类定义测试
│   ├── test_module_system.py  # 模块系统测试
│   ├── test_suite_v2.py       # 完整测试套件
│   └── run_tests.py           # 测试运行器
├── examples/             # 示例代码
│   ├── basic.duan        # 基础语法示例
│   ├── advanced.duan     # 高级功能示例
│   ├── class_example.duan # 类定义示例
│   ├── calculator.duan   # 计算器示例
│   ├── student_management.duan # 学生管理系统
│   └── modules/          # 模块化示例
├── stdlib/               # 标准库 (.duan 源文件)
│   ├── 数学工具.duan     # 数学工具库
├── docs/                 # 文档
│   ├── 统一语法规范_v1.6.md  # 语言规范
│   ├── 教程.md                # 学习教程
│   └── USER_MANUAL.md        # 用户手册
├── bootstrap/            # 自举相关
│   ├── lexer.duan        # 自举词法分析器
│   ├── parser.duan       # 自举语法解析器
│   ├── ast_nodes.duan    # 自举 AST 定义
│   └── codegen.duan      # 自举代码生成器
└── cli/duanc.py          # 命令行编译器
```

## 命令行工具

### 编译并运行

```bash
python cli/duanc.py examples/hello.duan --run
```

### 运行测试

```bash
# 运行综合测试
python test_comprehensive_v2.py

# 运行测试套件
python tests/run_tests.py

# 使用 pytest
python -m pytest tests/
```

## 当前状态

所有测试全部通过：

| 测试套件 | 状态 |
|----------|------|
| 综合测试（9 项：变量、函数、条件、循环、递归、类、继承） | ✅ 通过 |
| 边界测试（33 项：空值、负数、浮点、嵌套、递归深度等） | ✅ 通过 |
| 词法分析测试 | ✅ 通过 |
| 语法解析测试 | ✅ 通过 |
| 类定义测试 | ✅ 通过 |

**编译器状态：**
- 词法分析：正常（三层分词机制，支持中文标识符、关键字、运算符）
- 语法分析：正常（递归下降解析器，支持 v1.6 统一语法）
- AST 构建：正常（30+ AST 节点类型，`__slots__` 优化内存）
- 语义分析：正常（符号表、作用域检查）
- 代码生成：正常（Python 后端，支持完整特性）
- 错误处理：正常（结构化错误类，带行号/列号/上下文提示）

**性能指标（优化后）：**
- 词法分析：~0.053 ms/次（提升 32%）
- 语法解析：~0.060 ms/次（提升 20%）
- 完整编译：~0.127 s（33 项测试，提升 39%）

## 许可证

MIT License

---

*段言 - 让编程更自然*