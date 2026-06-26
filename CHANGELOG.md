# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.0] - 2026-06-26

### Added

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
