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

# Domains that intentionally resolve to loopback/private IPs (DNS rebinding / local routing tricks).
REBOUNDING_SUFFIXES = (
    ".localtest.me",
    ".lvh.me",
    ".nip.io",
    ".sslip.io",
    ".xip.io",
)
REBOUNDING_EXACT = {
    "localtest.me",
    "lvh.me",
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


def _is_rebinding_domain(host: str) -> bool:
    h = (host or "").strip().lower().rstrip(".")
    if not h:
        return False
    if h in REBOUNDING_EXACT:
        return True
    return any(h.endswith(suffix) for suffix in REBOUNDING_SUFFIXES)


def evaluate_urls(urls: List[str], allowlist: List[str], denylist: List[str]) -> NetworkDecision:
    for raw in urls:
        parsed = urlparse(raw)
        host = parsed.hostname or ""
        if not host:
            continue
        host_l = host.lower()

        if host_l in METADATA_HOSTS:
            return NetworkDecision(blocked=True, message="Metadata endpoint blocked", risk_score=0.9)
        if _is_private_ip(host_l):
            return NetworkDecision(blocked=True, message="Private IP blocked", risk_score=0.8)
        if _is_rebinding_domain(host_l):
            return NetworkDecision(blocked=True, message="Potential DNS rebinding host blocked", risk_score=0.85)
        if denylist and host_l in {d.lower() for d in denylist}:
            return NetworkDecision(blocked=True, message="Domain denylisted", risk_score=0.7)
        if allowlist and host_l not in {a.lower() for a in allowlist}:
            return NetworkDecision(blocked=True, message="Domain not allowlisted", risk_score=0.6)
    return NetworkDecision(blocked=False)
