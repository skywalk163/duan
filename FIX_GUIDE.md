# 段言编程语言 - 整合修复指南

## 当前状态（2026-06-13 00:01）

### 已完成 ✅

1. **统一AST格式** - `src/ast_unified.py`
2. **统一语法规范** - `docs/统一语法规范_v1.5.md`
3. **ANTLR语法规则修复** - `antlrparser/DuanLangParser.g4`（刚刚修复完成）

### 需要完成 ⏳

1. **重新生成ANTLR解析器代码**
2. **更新duan_visitor.py适配新语法**
3. **测试编译功能**

---

## 修复步骤

### 步骤1：重新生成ANTLR代码

**问题**：antlr-4.13.2-complete.jar文件损坏

**解决方案**：

```bash
# 方案A：使用pip安装的antlr4工具
pip install antlr4-tools
antlr4 -Dlanguage=Python3 -visitor -no-listener DuanLangLexer.g4
antlr4 -Dlanguage=Python3 -visitor -no-listener DuanLangParser.g4

# 方案B：手动下载jar（如果方案A不行）
curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor DuanLangLexer.g4
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor DuanLangParser.g4
```

### 步骤2：验证语法规则

已修复的语法规则：

```antlr
# 段落定义（正确）
paragraphDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

# 方法定义（正确）
methodDef
    : K_SEGMENT ID ( K_RECEIVE paramList )? ( K_RETURN typeAnnotation )?
      COLON block K_END PERIOD?
    ;

# 构造函数（正确）
constructorDef
    : K_CONSTRUCTOR ( K_RECEIVE paramList )? COLON block K_END PERIOD?
    ;

# 属性声明（正确）
attributeDecl
    : K_ATTRIBUTE ID ( K_AS typeAnnotation )? ( K_EQUAL expr )? PERIOD?
    ;
```

### 步骤3：测试解析器

```bash
# 测试词法分析
python -c "
import sys
sys.path.insert(0, 'antlrparser/duan_parser')
from antlr4 import InputStream
from DuanLangLexer import DuanLangLexer

code = '段落 测试。返回 一。结束。'
lexer = DuanLangLexer(InputStream(code))
tokens = lexer.getAllTokens()

for token in tokens:
    symbolic_name = lexer.symbolicNames[token.type] if token.type < len(lexer.symbolicNames) else 'UNKNOWN'
    print(f'{token.line}:{token.column} {symbolic_name} = {token.text!r}')
"

# 测试语法分析
python compile.py test_unified.duan

# 测试代码生成
python test_unified.py
```

---

## 关键文件清单

### 语法规范

- `docs/统一语法规范_v1.5.md` - 完整语法规范文档
- `antlrparser/DuanLangParser.g4` - ANTLR语法规则（已修复）
- `antlrparser/DuanLangParser.g4.backup` - 修复前的备份

### AST定义

- `src/ast_unified.py` - 统一AST节点定义（376行）
- `antlrparser/duan_ast.py` - ANTLR版本的AST定义（需要统一到ast_unified）

### 编译器

- `compile.py` - 当前可用的编译器（使用src解析器）
- `duan_compile.py` - 尝试统一ANTLR解析器的编译器（需要修复）

### 测试文件

- `test_unified.duan` - 统一语法测试用例
- `test_import.duan` - 模块导入测试
- `antlrparser/test/` - ANTLR测试套件

---

## Trae需要做什么

### 立即行动（5分钟）

1. **检查ANTLR语法规则**
   ```bash
   cat antlrparser/DuanLangParser.g4 | grep -A5 "paragraphDef\|methodDef\|constructorDef"
   ```
   
2. **重新生成ANTLR代码**
   ```bash
   cd antlrparser
   antlr4 -Dlanguage=Python3 -visitor DuanLangLexer.g4
   antlr4 -Dlanguage=Python3 -visitor DuanLangParser.g4
   ```

3. **测试基本功能**
   ```bash
   python compile.py test_unified.duan
   python test_unified.py
   ```

### 短期目标（1小时）

4. **更新duan_visitor.py**
   - 适配新的AST结构
   - 确保所有节点类型都正确处理

5. **整合测试用例**
   - 统一测试文件路径
   - 确保所有测试通过

### 中期目标（1天）

6. **完善编译器入口**
   - `compile.py`：支持`--target python/llvm`选项
   - 统一命令行接口

7. **更新文档**
   - 用户指南
   - 开发者文档

---

## 已知问题

### 问题1：ANTLR jar文件损坏

**症状**：
```
Error: Invalid or corrupt jarfile ../antlr-4.13.2-complete.jar
```

**解决方案**：
```bash
# 重新下载
curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar
java -jar antlr-4.13.1-complete.jar -version
```

### 问题2：测试套件导入错误

**症状**：
```
ModuleNotFoundError: No module named 'DuanLangLexer'
```

**解决方案**：
```python
# 修改导入路径
from duan_parser.DuanLangLexer import DuanLangLexer
```

### 问题3：编码问题（Windows）

**症状**：
```
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713'
```

**解决方案**：
```python
# 避免使用Unicode符号（✓、✗等）
# 使用ASCII符号（[OK]、[FAIL]等）
```

---

## 下一步

1. 修复ANTLR jar文件问题
2. 重新生成解析器代码
3. 测试基本功能
4. 更新duan_visitor.py
5. 整合测试用例

---

**更新时间**：2026-06-13 00:01
**状态**：语法规则已修复，等待重新生成ANTLR代码
