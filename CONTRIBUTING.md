# 贡献指南

感谢您对段言（Duan）编程语言的关注！我们欢迎各种形式的贡献，包括但不限于：

- 提交 Bug 报告
- 提出新功能建议
- 改进文档
- 提交代码修复
- 添加新的标准库模块
- 改进编译器性能

---

## 目录

1. [行为准则](#行为准则)
2. [开发环境搭建](#开发环境搭建)
3. [代码规范](#代码规范)
4. [分支管理](#分支管理)
5. [PR 流程](#pr-流程)
6. [提交信息规范](#提交信息规范)
7. [测试要求](#测试要求)
8. [文档要求](#文档要求)

---

## 行为准则

- 保持尊重和友善的沟通方式
- 接受建设性的批评和反馈
- 关注问题本身，而非人身攻击
- 维护包容、开放的社区氛围

---

## 开发环境搭建

### 前置要求

- Python 3.10 或更高版本
- Git
- 可选：VS Code（推荐安装段言扩展）

### 步骤

```bash
# 1. 克隆仓库
git clone https://github.com/skywalk163/duan.git
cd duan

# 2. 安装开发依赖
pip install -e .[dev]

# 3. 安装测试依赖
pip install pytest pytest-cov

# 4. 验证安装
python -m cli.duan --version
python -m cli.duan run examples/hello.duan
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行单元测试
python -m pytest tests/unit/

# 运行集成测试
python -m pytest tests/integration/

# 带覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 代码规范

### Python 代码规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范
- 使用 4 空格缩进（不使用 Tab）
- 行长度不超过 100 字符
- 使用有意义的变量名和函数名
- 函数和类必须包含文档字符串（docstring）

### 段言代码规范

- 使用 `设 变量 为 值` 的赋值语法（避免使用 `令 变量 = 值`）
- 使用 `段落 名称 接收 参数:` 定义函数（避免使用 `函数 名称(参数):`）
- 使用 `遍历 项 在 列表:` 进行遍历
- 使用中文关键字：`如果`/`否则`/`当`/`遍历`/`类`/`构造`/`己`
- 使用 4 空格缩进
- 在关键字和标识符之间保留空格：`设 甲 为 10`（而非 `设甲 为10`）

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量名 | 中文或英文，小写开头 | `姓名`, `user_name` |
| 函数名 | 中文或英文，动词开头 | `获取用户`, `calculate_sum` |
| 类名 | 中文或英文，大写开头 | `用户管理`, `UserManager` |
| 常量 | 全大写 | `MAX_COUNT`, `π` |
| 私有成员 | 下划线开头 | `_内部变量` |

---

## 分支管理

- `main` — 稳定发布分支，仅通过 PR 合并
- `develop` — 开发分支，日常开发的基础
- `feature/*` — 功能分支，从 develop 创建
- `fix/*` — 修复分支，从 develop 创建
- `docs/*` — 文档分支，从 develop 创建

### 分支命名示例

```
feature/添加类型推断系统
fix/修复列表越界错误
docs/更新API文档
```

---

## PR 流程

1. **创建 Issue** — 在提交 PR 前，先创建 Issue 描述你要解决的问题
2. **Fork 仓库** — 将仓库 fork 到你的账号
3. **创建分支** — 从最新的 `develop` 创建功能分支
4. **编写代码** — 遵循代码规范，确保测试通过
5. **提交 PR** — 填写 PR 模板，关联相关 Issue
6. **代码审查** — 至少一位维护者审查通过后方可合并

### PR 检查清单

- [ ] 代码符合项目规范
- [ ] 所有测试通过
- [ ] 新增代码有对应的测试覆盖
- [ ] 文档已更新（如需要）
- [ ] CHANGELOG.md 已更新
- [ ] 无遗留的调试代码或注释

---

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<类型>: <简短描述>

<详细描述（可选）>

<关联 Issue（可选）>
```

### 类型说明

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式调整 |
| `refactor` | 代码重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具链变更 |
| `perf` | 性能优化 |

### 示例

```
feat: 添加类型推断系统

实现基于 Hindley-Milner 的类型推断算法，支持
- 泛型函数类型推断
- 递归函数类型检查
- 多态类型推导

Closes #42
```

---

## 测试要求

- 所有新功能必须包含测试用例
- Bug 修复必须包含回归测试
- 测试覆盖率不低于 80%
- 测试文件放在 `tests/` 目录下，按类别分目录
- 测试命名：`test_<模块名>_<功能>.py`

### 测试类型

- **单元测试** (`tests/unit/`) — 测试单个模块/函数
- **集成测试** (`tests/integration/`) — 测试模块间交互
- **端到端测试** (`tests/e2e/`) — 测试完整编译-执行流程

---

## 文档要求

- 所有公开 API 必须有文档字符串
- 功能变更必须更新对应文档
- 文档使用 Markdown 格式
- 代码示例必须使用 v5.0 语法
- 文档更新后运行 `mkdocs build` 验证无错误

### 文档位置

- `docs/` — MkDocs 文档站
- 模块文档更新对应 `docs/` 下的文件
- API 文档通过 `tools/gen_api_docs.py` 自动生成

---

## 发布流程

1. 从 `develop` 创建 `release/vX.Y.Z` 分支
2. 更新版本号和 CHANGELOG.md
3. 运行完整测试套件
4. 创建 PR 合并到 `main`
5. 在 `main` 上打 Tag
6. 发布到 PyPI 和 VS Code Marketplace

---

再次感谢您的贡献！如有疑问，请在 GitHub 上创建 Issue 或 Discussion。