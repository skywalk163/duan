"""SSH 配置 - 从 .env 文件读取敏感信息，避免硬编码密码"""
import os


def _load_env():
    """从 .env 文件加载环境变量（不覆盖已有的环境变量）"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ.setdefault(key, value)
    return os.environ


_load_env()


def get(key, default=None):
    return os.environ.get(key, default)


# 便捷属性
SSH_HOST = os.environ.get('SSH_HOST', '')
SSH_USER_TRAE = os.environ.get('SSH_USER_TRAE', '')
SSH_PASS_TRAE = os.environ.get('SSH_PASS_TRAE', '')
SSH_USER_DUMATE = os.environ.get('SSH_USER_DUMATE', '')
SSH_PASS_DUMATE = os.environ.get('SSH_PASS_DUMATE', '')
SSH_PASS_DUMATE2 = os.environ.get('SSH_PASS_DUMATE2', '')
SUDO_PASS = os.environ.get('SUDO_PASS', '')