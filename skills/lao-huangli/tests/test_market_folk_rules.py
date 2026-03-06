import unittest

from test_huangli_calc import run_calc


class MarketFolkRulesTests(unittest.TestCase):
    def test_market_profile_emits_full_calendar_fields(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
        self.assertIn("daily", result)
        self.assertNotEqual(result["daily"]["jianchu"], "待规则库补齐")
        self.assertNotEqual(result["daily"]["yellowBlackDao"], "待规则库补齐")
        self.assertIn("decision", result)
        self.assertTrue(result["decision"]["yi"] or result["decision"]["ji"])


if __name__ == "__main__":
    unittest.main()
