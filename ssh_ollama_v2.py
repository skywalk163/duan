import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.0.88', username='trae', password='trae123', timeout=30)

MODEL_NAME = 'duan_v2'

cmds = [
    # 写入 prompt 文件
    """cat > /home/trae/test_prompt.txt << 'EOF'
用段言v3.2语法重写以下Python代码。

Python代码:
x = 5
y = 10
print(x + y)
EOF""",

    # 用文件管道输入
    f'cat /home/trae/test_prompt.txt | OLLAMA_NUM_GPU_LAYERS=0 ollama run {MODEL_NAME} 2>&1',
]

for cmd in cmds:
    print(f'=== Running...')
    stdin, stdout, stderr = client.exec_command(cmd, timeout=None)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(out)
    if err:
        print(f'STDERR: {err}')
    print()

client.close()
print('Done!')