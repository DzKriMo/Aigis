import datetime
import jwt

from ..config import settings


def create_token(tenant_id: int, api_key: str) -> str:
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(minutes=settings.jwt_exp_minutes)
    payload = {
        "iss": settings.jwt_issuer,
        "iat": now,
        "exp": exp,
        "tenant_id": tenant_id,
        "api_key": api_key,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)
