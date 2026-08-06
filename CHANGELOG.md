# 段言 CHANGELOG

## v5.1.0 (2026-08-06) — Level 7 类型注解系统 + 自举收敛验证

### 变量类型注解
- **新增 `设x为整数=10` 语法**：支持变量声明时标注类型
- 支持 7 种基本类型：`整数`/`文本`/`小数`/`布尔`/`空`/`列表`/`字典`
- 无初始值自动填充 `None`：`设x为整数` → `x: int = None`
- 完全向后兼容：`设x为10` 继续正常工作

### 函数参数和返回类型注解
- **参数类型注解**：`段add接收a整数,b整数返回整数`
- **函数返回类型**：`返回` 关键字后跟类型名
- 支持混合类型参数、无返回类型、向后兼容

### 复合类型注解
- **列表泛型**：`设arr为列表[整数]=[1,2,3]`
- **字典泛型**：`设map为字典[文本,整数]={"a":1}`
- 函数参数和返回值均支持复合类型

### 运行时类型检查
- **默认关闭**（零性能开销），通过 `开启类型检查` / `关闭类型检查` 控制范围
- 赋值时检查：`isinstance()` 验证类型，失败抛出 `TypeError`
- 函数参数自动检查类型是否匹配

### 编译器修复
- **括号表达式修复**：`(1加2)乘3` 正确生成 `(1 + 2) * 3`，不再丢失括号
- 同步修复 `bootstrap_level5.duan`、`level6_generated.py`、`level7_generated.py`

### 自举验证
- **Phase 1**：Level 6 无空格 + 纯缩进语法编译验证（9 用例）
- **Phase 2**：Level 7 类型注解语法编译验证（4 用例）
- **Phase 3**：生成代码语法正确性验证（2 用例）
- **Phase 4**：确定性编译收敛性验证（3 用例）
- **18/18 全部通过**

### 完整自举收敛
- **三次编译收敛**：`level7_generated.py` → 编译 `bootstrap_level5.duan` → 39KB → 二次编译 → 40KB → 三次编译 → 40KB → **完全一致**
- 验证了 Level 7 编译器能成功自举编译 35KB 的 `bootstrap_level5.duan` 源码，生成代码语法正确
- 自举生成代码可加载运行，完成二次编译，且第 2、3 轮输出收敛

### 测试覆盖
- 新增 Level 7 类型注解测试（20 用例）：7 组覆盖变量/函数/复合类型/运行时检查
- 新增 Level 7 自举验证测试（18 用例）：4 个相位验证编译收敛
- 回归测试：Level 5/6/7 共 **86 用例全部通过**

### 文档
- 新增 `docs/level7_spec.md`：Level 7 完整规格文档
- 更新 `docs/BOOTSTRAP_STRATEGY.md`：添加 Level 7 状态，版本 v1.4.0

### CLI 入口升级
- **duan6.py 升级为 Level 7 编译器**：引用 `level7_generated.py`，支持类型注解编译和运行
- 修复 BOM 字符读取问题，使用 `utf-8-sig` 编码
- 生成 `dist/duan7.exe`（6.99 MB），独立可执行文件，无需 Python 环境

## v5.0.1 (2026-08-05) — 自举编译器 Level 6 修复

### 异常处理深度追踪修复
- **comp_try 扫描逻辑**：找到 `捕获`/`最终` 后 depth 重置为 0，修复 finally 块被合并到 catch 块的 bug
- **try 嵌套 try**：内层 try 的 depth 追踪不再干扰外层 try 的边界检测

### 无空格词法分析器增强
- **ASCII 负号支持**：`-1` 中的负号不再被静默跳过，修复 w.process(-1) 变为 w.process(1) 的问题
- **关键字上下文匹配**：标识符读取过程中动态匹配关键字，支持 `foo接收a` 等无空格语法

### 纯缩进语法完整支持
- **compile_block 添加类定义处理**：`类` 关键字在函数体内不再被忽略
- **compile_stmts 添加类定义处理**：与 compile_block 保持一致
- **己 关键字处理**：`己.div(a,b)` 正确生成 `self.div(a,b)`，不再丢失 self 前缀

### 调试能力
- 添加 `调试模式` 全局开关
- comp_try 扫描循环、体边界计算、catch/finally 生成均添加详细日志
- comp_throw 添加异常表达式日志

### 测试覆盖
- 新增 Level 6 全面测试套件（26 用例）：无空格分词、纯缩进控制流、函数定义、异常处理、类定义、表达式运算、混合场景
- 边界场景测试（12 用例）：类方法异常、try 嵌套、类继承 + 异常传播、多层缩进连续 try-finally、类成员变量状态管理

## v5.0.0 (2026-08-04) — 类型推断性能演进（阶段一至三）

### 阶段一（v4.3.0）：低风险优化
- `is_instance` → `_ast_type_id` 整数分派：`type_inferencer.py` 中 39 处字符串比较替换为 O(1) 整数比较
- `TypeSubstitution` Copy-on-Write：`clone()` 延迟复制，减少 80% 对象创建开销
- `apply_substitution` 单例短路：`_SingletonType` 子类跳过完整替换链

### 阶段二（v4.4.0）：结构性优化
- 基于调用图的 HM 迭代优化：`_build_call_graph` + `_topo_sort_segments` 拓扑分层推断，无环段 1 轮、有环段 2 轮
- 增量推断缓存：`SegmentCacheEntry` + 源码哈希 + 依赖传播 + 级联失效
- `unify` 快速路径扩展：同引用快速返回 + 基本类型跳过发生检查 + 具体类型跳过递归

### 阶段三（v5.0.0）：架构级优化
- 并行段推断：`ThreadPoolExecutor` 拓扑分层并行推断，`snapshot()`/`merge_global()` 符号表隔离与合并
- 符号表全局索引：`_global_index` 扁平字典，O(1) 查找函数/类/枚举/trait
- 类型解析 LRU 缓存：`_parse_cache` 512 容量 + LRU 淘汰

### 文档与工具
- 新增 `docs/类型推断性能演进规划.md`：三阶段路线图、任务分解表、基准数据
- 新增 `bench_type_infer.py`：多维度基准测试脚本
- 新增 `profile_type_infer.py`：cProfile 性能分析脚本

## v4.2.0 (2026-08-04) — 可选类型系统与词法分析器修复

### Z 阶段：可选类型系统
- 增强 `type_checker.py`: GradedTypeChecker（三级检查：SIGNATURE/VARIABLE/EXPRESSION）
- 新增 `DuanTypeBridge`：Duan 类型 ↔ Python 类型桥接
- 新增 `CFGAnalyzer`：控制流分析（全路径返回检查、不可达代码检测）
- 增强 `type_inferencer.py`：HM 风格类型推断 + 类型缓存
- 增强 `parser_stmt.py`：支持复杂类型标注解析（泛型/联合类型/可选类型/函数类型）
- 增强 `compiler.py`：集成类型检查管道
- 8 个示例文件（Z1-Z8）：基本类型、泛型、联合类型、函数标注、分级检查、类型推断、类与接口、综合实战
- 53 个类型系统专项测试全部通过

### 词法分析器修复
- 在 `_COMPOUND_SAFE_SINGLE_KEYWORDS` 中补全 `加/减/乘/除`，避免复合词如"加法"被错误拆分
- 修复 `_tokenize_chinese_sequence` 中用户定义前缀匹配逻辑：当完整标识符本身是关键字时优先识别
- 新增 3 个词法分析器单元测试（18 子测试）
- 修复 `test_list_pop` 解析失败问题
- `test_L4_python_e2e.py` 添加网络可达性检测，动态跳过不可达网络测试

## v4.1.0 (2026-08-04) — 工具链生态与浏览器端支持

### R 阶段：L0 解析器补全
- 解析器 `parser_stmt.py` 全面支持 L0 单字关键字（若、遍、跳、过、返、试、捕、抛、终、导、出、否、接、承、配、自）
- 词法分析器 `lexer.py` 更新 `_COMPOUND_SAFE_SINGLE_KEYWORDS` 避免复合词误拆分
- 关键字定义 `keywords.py` 冻结 30 字 L0 核心字表

### S 阶段：LSP 语言服务器增强
- LSP 服务器 `lsp/duan_lsp.py` 补全 30 个 L0 关键字文档
- 支持悬停提示、自动补全、格式化功能
- 补全触发字符包含所有 L0 单字关键字

### T 阶段：格式化器与代码检查器
- 代码格式化器 `formatter.py` 更新 L0 关键字缩进和冒号规则
- 新建代码检查器 `linter.py`，包含 15 条规则（语法 S、风格 L、废弃 D、质量 Q）
- 支持 L0/L1 风格一致性检查、废弃语法检测、自动修复

### U 阶段：在线包注册表
- 包管理器 `duanpkg.py` 新增远程注册表支持（安装、发布、搜索）
- 新建注册表服务器 `registry_server.py`，提供 REST API（GET/POST 端点）
- 支持包存储、版本管理、下载分发

### V 阶段：AST 编译优化
- 新建 AST-based 优化器包 `optimizer/`（7 个模块）
- 常量折叠 `constant_fold.py`、死代码消除 `dead_code.py`、循环不变量 `loop_invariant.py`
- 窥孔优化 `peephole.py`、公共子表达式消除 `cse.py`、内联优化 `inline.py`

### W 阶段：交互式教程系统
- 新建 `playground/static/tutorial.js`，包含 6 章 20 课交互式教程
- 覆盖 L0 核心关键字、L1/L2 文体风格、L3 领域嵌入、L4 外部引用
- 支持代码验证、进度追踪、键盘导航、localStorage 持久化

### X 阶段：WebAssembly 编译目标
- 新建 `wasm_target.py`，支持 Pyodide 模式和独立 HTML 生成
- 新建 `playground/static/wasm.js`，Playground 集成 WASM 执行模式
- 支持 numpy/pandas/matplotlib 等常用包预加载

### Y 阶段：集成测试 + v4.1.0 发布
- 新建 `tests/test_v4_1_integration.py`，40 个集成测试覆盖全部新功能
- 版本号更新至 v4.1.0
- 现有测试集 132 通过（2 个已有边缘测试待修复）

## v4.0.0 (2026-08-04) — 五层分层语法架构正式发布

段言 v4.0 是自 v3.3 以来最大的一次架构升级，核心立意是**借鉴中文"一套字 + 多种文体 + 自然吸收专业符号"的智慧**，让段言既能服务青少年教学，也能用于商用大型项目。

本次发布作为 **duan4** 包独立发布（类似 python3 与 python2 的区别），与旧版 `duan` 包并存。

---

### A 阶段：L0 核心字表冻结 + 单字主形式 + 运算符符号化

- **L0 核心字表 30 字冻结**：`若设返段试捕抛终自承接配导出` `类空真跳遍当为否` `或且并` `打印输入` `和长` `引`，永不更改
- **单字关键字回归为主形式**：`若`/`设`/`返`/`段`/`试`/`捕`/`抛`/`终`/`自`/`承`/`接`/`配`/`导`/`出`
- **双字别名保留**：`如果`/`定义`/`返回`/`函数`/`段落` 等继续可用，不破坏现有代码
- **算术运算符符号化**：`+ - * / % ** //` 为主形式，`加上/减去/乘以/除以` 降级为 L1 白话体可选别名
- **嵌入块重命名**：`嵌入 Python:` → `引 Python:`，`嵌入 C:` → `引 C:`
- **迁移指南**：`v3.3_to_v4.0迁移指南.md` 完整覆盖所有变更

### B 阶段：L4 Python 引用层

- 实现 `引 Python:` 块的数据级互操作（参数传入/返回值传出，隔离命名空间）
- 5 个第三方包集成示例：numpy、pandas、matplotlib、requests、sklearn
- 目录：`examples/L4_python/`

### C 阶段：L3 领域嵌入层（嵌入块方式）

- SQL、正则表达式、数学公式三大领域 DSL 集成
- 6 个示例文件：`examples/L3_domain/`
- 不翻译专业符号，直接吸收到段言中

### D 阶段：L1 白话体 + L2 文言体双轨课程体系

- **L1 白话体**：10 课渐进式教程（`examples/L1_baihua/`），面向青少年教学
  - 中文标点 + 无空格 + 简化语法
- **L2 文言体**：学生成绩管理系统完整示例（`examples/L2_wenyan/`），面向商用项目
  - 英文标点 + 有空格 + 类型注解 + 类/模块/异常
- 双轨对照 README：`examples/L1_vs_L2_README.md`

### E 阶段：L3 原生语法 + L4 沙箱隔离

- **L3 原生语法**：SQL（sqlite3 参数化查询）、正则（命名捕获组）、数学（sympy 符号计算）
- **L4 沙箱隔离**：`exec()` 在独立命名空间中运行，`出` 关键字显式导出
- 修改文件：`src/code_generator.py`

### F 阶段：标准库增强 + 42 单元测试

- **日期时间模块**：日期格式化、时间差计算、时间戳转换、时区支持
- **统计模块**：均值、中位数、标准差、方差、分位数、线性回归
- **正则工具模块**：中文匹配、提取、替换、验证
- 42 条单元测试：`contrib/test_F3_三个增强模块.py`

### G 阶段：CI/CD + Playground 服务器

- **CI 工作流**（`.github/workflows/ci.yml`）：
  - `push`/`pull_request` 触发 `4.0dev` 和 `master` 分支
  - 自动安装 L3/L4 依赖 + 全量 pytest + 8 smoke demo
- **Playground Web API**（`playground/server.py`）：
  - `GET /api/demos/list` — 20+ demo 列表
  - `POST /api/demos/run?id=<id>` — 运行 demo
  - `GET /api/demos/<id>` — 获取 demo 详情
- **README 更新**：首页 v4.0 五层架构图

### H 阶段：语法规范终稿

- `docs/分层语法设计_v4.0.md` 状态更新为 "已实现"
- 版本历史从 v4.0.4 到 v4.0.11
- 打 `v4.0dev-HIJ` 标签

### I 阶段：contrib 模块直接导入

- `src/module_resolver.py` 搜索路径扩展至 `contrib/` 目录
- `.duan` 文件中可直接 `导入` contrib 模块，无需手动配置路径

### J 阶段：L4 C/Go/MoonBit 真实编译封装

- `src/code_generator.py` 增强：
  - C 语言：ctypes 动态加载 `.dll`/`.so`
  - Go 语言：`go build -buildmode=c-shared` 编译 + ctypes 加载
  - MoonBit 语言：`moon build` 编译 + ctypes 加载
- 平台适配：Windows `.dll` vs Linux/macOS `.so`
- 工具链缺失优雅降级：编译失败时提示安装指引
- 3 个示例：`examples/J阶段_L4_C_Go_MoonBit/`

### 修复

- 修复 `module_resolver.py` 中 `sys.path` 指向问题（`src/` 而非项目根目录）
- 修复 `code_generator.py` 中 f-string 语法错误（转义引号问题）
- 修复 `code_generator.py` 中 `from lexer import` 导入失败问题

---

## v3.5 (历史)

- T2-T4 语法增强 + DuMate 错误提示改善
- T1 深层链式赋值修复

## v3.3 (历史)

- 装饰器解析修复
- stdlib API 不匹配修复
- 缓存 TTL 问题修复
- duanpub 标准库集成（阶段 1-3）

## 更早版本

详见 git 历史。