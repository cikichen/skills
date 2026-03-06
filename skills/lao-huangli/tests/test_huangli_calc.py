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


class HuangliCalcTests(unittest.TestCase):
    def test_current_solar_term_uses_previous_month_term_before_first_jie(self) -> None:
        result = run_calc(2026, 3, 2, 12)

        self.assertEqual(result["solar_terms"]["current"], "雨水")
        self.assertEqual(result["solar_terms"]["next"], "惊蛰")

    def test_market_profile_sets_expected_boundaries(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")

        self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
        self.assertEqual(result["meta"]["yearBoundary"], "spring-festival")
        self.assertEqual(result["meta"]["dayBoundary"], "00:00")

    def test_bazi_day_boundary_keeps_input_timestamp_but_advances_logical_date(self) -> None:
        result = run_calc(2026, 3, 2, 23, "--mode", "bazi")

        self.assertEqual(result["date"]["input_iso"], "2026-03-02 23:00")
        self.assertEqual(result["date"]["effective_iso"], "2026-03-02 23:00")
        self.assertEqual(result["date"]["logical_date_iso"], "2026-03-03")
        self.assertEqual(result["ganzhi"]["day"], "丙午")


if __name__ == "__main__":
    unittest.main()
