#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言翻译器 — GPU LoRA 微调脚本

针对 GPU 环境优化，使用 transformers + peft 在 GPU 上对
Qwen2.5-0.5B-Instruct（或更大模型）进行 LoRA/QLoRA 微调。

与 train_cpu_lora.py 的区别：
  - 使用 bf16 混合精度（GPU 原生支持，速度提升 2-3 倍）
  - 更大 batch_size（16 vs 1），充分利用 GPU 并行
  - 更大 max_len（512 vs 256），覆盖更长代码样本
  - 更多 LoRA target modules（all-linear），效果更好
  - 支持 QLoRA 4bit 量化（显存不够时的降级方案）
  - 支持 gradient_checkpointing（省显存，适合大模型）

预计训练时间（Qwen2.5-0.5B，881 条 × 3 epochs = 2643 样本）：
  - RTX 3060 (12GB):  ~8 分钟
  - RTX 4090 (24GB):  ~3 分钟
  - A100 (40GB):      ~1 分钟

显存需求：
  - Qwen2.5-0.5B LoRA bf16:  ~3 GB
  - Qwen2.5-0.5B QLoRA 4bit: ~2 GB
  - Qwen2.5-1.5B LoRA bf16:  ~6 GB
  - Qwen2.5-1.5B QLoRA 4bit: ~4 GB

用法：
    # 标准训练（自动检测 GPU）
    python train_gpu_lora.py

    # 快速验证（2步）
    python train_gpu_lora.py --max-steps 2

    # QLoRA 4bit 量化训练（显存不够时）
    python train_gpu_lora.py --qlora

    # 使用更大模型
    python train_gpu_lora.py --model-path ./model_cache/qwen2.5-1.5b

    # 自定义参数
    python train_gpu_lora.py --epochs 5 --lora-rank 16 --batch-size 8

    # 训练后测试推理
    python train_gpu_lora.py --test-infer

前置条件：
    # GPU 版 PyTorch（根据 CUDA 版本选择）
    pip install torch --index-url https://download.pytorch.org/whl/cu121
    pip install transformers peft datasets accelerate

    # 如需 QLoRA
    pip install bitsandbytes
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ── 路径常量 ─
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATASET_PATH = os.path.join(_SCRIPT_DIR, "sft_dataset.jsonl")
_DEFAULT_MODEL_PATH = os.path.join(_SCRIPT_DIR, "model_cache", "qwen2.5-0.5b")
_DEFAULT_OUTPUT_DIR = os.path.join(_SCRIPT_DIR, "output", "qwen2.5_0.5b_duan_gpu")

# ── 系统提示词（与 CPU 版一致）──
SYSTEM_PROMPT = (
    "你是段言（DuanLang）编程语言 v3.2 的翻译专家。"
    "段言是一种中文编程语言，使用中文关键字。"
    "你的任务是将 Python 代码翻译为段言 v3.2 代码。\n"
    "关键规则：\n"
    "- 变量赋值: 设 x 为 10\n"
    "- 字符串赋值: 定义 s 等于 \"hello\"\n"
    "- 段落定义: 段落 名 接收 参数：\n"
    "- 条件: 如果 / 否则如果 / 否则：\n"
    "- 循环: 遍历 i 于 0至N： / 当 条件：\n"
    "- 运算: 加/减/乘/除以/取余/加上/减去/乘以\n"
    "- 比较: 等于/不等于/大于/小于/大于等于/小于等于\n"
    "- 逻辑: 且/或/非\n"
    "- 布尔: 真/假/空\n"
    "- 跳转: 跳出(break)/跳过(continue)/返回(return)\n"
    "- 长度: 用 len() 而非 长度()\n"
    "- 列表索引赋值: lst[0] = 10\n"
    "- 打印: 打印(x)"
)


# ═══════════════════════════════════════════════════════════════════
# 第 1 步：环境检查
# ═══════════════════════════════════════════════════════════════════

def check_environment(require_gpu: bool = True) -> bool:
    """检查 GPU 环境"""
    print("=" * 60)
    print("第 1 步：环境检查（GPU 模式）")
    print("=" * 60)

    ok = True

    # PyTorch + CUDA
    try:
        import torch
        print(f"  [OK] PyTorch {torch.__version__}")
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_mem / 1e9
            print(f"  [OK] GPU: {gpu_name} ({gpu_mem:.1f} GB)")
        else:
            if require_gpu:
                print("  [FAIL] 未检测到 GPU，此脚本需要 GPU 环境")
                print("         如需 CPU 训练，请使用 train_cpu_lora.py")
                ok = False
            else:
                print("  [WARN] 未检测到 GPU，将回退到 CPU 模式（会很慢）")
    except ImportError:
        print("  [FAIL] PyTorch 未安装")
        print("         pip install torch --index-url https://download.pytorch.org/whl/cu121")
        ok = False

    # transformers
    try:
        import transformers
        print(f"  [OK] transformers {transformers.__version__}")
    except ImportError:
        print("  [FAIL] transformers 未安装")
        ok = False

    # peft
    try:
        import peft
        print(f"  [OK] peft {peft.__version__}")
    except ImportError:
        print("  [FAIL] peft 未安装")
        ok = False

    # bitsandbytes（QLoRA 需要）
    try:
        import bitsandbytes
        print(f"  [OK] bitsandbytes {bitsandbytes.__version__}")
    except ImportError:
        print("  [WARN] bitsandbytes 未安装（仅 QLoRA 模式需要）")

    # 数据集
    if os.path.exists(_DATASET_PATH):
        with open(_DATASET_PATH, "r", encoding="utf-8") as f:
            count = sum(1 for _ in f)
        print(f"  [OK] 数据集: {_DATASET_PATH} ({count} 条)")
    else:
        print(f"  [FAIL] 数据集不存在: {_DATASET_PATH}")
        ok = False

    return ok


# ═══════════════════════════════════════════════════════════════════
# 第 2 步：数据集
# ═══════════════════════════════════════════════════════════════════

import torch
from torch.utils.data import Dataset


class DuanSFTDataset(Dataset):
    """段言 SFT 数据集（与 CPU 版共用同一数据格式）"""

    def __init__(self, jsonl_path: str, tokenizer, max_len: int = 512):
        self.data = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                self.data.append(item)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        instruction = item.get("instruction", "将Python代码转为段言代码：")
        code_input = item.get("input", "")
        output = item.get("output", "")

        # 构造 user 消息
        if code_input:
            user_msg = f"{instruction}\n\nPython 代码：\n{code_input}"
        else:
            user_msg = instruction

        # 构造 prompt 部分（system + user，不计算 loss）
        prompt_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        prompt_text = self.tokenizer.apply_chat_template(
            prompt_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        # 构造完整文本（prompt + assistant 回复）
        full_messages = prompt_messages + [
            {"role": "assistant", "content": output},
        ]
        full_text = self.tokenizer.apply_chat_template(
            full_messages,
            tokenize=False,
            add_generation_prompt=False,
        )

        # tokenize
        prompt_ids = self.tokenizer(
            prompt_text, truncation=True, max_length=self.max_len,
            return_tensors=None,
        )["input_ids"]

        full_ids = self.tokenizer(
            full_text, truncation=True, max_length=self.max_len,
            return_tensors=None,
        )["input_ids"]

        # labels: prompt 部分设为 -100，只对 assistant 回复计算 loss
        labels = list(full_ids)
        prompt_len = len(prompt_ids)
        for i in range(min(prompt_len, len(labels))):
            labels[i] = -100

        # padding 到 max_len
        pad_id = self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
        attention_mask = [1] * len(full_ids)

        while len(full_ids) < self.max_len:
            full_ids.append(pad_id)
            attention_mask.append(0)
            labels.append(-100)

        # 截断到 max_len
        full_ids = full_ids[: self.max_len]
        attention_mask = attention_mask[: self.max_len]
        labels = labels[: self.max_len]

        return {
            "input_ids": torch.tensor(full_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


# ═══════════════════════════════════════════════════════════════════
# 第 3 步：训练
# ═══════════════════════════════════════════════════════════════════

def train(
    model_path: str,
    output_dir: str,
    epochs: int = 3,
    lora_rank: int = 16,
    lora_alpha: int = 32,
    lr: float = 2e-4,
    max_len: int = 512,
    batch_size: int = 8,
    grad_accum: int = 2,
    warmup_ratio: float = 0.05,
    save_steps: int = 50,
    dataset_path: str = None,
    max_steps: int = -1,
    use_qlora: bool = False,
    gradient_checkpointing: bool = True,
):
    """执行 GPU LoRA 微调"""
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        BitsAndBytesConfig,
    )
    from peft import LoraConfig, get_peft_model, TaskType

    print("\n" + "=" * 60)
    print("第 2 步：加载模型")
    print("=" * 60)
    print(f"  模型路径: {model_path}")
    print(f"  QLoRA 4bit: {'是' if use_qlora else '否'}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_path, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # 加载模型 —— GPU 模式使用 bf16 或 4bit 量化
    if use_qlora:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=bnb_config,
            trust_remote_code=True,
        )
        print("  [QLoRA] 模型已 4bit 量化加载")
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        print("  [LoRA] 模型已 bf16 加载")

    # 自动选择设备
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    print(f"  设备: {device}")
    print(f"  模型参数量: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")

    # gradient checkpointing（省显存，大模型推荐）
    if gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False
        print("  [OK] gradient checkpointing 已启用")

    # ── 配置 LoRA ──
    print("\n" + "=" * 60)
    print("第 3 步：配置 LoRA")
    print("=" * 60)

    # GPU 版：训练更多模块（all-linear），效果更好
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_rank,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── 加载数据集 ──
    print("\n" + "=" * 60)
    print("第 4 步：加载数据集")
    print("=" * 60)

    train_dataset = DuanSFTDataset(dataset_path or _DATASET_PATH, tokenizer, max_len=max_len)
    print(f"  训练数据: {len(train_dataset)} 条")
    print(f"  max_len: {max_len}")

    # 统计类别分布
    categories = {}
    for item in train_dataset.data:
        cat = item.get("category", "未知")
        categories[cat] = categories.get(cat, 0) + 1
    print("  类别分布:")
    for cat, cnt in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {cnt}")

    # ── 训练参数 ──
    print("\n" + "=" * 60)
    print("第 5 步：训练（GPU）")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    checkpoint_dir = os.path.join(output_dir, "checkpoints")

    total_samples = len(train_dataset) * epochs
    total_steps = total_samples // (batch_size * grad_accum) + 1
    if max_steps > 0:
        total_steps = max_steps

    # GPU 速度估算
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        # 粗略估算：0.5B 模型 ~0.1秒/样本, 1.5B ~0.3秒/样本
        param_count = sum(p.numel() for p in model.parameters()) / 1e9
        sec_per_sample = max(0.05, param_count * 0.2)
        est_time = total_samples * sec_per_sample
        print(f"  GPU: {gpu_name}")
        print(f"  预计总步数: ~{total_steps}")
        print(f"  预计时间: ~{est_time:.0f} 秒 ({est_time / 60:.1f} 分钟)")
    else:
        print(f"  预计总步数: ~{total_steps}")
        print(f"  [WARN] CPU 模式，预计 ~{total_samples * 7 / 3600:.1f} 小时")

    print(f"  batch_size: {batch_size} x grad_accum: {grad_accum} = 等效 batch {batch_size * grad_accum}")
    print(f"  epochs: {epochs}, lr: {lr}, LoRA rank: {lora_rank}")
    print(f"  precision: bf16, QLoRA: {use_qlora}")
    print()

    training_args = TrainingArguments(
        output_dir=checkpoint_dir,
        num_train_epochs=epochs,
        max_steps=max_steps,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=lr,
        lr_scheduler_type="cosine",
        warmup_ratio=warmup_ratio,
        logging_steps=5,
        save_steps=save_steps,
        save_total_limit=3,
        bf16=torch.cuda.is_available(),  # GPU 用 bf16
        fp16=False,
        gradient_checkpointing=gradient_checkpointing,
        report_to="none",
        seed=42,
        dataloader_num_workers=0,
        remove_unused_columns=False,
        optim="adamw_torch",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        processing_class=tokenizer,
    )

    t0 = time.time()
    trainer.train()
    elapsed = time.time() - t0

    print(f"\n训练完成！耗时 {elapsed:.0f} 秒 ({elapsed / 60:.1f} 分钟)")

    # ── 保存 ──
    final_dir = os.path.join(output_dir, "final")
    model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    print(f"\nLoRA 权重保存到: {final_dir}")

    # 保存训练信息
    info = {
        "model_path": model_path,
        "dataset_path": _DATASET_PATH,
        "dataset_size": len(train_dataset),
        "epochs": epochs,
        "lora_rank": lora_rank,
        "lora_alpha": lora_alpha,
        "lr": lr,
        "max_len": max_len,
        "batch_size": batch_size,
        "grad_accum": grad_accum,
        "use_qlora": use_qlora,
        "training_time_seconds": elapsed,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "system_prompt": SYSTEM_PROMPT,
    }
    info_path = os.path.join(output_dir, "training_info.json")
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"训练信息保存到: {info_path}")

    return final_dir


# ═══════════════════════════════════════════════════════════════════
# 第 4 步：推理测试
# ═══════════════════════════════════════════════════════════════════

def test_inference(model_path: str, lora_path: str):
    """测试微调后的模型推理"""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print("\n" + "=" * 60)
    print("推理测试")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    tokenizer = AutoTokenizer.from_pretrained(
        model_path, trust_remote_code=True
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        model_path, dtype=dtype, trust_remote_code=True
    ).to(device)
    model = PeftModel.from_pretrained(base_model, lora_path).to(device)
    model.eval()

    test_cases = [
        ("def add(a, b):\n    return a + b", "加法段落"),
        ("for i in range(10):\n    print(i)", "循环打印"),
        ("def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "递归阶乘"),
        ("x = 10\ny = 20\nif x > y:\n    print('x大')\nelse:\n    print('y大')", "条件判断"),
        ("data = [3, 1, 4, 1, 5, 9, 2, 6]\ndata.sort()\nprint(data)", "列表排序"),
    ]

    for python_code, desc in test_cases:
        print(f"\n--- {desc} ---")
        print(f"Python: {python_code}")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"将以下 Python 代码翻译为段言 v3.2：\n\n{python_code}"},
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(text, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        response = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
        print(f"段言: {response}")


# ═══════════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="段言翻译器 — GPU LoRA 微调（需要 GPU 环境）"
    )
    parser.add_argument(
        "--model-path", default=_DEFAULT_MODEL_PATH,
        help=f"预训练模型路径（默认 {_DEFAULT_MODEL_PATH}）",
    )
    parser.add_argument(
        "--output-dir", default=_DEFAULT_OUTPUT_DIR,
        help=f"输出目录（默认 {_DEFAULT_OUTPUT_DIR}）",
    )
    parser.add_argument("--epochs", type=int, default=3, help="训练轮数（默认 3）")
    parser.add_argument("--lora-rank", type=int, default=16, help="LoRA rank（默认 16）")
    parser.add_argument("--lora-alpha", type=int, default=32, help="LoRA alpha（默认 32）")
    parser.add_argument("--lr", type=float, default=2e-4, help="学习率（默认 2e-4）")
    parser.add_argument("--max-len", type=int, default=512, help="最大序列长度（默认 512）")
    parser.add_argument("--batch-size", type=int, default=8, help="batch size（默认 8）")
    parser.add_argument("--grad-accum", type=int, default=2, help="梯度累积步数（默认 2）")
    parser.add_argument("--save-steps", type=int, default=50, help="保存间隔（默认 50）")
    parser.add_argument(
        "--max-steps", type=int, default=-1,
        help="最大训练步数（-1 表示用 epochs，正数则覆盖 epochs）",
    )
    parser.add_argument(
        "--dataset", default=None,
        help="自定义数据集路径（默认 sft_dataset.jsonl）",
    )
    parser.add_argument("--qlora", action="store_true", help="使用 QLoRA 4bit 量化训练（省显存）")
    parser.add_argument("--no-gc", action="store_true", help="禁用 gradient checkpointing")
    parser.add_argument("--dry-run", action="store_true", help="只检查环境不训练")
    parser.add_argument("--test-infer", action="store_true", help="训练后测试推理")
    parser.add_argument("--no-gpu-required", action="store_true", help="允许在无 GPU 时回退到 CPU")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # 环境检查
    if not check_environment(require_gpu=not args.no_gpu_required):
        print("\n环境检查未通过，请先安装缺失的依赖。")
        sys.exit(1)

    # 检查自定义数据集
    dataset_path = args.dataset
    if dataset_path:
        if not os.path.isabs(dataset_path):
            dataset_path = os.path.join(_SCRIPT_DIR, dataset_path)
        if not os.path.exists(dataset_path):
            print(f"\n[ERROR] 数据集不存在: {dataset_path}")
            sys.exit(1)
        print(f"\n使用自定义数据集: {dataset_path}")

    if args.dry_run:
        print("\n[Dry-run] 环境检查通过，未执行训练。")
        return

    # 检查模型路径
    if not os.path.exists(args.model_path):
        print(f"\n[ERROR] 模型路径不存在: {args.model_path}")
        print("请先运行: python download_model.py")
        sys.exit(1)

    # 训练
    final_dir = train(
        model_path=args.model_path,
        output_dir=args.output_dir,
        epochs=args.epochs,
        lora_rank=args.lora_rank,
        lora_alpha=args.lora_alpha,
        lr=args.lr,
        max_len=args.max_len,
        batch_size=args.batch_size,
        grad_accum=args.grad_accum,
        save_steps=args.save_steps,
        dataset_path=args.dataset,
        max_steps=args.max_steps,
        use_qlora=args.qlora,
        gradient_checkpointing=not args.no_gc,
    )

    # 推理测试
    if args.test_infer:
        test_inference(args.model_path, final_dir)

    print("\n" + "=" * 60)
    print("全部完成！")
    print("=" * 60)
    print(f"\n下一步：")
    print(f"  1. 合并 LoRA:    python merge_and_convert.py --merge-only")
    print(f"  2. 转 GGUF:      python merge_and_convert.py --convert-gguf")
    print(f"  3. 本地推理:     python local_infer.py --fine-tuned")
    print(f"  4. 集成到 CLI:   duan ai local \"写一个冒泡排序\"")


if __name__ == "__main__":
    main()
