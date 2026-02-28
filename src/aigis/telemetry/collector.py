from __future__ import annotations

import json
import time
from typing import Dict, Any

from ..config import settings


def emit(event: Dict[str, Any]):
    if not settings.aigis_telemetry_enabled:
        return
    payload = {
        "ts": time.time(),
        "event": event,
    }
    line = json.dumps(payload, ensure_ascii=False)
    if settings.aigis_telemetry_path:
        with open(settings.aigis_telemetry_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    else:
        print(line)
