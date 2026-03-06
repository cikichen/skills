# Lao Huangli Multi-Profile Design

**日期：** 2026-03-06

**目标：** 为 `skills/lao-huangli` 建立一个“单一历法核心 + 多 profile/ruleset”的结构，第一版至少支持 `market-folk-v1`、`xiejibianfang-v1`、`bazi-v1` 三套口径，并保证规则来源可追溯、不可编造。

## 背景

当前 `skills/lao-huangli/scripts/huangli_calc.py` 已支持两种基础口径：

- `market`：春节换年 + `00:00` 换日
- `bazi`：立春换年 + `23:00` 换日

但当前脚本仍只输出基础历法字段，宜忌/神煞/值神等规则字段仍是占位符。要继续扩展，不能直接把多种规则混进一个 `if/else` 脚本，否则会同时损坏维护性与可解释性。

## 设计原则

1. 先算历法，再套规则。
2. 基础历法层尽量共用，流派差异通过 `profile` 参数化。
3. 规则层通过 `ruleset` 装载，不允许把来源不明的规则硬编码进脚本。
4. 输出必须显式携带口径、边界、规则来源等级与版本。
5. `bazi` 与挂历宜忌不是同一体系，必须允许 `bazi-core` 与 `almanac-overlay` 分离。

## 支持范围

第一版正式支持三套 profile：

- `market-folk-v1`
  - 面向市售挂历 / 农民历
  - `spring-festival` 换年
  - `00:00` 换日
  - 展示优先

- `xiejibianfang-v1`
  - 以《钦定协纪辨方书》为规则底本
  - 默认使用民用日期边界起步：`spring-festival` + `00:00`
  - 强调规则出处和可解释性

- `bazi-v1`
  - 面向命理/排盘口径
  - `lichun` 换年
  - `23:00` 换日
  - 默认只输出 `bazi-core`
  - 可选挂接 `overlay-ruleset`

## 核心架构

统一执行流：

```text
输入
-> calendar core
-> profile 边界决策
-> ruleset 载入
-> rule engine 计算神煞/宜忌
-> 冲突裁决
-> 输出 + 来源说明
```

## 数据模型

建议运行时对象分为三层：

```json
{
  "calendarContext": {
    "profileId": "market-folk-v1",
    "date": {},
    "lunar": {},
    "ganzhi": {},
    "solarTerms": {},
    "boundaries": {}
  },
  "ruleContext": {
    "rulesetId": "xiejibianfang-v1",
    "jianchu": "",
    "yellowBlackDao": "",
    "dutyGod": "",
    "goodStars": [],
    "badStars": [],
    "chongsha": {},
    "directions": {},
    "sourceRefs": []
  },
  "decision": {
    "yi": [],
    "ji": [],
    "warnings": [],
    "explanations": []
  }
}
```

### `profile` 职责

`profile` 只负责“这一天怎么算”，包含：

- `id`
- `label`
- `yearBoundary`
- `dayBoundary`
- `timezonePolicy`
- `solarTermPrecision`
- `defaultDisplay`
- `enabledRuleFamilies`

### `ruleset` 职责

`ruleset` 只负责“当天如何判宜忌”，包含：

- `id`
- `source`
- `version`
- `families`
- `priorityPolicy`
- `conflictPolicy`

## 能力矩阵

### `market-folk-v1`

必须支持：

- 公历/农历/星期
- 年月日时干支
- 当前/下个节气
- 建除十二神
- 黄道/黑道
- 值神
- 冲煞
- 彭祖百忌
- 财神/喜神/福神
- 宜/忌

### `xiejibianfang-v1`

必须支持：

- 上述大多数字段
- 每条规则带 `sourceRef`
- 宜/忌附解释
- 输出中标明卷次来源

### `bazi-v1`

默认支持：

- 公历/农历/星期
- 年月日时干支
- 节气
- 12 时辰
- 年界/日界说明

默认不承诺：

- 挂历式宜忌
- 民用黄黑道字段

如需宜忌，必须显式开启：

- `overlayRuleset = xiejibianfang-v1` 或 `market-folk-v1`
- 输出中标记 `isHybrid = true`

## CLI 设计

保留现有脚本入口，扩展参数：

```bash
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile market-folk-v1 --format calendar
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 12 --profile xiejibianfang-v1 --format json --source-trace
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --format json
python3 skills/lao-huangli/scripts/huangli_calc.py 2026 3 2 23 --profile bazi-v1 --overlay-ruleset xiejibianfang-v1 --format calendar
```

建议新增参数：

- `--profile`
- `--overlay-ruleset`
- `--source-trace`
- `--compact`
- `--strict`
- `--explain`

## 文件布局

```text
skills/lao-huangli/
├── SKILL.md
├── scripts/
│   └── huangli_calc.py
├── rules/
│   ├── profiles/
│   │   ├── market-folk-v1.json
│   │   ├── xiejibianfang-v1.json
│   │   └── bazi-v1.json
│   ├── shared/
│   │   ├── actions.json
│   │   ├── directions.json
│   │   └── stems-branches.json
│   ├── market-folk-v1/
│   ├── xiejibianfang-v1/
│   └── bazi-v1/
└── tests/
```

## 规则落盘规范

每类规则单独成表，不混放：

- `jianchu.json`
- `yellow-black-dao.json`
- `duty-gods.json`
- `shensha-good.json`
- `shensha-bad.json`
- `chongsha.json`
- `pengzu.json`
- `taishen.json`
- `directions.json`
- `yi-ji-rules.json`
- `sources.json`

`yi-ji-rules.json` 采用“条件 + 作用 + 优先级”结构：

```json
{
  "id": "xjbfs-yi-travel-001",
  "action": "出行",
  "effect": "yi",
  "priority": 60,
  "conditions": [
    {"field": "jianchu", "op": "in", "value": ["开", "成", "定"]},
    {"field": "yellowBlackDao", "op": "in", "value": ["青龙", "明堂", "金匮", "天德", "玉堂", "司命"]}
  ],
  "reasonTemplate": "建除与黄道同吉，利于出行",
  "sourceRef": ["xiejibianfang:juan4", "xiejibianfang:juan7", "xiejibianfang:juan10"]
}
```

## 冲突裁决

统一裁决顺序：

1. 绝对禁忌覆盖一切
2. 强忌压过一般宜
3. 强宜压过一般忌
4. 其余按得分求和
5. 最终归类为 `宜 / 忌 / 慎用`

## 来源约束

### 来源等级

- `L1-primary`
  - 原始/准原始来源，如《钦定协纪辨方书》
- `L2-derived-documented`
  - 明确说明依据的现代整理
- `L3-market-observed`
  - 市售挂历/App 的观测归纳，只允许用于 `market-folk-v1`

禁止：

- 无来源规则
- 来源等级缺失
- 运行时兜底编造规则

### 规则必填字段

```json
{
  "id": "xjbfs-yi-travel-001",
  "sourceLevel": "L1-primary",
  "sourceRef": [
    {
      "work": "钦定协纪辨方书",
      "location": "卷十",
      "url": "https://zh.wikisource.org/..."
    }
  ],
  "confidence": 0.92,
  "interpretationType": "direct",
  "notes": "按卷十宜忌表归纳"
}
```

缺少 `sourceRef` 的规则不得参与执行。

## 输出约束

所有输出必须明确区分：

- 历法层：算法计算
- 规则层：哪套 ruleset
- 来源等级：`L1/L2/L3`
- 是否混合：`isHybrid`

示例：

```json
{
  "provenance": {
    "calendarCore": "algorithmic",
    "ruleLayer": "xiejibianfang-v1",
    "ruleSourceLevel": "L1-primary",
    "isHybrid": false
  }
}
```

## 实施顺序

1. 先重构脚本，拆出 `profile` 与 `ruleset` 基础设施。
2. 先实现 `xiejibianfang-v1` 最小闭环：
   - 建除十二神
   - 黄黑道十二神
   - 少量高频宜忌事项
3. 再实现 `market-folk-v1`：
   - 以 `xiejibianfang-v1` 为底
   - 仅在有证据时添加 `L3-market-observed` 差异
4. 最后实现 `bazi-v1`：
   - 完成 `bazi-core`
   - 再接 `overlay-ruleset`

## 验证策略

至少三类测试：

1. Schema 测试
   - 所有规则文件符合 schema
   - 所有规则具备来源字段

2. Source Integrity 测试
   - `xiejibianfang-v1` 不允许出现 `L3-market-observed`
   - `bazi-v1` 默认不输出无 overlay 的宜忌

3. Golden Case 测试
   - 基础历法样例
   - 卷四/卷七/卷十可追溯样例
   - 混合模式样例

## 风险与边界

- 市售挂历规则高度商品化，不存在单一官方标准。
- `xiejibianfang-v1` 规则实现时需要区分“直接原文”与“工程归纳”。
- `bazi-v1` 的宜忌一旦走 overlay，必须防止用户误解为“八字体系原生宜忌”。
- 节气如继续使用简化表，只能声明为近似值；若要卷十级别可解释输出，未来需补天文精度。

## 结论

本设计采用“单一历法核心 + 多 profile/ruleset”的方式，在不混淆挂历、通书、八字三类体系的前提下，实现统一接口、统一输出、统一校验，并通过来源等级与 `sourceRef` 保证规则不被编造。
