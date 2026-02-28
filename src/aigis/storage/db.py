from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings
from .models import Base

_ENGINE = None
_SESSION = None


def get_engine():
    global _ENGINE, _SESSION
    if _ENGINE is None:
        _ENGINE = create_engine(settings.database_url, echo=False, future=True)
        _SESSION = sessionmaker(bind=_ENGINE)
    return _ENGINE


def get_session():
    if not settings.aigis_db_enabled:
        return None
    if _SESSION is None:
        get_engine()
    return _SESSION()


def init_db():
    if not settings.aigis_db_enabled:
        return
    engine = get_engine()
    Base.metadata.create_all(engine)
