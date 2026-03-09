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

## 来源边界

- 基础历法层以 `GB/T 33661-2017《农历的编算和颁行》` 为准。
- 黄历规则层以 `《钦定协纪辨方书》` 为准。
- 若个别事实层字段暂未在 `《钦定协纪辨方书》` 中结构化落盘，可用其他可追溯古籍补充，但必须在 `provenance.sourceRefs` 中显式标明。
- 术语解释和展示材料只用于说明字段含义，不作为宜忌裁决依据。

## 脚本优先（准确性）

先跑脚本得到可复算字段，再补规则库字段：

```bash
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile market-folk-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile xiejibianfang-v1 --format json
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --overlay-ruleset xiejibianfang-v1 --format json
```

- 脚本可复算：农历、干支、节气区间、12时辰干支
- 规则字段（宜忌/值神/吉神凶神/冲煞/胎神/彭祖等）未加载规则库时会明确显示“待规则库补齐”

当前支持的 profile：

- `market-folk-v1`：春节换年 + 00:00 换日（大众挂历口径）
- `xiejibianfang-v1`：春节换年 + 00:00 换日（协纪辨方书规则底座预留）
- `bazi-v1`：立春换年 + 23:00 换日（命理排盘口径）

默认直接查询时，优先按 `market-folk-v1` 输出，效果更接近常见挂历版老黄历。

兼容说明：

- 仍兼容旧参数 `--mode market|bazi`
- 新调用应统一使用 `--profile`

依赖安装：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r skills/lao-huangli/requirements.txt
```

当前实现状态：

- `calendar_core` 与 `rule_engine` 骨架已建立
- 脚本已输出 `meta.profileId`、`profileLabel`、边界字段、`ruleLayer`、`overlayRuleset`
- `xiejibianfang-v1` 与 `market-folk-v1` 已输出可用的 `daily/decision`
- `daily` 已包含 `jianchu`、`yellowBlackDao`、`dutyGod`、`goodStars`、`badStars`、`chongsha`、`taishen`、`pengzu`
- `xiejibianfang-v1` 的 `宜/忌` 已覆盖 `建/除/满/平/定/执/破/危/成/收/开/闭` 的一批卷十直引条目
- `market-folk-v1` 已补齐常用 `冲煞`、`胎神`、`彭祖百忌`，并沿用同一批高频 `建除` 宜忌收口
- `market-folk-v1` 已补齐常用 `财神 / 喜神 / 福神` 方位
- `daily` 已包含 `jianchu`、`yellowBlackDao`、`chongsha`、`taishen`、`pengzu`
- `bazi-v1` 默认只输出 `bazi-core`；显式传入 `--overlay-ruleset` 后输出 hybrid 黄历层
- `provenance` 已输出 `ruleLayer`、`ruleSourceLevel`、`sourceRefs`、`isHybrid`
- 节气现已改为 `Skyfield + JPL ephemeris` 的天文时刻窗口输出，并带 `currentAt` / `nextAt`
- `solar_terms` 已带 `table`、`currentJie`、`currentQi`、`nextJie`、`nextQi`
- `lunar` 已带 `monthStartDate`、`monthEndDate`、`monthDayCount`、`leapMonth`、`zhongQi`、`containsZhongQi`、`anchorYear`、`yearMonthTable`、`yearMonthCount`、`yearLeapMonth`、`currentMonthIndex`、`calculationMode`
- 农历月序、定朔与无中气置闰仍未完整升级到 `GB/T 33661-2017` 口径

规则来源约束：

- 每条规则文件必须带 `sourceLevel`
- 每条规则文件必须带 `sourceRef`
- `xiejibianfang-v1` 当前混合 `L1-primary` 与 `L2-derived-documented`
- `market-folk-v1` 当前混合 `L2-derived-documented` 与 `L3-market-observed`

## 输出建议

- 公历 + 农历
- 干支四柱
- 当前/下一个节气
- 建除、值神、冲煞、胎神、彭祖百忌
- 宜/忌事项与解释
- 元信息：`yearBoundary`、`dayBoundary`、`rulesetVersion`

## 推荐展示（仿挂历，默认详细版）

默认采用“挂历完整版”（正常版本），不是简版。下面只示意版式，不表示某个真实日期的计算结果。

```text
┌────────────────────────────────────────────────────────────┐
│ YYYY年MM月DD日 星期X                                      │
│ 农历：二〇二六年 正月十四（闰月：否）                      │
│ 干支：年柱 / 月柱 / 日柱                                  │
│ 节气：当前 节气A → 下个 节气B                              │
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
