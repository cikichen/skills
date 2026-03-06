# Lao Huangli Standard Core + Xiejibianfang Design

**日期：** 2026-03-06

**目标：** 将 `skills/lao-huangli` 重构为“国家标准基础历法层 + 协纪辨方书规则层”的两阶段体系，确保基础历法与黄历规则各自有正式来源，且来源边界清晰、不可编造。

## 背景

当前 `skills/lao-huangli` 已具备：

- 多 profile 输出骨架
- 最小 `xiejibianfang-v1` / `market-folk-v1` 规则集
- `bazi-v1` 的边界与 overlay 机制
- 基础测试与来源元数据校验

但仍存在两个结构性问题：

1. 基础历法层尚未对齐国家标准 `GB/T 33661-2017《农历的编算和颁行》`
2. 老黄历规则层尚未扩展为完整的《钦定协纪辨方书》规则体系

这导致当前实现只能被诚实表述为“可运行的最小黄历原型”，而不是“完整、可追溯的标准化老黄历引擎”。

## 设计原则

1. **分层治理**：基础历法层与黄历规则层分开实现，不混源。
2. **标准优先**：农历、节气、干支等确定性字段以国家标准为准。
3. **原典优先**：建除、黄黑道、神煞、宜忌等规则字段以《钦定协纪辨方书》为准。
4. **显式缺失**：未实现规则不得伪造，必须明确返回未实现状态。
5. **来源可追溯**：所有规则条目必须带来源等级、出处和解释类型。
6. **验证先于宣称**：任何“已完成/已正确”声明都要以 fresh verification 为前提。

## 来源分层

### L1-A：基础历法原典

主来源：`docs/GB_T+33661-2017.pdf`

该标准覆盖：

- 农历编排规则
- 朔与节气的定义
- 闰月规则
- 干支纪年/纪日参考时间
- 表示方法
- 公开颁行要求

它负责回答：

- 这一天的农历日期是什么
- 是否闰月
- 当前与下一个节气是什么
- 年/月/日/时干支是什么

### L1-B：黄历规则原典

主来源：`《钦定协纪辨方书》`

该原典负责：

- 建除十二神
- 黄道黑道十二神
- 吉神凶煞起例
- 冲煞、胎神、彭祖百忌
- 宜忌事项裁决

它负责回答：

- 为什么今天是建日/破日
- 为什么今天值明堂/白虎
- 为什么某事项宜或忌

### L2：解释与展示辅助材料

这类材料包括：

- 术语解释文档
- 字段释义汇编
- 用户界面展示词典

它们可以：

- 解释“祭祀/祈福/纳采/移徙”等术语
- 帮助生成用户文案

但不能：

- 直接作为宜忌裁决依据
- 覆盖或替代 L1 主来源

## 两阶段架构

### Phase A：National Calendar Core

职责：实现 `GB/T 33661-2017` 口径的基础历法核心。

必须覆盖：

- 北京时间
- 朔日定月
- 冬至定十一月
- 无中气置闰
- 农历日期表示
- 干支纪年参考时间
- 干支纪日参考时间
- 节气与朔的计算精度要求

输出：

- 农历年/月/日/闰月
- 节气时刻与窗口
- 年/月/日/时干支
- 供规则层消费的标准化上下文

不负责：

- 建除
- 黄黑道
- 神煞
- 宜忌

### Phase B：Xiejibianfang Rule Layer

职责：在 Phase A 的确定性结果之上，叠加《钦定协纪辨方书》的规则系统。

必须覆盖：

- 建除十二神
- 黄道黑道十二神
- 吉神凶煞
- 冲煞
- 胎神
- 彭祖百忌
- 宜忌事项裁决

输出：

- `daily`
- `decision`
- `provenance`

不负责：

- 重新计算农历和节气
- 重写干支逻辑

## 模块设计

建议将当前单文件脚本拆分为：

```text
skills/lao-huangli/
├── scripts/
│   └── huangli_calc.py
├── src/
│   └── lao_huangli/
│       ├── calendar_core.py
│       ├── rule_engine.py
│       ├── profiles.py
│       ├── rendering.py
│       └── sources.py
├── rules/
│   ├── profiles/
│   ├── shared/
│   ├── xiejibianfang-v1/
│   ├── market-folk-v1/
│   └── bazi-v1/
└── tests/
```

### `calendar_core.py`

负责：

- 时间基准
- JDN/JD
- 节气/朔
- 农历月序
- 闰月判断
- 干支

### `rule_engine.py`

负责：

- 规则装载
- 建除/黄黑道命中
- 神煞计算
- 宜忌裁决

### `rendering.py`

负责：

- JSON 输出
- 挂历样式输出
- provenance/能力说明

### `sources.py`

负责：

- 来源等级枚举
- 来源对象校验
- 输出中来源聚合

## 规则数据模型

`xiejibianfang-v1` 规则文件至少拆为：

- `jianchu.json`
- `yellow-black-dao.json`
- `duty-gods.json`
- `good-stars.json`
- `bad-stars.json`
- `chongsha.json`
- `taishen.json`
- `pengzu.json`
- `yi-ji-rules.json`
- `sources.json`

每条规则必须带：

- `id`
- `sourceLevel`
- `sourceRef`
- `interpretationType`
- `notes`

其中：

- `sourceLevel`：`L1-primary` / `L2-derived-documented` / `L3-market-observed`
- `interpretationType`：`direct` / `derived` / `market-observed`

`xiejibianfang-v1` 仅允许：

- `L1-primary`
- 少量必要的 `L2-derived-documented`

禁止：

- `L3-market-observed`
- 无来源规则
- 占位结果伪装成真实规则

## 适用范围与非目标

### 本轮纳入范围

- 完整对齐国家标准的基础历法层设计
- 完整协纪辨方书版规则层设计
- Golden cases 和来源校验设计

### 本轮非目标

- 先行扩展 `market-folk-v1` 到完整挂历版
- 用市售黄历结果“反推”规则
- 用术语百科替代原典规则

## 验证策略

### 基础历法层验证

对照对象：

- 国家标准参考条款
- 官方农历年历/月历

抽样至少覆盖：

- 普通日
- 节气交接日
- 月首/月末
- 闰月年
- `23:00` / `00:00` 边界样例

### 规则层验证

对照对象：

- 《钦定协纪辨方书》卷次原文
- 已结构化规则文件

验证目标：

- 每条可执行规则都能追到卷次
- 没有无来源运行中规则
- `xiejibianfang-v1` 不混入市场观察型规则

### 输出验证

每次结果都必须显式区分：

- `algorithmic`
- `rule-derived`

并带上：

- `profileId`
- `rulesetVersion`
- `ruleSourceLevel`
- `sourceRefs`
- `isHybrid`

## 分批实施策略

### Batch 1：国家标准基础历法层

目标：

- 先把农历/节气/干支真正对齐 `GB/T 33661-2017`

关键工作：

- 替换近似节气表
- 固化干支纪年/纪日参考时间
- 增加官方样例测试

### Batch 2：协纪辨方书规则事实层

目标：

- 扩建建除、黄黑道、神煞、冲煞、胎神、彭祖等规则族

关键工作：

- 建立完整规则文件骨架
- 补充来源元数据
- 建立逐类测试

### Batch 3：宜忌裁决层

目标：

- 根据规则事实层生成完整宜忌

关键工作：

- 建立裁决优先级
- 实现冲突处理
- 增加 golden cases

## 推荐结论

优先顺序必须是：

1. `GB/T 33661-2017` 基础历法层
2. 《钦定协纪辨方书》规则事实层
3. 《钦定协纪辨方书》宜忌裁决层
4. `market-folk-v1` 的派生和展示优化

这能保证：

- 日子先算对
- 再判对
- 最后再谈“像挂历”

