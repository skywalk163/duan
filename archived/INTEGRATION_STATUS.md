# 段言编程语言 - 整合状态报告

## 时间：2026-06-12 23:58

---

## 一、当前状态概览

### ✅ 已完成

1. **统一AST格式** - `src/ast_unified.py` (376行)
   - 合并了src和antlrparser的所有AST节点
   - 支持37个AST节点类型

2. **统一语法规范** - `docs/统一语法规范_v1.5.md`
   - 采用src语法风格：`设 甲 为 三。`
   - 段落定义：`段落 平方 接收 数值。`
   - 类定义：`类 狗 继承 动物 实现 可打印。`

3. **ANTLR语法文件修改** - 部分完成
   - `DuanLangLexer.g4`：已添加新关键字（设、为、段落、接收、类、接口、实现、属性、构造、新建、己）
   - `DuanLangParser.g4`：部分修改（但还在使用旧语法）

4. **编译器整合** - `compile.py` + `duan_compile.py`
   - `compile.py`：使用src的手写解析器（可工作）
   - `duan_compile.py`：尝试使用ANTLR解析器（部分工作）

### ⚠️ 存在的问题

#### 问题1：ANTLR语法规则不一致

**位置**：`antlrparser/DuanLangParser.g4` 第52-57行

**当前状态**：
```antlr
paragraphDef
    : K_SEGMENT ( BOOK_L ID BOOK_R | ID ) ( K_RECEIVE paramList )? ...
```

**应该改为**：
```antlr
paragraphDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ...
```

**原因**：统一语法规范中，段落名直接跟在`段落`关键字后，不需要书名号`《》`

---

#### 问题2：方法定义语法不一致

**位置**：`antlrparser/DuanLangParser.g4` 第81-88行

**当前状态**：
```antlr
methodDef
    : ( K_METHOD | K_SEGMENT ) ID ( LPAREN paramList? RPAREN | K_RECEIVE paramList )? ...
    
constructorDef
    : K_CONSTRUCTOR LPAREN paramList? RPAREN ...
```

**应该改为**：
```antlr
methodDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

constructorDef
    : K_CONSTRUCTOR ( K_RECEIVE paramList )? COLON block K_END PERIOD?
    ;
```

**原因**：统一语法规范中，方法也是段落，使用`段落`关键字和`接收`关键字

---

#### 问题3：ANTLR解析器代码未重新生成

**位置**：`antlrparser/duan_parser/DuanLangParser.py`

**症状**：
```python
# 测试失败
code = '段落 测试。返回 一。结束。'
# 错误：mismatched input '段落' expecting {'《', ID}
```

**原因**：修改了`.g4`文件但没有重新生成解析器代码

**解决方案**：
```bash
cd antlrparser
java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener DuanLangParser.g4
java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener DuanLangLexer.g4
```

---

#### 问题4：测试套件导入错误

**位置**：`antlrparser/test_parse_tree.py`

**症状**：
```
ModuleNotFoundError: No module named 'DuanLangLexer'
```

**原因**：ANTLR生成的Python文件在`duan_parser/`子目录下

**解决方案**：
```python
# 修改导入路径
from duan_parser.DuanLangLexer import DuanLangLexer
```

---

## 二、需要修复的文件清单

### 高优先级

1. `antlrparser/DuanLangParser.g4` - 修改段落、方法、构造函数语法规则
2. 重新生成ANTLR解析器代码
3. `antlrparser/duan_visitor.py` - 适配新语法规则

### 中优先级

4. `compile.py` - 整合双后端选择（Python/LLVM）
5. `src/code_generator_unified.py` - 使用统一AST
6. 测试文件导入路径修复

### 低优先级

7. 文档更新
8. 示例代码更新

---

## 三、推荐的修复步骤

### 步骤1：修复ANTLR语法规则

编辑 `antlrparser/DuanLangParser.g4`，统一所有语法规则到新规范：

```antlr
// 段落定义
paragraphDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

// 方法定义
methodDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

// 构造函数
constructorDef
    : K_CONSTRUCTOR ( K_RECEIVE paramList )?
      COLON block K_END PERIOD?
    ;

// 类定义
classDef
    : K_CLASS ID
      ( K_INHERIT typeAnnotation ( COMMA typeAnnotation )* )?
      ( K_IMPLEMENTS typeAnnotation ( COMMA typeAnnotation )* )?
      COLON classMember* K_END PERIOD?
    ;
```

### 步骤2：重新生成ANTLR代码

```bash
cd antlrparser
java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor DuanLangLexer.g4
java -jar ../antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor DuanLangParser.g4
```

### 步骤3：更新Visitor

编辑 `antlrparser/duan_visitor.py`，适配新语法规则生成的AST。

### 步骤4：测试

```bash
# 测试词法分析
python -c "
from antlr4 import InputStream
from duan_parser.DuanLangLexer import DuanLangLexer
code = '段落 测试。返回 一。结束。'
lexer = DuanLangLexer(InputStream(code))
for t in lexer.getAllTokens():
    print(f'{lexer.symbolicNames[t.type]}: {t.text}')
"

# 测试语法分析
python compile.py test_unified.duan

# 测试代码生成
python test_unified.py
```

---

## 四、语法对比示例

### 变量声明

| 实现 | 语法 | Python输出 |
|------|------|-----------|
| src | `设 甲 为 三。` | `甲 = 3` |
| antlrparser（旧） | `定义甲等于10。` | `甲 = 10` |
| 统一规范 | `设 甲 为 三。` | `甲 = 3` |

### 段落定义

| 实现 | 语法 | Python输出 |
|------|------|-----------|
| src | `段落 平方 接收 数值。` | `def 平方(数值):` |
| antlrparser（旧） | `《平方》段(数值)：` | `def 平方(数值):` |
| 统一规范 | `段落 平方 接收 数值。` | `def 平方(数值):` |

### 类定义

| 实现 | 语法 | Python输出 |
|------|------|-----------|
| src | `类 狗 继承 动物。` | `class 狗(动物):` |
| antlrparser（旧） | `《狗》类 继承 《动物》:` | `class 狗(动物):` |
| 统一规范 | `类 狗 继承 动物。` | `class 狗(动物):` |

---

## 五、下一步行动

### 立即行动

- [ ] 修复 `DuanLangParser.g4` 的语法规则
- [ ] 重新生成ANTLR代码
- [ ] 测试基本解析功能

### 短期目标（1-2天）

- [ ] 完善统一编译入口
- [ ] 整合测试用例
- [ ] 更新文档

### 长期目标（1周）

- [ ] 实现LLVM后端
- [ ] 完善标准库
- [ ] 发布v2.0版本

---

## 六、Trae的修改记录

根据git状态，Trae已经修改了：

1. ✅ `antlrparser/DuanLangLexer.g4` - 添加了新关键字
2. ⚠️ `antlrparser/DuanLangParser.g4` - 部分修改（需要继续完善）
3. ✅ `antlrparser/duan_ast.py` - AST节点更新
4. ✅ `src/code_generator_unified.py` - 创建统一代码生成器
5. ⚠️ `antlrparser/duan_parser/` - ANTLR生成的解析器代码（需要重新生成）

---

## 七、关键决策记录

### 决策1：语法统一到src风格

**理由**：
- src语法更符合中文表达习惯
- 减少标点符号使用
- 保持一致性

### 决策2：统一解析器 + 双后端

**理由**：
- ANTLR解析器更稳定、可维护
- Python后端轻量、易调试
- LLVM后端高性能、原生执行

### 决策3：保留书名号《》用于模块名

**理由**：
- 符合中文习惯
- 明确模块边界
- 示例：`导入《数学工具》。`

---

## 八、联系信息

如有疑问，请检查：
1. `docs/统一语法规范_v1.5.md` - 完整语法规范
2. `src/ast_unified.py` - AST节点定义
3. `compile.py` - 当前可用的编译器

---

**报告生成时间**：2026-06-12 23:58
**状态**：整合进行中，关键语法规则需要修复
