# duan-blocks

段言积木组合平台——把「用户自然语言需求」映射为「预置积木的组合装配」，零 token、全离线。

```
duan-combo "对一批数字求和再算平均" --输入 "[1,2,3,4,5]"
duan-combo "把这段中文转成拼音" --输入 '"你好"' --json
```

- **零 token 常态**：选块/校验/接线/粘合全本地（概念图 + TF-IDF 混合选块，不调 LLM）。
- **兜底沉淀**：仅能力缺失时经 LLM（或本地规则）生成新积木并永久入库存，下次零 token 复用。
- **运行依赖**：段言运行时（`pip install duan`）；拼音/繁简等中文能力可选
  `pip install duan-blocks[zh]`（pypinyin / opencc）。
- **定位**：默认从当前目录向上找仓库内 `积木库/`，也可 `export DUAN_BLOCKS_LIB=/path/to/积木库`。
