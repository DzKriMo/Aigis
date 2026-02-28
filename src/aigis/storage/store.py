from typing import Dict, Any

from ..telemetry.collector import emit

class InMemoryStore:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str):
        self.sessions[session_id] = {
            "events": [],
            "pending_approvals": set(),
            "approved": set(),
        }

    def session_exists(self, session_id: str) -> bool:
        return session_id in self.sessions

    def log_event(self, session_id: str, event: Dict[str, Any]):
        self.sessions[session_id]["events"].append(event)
        emit({"session_id": session_id, **event})

    def add_pending_approval(self, session_id: str, approval_hash: str):
        self.sessions[session_id]["pending_approvals"].add(approval_hash)

    def is_approved(self, session_id: str, approval_hash: str) -> bool:
        return approval_hash in self.sessions[session_id]["approved"]

    def approve(self, session_id: str, approval_hash: str) -> bool:
        pending = self.sessions[session_id]["pending_approvals"]
        if approval_hash not in pending:
            return False
        pending.remove(approval_hash)
        self.sessions[session_id]["approved"].add(approval_hash)
        return True

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self.sessions.get(session_id, {})

    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        return self.sessions
