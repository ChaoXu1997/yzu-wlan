import json
import os
import sys
from pathlib import Path

CONFIG_DIR = (
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "yzu-wlan"
)
CONFIG_PATH = CONFIG_DIR / "config.json"

ISP_SERVICES = [
    "电信互联网服务",
    "移动互联网服务",
    "联通互联网服务",
    "学校互联网服务",
    "校内免费服务",
]

DEFAULT_SERVICE = "电信互联网服务"

DEFAULTS = {
    "service": DEFAULT_SERVICE,
    "check_interval": 60,
    "start_delay": 5,
}


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        return None
    with open(path) as f:
        cfg = json.load(f)
    for key in ("username", "password"):
        if key not in cfg:
            return None
    if cfg.get("service") not in ISP_SERVICES:
        cfg["service"] = DEFAULT_SERVICE
    for key, val in DEFAULTS.items():
        cfg.setdefault(key, val)
    return cfg


def save_config(cfg: dict, path: Path = CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)
        f.write("\n")
    os.chmod(path, 0o600)


def setup_wizard(path: Path = CONFIG_PATH) -> dict:
    print("=== 扬州大学校园网自动登录 配置向导 ===\n")

    existing = load_config(path)

    username = input(
        f"用户名 [{'*' * len(existing['username'])}]: " if existing else "用户名: "
    )
    if not username and existing:
        username = existing["username"]
    while not username:
        print("用户名不能为空")
        username = input("用户名: ")

    password = input(
        f"密码 [{'*' * len(existing['password'])}]: " if existing else "密码: "
    )
    if not password and existing:
        password = existing["password"]
    while not password:
        print("密码不能为空")
        password = input("密码: ")

    print(f"\n网络服务商:")
    for i, svc in enumerate(ISP_SERVICES, 1):
        marker = " (默认)" if svc == DEFAULT_SERVICE else ""
        print(f"  {i}. {svc}{marker}")

    default_idx = ISP_SERVICES.index(DEFAULT_SERVICE) + 1
    svc_input = input(f"选择 [1-{len(ISP_SERVICES)}] (默认 {default_idx}): ").strip()
    if svc_input:
        try:
            idx = int(svc_input)
            service = ISP_SERVICES[idx - 1]
        except (ValueError, IndexError):
            print(f"无效选择，使用默认: {DEFAULT_SERVICE}")
            service = DEFAULT_SERVICE
    else:
        service = DEFAULT_SERVICE

    interval_input = input("检测间隔/秒 (默认 60): ").strip()
    check_interval = int(interval_input) if interval_input else 60

    delay_input = input("重连延时/秒 (默认 5): ").strip()
    start_delay = int(delay_input) if delay_input else 5

    cfg = {
        "username": username,
        "password": password,
        "service": service,
        "check_interval": check_interval,
        "start_delay": start_delay,
    }

    save_config(cfg, path)
    print(f"\n配置已保存到 {path}")
    return cfg
