# 段言编译器归档文件

本目录存放历史版本文件，仅作参考，不参与编译。

## 目录结构

```
archived/
├── parsers/        # 历史解析器版本
│   ├── duan_parser.py          - 第一版解析器
│   ├── duan_parser_v2.py       - 第二版解析器
│   ├── duan_parser_final.py    - 最终版解析器
│   ├── duan_parser_integrated.py - 集成版解析器
│   ├── duan_lark.py            - Lark解析器版本
│   ├── duan_lark_simple.py     - Lark简化版本
│   └── parser.py               - 旧版解析器
├── tests/          # 历史测试文件
│   ├── quick_test.py
│   ├── simple_test.py
│   └── test_*.py
└── pipelines/      # 历史流水线
    ├── simple_pipeline.py
    └── complete_pipeline.py
```

## 归档原因

- **解析器**：已完成递归下降解析器（duan_parser_v3.py），历史版本不再使用
- **测试**：已创建完整测试套件（tests/目录），历史测试文件不再使用
- **流水线**：已集成到主代码中，独立流水线文件不再使用

## 注意事项

这些文件仅作历史参考，可能包含：
- 过时的设计思路
- 不兼容的接口
- 已修复的bug

**请勿使用这些文件进行开发！**

---

**归档时间：** 2026-06-10  
**归档原因：** 代码清理，优化项目结构
