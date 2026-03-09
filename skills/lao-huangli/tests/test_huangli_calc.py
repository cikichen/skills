import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "huangli_calc.py"


def run_calc(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args), "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def run_calc_text(*args: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args), "--format", "calendar"],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


class HuangliCalcTests(unittest.TestCase):
    def test_golden_case_2026_03_02_market(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["lunar"]["text"], "2026年1月14日")
        self.assertEqual(result["ganzhi"]["day"], "乙亥")
        self.assertEqual(result["solar_terms"]["current"], "雨水")

    def test_current_solar_term_uses_previous_month_term_before_first_jie(self) -> None:
        result = run_calc(2026, 3, 2, 12)

        self.assertEqual(result["solar_terms"]["current"], "雨水")
        self.assertEqual(result["solar_terms"]["next"], "惊蛰")

    def test_market_profile_sets_expected_boundaries(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
        self.assertEqual(result["meta"]["yearBoundary"], "spring-festival")
        self.assertEqual(result["meta"]["dayBoundary"], "00:00")

    def test_default_profile_is_market_folk(self) -> None:
        result = run_calc(2026, 3, 2, 12)

        self.assertEqual(result["meta"]["profileId"], "market-folk-v1")

    def test_bazi_day_boundary_keeps_input_timestamp_but_advances_logical_date(self) -> None:
        result = run_calc(2026, 3, 2, 23, "--mode", "bazi")

        self.assertEqual(result["date"]["input_iso"], "2026-03-02 23:00")
        self.assertEqual(result["date"]["effective_iso"], "2026-03-02 23:00")
        self.assertEqual(result["date"]["logical_date_iso"], "2026-03-03")
        self.assertEqual(result["ganzhi"]["day"], "丙子")

    def test_golden_case_2026_03_06_matches_official_almanac(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["lunar"]["text"], "2026年1月18日")
        self.assertEqual(result["ganzhi"]["month"], "辛卯")
        self.assertEqual(result["ganzhi"]["day"], "己卯")
        self.assertEqual(result["solar_terms"]["current"], "惊蛰")
        self.assertEqual(result["daily"]["jianchu"], "建")
        self.assertEqual(result["daily"]["yellowBlackDao"], "明堂")

    def test_calendar_format_renders_real_rule_facts(self) -> None:
        text = run_calc_text(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("值神：明堂", text)
        self.assertIn("吉神宜趋：明堂", text)
        self.assertIn("冲鸡煞西", text)
        self.assertIn("占大门外正西", text)
        self.assertIn("己不破券，二主并亡", text)

    def test_market_calendar_format_renders_directions_and_short_note(self) -> None:
        text = run_calc_text(2026, 3, 6, 12)

        self.assertIn("财神：正北", text)
        self.assertIn("喜神：东北", text)
        self.assertIn("福神：正北", text)
        self.assertNotIn("overlayRuleset=", text)
        self.assertNotIn("effectiveAt=", text)


if __name__ == "__main__":
    unittest.main()
