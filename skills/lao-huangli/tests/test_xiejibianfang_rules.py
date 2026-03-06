import unittest

from test_huangli_calc import run_calc


class XiejibianfangRulesTests(unittest.TestCase):
    def test_xiejibianfang_profile_emits_jianchu_field(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("daily", result)
        self.assertIn("jianchu", result["daily"])


if __name__ == "__main__":
    unittest.main()
