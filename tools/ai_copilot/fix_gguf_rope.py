#!/usr/bin/env python3
"""
修复 GGUF 文件中 rope.freq_base 为 0.0 的问题。

问题根因：
  safetensors -> GGUF 转换时，qwen2.rope.freq_base 可能丢失为 0.0，
  导致 llama.cpp 在采样阶段触发断言崩溃 (llama-sampling.cpp:662)。

修复方法：
  在 GGUF 文件中定位 qwen2.rope.freq_base 的字节偏移，
  将其从 0.0 修改为 1000000.0（Qwen2.5 默认值）。

用法：
  python fix_gguf_rope.py <input.gguf> [output.gguf]

  - 不指定 output 时，在原文件上就地修改（会自动备份 .bak）
  - 指定 output 时，写入新文件，原文件不变
"""

import struct
import sys
import shutil
import os


DEFAULT_ROPE_FREQ_BASE = 1000000.0  # Qwen2.5 默认值


def find_rope_freq_base_offset(gguf_path: str) -> int:
    """在 GGUF 文件中找到 qwen2.rope.freq_base 的字节偏移。

    返回值：
      成功时返回 freq_base 值的字节偏移（float32，4 字节）。
      如果未找到则抛出 RuntimeError。
    """
    with open(gguf_path, "rb") as f:
        magic = f.read(4)
        if magic != b"GGUF":
            raise ValueError(f"不是 GGUF 文件: magic={magic!r}")

        version = struct.unpack("<I", f.read(4))[0]
        tensor_count = struct.unpack("<Q", f.read(8))[0]
        kv_count = struct.unpack("<Q", f.read(8))[0]

        for _ in range(kv_count):
            # 读取 key (gguf string: u64 len + bytes)
            key_len = struct.unpack("<Q", f.read(8))[0]
            key = f.read(key_len).decode("utf-8")

            # 读取 value type
            vtype = struct.unpack("<I", f.read(4))[0]
            val_offset = f.tell()

            if vtype == 6:  # FLOAT32
                val = struct.unpack("<f", f.read(4))[0]
                if key == "qwen2.rope.freq_base":
                    return val_offset
            elif vtype in (0, 1, 7):  # UINT8, INT8, BOOL
                f.read(1)
            elif vtype in (2, 3):  # UINT16, INT16
                f.read(2)
            elif vtype in (4, 5):  # UINT32, INT32
                f.read(4)
            elif vtype == 8:  # STRING
                slen = struct.unpack("<Q", f.read(8))[0]
                f.read(slen)
            elif vtype == 9:  # ARRAY
                arr_type = struct.unpack("<I", f.read(4))[0]
                arr_len = struct.unpack("<Q", f.read(8))[0]
                _skip_array(f, arr_type, arr_len)
            elif vtype in (10, 11, 12):  # UINT64, INT64, FLOAT64
                f.read(8)
            else:
                raise ValueError(f"未知的 GGUF value type: {vtype}")

    raise RuntimeError("未在 GGUF 文件中找到 qwen2.rope.freq_base")


def _skip_array(f, arr_type: int, arr_len: int):
    """跳过 GGUF 数组数据。"""
    type_sizes = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1, 10: 8, 11: 8, 12: 8}
    if arr_type in type_sizes:
        f.read(type_sizes[arr_type] * arr_len)
    elif arr_type == 8:  # STRING array
        for _ in range(arr_len):
            sl = struct.unpack("<Q", f.read(8))[0]
            f.read(sl)
    else:
        raise ValueError(f"未知的数组元素类型: {arr_type}")


def read_freq_base(gguf_path: str) -> float:
    """读取当前 rope.freq_base 值。"""
    offset = find_rope_freq_base_offset(gguf_path)
    with open(gguf_path, "rb") as f:
        f.seek(offset)
        return struct.unpack("<f", f.read(4))[0]


def fix_rope_freq_base(input_path: str, output_path: str | None = None):
    """修复 GGUF 文件中的 rope.freq_base。

    Args:
      input_path: 输入 GGUF 文件路径。
      output_path: 输出路径。None 时就地修改（自动备份 .bak）。
    """
    current = read_freq_base(input_path)
    print(f"当前 rope.freq_base = {current}")

    if current == DEFAULT_ROPE_FREQ_BASE:
        print(f"已经是 {DEFAULT_ROPE_FREQ_BASE}，无需修复。")
        if output_path and output_path != input_path:
            shutil.copy2(input_path, output_path)
            print(f"已复制到 {output_path}")
        return

    if current != 0.0:
        print(f"警告：当前值 {current} 不是 0.0，仍将修改为 {DEFAULT_ROPE_FREQ_BASE}")

    offset = find_rope_freq_base_offset(input_path)
    new_bytes = struct.pack("<f", DEFAULT_ROPE_FREQ_BASE)

    if output_path is None:
        # 就地修改，先备份
        bak_path = input_path + ".bak"
        shutil.copy2(input_path, bak_path)
        print(f"备份保存到 {bak_path}")

        with open(input_path, "r+b") as f:
            f.seek(offset)
            f.write(new_bytes)
        output_path = input_path
    else:
        # 写入新文件
        with open(input_path, "rb") as src, open(output_path, "wb") as dst:
            data = bytearray(src.read())
            data[offset : offset + 4] = new_bytes
            dst.write(data)

    # 验证
    verify = read_freq_base(output_path)
    print(f"修复完成: {output_path}")
    print(f"验证 rope.freq_base = {verify}")
    if verify != DEFAULT_ROPE_FREQ_BASE:
        raise RuntimeError(f"验证失败: 期望 {DEFAULT_ROPE_FREQ_BASE}, 实际 {verify}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None

    if not os.path.isfile(input_path):
        print(f"错误: 文件不存在: {input_path}")
        sys.exit(1)

    fix_rope_freq_base(input_path, output_path)


if __name__ == "__main__":
    main()
