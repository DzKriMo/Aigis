from fastapi import Header, HTTPException
from ..config import settings

def require_api_key(x_api_key: str = Header(default="")):
    if not x_api_key or x_api_key != settings.aigis_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
