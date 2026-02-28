from fastapi import APIRouter, Depends
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}
