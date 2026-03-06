import unittest

from test_huangli_calc import run_calc


class BaziProfileTests(unittest.TestCase):
    def test_bazi_profile_defaults_to_core_without_yi_ji(self) -> None:
        result = run_calc(2026, 3, 2, 23, "--profile", "bazi-v1")

        self.assertFalse(result["capabilities"]["yiJi"])
        self.assertFalse(result["provenance"]["isHybrid"])
        self.assertEqual(result["meta"]["profileId"], "bazi-v1")

    def test_bazi_overlay_enables_hybrid_almanac_output(self) -> None:
        result = run_calc(
            2026,
            3,
            2,
            23,
            "--profile",
            "bazi-v1",
            "--overlay-ruleset",
            "xiejibianfang-v1",
        )

        self.assertTrue(result["capabilities"]["yiJi"])
        self.assertTrue(result["provenance"]["isHybrid"])
        self.assertEqual(result["provenance"]["ruleLayer"], "xiejibianfang-v1")


if __name__ == "__main__":
    unittest.main()
