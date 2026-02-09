# structured-workflow（轻量版）

面向“默认触发”场景的低 token 技能：

- 元数据高召回（适用于所有任务）
- 正文极简（常驻规则最小化）
- 复杂细则外置到 `references/` 按需读取

## 目录结构

```text
structured-workflow-skill/
├─ structured-workflow/
│  ├─ SKILL.md
│  └─ references/
│     ├─ architecture.md
│     ├─ workflow.md
│     └─ quality-gates.md
├─ README.md
└─ LICENSE
```

## 设计目标

1. 保持“每次可触发”能力。
2. 降低默认上下文占用。
3. 仅在复杂任务时加载详细规则。

## 默认规则（来自 SKILL.md）

- 全部使用简体中文
- 先结论后要点，最小充分输出
- 顺序：构思方案 → 提请审核 → 分解任务
- 编码前先调研并澄清疑点
- KISS：简单优先、可维护优先
- 事实优先，发现错误直接修正
- 固定指令仅在用户明确要求时输出

## 兼容性

- OpenCode
- Claude Code
