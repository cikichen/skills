import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RulesSchemaTests(unittest.TestCase):
    def test_profile_files_exist(self) -> None:
        profiles_dir = ROOT / "rules" / "profiles"
        for name in ["market-folk-v1.json", "xiejibianfang-v1.json", "bazi-v1.json"]:
            self.assertTrue((profiles_dir / name).exists(), msg=name)

    def test_profile_has_required_fields(self) -> None:
        path = ROOT / "rules" / "profiles" / "market-folk-v1.json"
        data = json.loads(path.read_text())

        for key in ["id", "label", "yearBoundary", "dayBoundary", "enabledRuleFamilies"]:
            self.assertIn(key, data)

    def test_shared_tables_exist(self) -> None:
        shared_dir = ROOT / "rules" / "shared"
        for name in ["actions.json", "directions.json"]:
            self.assertTrue((shared_dir / name).exists(), msg=name)


if __name__ == "__main__":
    unittest.main()
