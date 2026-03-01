import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aegis.prellm.network import evaluate_urls  # noqa: E402


class NetworkFirewallTests(unittest.TestCase):
    def test_blocks_localtest_me(self):
        decision = evaluate_urls(["http://localtest.me/admin"], allowlist=[], denylist=[])
        self.assertTrue(decision.blocked)
        self.assertIn("rebinding", (decision.message or "").lower())

    def test_blocks_nip_io(self):
        decision = evaluate_urls(["http://127.0.0.1.nip.io/admin"], allowlist=[], denylist=[])
        self.assertTrue(decision.blocked)


if __name__ == "__main__":
    unittest.main()
