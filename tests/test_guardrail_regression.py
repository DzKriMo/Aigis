import os
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aegis.policies.loader import load_policies  # noqa: E402
from aegis.policies.engine import PolicyEngine  # noqa: E402
from aegis.detectors.registry import DetectorRegistry  # noqa: E402
from aegis.runtime.runner import GuardedRuntime  # noqa: E402
from aegis.storage.store import InMemoryStore  # noqa: E402


class GuardrailRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("AEGIS_LLM_ENABLED", "false")
        cls.detectors = DetectorRegistry.default()
        cls.engine = PolicyEngine(load_policies(), fail_closed=True)
        cls.runtime = GuardedRuntime(store=InMemoryStore())
        cls.session_id = "regression-session"
        cls.runtime.store.create_session(cls.session_id)
        corpus_path = ROOT / "tests" / "data" / "guardrail_regression_cases.yaml"
        with open(corpus_path, "r", encoding="utf-8") as f:
            cls.cases = (yaml.safe_load(f) or {}).get("cases", [])

    def test_attack_corpus(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                kind = case["kind"]
                if kind == "message":
                    result = self.runtime.handle_user_message(
                        session_id=self.session_id,
                        content=case["content"],
                        metadata={},
                    )
                    for action in case.get("expected_actions", []):
                        self.assertIn(action, result.actions)
                elif kind == "policy_eval":
                    decision = self.engine.evaluate(
                        text=case["content"],
                        stage=case["stage"],
                        detectors=self.detectors,
                        context={"labels": [], "metadata": {}},
                    )
                    expected = case.get("expected", {})
                    if "blocked" in expected:
                        self.assertEqual(expected["blocked"], decision.blocked)
                    if "redact" in expected:
                        self.assertEqual(expected["redact"], decision.redact)
                elif kind == "tool":
                    tool_result = self.runtime.handle_tool_call(
                        session_id=self.session_id,
                        tool_name=case["tool_name"],
                        payload=case.get("payload", {}),
                        environment=case.get("environment"),
                        allowlist=[],
                        denylist=[],
                        filesystem_root=None,
                    )
                    expected = case.get("expected", {})
                    if "allowed" in expected:
                        self.assertEqual(expected["allowed"], tool_result["allowed"])
                    if expected.get("has_approval_hash"):
                        self.assertTrue(bool(tool_result.get("approval_hash")))
                    if "message_contains" in expected:
                        msg = (tool_result.get("message") or "").lower()
                        self.assertIn(expected["message_contains"].lower(), msg)
                else:
                    self.fail(f"Unsupported case kind: {kind}")


if __name__ == "__main__":
    unittest.main()
