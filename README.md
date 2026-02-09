# skills

[中文说明](README_CN.md)

Unified monorepo for reusable agent skills.

## Overview

This repository consolidates multiple standalone skill projects into one place for easier maintenance, discovery, and release management.

## Available Skills

| Skill | Description | Documentation |
|-------|-------------|---------------|
| **python-venv** | Python virtual environment management - enforces venv usage for projects with dependencies | [English](docs/skills/python-venv.md) · [中文](docs/skills/python-venv_CN.md) |
| **structured-workflow** | Lightweight structured workflow with Chinese output and KISS principles | [English](docs/skills/structured-workflow.md) |
| **wsl-shell-reliability** | Reliability-first shell selection for Windows (WSL/PowerShell) | [English](docs/skills/wsl-shell-reliability.md) · [中文](docs/skills/wsl-shell-reliability_CN.md) |

## Quick Start

### Installation

Each skill can be installed independently. See individual skill documentation for detailed installation instructions.

**General pattern for AI assistants:**

```bash
# OpenCode
cd ~/.config/opencode/skills
git clone <skill-repo-url> <skill-name>

# Claude Code
cd ~/.claude/skills
git clone <skill-repo-url> <skill-name>
```

### Usage

Skills are automatically loaded by compatible AI assistants. Each skill contains:
- `SKILL.md` - Core instruction file for AI agents
- `references/` - Supporting documentation and patterns

---

## Repository Structure

```text
skills/
  README.md                    # This file - overview and navigation
  README_CN.md                 # Chinese version
  LICENSE                      # MIT license
  .gitignore
  docs/
    SKILL_REQUIREMENTS.md      # Skill structure requirements
    skills/                    # Detailed skill documentation
      python-venv.md
      python-venv_CN.md
      structured-workflow.md
      wsl-shell-reliability.md
      wsl-shell-reliability_CN.md
  spec/
    agent-skills-spec.md       # Skill specification
  template/
    SKILL.md                   # Template for new skills
  skills/
    <skill-name>/
      SKILL.md                 # Core instruction for AI agents
      references/              # Supporting documentation
```

## Adding a New Skill

1. Create a new directory under `skills/` with a kebab-case name
2. Add `SKILL.md` with core instructions for AI agents
3. (Optional) Add `references/` directory for supporting docs
4. Create documentation in `docs/skills/<skill-name>.md`
5. Update this README to include the new skill in the table above

See [SKILL_REQUIREMENTS.md](docs/SKILL_REQUIREMENTS.md) for detailed requirements.

## Contributing

Contributions are welcome! Please ensure:
- Skills follow the structure defined in `docs/SKILL_REQUIREMENTS.md`
- Documentation is clear and includes examples
- Skills are tested with target AI assistants

## License

MIT - See [LICENSE](LICENSE) for details.
