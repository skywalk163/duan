# 段言（Duan）API 参考

## 目录

1. [解析器 API](#解析器-api)
2. [解释器 API](#解释器-api)
3. [编译器 API](#编译器-api)
4. [AST 节点](#ast-节点)
5. [内置函数](#内置函数)

---

## 解析器 API

### 模块: `duan_visitor`

#### `parse_source(source: str) -> Module`

解析段言源代码为 AST 模块。

**参数:**
- `source`: 段言源代码字符串

**返回:**
- `Module`: AST 模块节点

**示例:**
```python
from antlrparser.duan_visitor import parse_source

source = "定义 x 等于 10。"
module = parse_source(source)
```

#### `parse_file(filepath: str) -> Module`

从文件读取并解析段言源代码。

**参数:**
- `filepath`: 源文件路径

**返回:**
- `Module`: AST 模块节点

#### `DuanParser` 类

**方法:**
- `__init__()`: 初始化解析器
- `parse(source: str) -> Module`: 解析源代码

---

## 解释器 API

### 模块: `duan_interpreter`

#### `run_source(source: str, filepath: str = None, search_paths: List[str] = None) -> Interpreter`

解析并执行段言源代码。

**参数:**
- `source`: 段言源代码
- `filepath`: 源文件路径（用于模块导入）
- `search_paths`: 模块搜索路径

**返回:**
- `Interpreter`: 执行后的解释器实例

**示例:**
```python
from antlrparser.duan_interpreter import run_source

interpreter = run_source("打印(\"你好世界\")。")
print(interpreter.get_output())  # 输出: 你好世界
```

#### `run_file(filepath: str, search_paths: List[str] = None) -> Interpreter`

从文件读取并执行段言源代码。

**参数:**
- `filepath`: 源文件路径
- `search_paths`: 模块搜索路径

**返回:**
- `Interpreter`: 执行后的解释器实例

#### `Interpreter` 类

**属性:**
- `global_env`: 全局变量环境
- `output_lines`: 输出行列表

**方法:**
- `interpret(node: ASTNode)`: 解释执行 AST 节点
- `interpret_module(module: Module)`: 解释执行模块
- `reset()`: 重置解释器状态
- `get_output()`: 获取所有输出

---

## 编译器 API

### 模块: `duan_llvm`

#### `compile_duan(source_code: str, output_name: str = "output.exe") -> bool`

编译段言源码为可执行文件。

**参数:**
- `source_code`: 段言源代码
- `output_name`: 输出文件名

**返回:**
- `bool`: 是否编译成功

**示例:**
```python
from antlrparser.duan_llvm import compile_duan

source = "打印(42)。"
success = compile_duan(source, "test.exe")
if success:
    os.system("test.exe")  # 输出: 42
```

#### `LLVMCodeGen` 类

**方法:**
- `generate(module: Module) -> str`: 生成 LLVM IR 字符串
- `_generate_segment(seg)`: 生成段落代码
- `_generate_class(cls)`: 生成类代码

---

## AST 节点

### 基础节点

#### `ASTNode`
所有 AST 节点的基类。

**属性:**
- `line`: 行号
- `column`: 列号

### 字面量节点

#### `NumberLiteral`
数字字面量。

**属性:**
- `value`: 数值（int 或 float）

#### `StringLiteral`
字符串字面量。

**属性:**
- `value`: 字符串值

#### `BooleanLiteral`
布尔字面量。

**属性:**
- `value`: 布尔值

#### `NullLiteral`
空值字面量。

### 表达式节点

#### `BinaryOp`
二元运算表达式。

**属性:**
- `left`: 左操作数
- `operator`: 运算符
- `right`: 右操作数

#### `UnaryOp`
一元运算表达式。

**属性:**
- `operator`: 运算符
- `operand`: 操作数

#### `FunctionCall`
函数调用表达式。

**属性:**
- `name`: 函数名（Identifier 或 SegmentName）
- `arguments`: 参数列表

#### `ListLiteral`
列表字面量。

**属性:**
- `elements`: 元素列表

#### `DictLiteral`
字典字面量。

**属性:**
- `entries`: 键值对列表

### 语句节点

#### `VariableDeclaration`
变量声明。

**属性:**
- `name`: 变量名
- `value`: 初始值

#### `Assignment`
赋值语句。

**属性:**
- `target`: 目标（Identifier 或 PropertyAccess）
- `value`: 值

#### `IfStatement`
条件语句。

**属性:**
- `condition`: 条件表达式
- `then_body`: 真分支
- `else_body`: 假分支
- `elseif_conditions`: elif 条件列表
- `elseif_bodies`: elif 分支列表

#### `WhileStatement`
当循环。

**属性:**
- `condition`: 条件表达式
- `body`: 循环体

#### `ForeachStatement`
遍历循环。

**属性:**
- `variable`: 循环变量名
- `iterable`: 可迭代对象
- `body`: 循环体

#### `ReturnStatement`
返回语句。

**属性:**
- `value`: 返回值

#### `PrintStatement`
打印语句。

**属性:**
- `value`: 要打印的值

### 定义节点

#### `SegmentDefinition`
段落定义（函数）。

**属性:**
- `name`: 段落名
- `parameters`: 参数列表
- `body`: 函数体
- `return_type`: 返回类型

#### `ClassDefinition`
类定义。

**属性:**
- `name`: 类名
- `superclasses`: 父类列表
- `interfaces`: 实现的接口列表
- `fields`: 字段列表
- `methods`: 方法列表
- `constructor`: 构造函数

#### `InterfaceDefinition`
接口定义。

**属性:**
- `name`: 接口名
- `superinterfaces`: 父接口列表
- `methods`: 方法签名列表
- `properties`: 属性签名列表

---

## 内置函数

### 数学函数

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `abs` | 绝对值 | `(x: 数)` | 数 |
| `max` | 最大值 | `(x: 数, y: 数, ...)` | 数 |
| `min` | 最小值 | `(x: 数, y: 数, ...)` | 数 |
| `sqrt` | 平方根 | `(x: 数)` | 数 |
| `pow` | 幂运算 | `(base: 数, exp: 数)` | 数 |
| `round` | 四舍五入 | `(x: 数)` | 数 |

### 字符串函数

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `len` | 长度 | `(s: 串)` | 数 |
| `trim` | 去除空白 | `(s: 串)` | 串 |
| `substring` | 子串 | `(s: 串, start: 数, end: 数)` | 串 |

### 列表函数

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `listLen` | 列表长度 | `(list: 列)` | 数 |
| `listAppend` | 追加元素 | `(list: 列, item)` | 空 |
| `listReverse` | 反转列表 | `(list: 列)` | 空 |
| `listIndexOf` | 查找索引 | `(list: 列, item)` | 数 |
| `listContains` | 包含检查 | `(list: 列, item)` | 布尔 |
| `listSlice` | 切片 | `(list: 列, start: 数, end: 数)` | 列 |
| `listConcat` | 拼接 | `(list1: 列, list2: 列)` | 列 |

### 类型转换

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `_串化` | 转字符串 | `(x)` | 串 |
| `_数化` | 转数字 | `(x)` | 数 |

### 文件操作

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `_读文件` | 读取文件 | `(path: 串)` | 串 |
| `_写文件` | 写入文件 | `(path: 串, content: 串)` | 空 |

### 调试函数

| 函数名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| `printDebug` | 调试打印 | `(msg: 串, value)` | 空 |
| `assert` | 断言 | `(condition: 布尔, msg: 串)` | 空 |

---

## 命令行接口

### `duan_cli.py`

```bash
duan compile <source> -o <output>    # 编译为可执行文件
duan run <source>                     # 解释执行
duan parse <source>                   # 解析并显示 AST
```

**选项:**
- `-o, --output`: 指定输出文件名（仅 compile）