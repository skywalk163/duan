# 安全审计报告

**审计日期**: 2026-08-06  
**项目**: 段言 (Duan) v5.0.0  
**审计范围**: 源代码、依赖声明、配置文件、Web 服务

---

## 1. 依赖安全

### pyproject.toml 依赖检查

| 依赖 | 最低版本 | 状态 |
|------|----------|------|
| setuptools | >=61.0 | ✅ 基础构建依赖，无已知漏洞 |
| antlr4-python3-runtime | >=4.13.0 | ✅ 可选依赖，仅 ANTLR 后端使用 |
| pytest | >=7.0.0 | ✅ 开发依赖 |
| pytest-cov | >=4.0.0 | ✅ 开发依赖 |
| flake8 | >=6.0.0 | ✅ 开发依赖 |
| black | >=23.0.0 | ✅ 开发依赖 |
| isort | >=5.12.0 | ✅ 开发依赖 |
| mypy | >=1.0.0 | ✅ 开发依赖 |
| autopep8 | >=2.0.0 | ✅ 开发依赖 |
| prompt-toolkit | >=3.0.0 | ✅ 可选依赖，仅 REPL 使用 |
| sphinx | >=7.0.0 | ✅ 可选依赖，仅文档构建 |

**结论**: 依赖健康，无已知高危漏洞。所有依赖使用最低版本约束，未固定到已知有漏洞的版本。

---

## 2. 硬编码凭据扫描

### 2.1 高风险：硬编码 SSH 凭据

| 文件 | 行号 | 内容 | 严重程度 |
|------|------|------|----------|
| `tools/ai_copilot/remote_test_v8.py` | 14-16 | `SSH_HOST = "192.168.0.88"`, `SSH_USER = "trae"`, `SSH_PASS = "trae123"` | 🔴 高 |

**说明**: 该文件位于 gitignored 目录（`.gitignore` 第 198 行 `tools/ai_copilot/remote_*.py`），不会进入版本控制。但硬盘上仍存在明文凭据，建议删除或改为读取环境变量。

### 2.2 已修复：历史硬编码凭据

之前 18 个 SSH 脚本的硬编码凭据问题已在 v4.0 阶段通过 `ssh_config.py` + `.env` 模式修复，相关脚本已归档。

### 2.3 无风险：环境变量引用

以下文件通过环境变量读取凭据，为正确做法：

- `ssh_config.py`: `os.environ.get('SSH_PASS_TRAE', '')`, `os.environ.get('SUDO_PASS', '')`
- `tools/ai_copilot/diagnose_gguf.py`～`diagnose_gguf3.py`: `PASS = SSH_PASS_DUMATE2`（从环境变量导入）
- `tools/ai_copilot/deploy_remote.py`: `PASS = SSH_PASS_DUMATE`（从环境变量导入）

### 2.4 无风险：URL 解析中的 password 参数

`stdlib/duanpub/邮件.py`、`stdlib/duanpub/URL解析.py` 中的 `password` 参数为正常库函数参数，用于运行时配置，非硬编码凭据。

---

## 3. 安全模式检查

### 3.1 eval() 使用

| 文件 | 行号 | 用途 | 风险评估 |
|------|------|------|----------|
| `src/repl/executor.py` | 238, 279, 292 | REPL 表达式求值 | 🟡 低风险 — REPL 本身需要动态求值，属于预期行为 |

**结论**: 所有 eval 调用位于 REPL 上下文中，属于语言交互式解释器的正常功能，风险可控。

### 3.2 exec() 使用

| 文件 | 行号 | 用途 | 风险评估 |
|------|------|------|----------|
| `src/error_formatter.py` | 361, 406 | 运行时错误格式化 | 🟢 低风险 — 执行用户生成的代码 |
| `src/file_watcher.py` | 153 | 文件变更时执行 | 🟢 低风险 — 执行用户生成的代码 |
| `src/package_manager.py` | 495 | 包管理器执行 | 🟢 低风险 — 执行 Python 代码 |
| `src/profiler.py` | 90, 148 | 性能分析器 | 🟢 低风险 — 执行用户生成的代码 |
| `src/repl/executor.py` | 350 | REPL 代码执行 | 🟢 低风险 — REPL 核心功能 |
| `src/test_runner.py` | 129, 138 | 测试运行器 | 🟢 低风险 — 执行测试代码 |

**结论**: 所有 exec 调用是转译器/编译器的核心功能（将生成的 Python 代码交付执行），属于语言实现的本质需求。

### 3.3 subprocess 调用

| 文件 | 行号 | 命令 | shell=True | 风险评估 |
|------|------|------|------------|----------|
| `src/package_installer.py` | 806 | `git pull` | 否 | 🟢 安全 — 固定命令+参数列表 |
| `src/package_installer.py` | 831 | `git clone` | 否 | 🟢 安全 — 固定命令+参数列表 |
| `src/package_installer.py` | 987 | `git --version` | 否 | 🟢 安全 — 固定命令 |
| `src/llvm/compiler.py` | 349-980 | `cc/clang` 编译 | 否 | 🟢 安全 — 固定命令+参数列表 |
| `src/repl/core.py` | 113 | `cls/clear` | 否 | 🟢 安全 — 固定命令，清屏操作 |
| `contrib/进程.py` | 56 | 用户提供命令 | **是** | 🟡 中低风险 — 需在信任环境中使用 |

**结论**: 除 `contrib/进程.py` 外，所有 subprocess 调用使用列表形式传递参数，避免 shell 注入。`contrib/进程.py` 的 `shell=True` 是设计意图（执行系统命令），应在文档中注明安全警告。

### 3.4 路径遍历检查

| 文件 | 端点/函数 | 风险 | 状态 |
|------|-----------|------|------|
| `playground/server.py:874` | `GET /api/projects/<name>/files/<path:filepath>` | 未对 `filepath` 做 `../` 过滤 | 🟡 中风险 |
| `playground/server.py:889` | `PUT /api/projects/<name>/files/<path:filepath>` | 已做 `replace('/','_')` 处理 | 🟢 安全 |
| `playground/server.py:908` | `POST /api/projects/<name>/files` | 已做 `replace('/','_')` 处理 | 🟢 安全 |
| `playground/server.py:673` | `_get_project_dir()` | 已做 `..` 替换 | 🟢 安全 |

**结论**: `get_project_file` 端点缺少对 `filepath` 参数的路径遍历防护，与其他端点行为不一致。建议添加 `replace('..', '_')` 处理。

### 3.5 反序列化安全

**结论**: 未发现 `pickle.loads`、`yaml.load`（带 unsafe 模式）、`marshal.loads` 等不安全反序列化模式。

---

## 4. 配置安全

| 检查项 | 状态 |
|--------|------|
| `.env` 是否在 `.gitignore` 中 | ✅ 是（第 177 行） |
| `.env.example` 是否存在 | ✅ 是（v4.1.0 添加） |
| SSH 脚本是否 gitignored | ✅ 是（`ssh_*.py` 第 206 行） |
| AI Copilot 远程脚本是否 gitignored | ✅ 是（`tools/ai_copilot/remote_*.py` 第 198 行） |
| 敏感信息是否通过环境变量配置 | ✅ 是（`ssh_config.py` 模式） |

---

## 5. 总体风险评估

| 严重程度 | 问题数 | 说明 |
|----------|--------|------|
| 🔴 高 | 1 | 硬编码 SSH 凭据在 gitignored 文件中残留 |
| 🟡 中 | 1 | `get_project_file` 端点缺少路径遍历防护 |
| 🟢 低 | 2 | `shell=True` 在 `contrib/进程.py` 中；REPL 中 eval 使用 |
| ℹ️ 信息 | 0 | 核心 exec/subprocess 使用属于语言实现本质需求 |

### 建议修复项（优先级排序）

1. **高**: 删除 `tools/ai_copilot/remote_test_v8.py` 中的硬编码凭据，改用环境变量读取（与 `ssh_config.py` 一致）
2. **中**: 在 `playground/server.py:874` 的 `get_project_file` 中添加 `filepath` 的 `../` 过滤
3. **低**: 在 `contrib/进程.py` 文档字符串中添加 `shell=True` 的安全警告，提示不要在不可信输入上使用

---

*审计工具: 静态代码扫描 + 人工核查*  
*审计范围: src/、cli/、stdlib/、playground/、contrib/、tools/ai_copilot/ 目录*