import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aegis.config import settings  # noqa: E402
from aegis.security.startup import validate_startup_settings  # noqa: E402


class ProductionHardeningTests(unittest.TestCase):
    def setUp(self):
        self.original = {
            "aegis_env": settings.aegis_env,
            "aegis_api_key": settings.aegis_api_key,
            "jwt_secret": settings.jwt_secret,
            "aegis_fail_closed": settings.aegis_fail_closed,
            "aegis_cors_origins": list(settings.aegis_cors_origins),
            "aegis_rate_limit_backend": settings.aegis_rate_limit_backend,
        }

    def tearDown(self):
        for key, value in self.original.items():
            setattr(settings, key, value)

    def test_prod_rejects_insecure_defaults(self):
        settings.aegis_env = "prod"
        settings.aegis_api_key = "changeme"
        settings.jwt_secret = "dev-secret-change"
        settings.aegis_fail_closed = False
        settings.aegis_cors_origins = ["*"]
        settings.aegis_rate_limit_backend = "memory"
        with self.assertRaises(RuntimeError):
            validate_startup_settings()

    def test_prod_accepts_hardened_configuration(self):
        settings.aegis_env = "production"
        settings.aegis_api_key = "replace-with-real-key"
        settings.jwt_secret = "long-enough-production-secret"
        settings.aegis_fail_closed = True
        settings.aegis_cors_origins = ["https://aegis.example.com"]
        settings.aegis_rate_limit_backend = "sqlite"
        validate_startup_settings()


if __name__ == "__main__":
    unittest.main()
