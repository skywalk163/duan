#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段言翻译器 — LoRA 合并 + GGUF 转换脚本

微调完成后，将 LoRA 权重合并到基础模型，然后可选地转换为
GGUF 格式（供 ollama / llama.cpp 使用）。

用法：
    # 只合并 LoRA（默认，自动检测模型）
    python merge_and_convert.py --merge-only

    # 合并 + 转 GGUF
    python merge_and_convert.py --convert-gguf

    # 使用预设（自动设置 base-model / lora-path / output-dir）
    python merge_and_convert.py --preset qwen3.5-2b --convert-gguf
    python merge_and_convert.py --preset qwen2.5-0.5b --merge-only

    # 指定路径
    python merge_and_convert.py --base-model ./model_cache/qwen2.5-0.5b --lora-path ./output/qwen2.5_0.5b_duan_gpu/final

前置条件（GGUF 转换）：
    git clone https://github.com/ggerganov/llama.cpp
    pip install -r llama.cpp/requirements.txt
"""

import argparse
import os
import sys
import subprocess
import shutil
from pathlib import Path

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_BASE_MODEL = os.path.join(_SCRIPT_DIR, "model_cache", "qwen2.5-0.5b")


def _find_lora_path():
    """自动检测 LoRA 权重路径，优先 GPU 训练产物，支持多模型"""
    # 按优先级检测所有已知模型的 GPU/CPU 输出目录
    candidates = [
        ("qwen3.5_2b_duan_gpu", "qwen3.5-2b"),
        ("qwen2.5_1.5b_duan_gpu", "qwen2.5-1.5b"),
        ("qwen2.5_0.5b_duan_gpu", "qwen2.5-0.5b"),
        ("qwen2.5_0.5b_duan_cpu", "qwen2.5-0.5b"),
    ]
    for name, label in candidates:
        p = os.path.join(_SCRIPT_DIR, "output", name, "final")
        if os.path.isdir(p):
            print(f"[自动检测] LoRA 路径: {p} ({label})")
            return p
    # 默认回退
    return os.path.join(_SCRIPT_DIR, "output", "qwen2.5_0.5b_duan_gpu", "final")


# 模型预设：与 train_gpu_lora.py 中的 MODEL_PRESETS 保持一致
MERGE_PRESETS = {
    "qwen2.5-0.5b": {
        "base_model": os.path.join(_SCRIPT_DIR, "model_cache", "qwen2.5-0.5b"),
        "lora_dir": "qwen2.5_0.5b_duan_gpu",
        "merged_dir": "duan_translator_merged_0.5b",
    },
    "qwen2.5-1.5b": {
        "base_model": os.path.join(_SCRIPT_DIR, "model_cache", "qwen2.5-1.5b"),
        "lora_dir": "qwen2.5_1.5b_duan_gpu",
        "merged_dir": "duan_translator_merged_1.5b",
    },
    "qwen3.5-2b": {
        "base_model": os.path.join(_SCRIPT_DIR, "model_cache", "qwen3.5-2b"),
        "lora_dir": "qwen3.5_2b_duan_gpu",
        "merged_dir": "duan_translator_merged_3.5_2b",
    },
}


_DEFAULT_LORA_PATH = _find_lora_path()
_DEFAULT_MERGED_DIR = os.path.join(_SCRIPT_DIR, "output", "duan_translator_merged")


def merge_lora(base_model_path: str, lora_path: str, output_dir: str):
    """合并 LoRA 权重到基础模型"""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print("=" * 60)
    print("合并 LoRA 权重")
    print("=" * 60)
    print(f"  基础模型: {base_model_path}")
    print(f"  LoRA 路径: {lora_path}")
    print(f"  输出目录: {output_dir}")
    print()

    # 加载基础模型
    print("[1/3] 加载基础模型...")
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_path, trust_remote_code=True
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        dtype=torch.float32,
        trust_remote_code=True,
    )
    print(f"  OK ({sum(p.numel() for p in base_model.parameters()) / 1e6:.1f}M params)")

    # 加载 LoRA
    print("[2/3] 加载 LoRA 权重...")
    model = PeftModel.from_pretrained(base_model, lora_path)
    print("  OK")

    # 合并
    print("[3/3] 合并权重...")
    merged_model = model.merge_and_unload()

    os.makedirs(output_dir, exist_ok=True)
    merged_model.save_pretrained(output_dir, safe_serialization=True)
    tokenizer.save_pretrained(output_dir)
    print(f"  合并后模型保存到: {output_dir}")

    # 保存 Modelfile（给 ollama 用）
    modelfile_path = os.path.join(output_dir, "Modelfile")
    with open(modelfile_path, "w", encoding="utf-8") as f:
        f.write("""# 段言翻译器 — ollama Modelfile
# 用法: ollama create duan-translator -f Modelfile

FROM ./duan_translator.gguf

TEMPLATE \"\"\"{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ end }}\"\"\"

SYSTEM \"\"\"你是段言（DuanLang）编程语言 v3.2 的翻译专家。你的任务是将 Python 代码翻译为段言 v3.2 代码。只输出段言代码，不要解释。\"\"\"

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|endoftext|>"
""")
    print(f"  Modelfile 保存到: {modelfile_path}")

    return output_dir


def convert_to_gguf(model_dir: str, output_gguf: str = None, quantize: str = "q4_k_m"):
    """将合并后的模型转换为 GGUF 格式

    需要 llama.cpp 的 convert_hf_to_gguf.py 脚本。
    """
    print("\n" + "=" * 60)
    print("转换为 GGUF 格式")
    print("=" * 60)

    if output_gguf is None:
        output_gguf = os.path.join(model_dir, "duan_translator.gguf")

    # 查找 llama.cpp 的转换脚本
    convert_script = None
    candidates = [
        os.path.join(_SCRIPT_DIR, "..", "..", "llama.cpp", "convert_hf_to_gguf.py"),
        os.path.join(os.path.expanduser("~"), "llama.cpp", "convert_hf_to_gguf.py"),
        "convert_hf_to_gguf.py",  # 如果在 PATH 中
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            convert_script = candidate
            break

    # 尝试 pip 安装的 llama_cpp
    if convert_script is None:
        try:
            import llama_cpp
            # 有些版本附带转换脚本
            convert_script = os.path.join(
                os.path.dirname(llama_cpp.__file__),
                "convert_hf_to_gguf.py",
            )
            if not os.path.exists(convert_script):
                convert_script = None
        except ImportError:
            pass

    if convert_script is None:
        print("[WARN] 未找到 llama.cpp 转换脚本")
        print("\n请手动安装 llama.cpp:")
        print("  git clone https://github.com/ggerganov/llama.cpp")
        print("  cd llama.cpp")
        print("  pip install -r requirements.txt")
        print(f"\n然后运行:")
        print(f"  python llama.cpp/convert_hf_to_gguf.py {model_dir} --outfile {output_gguf} --outtype {quantize}")
        print(f"\n或者使用 Python 直接推理（不需要 GGUF）:")
        print(f"  python local_infer.py --fine-tuned")
        return False

    print(f"  模型目录: {model_dir}")
    print(f"  输出 GGUF: {output_gguf}")
    print(f"  量化: {quantize}")
    print(f"  转换脚本: {convert_script}")
    print()

    cmd = [
        sys.executable, convert_script,
        model_dir,
        "--outfile", output_gguf,
        "--outtype", quantize,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"[ERROR] GGUF 转换失败:")
        print(result.stdout)
        print(result.stderr)
        return False

    print(f"  GGUF 转换完成: {output_gguf}")
    size_mb = os.path.getsize(output_gguf) / (1024 * 1024)
    print(f"  文件大小: {size_mb:.0f} MB")

    # 提示如何加载到 ollama
    print(f"\n加载到 ollama:")
    print(f"  cd {model_dir}")
    print(f"  ollama create duan-translator -f Modelfile")
    print(f"  ollama run duan-translator \"将以下代码翻译为段言: def add(a,b): return a+b\"")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="段言翻译器 — LoRA 合并 + GGUF 转换"
    )
    parser.add_argument(
        "--preset",
        choices=list(MERGE_PRESETS.keys()),
        default=None,
        help="模型预设，自动设置 base-model / lora-path / output-dir",
    )
    parser.add_argument(
        "--base-model", default=_DEFAULT_BASE_MODEL,
        help="基础模型路径",
    )
    parser.add_argument(
        "--lora-path", default=_DEFAULT_LORA_PATH,
        help="LoRA 权重路径",
    )
    parser.add_argument(
        "--output-dir", default=_DEFAULT_MERGED_DIR,
        help="合并后模型输出目录",
    )
    parser.add_argument(
        "--merge-only", action="store_true",
        help="只合并 LoRA，不转 GGUF",
    )
    parser.add_argument(
        "--convert-gguf", action="store_true",
        help="合并后转换为 GGUF 格式",
    )
    parser.add_argument(
        "--quantize", default="q4_k_m",
        choices=["f32", "f16", "q8_0", "q4_k_m", "q4_k_s", "q5_k_m"],
        help="GGUF 量化方式（默认 q4_k_m）",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # ── 应用模型预设 ──
    if args.preset:
        preset = MERGE_PRESETS[args.preset]
        args.base_model = preset["base_model"]
        args.lora_path = os.path.join(_SCRIPT_DIR, "output", preset["lora_dir"], "final")
        args.output_dir = os.path.join(_SCRIPT_DIR, "output", preset["merged_dir"])
        print(f"[预设] {args.preset}")
        print(f"  base_model: {args.base_model}")
        print(f"  lora_path: {args.lora_path}")
        print(f"  output_dir: {args.output_dir}")
        print()

    # 检查路径
    if not os.path.exists(args.base_model):
        print(f"[ERROR] 基础模型不存在: {args.base_model}")
        if args.preset:
            print("请先运行: python download_model.py")
        sys.exit(1)
    if not os.path.exists(args.lora_path):
        print(f"[ERROR] LoRA 权重不存在: {args.lora_path}")
        print("请先运行: python train_gpu_lora.py --preset " + (args.preset or "qwen2.5-0.5b"))
        sys.exit(1)

    # 合并
    merged_dir = merge_lora(args.base_model, args.lora_path, args.output_dir)

    # 转 GGUF
    if args.convert_gguf:
        convert_to_gguf(merged_dir, quantize=args.quantize)

    if not args.convert_gguf and not args.merge_only:
        # 默认只合并
        pass

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
    print(f"\n合并后模型: {merged_dir}")
    print(f"\n下一步:")
    print(f"  推理测试:     python local_infer.py --fine-tuned")
    print(f"  转 GGUF:      python merge_and_convert.py --convert-gguf")
    print(f"  ollama 加载:  cd {merged_dir} && ollama create duan-translator -f Modelfile")


if __name__ == "__main__":
    main()
