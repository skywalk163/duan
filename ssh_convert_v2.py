import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.0.88', username='trae', password='trae123', timeout=30)

MODEL_DIR = '/home/skywalk/Downloads/kaggle/working/output_v2/v1-20260731-092537/checkpoint-192-merged'
OUTPUT_DIR = '/home/trae/duan_model_v2'
OUTPUT_GGUF = '/home/trae/duan_translator_v2_fp16.gguf'
LLAMA_DIR = '/home/trae/llama.cpp'

cmds = [
    # 1. 用 sudo -S 并传入密码来复制模型
    f"echo 'trae123' | sudo -S rm -rf {OUTPUT_DIR}",
    f"echo 'trae123' | sudo -S cp -r {MODEL_DIR} {OUTPUT_DIR}",
    f"echo 'trae123' | sudo -S chmod -R 777 {OUTPUT_DIR}",

    # 2. 确认文件可读
    f'ls -la {OUTPUT_DIR}/',

    # 3. 转换模型
    f'cd {LLAMA_DIR} && python3.12 convert_hf_to_gguf.py {OUTPUT_DIR} --outfile {OUTPUT_GGUF} --outtype f16 2>&1',

    # 4. 检查输出文件
    f'ls -lh {OUTPUT_GGUF}',
]

for cmd in cmds:
    print(f'=== Running: {cmd}')
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(out)
    if err:
        print(f'STDERR: {err}')
    print()

client.close()
print('Done!')