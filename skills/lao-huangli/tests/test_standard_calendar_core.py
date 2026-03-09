import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from test_huangli_calc import run_calc


class StandardCalendarCoreTests(unittest.TestCase):
    def test_calendar_core_module_exposes_build_context(self) -> None:
        from lao_huangli.calendar_core import CalendarCoreInput, build_calendar_context

        result = build_calendar_context(
            CalendarCoreInput(
                year=2026,
                month=3,
                day=6,
                hour=12,
                year_boundary="spring-festival",
                day_boundary="00:00",
            )
        )

        self.assertIn("date", result)
        self.assertIn("lunar", result)
        self.assertIn("ganzhi", result)
        self.assertIn("solar_terms", result)

    def test_calendar_core_exposes_standard_reference_constants(self) -> None:
        from lao_huangli.calendar_core import (
            DAY_GANZHI_REFERENCE_DATE,
            YEAR_GANZHI_REFERENCE_YEAR,
        )

        self.assertEqual(DAY_GANZHI_REFERENCE_DATE, (1949, 10, 1))
        self.assertEqual(YEAR_GANZHI_REFERENCE_YEAR, 1984)

    def test_1949_10_01_matches_standard_day_reference(self) -> None:
        result = run_calc(1949, 10, 1, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["ganzhi"]["day"], "甲子")

    def test_1984_02_02_matches_standard_year_reference(self) -> None:
        result = run_calc(1984, 2, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["lunar"]["text"], "1984年1月1日")
        self.assertEqual(result["ganzhi"]["year"], "甲子")

    def test_2026_03_06_matches_official_calendar_sample(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["lunar"]["text"], "2026年1月18日")
        self.assertEqual(result["ganzhi"]["month"], "辛卯")
        self.assertEqual(result["ganzhi"]["day"], "己卯")
        self.assertEqual(result["solar_terms"]["current"], "惊蛰")

    def test_solar_terms_emit_precision_metadata(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["solar_terms"]["precision"], "astronomical")
        self.assertEqual(result["solar_terms"]["calculationMode"], "skyfield-jpl")

    def test_solar_terms_include_crossing_timestamps(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertIn("currentAt", result["solar_terms"])
        self.assertIn("nextAt", result["solar_terms"])

    def test_solar_terms_change_across_same_day_crossing_hour(self) -> None:
        before = run_calc(2026, 3, 5, 21, "--profile", "market-folk-v1")
        after = run_calc(2026, 3, 5, 22, "--profile", "market-folk-v1")

        self.assertEqual(before["solar_terms"]["current"], "雨水")
        self.assertEqual(after["solar_terms"]["current"], "惊蛰")

    def test_solar_terms_expose_jie_qi_navigation_like_table(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertIn("table", result["solar_terms"])
        self.assertIn("currentJie", result["solar_terms"])
        self.assertIn("currentQi", result["solar_terms"])
        self.assertIn("nextJie", result["solar_terms"])
        self.assertIn("nextQi", result["solar_terms"])
        self.assertEqual(result["solar_terms"]["currentJie"]["name"], "惊蛰")
        self.assertEqual(result["solar_terms"]["currentQi"]["name"], "雨水")
        self.assertEqual(result["solar_terms"]["nextQi"]["name"], "春分")

    def test_lunar_exposes_month_start_and_calculation_mode(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["lunar"]["monthStartDate"], "2026-02-17")
        self.assertEqual(result["lunar"]["calculationMode"], "astronomical-lunation-table")
        self.assertEqual(result["lunar"]["leapMonth"], 0)


if __name__ == "__main__":
    unittest.main()
