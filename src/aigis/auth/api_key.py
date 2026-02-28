from fastapi import Header, HTTPException, Request
from ..config import settings
from .rate_limit import limiter


def require_api_key(x_api_key: str = Header(default=""), request: Request = None):
    if not x_api_key or x_api_key != settings.aigis_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    client_id = x_api_key
    if request and request.client:
        client_id = f"{x_api_key}:{request.client.host}"
    if not limiter.allow(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
