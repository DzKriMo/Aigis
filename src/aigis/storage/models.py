from __future__ import annotations

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean

Base = declarative_base()


class PolicyRecord(Base):
    __tablename__ = "aigis_policies"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    stage = Column(String(32), nullable=False)
    action = Column(String(32), nullable=False)
    match_json = Column(Text, nullable=False)
    risk = Column(String(32), nullable=True)
    enabled = Column(Boolean, default=True)


class ToolPolicyRecord(Base):
    __tablename__ = "aigis_tool_policies"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    allowed_envs = Column(Text, nullable=True)  # JSON array
    allowlist = Column(Text, nullable=True)  # JSON array
    timeout_seconds = Column(Integer, nullable=False, default=5)
    max_bytes = Column(Integer, nullable=True)
