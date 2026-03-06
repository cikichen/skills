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
        self.assertIn("decision", result)
        self.assertIn("yi", result["decision"])
        self.assertIn("ji", result["decision"])
        self.assertIn("sourceRefs", result["provenance"])
        self.assertTrue(result["provenance"]["sourceRefs"])

    def test_xiejibianfang_decision_emits_explanations_and_source_trace(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertTrue(result["decision"]["explanations"])
        self.assertTrue(result["provenance"]["sourceRefs"])


if __name__ == "__main__":
    unittest.main()
