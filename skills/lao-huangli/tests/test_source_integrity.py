import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SourceIntegrityTests(unittest.TestCase):
    def test_xiejibianfang_rule_family_files_exist(self) -> None:
        rules_dir = ROOT / "rules" / "xiejibianfang-v1"
        for name in [
            "duty-gods.json",
            "good-stars.json",
            "bad-stars.json",
            "chongsha.json",
            "taishen.json",
            "pengzu.json",
            "sources.json",
        ]:
            self.assertTrue((rules_dir / name).exists(), msg=name)

    def test_all_rules_have_source_fields(self) -> None:
        rules_dir = ROOT / "rules"
        rule_files = [
            path
            for path in rules_dir.rglob("*.json")
            if "profiles" not in path.parts and "shared" not in path.parts
        ]

        self.assertTrue(rule_files, msg="no rule files found")

        for path in rule_files:
            data = json.loads(path.read_text())
            self.assertIsInstance(data, list, msg=path.name)
            for item in data:
                self.assertIn("sourceLevel", item, msg=path.name)
                self.assertIn("sourceRef", item, msg=path.name)


if __name__ == "__main__":
    unittest.main()
