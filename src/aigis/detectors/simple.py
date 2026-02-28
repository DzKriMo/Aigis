import re
from typing import Dict

from .semantic import SemanticMatcher

# NOTE: placeholder heuristics for MVP only. Replace with real models / services.

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"developer message",
    r"jailbreak",
]

JAILBREAK_PATTERNS = [
    r"do anything now",
    r"dan mode",
]

PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b\d{16}\b",  # card-like
]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",  # AWS key
    r"sk-[A-Za-z0-9]{20,}",  # OpenAI-like key
    r"BEGIN PRIVATE KEY",
]

POLICY_VIOLATION = [
    r"build a bomb",
    r"credit card fraud",
]

EXFIL_PATTERNS = [
    r"authorization:\s*bearer",
    r"api[-_ ]?key",
    r"password",
]

GOAL_HIJACK = [
    r"new instructions override",
    r"change the goal",
]

DATA_LEAKAGE = [
    r"internal only",
    r"confidential",
]


def _match_any(patterns, text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def detect_prompt_injection(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    return _match_any(INJECTION_PATTERNS, text) or matcher.match("prompt_injection", text)


def detect_jailbreak(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    return _match_any(JAILBREAK_PATTERNS, text) or matcher.match("jailbreak", text)


def detect_pii(text: str, context: Dict) -> bool:
    return _match_any(PII_PATTERNS, text)


def detect_secrets(text: str, context: Dict) -> bool:
    return _match_any(SECRET_PATTERNS, text)


def detect_policy_violation(text: str, context: Dict) -> bool:
    return _match_any(POLICY_VIOLATION, text)


def detect_exfiltration(text: str, context: Dict) -> bool:
    # If content is labeled confidential, be more aggressive
    labels = context.get("labels") or []
    if "CONFIDENTIAL" in labels and _match_any(EXFIL_PATTERNS, text):
        return True
    matcher = SemanticMatcher.from_env()
    return _match_any(EXFIL_PATTERNS, text) or matcher.match("exfiltration", text)


def detect_goal_hijack(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    return _match_any(GOAL_HIJACK, text) or matcher.match("goal_hijack", text)


def detect_data_leakage(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    return _match_any(DATA_LEAKAGE, text) or matcher.match("data_leakage", text)
