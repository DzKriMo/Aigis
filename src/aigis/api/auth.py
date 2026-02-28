from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth.api_key import require_api_key
from ..auth.jwt import create_token
from ..config import settings
from ..storage.db import get_session, init_db
from ..storage.models import Tenant, ApiKey

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/auth/token", response_model=TokenResponse, dependencies=[Depends(require_api_key)])
def issue_token():
    # Demo: issue token for default tenant/api key
    init_db()
    s = get_session()
    if s is None:
        raise HTTPException(status_code=500, detail="DB disabled")
    tenant = s.query(Tenant).filter_by(name="default").first()
    if tenant is None:
        tenant = Tenant(name="default")
        s.add(tenant)
        s.commit()
        s.refresh(tenant)
    key = s.query(ApiKey).filter_by(key=settings.aigis_api_key).first()
    if key is None:
        key = ApiKey(tenant_id=tenant.id, key=settings.aigis_api_key, active=True)
        s.add(key)
        s.commit()
    s.close()
    token = create_token(tenant_id=tenant.id, api_key=settings.aigis_api_key)
    return TokenResponse(access_token=token)
