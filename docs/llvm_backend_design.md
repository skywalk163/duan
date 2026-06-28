# LLVM 后端设计文档

## 概述

段言 LLVM 后端将段言源代码编译为原生可执行文件，提供远高于 Python 解释执行的运行性能。后端基于 LLVM IR 中间表示，通过 clang 编译链接为目标平台的原生机器码。

## 编译流程

```
.duan 源文件
    │
    ▼
┌─────────────────┐
│   Lexer         │  词法分析
│   lexer.py      │  → Token 流
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DuanParser v3  │  语法分析
│  duan_parser_v3 │  → v3 AST
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AstAdapter    │  AST 适配
│  compiler.py    │  → 统一 AST
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TypedLLVMCodeGen│  代码生成
│ codegen_typed.py│  → LLVM IR (.ll)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      clang      │  编译优化
│                 │  → 目标文件 (.o)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      clang      │  链接
│  + runtime_typed│  → 可执行文件 (.exe)
└─────────────────┘
```

## 两种模式对比

### String 模式（旧版）
- 类型系统基于 i8* 字符串
- 所有值都以字符串形式存储
- 算术运算需要 atoi/itoa 转换
- 实现简单，但性能较差

### Typed 模式（推荐）
- 类型系统基于 DuanValue 结构体
- 算术运算直接在原生类型（i64/double）上操作
- 通过指针传递，避免 C/LLVM ABI 不兼容
- 性能优异，是当前主要开发方向

## DuanValue 类型系统

### 结构体定义

**LLVM IR 定义**：
```llvm
{ i32 type, i64 i64_val, double f64_val, ptr str_val, i32 bool_val, [4 x i8] padding }
```

**C 定义**：
```c
typedef struct {
    int type;          /* 0=NULL 1=INT 2=FLOAT 3=STR 4=LIST 5=BOOL */
    int64_t i64;       /* INT */
    double f64;        /* FLOAT */
    char* str;         /* STR / LIST (序列化) */
    int boolean;       /* BOOL */
} DuanValue;
```

### 类型标记

| 值 | 类型 | 存储位置 |
|----|------|----------|
| 0 | NULL（空） | - |
| 1 | INT（64位整数） | i64 |
| 2 | FLOAT（64位浮点数） | f64 |
| 3 | STRING（字符串） | str |
| 4 | LIST（列表） | str（序列化字符串） |
| 5 | BOOL（布尔值） | boolean |

### 指针传递策略

**问题**：C 和 LLVM 对结构体的内存布局、对齐方式可能存在差异（ABI 不兼容），直接传递结构体可能导致崩溃。

**解决方案**：所有 DuanValue 通过指针传递，运行时函数接收 `DuanValue*` 参数，结果写入 `result` 指针。

```llvm
; 函数签名示例
declare void @dv_add(ptr result, ptr a, ptr b)
declare void @dv_println(ptr value)
```

## 代码生成核心

### 寄存器分配

使用简单的递增计数器分配虚拟寄存器：

```python
def new_register(self) -> str:
    self._reg_counter += 1
    return f'%{self._reg_counter}'
```

### 标签管理

标签用于控制流（分支、循环、函数等）：

```python
def new_label(self, prefix: str) -> str:
    self._label_counter += 1
    return f'{prefix}_{self._label_counter}'
```

### Alloca 延迟生成

LLVM 要求 alloca 指令必须在函数入口块（entry block）中。通过 `_pending_allocas` 列表延迟生成：

```python
# 收集阶段
self._pending_allocas.append(f'{reg} = alloca {DUANVALUE_STRUCT}')

# 函数入口统一生成
for alloca in self._pending_allocas:
    self.emit(alloca)
```

## 异常处理实现

### 语法

```段言
尝试：
    可能抛出异常的代码
捕获 异常变量：
    异常处理代码
最终：
    无论是否异常都执行的代码
结束。
```

### 实现机制

基于 C 标准库的 `setjmp`/`longjmp` 实现非局部跳转：

- `setjmp(buf)`：保存当前执行环境，返回 0
- `longjmp(buf, val)`：跳转到 `setjmp` 位置，`setjmp` 返回 `val`

### 跨平台 setjmp 适配

不同平台的 `setjmp` 函数签名存在差异，代码生成器根据目标平台动态生成对应的调用：

#### Windows x64

**问题**：Windows x64 的 `_setjmp` 需要两个参数：
1. jmp_buf 指针
2. 帧地址（用于栈展开）

如果在 C 函数中调用 `setjmp`，当 C 函数返回后，栈帧失效，`longjmp` 会崩溃。

**解决方案**：
- 在 LLVM IR 中直接调用 `_setjmp`
- 使用 `llvm.frameaddress.p0(i32 0)` 获取当前帧地址
- setjmp 的帧地址指向当前 LLVM 函数的栈帧，长期有效

```llvm
%frame_addr = call ptr @llvm.frameaddress.p0(i32 0)
%setjmp_result = call i32 @_setjmp(ptr %jmp_buf_ptr, ptr %frame_addr)
```

#### Linux / macOS

Linux 和 macOS 使用标准 C 库的 `setjmp`，只需一个参数（jmp_buf 指针）：

```llvm
%setjmp_result = call i32 @setjmp(ptr %jmp_buf_ptr)
```

#### 平台检测机制

代码生成器在初始化时检测目标平台：
- `is_windows`：Windows 平台（win32/cygwin）
- `is_linux`：Linux 平台
- `is_macos`：macOS 平台（darwin）

支持通过 `target_platform` 参数显式指定目标平台，便于交叉编译场景。

### Try 层级管理

使用全局数组和计数器管理嵌套 try-catch：

```c
#define MAX_TRY_DEPTH 16
static jmp_buf __dv_jmp_bufs[MAX_TRY_DEPTH];
static int __dv_try_level = -1;

void* dv_try_push(void) {
    __dv_try_level++;
    if (__dv_try_level >= MAX_TRY_DEPTH) {
        __dv_try_level--;
        return NULL;
    }
    return (void*)__dv_jmp_bufs[__dv_try_level];
}

void dv_try_pop(void) {
    if (__dv_try_level >= 0) {
        __dv_try_level--;
    }
}

void dv_throw(DuanValue* exc) {
    if (__dv_try_level < 0) return;
    // 保存异常消息
    char* s = dv_to_string(exc);
    strncpy(__dv_exception_str, s, 1023);
    free(s);
    // 跳转到当前 try 层级
    int level = __dv_try_level;
    longjmp(__dv_jmp_bufs[level], 1);
}
```

### 控制流设计

```
入口:
  jmp_buf_ptr = dv_try_push()
  frame_addr = llvm.frameaddress(0)
  setjmp_result = _setjmp(jmp_buf_ptr, frame_addr)
  if setjmp_result != 0 → catch 分派
  else → try 块

try 块:
  执行 try 体
  dv_try_pop()
  有 finally → finally_from_try → finally 块
  无 finally → end

catch 分派:
  有 catch → catch 块
  无 catch 但有 finally → finally 块（之后重新抛出）

catch 块:
  dv_try_pop()
  获取异常消息
  执行 catch 体
  有 finally → finally 块
  无 finally → end

finally 块:
  执行 finally 体
  有 catch → end
  无 catch → 重新抛出异常（向外层传播）
```

### 特殊情况处理

1. **既无 catch 也无 finally**：直接执行 try 体，不设置 setjmp
2. **无 catch 但有 finally**：finally 执行完后重新抛出异常
3. **异常信息存储**：全局缓冲区 `__dv_exception_str[1024]`

## 列表实现

列表内部使用序列化字符串存储，格式为：

```
list:长度:元素1\x1f元素2\x1f元素3\x1f...
```

使用 `\x1f`（单元分隔符）作为元素分隔符，避免与普通字符串冲突。

### 数字自动检测

从列表中获取元素时，自动检测元素类型：
- 纯数字字符串 → INT 类型
- 含一个小数点的数字字符串 → FLOAT 类型
- 其他 → STRING 类型

## 类与对象实现

对象内部也使用序列化字符串存储，格式为：

```
obj:字段数:字段名1\x1f值1\x1f字段名2\x1f值2\x1f...
```

使用 `\x1f` 分隔字段名和值。

## 运行时库

### 文件结构

| 文件 | 说明 |
|------|------|
| `runtime_typed.c` | 类型化运行时库（C 实现） |
| `runtime.c` | string 模式运行时库 |

### 运行时函数分类

**值构造器**：`dv_null`, `dv_int`, `dv_float`, `dv_str`, `dv_bool`

**算术运算**：`dv_add`, `dv_sub`, `dv_mul`, `dv_div`

**比较运算**：`dv_eq`, `dv_lt`, `dv_gt`, `dv_le`, `dv_ge`

**I/O**：`dv_print`, `dv_println`, `dv_input`

**字符串操作**：`dv_concat`, `dv_str_len`

**列表操作**：`dv_list_new`, `dv_list_len`, `dv_list_get`, `dv_list_append`, `dv_list_clear`

**时间**：`dv_timestamp`, `dv_format_time`

**文件**：`dv_file_exists`, `dv_read_file`, `dv_write_file`

**异常处理**：`dv_try_push`, `dv_try_pop`, `dv_throw`, `dv_get_exception_str`, `dv_clear_exception`

**类操作**：`dv_class_new`, `dv_class_set_member`, `dv_class_get_member`

## 编译入口

`src/llvm/compiler.py` 提供完整的编译流程：

### 主要函数

- `compile_source(source)`：编译源码为 LLVM IR 字符串
- `compile_source_typed(source)`：编译源码为 LLVM IR（typed 模式）
- `compile_duan(source_path, output_path)`：编译 .duan 文件为可执行文件
- `compile_duan_typed(source_path, output_path)`：typed 模式编译
- `find_clang()`：查找 clang 编译器

### 使用示例

```python
from llvm.compiler import compile_duan_typed

exe_path = compile_duan_typed('hello.duan', verbose=True)
print(f'编译成功: {exe_path}')
```

## 已知限制

### 类型系统
- **字符串编码**：当前使用 UTF-8 字符串，未完全支持 Unicode 字符串操作（如按字符索引、子串等）
- **垃圾回收**：使用 malloc/free 手动管理内存，没有自动垃圾回收
- **列表存储**：列表使用序列化字符串存储，访问元素需要解析，性能较低
- **对象存储**：对象使用序列化字符串存储，字段访问需要线性查找

### 异常处理
- **异常类型**：目前只支持字符串异常消息，不支持自定义异常类型和类型匹配
- **线程安全**：全局变量（try 层级、异常消息）非线程安全
- **最大 try 深度**：最多 16 层嵌套 try-catch

### 标准库
- **覆盖度低**：仅实现了 48 个运行时函数，Python 后端有 23 个标准库模块
- **缺少数学库**：sin/cos/sqrt 等数学函数尚未实现
- **缺少字符串操作**：分割、替换、查找等字符串操作有限

### 平台支持
- **已支持平台**：Windows x64、Linux x64
- **setjmp 适配**：已实现 Windows `_setjmp` 与 Linux/macOS 标准 `setjmp` 的条件生成
- **可执行文件后缀**：Windows 生成 `.exe`，Linux/macOS 生成无后缀可执行文件
- **待支持**：macOS、ARM64、WebAssembly

### 优化程度
- **无 LLVM 优化**：未启用 LLVM 的 O1/O2/O3 优化 Pass
- **无 SSA 优化**：代码生成未利用 LLVM 的 SSA 形式进行深度优化

## 未来规划

### 短期目标（v1.9.x）— 功能补全与稳定性提升

#### 1. 内置函数扩充
- [x] **数学函数**：`sin`、`cos`、`sqrt`、`pow`、`abs`、`floor`、`ceil`、`取模` 等 ✅
- [x] **字符串操作**：`分割`、`替换`、`查找`、`子串`、`转大写`、`转小写`、`去除空白` 等 ✅
- [x] **列表操作**：`插入`、`删除`、`反转`、`排序`、`查找元素索引`、`包含`、`设置元素`、`列表字面量` 等 ✅
- [x] **文件操作**：`追加文件`、`列出目录`、`删除文件`、`文件大小`、`读取文件`、`写入文件`、`文件存在` 等 ✅
- [x] **系统操作**：`环境变量`、`设置环境变量`、`参数列表`、`退出程序`、`当前目录`、`切换目录`、`执行命令` 等 ✅
- [x] **类型转换函数**：`转整数`、`转浮点`、`转字符串`、`转布尔` 等显式转换 ✅
- [x] **字符串连接列表**：`join`/`连接字符串` ✅

#### 2. 异常处理增强
- [ ] **自定义异常类型**：支持定义异常类，按类型捕获异常
- [ ] **异常栈追踪**：抛出异常时记录调用栈，便于调试
- [ ] **多重捕获**：支持多个捕获块按类型匹配
- [ ] **异常链式传递**：支持异常 cause，保留原始异常信息

#### 3. 类型系统改进
- [ ] **字典/映射类型**：新增 `dict` 类型，支持键值对存储（替代当前对象序列化方案）
- [ ] **列表优化**：改用动态数组存储列表元素，提升随机访问性能
- [x] **类型转换函数**：`转整数`、`转浮点`、`转字符串`、`转布尔` 等显式转换 ✅
- [ ] **可空类型**：与语言层面的可空类型对接，支持 null 安全检查

#### 4. 稳定性与测试
- [ ] **完善测试覆盖**：将 LLVM 后端纳入 CI，运行完整测试套件
- [ ] **内存泄漏检测**：使用 valgrind/AddressSanitizer 检测内存泄漏
- [ ] **边界情况处理**：除零、空指针、索引越界等边界错误的优雅处理
- [ ] **错误信息改进**：编译错误包含行号、列号和源代码上下文

### 中期目标（v2.0）— 性能优化与生态完善

#### 1. 内存管理
- [ ] **引用计数 GC**：实现基于引用计数的自动垃圾回收
- [ ] **循环引用处理**：使用弱引用或周期回收处理循环引用
- [ ] **内存池**：小对象内存池分配，减少 malloc 开销
- [ ] **字符串池**：字符串常量池，避免重复分配

#### 2. 性能优化
- [ ] **LLVM 优化 Pass**：启用 O1/O2 优化，集成 InstCombine、GVN、DCE 等
- [ ] **函数内联**：小函数自动内联，减少调用开销
- [ ] **循环优化**：循环不变量外提、循环展开、循环向量化
- [ ] **常量传播**：跨函数常量传播与折叠
- [ ] **逃逸分析**：栈上分配未逃逸对象，减少 GC 压力
- [ ] **内联缓存**：方法调用的内联缓存（Inline Cache）优化

#### 3. 标准库移植
- [ ] **数学模块**：完整移植数学模块（三角函数、对数、随机数等）
- [ ] **字符串处理模块**：移植字符串处理模块（正则、编码转换等）
- [ ] **JSON 模块**：移植 JSON 解析与序列化
- [ ] **时间/日期模块**：移植时间与日期处理
- [ ] **文件系统模块**：移植文件系统操作
- [ ] **哈希模块**：MD5、SHA1、SHA256 等哈希算法
- [ ] **正则模块**：正则表达式支持（集成 PCRE 或 re2）

#### 4. 模块系统支持
- [ ] **导入/导出**：支持模块导入导出语法
- [ ] **模块解析**：实现模块路径解析与缓存
- [ ] **跨模块调用**：支持调用其他模块的函数和类
- [ ] **标准库加载**：内置标准库模块的自动加载机制

#### 5. 开发工具
- [ ] **调试信息**：生成 DWARF 调试信息，支持 gdb/lldb 调试
- [ ] **性能分析**：支持生成性能分析所需的符号表
- [ ] **编译缓存**：增量编译，缓存已编译的模块

### 长期目标（v2.x+）— 高级特性与平台扩展

#### 1. 高级类型系统
- [ ] **泛型特化**：泛型函数/类的单态化（monomorphization），生成特化代码
- [ ] **接口/协议**：接口定义与动态派发
- [ ] **枚举类型**：带关联值的代数数据类型（ADT）
- [ ] **模式匹配**：match 表达式与解构赋值
- [ ] **类型推断集成**：将 HM 类型推断结果用于代码生成优化

#### 2. JIT 编译
- [ ] **LLVM ORC JIT**：集成 LLVM ORC JIT 引擎，支持即时编译
- [ ] **REPL 支持**：LLVM 后端的 REPL 交互式环境
- [ ] **动态加载**：运行时动态编译和加载代码
- [ ] **分层编译**：解释执行 → 快速 JIT → 优化 JIT 的分层编译策略

#### 3. 并发与并行
- [ ] **协程**：支持 async/await 异步编程
- [ ] **多线程**：线程安全的运行时，支持多线程并行
- [ ] **通道/消息传递**：CSP 风格的并发模型
- [ ] **并行循环**：自动并行化的遍历循环

#### 4. 跨平台支持
- [x] **Linux 支持**：适配 Linux x64 平台 ✅
- [ ] **macOS 支持**：适配 macOS x64/ARM64 平台
- [ ] **ARM64 支持**：支持 ARM64 架构（树莓派、移动设备等）
- [ ] **WebAssembly**：编译为 WASM，支持浏览器运行
- [ ] **跨平台 CI**：多平台持续集成测试

#### 5. 高级优化
- [ ] **逃逸分析与栈分配**：基于逃逸分析的对象栈分配
- [ ] **向量化**：SIMD 向量化优化
- [ ] **PGO（Profile-Guided Optimization）**：基于运行时 profile 的优化
- [ ] **LTO（Link-Time Optimization）**：链接时优化
- [ ] **GC 优化**：分代垃圾回收、增量 GC、并发 GC

#### 6. 自举与元循环
- [ ] **段言自举**：用段言重写编译器核心部分
- [ ] **元循环解释器**：在段言中实现段言解释器
- [ ] **编译器即库**：编译器作为库嵌入到段言程序中
- [ ] **编译期计算**：支持编译期函数执行（const eval）

### 优先级路线图

```
v1.9.x (短期)                    v2.0 (中期)                      v2.x+ (长期)
┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
│ 内置函数扩充       │        │ 引用计数 GC       │        │ 泛型特化           │
│ 异常处理增强       │──────▶│ LLVM 优化 Pass    │──────▶│ JIT 编译           │
│ 字典/列表优化      │        │ 标准库移植        │        │ 协程/多线程        │
│ 稳定性与测试       │        │ 模块系统支持      │        │ 跨平台（Linux/macOS）│
│                   │        │ 调试信息生成      │        │ 自举与元循环        │
└───────────────────┘        └───────────────────┘        └───────────────────┘
```

### 当前进度追踪

| 类别 | 已实现 | 计划中 | 完成度 |
|------|--------|--------|--------|
| 基础类型（int/float/bool/str） | ✅ | - | 100% |
| 列表类型 | ✅（序列化字符串） | 动态数组优化 | 60% |
| 类与对象 | ✅（序列化字符串） | 字典优化 | 50% |
| 算术运算 | ✅ | - | 100% |
| 比较运算 | ⚠️（在函数内正常，顶级条件分支有问题） | 调试修复 | 90% |
| 逻辑运算 | ⚠️（布尔条件判断有问题） | 调试修复 | 80% |
| 条件分支（如果/否则） | ⚠️（布尔值条件有问题） | 调试修复 | 80% |
| 循环（遍历/当） | ✅ | - | 100% |
| 函数（段落） | ✅ | - | 100% |
| 类与继承 | ✅ | - | 100% |
| 异常处理（尝试/捕获/抛出/最终） | ✅（含自定义异常类型） | - | 100% |
| 打印/输入 | ✅ | - | 100% |
| 字符串操作 | ✅ | 更多字符串操作 | 80% |
| 文件读写 | ✅ | 更多文件操作 | 60% |
| 时间函数 | ✅ | 日期时间模块 | 30% |
| 垃圾回收 | ❌ | 引用计数 GC | 0% |
| 模块系统 | ❌ | 导入/导出 | 0% |
| LLVM 优化 | ❌ | O1/O2 优化 | 0% |
| 调试信息 | ❌ | DWARF 支持 | 0% |
| JIT 编译 | ❌ | ORC JIT | 0% |

### 已知问题

1. **比较运算符在顶级条件分支中无效**
   - 在函数内使用比较运算符正常
   - 在顶级（模块作用域）使用 `如果 x > y：` 时程序行为异常
   - 原因：可能是代码生成或运行时对顶级条件分支处理有误

2. **布尔条件判断问题**
   - `如果 flag：` 其中 flag 为真时，可能不执行 if 体
   - 原因：布尔值的真值判断逻辑可能有问题

### 待修复

- [ ] 比较运算符在顶级条件分支中的问题
- [ ] 布尔条件真值判断问题
- [ ] 条件分支 `如果 x > y：` 中 `>` 符号处理
