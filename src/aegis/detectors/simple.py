import re
from typing import Dict

from .semantic import SemanticMatcher

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore (all|any) (previous|prior|earlier) (instructions?|rules?)",
    r"disregard (the )?(above|previous|prior) (instructions?|rules?)",
    r"forget (your|all) (instructions?|guardrails?|safety)",
    r"override (the )?(system|developer|policy) (prompt|message|instructions?)",
    r"system prompt",
    r"system configuration",
    r"developer message",
    r"hidden instructions",
    r"jailbreak",
]

JAILBREAK_PATTERNS = [
    r"do anything now",
    r"dan mode",
    r"no rules mode",
    r"bypass (all )?(safety|guardrails?|restrictions?)",
]

PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b\d{16}\b",
]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"sk-[A-Za-z0-9]{20,}",
    r"BEGIN PRIVATE KEY",
]

POLICY_VIOLATION = [
    r"build a bomb",
    r"credit card fraud",
]

EXFIL_PATTERNS = [
    r"authorization:\s*bearer",
    r"api[-_ ]?key",
    r"\b(environment variables?|env vars?)\b",
    r"\b(exfiltrat(e|ion)|steal|dump|leak|export)\b.{0,60}\b(credentials?|tokens?|secrets?|passwords?|api[-_ ]?keys?|environment variables?)\b",
    r"\b(output|print|reveal|show|display|tell|list)\b.{0,100}\b(system (prompt|configuration|instructions?)|developer message|hidden instructions?|hidden policies?|internal (rules|config|policy)|secret(s)?|token(s)?|api[-_ ]?key|environment variables?|env vars?)\b",
]

GOAL_HIJACK = [
    r"new instructions override",
    r"change the goal",
    r"before answering",
    r"before doing that",
    r"do this first",
    r"instead of your instructions",
]

DATA_LEAKAGE = [
    r"internal only",
    r"confidential",
]

TASK_VERBS = re.compile(
    r"\b(summarize|summarise|translate|analyze|analyse|answer|write|explain|draft|review)\b",
    re.IGNORECASE,
)
LEAK_VERBS = re.compile(r"\b(output|reveal|print|show|display|dump|expose|list|tell)\b", re.IGNORECASE)
DISCLOSURE_QUERY_VERBS = re.compile(r"\b(what|which|show|tell|list|print|reveal|output|dump|display)\b", re.IGNORECASE)
SENSITIVE_TARGETS = re.compile(
    r"\b(system (prompt|configuration|instructions?)|initial instructions?|instructions you were initialized with|developer message|hidden instructions?|hidden policies?|internal (rules|config|policy)|policies govern your responses|chain[- ]of[- ]thought|environment variables?|env vars?)\b",
    re.IGNORECASE,
)
SEQUENCE_MARKERS = re.compile(
    r"\b(before answering|before you answer|before doing that|first[, ]|then[, ]|also[, ]|prior to answering)\b",
    re.IGNORECASE,
)
RESEARCH_CONTEXT = re.compile(
    r"\b(example|for example|demonstrate|demonstration|explain|analyze|analysis|awareness|training|defensive|red team|research)\b",
    re.IGNORECASE,
)
FICTION_CONTEXT = re.compile(r"\b(fiction|fictional|story|novel|script|roleplay)\b", re.IGNORECASE)
DIRECT_IMPERATIVE = re.compile(
    r"\b(ignore|disregard|forget|override|reveal|output|print|dump|show|display|expose|tell|list)\b",
    re.IGNORECASE,
)


def _match_any(patterns, text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def _looks_like_benign_discussion(text: str) -> bool:
    has_injection_topic = bool(re.search(r"\b(prompt injection|jailbreak)\b", text, re.IGNORECASE))
    return bool(has_injection_topic and RESEARCH_CONTEXT.search(text))


def _is_fictional_context(text: str) -> bool:
    return bool(FICTION_CONTEXT.search(text))


def _has_direct_sensitive_exfil_request(text: str) -> bool:
    has_sensitive_target = bool(SENSITIVE_TARGETS.search(text))
    if not has_sensitive_target:
        return False
    return bool(LEAK_VERBS.search(text) or DISCLOSURE_QUERY_VERBS.search(text))


def _multi_stage_hijack_score(text: str) -> int:
    score = 0
    benign_discussion = _looks_like_benign_discussion(text)

    if _match_any(INJECTION_PATTERNS, text):
        score += 2
    if SEQUENCE_MARKERS.search(text):
        score += 1
    if TASK_VERBS.search(text):
        score += 1
    if _has_direct_sensitive_exfil_request(text):
        score += 4
    if re.search(r"\b(entire|full|complete|exact|any)\b", text, re.IGNORECASE) and SENSITIVE_TARGETS.search(text):
        score += 1

    if benign_discussion and not _has_direct_sensitive_exfil_request(text):
        score = min(score, 2)

    return score


def detect_prompt_injection(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    llm = context.get("llm_classification", {})

    strong_attack = _multi_stage_hijack_score(text) >= 4
    benign_discussion = _looks_like_benign_discussion(text)

    if _is_fictional_context(text) and not strong_attack:
        return False
    if strong_attack:
        return True
    if benign_discussion:
        return True

    return _match_any(INJECTION_PATTERNS, text) or matcher.match("prompt_injection", text) or bool(llm.get("prompt_injection", False))


def detect_jailbreak(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    llm = context.get("llm_classification", {})
    return _match_any(JAILBREAK_PATTERNS, text) or matcher.match("jailbreak", text) or bool(llm.get("jailbreak", False))


def detect_pii(text: str, context: Dict) -> bool:
    llm = context.get("llm_classification", {})
    return _match_any(PII_PATTERNS, text) or bool(llm.get("pii", False))


def detect_secrets(text: str, context: Dict) -> bool:
    llm = context.get("llm_classification", {})
    return _match_any(SECRET_PATTERNS, text) or bool(llm.get("secrets", False))


def detect_policy_violation(text: str, context: Dict) -> bool:
    llm = context.get("llm_classification", {})
    return _match_any(POLICY_VIOLATION, text) or bool(llm.get("policy_violation", False))


def detect_exfiltration(text: str, context: Dict) -> bool:
    labels = context.get("labels") or []
    if "CONFIDENTIAL" in labels and _match_any(EXFIL_PATTERNS, text):
        return True
    if _is_fictional_context(text) and not DIRECT_IMPERATIVE.search(text):
        return False

    matcher = SemanticMatcher.from_env()
    llm = context.get("llm_classification", {})
    return _match_any(EXFIL_PATTERNS, text) or matcher.match("exfiltration", text) or bool(llm.get("exfiltration", False))


def detect_goal_hijack(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    llm = context.get("llm_classification", {})

    score = _multi_stage_hijack_score(text)
    if _is_fictional_context(text) and score < 4:
        return False
    if _looks_like_benign_discussion(text) and not _has_direct_sensitive_exfil_request(text):
        return False

    if _has_direct_sensitive_exfil_request(text):
        return True
    if score >= 4:
        return True

    return _match_any(GOAL_HIJACK, text) or matcher.match("goal_hijack", text) or bool(llm.get("goal_hijack", False))


def detect_data_leakage(text: str, context: Dict) -> bool:
    matcher = SemanticMatcher.from_env()
    llm = context.get("llm_classification", {})
    return _match_any(DATA_LEAKAGE, text) or matcher.match("data_leakage", text) or bool(llm.get("data_leakage", False))
