import argparse
import logging
import sys
from pathlib import Path

from yzu_wlan import __version__
from yzu_wlan.config import CONFIG_PATH, load_config, setup_wizard
from yzu_wlan.daemon import run_daemon


def main():
    parser = argparse.ArgumentParser(
        prog="yzu-wlan",
        description="扬州大学校园网自动登录",
    )
    parser.add_argument("--config", type=Path, default=CONFIG_PATH, help="配置文件路径")
    parser.add_argument("--daemon", action="store_true", help="以守护进程模式持续运行")
    parser.add_argument("--setup", action="store_true", help="运行配置向导")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument(
        "--version", action="version", version=f"yzu-wlan {__version__}"
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%H:%M:%S"
    )

    if args.setup:
        setup_wizard(args.config)
        return

    cfg = load_config(args.config)
    if cfg is None:
        print("未找到配置，正在运行配置向导...\n")
        cfg = setup_wizard(args.config)

    try:
        run_daemon(cfg, once=not args.daemon)
    except KeyboardInterrupt:
        sys.exit(0)
