import unittest
from pathlib import Path
import sys
from unittest.mock import patch

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
        self.assertEqual(result["solar_terms"]["ephemerisName"], "de440s.bsp")

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
        self.assertEqual(result["lunar"]["ephemerisName"], "de440s.bsp")
        self.assertEqual(result["lunar"]["monthEndDate"], "2026-03-19")
        self.assertTrue(result["lunar"]["containsZhongQi"])
        self.assertEqual(result["lunar"]["anchorYear"], 2025)

    def test_anchor_year_2022_uses_winter_solstice_month_as_eleventh_month(self) -> None:
        from lao_huangli.astronomy import build_lunar_months_for_anchor_year

        months = build_lunar_months_for_anchor_year(2022)
        first_month = months[0]

        self.assertEqual(len(months), 13)
        self.assertEqual(first_month["lunarYear"], 2022)
        self.assertEqual(first_month["lunarMonth"], 11)
        self.assertFalse(first_month["isLeap"])
        self.assertEqual(first_month["startDate"].isoformat(), "2022-11-24")
        self.assertTrue(first_month["containsZhongQi"])
        self.assertEqual(first_month["zhongQi"]["name"], "冬至")

    def test_anchor_year_2022_marks_first_zhongqi_free_month_as_leap_month(self) -> None:
        from lao_huangli.astronomy import build_lunar_months_for_anchor_year

        months = build_lunar_months_for_anchor_year(2022)
        leap_months = [month for month in months if month["isLeap"]]

        self.assertEqual(len(leap_months), 1)
        self.assertEqual(leap_months[0]["lunarYear"], 2023)
        self.assertEqual(leap_months[0]["lunarMonth"], 2)
        self.assertEqual(leap_months[0]["startDate"].isoformat(), "2023-03-22")
        self.assertFalse(leap_months[0]["containsZhongQi"])
        self.assertIsNone(leap_months[0]["zhongQi"])

    def test_lunar_year_2026_month_sequence_starts_on_2026_02_17(self) -> None:
        from lao_huangli.calendar_core import get_lunar_months_for_year

        months = get_lunar_months_for_year(2026)
        first_month = months[0]

        self.assertEqual(first_month["lunarYear"], 2026)
        self.assertEqual(first_month["lunarMonth"], 1)
        self.assertFalse(first_month["isLeap"])
        self.assertEqual(first_month["startDate"].isoformat(), "2026-02-17")
        self.assertEqual(first_month["zhongQi"]["name"], "雨水")

    def test_calendar_context_exposes_lunar_year_month_table(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")

        months = result["lunar"]["yearMonthTable"]
        self.assertEqual(len(months), 12)
        self.assertEqual(result["lunar"]["yearMonthCount"], 12)
        self.assertEqual(result["lunar"]["yearLeapMonth"], 0)
        self.assertEqual(result["lunar"]["currentMonthIndex"], 1)
        self.assertEqual(months[0]["lunarMonth"], 1)
        self.assertEqual(months[0]["startDate"], "2026-02-17")
        self.assertFalse(months[0]["isLeap"])
        self.assertEqual(months[0]["zhongQi"]["name"], "雨水")
        self.assertEqual(months[-1]["lunarMonth"], 12)

    def test_calendar_context_exposes_leap_month_in_year_table(self) -> None:
        result = run_calc(2023, 4, 1, 12, "--profile", "market-folk-v1")

        leap_months = [month for month in result["lunar"]["yearMonthTable"] if month["isLeap"]]
        self.assertEqual(result["lunar"]["yearMonthCount"], 13)
        self.assertEqual(result["lunar"]["yearLeapMonth"], 2)
        self.assertEqual(len(leap_months), 1)
        self.assertEqual(leap_months[0]["lunarMonth"], 2)
        self.assertEqual(leap_months[0]["startDate"], "2023-03-22")
        self.assertFalse(leap_months[0]["containsZhongQi"])

    def test_gregorian_to_lunar_only_falls_back_on_expected_value_error(self) -> None:
        from lao_huangli.calendar_core import gregorian_to_lunar

        with patch(
            "lao_huangli.calendar_core.get_lunar_month_context",
            side_effect=ValueError("context not found"),
        ), patch(
            "lao_huangli.calendar_core._gregorian_to_lunar_table",
            return_value=(2026, 1, 18, False),
        ):
            result = gregorian_to_lunar(2026, 3, 6)

        self.assertEqual(result[:4], (2026, 1, 18, False))
        self.assertEqual(result[4]["calculationMode"], "table-fallback")

    def test_gregorian_to_lunar_does_not_swallow_unexpected_errors(self) -> None:
        from lao_huangli.calendar_core import gregorian_to_lunar

        with patch(
            "lao_huangli.calendar_core.get_lunar_month_context",
            side_effect=RuntimeError("unexpected failure"),
        ):
            with self.assertRaises(RuntimeError):
                gregorian_to_lunar(2026, 3, 6)

    def test_1901_and_2099_stay_on_astronomical_path(self) -> None:
        early = run_calc(1901, 2, 19, 12, "--profile", "market-folk-v1")
        late = run_calc(2099, 12, 15, 12, "--profile", "market-folk-v1")

        self.assertEqual(early["lunar"]["calculationMode"], "astronomical-lunation-table")
        self.assertEqual(late["lunar"]["calculationMode"], "astronomical-lunation-table")
        self.assertEqual(early["lunar"]["ephemerisName"], "de440s.bsp")
        self.assertEqual(late["lunar"]["ephemerisName"], "de440s.bsp")


if __name__ == "__main__":
    unittest.main()
