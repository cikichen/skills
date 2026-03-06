# Lao Huangli Standard Core + Xiejibianfang Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `skills/lao-huangli` 建立“国家标准基础历法层 + 协纪辨方书规则层”的实现基础，先完成 `GB/T 33661-2017` 对齐的 calendar core，再逐步接入完整 `xiejibianfang-v1` 规则层。

**Architecture:** 将当前 `scripts/huangli_calc.py` 中混合的历法与规则逻辑拆为 `calendar_core` 与 `rule_engine` 两层。基础历法层只认 `docs/GB_T+33661-2017.pdf`，规则层只认《钦定协纪辨方书》及其受控结构化规则表。所有新增行为都先写失败测试，再做最小实现。

**Tech Stack:** Python 3、`unittest`、JSON 规则文件、现有 CLI 脚本

---

### Task 1: 记录国家标准约束并建立 golden tests 骨架

**Files:**
- Create: `skills/lao-huangli/tests/test_standard_calendar_core.py`
- Modify: `skills/lao-huangli/tests/test_huangli_calc.py`
- Reference: `docs/GB_T+33661-2017.pdf`

**Step 1: 写失败测试，固定国家标准相关样例**

```python
def test_day_ganzhi_reference_matches_standard():
    result = run_calc(1949, 10, 1, 12, "--profile", "market-folk-v1")
    assert result["ganzhi"]["day"] == "甲子"
```

再补：

- `1984-02-02` 对应 `甲子年`
- 节气/农历样例来自官方年历或月历

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，暴露当前 calendar core 与标准不一致或覆盖不完整

**Step 3: 只补最小测试骨架，不实现新逻辑**

- 保持断言集中在标准条款可核实内容
- 不先引入规则层断言

**Step 4: 再次运行测试确认仍为预期失败**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: 失败点明确落在标准历法层

**Step 5: Commit**

```bash
git add skills/lao-huangli/tests/test_standard_calendar_core.py skills/lao-huangli/tests/test_huangli_calc.py
git commit -m "test: add standard calendar core golden cases"
```

### Task 2: 抽离 `calendar_core` 模块骨架

**Files:**
- Create: `skills/lao-huangli/src/lao_huangli/calendar_core.py`
- Create: `skills/lao-huangli/src/lao_huangli/__init__.py`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_standard_calendar_core.py`

**Step 1: 写失败测试，要求 CLI 通过新模块返回相同结构**

```python
def test_cli_uses_calendar_core_for_basic_fields():
    result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")
    assert "lunar" in result
    assert "ganzhi" in result
    assert "solar_terms" in result
```

**Step 2: 运行测试确认失败或 import 错误**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: FAIL，提示 `calendar_core` 尚不存在或 CLI 尚未接入

**Step 3: 最小实现模块骨架**

```python
def build_calendar_context(...):
    return {
        "date": ...,
        "lunar": ...,
        "ganzhi": ...,
        "solar_terms": ...,
    }
```

CLI 中仅改成装配调用，不重构行为。

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: CLI 行为不变，结构性测试通过

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli skills/lao-huangli/scripts/huangli_calc.py
git commit -m "refactor: extract lao-huangli calendar core scaffold"
```

### Task 3: 固化国家标准纪年/纪日参考时间

**Files:**
- Modify: `skills/lao-huangli/src/lao_huangli/calendar_core.py`
- Test: `skills/lao-huangli/tests/test_standard_calendar_core.py`

**Step 1: 写失败测试**

```python
def test_1949_10_01_is_jiazi_day():
    result = run_calc(1949, 10, 1, 12, "--profile", "market-folk-v1")
    assert result["ganzhi"]["day"] == "甲子"

def test_1984_02_02_is_jiazi_year_reference():
    result = run_calc(1984, 2, 2, 12, "--profile", "market-folk-v1")
    assert result["ganzhi"]["year"] == "甲子"
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest skills.lao-huangli.tests.test_standard_calendar_core -v`
Expected: FAIL，显示参考时间尚未完全显式化

**Step 3: 最小实现**

- 为纪年、纪日引入显式命名常量
- 用标准参考时间替代隐含魔数
- 保持现有通过样例继续通过

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest skills.lao-huangli.tests.test_standard_calendar_core -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/calendar_core.py skills/lao-huangli/tests/test_standard_calendar_core.py
git commit -m "fix: align ganzhi references with national standard"
```

### Task 4: 替换近似节气表的接口边界

**Files:**
- Modify: `skills/lao-huangli/src/lao_huangli/calendar_core.py`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_standard_calendar_core.py`
- Reference: `docs/GB_T+33661-2017.pdf`

**Step 1: 写失败测试，要求节气结果带可扩展的精度元数据**

```python
def test_solar_terms_emit_precision_metadata():
    result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")
    assert "precision" in result["solar_terms"]
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest skills.lao-huangli.tests.test_standard_calendar_core -v`
Expected: FAIL，当前 `solar_terms` 未暴露精度能力

**Step 3: 最小实现**

- 将当前节气近似逻辑封装成单独函数接口
- 暴露 `precision`、`calculationMode`
- 先不在本任务内实现 1 秒级天文算法，只把替换点抽出来

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest skills.lao-huangli.tests.test_standard_calendar_core -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/calendar_core.py skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_standard_calendar_core.py
git commit -m "refactor: isolate solar term calculation interface"
```

### Task 5: 抽离 `rule_engine` 模块骨架

**Files:**
- Create: `skills/lao-huangli/src/lao_huangli/rule_engine.py`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`

**Step 1: 写失败测试，要求规则层通过统一入口输出**

```python
def test_xiejibianfang_rules_are_resolved_by_rule_engine():
    result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")
    assert "daily" in result
    assert "decision" in result
```

**Step 2: 运行测试确认失败或未接入新模块**

Run: `python3 -m unittest skills.lao-huangli.tests.test_xiejibianfang_rules -v`
Expected: FAIL，说明尚未通过 `rule_engine` 统一装配

**Step 3: 最小实现**

```python
def evaluate_ruleset(calendar_context, ruleset_id):
    return daily, decision, provenance
```

CLI 改为调用该函数。

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest skills.lao-huangli.tests.test_xiejibianfang_rules -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/rule_engine.py skills/lao-huangli/scripts/huangli_calc.py
git commit -m "refactor: extract lao-huangli rule engine scaffold"
```

### Task 6: 扩建 `xiejibianfang-v1` 规则文件骨架

**Files:**
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/duty-gods.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/good-stars.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/bad-stars.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/chongsha.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/taishen.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/pengzu.json`
- Create: `skills/lao-huangli/rules/xiejibianfang-v1/sources.json`
- Test: `skills/lao-huangli/tests/test_source_integrity.py`

**Step 1: 写失败测试，要求这些规则文件存在且都带来源字段**

```python
def test_xiejibianfang_rule_families_exist():
    for name in [...]:
        assert (ROOT / "rules" / "xiejibianfang-v1" / name).exists()
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest skills.lao-huangli.tests.test_source_integrity -v`
Expected: FAIL，提示规则文件缺失

**Step 3: 最小实现**

- 创建空骨架列表或最小条目
- 每个条目都带 `sourceLevel/sourceRef/interpretationType/notes`

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest skills.lao-huangli.tests.test_source_integrity -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/rules/xiejibianfang-v1 skills/lao-huangli/tests/test_source_integrity.py
git commit -m "feat: add xiejibianfang rule family skeletons"
```

### Task 7: 为规则事实层补充逐类测试入口

**Files:**
- Create: `skills/lao-huangli/tests/test_rule_facts.py`
- Modify: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`

**Step 1: 写失败测试，分别约束建除、黄黑道、冲煞、胎神、彭祖字段**

```python
def test_rule_facts_include_chongsha_taishen_pengzu():
    result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")
    assert "daily" in result
    assert "chongsha" in result["daily"]
    assert "taishen" in result["daily"]
    assert "pengzu" in result["daily"]
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest skills.lao-huangli.tests.test_rule_facts -v`
Expected: FAIL，显示规则事实层字段还未接出

**Step 3: 只添加测试，不实现**

- 保证失败点聚焦在缺字段，而不是测试写错

**Step 4: 再运行一次确认失败信息正确**

Run: `python3 -m unittest skills.lao-huangli.tests.test_rule_facts -v`
Expected: FAIL，缺少对应字段

**Step 5: Commit**

```bash
git add skills/lao-huangli/tests/test_rule_facts.py skills/lao-huangli/tests/test_xiejibianfang_rules.py
git commit -m "test: add xiejibianfang rule fact expectations"
```

### Task 8: 建立宜忌裁决器接口和优先级骨架

**Files:**
- Modify: `skills/lao-huangli/src/lao_huangli/rule_engine.py`
- Modify: `skills/lao-huangli/rules/xiejibianfang-v1/yi-ji-rules.json`
- Test: `skills/lao-huangli/tests/test_xiejibianfang_rules.py`

**Step 1: 写失败测试，要求 `decision` 同时输出 items 与 explanations**

```python
def test_decision_contains_explanations_and_source_trace():
    result = run_calc(2026, 3, 6, 12, "--profile", "xiejibianfang-v1")
    assert "explanations" in result["decision"]
    assert result["provenance"]["sourceRefs"]
```

**Step 2: 运行测试确认失败**

Run: `python3 -m unittest skills.lao-huangli.tests.test_xiejibianfang_rules -v`
Expected: FAIL，裁决接口尚不完整

**Step 3: 最小实现**

- 在 `rule_engine` 中建立裁决顺序骨架：
  - 绝对禁忌
  - 强忌
  - 强宜
  - 其余求和
- 暂时仍只消费小规模规则

**Step 4: 运行测试确认通过**

Run: `python3 -m unittest skills.lao-huangli.tests.test_xiejibianfang_rules -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/rule_engine.py skills/lao-huangli/rules/xiejibianfang-v1/yi-ji-rules.json skills/lao-huangli/tests/test_xiejibianfang_rules.py
git commit -m "feat: add xiejibianfang decision engine skeleton"
```

### Task 9: 更新技能文档，明确双原典体系

**Files:**
- Modify: `skills/lao-huangli/SKILL.md`
- Modify: `docs/skills/lao-huangli.md`
- Modify: `docs/skills/lao-huangli_CN.md`

**Step 1: 写失败测试或检查清单**

建立人工 checklist：

- 文档中明确写出 `GB/T 33661-2017` 负责基础历法层
- 文档中明确写出《钦定协纪辨方书》负责规则层
- 文档中不再把术语百科当作规则原典

**Step 2: 按 checklist 修改文档**

- 更新“来源约束”
- 更新“完整性边界”
- 更新“推荐实现顺序”

**Step 3: 运行最小文档一致性检查**

Run: `rg -n "GB/T 33661|协纪辨方书|术语" skills/lao-huangli docs/skills`
Expected: 三份文档都出现正确来源说明

**Step 4: Commit**

```bash
git add skills/lao-huangli/SKILL.md docs/skills/lao-huangli.md docs/skills/lao-huangli_CN.md
git commit -m "docs: document standard core and xiejibianfang split"
```

### Task 10: 全量验证并收口

**Files:**
- Verify only

**Step 1: 跑全量测试**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: 所有测试通过

**Step 2: 跑关键 CLI 样例**

Run:

```bash
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 6 12 --profile xiejibianfang-v1 --format json
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --format json
```

Expected:

- `2026-03-06` 输出 `己卯日`
- `2026-03-06` 输出 `建 / 明堂`
- `bazi-v1` 仍保留正确的 `23:00` 逻辑日切换

**Step 3: 检查工作区只包含本轮改动**

Run: `git status --short`
Expected: 只出现本轮文件

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: lay foundation for standard calendar core and full xiejibianfang rules"
```

