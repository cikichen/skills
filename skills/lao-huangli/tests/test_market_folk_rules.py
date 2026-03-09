import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_huangli_calc import run_calc


class MarketFolkRulesTests(unittest.TestCase):
    def test_market_profile_emits_full_calendar_fields(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
        self.assertIn("daily", result)
        self.assertNotEqual(result["daily"]["jianchu"], "待规则库补齐")
        self.assertNotEqual(result["daily"]["yellowBlackDao"], "待规则库补齐")
        self.assertEqual(result["daily"]["dutyGod"], "勾陈")
        self.assertIn("勾陈", result["daily"]["badStars"])
        self.assertIn("decision", result)
        self.assertTrue(result["decision"]["yi"] or result["decision"]["ji"])

    def test_market_profile_emits_rule_facts_not_placeholders(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["daily"]["chongsha"], "冲鸡煞西")
        self.assertEqual(result["daily"]["taishen"], "占大门外正西")
        self.assertEqual(
            result["daily"]["pengzu"],
            "己不破券，二主并亡；卯不穿井，泉水不香",
        )

    def test_market_profile_emits_direction_fields(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["daily"]["caiShen"], "正北")
        self.assertEqual(result["daily"]["xiShen"], "东北")
        self.assertEqual(result["daily"]["fuShen"], "正北")
        self.assertEqual(result["provenance"]["ruleSourceLevel"], "L2-derived-documented")

    def test_market_profile_expands_common_jianchu_yi_ji(self) -> None:
        result = run_calc(2026, 3, 3, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["daily"]["jianchu"], "开")
        self.assertIn("开市", result["decision"]["yi"])
        self.assertIn("立券交易", result["decision"]["yi"])
        self.assertIn("安葬", result["decision"]["ji"])
        self.assertIn("破土", result["decision"]["ji"])

    def test_market_profile_emits_hour_luck(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        hour_slots = {item["name"]: item for item in result["hour_slots"]}
        self.assertEqual(hour_slots["子"]["tianShen"], "司命")
        self.assertEqual(hour_slots["子"]["luck"], "吉")
        self.assertEqual(hour_slots["丑"]["tianShen"], "勾陈")
        self.assertEqual(hour_slots["丑"]["luck"], "凶")

    def test_market_profile_empty_star_side_is_still_marked_implemented(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["daily"]["badStars"], [])
        self.assertEqual(
            result["provenance"]["fieldSources"]["badStars"]["status"],
            "implemented",
        )


if __name__ == "__main__":
    unittest.main()
