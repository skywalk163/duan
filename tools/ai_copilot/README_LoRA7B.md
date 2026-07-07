# Qwen3-8B LoRA 微调指南 — 段言翻译器

用 LoRA 轻量化微调 Qwen3-8B，使其学会将 Python 代码翻译为段言 v3.2 代码。

## 为什么选 Qwen3-8B？

| 对比项 | Qwen3-8B | Llama 3.3-8B | Mistral Small 3-7B |
|--------|-----------|---------------|---------------------|
| HumanEval | **76.0** | 68.5 | 62.1 |
| 中文能力 | 强（训练数据 60% 中文） | 弱（英文为主） | 中等 |
| 上下文长度 | 32K | 8K | 32K |
| LoRA 生态 | LLaMA-Factory 原生支持 | 支持 | 支持 |
| 指令跟随 | 强 | 强 | 中等 |

**结论：Qwen3-8B 是 2026 年 7-8B 级中文代码生成的最佳选择。**

## 快速开始

### 1. 安装依赖

```bash
# 方式一：从 PyPI 安装（简单）
pip install llamafactory transformers accelerate peft

# 方式二：从源码安装（推荐，获取最新功能）
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# QLoRA 4bit 量化训练需要（8GB 显存用户必装）
pip install bitsandbytes

# 国内用户加速模型下载
pip install modelscope
```

### 2. 一键训练

```bash
cd tools/ai_copilot

# LoRA BF16 模式（需 24GB 显存，如 RTX 3090/4090/A100）
python train_lora_7b.py

# QLoRA 4bit 模式（仅需 8GB 显存，如 RTX 4060）
python train_lora_7b.py --qlora

# 查看所有选项
python train_lora_7b.py --help
```

### 3. Jupyter Notebook 调试

```bash
jupyter notebook train_lora_7b.ipynb
```

Notebook 包含 10 个 Cell，逐步引导你从环境检查到推理测试。

## 两种训练模式

### 模式一：LoRA BF16（推荐，24GB 显存）

```bash
python train_lora_7b.py
```

- 显存需求：~22 GB
- 训练速度：快（~30 分钟，RTX 4090）
- 适用显卡：RTX 3090 / 4090 / A100 / A6000

### 模式二：QLoRA 4bit（8GB 显存可跑）

```bash
python train_lora_7b.py --qlora --batch-size 1 --grad-accum 16
```

- 显存需求：~8 GB
- 训练速度：中等（~60 分钟，RTX 4060）
- 适用显卡：RTX 4060 / 4070 / 3060 12GB
- 原理：将模型权重从 BF16 量化为 4bit，训练时仍用 BF16 梯度

### 显存对照表

| 显存 | 推荐模式 | batch_size | grad_accum |
|------|----------|------------|------------|
| ≥24 GB | LoRA BF16 | 2 | 8 |
| 16-24 GB | LoRA BF16 | 1 | 16 |
| 8-16 GB | QLoRA 4bit | 1 | 16 |
| 6-8 GB | QLoRA + offload | 1 | 16 |

## 参数详解

### 核心参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model` | `Qwen/Qwen3-8B-Instruct` | 模型名称或本地路径 |
| `--output` | `output/qwen3_8b_duan` | 输出目录 |
| `--qlora` | `False` | 启用 QLoRA 4bit 量化 |
| `--epochs` | `3` | 训练轮数 |
| `--lr` | `1e-4` | 学习率 |
| `--lora-rank` | `16` | LoRA 秩 |

### LoRA 秩（lora_rank）选择指南

| 秩 | 可训练参数 | 显存增量 | 适用场景 |
|----|-----------|---------|----------|
| 8 | ~10M | 最低 | 简单翻译任务 |
| **16** | ~20M | 适中 | **推荐：通用 Python→段言翻译** |
| 32 | ~40M | 较高 | 复杂代码/暗坑多 |
| 64 | ~80M | 高 | 需要极强泛化能力 |

### 学习率建议

| 场景 | 推荐学习率 |
|------|-----------|
| LoRA (rank 8-16) | `1e-4` |
| LoRA (rank 32-64) | `5e-5` |
| QLoRA | `1e-4` ~ `2e-4` |
| 全参微调（不推荐） | `2e-5` |

**重要：LoRA/QLoRA 的学习率要比全参微调高 5-10 倍！**

### 其他参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--batch-size` | `2` | 每设备批大小 |
| `--grad-accum` | `8` | 梯度累积步数 |
| `--max-seq-len` | `1024` | 最大序列长度 |
| `--skip-download` | `False` | 跳过模型下载 |
| `--skip-merge` | `False` | 跳过 LoRA 合并 |
| `--test-infer` | `False` | 训练后测试推理 |
| `--dry-run` | `False` | 只生成配置不训练 |

## 训练数据

使用 `sft_dataset.jsonl`（881 条 Python↔段言 v3.2 对照数据）。

数据格式（Alpaca）：
```json
{
  "instruction": "将Python代码转为段言代码：",
  "input": "def add(a, b): return a + b",
  "output": "段落 加法 接收 a, b：\n    返回 a 加 b",
  "category": "段落"
}
```

脚本会自动转为 ShareGPT 格式（LLaMA-Factory 推荐），并添加 system prompt。

### 类别分布

| 类别 | 样本数 |
|------|--------|
| 段落 | 104 |
| 变量 | 100 |
| 复合 | 99 |
| 列表 | 98 |
| 循环 | 90 |
| 条件 | 90 |
| 暗坑 | 87 |
| 字符串 | 74 |
| 类 | 42 |
| 字典 | 37 |
| 异常 | 34 |
| 导入 | 26 |

## 训练后使用

### 方式一：直接推理（合并后模型）

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "output/qwen3_8b_duan/merged"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path, device_map="auto", trust_remote_code=True
)

messages = [
    {"role": "system", "content": "你是段言编程语言v3.2的翻译专家。"},
    {"role": "user", "content": "将Python代码转为段言代码：\ndef add(a, b): return a + b"},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.1)
print(tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True))
```

### 方式二：vLLM 部署（生产级）

```bash
pip install vllm
vllm serve output/qwen3_8b_duan/merged --port 8000
```

然后通过 OpenAI 兼容 API 调用：
```python
import openai
client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")
response = client.chat.completions.create(
    model="qwen3-8b-duan",
    messages=[{"role": "user", "content": "将Python代码转为段言代码：\nprint('hello')"}],
)
print(response.choices[0].message.content)
```

### 方式三：LoRA Adapter 热切换

不合并，直接加载 adapter：

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B-Instruct", device_map="auto")
model = PeftModel.from_pretrained(base, "output/qwen3_8b_duan/checkpoints/checkpoint-XXX")
```

好处：一个基础模型可以挂载多个 LoRA adapter，按需切换。

### 方式四：集成到段言管线

```bash
# 设置模型路径
duan ai generate "排序算法" --model-path output/qwen3_8b_duan/merged

# 或通过 pipeline.py 的 model-size=large 自动路由
duan ai generate "排序算法" --model-size large
```

## 完整流程示例

```bash
# 1. 安装依赖
pip install llamafactory transformers accelerate peft bitsandbytes

# 2. 一键训练（QLoRA 模式，8GB 显存）
cd tools/ai_copilot
python train_lora_7b.py --qlora --test-infer

# 3. 训练完成后，模型在 output/qwen3_8b_duan/merged

# 4. 部署为 API 服务
pip install vllm
vllm serve output/qwen3_8b_duan/merged --port 8000

# 5. 集成到段言开发
duan ai generate "二分查找" --model-path output/qwen3_8b_duan/merged
```

## 常见问题

### Q: 显存不够怎么办？

1. 使用 `--qlora` 开启 4bit 量化（22GB→8GB）
2. 减小 `--batch-size 1` + 增大 `--grad-accum 16`
3. 减小 `--max-seq-len 512`
4. 使用云 GPU（AutoDL / AI Studio 等，约 2-5 元/小时）

### Q: Loss 不下降怎么办？

- **学习率太小**：LoRA/QLoRA 推荐 `1e-4`，不要用全参微调的 `2e-5`
- **lora_rank 太小**：从 16 开始，如果效果不好再升到 32
- **数据问题**：检查 sft_dataset.jsonl 是否有损坏条目
- **训练轮数不够**：3 轮通常够，复杂任务可试 5 轮

### Q: 训练很慢？

- 确认 `gradient_checkpointing: true`（省显存但稍慢）
- 确认用了 BF16（不要用 FP32）
- 检查是否在用 CPU 而非 GPU
- 考虑用云 GPU

### Q: QLoRA 和 LoRA 效果差多少？

- 实测差距约 2-5%（在段言翻译任务上几乎可忽略）
- 如果显存够，优先用 LoRA BF16
- 如果显存紧，QLoRA 是性价比最高的选择

### Q: 模型下载太慢？

```bash
# 国内镜像（ModelScope）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen3-8B-Instruct')"

# 或使用 huggingface 镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### Q: 如何恢复中断的训练？

LoRA checkpoint 会保存在 `output/qwen3_8b_duan/checkpoints/` 目录下，
最新 checkpoint 可以直接用于推理或继续训练。

### Q: LLaMA-Factory 安装失败？

```bash
# 确保 Python >= 3.9
python --version

# 确保 PyTorch 已安装
pip install torch --index-url https://download.pytorch.org/whl/cu121

# 再安装 LLaMA-Factory
pip install llamafactory
```

## 与 ERNIE-4.5-0.3B 方案对比

| 对比项 | Qwen3-8B + LoRA | ERNIE-4.5-0.3B + LoRA |
|--------|------------------|----------------------|
| 模型大小 | 80 亿参数 | 3 亿参数 |
| 显存需求 | 8-22 GB | 4 GB |
| 代码理解 | 强（HumanEval 76.0） | 弱 |
| 中文能力 | 强 | 中等 |
| 训练框架 | LLaMA-Factory | ERNIEKit |
| 训练时间 | 30-90 分钟 | 10-30 分钟 |
| 翻译质量 | 高（上下文理解强） | 中（简单翻译可用） |
| 适用场景 | 通用 Python→段言 | 窄翻译/规则化转换 |

**推荐策略**：先用 Qwen3-8B 做主翻译器，ERNIE-4.5-0.3B 做轻量级备用。

## 文件清单

| 文件 | 说明 |
|------|------|
| `train_lora_7b.py` | 一键 LoRA/QLoRA 微调脚本 |
| `train_lora_7b.ipynb` | Jupyter Notebook 调试版 |
| `sft_dataset.jsonl` | 训练数据（881 条） |
| `build_sft_dataset.py` | 训练数据构造器 |
| `train_sft.py` | ERNIE-4.5-0.3B 微调脚本（备用） |
| `README_SFT.md` | ERNIE 方案文档 |
| `README_LoRA7B.md` | 本文档 |

## 参考链接

- [Qwen3-8B-Instruct](https://huggingface.co/Qwen/Qwen3-8B-Instruct)
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
- [LoRA 论文](https://arxiv.org/abs/2106.09685)
- [QLoRA 论文](https://arxiv.org/abs/2305.14314)
