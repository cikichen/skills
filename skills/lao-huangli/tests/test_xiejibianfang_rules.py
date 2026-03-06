import unittest

from test_huangli_calc import run_calc


class XiejibianfangRulesTests(unittest.TestCase):
    def test_xiejibianfang_profile_emits_jianchu_field(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("daily", result)
        self.assertIn("jianchu", result["daily"])

    def test_xiejibianfang_profile_emits_yellow_black_dao_and_yi_ji(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("yellowBlackDao", result["daily"])
        self.assertIn("decision", result)
        self.assertIn("yi", result["decision"])
        self.assertIn("ji", result["decision"])
        self.assertIn("sourceRefs", result["provenance"])
        self.assertTrue(result["provenance"]["sourceRefs"])


if __name__ == "__main__":
    unittest.main()
