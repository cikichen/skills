# skills

Unified monorepo for reusable agent skills.

## Overview

This repository consolidates multiple standalone skill projects into one place for easier maintenance, discovery, and release management.

Current imported projects:

- `skills/python-venv`
- `skills/structured-workflow`
- `skills/wsl-shell-reliability`

## Skill Capabilities (Detailed)

### 1) `python-venv`

Core capabilities:

- Enforces virtual environment usage when Python work requires third-party dependencies.
- Reuses existing environments first (`.venv`, `venv`, `env`, `.env`) before creating new ones.
- Supports explicit user choice when no environment exists: create local venv, use system Python, or custom path.
- Supports `uv` (preferred), standard `venv`, and Conda-based workflows.
- Allows stdlib-only one-liners without forcing venv.

Typical trigger conditions:

- Running Python scripts with third-party imports.
- `pip install` / `uv pip install` and dependency setup.
- Multi-file Python projects with dependency manifests.

Constraints / guardrails:

- Must check existing environments first, then reuse.
- Must ask user choice when no environment is found.
- Should not force venv for stdlib-only quick one-liners.

CN/EN citations:

- EN quote: "Before running Python scripts or installing packages, check for existing virtual environments and reuse them if found." (`skills/python-venv/SKILL.md`)
- ZH 引用: "安装包或使用第三方依赖时必须使用 venv" (`skills/python-venv/README_CN.md`)
- EN quote: "Skip venv for simple stdlib-only commands" (`skills/python-venv/README.md`)

### 2) `structured-workflow`

Core capabilities:

- Provides default always-on lightweight workflow rules.
- Enforces Simplified Chinese output and concise, conclusion-first responses.
- Standardizes execution order: plan concept -> review -> task breakdown.
- Keeps advanced architecture/process checklists in `references/` for on-demand loading.

Typical trigger conditions:

- Any general task that benefits from structured but low-overhead execution.
- Tasks requiring consistent response style and process sequencing.

Constraints / guardrails:

- Output language is fixed to Simplified Chinese.
- Favor KISS and factual corrections over verbosity.
- Detailed playbooks should be loaded on demand, not by default.

CN/EN citations:

- ZH 引用: "默认启用：中文输出、结构化流程、简洁优先。适用于所有任务。" (`skills/structured-workflow/SKILL.md`)
- ZH 引用: "执行顺序：构思方案 → 提请审核 → 分解任务。" (`skills/structured-workflow/SKILL.md`)
- EN quote (translated): "Default-on: Chinese output, structured process, concise-first; suitable for all tasks." (translated from `skills/structured-workflow/SKILL.md`)

### 3) `wsl-shell-reliability`

Core capabilities:

- Applies reliability-first shell selection for Windows execution paths.
- Chooses WSL/bash or PowerShell/CMD by task semantics and failure risk.
- Defines explicit fallback protocol while preserving command intent.
- Includes shell-aware generation rules and translation hints for common bash/PowerShell differences.

Typical trigger conditions:

- Any terminal execution task on Windows.
- POSIX-heavy commands with quoting/path fragility.
- Repeated command failures caused by shell mismatch.

Constraints / guardrails:

- Must not silently switch shells.
- Must preserve semantics during fallback translation.
- Must not enforce one-shell purity by installing unnecessary tools.

CN/EN citations:

- EN quote: "Choose WSL or PowerShell based on execution risk, not preference." (`skills/wsl-shell-reliability/SKILL.md`)
- EN quote: "This skill does not force WSL." (`skills/wsl-shell-reliability/SKILL.md`)
- ZH 引用: "根据任务语义与失败风险，在 WSL / PowerShell 间做可靠性优先选择。" (`skills/wsl-shell-reliability/README_CN.md`)

## External References (Bilingual)

- Python `venv` official docs / Python `venv` 官方文档: https://docs.python.org/3/library/venv.html
- Python packaging guide for venv / Python 打包与 venv 指南: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- WSL official docs (Microsoft Learn) / WSL 官方文档（Microsoft Learn）: https://learn.microsoft.com/windows/wsl/
- WSL troubleshooting / WSL 故障排查: https://learn.microsoft.com/windows/wsl/troubleshooting

## Repository Structure

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

## Add a New Skill Project

1. Create a new folder under `skills/` with a clear kebab-case name.
2. Include all required files listed in `docs/SKILL_REQUIREMENTS.md`.
3. Add bilingual docs when possible (`README.md` + `README_CN.md`).
4. Keep project-level license consistent (MIT recommended).

## Recommended Next Steps

- Add CI checks (structure + markdown/link validation)
- Add CODEOWNERS for per-skill ownership
- Standardize per-skill metadata format (`skill.json`/`manifest`)

## License

MIT. See [LICENSE](./LICENSE).
