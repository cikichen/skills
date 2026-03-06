# Lao Huangli Skyfield Standard Core Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `skills/lao-huangli` 引入 `Skyfield` 天文历算底座，替换节气近似表并暴露真实节气时刻能力。

**Architecture:** 新增 `astronomy.py` 负责天文事件查询，`calendar_core.py` 负责历法口径封装，CLI 继续经由 `build_calendar_context()` 输出兼容结构。先完成节气能力升级，再为后续定朔/闰月改造保留接口。

**Tech Stack:** Python 3、uv、Skyfield、JPL ephemeris、unittest

---

### Task 1: 建立 Skyfield 依赖与节气接口失败测试

**Files:**
- Create: `skills/lao-huangli/src/lao_huangli/astronomy.py`
- Modify: `skills/lao-huangli/tests/test_standard_calendar_core.py`

**Step 1: Write the failing test**

```python
def test_solar_terms_use_astronomical_precision():
    result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")
    self.assertEqual(result["solar_terms"]["precision"], "astronomical")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest skills.laohuangli.tests.test_standard_calendar_core -v`
Expected: FAIL, 当前仍输出 `day-approximate`

**Step 3: Write minimal implementation**

- 新增 `astronomy.py`
- 暴露节气查询入口

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest skills.laohuangli.tests.test_standard_calendar_core -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/astronomy.py skills/lao-huangli/tests/test_standard_calendar_core.py
git commit -m "test: add astronomical solar term expectations"
```

### Task 2: 用 Skyfield 接管节气窗口输出

**Files:**
- Modify: `skills/lao-huangli/src/lao_huangli/calendar_core.py`
- Modify: `skills/lao-huangli/scripts/huangli_calc.py`
- Test: `skills/lao-huangli/tests/test_standard_calendar_core.py`

**Step 1: Write the failing test**

```python
def test_solar_terms_include_crossing_timestamps():
    result = run_calc(2026, 3, 6, 12, "--profile", "market-folk-v1")
    self.assertIn("currentAt", result["solar_terms"])
    self.assertIn("nextAt", result["solar_terms"])
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest skills.laohuangli.tests.test_standard_calendar_core -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- `calendar_core.py` 调用 `astronomy.py`
- 输出 `currentAt` / `nextAt`

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest skills.laohuangli.tests.test_standard_calendar_core -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/lao-huangli/src/lao_huangli/calendar_core.py skills/lao-huangli/scripts/huangli_calc.py skills/lao-huangli/tests/test_standard_calendar_core.py
git commit -m "feat: use skyfield solar term windows"
```

### Task 3: 全量回归并补文档

**Files:**
- Modify: `skills/lao-huangli/SKILL.md`
- Modify: `docs/skills/lao-huangli.md`
- Modify: `docs/skills/lao-huangli_CN.md`

**Step 1: Update docs**

- 说明节气已升级为天文时刻来源
- 明确农历月序/闰月仍未完全重写

**Step 2: Run full verification**

Run: `python3 -m unittest discover -s skills/lao-huangli/tests -p 'test_*.py'`
Expected: PASS

**Step 3: Commit**

```bash
git add skills/lao-huangli/SKILL.md docs/skills/lao-huangli.md docs/skills/lao-huangli_CN.md
git commit -m "docs: describe astronomical solar term support"
```
