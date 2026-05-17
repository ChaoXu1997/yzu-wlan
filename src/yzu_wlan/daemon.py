import logging
import time

from yzu_wlan.portal import get_portal_url, is_online, login

logger = logging.getLogger(__name__)


def run_daemon(cfg: dict, once: bool = False) -> None:
    check_interval = cfg.get("check_interval", 60)
    start_delay = cfg.get("start_delay", 5)
    connected = False

    while True:
        if is_online():
            if not connected:
                logger.info("已联网")
                connected = True
            if once:
                return
            time.sleep(check_interval)
            continue

        connected = False
        logger.info("未联网，%d 秒后尝试登录...", start_delay)
        time.sleep(start_delay)

        try:
            portal_url = get_portal_url()
            logger.debug("Portal URL: %s", portal_url)
        except Exception as e:
            logger.error("获取 Portal URL 失败: %s", e)
            if once:
                return
            time.sleep(check_interval)
            continue

        logger.info(
            "正在登录 (用户: %s, 服务商: %s)...", cfg["username"], cfg["service"]
        )
        try:
            login(portal_url, cfg["username"], cfg["password"], cfg["service"])
            logger.info("登录成功")
            connected = True
        except Exception as e:
            logger.error("登录失败: %s", e)

        if once:
            return
        time.sleep(check_interval)
