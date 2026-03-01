import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aegis.policies.engine import PolicyEngine  # noqa: E402
from aegis.detectors.registry import DetectorRegistry  # noqa: E402


class FailClosedTests(unittest.TestCase):
    def setUp(self):
        self.detectors = DetectorRegistry.default()
        self.context = {"labels": [], "metadata": {}}

    def test_unknown_stage_blocks_when_fail_closed(self):
        engine = PolicyEngine(policies=[], fail_closed=True)
        decision = engine.evaluate(
            text="hello",
            stage="unknown_stage",
            detectors=self.detectors,
            context=self.context,
        )
        self.assertTrue(decision.blocked)
        self.assertIn("Unknown policy stage", decision.message or "")

    def test_policy_match_error_blocks_when_fail_closed(self):
        engine = PolicyEngine(
            policies=[
                {
                    "id": "bad_regex",
                    "stage": "prellm",
                    "match": {"any": [{"regex": "["}]},  # invalid regex
                    "action": "warn",
                }
            ],
            fail_closed=True,
        )
        decision = engine.evaluate(
            text="anything",
            stage="prellm",
            detectors=self.detectors,
            context=self.context,
        )
        self.assertTrue(decision.blocked)
        self.assertIn("Policy evaluation error", decision.message or "")


if __name__ == "__main__":
    unittest.main()
