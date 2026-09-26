from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from fintech_sim import generate_prototype, validate_prototype  # noqa: E402


class PrototypeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_prototype(PROJECT_ROOT)
        cls.result = validate_prototype(PROJECT_ROOT, write_report=True)

    def test_all_integrity_and_scenario_checks_pass(self) -> None:
        failures = [
            f"{check['check']}: {check['detail']}"
            for check in self.result["checks"]
            if not check["passed"]
        ]
        self.assertTrue(self.result["all_passed"], "\n".join(failures))

    def test_expected_prototype_scale(self) -> None:
        self.assertEqual(self.result["summary"]["transfers"], 10_000)
        self.assertEqual(self.result["summary"]["customers"], 3_500)
        self.assertEqual(self.result["summary"]["corridors"], 20)


if __name__ == "__main__":
    unittest.main()
