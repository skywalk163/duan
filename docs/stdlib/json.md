# JSON 模块

## 函数列表

| 函数 | 说明 |
|------|------|
| `解析(json_str)` | 解析 JSON 字符串 |
| `序列化(obj)` | 序列化为 JSON 字符串 |
| `美化(obj)` | 美化输出 JSON |
| `从文件读取(path)` | 从文件读取 JSON |
| `写入文件(path, obj)` | 写入 JSON 到文件 |

## 示例

```python
# 解析 JSON
设 数据 = 解析('{"name": "张三", "age": 18}')
印(数据["name"])

# 序列化
设 json_str = 序列化({"a": 1, "b": 2})
印(json_str)
```