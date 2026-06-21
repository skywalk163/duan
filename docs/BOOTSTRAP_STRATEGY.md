# 段言自举策略和路线图

**日期**: 2026-06-20  
**版本**: v1.1.0  
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

## 二、当前状态（2026-06-20）

### 2.1 已完成的工作

```
阶段1：语法规范（已完成）
  ├── ANTLR 语法文件：DuanLangLexer.g4 / DuanLangParser.g4
  ├── ANTLR 解析器生成器
  └── 句法规范：段落 段名 接收 参数：body结束。

阶段2：bootstrap 编译器核心（已完成）
  ├── token.duan      - Token 类型定义与构造函数
  ├── duan_ast.duan   - AST 节点构造函数
  ├── lexer.duan      - 词法分析器（支持汉字标识符、关键字、缩进）
  ├── parser.duan     - 递归下降语法分析器
  ├── codegen.duan    - Python 代码生成器
  ├── compiler.duan   - 主编译器入口
  └── main.duan       - CLI 入口

阶段3：测试验证（已完成）
  ├── test_bootstrap_pipeline.py  - 4项测试全部通过
  │   ├── ANTLR 解释器运行测试
  │   ├── ANTLR AST 检查测试
  │   ├── Bootstrap 代码生成测试
  │   └── 带函数的代码生成测试
  └── run_compiler.py             - Python 端编译器运行器
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

1. **调试 bootstrap 编译器自身**：让 `run_compiler.py` 能加载并运行 bootstrap .duan 文件
2. **解决 ANTLR 与 bootstrap 语法兼容性**：统一 `段` → `段落`，统一 `结束` 使用
3. **实现自举编译**：用 bootstrap 编译器编译自身，生成 `compiler_gen.py`
4. **交叉验证**：确保 ANTLR 输出和自举输出等价
5. **完善文档**：记录完整的开发和使用流程

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