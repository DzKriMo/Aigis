from dataclasses import dataclass
from typing import List
import ipaddress
from urllib.parse import urlparse

METADATA_HOSTS = {
    "169.254.169.254",
    "metadata.google.internal",
    "169.254.170.2",
    "100.100.100.200",
}

@dataclass
class NetworkDecision:
    blocked: bool = False
    message: str | None = None
    risk_score: float = 0.0

    def to_dict(self):
        return {"blocked": self.blocked, "message": self.message, "risk_score": self.risk_score}


def _is_private_ip(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False


def evaluate_urls(urls: List[str], allowlist: List[str], denylist: List[str]) -> NetworkDecision:
    for raw in urls:
        parsed = urlparse(raw)
        host = parsed.hostname or ""
        if not host:
            continue
        if host in METADATA_HOSTS:
            return NetworkDecision(blocked=True, message="Metadata endpoint blocked", risk_score=0.9)
        if _is_private_ip(host):
            return NetworkDecision(blocked=True, message="Private IP blocked", risk_score=0.8)
        if denylist and host in denylist:
            return NetworkDecision(blocked=True, message="Domain denylisted", risk_score=0.7)
        if allowlist and host not in allowlist:
            return NetworkDecision(blocked=True, message="Domain not allowlisted", risk_score=0.6)
    return NetworkDecision(blocked=False)
