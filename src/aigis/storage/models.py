from __future__ import annotations

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey

Base = declarative_base()


class Tenant(Base):
    __tablename__ = "aigis_tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)


class ApiKey(Base):
    __tablename__ = "aigis_api_keys"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("aigis_tenants.id"), nullable=False)
    key = Column(String(128), nullable=False, unique=True)
    active = Column(Boolean, default=True)


class SessionRecord(Base):
    __tablename__ = "aigis_sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), nullable=False, unique=True)
    tenant_id = Column(Integer, ForeignKey("aigis_tenants.id"), nullable=True)


class EventRecord(Base):
    __tablename__ = "aigis_events"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), nullable=False)
    stage = Column(String(64), nullable=True)
    payload = Column(Text, nullable=False)


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
