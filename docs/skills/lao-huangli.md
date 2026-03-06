# lao-huangli

老黄历计算与解释技能，面向“如何算出农历/干支/节气/宜忌”的工程化问答。

## 适用场景

- 用户询问“老黄历是怎么算出来的”
- 需要给某一天输出：农历、干支、节气、冲煞、宜忌
- 需要区分“可精确计算”与“规则流派差异”

## 目录结构

```text
skills/lao-huangli/
├── SKILL.md
├── rules/
│   ├── profiles/
│   ├── shared/
│   ├── market-folk-v1/
│   ├── xiejibianfang-v1/
│   └── bazi-v1/
├── scripts/
│   └── huangli_calc.py
├── tests/
│   ├── test_huangli_calc.py
│   ├── test_rules_schema.py
│   └── test_source_integrity.py
└── references/
    ├── calculation-pipeline.md
    └── rules-and-variants.md
```

## 方法论（先历法、后规则）

1. 输入标准化（日期时间、时区、边界设定）
2. 计算基础历法（JDN、节气、朔望、农历）
3. 计算干支（年/月/日/时）
4. 套神煞/值神/建除规则表
5. 用规则引擎生成宜忌与理由

## Source Boundary

- The calendar core should follow `GB/T 33661-2017 Calculation and promulgation of the Chinese calendar`.
- The almanac rule layer should follow `Qinding Xieji Bianfang Shu`.
- If a fact-layer field has not yet been structurally extracted from `Qinding Xieji Bianfang Shu`, another traceable classical source may be used only when it is explicitly listed in `provenance.sourceRefs`.
- Glossaries and field explainers are documentation aids only, not rule authorities.

## Script-first Accuracy

Run script first for reproducible fields, then enrich with ruleset fields:

```bash
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile market-folk-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile xiejibianfang-v1 --format json
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --overlay-ruleset xiejibianfang-v1 --format json
```

- Script-computable: lunar date, ganzhi pillars, solar-term window, 12-hour ganzhi slots
- Rule-table fields (yi/ji, stars, duty god, etc.) stay explicit placeholders until a ruleset is loaded

Supported calculation profiles:

- `market-folk-v1`: spring-festival year boundary + 00:00 day boundary
- `xiejibianfang-v1`: spring-festival year boundary + 00:00 day boundary
- `bazi-v1`: lichun year boundary + 23:00 day boundary

Compatibility note:

- Legacy `--mode market|bazi` is still accepted
- New work should use `--profile`

Current implementation status:

- The `calendar_core` and `rule_engine` scaffolds are now in place
- The script emits `meta.profileId`, `profileLabel`, boundary metadata, `ruleLayer`, and `overlayRuleset`
- `xiejibianfang-v1` and `market-folk-v1` now emit minimal `daily` and `decision` outputs
- `daily` now carries `jianchu`, `yellowBlackDao`, `chongsha`, `taishen`, and `pengzu`
- `bazi-v1` defaults to `bazi-core`; `--overlay-ruleset` enables hybrid almanac output
- `provenance` emits `ruleLayer`, `ruleSourceLevel`, `sourceRefs`, and `isHybrid`
- Solar terms are still exposed as `day-approximate / table-window`, not yet full standard-grade astronomical calculation

Rule provenance constraints:

- Every rule file must carry `sourceLevel`
- Every rule file must carry `sourceRef`
- `xiejibianfang-v1` currently mixes `L1-primary` and `L2-derived-documented`
- `market-folk-v1` currently mixes `L2-derived-documented` and `L3-market-observed`

## 输出建议

- 公历与农历
- 干支四柱
- 当前/下一个节气
- 建除、值神、冲煞、胎神、彭祖百忌
- 宜/忌事项 + 规则理由
- `meta`（规则版本、年界、日界）

## Recommended Display (Calendar-like, default full version)

Default output should be a **full calendar-style panel** (not a brief card), unless user explicitly requests a concise mode. The block below shows layout only, not a real calculated date.

```text
┌────────────────────────────────────────────────────────────┐
│ YYYY-MM-DD Weekday                                         │
│ Lunar: Year YYYY Month M Day D (Leap: No)                │
│ Ganzhi: Year Pillar / Month Pillar / Day Pillar          │
│ Solar terms: Current term -> Next term (approximate)     │
├────────────────────────────────────────────────────────────┤
│ [Yi] travel, worship, meetup, pray, wealth                │
│ [Ji] groundbreaking, warehouse opening, demolition         │
├────────────────────────────────────────────────────────────┤
│ Jianchu / Duty God / Yellow-Black day / Chongsha          │
│ Taishen / Pengzu taboo / Good stars / Bad stars           │
│ Wealth God / Joy God / Fortune God directions             │
├────────────────────────────────────────────────────────────┤
│ Hourly fortune (12 two-hour slots, one line per slot)     │
└────────────────────────────────────────────────────────────┘
```

Order: date → lunar/ganzhi/solar-term → yi/ji → daily gods/aux data → 12-hour table.

## 注意事项

- 历法层可精算；宜忌层通常依赖规则库
- 不同流派在年界（日界）与规则映射上会出现差异
- 输出应带“文化参考”免责声明，不替代法律、医疗、财务、安全建议
