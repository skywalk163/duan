import paramiko
from ssh_config import SSH_HOST, SSH_USER_TRAE, SSH_PASS_TRAE

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER_TRAE, password=SSH_PASS_TRAE, timeout=10)

cmds = [
    'ls /usr/local/bin/python* 2>&1',
    'ls /usr/bin/python* 2>&1',
    'pkg info | grep python 2>&1',
    'pip --version 2>&1',
    'pip3 --version 2>&1',
    'echo $PATH',
    'ollama list 2>&1',
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