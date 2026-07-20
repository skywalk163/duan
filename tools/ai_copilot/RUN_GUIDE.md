# 段言 LoRA 微调运行指南

本指南说明如何在本地使用小模型 LoRA 微调，让模型学会将 Python 代码翻译为段言 v3.2 代码。

## 快速总结

- **基础模型**：Qwen2.5-0.5B-Instruct（0.5B 参数，CPU 也能跑）
- **训练方法**：LoRA 微调（只训练 q/v/k/o_proj，参数量 ~0.1%）
- **数据集**：881 条 Python→段言 对照（`sft_dataset.jsonl`）
- **2步验证训练**：28 秒完成，LoRA 权重 2.1MB
- **全量训练 CPU 估算**：~5.1 小时（不推荐）
- **全量训练 GPU 估算**：~8 分钟（RTX 3060） / ~3 分钟（RTX 4090）

## 文件结构

```
tools/ai_copilot/
├── sft_dataset.jsonl           # 训练数据（881 条 Python→段言 对照）
├── train_cpu_lora.py           # CPU 训练脚本（已验证可用）
├── train_gpu_lora.py           # GPU 训练脚本（推荐，速度提升 30 倍）
├── download_model.py           # 模型下载脚本
├── local_infer.py              # 推理脚本
├── merge_and_convert.py        # LoRA 合并 & GGUF 转换
├── model_cache/
│   └── qwen2.5-0.5b/           # 基础模型（~1GB）
└── output/
    ├── smoke_test/             # 2步验证训练产物
    └── qwen2.5_0.5b_duan_gpu/  # GPU 全量训练产物
```

## 环境准备

### CPU 环境（开发验证用）

```bash
# 安装 PyTorch CPU 版
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 安装其余依赖
pip install transformers peft datasets accelerate

# Windows 还需要 VC++ Redistributable
# 下载: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### GPU 环境（全量训练用）

```bash
# 安装 GPU 版 PyTorch（根据 CUDA 版本）
pip install torch --index-url https://download.pytorch.org/whl/cu121

# 安装其余依赖
pip install transformers peft datasets accelerate

# 如需 QLoRA 4bit 量化训练（显存不够时）
pip install bitsandbytes
```

## 下载模型

```bash
cd tools/ai_copilot

# 使用 HF 镜像下载（国内推荐）
HF_ENDPOINT=https://hf-mirror.com python download_model.py --model qwen2.5-0.5b
```

如果下载超时，可以手动用 curl 下载：

```bash
curl -L -o model_cache/qwen2.5-0.5b/model.safetensors \
  "https://hf-mirror.com/Qwen/Qwen2.5-0.5B-Instruct/resolve/main/model.safetensors"
```

## 训练

### 2步验证训练（CPU，30 秒内）

验证全流程是否跑通：

```bash
python train_cpu_lora.py --max-steps 2 --batch-size 2 --grad-accum 1 --max-len 256 \
  --output-dir output/smoke_test
```

验证内容：
- 模型能加载 ✓
- LoRA 配置正确 ✓
- 数据集能读取 ✓
- 训练能跑 ✓
- 权重能保存 ✓

### 全量训练（GPU 推荐）

```bash
# 标准 GPU 训练（~8 分钟，RTX 3060）
python train_gpu_lora.py

# 快速验证（GPU 上 2 步）
python train_gpu_lora.py --max-steps 2

# QLoRA 4bit 量化（显存 < 4GB 时）
python train_gpu_lora.py --qlora

# 使用更大模型（效果更好）
python train_gpu_lora.py --model-path ./model_cache/qwen2.5-1.5b

# 自定义参数
python train_gpu_lora.py --epochs 5 --lora-rank 32 --batch-size 16
```

### 全量训练（CPU，不推荐，~5 小时）

```bash
# 过夜运行
python train_cpu_lora.py --epochs 3
```

## 推理验证

### 方法 1：直接 Python 脚本

```bash
# 训练后测试推理
python train_gpu_lora.py --test-infer

# 或单独推理
python local_infer.py --fine-tuned "写一个冒泡排序"
```

### 方法 2：自定义推理脚本

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model_path = "tools/ai_copilot/model_cache/qwen2.5-0.5b"
lora_path = "tools/ai_copilot/output/qwen2.5_0.5b_duan_gpu/final"

tokenizer = AutoTokenizer.from_pretrained(model_path)
base = AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.float32)
model = PeftModel.from_pretrained(base, lora_path)

messages = [
    {"role": "system", "content": "你是段言翻译专家..."},
    {"role": "user", "content": "将以下 Python 翻译为段言：\ndef add(a,b): return a+b"},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

## 训练参数说明

| 参数 | CPU 默认 | GPU 默认 | 说明 |
|------|----------|----------|------|
| `--epochs` | 3 | 3 | 训练轮数 |
| `--lora-rank` | 8 | 16 | LoRA 秩，越大效果越好但越慢 |
| `--lora-alpha` | 16 | 32 | LoRA alpha，通常 = rank × 2 |
| `--lr` | 2e-4 | 2e-4 | 学习率 |
| `--max-len` | 512 | 512 | 最大序列长度 |
| `--batch-size` | 1 | 8 | 批大小 |
| `--grad-accum` | 16 | 2 | 梯度累积步数 |
| `--max-steps` | -1 | -1 | 最大步数（正数覆盖 epochs） |
| `--qlora` | N/A | False | 4bit 量化训练 |

## 预期效果

训练 3 epochs 后，模型应能正确翻译：

| Python | 段言 |
|--------|------|
| `x = 10` | `设 x 为 10` |
| `def add(a, b): return a + b` | `段落 加法 接收 a, b：\n    返回 a 加 b` |
| `for i in range(10): print(i)` | `遍历 i 于 0至10：\n    打印(i)` |
| `if x > 5: print("大")` | `如果 x 大于 5：\n    打印("大")` |

## 后续步骤

1. **合并 LoRA**：`python merge_and_convert.py --merge-only`
2. **转 GGUF**：`python merge_and_convert.py --convert-gguf`
3. **集成到 CLI**：`duan ai local "写一个冒泡排序"`
4. **部署到 ollama**：参考 `local_infer.py` 的 ollama 后端

## 故障排除

### torch 导入失败（Windows）

```
OSError: [WinError 126] 找不到指定的模块
```

**解决**：安装 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### 模型下载超时

**解决**：使用 HF 镜像 `HF_ENDPOINT=https://hf-mirror.com`，或用 `curl -C -` 断点续传

### 显存不足

**解决**：使用 QLoRA 4bit 量化 `--qlora`，或减小 `--batch-size` 和 `--max-len`
