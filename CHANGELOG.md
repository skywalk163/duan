# 段言 CHANGELOG

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