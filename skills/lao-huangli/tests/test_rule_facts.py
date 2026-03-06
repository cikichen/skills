import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_huangli_calc import run_calc


class RuleFactTests(unittest.TestCase):
    def test_xiejibianfang_daily_fact_fields_exist(self) -> None:
        result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")

        self.assertIn("chongsha", result["daily"])
        self.assertIn("taishen", result["daily"])
        self.assertIn("pengzu", result["daily"])
        self.assertEqual(result["daily"]["chongsha"], "冲鸡煞西")
        self.assertEqual(result["daily"]["taishen"], "占大门外正西")
        self.assertEqual(result["daily"]["pengzu"], "己不破券，二主并亡；卯不穿井，泉水不香")

    def test_xiejibianfang_daily_fact_fields_match_second_golden_case(self) -> None:
        result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")

        self.assertEqual(result["daily"]["chongsha"], "冲蛇煞西")
        self.assertEqual(result["daily"]["taishen"], "碓磨床外西南")
        self.assertEqual(result["daily"]["pengzu"], "乙不栽植，千株不长；亥不嫁娶，不利新郎")


if __name__ == "__main__":
    unittest.main()
