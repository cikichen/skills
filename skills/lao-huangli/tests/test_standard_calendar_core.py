import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_huangli_calc import run_calc


class StandardCalendarCoreTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
