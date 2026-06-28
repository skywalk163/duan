# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.0] - 2026-06-28

### Added

- **完整类系统（LLVM 后端 typed 模式）**

  阶段1 - 类系统基础
  - 类元信息系统：DuanClassInfo 结构体全局表，存储类名、父类、方法表、属性表
  - 类注册与查找：dv_register_class、dv_find_class、dv_find_method
  - 对象序列化存储：格式 `obj:__class__\x1f类名\x1f属性\x1f值...`
  - 属性继承初始化：递归收集父类属性，子类实例包含所有继承属性
  - 类实例化：dv_class_new_named 创建带类名的对象实例
  - 属性访问与赋值：dv_class_get_member、dv_class_set_member

  阶段2 - 方法与构造函数
  - 方法编译为独立函数：命名约定 `_method_类名_方法名`
  - self（己）支持：方法内 "己" 映射到 self 参数
  - 方法调用：dv_call_method 动态查找并调用方法
  - 构造函数：与类名同名的方法作为构造函数，new 时自动调用
  - 实例方法注册：dv_register_method 登记实例方法

  阶段3 - 继承与 super
  - 单继承支持：类定义 `类 子类 继承 父类`
  - 方法重写：子类方法同名覆盖父类实现
  - super 调用：dv_call_super_method 从父类开始查找方法
  - 多层继承：支持多级继承链查找

  阶段4 - 类型判断
  - isinstance 内置函数：dv_isinstance 判断对象是否是指定类或其子类的实例
  - type 内置函数：dv_get_type_name 获取对象类型名称
  - 内置函数别名：是实例、是否实例、instance_of、type、typeof、取类型、类型名

  阶段5 - 运算符重载
  - 算术运算重载：+ - * / 对应方法名 加/减/乘/除 或 __add__/__sub__/__mul__/__div__
  - 运行时自动查找重载方法：dv_try_operator_overload
  - 基础类型运算不受影响：整数、浮点数、字符串运算保持原有逻辑

  阶段6 - 类方法与静态方法
  - 类方法：方法名前缀 `类`，通过 dv_call_class_method 调用
  - 静态方法：方法名前缀 `静`，通过 dv_call_static_method 调用
  - 调用方式：类名.方法名()
  - 方法类型标记：DuanClassInfo.method_flags 区分实例/类/静态方法

  阶段7 - 异常处理增强（B 方案）
  - 自定义异常类型：用户可定义继承自"异常"的异常类
  - 内置异常类：异常、运行时异常、值异常、索引异常、类型异常、IO异常、内存异常、算术异常
  - 多重捕获：支持多个捕获块按类型顺序匹配
  - 继承匹配：子类异常可被父类捕获块捕获
  - 完全向后兼容：原有字符串异常语法仍然支持

### Fixed

- **运行时库编译错误**
  - 添加 `#include <direct.h>` 解决 Windows 下的 _getcwd/_chdir 声明问题
  - 修复 strcpy/strncpy/fopen/localtime/getenv 等函数的弃用警告

- **LLVM IR 寄存器编号错误**
  - 每个函数开始时重置 _reg_counter = 0
  - 非 void 返回的函数调用必须显式赋值给寄存器

- **对象状态同步问题**
  - 属性赋值后对象必须存回原变量，防止 use-after-free
  - dv_class_set_member 支持原地更新已有属性

- **方法参数传递**
  - 修复参数顺序：result → self → args → num_args

### Documentation

- 新增 `docs/class_system_design.md` - 类系统完整设计文档
- 更新 `docs/llvm_backend_design.md` - 补充异常处理和类系统章节

## [1.8.0] - 2026-06-27

### Added

- **LLVM 后端（typed 模式）**
  - 基于 DuanValue 结构体的类型化 LLVM IR 生成
  - 算术运算直接操作原生类型（i64/double），无需 atoi/itoa 转换
  - 通过指针传递 DuanValue，消除 C 与 LLVM 间的 ABI 不兼容问题
  - `src/llvm/codegen_typed.py` - 类型化 LLVM 代码生成器
  - `src/llvm/runtime_typed.c` - 类型化运行时库

- **异常处理（LLVM 后端）**
  - 支持 `尝试`/`捕获`/`最终`/`抛出` 完整异常处理语法
  - 基于 setjmp/longjmp 的异常传播机制
  - Windows x64 平台优化：内联 `_setjmp` + `llvm.frameaddress` 避免栈帧失效
  - 支持嵌套 try-catch、函数内抛出异常、多层函数调用栈传播
  - 支持 finally 块（无论是否抛出异常都会执行）
  - 10 个 LLVM 后端异常处理测试全部通过

### Fixed

- **finally 块执行逻辑修复**
  - 修复无异常抛出时 finally 块不执行的问题
  - 重构控制流：try → finally → end，catch → finally → end

- **无 catch 的 try 异常传播修复**
  - 修复只有 finally 没有 catch 时，异常被吞掉不向外传播的问题
  - 无 catch 也无 finally 的 try 直接执行体，不设置 setjmp

- **main 函数多余调用修复**
  - 修复 typed 模式下 main 函数自动调用第一个无参数段落的问题
  - 改为只调用名为"主程序/主入口/main"的段落，与父类行为一致

- **清理调试输出**
  - 移除 `_collect_segment` 中的 DEBUG 打印语句

## [1.7.0] - 2026-06-26

### Added

- **ANTLR 后端 v3 语法支持**
  - 添加预处理层将纯缩进语法转换为带结束标记的形式
  - 支持无括号打印语句：`打印 "你好"`（不再强制要求括号）
  - 支持范围表达式：`1至10` → 预处理转换为 `范围(1, 11)`
  - 支持句号可选：表达式语句和变量声明句号可选
  - `antlrparser/indent_preprocessor.py` - 缩进语法预处理模块

- **泛型系统**：实现泛型类型参数和泛型函数
  - 支持 `类 栈[T]:` 泛型类语法
  - 支持 `段落 恒等[T] 参数 x：` 泛型函数语法
  - 支持泛型方法：`段落 转换[T] 接收 值:`
  - 类型擦除策略，与 Python 动态类型兼容

- **标准库扩充**：新增 11 个功能模块
  - `日志.duan/py` - 结构化日志输出
  - `进制转换.duan/py` - 进制转换工具
  - `迭代工具.duan/py` - map/filter/reduce 等高阶函数
  - `命令行参数.duan/py` - 命令行参数解析
  - `终端颜色.duan/py` - 终端彩色输出
  - `系统信息.duan/py` - 系统与硬件信息
  - `配置.duan/py` - JSON 配置文件读写
  - `表格.duan/py` - 格式化表格输出
  - `随机数据.duan/py` - 随机数与随机选择
  - `缓存.duan/py` - 函数结果缓存
  - `CSV.duan/py` - CSV 文件读写

- **性能基准测试框架**
  - `benchmarks/run_benchmarks.py` - 基准测试运行器
  - 8 个基准测试程序覆盖不同场景
  - 测量词法分析、语法解析、代码生成各阶段性能

- **文档更新**
  - `docs/syntax.md` - 添加泛型语法章节
  - `docs/统一语法规范_v3.1.md` - 添加泛型语法说明

### Changed

- **性能优化**：Phase 8 深度优化
  - 词法分析器：字符分类查表优化
  - 解析器：增量编译缓存
  - 代码生成器：缩进缓存优化
  - 运行时：常量折叠、死代码消除、循环不变量外提

### Fixed

- **技术债务清理**
  - 删除旧文档和冗余文件
  - 完善 .gitignore

## [1.6.1] - 2026-06-15

### Added

- MkDocs 文档网站

## [1.6.0] - 2026-06-14

### Added

- Phase 7.5: 调试器/REPL 工具链
- Phase 7.6: LSP 语言服务器完善

## [1.5.0] - 2026-06-10

### Added

- Phase 6: 测试框架完善
- Phase 7: IDE 集成（LSP + DAP）
