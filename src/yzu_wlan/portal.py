import json
import logging
import re
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError

logger = logging.getLogger(__name__)

_PORTAL_DETECT_URL = "http://123.123.123.123"
_ONLINE_CHECK_URL = "http://111.13.141.31/generate_204"
_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"


def is_online() -> bool:
    req = Request(_ONLINE_CHECK_URL, headers={"Host": "connect.rom.miui.com"})
    try:
        resp = urlopen(req, timeout=5)
        return resp.status == 204
    except Exception:
        return False


def get_portal_url() -> str:
    req = Request(_PORTAL_DETECT_URL, headers={"User-Agent": _USER_AGENT})
    try:
        resp = urlopen(req, timeout=5)
    except URLError as e:
        if hasattr(e, "read"):
            body = e.read().decode("utf-8", errors="replace")
        else:
            raise RuntimeError(f"Cannot get portal URL: {e}")
    else:
        body = resp.read().decode("utf-8", errors="replace")

    match = re.search(r"href='([^']+)'", body)
    if not match:
        raise RuntimeError("Cannot find portal URL in redirect page")
    return match.group(1)


def login(portal_url: str, username: str, password: str, service: str) -> None:
    match = re.match(r"http://(.+?)/.*?\?(.+)", portal_url)
    if not match:
        raise RuntimeError(f"Invalid portal URL: {portal_url}")
    host = match.group(1)
    query_string = match.group(2)

    body = urlencode(
        {
            "userId": username,
            "password": password,
            "service": quote(service, safe=""),
            "queryString": query_string,
            "validcode": "",
            "passwordEncrypt": "false",
        }
    )

    url = f"http://{host}/eportal/InterFace.do?method=login"
    req = Request(
        url,
        data=body.encode("utf-8"),
        headers={
            "User-Agent": _USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        resp = urlopen(req, timeout=5)
    except Exception as e:
        raise RuntimeError(f"Login request failed: {e}")

    data = json.loads(resp.read().decode("utf-8"))
    if data.get("result") != "success":
        raise RuntimeError(data.get("message", "Unknown login error"))
