from __future__ import annotations

import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..config import settings

_ENGINE = None
_SESSION_FACTORY = None


def _ensure_engine():
    global _ENGINE, _SESSION_FACTORY
    if _ENGINE is not None:
        return
    _ENGINE = create_async_engine(settings.database_url, echo=False)
    _SESSION_FACTORY = sessionmaker(_ENGINE, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> Optional[AsyncSession]:
    if not settings.aigis_db_enabled:
        return None
    _ensure_engine()
    return _SESSION_FACTORY()


def run_async(coro):
    return asyncio.run(coro)
