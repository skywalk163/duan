#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断训练 loss=0 的根因"""

import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

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

def main():
    from transformers import AutoTokenizer

    model_path = os.path.join(_SCRIPT_DIR, "model_cache", "qwen2.5-0.5b")
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load dataset
    dataset_path = os.path.join(_SCRIPT_DIR, "sft_dataset_enhanced.jsonl")
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = [json.loads(l) for l in f if l.strip()]

    print(f"Total samples: {len(data)}")

    max_len = 256
    over_count = 0
    zero_output_count = 0

    for i, item in enumerate(data):
        instruction = item.get("instruction", "")
        code_input = item.get("input", "")
        output = item.get("output", "")

        user_msg = f"{instruction}\n\nPython 代码：\n{code_input}" if code_input else instruction
        prompt_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        prompt_text = tokenizer.apply_chat_template(
            prompt_messages, tokenize=False, add_generation_prompt=True
        )
        prompt_ids = tokenizer(
            prompt_text, truncation=True, max_length=max_len, return_tensors=None
        )["input_ids"]

        full_messages = prompt_messages + [{"role": "assistant", "content": output}]
        full_text = tokenizer.apply_chat_template(
            full_messages, tokenize=False, add_generation_prompt=False
        )
        full_ids = tokenizer(
            full_text, truncation=True, max_length=max_len, return_tensors=None
        )["input_ids"]

        prompt_len = len(prompt_ids)
        full_len = len(full_ids)
        # output tokens = tokens after prompt that are not -100
        effective_output = full_len - min(prompt_len, full_len)

        if prompt_len >= max_len:
            over_count += 1
        if effective_output <= 0:
            zero_output_count += 1

        if i < 10:
            print(f"  [{i}] prompt={prompt_len}, full={full_len}, output_tokens={effective_output}, over_256={prompt_len >= max_len}")

    print(f"\n=== Summary ===")
    print(f"Samples with prompt >= max_len(256): {over_count}/{len(data)} ({over_count/len(data)*100:.1f}%)")
    print(f"Samples with 0 output tokens (no loss): {zero_output_count}/{len(data)} ({zero_output_count/len(data)*100:.1f}%)")

    # Also check with max_len=512
    max_len = 512
    over_count_512 = 0
    zero_output_count_512 = 0
    for item in data:
        instruction = item.get("instruction", "")
        code_input = item.get("input", "")
        user_msg = f"{instruction}\n\nPython 代码：\n{code_input}" if code_input else instruction
        prompt_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        prompt_text = tokenizer.apply_chat_template(
            prompt_messages, tokenize=False, add_generation_prompt=True
        )
        prompt_ids = tokenizer(
            prompt_text, truncation=True, max_length=max_len, return_tensors=None
        )["input_ids"]
        full_messages = prompt_messages + [{"role": "assistant", "content": output}]
        full_text = tokenizer.apply_chat_template(
            full_messages, tokenize=False, add_generation_prompt=False
        )
        full_ids = tokenizer(
            full_text, truncation=True, max_length=max_len, return_tensors=None
        )["input_ids"]
        prompt_len = len(prompt_ids)
        full_len = len(full_ids)
        effective_output = full_len - min(prompt_len, full_len)
        if prompt_len >= max_len:
            over_count_512 += 1
        if effective_output <= 0:
            zero_output_count_512 += 1

    print(f"\nWith max_len=512:")
    print(f"  Over: {over_count_512}/{len(data)} ({over_count_512/len(data)*100:.1f}%)")
    print(f"  Zero output: {zero_output_count_512}/{len(data)} ({zero_output_count_512/len(data)*100:.1f}%)")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
