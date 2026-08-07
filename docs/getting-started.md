# 快速开始

> **适用版本：** v6.0
> **最后更新：** 2026-08-07

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install duan
```

安装后即可使用 `duan` 命令：
```bash
duan --version
duan --help
```

### 从源码安装

```bash
git clone https://github.com/skywalk163/duan.git
cd duan
pip install -e .
```

## 3 步跑起来

### 第1步：创建程序

创建文件 `hello.duan`：

```段言
打印 "你好，段言！"
```

### 第2步：运行

```bash
duan run hello.duan
```

### 第3步：验证

```
你好，段言！
```

看到输出就说明安装成功！

## v6.0 语法示例

### 变量声明

```段言
设 姓名 为 "张三"
设 年龄 为 25
设 分数 为 95.5
设 列表 为 [1, 2, 3, 4, 5]
设 字典 为 {"名字": "张三", "年龄": 25}
```

### 段落（函数）

```段言
段落 加法 接收 甲, 乙：
    返回 甲 + 乙

设 结果 为 加法(3, 5)
打印 结果  # 输出：8
```

### 条件判断

```段言
设 分数 为 85

如果 分数 >= 90：
    打印 "优秀"
否则如果 分数 >= 60：
    打印 "及格"
否则：
    打印 "不及格"
```

### 循环

```段言
# 遍历范围
遍历 i 在 1 到 5：
    打印 i

# 遍历列表
设 水果 为 ["苹果", "香蕉", "橘子"]
遍历 水果 为 果：
    打印 果

# 当循环
设 计数 为 0
当 计数 < 5：
    打印 计数
    设 计数 为 计数 + 1
```

### 类与对象

```段言
类 动物：
    属性 名字

    构造 接收 名字：
        己.名字 为 名字

    段落 介绍 接收：
        打印(f"我叫{己.名字}")

设 小狗 为 动物("旺财")
小狗.介绍()
```

### 异常处理

```段言
尝试：
    设 结果 为 10 / 0
捕获 错误：
    打印("出错了：" + 转字符串(错误))
最终：
    打印("操作结束")
```

### 模块导入

```段言
导入 数学

设 结果 为 数学.平方根(16)
打印 结果  # 输出：4.0

# 从模块导入特定函数
从 数学 导入 阶乘
打印 阶乘(5)  # 输出：120
```

### 模式匹配

```段言
匹配 值：
    情况 1：
        打印("一")
    情况 2：
        打印("二")
    默认：
        打印("其他")
```

### 异步编程

```段言
异步 段落 获取数据 接收 url：
    返回 等待 请求(url)

异步 范围：
    设 数据 为 等待 获取数据("https://api.example.com")
    打印 数据
```

## CLI 命令

### 常用命令

```bash
duan run hello.duan         # 解释执行
duan compile hello.duan     # 编译为 Python
duan ast hello.duan         # 显示 AST
duan tokens hello.duan      # 显示 Token 流
duan check hello.duan       # 语法检查
duan repl                   # 交互式编程环境
duan tutorial               # 交互式教程
```

### 包管理命令

```bash
duan pkg init myproject     # 初始化新项目
duan pkg -p myproject build # 编译项目
duan pkg -p myproject run   # 运行项目
duan pkg -p myproject native -o output.exe  # LLVM 原生编译
```

### AI 辅助命令

```bash
duan ai generate "写一个冒泡排序"  # AI 生成代码
duan ai fix hello.duan "第3行语法错误"  # 修复代码
duan ai card  # 查看语法速查卡
duan ai check hello.duan  # 后端兼容性检测
```

### 后端选择

```bash
# SRC 后端（默认，无需额外依赖）
duan run hello.duan

# ANTLR 后端（兼容旧语法）
duan run hello.duan --backend antlr

# LLVM 后端（原生编译）
duan compile hello.duan --backend llvm-typed -o hello.exe
```

## 示例程序

项目包含多个示例程序：

```bash
# 运行示例
duan run examples/hello.duan
duan run examples/basic.duan
duan run examples/class_example.duan
```

示例列表：
- `examples/hello.duan` - Hello World
- `examples/basic.duan` - 基础语法
- `examples/class_example.duan` - 类示例
- `examples/hanoi.duan` - 汉诺塔算法
- `examples/calculator.duan` - 计算器
- `examples/student_management.duan` - 学生管理系统

## 更多资源

- 📖 [30 分钟入门段言](30分钟入门段言.md) — 零基础入门教程
- 📚 [语法规范](syntax.md) — 完整语法参考
- 🛠️ [工具链](tools.md) — CLI、LSP、调试器、AI Copilot
- 📦 [包管理器使用指南](包管理器使用指南.md) — duanpub 包管理
- 🌐 [API 文档](api/index.md) — 标准库参考
- 📋 [项目路线图](ROADMAP.md) — 版本规划与愿景