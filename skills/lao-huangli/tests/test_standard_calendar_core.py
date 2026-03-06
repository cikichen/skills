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

        self.assertEqual(result["solar_terms"]["precision"], "day-approximate")
        self.assertEqual(result["solar_terms"]["calculationMode"], "table-window")


if __name__ == "__main__":
    unittest.main()
