# Source - https://github.com/django/django/blob/main/django/core/validators.py#L130

import ipaddress
import re
from urllib.parse import urlsplit

_UL = "\u00a1-\uffff"

_HOSTNAME_RE = (
    r"[a-z" + _UL + r"0-9](?:[a-z" + _UL + r"0-9-]{0,61}[a-z" + _UL + r"0-9])?"
)
_DOMAIN_RE = r"(?:\.(?!-)[a-z" + _UL + r"0-9-]{1,63}(?<!-))*"
_TLD_RE = (
    r"\."  # pyright: ignore[reportImplicitStringConcatenation]
    r"(?!-)"
    r"(?:[a-z" + _UL + "-]{2,63}"  # pyright: ignore[reportImplicitStringConcatenation]
    r"|xn--[a-z0-9]{1,59})"
    r"(?<!-)"
    r"\.?"
)

_IPV4_RE = (
    r"(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)"
    r"(?:\.(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)){3}"
)

_HOST_RE = "(" + _HOSTNAME_RE + _DOMAIN_RE + _TLD_RE + "|localhost)"

_URL_RE = re.compile(
    r"^(?:[a-z0-9.+-]*)://"  # pyright: ignore[reportImplicitStringConcatenation]
    r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"
    r"(?:" + _IPV4_RE + r"|\[[0-9a-f:.]+\]|" + _HOST_RE + ")"  # pyright: ignore[reportImplicitStringConcatenation]
    r"(?::[0-9]{1,5})?"
    r"(?:[/?#][^\s]*)?"
    r"\Z",
    re.IGNORECASE,
)

_ALLOWED_SCHEMES = {"http", "https", "ftp", "ftps"}
_UNSAFE_CHARS = frozenset("\t\r\n")


def validate_url(url: str) -> bool:
    stripped_url = url.strip()

    if len(stripped_url) > 2048:
        return False

    if _UNSAFE_CHARS.intersection(stripped_url):
        return False

    scheme = stripped_url.split("://")[0].lower()
    if scheme not in _ALLOWED_SCHEMES:
        return False

    try:
        splitted_url = urlsplit(stripped_url)
    except ValueError:
        return False

    if not _URL_RE.match(stripped_url):
        return False

    host_match = re.search(r"^\[(.+)\](?::[0-9]{1,5})?$", splitted_url.netloc)
    if host_match:
        try:
            _ = ipaddress.IPv6Address(host_match[1])
        except ValueError:
            return False

    if splitted_url.hostname is None or len(splitted_url.hostname) > 253:
        return False

    return True
