# Lao Huangli Remaining Work

## 当前状态

`lao-huangli` 已完成以下基础能力：

- `GB/T 33661-2017` 锚点测试已接入，覆盖 `1949-10-01 = 甲子日`、`1984-02-02 = 甲子年` 和 `2026-03-06` 官方样例。
- `xiejibianfang-v1` 已接入最小可用规则层，当前可输出 `建除`、`黄黑道`、`冲煞`、`胎神`、`彭祖百忌` 和一部分 `宜/忌`。
- 输出已区分字段来源，`provenance.fieldSources` 会标记 `L1-primary` 与 `L2-derived-documented`。

## 未完成事项

### 1. 基础历法层尚未完全对齐国家标准精度

- 节气窗口已经升级为 `Skyfield + JPL ephemeris` 的天文时刻输出，但目前只完成了节气层。
- 当前农历核心还没有实现真正的 `定朔` 计算，也没有按标准完整落地“含冬至者为十一月”和“无中气置闰”流程。
- 需要继续把 `calendar_core.py` 从“天文节气 + 表驱动农历”推进到真正的国家标准口径。

### 2. 《协纪辨方书》规则层仍不完整

- `good-stars.json`、`bad-stars.json`、`duty-gods.json`、`sources.json` 目前仍是骨架文件，尚未接入真实命中逻辑。
- `yi-ji-rules.json` 目前只覆盖最小闭环和卷十中一部分可直接程序化的条目，尚未完整覆盖各类 `建除` 与神煞组合裁决。
- `market-folk-v1` 还没有基于 `xiejibianfang-v1` 完成系统化派生。

### 3. 字段来源仍需继续收紧

- `taishen` 当前来源等级是 `L2-derived-documented`，还不是直接原典表。
- `chongsha` 当前来源等级也是 `L2-derived-documented`，后续需要继续补更硬的古籍对应依据。
- 需要继续明确哪些字段来自《协纪辨方书》，哪些字段来自补充古籍或现代整理资料。

### 4. 测试覆盖仍需扩展

- 需要补更多 `golden cases`，至少覆盖节气交接日、月首月末、闰月年和更多干支组合。
- 需要补规则层对照样例，避免只靠少量日期回归。
- 需要增加 `market-folk-v1` 和 `bazi-v1 + overlay` 的系统性回归测试。

## 推荐下一步

1. 先完成 `calendar_core.py` 的国家标准升级，替换近似节气表。
2. 再补 `xiejibianfang-v1` 的 `good-stars / bad-stars / duty-gods` 真实规则。
3. 最后扩完整 `宜/忌` 裁决，并补足 `market-folk-v1` 的派生规则。
