import json
import time
from datetime import datetime, timezone
from typing import Dict, Any

from ..telemetry.collector import emit
from .db import get_session, init_db
from .models import SessionRecord, EventRecord


class DbStore:
    def __init__(self):
        init_db()

    def create_session(self, session_id: str, tenant_id: int | None = None):
        s = get_session()
        if s is None:
            return
        rec = SessionRecord(session_id=session_id, tenant_id=tenant_id)
        s.add(rec)
        s.commit()
        s.close()

    def session_exists(self, session_id: str) -> bool:
        s = get_session()
        if s is None:
            return False
        exists = s.query(SessionRecord).filter_by(session_id=session_id).first() is not None
        s.close()
        return exists

    def log_event(self, session_id: str, event: Dict[str, Any]):
        if "ts" not in event:
            event["ts"] = time.time()

        # Human-friendly timestamp for logs and API consumers.
        event["ts_readable"] = datetime.fromtimestamp(float(event["ts"]), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        emit({"session_id": session_id, **event})
        s = get_session()
        if s is None:
            return
        payload = json.dumps(event)
        rec = EventRecord(session_id=session_id, stage=event.get("stage"), payload=payload)
        s.add(rec)
        s.commit()
        s.close()

    def get_session(self, session_id: str) -> Dict[str, Any]:
        s = get_session()
        if s is None:
            return {}
        events = s.query(EventRecord).filter_by(session_id=session_id).order_by(EventRecord.id.asc()).all()
        s.close()
        return {"events": [json.loads(e.payload) for e in events]}

    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        s = get_session()
        if s is None:
            return {}
        sessions = s.query(SessionRecord).all()
        result = {}
        for sess in sessions:
            count = s.query(EventRecord).filter_by(session_id=sess.session_id).count()
            result[sess.session_id] = {"events": [None] * count}
        s.close()
        return result

    # approvals not persisted in DB for demo
    def add_pending_approval(self, session_id: str, approval_hash: str):
        pass

    def is_approved(self, session_id: str, approval_hash: str) -> bool:
        return False

    def approve(self, session_id: str, approval_hash: str) -> bool:
        return False
