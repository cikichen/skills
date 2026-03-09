import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lao_huangli.calendar_core import CalendarCoreInput, build_calendar_context
from test_huangli_calc import run_calc


class XiejibianfangRulesTests(unittest.TestCase):
    def test_rule_engine_exposes_unified_rule_layer_entry(self) -> None:
        from lao_huangli.rule_engine import evaluate_rule_layer

        calendar_context = build_calendar_context(
            CalendarCoreInput(
                year=2026,
                month=3,
                day=6,
                hour=12,
                year_boundary="spring-festival",
                day_boundary="00:00",
            )
        )

        result = evaluate_rule_layer(
            profile_id="xiejibianfang-v1",
            overlay_ruleset=None,
            calendar_context=calendar_context,
        )

        self.assertIn("daily", result)
        self.assertIn("decision", result)
        self.assertIn("provenance", result)

    def test_xiejibianfang_profile_emits_jianchu_field(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("daily", result)
        self.assertIn("jianchu", result["daily"])

    def test_xiejibianfang_profile_emits_yellow_black_dao_and_yi_ji(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("yellowBlackDao", result["daily"])
        self.assertIn("dutyGod", result["daily"])
        self.assertIn("goodStars", result["daily"])
        self.assertIn("badStars", result["daily"])
        self.assertIn("decision", result)
        self.assertIn("yi", result["decision"])
        self.assertIn("ji", result["decision"])
        self.assertIn("sourceRefs", result["provenance"])
        self.assertTrue(result["provenance"]["sourceRefs"])

    def test_xiejibianfang_decision_emits_explanations_and_source_trace(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertTrue(result["decision"]["explanations"])
        self.assertTrue(result["provenance"]["sourceRefs"])

    def test_xiejibianfang_jianchu_rules_expand_yi_items(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("上官赴任", result["decision"]["yi"])
        self.assertTrue(
            any("建日" in explanation for explanation in result["decision"]["explanations"])
        )

    def test_xiejibianfang_shou_day_adds_na_cai(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("纳财", result["decision"]["yi"])
        self.assertNotIn("修仓库", result["decision"]["yi"])
        self.assertNotIn("栽种", result["decision"]["yi"])
        self.assertNotIn("牧养", result["decision"]["yi"])

    def test_xiejibianfang_chu_day_only_keeps_unconditional_items(self) -> None:
        result = run_calc(2026, 3, 7, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["daily"]["jianchu"], "除")
        self.assertIn("解除", result["decision"]["yi"])
        self.assertNotIn("出师", result["decision"]["yi"])
        self.assertNotIn("安抚边境", result["decision"]["yi"])

    def test_xiejibianfang_ding_day_only_keeps_guandai(self) -> None:
        result = run_calc(2026, 3, 10, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["daily"]["jianchu"], "定")
        self.assertIn("冠带", result["decision"]["yi"])
        self.assertNotIn("计策", result["decision"]["yi"])
        self.assertNotIn("运谋", result["decision"]["yi"])

    def test_xiejibianfang_kai_day_adds_kaishi_and_burial_taboos(self) -> None:
        result = run_calc(2026, 3, 3, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["daily"]["jianchu"], "开")
        self.assertIn("开市", result["decision"]["yi"])
        self.assertIn("立券交易", result["decision"]["yi"])
        self.assertIn("破土", result["decision"]["ji"])
        self.assertIn("安葬", result["decision"]["ji"])

    def test_xiejibianfang_bi_day_adds_tifang_and_many_taboos(self) -> None:
        result = run_calc(2026, 3, 4, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["daily"]["jianchu"], "闭")
        self.assertIn("补垣塞穴", result["decision"]["yi"])
        self.assertIn("筑堤防", result["decision"]["yi"])
        self.assertNotIn("筑堤防", result["decision"]["ji"])
        self.assertNotIn("修仓库", result["decision"]["ji"])
        self.assertNotIn("破土", result["decision"]["ji"])

    def test_xiejibianfang_emits_field_level_sources(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("fieldSources", result["provenance"])
        self.assertEqual(
            result["provenance"]["fieldSources"]["dutyGod"]["sourceLevel"],
            "L1-primary",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["goodStars"]["sourceLevel"],
            "L1-primary",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["badStars"]["sourceLevel"],
            "L1-primary",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["chongsha"]["sourceLevel"],
            "L2-derived-documented",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["pengzu"]["sourceLevel"],
            "L1-primary",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["taishen"]["sourceLevel"],
            "L2-derived-documented",
        )
        self.assertEqual(
            result["provenance"]["fieldSources"]["taishen"]["status"],
            "implemented",
        )

    def test_xiejibianfang_exposes_duty_god_and_star_lists(self) -> None:
        good_day = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")
        bad_day = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(good_day["daily"]["dutyGod"], "明堂")
        self.assertIn("明堂", good_day["daily"]["goodStars"])
        self.assertEqual(good_day["daily"]["badStars"], [])
        self.assertEqual(bad_day["daily"]["dutyGod"], "勾陈")
        self.assertEqual(bad_day["daily"]["goodStars"], [])
        self.assertIn("勾陈", bad_day["daily"]["badStars"])
        self.assertTrue(good_day["capabilities"]["dutyGod"])


if __name__ == "__main__":
    unittest.main()
