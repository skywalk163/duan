import paramiko
from ssh_config import SSH_HOST, SSH_USER_TRAE, SSH_PASS_TRAE

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER_TRAE, password=SSH_PASS_TRAE, timeout=10)

cmds = [
    'python3 --version 2>&1 || python --version 2>&1',
    'which python3 2>&1 || which python 2>&1',
    'which ollama 2>&1',
    'which git 2>&1',
    'pip3 list 2>/dev/null | grep -i torch || pip list 2>/dev/null | grep -i torch',
    'freebsd-version',
]

for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f'[{cmd}]')
    if out:
        print(f'  out: {out}')
    if err:
        print(f'  err: {err}')

client.close()