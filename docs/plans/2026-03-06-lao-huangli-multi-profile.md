# Lao Huangli Multi-Profile Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `skills/lao-huangli` 建立可追溯的多 profile/ruleset 结构，第一版支持 `market-folk-v1`、`xiejibianfang-v1`、`bazi-v1`。

**Architecture:** 保留单一历法核心，把边界差异放在 `profile`，把规则差异放在 `ruleset`，再通过统一 rule engine 和冲突裁决器输出结果。所有规则文件必须带来源等级与出处引用，避免编造。

**Tech Stack:** Python 3 标准库、JSON 规则文件、`unittest`

---

### Task 1: 建立 rules/profile 基础目录与 schema 测试

**Files:**
- Create: `skills/lao-huangli/rules/profiles/market-folk-v1.json`
- Create: `skills/lao-huangli/rules/profiles/xiejibianfang-v1.json`
- Create: `skills/lao-huangli/rules/profiles/bazi-v1.json`
- Create: `skills/lao-huangli/rules/shared/actions.json`
- Create: `skills/lao-huangli/rules/shared/directions.json`
- Create: `skills/lao-huangli/tests/test_rules_schema.py`

**Step 1: 写失败测试，约束 profile 文件和最小共享表存在**

```python
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RulesSchemaTests(unittest.TestCase):
    def test_profile_files_exist(self):
        for name in ["market-folk-v1.json", "xiejibianfang-v1.json", "bazi-v1.json"]:
            self.assertTrue((ROOT / "rules" / "profiles" / name).exists())

    def test_profile_has_required_fields(self):
        data = json.loads((ROOT / "rules" / "profiles" / "market-folk-v1.json").read_text())
        for key in ["id", "label", "yearBoundary", "dayBoundary", "enabledRuleFamilies"]:
            self.assertIn(key, data)
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，提示缺少 `rules/profiles/*.json`

**Step 3: 用最小实现创建 profile 与 shared 文件**

```json
{
  "id": "market-folk-v1",
  "label": "市售挂历版",
  "yearBoundary": "spring-festival",
  "dayBoundary": "00:00",
  "enabledRuleFamilies": []
}
```

**Step 4: 重新运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: 新增 schema 测试 PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/rules/profiles skills/lao-huangli/rules/shared skills/lao-huangli/tests/test_rules_schema.py
git commit -m "feat: add lao-huangli profile scaffolding"
```

### Task 2: 重构脚本参数，从 mode 迁移到 profile

**Files:**
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_huangli_calc.py`

**Step 1: 写失败测试，要求脚本接受 `--profile`**

```python
def test_market_profile_sets_expected_boundaries(self) -> None:
    result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")
    self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
    self.assertEqual(result["meta"]["yearBoundary"], "spring-festival")
    self.assertEqual(result["meta"]["dayBoundary"], "00:00")
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，提示 `unrecognized arguments: --profile`

**Step 3: 最小实现**

```python
parser.add_argument("--profile", default="market-folk-v1")

profile_cfg = load_profile(args.profile)
logical_dt = _apply_day_boundary(input_dt, profile_cfg["dayBoundary"])
```

并在输出里加入：

```python
"meta": {
    "profileId": profile_cfg["id"],
    "profileLabel": profile_cfg["label"],
    ...
}
```

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: `test_huangli_calc.py` 全绿

**Step 5: Commit**

```bash
git add skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_huangli_calc.py
git commit -m "refactor: switch lao-huangli to profile-based boundaries"
```

### Task 3: 增加来源完整性测试

**Files:**
- Create: `skills/lao-huangli/tests/test_source_integrity.py`

**Step 1: 写失败测试，要求规则文件必须包含来源字段**

```python
class SourceIntegrityTests(unittest.TestCase):
    def test_all_rules_have_source_fields(self):
        rules_dir = ROOT / "rules"
        for path in rules_dir.rglob("*.json"):
            if "profiles" in path.parts or "shared" in path.parts:
                continue
            data = json.loads(path.read_text())
            for item in data:
                self.assertIn("sourceLevel", item)
                self.assertIn("sourceRef", item)
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，因为规则文件尚不存在或缺来源

**Step 3: 暂时创建最小规则集占位，全部带来源字段**

```json
[
  {
    "id": "placeholder",
    "sourceLevel": "L1-primary",
    "sourceRef": [{"work": "钦定协纪辨方书", "location": "卷四", "url": "https://zh.wikisource.org/..."}]
  }
]
```

**Step 4: 重新运行测试**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: source integrity 测试 PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/tests/test_source_integrity.py skills/lao-huangli/rules
git commit -m "test: enforce rule source metadata"
```

### Task 4: 实现 xiejibianfang-v1 的建除十二神最小闭环

**Files:**
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/jianchu.json`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`

**Step 1: 写失败测试**

```python
def test_xiejibianfang_profile_emits_jianchu_field(self):
    result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")
    self.assertIn("daily", result)
    self.assertIn("jianchu", result["daily"])
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，`daily.jianchu` 缺失

**Step 3: 最小实现**

```python
def compute_jianchu(profile_id: str, month_branch: str, day_branch: str) -> str:
    ...

daily = {"jianchu": compute_jianchu(...)}
```

规则文件记录：

```json
{
  "id": "xjbfs-jianchu-cycle",
  "sourceLevel": "L1-primary",
  "sourceRef": [{"work": "钦定协纪辨方书", "location": "卷四", "url": "..."}]
}
```

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/rules/xiejibianfang-v1/jianchu.json skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_xiejibianfang_rules.py
git commit -m "feat: add xiejibianfang jianchu rules"
```

### Task 5: 实现 xiejibianfang-v1 的黄黑道十二神与最小宜忌

**Files:**
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/yellow-black-dao.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/yi-ji-rules.json`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`

**Step 1: 写失败测试**

```python
def test_xiejibianfang_profile_emits_yellow_black_dao_and_yi_ji(self):
    result = run_calc(2026, 3, 2, 12, "--profile", "xiejibianfang-v1")
    self.assertIn("yellowBlackDao", result["daily"])
    self.assertIn("yi", result["decision"])
    self.assertIn("ji", result["decision"])
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，缺少 `yellowBlackDao` 和 `decision`

**Step 3: 最小实现**

```python
rule_context = {
    "jianchu": daily["jianchu"],
    "yellowBlackDao": compute_yellow_black_dao(...),
}
decision = evaluate_rules(rule_context, ruleset="xiejibianfang-v1")
```

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/rules/xiejibianfang-v1 skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_xiejibianfang_rules.py
git commit -m "feat: add xiejibianfang yellow-black-dao and yi-ji rules"
```

### Task 6: 实现 market-folk-v1 规则集

**Files:**
- Create: `skills/lao-huangli/rules/market-folk-v1/jianchu.json`
- Create: `skills/lao-huangli/rules/market-folk-v1/yellow-black-dao.json`
- Create: `skills/lao-huangli/rules/market-folk-v1/yi-ji-rules.json`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_market_folk_rules.py`

**Step 1: 写失败测试**

```python
def test_market_profile_emits_full_calendar_fields(self):
    result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")
    self.assertEqual(result["meta"]["profileId"], "market-folk-v1")
    self.assertIn("daily", result)
    self.assertIn("decision", result)
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL

**Step 3: 最小实现**

```python
if profile_id == "market-folk-v1":
    ruleset_id = "market-folk-v1"
```

并在规则文件中标注：

```json
{
  "sourceLevel": "L3-market-observed",
  "interpretationType": "market-observed"
}
```

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/rules/market-folk-v1 skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_market_folk_rules.py
git commit -m "feat: add market folk ruleset"
```

### Task 7: 实现 bazi-v1 的 core 与 overlay

**Files:**
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Create: `skills/lao-huangli/rules/bazi-v1/overlay-defaults.json`
- Test: `skills/lao-huangli/tests/test_bazi_profile.py`

**Step 1: 写失败测试**

```python
def test_bazi_profile_defaults_to_core_without_yi_ji(self):
    result = run_calc(2026, 3, 2, 23, "--profile", "bazi-v1")
    self.assertFalse(result["capabilities"]["yiJi"])

def test_bazi_overlay_enables_hybrid_almanac_output(self):
    result = run_calc(2026, 3, 2, 23, "--profile", "bazi-v1", "--overlay-ruleset", "xiejibianfang-v1")
    self.assertTrue(result["capabilities"]["yiJi"])
    self.assertTrue(result["provenance"]["isHybrid"])
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL

**Step 3: 最小实现**

```python
overlay_ruleset = args.overlay_ruleset
is_hybrid = profile_id == "bazi-v1" and overlay_ruleset is not None
```

并控制输出：

```python
if profile_id == "bazi-v1" and not overlay_ruleset:
    decision = {"yi": [], "ji": [], "warnings": []}
    capabilities["yiJi"] = False
```

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/rules/bazi-v1/overlay-defaults.json skills/lao-huangli/tests/test_bazi_profile.py
git commit -m "feat: add bazi core and overlay support"
```

### Task 8: 更新技能文档与验证说明

**Files:**
- Modify: `skills/lao-huangli/SKILL.md`
- Modify: `docs/skills/lao-huangli.md`
- Modify: `docs/skills/lao-huangli_CN.md`

**Step 1: 写失败检查清单**

```text
- 文档仍只写 mode，不写 profile
- 文档未说明 sourceLevel/sourceRef 约束
- 文档未说明 bazi overlay 是 hybrid
```

**Step 2: 运行人工检查确认需要更新**

Run: `rg -n "mode|market|bazi|rulesetVersion|source" skills/lao-huangli/SKILL.md docs/skills/lao-huangli.md docs/skills/lao-huangli_CN.md`
Expected: 看到旧描述仍以 `mode` 为中心

**Step 3: 最小实现**

更新文档内容，加入：

- 三个 profile 说明
- 规则来源等级
- `bazi-core` / `overlay`
- 验证命令

**Step 4: 运行检查**

Run: `rg -n "profile|sourceLevel|isHybrid|overlayRuleset" skills/lao-huangli/SKILL.md docs/skills/lao-huangli.md docs/skills/lao-huangli_CN.md`
Expected: 命中文档新增字段说明

**Step 5: Commit**

```bash
git add skills/lao-huangli/SKILL.md docs/skills/lao-huangli.md docs/skills/lao-huangli_CN.md
git commit -m "docs: document lao-huangli profiles and rule provenance"
```

### Task 9: 全量验证

**Files:**
- Modify: `skills/lao-huangli/tests/test_huangli_calc.py`
- Modify: `skills/lao-huangli/tests/test_rules_schema.py`
- Modify: `skills/lao-huangli/tests/test_source_integrity.py`
- Modify: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`
- Modify: `skills/lao-huangli/tests/test_market_folk_rules.py`
- Modify: `skills/lao-huangli/tests/test_bazi_profile.py`

**Step 1: 增加 golden case**

```python
def test_golden_case_2026_03_02_market(self):
    result = run_calc(2026, 3, 2, 12, "--profile", "market-folk-v1")
    self.assertEqual(result["lunar"]["text"], "2026年1月14日")
    self.assertEqual(result["solar_terms"]["current"], "雨水")
```

**Step 2: 运行全量测试**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: 全绿

**Step 3: 手动抽查 CLI**

Run: `python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile xiejibianfang-v1 --format json`
Expected: 返回 `profileId`、`ruleLayer`、`sourceRef`

Run: `python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --overlay-ruleset xiejibianfang-v1 --format calendar`
Expected: 返回 `isHybrid=true` 的边界说明

**Step 4: Commit**

```bash
git add skills/lao-huangli/tests
git commit -m "test: add lao-huangli multi-profile verification"
```
