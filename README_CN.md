# skills

[English](README.md)

统一管理可复用 Agent Skill 的 Monorepo。

## 项目简介

这个仓库把多个独立 skill 项目集中到同一处，便于统一维护、检索和发布。

## 可用的 Skills

| Skill | 描述 | 文档 |
|-------|------|------|
| **python-venv** | Python 虚拟环境管理 - 强制在有依赖的项目中使用 venv | [English](docs/skills/python-venv.md) · [中文](docs/skills/python-venv_CN.md) |
| **structured-workflow** | 轻量结构化工作流，中文输出和 KISS 原则 | [中文](docs/skills/structured-workflow.md) |
| **wsl-shell-reliability** | Windows 可靠性优先的 Shell 选择（WSL/PowerShell） | [English](docs/skills/wsl-shell-reliability.md) · [中文](docs/skills/wsl-shell-reliability_CN.md) |

## 快速开始

### 安装

每个 skill 可以独立安装。详细安装说明请参考各个 skill 的文档。

**AI 助手的通用安装模式：**

```bash
# OpenCode
cd ~/.config/opencode/skills
git clone <skill-repo-url> <skill-name>

# Claude Code
cd ~/.claude/skills
git clone <skill-repo-url> <skill-name>
```

### 使用

Skills 会被兼容的 AI 助手自动加载。每个 skill 包含：
- `SKILL.md` - AI agent 的核心指令文件
- `references/` - 支持文档和模式

## 添加新 Skill

1. 在 `skills/` 下创建 kebab-case 命名的新目录
2. 添加 `SKILL.md`，包含 AI agent 的核心指令
3. （可选）添加 `references/` 目录存放支持文档
4. 在 `docs/skills/<skill-name>.md` 创建文档
5. 更新本 README，在上面的表格中添加新 skill

详细要求请参考 [SKILL_REQUIREMENTS.md](docs/SKILL_REQUIREMENTS.md)。

## 贡献

欢迎贡献！请确保：
- Skills 遵循 `docs/SKILL_REQUIREMENTS.md` 中定义的结构
- 文档清晰并包含示例
- Skills 在目标 AI 助手中经过测试

## 许可证

MIT - 详见 [LICENSE](LICENSE)。
