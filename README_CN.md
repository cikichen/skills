# skills

统一管理可复用 Agent Skill 的 Monorepo。

## 仓库说明

这个仓库把多个独立 skill 项目集中到同一处，便于统一维护、检索和发布。

当前已纳入的项目：

- `skills/python-venv`
- `skills/structured-workflow`
- `skills/wsl-shell-reliability`

## 目录结构

```text
skills/
  README.md
  README_CN.md
  LICENSE
  docs/
    SKILL_REQUIREMENTS.md
  spec/
    agent-skills-spec.md
  template/
    SKILL.md
  skills/
    <skill-name>/
      SKILL.md
      references/
      README.md
      LICENSE
```

## 新增 Skill 项目建议流程

1. 在 `skills/` 下新建 kebab-case 命名的目录。
2. 按 `docs/SKILL_REQUIREMENTS.md` 补齐必备文件。
3. 尽量提供双语文档（`README.md` + `README_CN.md`）。
4. 统一许可证（推荐 MIT）。

## 建议后续补充

- 增加 CI 校验（结构校验 + Markdown/链接校验）
- 配置 CODEOWNERS 做分目录维护
- 统一 skill 元数据格式（如 `skill.json` / manifest）

## 许可证

MIT，详见 [LICENSE](./LICENSE)。
