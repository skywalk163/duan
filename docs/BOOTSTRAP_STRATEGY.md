# 段言自举策略和路线图

**日期**: 2026-08-05  
**版本**: v1.2.0  
**目标**: 用段言重写段言编译器，实现真正的自举

---

## 一、自举定义

### 1.1 什么是真正的自举？

**自举（Bootstrap）**：用语言自身编写编译器，能够编译自己。

**三个层次**：
1. **伪自举** - 代码中大量使用Python代码块
2. **部分自举** - 核心逻辑用段言实现，少量依赖内置函数
3. **完全自举** - 编译器完全用段言实现，能编译自己

### 1.2 我们的目标

**目标**：实现**部分自举**
- 编译器核心逻辑用段言实现
- 依赖标准库提供的基础函数（文件I/O、列表操作等）
- 能够编译一个简化版的段言程序
- 最终能够编译自己

---

## 二、当前状态（2026-08-05）

### 2.1 已完成的工作

```
Level 3：自举编译器 v1（已完成）
  ├── bootstrap_level3.duan  - 段言自举编译器源码
  ├── level3_generated.py    - Python 手动实现
  ├── 三次自举一致性验证通过
  └── 支持：变量、函数、控制流、类、列表操作

Level 4：面向对象增强（已完成）
  ├── level4_generated.py    - 完整面向对象支持
  ├── 类定义、继承、属性访问、父类调用
  └── 编译器可以自举自身

Level 5：异常处理 + 模块系统（已完成）
  ├── level5_generated.py    - 异常处理 + 模块系统
  ├── bootstrap_level5.duan  - 段言自举编译器源码
  ├── 异常处理：尝试/捕获/最终/抛出
  ├── 模块系统：导入/导出/内联/搜索路径
  └── 测试：test_level5_exception.py + test_level5_module.py

Level 6：无空格分词 + 纯缩进语法（已完成）
  ├── level6_generated.py    - 无空格分词 + 纯缩进
  ├── 无空格词法分析器：最长前缀匹配自动拆分关键字
  ├── 纯缩进块结构：INDENT/DEDENT 令牌，移除结束关键字
  ├── 异常处理核心修复：finally 块深度追踪、类定义处理
  └── 测试：38 用例全部通过（26 全面 + 12 边界场景）
```

### 2.2 当前架构

```
┌──────────────────────────────────────────────────┐
│                Bootstrap 编译器                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │ lexer    │→ │ parser   │→ │ codegen      │    │
│  │ .duan    │  │ .duan    │  │ .duan        │    │
│  └──────────┘  └──────────┘  └──────────────┘    │
│                      ↑                            │
│                 compiler.duan                     │
│                  (协调器)                          │
└──────────────────────────────────────────────────┘
         ↑                    ↓
    ANTLR 解释器          Python 代码
    (开发时运行)          (生产运行)
```

### 2.3 代码规范

所有 bootstrap 代码使用 **ANTLR 规范语法**：

```段言
段落 函数名 接收 参数1, 参数2：
  定义 result 等于 表达式。
  返回 result。
结束。
```

- 使用 `段落` 关键字（而非 `段`）
- 使用 `接收` 声明参数
- 使用 `结束。` 终止块
- 使用英文标识符避免与中文关键字冲突
- 标准库函数调用使用 `《函数名》(args)` 语法

---

## 三、实现路线图

### 3.1 渐进式自举策略

```
阶段1：bootstrap 编译器实现 ✅
  ├── 用段言编写编译器核心组件
  ├── 在 ANTLR 解释器上运行
  └── 验证代码生成逻辑正确

阶段2：自举编译（当前）
  ├── 用 bootstrap 编译器编译自身
  ├── 解决 列→列表 一致性等兼容性问题
  └── 实现自举编译管道

阶段3：交叉验证
  ├── 比较 ANTLR 输出和自举输出
  └── 确保代码生成等价

阶段4：完全自举
  ├── bootstrap 编译器能编译自己
  ├── 生成的编译器再次编译自身
  └── 两次输出一致
```

### 3.2 当前模块功能

| 模块 | 功能 | 状态 |
|------|------|------|
| `token.duan` | Token类型定义、关键字检查、符号映射 | ✅ 完成 |
| `duan_ast.duan` | AST节点构造函数（program, paragraph_def, var_decl等） | ✅ 完成 |
| `lexer.duan` | 词法分析（关键字、标识符、数字、字符串、符号、缩进） | ✅ 完成 |
| `parser.duan` | 递归下降语法分析（变量声明、赋值、条件、循环、函数定义） | ✅ 完成 |
| `codegen.duan` | Python代码生成（表达式、语句、函数、内置映射） | ✅ 完成 |
| `compiler.duan` | 编译管道协调（compile_source, compile_file） | ✅ 完成 |
| `main.duan` | CLI入口 | ✅ 完成 |
| `run_compiler.py` | Python端运行器 | ✅ 完成 |

---

## 四、数据结构

### 4.1 Token

使用字典表示：

```段言
# 创建令牌
段落 创建令牌 接收 种别, 值, 横, 纵：
  定义 令牌 等于 《字典创建》()。
  《字典设置》(令牌, "种别", 种别)。
  《字典设置》(令牌, "值", 值)。
  《字典设置》(令牌, "横", 横)。
  《字典设置》(令牌, "纵", 纵)。
  返回 令牌。
结束。
```

### 4.2 AST

使用列表（数组）表示，节点类型为第一个元素：

```段言
# 示例：变量声明节点
["var_decl", "名称", ["number", "42"]]

# 示例：函数定义节点
["paragraph_def", "函数名", ["参数1", "参数2"], [body_stmt1, body_stmt2]]
```

支持的节点类型：`program`, `paragraph_def`, `var_decl`, `assign`, `compound_assign`, `if_stmt`, `while_loop`, `return`, `expr_stmt`, `identifier`, `number`, `string`, `boolean`, `null`, `binary_op`, `unary_op`, `func_call`, `member_access`

---

## 五、API 参考

### 5.1 编译器API

```段言
compile_source(source: 字符串) → 字符串
  # 输入：段言源代码
  # 输出：Python 代码

compile_file(filepath: 字符串) → 字符串
  # 输入：段言源代码文件路径
  # 输出：Python 代码
```

### 5.2 运行方式

```bash
# 方式1：使用 Python runner（推荐）
python bootstrap/run_compiler.py <source.duan> [output.py]

# 方式2：运行测试
python bootstrap/test_bootstrap_pipeline.py

# 方式3：直接通过 ANTLR 解释器
python -c "
from duan_interpreter import run_source
interp = run_source(open('bootstrap/compiler.duan').read())
# 然后调用 interp.env.get('compile_source') 等
"
```

---

## 六、下一步工作

1. **Level 6 自举验证**：用 level6_generated.py 编译 bootstrap 编译器，验证自举一致性
2. **Level 7 类型注解**：变量类型标注、函数参数/返回值类型、编译期类型检查
3. **Level 7+ 后端的自举**：Level 7 生成的 Python 代码再次编译自身，实现二次自举收敛
4. **LLVM 后端集成**：将自举编译器生成的代码通过 LLVM 编译为原生可执行文件
5. **完善文档**：记录完整的开发和测试流程

---

## 七、测试

### 7.1 测试套件

```bash
# 运行所有测试
python bootstrap/test_bootstrap_pipeline.py

# 输出期望：
# - Test 1: ANTLR Run ✓
# - Test 2: ANTLR Parse ✓
# - Test 3: Bootstrap Codegen ✓
# - Test 4: Codegen w/ Functions ✓
# - All tests passed!
```

### 7.2 测试用例

`test_simple.duan`:
```段言
设 x 为 42。
打印 x。
```

编译后生成：
```python
x = 42
_duan_builtin.打印(x)
```

执行输出：`42`

---

## 八、技术要点

1. **一致性**：所有 bootstrap 代码使用 `列表` 前缀（而非 `列`），确保代码生成映射正确
2. **映射表**：`map_builtin` 函数将段言内置函数名映射到 `_duan_builtin.*`
3. **缩进处理**：使用缩进栈生成 INDENT/DEDENT 令牌
4. **先匹配长关键字**：词法分析器优先匹配较长关键字（如 `否则若` 优先于 `否则`）
---

## 九、Level 3 自举编译器（2026-06-30）

### 9.1 概述

Level 3 编译器是用段言自身编写的自举编译器，实现了**真正的二次自举**：
- 编译器源码：`bootstrap/bootstrap_level3.duan`
- 第一次自举输出：`bootstrap/level3_self_compiled.py`
- 第二次自举输出：`bootstrap/level3_self_compiled2.py`
- 稳定性验证：第二次与第三次自举输出**完全一致**

### 9.2 支持的语法特性

| 类别 | 特性 | 关键字 |
|------|------|--------|
| 变量 | 变量声明 | `设`、`为` |
| 函数 | 函数定义 | `段`、`段落`、`接收`、`返回` |
| 控制流 | 条件语句 | `如果`、`否则`、`结束` |
| 控制流 | 循环 | `当`（while）、`遍历`（for） |
| 运算符 | 算术 | `加`、`减`、`乘`、`除`、`取模` |
| 运算符 | 比较 | `等于`、`不等于`、`小于`、`大于`、`小于等于`、`大于等于` |
| 运算符 | 布尔 | `且`、`或`、`非` |
| 面向对象 | 类定义 | `类`、`属性`、`己` |
| 数据结构 | 列表 | `列表创建`、`列表追加`、`列表获取`、`列表长度` |
| 字符串 | 字符串操作 | `字符串长度`、`字符串获取`、`截取` |

### 9.3 关键技术实现

#### 9.3.1 递归转迭代

为了避免 Python 递归深度限制并提升性能，所有核心函数均为**迭代实现**：

- `扫`（词法扫描）：while 循环迭代处理每个字符
- `compile_stmts`（语句编译）：while 循环逐条处理语句
- `compile_block`（块编译）：迭代处理块内语句
- `find_matching_end`（匹配结束关键字）：迭代遍历，level 计数跟踪嵌套
- `加缩进行`（缩进处理）：迭代逐行处理
- `compile_top`（顶层编译）：迭代处理顶层函数
- `收集参数`（参数收集）：迭代收集参数列表

#### 9.3.2 嵌套块匹配

`find_matching_end` 函数通过 level 计数器正确处理多种嵌套块结构：

- `如果` -> level +1
- `当` -> level +1
- `遍历` -> level +1
- `类` -> level +1
- `段落` / `段` -> level +1
- `否则` -> level == 1 时返回当前位置
- `结束` -> level == 1 时返回 p+1，否则 level -1

#### 9.3.3 表达式层级

表达式解析采用递归下降，按优先级分层：

```
或表达式 -> 且表达式 -> 比较表达式 -> 加减表达式 -> 乘除表达式 -> 一元表达式
```

每层均支持**连续同优先级运算**（while 循环实现）。

### 9.4 性能数据

| 指标 | 值 |
|------|-----|
| 编译自身耗时 | ~0.12 秒 |
| 生成代码行数 | ~600 行 |
| 函数数量 | 40 个 |
| 源码大小 | 23,112 字节 |
| 生成代码大小 | 24,347 字节 |

### 9.5 自举验证

**验证方法**：三次自举一致性测试

1. 用 Python 手动实现的编译器（level3_generated.py）编译 bootstrap_level3.duan -> level3_self_compiled.py
2. 用 level3_self_compiled.py 编译 bootstrap_level3.duan -> level3_self_compiled2.py
3. 用 level3_self_compiled2.py 编译 bootstrap_level3.duan -> level3_self_compiled3.py
4. 验证 level3_self_compiled2.py 与 level3_self_compiled3.py **完全相同**

**验证结果**：通过，二次自举稳定。

### 9.6 已知限制

1. 字符串仅支持双引号，单引号仅用于转义（`'"'` 表示双引号，`"'"` 表示单引号）
2. 不支持注释嵌套
3. 错误处理较简单，依赖运行时异常
4. 仅支持 Python 代码生成后端
5. 列表/字典字面量需要通过函数调用创建

---

## 十、Level 5 自举编译器 — 异常处理与模块系统（2026-07-01）

### 10.1 概述

Level 5 编译器在 Level 4 面向对象的基础上，增加了**异常处理**和**模块系统**两大特性：

- 编译器源码：`bootstrap/bootstrap_level5.duan`
- Python 手动实现：`bootstrap/level5_generated.py`
- 模块预处理器：`bootstrap/module_preprocessor.py`

### 10.2 新增语法特性

| 类别 | 特性 | 关键字 |
|------|------|--------|
| 异常处理 | try 块 | `尝试` |
| 异常处理 | catch 块 | `捕获` |
| 异常处理 | finally 块 | `最终` |
| 异常处理 | 抛出异常 | `抛出` |
| 模块系统 | 导入模块 | `导入` |
| 模块系统 | 导出符号 | `导出` |

### 10.3 异常处理实现

#### 10.3.1 处理流程

```
尝试(try) 块 → 捕获(catch) 块序列 → 最终(finally) 块
```

- `comp_try` 函数扫描 tokens 定位 `捕获`/`最终` 位置
- 使用 depth 计数器追踪 INDENT/DEDENT 嵌套层级
- 每个捕获块生成独立的 `except` 分支
- `最终` 块生成 `finally` 分支
- `comp_throw` 函数将 `抛出` 语句转换为 `raise`

#### 10.3.2 异常类型映射

| 中文别名 | Python 类型 |
|---------|-----------|
| 异常 | Exception |
| 值错误 | ValueError |
| 类型错误 | TypeError |
| 键错误 | KeyError |
| 索引错误 | IndexError |
| 除零错误 | ZeroDivisionError |
| 属性错误 | AttributeError |
| 名称错误 | NameError |
| 文件错误 | FileNotFoundError |
| 运行错误 | RuntimeError |

### 10.4 模块系统实现

#### 10.4.1 处理流程

1. 模块预处理器（`module_preprocessor.py`）扫描导入语句
2. 构建模块依赖图，执行拓扑排序
3. 沿搜索路径定位模块文件
4. 编译期内联：将模块代码嵌入到主模块中

#### 10.4.2 搜索路径

1. 当前目录
2. 当前目录/模块/
3. 当前目录/modules/
4. 当前目录/test_modules/
5. 标准库目录

### 10.5 测试覆盖

| 测试文件 | 用例数 | 测试内容 |
|---------|-------|---------|
| `test_level5_exception.py` | 10 | try-catch-finally 基本流程、异常类型匹配、抛出变量 |
| `test_level5_module.py` | 6 | 导入导出、内联导出、嵌套模块、标准库导入 |

---

## 十一、Level 6 自举编译器 — 无空格分词与纯缩进语法（2026-08-05）

### 11.1 概述

Level 6 编译器是自举编译器系列的重大升级，引入了**无空格分词**和**纯缩进语法**两个核心特性：

- Python 实现：`bootstrap/level6_generated.py`
- 全面测试：`bootstrap/test_level6_full.py`（26 用例）
- 边界场景测试：`bootstrap/_test_edge_cases.py`（12 用例）

### 11.2 核心设计

#### 11.2.1 无空格分词

传统分词依赖空格分隔关键字和标识符，Level 6 改用**最长前缀匹配**算法：

```
输入: "段foo接收a"
     ↓ 最长匹配
令牌: [KW("段"), ID("foo"), KW("接收"), ID("a")]
```

- 从当前位置开始，在关键字列表中查找最长匹配项
- 匹配到关键字后，剩余部分作为标识符
- 支持 `foo接收a` 等无空格语法

#### 11.2.2 纯缩进语法

用缩进层级替代 `结束` 关键字，通过 INDENT/DEDENT 令牌管理块边界：

```
段主函数                    →  FUNC("主函数"), INDENT
    设x为42                 →  VAR("x"), NUM("42")
    如果x大于5              →  IF, INDENT
        输出("big")         →  CALL("输出"), STR("big")
    否则                    →  ELSE, DEDENT, INDENT
        输出("small")       →  CALL("输出"), STR("small")
                            →  DEDENT, DEDENT
```

- 缩进栈管理：当前缩进 > 栈顶 → 生成 INDENT；当前缩进 < 栈顶 → 生成 DEDENT
- 纯缩进 + 无空格组合：`如果x大于5` 即 `if x > 5`

### 11.3 修复记录

#### 11.3.1 finally 块深度追踪修复

**问题**：`comp_try` 函数中，扫描到 `捕获`/`最终` 关键字后 depth 被错误重置为 1，导致 finally 块的 INDENT 将 depth 推到 2，DEDENT 只回到 1，无法触发 depth == 0 的结束检测。

**修复**：将 `depth = 1` 改为 `depth = 0`，使后续 INDENT → DEDENT 能正确归零。

#### 11.3.2 类定义处理修复

**问题**：`compile_block` 和 `compile_stmts` 函数缺少对 `类` 关键字的处理，导致类定义被当作普通语句生成，类体被忽略。

**修复**：添加 `tv == "类"` 分支，调用 `compile_class` 函数处理类定义。

#### 11.3.3 ASCII 负号支持

**问题**：词法分析器不支持 ASCII 负号，`-1` 中的 `-` 被静默跳过，导致 `w.process(-1)` 被解析为 `w.process(1)`。

**修复**：在词法分析器中添加 `-` 开头数字的处理逻辑，生成负数字面量。

#### 11.3.4 己 关键字处理

**问题**：`compile_block` 和 `compile_stmts` 缺少对 `己` 关键字的处理，导致 `己.div(a,b)` 生成 `div(a,b)` 而非 `self.div(a,b)`。

**修复**：添加 `KW(己)` 分支，调用表达式解析生成正确的 `self` 前缀代码。

### 11.4 调试能力

- 添加 `调试模式` 全局开关（设为 `真` 可输出详细日志）
- comp_try 扫描循环：INDENT/DEDENT 追踪、捕获/最终定位、边界计算
- 各分支体结束位置计算日志
- comp_throw 异常表达式日志

### 11.5 测试覆盖

| 测试类别 | 用例数 | 测试内容 |
|---------|-------|---------|
| 无空格分词 | 5 | 函数定义、变量声明、返回语句、if 语句、混合分隔符 |
| 纯缩进控制流 | 5 | if-else、while、for、嵌套 if、嵌套 while |
| 纯缩进函数 | 4 | 简单函数、多函数、递归、函数嵌套调用 |
| 纯缩进异常 | 4 | try-catch、try-catch-finally、try-finally、抛出变量 |
| 纯缩进类 | 2 | 简单类、类继承 |
| 表达式运算 | 4 | 算术优先级、比较、非运算、字符串拼接 |
| 混合场景 | 2 | 复杂嵌套、异常+循环混合 |
| 边界场景 | 12 | 类方法异常、try 嵌套、类继承+异常传播、多层缩进连续 try-finally、类成员变量状态管理 |

### 11.6 性能数据

| 指标 | 值 |
|------|-----|
| 生成代码行数 | ~1500 行 |
| 函数数量 | 40+ 个 |
| 测试通过率 | 38/38 全部通过 |
