# 贡献指南

感谢您对段言（Duan）编程语言的关注！我们欢迎各种形式的贡献，包括但不限于：

- 提交 Bug 报告
- 提出新功能建议
- 改进文档
- 提交代码修复
- 添加新的标准库模块
- 改进编译器性能
- 撰写技术博客
- 参与社区讨论和答疑

---

## 目录

1. [行为准则](#行为准则)
2. [开发环境搭建](#开发环境搭建)
3. [代码规范](#代码规范)
4. [开发流程](#开发流程)
5. [分支管理](#分支管理)
6. [PR 提交流程](#pr-提交流程)
7. [PR 检查清单](#pr-检查清单)
8. [提交信息规范](#提交信息规范)
9. [测试要求](#测试要求)
10. [文档要求](#文档要求)
11. [发布流程](#发布流程)
12. [获取帮助](#获取帮助)

---

## 行为准则

- **尊重他人**：保持尊重和友善的沟通方式，接纳不同背景和水平的贡献者
- **建设性反馈**：接受建设性的批评和反馈，关注问题本身，而非人身攻击
- **包容开放**：维护包容、开放的社区氛围，欢迎所有水平的开发者
- **协作精神**：优先考虑项目整体利益，乐于分享知识和经验
- **禁止行为**：不欢迎任何形式的骚扰、歧视、人身攻击和不当言论

---

## 开发环境搭建

### 前置要求

- **Python 3.10 或更高版本**（推荐 Python 3.12）
- **Git**（版本 2.30+）
- **VS Code**（推荐，安装段言扩展可获得语法高亮和 LSP 支持）
- **可选**：LLVM/Clang（用于 LLVM 后端编译，版本 14+）

### 快速开始

```bash
# 1. Fork 仓库
#    访问 https://github.com/skywalk163/duan 点击 Fork

# 2. 克隆你的 fork
git clone https://github.com/你的用户名/duan.git
cd duan

# 3. 添加 upstream 远程仓库
git remote add upstream https://github.com/skywalk163/duan.git

# 4. 安装开发依赖
pip install -e .[dev]

# 5. 安装测试依赖
pip install pytest pytest-cov pytest-xdist

# 6. 验证安装
python -m cli.duan --version
python -m cli.duan run examples/hello.duan
```

### 验证安装成功

```bash
# 运行一个简单的段言程序
echo '打印 "你好，段言！"' > test.duan
duan run test.duan
# 输出：你好，段言！
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 使用多核加速
python -m pytest tests/ -n auto

# 运行单元测试
python -m pytest tests/unit/

# 运行集成测试
python -m pytest tests/integration/

# 运行端到端测试
python -m pytest tests/e2e/

# 带覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html

# 运行特定测试文件
python -m pytest tests/unit/test_lexer.py -v

# 运行匹配特定名称的测试
python -m pytest tests/ -k "test_parser"
```

### 其他开发工具

```bash
# 交互式 REPL
duan repl

# 启动交互式教程
duan tutorial

# 查看 AST
duan ast examples/hello.duan

# 查看 Token 流
duan tokens examples/hello.duan

# 编译为 Python 代码
duan compile examples/hello.duan

# LLVM 编译（需要 LLVM/Clang）
duan compile examples/hello.duan --backend llvm-typed
```

---

## 代码规范

### Python 代码规范

段言的编译器基础设施使用 Python 编写，遵循以下规范：

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范
- 使用 **4 空格缩进**（不使用 Tab）
- 行长度不超过 **100 字符**
- 使用有意义的变量名和函数名
- 函数和类必须包含文档字符串（docstring）
- 类型注解：所有函数参数和返回值应包含类型注解

```python
# 好的示例
def calculate_sum(numbers: list[int]) -> int:
    """计算列表中所有数字的和。

    Args:
        numbers: 整数列表

    Returns:
        所有数字的和
    """
    return sum(numbers)
```

### 段言代码规范

段言代码遵循 v6.0 语法规范：

- 使用 `设 变量 为 值` 的赋值语法（避免使用 `令 变量 = 值` 等旧语法）
- 使用 `段落 名称 接收 参数:` 定义函数（避免使用 `函数 名称(参数):`）
- 使用 `遍历 项 于 列表:` 进行遍历（注意使用 `于` 而非 `在`）
- 使用中文关键字：`如果`/`否则`/`当`/`遍历`/`类`/`构造`/`己`
- 使用 4 空格缩进
- 在关键字和标识符之间保留空格：`设 甲 为 10`（而非 `设甲 为10`）
- 使用 `：`（中文冒号）结束语句块头部
- 使用 `。`（中文句号）结束语句（可选，但建议保持一致）

```段言
# 推荐的段言代码风格
设 姓名 为 "段言"

段落 问候 接收 名字:
    打印("你好，" + 名字 + "！")

遍历 数字 于 1 到 5:
    如果 数字 % 2 等于 0:
        打印(数字 + "是偶数")
    否则:
        打印(数字 + "是奇数")
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量名 | 中文或英文，小写开头 | `姓名`, `user_name` |
| 函数/段落名 | 中文或英文，动词开头 | `获取用户`, `calculate_sum` |
| 类名 | 中文或英文，大写开头 | `用户管理`, `UserManager` |
| 常量 | 全大写 | `MAX_COUNT`, `π` |
| 私有成员 | 下划线开头 | `_内部变量` |
| 文件名 | 中文或英文，小写 | `数据层.duan`, `main.duan` |
| 包名 | 中文或英文，简短 | `文件系统`, `JSON` |

### 格式化规范

- 段言代码：使用 `duan fmt` 命令自动格式化代码
- Python 代码：使用 `black` 和 `isort` 格式化

```bash
# 格式化段言代码
duan fmt myfile.duan

# 格式化 Python 代码
pip install black isort
black src/ tests/
isort src/ tests/
```

### 文件组织规范

```
模块名.duan          # 主模块文件
模块名/              # 包目录
├── __init__.duan    # 包初始化
├── 子模块1.duan     # 子模块
└── 子模块2.duan
```

---

## 开发流程

### 标准的贡献流程

```
1. 选择任务
    │
    ▼
2. 创建 Issue（描述你要解决的问题）
    │
    ▼
3. 同步最新代码
    │
    ▼
4. 创建功能分支
    │
    ▼
5. 编写代码（遵循代码规范）
    │
    ▼
6. 编写/更新测试
    │
    ▼
7. 本地运行测试（确保全部通过）
    │
    ▼
8. 提交代码（遵循提交信息规范）
    │
    ▼
9. 推送到你的 Fork
    │
    ▼
10. 创建 Pull Request
    │
    ▼
11. 代码审查（根据需要修改）
    │
    ▼
12. 合并 PR
```

### 详细步骤说明

#### 步骤 1：选择任务

- 查看 [Issue 列表](https://github.com/skywalk163/duan/issues)，寻找标注 `good first issue` 或 `help wanted` 标签的任务
- 在 Issue 下留言表示你想认领该任务
- 如果你是新手，建议从文档改进或简单 Bug 修复开始

#### 步骤 2：同步最新代码

```bash
# 确保你的 main 分支是最新的
git checkout main
git pull upstream main
git push origin main
```

#### 步骤 3：创建功能分支

```bash
# 从最新的 main 创建分支
git checkout -b feature/你的功能名称
# 或
git checkout -b fix/你的修复名称
# 或
git checkout -b docs/你的文档更新名称
```

#### 步骤 4：编写代码

- 遵循[代码规范](#代码规范)中的要求
- 保持改动范围聚焦，一个 PR 解决一个问题
- 如果是修复 Bug，先编写复现测试用例

#### 步骤 5：运行测试

```bash
# 运行所有测试确保不破坏现有功能
python -m pytest tests/

# 运行变更相关的测试
python -m pytest tests/unit/test_lexer.py -v
```

---

## 分支管理

### 分支策略

- `main` — **稳定发布分支**，仅通过 PR 合并，始终保持可发布状态
- `develop` — **开发分支**，日常开发的基础，包含最新功能
- `feature/*` — **功能分支**，从 `develop` 创建，合并回 `develop`
- `fix/*` — **修复分支**，从 `develop` 创建，合并回 `develop`
- `docs/*` — **文档分支**，从 `develop` 创建，合并回 `develop`
- `release/*` — **发布分支**，从 `develop` 创建，合并到 `main` 和 `develop`

### 分支命名示例

```
feature/添加类型推断系统
feature/实现模式匹配
fix/修复列表越界错误
fix/修复JSON解析编码问题
docs/更新API文档
docs/添加Web框架教程
release/v6.1.0
```

### 保持分支同步

```bash
# 定期从 develop 同步更新
git checkout feature/你的功能
git pull upstream develop
# 解决冲突后
git push origin feature/你的功能
```

---

## PR 提交流程

### 创建 PR 前的准备

1. **确保所有测试通过**：`python -m pytest tests/`
2. **确保代码格式正确**：Python 代码使用 `black`，段言代码使用 `duan fmt`
3. **确保文档已更新**：新增功能需要更新对应文档
4. **确保 CHANGELOG.md 已更新**：在 `[Unreleased]` 部分添加变更记录

### 提交 PR

1. 访问 [duan 仓库](https://github.com/skywalk163/duan)
2. 点击 "New Pull Request"
3. 选择你的 fork 和分支
4. 填写 PR 模板，包含：
   - **变更描述**：清晰描述变更内容和动机
   - **关联 Issue**：使用 `Closes #123` 格式关联 Issue
   - **变更类型**：选择对应的变更类型
   - **测试说明**：描述测试方法和结果
5. 点击 "Create Pull Request"

### 代码审查

- PR 创建后，维护者会进行审查
- 审查者可能会提出修改建议，请及时响应
- 修改后推送新 commit，PR 会自动更新
- 至少需要 **1 位维护者** 批准后方可合并

### PR 合并后的清理

```bash
# 切回 main 分支并更新
git checkout main
git pull upstream main

# 删除本地功能分支
git branch -d feature/你的功能

# 删除远程功能分支
git push origin --delete feature/你的功能
```

---

## PR 检查清单

提交 PR 前，请逐项检查：

- [ ] **代码规范**：代码符合项目代码规范
- [ ] **测试通过**：所有现有测试通过，无新增失败
- [ ] **测试覆盖**：新增代码有对应的测试覆盖
  - Bug 修复：包含回归测试
  - 新功能：包含单元测试
- [ ] **文档更新**：相关文档已更新（如需要）
- [ ] **CHANGELOG 更新**：CHANGELOG.md 已更新
- [ ] **无调试代码**：无遗留的调试代码或 `print` 语句
- [ ] **无冲突**：分支已与目标分支同步，无冲突
- [ ] **Commit 规范**：提交信息遵循 Conventional Commits 规范
- [ ] **单一职责**：一个 PR 只解决一个问题
- [ ] **本地验证**：代码在本地环境中测试通过

---

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<类型>: <简短描述>

<详细描述（可选）>

<关联 Issue（可选）>
```

### 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加模式匹配支持` |
| `fix` | Bug 修复 | `fix: 修复列表越界访问错误` |
| `docs` | 文档变更 | `docs: 更新 API 参考文档` |
| `style` | 代码格式调整 | `style: 格式化 parser_core.py` |
| `refactor` | 代码重构 | `refactor: 重构词法分析器架构` |
| `test` | 测试相关 | `test: 添加异常处理测试用例` |
| `chore` | 构建/工具链变更 | `chore: 更新 pytest 配置` |
| `perf` | 性能优化 | `perf: 优化词法分析器吞吐量 24%` |

### 提交信息示例

```
feat: 添加结构化模式匹配

实现 `匹配`/`模式` 语法，支持：
- 类型匹配模式（`整数 甲`、`字符串 乙`）
- 列表模式（`[整数 甲, 整数 乙]`）
- 字典模式（`{"name": 字符串 名}`）
- 守卫条件（`若 条件`）
- 通配符模式（`_`）

Closes #156
```

```
fix: 修复 JSON 解析时中文编码错误

当 JSON 字符串包含中文 Unicode 转义序列时，
解析器会错误地截断字符串。已修复转义序列处理逻辑。

Fixes #142
```

---

## 测试要求

### 基本原则

- 所有新功能**必须**包含测试用例
- Bug 修复**必须**包含回归测试
- 测试覆盖率**不低于 80%**
- 测试文件放在 `tests/` 目录下，按类别分目录
- 测试命名：`test_<模块名>_<功能>.py`

### 测试类型

| 类型 | 目录 | 说明 |
|------|------|------|
| **单元测试** | `tests/unit/` | 测试单个模块/函数，隔离外部依赖 |
| **集成测试** | `tests/integration/` | 测试模块间交互和协作 |
| **端到端测试** | `tests/e2e/` | 测试完整编译-执行流程 |

### 编写测试

```python
# tests/unit/test_lexer.py 示例
import pytest
from src.lexer import Lexer

class TestLexer:
    def test_中文关键字识别(self):
        """测试中文关键字是否能正确识别"""
        lexer = Lexer("设 变量 为 10")
        tokens = lexer.tokenize()
        assert tokens[0].type == "KEYWORD"
        assert tokens[0].value == "设"

    def test_字符串字面量(self):
        """测试字符串字面量解析"""
        lexer = Lexer('打印 "你好"')
        tokens = lexer.tokenize()
        assert tokens[1].type == "STRING"
        assert tokens[1].value == "你好"
```

### 段言语言测试

```段言
# tests/final_test.duan 示例
导入 断言工具。

段落 测试加法:
    设 结果 为 1 + 2
    断言相等(结果, 3, "1 + 2 应该等于 3")

段落 测试列表:
    设 列表 为 [1, 2, 3]
    列表.追加(4)
    断言相等(列表长度(列表), 4, "列表长度应该为 4")

测试加法()
测试列表()
打印("所有测试通过！")
```

### 运行测试的最佳实践

```bash
# 开发时频繁运行相关测试
python -m pytest tests/unit/test_lexer.py -v --tb=short

# 提交前运行完整测试套件
python -m pytest tests/ -x  # -x 在第一个失败时停止

# 生成覆盖率报告
python -m pytest tests/ --cov=src --cov-report=term-missing
```

---

## 文档要求

### 文档规范

- 所有公开 API **必须**有文档字符串
- 功能变更**必须**更新对应文档
- 文档使用 **Markdown** 格式
- 代码示例**必须**使用 **v6.0 语法**
- 文档更新后运行 `mkdocs build` 验证无错误
- 文档中的路径使用相对路径

### 文档位置

| 目录 | 内容 |
|------|------|
| `docs/` | MkDocs 文档站，包含入门指南、语法规范、教程等 |
| `docs/api/` | API 参考文档，通过 `tools/gen_api_docs.py` 自动生成 |
| `docs/blog/` | 技术博客文章 |
| `docs/community/` | 社区相关文档 |
| `docs/en/` | 英文文档 |
| `docs/tutorials/` | 交互式教程 |

### 文档字符串格式

```python
def 函数名(参数1: str, 参数2: int) -> bool:
    """函数简短描述。

    函数详细描述，说明函数的功能、行为和注意事项。

    Args:
        参数1: 参数1的描述
        参数2: 参数2的描述

    Returns:
        返回值的描述

    Raises:
        异常类型: 异常触发条件

    Examples:
        ```段言
        设 结果 为 函数名("test", 42)
        ```
    """
```

### 构建文档站

```bash
# 安装文档构建工具
pip install mkdocs mkdocs-material

# 本地预览
mkdocs serve

# 构建静态站点
mkdocs build

# 部署到 GitHub Pages
mkdocs gh-deploy
```

---

## 发布流程

1. **创建发布分支**：从 `develop` 创建 `release/vX.Y.Z` 分支
2. **更新版本号**：更新 `pyproject.toml`、`cli/duan.py` 等文件的版本号
3. **更新 CHANGELOG**：将 `[Unreleased]` 改为 `[X.Y.Z] - 日期`
4. **运行完整测试套件**：确保所有测试通过
5. **构建文档**：`mkdocs build` 确保文档构建成功
6. **创建 PR**：将 `release/vX.Y.Z` 合并到 `main` 和 `develop`
7. **打 Tag**：在 `main` 上打版本 Tag
8. **发布**：
   - PyPI 发布：`python -m build && python -m twine upload dist/*`
   - VS Code Marketplace 发布
   - GitHub Release 创建
9. **发布公告**：在 GitHub Discussions 和社区渠道发布更新公告

---

## 获取帮助

如果在贡献过程中遇到问题，可以通过以下渠道获取帮助：

### 文档

- [项目文档站](https://skywalk163.github.io/duan/)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [API 参考](docs/API_REFERENCE.md)

### 社区渠道

- **GitHub Issues**：报告 Bug 和功能建议
- **GitHub Discussions**：一般讨论、提问和技术交流
  - [一般讨论](https://github.com/skywalk163/duan/discussions/categories/general)
  - [问题求助](https://github.com/skywalk163/duan/discussions/categories/help)
  - [功能建议](https://github.com/skywalk163/duan/discussions/categories/ideas)
  - [展示分享](https://github.com/skywalk163/duan/discussions/categories/showcase)

### 常见问题

**Q: 我是一个新手，如何开始贡献？**
A: 建议从标注 `good first issue` 标签的任务开始，这些任务通常比较简单。你也可以从文档改进开始，比如修正错别字、改进示例代码等。

**Q: 我不确定某个功能是否属于 Bug，应该怎么办？**
A: 可以在 Discussions 中先发起讨论，或者创建一个 Issue 并标注为 `question` 标签。

**Q: 我的 PR 被要求修改，但我不确定如何修改？**
A: 在 PR 评论中提问，审查者会提供更详细的指导。你也可以在 Discussions 中寻求帮助。

**Q: 如何设置 LLVM 开发环境？**
A: 安装 LLVM 14+ 和 Clang，确保 `clang` 命令在 PATH 中。详细信息请参考[开发指南](docs/DEVELOPMENT_GUIDE.md)。

---

## 再次感谢

再次感谢您对段言的关注和贡献！无论您贡献的是代码、文档、测试还是社区讨论，每一份贡献都让段言变得更好。

让我们携手，共同推动中文编程语言的发展！🚀

---

> 段言项目地址：[https://github.com/skywalk163/duan](https://github.com/skywalk163/duan)
> 文档站：[https://skywalk163.github.io/duan/](https://skywalk163.github.io/duan/)
> 许可证：MIT