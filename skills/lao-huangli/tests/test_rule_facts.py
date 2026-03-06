import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_huangli_calc import run_calc


class RuleFactTests(unittest.TestCase):
    def test_xiejibianfang_daily_fact_fields_exist(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("chongsha", result["daily"])
        self.assertIn("taishen", result["daily"])
        self.assertIn("pengzu", result["daily"])
        self.assertEqual(result["daily"]["chongsha"], "待规则库补齐")
        self.assertEqual(result["daily"]["taishen"], "待规则库补齐")
        self.assertEqual(result["daily"]["pengzu"], "待规则库补齐")


if __name__ == "__main__":
    unittest.main()
