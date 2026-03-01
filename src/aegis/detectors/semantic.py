from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import math

from ..config import settings

_MODEL = None
_MODEL_ERROR = None
_MATCHER = None


def _lazy_load_model(model_id: str):
    global _MODEL, _MODEL_ERROR
    if _MODEL is not None or _MODEL_ERROR is not None:
        return _MODEL
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception as exc:  # pragma: no cover
        _MODEL_ERROR = exc
        return None
    try:
        _MODEL = SentenceTransformer(model_id)
        return _MODEL
    except Exception as exc:  # pragma: no cover
        _MODEL_ERROR = exc
        return None


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


@dataclass
class SemanticMatcher:
    model_id: str
    enabled: bool
    thresholds: Dict[str, float]
    phrases: Dict[str, List[str]]
    _embeddings: Dict[str, List[List[float]]] | None = None

    def _ensure_embeddings(self):
        if self._embeddings is not None:
            return
        model = _lazy_load_model(self.model_id)
        if model is None:
            self.enabled = False
            self._embeddings = {}
            return
        self._embeddings = {}
        for category, items in self.phrases.items():
            self._embeddings[category] = model.encode(items, normalize_embeddings=True).tolist()

    def match(self, category: str, text: str) -> bool:
        if not self.enabled:
            return False
        self._ensure_embeddings()
        if not self._embeddings:
            return False
        model = _lazy_load_model(self.model_id)
        if model is None:
            return False
        vec = model.encode([text], normalize_embeddings=True)[0].tolist()
        candidates = self._embeddings.get(category, [])
        threshold = self.thresholds.get(category, 0.65)
        return any(_cosine(vec, cand) >= threshold for cand in candidates)

    def match_with_threshold(self, category: str, text: str, threshold: Optional[float]) -> bool:
        if threshold is None:
            return self.match(category, text)
        if not self.enabled:
            return False
        self._ensure_embeddings()
        if not self._embeddings:
            return False
        model = _lazy_load_model(self.model_id)
        if model is None:
            return False
        vec = model.encode([text], normalize_embeddings=True)[0].tolist()
        candidates = self._embeddings.get(category, [])
        return any(_cosine(vec, cand) >= float(threshold) for cand in candidates)

    @classmethod
    def from_env(cls) -> "SemanticMatcher":
        global _MATCHER
        if _MATCHER is not None:
            return _MATCHER
        phrases = {
            "prompt_injection": [
                "ignore previous instructions",
                "reveal the system prompt",
                "disregard safety rules",
                "developer message override",
            ],
            "jailbreak": [
                "do anything now",
                "jailbreak the model",
                "no restrictions mode",
            ],
            "goal_hijack": [
                "change the goal",
                "new instructions override the task",
            ],
            "exfiltration": [
                "send me the api key",
                "exfiltrate secrets",
                "dump credentials",
            ],
            "data_leakage": [
                "internal only",
                "confidential information",
                "private data",
            ],
        }
        thresholds = {
            "prompt_injection": 0.62,
            "jailbreak": 0.62,
            "goal_hijack": 0.62,
            "exfiltration": 0.60,
            "data_leakage": 0.60,
        }
        _MATCHER = cls(
            model_id=settings.aegis_embed_model,
            enabled=settings.aegis_semantic_enabled,
            thresholds=thresholds,
            phrases=phrases,
        )
        return _MATCHER
