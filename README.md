# 段言 (DuanLang)

段言是一种面向中文用户的编程语言，采用中文关键字和自然语言风格的语法设计。

## 特性

- 🀄 **中文语法** - 使用中文关键字，如 `定义`、`如果`、`当`、`类` 等
- 🌟 **面向对象** - 支持类、接口、继承、方法等面向对象特性
- 🔄 **解释器** - 内置解释器支持即时运行
- 🔥 **编译器** - 支持编译为 LLVM IR，最终生成原生可执行文件
- 📚 **标准库** - 内置数学函数、字符串处理、列表操作等

## 快速开始

### 安装依赖

```bash
pip install antlr4-python3-runtime
```

### 运行示例

```python
from duan_visitor import parse_source
from duan_interpreter import Interpreter

source = """
定义 问候语 等于 "你好，世界！"。
打印(问候语)。
"""

module = parse_source(source)
interpreter = Interpreter()
interpreter.interpret_module(module)
```

输出：
```
你好，世界！
```

## 语法示例

### 变量和基本类型

```段言
定义 年龄 等于 25。
定义 姓名 等于 "张三"。
定义 身高 等于 1.75。
定义 已婚 等于 真。
定义 空值 等于 空。
```

### 条件语句

```段言
如果 年龄 大于 18 那么
    打印("成年人")。
否则如果 年龄 大于 12 那么
    打印("青少年")。
否则
    打印("儿童")。
结束。
```

### 循环

```段言
定义 i 等于 0。
当 i 小于 10 那么
    打印(i)。
    i 等于 i + 1。
结束。
```

### 类和对象

```段言
《人》类:
  定义 姓名 等于 ""。
  定义 年龄 等于 0。
  
  《初始化》方法(姓名参数, 年龄参数):
    姓名 等于 姓名参数。
    年龄 等于 年龄参数。
  结束。
  
  《说话》方法():
    打印(姓名 + "，年龄: " + _串化(年龄))。
  结束。
结束。

定义 张三 等于 新 人("张三", 25)。
张三之说话()。
```

### 段落（函数）

```段言
《计算平方》段(数字):
  返回 数字 * 数字。
结束。

定义 结果 等于 《计算平方》(5)。
打印(结果)。
```

## 命令行工具

### 运行脚本

```bash
python duan_cli.py run example.duan
```

### 编译为可执行文件

```bash
python duan_cli.py compile example.duan -o example.exe
```

## 项目结构

```
duan/
├── antlrparser/          # ANTLR 解析器相关文件
│   ├── DuanLang.g4       # 语法定义文件
│   ├── duan_ast.py       # 抽象语法树定义
│   ├── duan_visitor.py   # AST 访问器
│   ├── duan_interpreter.py # 解释器
│   ├── duan_llvm.py      # LLVM 代码生成器
│   └── duan_tokenizer.py # 自定义分词器
├── runtime/              # 运行时库
├── tests/                # 测试用例
└── duan_cli.py           # 命令行工具
```

## 标准库函数

### 数学函数
- `sin(x)` - 正弦
- `cos(x)` - 余弦  
- `sqrt(x)` - 平方根
- `abs(x)` - 绝对值

### 字符串函数
- `len(串)` - 字符串长度
- `strcmp(串1, 串2)` - 字符串比较

### 类型转换
- `_串化(x)` - 转换为字符串
- `_数化(串)` - 转换为数字

## 开发

### 重新生成解析器

```bash
cd antlrparser
antlr4 -Dlanguage=Python3 DuanLang.g4 -visitor -o duan_parser
```

### 运行测试

```bash
python -m pytest tests/
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

*段言 - 让编程更自然*
