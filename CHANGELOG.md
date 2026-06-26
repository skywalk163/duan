# 段言 (DuanLang) 变更日志

所有重要的更改都会记录在此文件中。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
并使用 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.6.1] - 2026-06-25

**编辑器集成与深度调试功能。** 完成 VS Code 插件、LSP 客户端集成、调试适配器（DAP 协议）、交互式调试 REPL，完善 Phase 7.5 和 Phase 7.6 至约 90% 完成度。

### ✨ 新增

#### 🎨 VS Code 插件 (`vscode-extension/`)
- **完整的扩展配置**（`package.json`）：
  - 语言 ID：`duan`
  - 文件关联：`.duan` 文件
  - 调试器定义：`duan` 类型
  - 命令注册：运行文件、打开 REPL、重启服务器
- **LSP 客户端集成**（`src/extension.ts`）：
  - 自动连接 LSP 服务器
  - 支持 stdio 和调试模式启动
  - 中间件支持自定义补全和悬停
- **调试配置提供者**（`src/debugConfiguration.ts`）：
  - 启动调试、附加调试配置
  - 自动检测当前文件
  - 配置文件验证

#### 📝 语法与代码片段
- **TextMate 语法定义**（`syntaxes/duan.tmLanguage.json`）：
  - 关键字高亮（控制流、声明、类型）
  - 动词高亮（算术、字符串、列表操作）
  - 中文标识符支持
  - 字符串插值高亮
- **代码片段**（`snippets/duan.json`）：
  - 函数定义（段落）
  - 条件语句（如果）
  - 循环语句（遍历、当）
  - 类定义
  - 异常处理（尝试）
- **语言配置**（`language-configuration.json`）：
  - 自动闭合括号
  - 缩进规则
  - 折叠标记

#### 🐛 调试适配器 (`debug-adapter/`)
- **DAP 协议实现**（`duan_debug_adapter.py`）：
  - 完整的调试协议消息处理
  - 断点管理（设置、清除、条件断点）
  - 线程和调用栈
  - 变量查看
  - 配置生成器（`config_generator.py`）

#### 🔧 深度调试功能
- **调试器核心**（`tools/duan_debug.py`）：
  - `DuanDebugger`：断点管理、单步执行、变量监视
  - `DebuggerContext`：调试上下文管理器
  - `StackFrame`：调用栈帧
  - 支持条件断点、命中计数
- **交互式调试 REPL**（`tools/duan_debug_repl.py`）：
  - `b <行号>`：设置断点
  - `d <行号>`：删除断点
  - `c`：继续执行
  - `n`：单步跳过
  - `s`：单步进入
  - `r`：单步返回
  - `p <变量>`：打印变量
  - `w`：显示调用栈
  - `l`：显示源代码
  - `vars`：显示所有变量

#### 🔗 CLI 集成
- **新增 `duan debug` 命令**：
  ```bash
  duan debug                    # 启动调试 REPL
  duan debug hello.duan        # 调试指定文件
  ```

### 📦 项目结构

```
vscode-extension/          # VS Code 插件
├── package.json           # 扩展配置
├── language-configuration.json  # 语言配置
├── src/
│   ├── extension.ts       # 扩展入口
│   └── debugConfiguration.ts  # 调试配置
├── syntaxes/
│   └── duan.tmLanguage.json   # 语法高亮
└── snippets/
    └── duan.json         # 代码片段

debug-adapter/             # 调试适配器
├── duan_debug_adapter.py  # DAP 协议实现
└── config_generator.py    # 配置生成器

tools/                     # 工具
├── repl.py               # REPL
├── duan_debug.py         # 调试器核心
└── dnan_debug_repl.py    # 调试 REPL
```

### 🧪 测试

- **单元测试新增**：
  - `tests/unit/test_errors.py`：错误格式化测试（6 个）
  - `tests/unit/test_lsp.py`：LSP 基础测试（13 个）
- **测试总数**：88 个单元/集成测试全部通过（1 跳过）

---

## [1.6.0] - 2026-06-25

**性能优化与工具链完善。** 建立基准测试框架，词法分析器性能提升约 **2.1 倍**，新增 REPL 交互式解释器，完善开发工具链，代码生成器增加常量折叠与死代码消除优化，添加错误提示美化与 LSP 基础框架。

### ✨ 新增

#### ⚡ 性能优化
- **基准测试框架**（`benchmarks/run_benchmarks.py`）：
  - 8 个基准测试程序（fibonacci、bubble_sort、class_system、hanoi 等）
  - 编译各阶段计时：词法分析 → 语法解析 → 代码生成 → 执行
  - 内存占用测量（`--mem` 参数）
  - JSON 格式输出（`--json` 参数）
  - Token 数量统计
- **词法分析器重大优化（平均提升 2.1 倍）**：
  - 消除 `_is_han` 字典缓存：CJK 汉字范围是连续的，直接 `ord()` 比较比字典查找快
  - 热点方法局部变量缓存：`_tokenize_chinese_sequence`、`_tokenize_identifier_or_keyword` 等
  - 关键字匹配优化：使用模块级 `_ALL_KEYWORDS_BY_LENGTH` 替代实例属性
  - Token 对象轻量化：`@dataclass(slots=True)` 减少内存和 GC 压力
  - 各基准测试提升：bubble_sort 2.7x、class_system 2.5x、large_expressions 2.6x
- **代码生成优化**：
  - **常量折叠**：编译时计算常量表达式（数字运算、字符串拼接）
  - **死代码消除**：移除恒真/恒假条件分支
- **解析器性能分析**：完成解析器性能热点分析，识别 `_current`、`_consume` 等高频调用点

#### 🔧 工具链完善
- **错误提示美化**（`src/errors.py`）：
  - 中文错误类型映射（SyntaxError → 语法错误、NameError → 名称错误等）
  - 源代码上下文显示（带行号和列指示符）
  - 栈追踪美化（只显示项目内的调用栈）
  - 自定义异常类：`DuanError`、`LexerError`、`SemanticError`
- **REPL 交互式解释器**（`tools/repl.py`）增强：
  - 命令历史记录功能
  - 调试命令：`跟踪(trace)`、`断点(bp)`
  - 美化的变量显示（带类型信息）
  - 美化的帮助和错误输出
- **LSP 语言服务器**（`lsp/duan_lsp.py`）基础框架：
  - 文档管理器：支持打开、更改、关闭文档
  - 代码补全：关键字、动词、变量名
  - 跳转定义：查找变量/函数定义位置
  - 诊断信息：语法错误实时提示
  - 文档符号：提取函数、变量定义

#### 📦 项目结构
- **`tools/` 工具包**：统一存放 REPL、调试器等开发工具
- **`benchmarks/` 基准测试目录**：测试程序、运行器和结果分析

### 🐛 修复

- **CLI REPL 导入路径**：修复 `duan_unified.py` 中 REPL 模块导入，支持从 `tools.repl` 加载

### 🧪 测试

- 所有 64 个单元/集成测试全部通过（1 跳过）
- 词法分析器 8 个单元测试通过
- 解析器 12 个单元测试通过
- 类系统 10 个集成测试通过
- 模块系统 3 个集成测试通过
- 标准库 28 个集成测试通过

---

## [1.5.0] - 2026-06-25

**类系统与模块系统深度完善。** 类继承、构造函数、方法重写功能全部打通，模块依赖解析与导入导出完整可用，测试覆盖 93 个用例全部通过。

### ✨ 新增

#### 🏗️ 类系统完善
- **完整类定义支持**：属性声明、构造函数、方法定义
- **类继承**：单继承、方法重写、父类方法继承
- **`己` 关键字**：类内部访问自身属性（`己属性名` → `self.属性名`）
- **方法调用**：实例方法调用正确生成带括号的 Python 代码
- **多类定义**：同一文件中支持多个类定义

#### 📦 模块系统完善
- **模块依赖解析**：`ModuleDependencyResolver` 支持模块查找与依赖图构建
- **拓扑排序**：按依赖关系排序编译顺序
- **导入语句**：`从 模块 导入 符号` 和 `导入 模块` 语法
- **导出语句**：`导出 符号列表` 语法
- **跨模块使用**：函数和类可跨模块导入使用

#### 🧪 测试体系扩展
- **类系统集成测试**：10 个用例覆盖类定义、继承、方法重写等（`tests/integration/test_class_system.py`）
- **模块系统端到端测试**：7 个用例覆盖依赖解析、导入导出等（`tests/e2e/test_module_e2e.py`）
- **测试总数**：93 个测试全部通过（0 失败，2 跳过）

### 🐛 修复

- **方法调用缺少括号**：修复 `_convert_member_access` 中空参数列表判断 bug，空参数方法调用正确生成 `()`
- **导出语句转换失败**：修复 `_convert_export_stmt` 中 `ExportStatement` 初始化参数不匹配

### 📝 文档

- 更新 [README.md](README.md)：添加类和模块语法示例
- 新增类系统集成测试文档
- 新增模块系统端到端测试文档

---

## [1.4.1] - 2026-06-25

**编译器统一与测试体系完善。** 两套编译器后端（ANTLR + SRC）统一支持 3.x 纯缩进语法，LLVM 代码生成修复关键 bug，建立系统化测试体系。

### ✨ 新增

#### 🏗️ 双后端编译器统一
- **ANTLR 后端支持 3.x 语法**：纯缩进语法无需 `结束` 关键字
- **SRC 后端 LLVM 支持**：手写递归下降解析器可生成 LLVM IR
- **统一 CLI 工具**：`cli/duan_unified.py` 支持 `--target antlr|src` 切换后端
- **AST 适配器**：`src/compiler.py` 中的 `AstAdapter` 统一两种 AST 格式

#### 🔧 LLVM 代码生成修复
- **Entry Block Alloca**：所有 alloca 指令移到函数入口块，修复 LLVM 支配关系错误
- **终止语句去重分支**：`ret/break/continue` 后不再添加冗余 `br` 指令
- **主程序防重复调用**：`_gen_main` 确保主程序只执行一次
- **字符串拼接修复**：修复字符串操作中的类型转换错误
- **时间戳转换修复**：修复 double 到 char* 的类型不匹配
- **列表索引数字字面量**：修复列表索引中数字字面量的类型转换

#### 🧪 系统化测试体系
- **三级测试结构**：`tests/unit/`、`tests/integration/`、`tests/e2e/`
- **词法分析器测试**：关键字、字面量、插值、列表/字典语法
- **语法解析器测试**：变量声明、函数定义、控制流、嵌套块
- **类型系统测试**：HM 推断、可空类型
- **自举编译器测试**：Bootstrap 自举验证
- **LLVM 管线测试**：IR 生成和编译验证
- **统一测试运行器**：`python tests/run_tests.py --unit|--integration|--e2e|--quick`

#### 📚 文档整理
- 清理重复文档，统一文档来源
- 更新 README 反映双后端架构
- 补充模块 `__init__.py` 文档字符串

### 🐛 修复

- **空行解析截断**：修复 v3 解析器遇到空行时提前停止解析的 bug
- **顶层表达式语句丢失**：修复顶层语句未包装 `ExpressionStatement` 导致打印语句丢失
- **方法调用未生成代码**：修复 `列表.追加()` 等方法调用在 LLVM 后端未生成代码
- **ForeachStatement 属性兼容**：修复 `variable` vs `var_name` 属性名不一致
- **重复文档清理**：删除 4 个过时语法规范版本和 4 个重复教程/指南文档

### 📝 文档

- 更新 [README.md](README.md)：双后端架构说明
- 新增 `docs/段言-完整规范文档.md`：v1.4.1 完整语言规范
- 保留 `docs/统一语法规范_v3.1.md`：最新语法规范

### ⚙️ CI/CD & 构建

- GitHub Actions 扩展为三级测试：unit / integration / e2e
- CI 新增 PyPI 自动发布工作流（基于 tag 触发）
- 新增发布前检查清单

---

## [1.0.0] - 2026-06-21

**首个稳定版本发布。** 段言现在拥有完整的编译流水线、类型系统、模块化支持和包管理。

### ✨ 新增

#### 🔬 HM 全局类型推断系统
- 实现 Hindley-Milner 风格的全局类型推断
- **两阶段推断架构**：预扫描注册 → 段体推断 + 泛化
- **let-polymorphism**：自动识别泛型段落并实例化
- **类型合一 (Unification)**：支持 `TypeVar` 与具体类型的双向推导
- **泛型支持**：泛型段落、泛型类、泛型接口
- **类型 ID 机制**：使用整数 `_type_id` 快速判断类型（替代 `isinstance` 链，性能提升 30-40%）
- **基本类型单例化**：每个基本类型只有一个实例，减少内存占用
- **方法签名缓存**：类方法解析后缓存，避免重复扫描
- **两轮迭代推断**：段体调用段时，先解决被调用者类型，再推断调用者

#### 🛡️ 可空类型 unwrap 系统
- 实现编译期可空类型检查
- **`!` 后置解包运算符**：`值!` 强制断言非空
- **`unwrap(值)` 函数形式**：可读性更强的解包方式
- **运行时断言**：`_duan_unwrap()` 在解包时检查空值
- **`OptionalTypeWrapper`**：内部表示 `数|空` 等可空类型
- **与 HM 推断协作**：解包后类型自动从 `数|空` 精化为 `数`
- **运算时检查**：可空值参与运算时必须先解包
- **段落参数检查**：非可空形参不能接受可空实参

#### 📦 模块系统与包管理
- **文件即模块**：每个 `.duan` 文件编译为独立模块，拥有独立符号表
- **依赖图拓扑排序**：使用 Kahn 算法确定编译顺序，避免依赖问题
- **循环依赖检测**：自动检测并报告模块间循环引用
- **`package.toml` 配置格式**：
  - `[package]`：包名、版本、描述、作者、入口文件
  - `[dependencies]`：本地依赖（`path`），预留 Git/注册表依赖
  - `[build]`：输出文件、目标运行时、优化开关
- **`PackageManager`**：统一管理项目加载、发现、编译流程
- **`PackageConfig`**：数据结构封装配置信息
- **`ModuleResolver`**：负责解析模块导入关系
- **`段言 init` 命令**：初始化新项目（创建 package.toml + main.duan）
- **`段言 build` 命令**：完整编译项目
- **跨模块 HM 类型推断**：导入的段落签名保留，可在当前模块继续推断
- **跨模块可空类型检查**：跨模块调用时保留可空性信息

#### 🎯 语法精简
- **移除 `结束` 关键字**：改为依赖缩进确定代码块范围（类似 Python）
- `如果...就...否则...` 与 `段落...` 现在仅靠缩进来标识范围

### 📝 文档

- 新增 `docs/HM全局类型推断系统.md`：详细说明类型推断架构、合一算法、推断流程
- 新增 `docs/可空类型unwrap系统.md`：详细说明可空类型表示、解包机制、编译期检查
- 新增 `docs/模块系统与包管理.md`：详细说明模块系统、包管理、依赖图构建
- 重写 `docs/API_REFERENCE.md`：基于 v1.0 最新 API 的完整参考
- 更新 `README.md`：加入三大特性章节与 v1.0 发行说明

### 🧪 测试

- **核心特性测试**：`tests/_test_three_features.py`（42 个测试，全部通过）
- **HM 推断测试**：`tests/_test_hm_inference.py`（30+ 测试）
- **可空类型测试**：`tests/_test_null_safety.py`（15+ 测试）
- **包管理测试**：`tests/_test_package_system.py`（10+ 测试）
- **其他测试**：`tests/` 目录 30+ 测试文件覆盖词法/语法/语义/代码生成

### ⚙️ CI/CD & 构建
- GitHub Actions：自动 pytest 测试 + 覆盖率报告（`.github/workflows/ci.yml`）
- `pyproject.toml`：完整项目元数据，支持 `pip install`
- 提供 `python -m cli.duan` 和 `python -m cli.duanc` 命令入口

### 🔧 架构优化

- 清理 `archived/` 废弃代码，整理项目结构
- 将 `_test_*.py` 从项目根目录移动到 `tests/`
- 统一测试基础设施（`conftest.py`）：添加 src 路径、提供标准 fixture
- 清理 `bootstrap/archive/` 历史代码
- 项目文件数从 400+ 精简到 ~200

---

## [0.1.0] - 2025-2026

**早期开发版本** — 此版本区间包含段言编译器的初始开发：
- 中文语法设计与解析器实现（ANTLR 版 + 手写版）
- AST 节点系统（dataclass + `__slots__` 两版）
- Python 后端代码生成器
- 面向对象特性：类、继承、接口
- 基本的循环/条件/异常语句
- 解释器与 REPL 探索

---

*变更日志遵循语义化版本：主版本号.次版本号.修订号*
