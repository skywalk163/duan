# 段言（DuanLang）编程语言

**段言**是一门基于中文的编程语言，采用中文关键字，让编程更加直观易懂。

## ✨ 核心特性

- 🀄 **中文语法**：全中文关键字，符合中文思维习惯
- 🚀 **自举编译**：编译器本身用段言编写（bootstrap_v3.duan，95 个函数），可自举编译
- ⚡ **LLVM 原生编译**：支持编译为原生机器码（EXE），无需 Python 运行时
- 📦 **双后端架构**：Python 解释执行 + LLVM 原生编译，灵活切换
- 🔧 **丰富标准库**：数学工具、字符串工具、列表工具、JSON、CSV、文件系统等
- 🔗 **C FFI 绑定**：支持调用 C 动态库，枚举/联合体/变长参数/回调/位域/函数指针

## 里程碑

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| v3.2 语法 | ✅ | 成熟稳定的中文编程语言 |
| 自举编译器 | ✅ | 用段言编写的段言编译器（62KB / 95 函数） |
| LLVM 后端 | ✅ | 支持编译为原生 EXE（clang 零错误） |
| 自举编译 | ✅ | 自举编译器可通过 LLVM 编译为原生 EXE（525KB） |
| AI Copilot | ✅ | 算力不足场景下的段言代码生成工具链 + LoRA 微调 |
| C FFI 绑定 | ✅ | 四阶段实现 + @C 语法标记：基础FFI → 指针/数组 → 枚举/联合体/变长参数 → typedef/位域/调试 |

## 快速开始（3 步跑通）

### 第 1 步：安装 Python

段言需要 **Python 3.10+**。检查你的版本：

```bash
python --version
# 输出应为 Python 3.10.x 或更高
```

> 没装 Python？去 [python.org](https://www.python.org/downloads/) 下载安装。
> Windows 用户安装时请勾选 **Add Python to PATH**。

### 第 2 步：安装段言

**方式 A：从源码安装（推荐，开发者适用）**

```bash
git clone https://gitcode.com/skywalk163/duan.git
cd duan
pip install -e .
```

**方式 B：从 PyPI 安装（仅使用）**

```bash
pip install duan
```

安装完成后验证：

```bash
duan --version
# 输出：段言编译器 v4.0
```

### 第 3 步：运行你的第一个程序

创建文件 `hello.duan`，写入以下内容：

```段言
打印 "你好，世界！"
```

运行它：

```bash
duan run hello.duan
# 输出：你好，世界！
```

就这么简单！无需安装任何额外依赖。

## 示例程序

项目自带示例文件，可以直接运行：

```bash
# 运行 Hello World 示例（阶乘、循环）
duan run examples/hello.duan

# 输出：
# 你好，世界！
# 5的阶乘是：
# 120
# 1到10的和：
# 55
# 程序运行完成！
```

## 语法入门

### 变量

```段言
令 姓名 = "张三"
令 年龄 = 25
打印 姓名
打印 年龄
```

### 函数（段落）

```段言
函数 加法(a, b):
    返回 a + b

打印 加法(3, 5)    # 输出：8
```

### 条件语句

```段言
令 分数 = 85

如果 分数 >= 90:
    打印 "优秀"
否则如果 分数 >= 60:
    打印 "及格"
否则：
    打印 "不及格"
```

### 循环

```段言
# 当循环
令 计数 = 0
当 计数 < 5:
    打印 计数
    令 计数 = 计数 + 1

# 遍历循环
遍历 项 于 1至5:
    打印 项
```

### 字符串

```段言
令 名字 = "段言"
打印 "你好，" + 名字 + "！"
```

## 📖 教程

- [**30 分钟入门段言**](docs/30分钟入门段言.md) — 零基础入门教程，涵盖变量、运算、条件、循环、函数、列表、类、异常处理、文件操作、模块系统
- [**端到端实战教程**](docs/端到端实战教程.md) — 从零构建天气查询程序，涵盖 duanpub 库导入、文件操作、异常处理和 Python 代码转译

## 命令行工具

```bash
# 运行段言程序（默认使用 SRC 后端，无需额外依赖）
duan run hello.duan

# 编译为 Python 文件
duan compile hello.duan -o hello.py

# 语法检查
duan check hello.duan

# 类型检查（三级：签名/变量/表达式）
duan check hello.duan --type-check 表达式

# 独立类型检查
duan type-check hello.duan --level 变量

# 查看 Token 流
duan tokens hello.duan

# 查看 AST
duan ast hello.duan

# 初始化新项目
duan init myproject
```

### 包管理

```bash
# 初始化新包（创建 package.toml 与 主.duan）
duan pkg init myproject

# 编译项目
duan pkg -p myproject build

# 运行项目
duan pkg -p myproject run

# LLVM 原生编译
duan pkg -p myproject native -o output.exe
```

### 后端选择

段言支持多种编译后端：

| 后端 | 命令 | 说明 | 额外依赖 |
|------|------|------|---------|
| **SRC**（默认） | `duan run hello.duan` | 手写解析器，v3.2 语法，Python 解释执行 | **无** |
| ANTLR | `duan run hello.duan --backend antlr` | ANTLR 解析器，兼容模式 | `pip install antlr4-python3-runtime` |
| LLVM | `duan compile hello.duan --backend llvm-typed -o hello.exe` | 原生编译为 EXE | 安装 LLVM/Clang |

**新手建议**：直接用默认的 SRC 后端即可，无需任何额外安装。

### 编译为 EXE

如需编译为 Windows 可执行文件：

```bash
# 方式1：使用 PyInstaller（简单，但文件较大）
pip install pyinstaller
duan compile hello.duan -o hello.exe

# 方式2：使用 LLVM 原生编译（需要安装 LLVM）
duan compile hello.duan --backend llvm-typed -o hello.exe
```

## AI Copilot（算力不足时让 AI 写段言代码）

段言提供完整的 AI 辅助工具链，即使只有小模型（7B 以下），也能帮你写出正确的段言代码。

> **模型已上线**：训练好的段言翻译器模型已发布到 Ollama 官网，可直接拉取使用：
> ```bash
> ollama pull airoot/duan-translator
> ```
> 模型主页：[https://ollama.com/airoot/duan-translator](https://ollama.com/airoot/duan-translator)
> 详细使用说明见 [段言翻译器使用指南](段言翻译器使用指南.md)

### 核心思路

```
用户需求 → AI 生成 Python → 微调模型翻译为段言 → duan ai check 验证
```

1. 大模型生成 Python 代码（擅长）
2. 微调后的小模型将 Python 翻译为段言（专精）
3. `duan ai check` 检查暗坑和后端兼容性

### 使用方式

```bash
# 一键生成段言代码（自动组装速查卡 + 片段 + 暗坑提示）
duan ai generate "写一个二分查找函数"
duan ai generate "排序算法" --model-size small   # 小模型用精简提示
duan ai generate "文件读写" --model-size large   # 大模型用完整提示

# 修复出错的段言代码
duan ai fix hello.duan "第3行语法错误"

# 查看语法速查卡（复制给 AI 当参考）
duan ai card

# 查看代码片段模板
duan ai snippets

# 后端感知检测（类关键字→提示切换 LLVM 后端）
duan ai check hello.duan
```

### LoRA 微调训练

提供三套微调方案，覆盖从 0.3B 到 8B 的模型：

| 方案 | 模型 | 显存 | 训练时间 | 定位 |
|------|------|------|----------|------|
| ERNIE-4.5-0.3B | 0.3B | ~4 GB | 10-30 分钟 | 轻量级窄翻译 |
| Qwen3.5-2B | 2B | ~5 GB | ~10 分钟 | 开发调试首选 |
| Qwen3-8B | 8B | ~22 GB | ~30 分钟 | 生产部署，效果最强 |

```bash
cd tools/ai_copilot

# 开发调试：2B 模型快速验证
python train_lora_7b.py --model-preset qwen3.5-2b

# 生产部署：8B 模型最高质量
python train_lora_7b.py --model-preset qwen3-8b

# 显存不够：QLoRA 4bit 量化
python train_lora_7b.py --model-preset qwen3.5-2b --qlora
```

详细文档：
- [LoRA 微调指南（Qwen3-8B / Qwen3.5-2B）](tools/ai_copilot/README_LoRA7B.md)
- [ERNIE 微调指南（0.3B）](tools/ai_copilot/README_SFT.md)
- [Kaggle 双 T4 + Swift 训练指南](tools/ai_copilot/RUN_GUIDE.md#kaggle-双-t4--swift-训练指南) — 免费 GPU 训练，新手友好
- [完整运行指南](tools/ai_copilot/RUN_GUIDE.md)

## 标准库

段言提供丰富的中文标准库，位于 `stdlib/` 目录，包含 **14个阶段**、**60+个模块**：

```段言
从 数学工具 导入 阶乘
打印 阶乘(10)
```

### 阶段1：基础核心模块

| 模块 | 说明 |
|------|------|
| builtins | 内置函数 |
| 数学 | 绝对值、三角函数、阶乘、统计函数 |
| 字符串处理 | 分割、拼接、替换、查找、截取 |
| 文件系统 | 读写文件、目录操作、路径处理 |
| 日志 | 日志记录 |
| JSON | 解析与序列化 |

### 阶段2：数据结构与工具

| 模块 | 说明 |
|------|------|
| 日期时间 | 日期解析/格式化、时区转换 |
| 随机 | 随机数生成、UUID |
| 集合 | 集合操作（并集/交集/差集） |
| 迭代工具 | 计数器、排列组合 |
| 数据结构 | 栈、队列、二叉搜索树 |

### 阶段3：系统与网络

| 模块 | 说明 |
|------|------|
| 网络请求 | HTTP 请求（GET/POST） |
| 进程 | 进程管理 |
| 线程 | 线程创建与管理、锁、信号量 |
| 时间管理 | 计时器、定时器 |

### 阶段4：编码与安全

| 模块 | 说明 |
|------|------|
| 编码解码 | Base64、URL编码 |
| 加密 | 对称/非对称加密 |
| 哈希 | MD5、SHA系列哈希 |

### 阶段5：高级特性

| 模块 | 说明 |
|------|------|
| 装饰器 | 缓存、重试、计时、日志等11种装饰器 |
| 上下文管理器 | 临时文件、资源管理等13种上下文管理器 |

### 阶段6：数据科学与计算

| 模块 | 说明 |
|------|------|
| 统计函数 | 平均数、标准差、协方差、相关系数 |
| 矩阵运算 | 矩阵创建、运算、行列式 |
| 线性代数 | 向量、矩阵运算、特征值 |

### 阶段7：文本处理与解析

| 模块 | 说明 |
|------|------|
| 正则表达式 | 正则匹配、捕获、替换 |
| 模板引擎 | 变量替换、条件渲染 |
| CSV读写器 | CSV/TSV读写 |
| JSON解析器 | JSON解析与生成 |

### 阶段8：Web 与通信协议

| 模块 | 说明 |
|------|------|
| HTTP客户端 | GET/POST、Cookie、重定向 |
| HTTP服务端 | 路由、中间件、静态文件 |
| WebSocket支持 | 长连接、双向通信 |
| SMTP邮件 | 发送邮件、附件 |
| URL工具 | 查询参数、编码 |

### 阶段9：测试与调试

| 模块 | 说明 |
|------|------|
| 单元测试框架 | 断言、测试套件、夹具 |
| Mock工具 | 模拟对象、打桩 |
| 性能基准测试 | 计时、内存测量 |
| 日志系统增强 | 分级、滚动、格式化 |
| 断言工具 | 丰富断言类型 |

### 阶段10：元编程与代码生成

| 模块 | 说明 |
|------|------|
| AST操作 | 解析、修改、生成代码 |
| 类型系统增强 | 泛型、类型校验 |
| 对象池缓存 | 对象复用、LRU缓存 |
| 插件系统 | 动态加载、热更新 |
| DSL支持 | 领域特定语言解析 |

### 阶段11：安全与权限

| 模块 | 说明 |
|------|------|
| OAuth_JWT认证 | 令牌生成与验证 |
| 访问控制 | RBAC/ACL角色权限管理 |
| 加密协议 | 对称/非对称加密、数字签名 |
| 输入校验净化 | SQL注入防护、XSS过滤 |
| 审计日志 | 操作记录、追溯 |

### 阶段12：并发与分布式

| 模块 | 说明 |
|------|------|
| Actor模型 | 消息传递、并发单元 |
| 分布式锁 | 内存分布式锁、读写锁、信号量 |
| 消息队列 | 生产者消费者、发布订阅、工作队列 |
| 任务队列调度器 | 定时任务、重试机制、Cron调度 |
| 工作流引擎 | DAG任务编排、并行执行 |

### 阶段13：系统工具与补充库

| 模块 | 说明 |
|------|------|
| 系统接口 | 环境变量、命令行参数、进程信息、路径操作 |
| 外部命令 | 命令执行、管道、超时、环境隔离 |
| 参数解析 | 命令行参数解析、子命令、自动帮助 |
| 临时文件 | 临时文件/目录创建、上下文自动清理 |
| 美化输出 | 数据结构格式化、表格、JSON美化 |
| 复制 | 浅复制、深复制 |
| 文件匹配 | glob通配符、fnmatch匹配 |
| 对象序列化 | pickle序列化、JSON序列化、文件持久化 |
| 枚举 | 枚举类型定义、成员遍历、值查找 |
| 文本差异 | 文本比较、相似度、差异输出 |
| 压缩 | ZIP/GZIP/zlib压缩解压、CRC32校验 |
| 高级文件 | 复制、删除、目录大小、磁盘使用、文件树 |
| 字符串常量 | 字符常量、字符分类、字符串操作工具 |
| 函数工具 | 偏函数、归约、管道、组合、柯里化 |
| 集合工具 | 默认字典、有序字典、计数器、双端队列、命名元组 |

### 阶段14：C FFI 外部函数接口

段言支持直接调用 C 动态库（.so/.dll），通过四阶段演进实现完整的 C 语言互操作：

| 功能 | 语法 | 说明 |
|------|------|------|
| 加载库 | `加载库 "路径" 为 别名` | 加载 C 动态库 |
| 函数声明 | `外部 段落 名称 接收 参数 返回 类型 在 库` | 声明 C 函数 |
| 结构体 | `外部 结构体 名称 { 字段: 类型 }` | 定义 C 结构体 |
| 回调 | `外部 回调 名称 接收 参数 返回 类型` | 定义 C 回调类型 |
| 指针操作 | `取地址` / `解引用` / `指针偏移` | 指针运算 |
| 数组操作 | `创建数组` / `设置数组` | C 数组管理 |
| 内存管理 | `分配内存` / `释放内存` | 手动内存管理 |
| 错误处理 | `捕获 外部错误 为 变量：` | FFI 异常捕获 |
| 枚举 | `外部 枚举 名称 { 成员 = 值 }` | C 枚举映射 |
| 联合体 | `外部 联合体 名称 { 字段: 类型 }` | C union 支持 |
| 变长参数 | `外部 变长参数 段落 名称 接收...` | printf 风格 |
| 类型别名 | `外部 类型别名 名称 为 类型` | C typedef |
| 位域 | `外部 位域 名称 : 类型 { 字段: 位数 }` | C bitfield |
| 函数指针 | `外部 函数指针 名称 接收 参数 返回 类型` | C 函数指针类型 |
| 调试 | `外部 调试 { 开启, 记录调用 }` | FFI 调用日志 |
| 预处理器宏 | `外部 宏 名称 为 值` | C 宏定义 |
| `@C` 标记 | `@C 段落/结构体/枚举 ...` | 独立语法标记，与 `外部` 并行 |

```段言
加载库 "libm.so" 为 math。
外部 段落 平方根 接收 输入: 小数 返回 小数 在 math。
外部 结构体 点 { x: 小数, y: 小数 }。
外部 枚举 颜色 { 红 = 0, 绿 = 1, 蓝 = 2 }。

设 结果 为 平方根(16.0)   # 调用 C 的 sqrt 函数
打印 结果                  # 输出: 4.0

# 或使用 @C 语法标记（更简洁）
@C 段落 绝对值 接收 甲: 小数 返回 小数 在 math。
```

> 详细文档：[C FFI 绑定指南](docs/ffi.md)

## 语法参考（v4.0）

| 语法 | 说明 | 示例 |
|------|------|------|
| `令 X = Y` | 变量声明（推荐） | `令 年龄 = 25` |
| `设 X 为 Y` | 变量声明（中文风格） | `设 年龄 为 25` |
| `函数 名(参数):` | 函数定义（推荐） | `函数 加法(a, b):` |
| `段落 名 接收 参数：` | 函数定义（中文风格） | `段落 加法 接收 a, b：` |
| `如果 条件：` | 条件语句 | `如果 年龄 > 18：` |
| `否则如果 条件：` | 否则如果 | `否则如果 年龄 > 12：` |
| `否则：` | 否则 | `否则：` |
| `当 条件：` | 当循环 | `当 计数 < 10：` |
| `遍历 变量 于 列表：` | 遍历循环 | `遍历 i 于 1至10：` |
| `返回 X` | 返回值 | `返回 a + b` |
| `打印 X` | 打印输出 | `打印 "你好"` |
| `从 模块 导入 符号` | 从模块导入 | `从 数学工具 导入 阶乘` |
| `导入 模块` | 导入整个模块 | `导入 数学工具` |
| `导出 符号列表` | 导出符号 | `导出 加法, 减法` |
| `跳出` | 跳出循环 | `跳出` |
| `跳过` | 跳过本次循环 | `跳过` |

### 运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `+` / `加上` | 加法 | `a + b` |
| `-` / `减去` | 减法 | `a - b` |
| `*` / `乘以` | 乘法 | `a * b` |
| `/` / `除以` | 除法 | `a / b` |
| `%` / `取余` | 取模 | `a % b` |
| `**` / `幂` | 幂运算 | `a ** b` |
| `//` / `整除` | 整除 | `a // b` |
| `==` / `等于` | 相等比较 | `a == b` |
| `!=` / `不等于` | 不等比较 | `a != b` |
| `>` / `大于` | 大于 | `a > b` |
| `<` / `小于` | 小于 | `a < b` |
| `>=` / `大于等于` | 大于等于 | `a >= b` |
| `<=` / `小于等于` | 小于等于 | `a <= b` |
| `且` / `或` / `非` | 逻辑运算 | `a 且 b` |

### 复合赋值

| Python | 段言 | 说明 |
|--------|------|------|
| `x += y` | `设 x 为 x 加上 y` | 加法复合赋值 |
| `x -= y` | `设 x 为 x 减去 y` | 减法复合赋值 |
| `x *= y` | `设 x 为 x 乘以 y` | 乘法复合赋值 |
| `x /= y` | `设 x 为 x 除以 y` | 除法复合赋值 |
| `x //= y` | `设 x 为 x 整除 y` | 整除复合赋值 |
| `x %= y` | `设 x 为 x 取余 y` | 取模复合赋值 |
| `x **= y` | `设 x 为 x 幂 y` | 幂复合赋值 |

### 类与面向对象

```段言
类 动物：
    属性 名字
    构造 接收 名字：
        己.名字 = 名字
    函数 介绍():
        打印 "我叫" + 己.名字

类 狗 继承 动物：
    函数 叫声():
        打印 "汪汪汪"

令 小狗 = 狗("旺财")
小狗.介绍()
小狗.叫声()
```

### 类型注解与检查

段言支持三级类型检查（签名级/变量级/表达式级）：

```段言
函数 加法(甲: 数, 乙: 数) -> 数:
    返回 甲 + 乙

严格 函数 计算(输入: 字符串) -> 字典:
    ...
```

```bash
# 类型检查
duan check hello.duan --type-check 签名
duan type-check hello.duan --level 表达式
```

## 项目结构

```
duan/
├── src/                 # 核心编译器（活跃维护）
│   ├── lexer.py         # 词法分析器
│   ├── parser_core.py   # 解析器核心
│   ├── parser_stmt.py   # 语句解析
│   ├── parser_expr.py   # 表达式解析
│   ├── ast_nodes_v3.py  # AST 节点定义
│   ├── code_generator.py     # Python 代码生成
│   ├── code_generator_unified.py  # 统一代码生成
│   ├── compiler.py      # 编译器主体
│   ├── type_checker.py  # 三级类型检查器
│   ├── type_inferencer.py   # HM 类型推断
│   ├── package_manager.py   # 包管理器
│   ├── module_resolver.py   # 模块解析器
│   ├── llvm/            # LLVM 后端
│   │   ├── codegen_typed.py  # LLVM 代码生成（typed 模式）
│   │   └── compiler.py       # LLVM 编译入口
│   └── optimizer/       # 代码优化器
├── cli/                 # 命令行工具
│   └── duan.py          # 主入口（duan 命令，含 pkg 子命令）
├── stdlib/              # 标准库（60+ 模块）
│   ├── FFI.py          # C FFI 运行时模块（~500 行）
│   ├── FFI.duan        # C FFI 段言实现
├── lsp/                 # LSP 语言服务器
├── debug-adapter/       # DAP 调试适配器
├── tools/               # 调试器等工具
│   └── ai_copilot/      # AI 辅助工具链
│       ├── syntax_card.py          # 语法速查卡生成
│       ├── snippets.py             # 代码片段模板
│       ├── prompt_generator.py     # prompt 生成器
│       ├── pipeline.py             # 一揽子管线
│       ├── build_sft_dataset.py    # SFT 训练集构造
│       ├── train_lora_7b.py        # Qwen3-8B/3.5-2B LoRA 微调
│       ├── train_lora_7b.ipynb     # Notebook 调试版
│       ├── train_sft.py            # ERNIE-4.5-0.3B 微调
│       ├── sft_dataset.jsonl       # 881 条训练数据
│       ├── README_LoRA7B.md        # LoRA 微调文档
│       └── README_SFT.md           # ERNIE 微调文档
├── demos/               # 示范项目
├── examples/            # 示例程序
├── tests/               # 测试
│   ├── test_ffi.py      # C FFI 第一阶段测试（16 个）
│   ├── test_ffi_phase2.py  # C FFI 第二阶段测试（17 个）
│   ├── test_ffi_phase3.py  # C FFI 第三阶段测试（23 个）
│   ├── test_ffi_phase4.py  # C FFI 第四阶段测试（28 个）
│   ├── test_ffi_at_c.py    # @C 语法标记测试（19 个）
│   ├── unit/            # 单元测试
│   ├── integration/     # 集成测试
│   └── e2e/            # 端到端测试
└── docs/                # 文档
```

## 开发

### 环境准备

```bash
# 克隆项目
git clone https://gitcode.com/skywalk163/duan.git
cd duan

# 安装（开发模式）
pip install -e .

# 安装开发工具（可选）
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有核心测试
python -m pytest tests/test_parser.py tests/test_lexer.py tests/test_async.py -v

# 运行单元测试
python -m pytest tests/unit/ -v

# 运行全部测试
python -m pytest tests/ -v
```

### 代码格式

项目使用 UTF-8 编码和中文注释。

## 常见问题

### Q: 运行时报 `No module named 'antlr4'`

**A:** 这是 ANTLR 后端的依赖。两种解决方案：

1. **用默认 SRC 后端**（推荐，无需额外安装）：
   ```bash
   duan run hello.duan
   ```

2. **安装 ANTLR 运行时**（如需使用 `--backend antlr`）：
   ```bash
   pip install antlr4-python3-runtime
   ```

### Q: `pip install antlr4` 报错

**A:** 正确的包名是 `antlr4-python3-runtime`，不是 `antlr4`：
```bash
pip install antlr4-python3-runtime
```

### Q: 编译为 EXE 失败

**A:** 两种方式：

1. **PyInstaller 方式**（简单）：
   ```bash
   pip install pyinstaller
   duan compile hello.duan -o hello.exe
   ```

2. **LLVM 方式**（原生编译，需安装 LLVM）：
   ```bash
   duan compile hello.duan --backend llvm-typed -o hello.exe
   ```

### Q: Python 版本要求

**A:** 段言需要 Python 3.10 或更高版本。检查版本：
```bash
python --version
```

## 文档

- [语法规范 v3.2](docs/统一语法规范_v3.2.md)
- [快速开始](docs/getting-started.md)
- [架构设计](docs/architecture.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)
- [用户手册](docs/USER_MANUAL.md)
- [工具链](docs/tools.md)（CLI、调试器、LSP、AI Copilot）
- [AI Copilot LoRA 微调指南](tools/ai_copilot/README_LoRA7B.md)
- [AI Copilot ERNIE 微调指南](tools/ai_copilot/README_SFT.md)

## 许可证

本项目采用 MIT 许可证。
