# lao-huangli

老黄历计算与解释技能，面向“老黄历怎么得出”的工程化场景。

## 适用场景

- 解释老黄历生成原理
- 指定日期输出农历、干支、节气、宜忌
- 说明哪些结果是可精算、哪些依赖规则流派

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

## 核心方法

1. 输入标准化（日期、时区、年界/日界规则）
2. 历法层计算（JDN、节气、朔望、农历）
3. 干支层计算（年/月/日/时）
4. 规则层映射（建除、值神、神煞、冲煞）
5. 规则引擎生成宜忌并给出理由

## 脚本优先（准确性）

先跑脚本得到可复算字段，再补规则库字段：

```bash
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile market-folk-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile xiejibianfang-v1 --format json
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --overlay-ruleset xiejibianfang-v1 --format json
```

- 脚本可复算：农历、干支、节气区间、12时辰干支
- 规则字段（宜忌/神煞/值神等）未加载规则库时会明确显示“待规则库补齐”

当前支持的 profile：

- `market-folk-v1`：春节换年 + 00:00 换日（大众挂历口径）
- `xiejibianfang-v1`：春节换年 + 00:00 换日（协纪辨方书规则底座预留）
- `bazi-v1`：立春换年 + 23:00 换日（命理排盘口径）

兼容说明：

- 仍兼容旧参数 `--mode market|bazi`
- 新调用应统一使用 `--profile`

当前实现状态：

- 脚本已输出 `meta.profileId`、`profileLabel`、边界字段、`ruleLayer`、`overlayRuleset`
- `xiejibianfang-v1` 与 `market-folk-v1` 已输出最小 `daily/decision`
- `bazi-v1` 默认只输出 `bazi-core`；显式传入 `--overlay-ruleset` 后输出 hybrid 黄历层
- `provenance` 已输出 `ruleLayer`、`ruleSourceLevel`、`sourceRefs`、`isHybrid`

规则来源约束：

- 每条规则文件必须带 `sourceLevel`
- 每条规则文件必须带 `sourceRef`
- `xiejibianfang-v1` 当前使用 `L1-primary`
- `market-folk-v1` 当前混合 `L2-derived-documented` 与 `L3-market-observed`

## 输出建议

- 公历 + 农历
- 干支四柱
- 当前/下一个节气
- 建除、值神、冲煞、胎神、彭祖百忌
- 宜/忌事项与解释
- 元信息：`yearBoundary`、`dayBoundary`、`rulesetVersion`

## 推荐展示（仿挂历，默认详细版）

默认采用“挂历完整版”（正常版本），不是简版。

```text
┌────────────────────────────────────────────────────────────┐
│ 2026年03月02日 星期一                                     │
│ 农历：二〇二六年 正月十四（闰月：否）                      │
│ 干支：丙午年 庚寅月 乙巳日                                │
│ 节气：当前 雨水 → 下个 惊蛰                                │
├────────────────────────────────────────────────────────────┤
│ 【宜】出行  会友  祭祀  祈福  纳财                          │
│ 【忌】动土  开仓  破屋                                      │
├────────────────────────────────────────────────────────────┤
│ 建除：定日  黄黑道：黄道日  值神：天德                     │
│ 冲煞：冲鸡煞西  胎神：仓库门外正南  彭祖百忌：丁不剃头...   │
│ 吉神宜趋：天德、月德、天恩  凶神宜忌：五虚、土符            │
│ 财神：正西  喜神：正南  福神：西北                          │
├────────────────────────────────────────────────────────────┤
│ 时辰吉凶：子/丑/寅/...（12时辰逐行列出）                   │
└────────────────────────────────────────────────────────────┘
```

排版顺序：日期 → 农历/干支/节气 → 宜忌 → 神煞/方位 → 时辰吉凶（12 行）。
只有用户明确说“简版/速览”才降级输出。

## 注意

- 历法与干支可精算；宜忌多依赖规则库
- 不同流派会造成同日结论差异
- 建议在输出中附“文化参考”提示
