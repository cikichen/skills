# skills

[中文说明](README_CN.md)

Unified monorepo for reusable agent skills.

## Overview

This repository consolidates multiple standalone skill projects into one place for easier maintenance, discovery, and release management.

Current imported projects:

- `skills/python-venv`
- `skills/structured-workflow`
- `skills/wsl-shell-reliability`

---

## Skill Capabilities (Detailed)

### 1) `python-venv` — Python Virtual Environment Management

**Core capabilities:**

- Enforces virtual environment usage when Python work requires third-party dependencies.
- Reuses existing environments first (`.venv`, `venv`, `env`, `.env`) before creating new ones.
- Supports explicit user choice when no environment exists: create local venv, use system Python, or custom path.
- Supports `uv` (preferred), standard `venv`, and Conda-based workflows.
- Allows stdlib-only one-liners without forcing venv.

**Typical trigger conditions:**

- Running Python scripts with third-party imports.
- `pip install` / `uv pip install` and dependency setup.
- Multi-file Python projects with dependency manifests.

**Constraints / guardrails:**

- Must check existing environments first, then reuse.
- Must ask user choice when no environment is found.
- Should not force venv for stdlib-only quick one-liners.

**Key citations:**

> "Before running Python scripts or installing packages, check for existing virtual environments and reuse them if found."  
> — `skills/python-venv/SKILL.md`

> "Skip venv for simple stdlib-only commands"  
> — `skills/python-venv/README.md`

**When venv is Required:**

| Scenario | Required? | Reason |
|----------|-----------|--------|
| `pip install` / `uv pip install` | ✅ YES | Installing packages |
| Running `.py` files with third-party imports | ✅ YES | Needs dependencies |
| `python script.py` with `requirements.txt` | ✅ YES | Project dependencies |
| Multi-file Python projects | ✅ YES | Isolation needed |

**When venv is NOT Required:**

| Scenario | Example |
|----------|---------|
| Simple stdlib one-liner | `python3 -c "print('hello')"` |
| Built-in modules only | `python3 -c "import json; ..."` |
| Version check | `python3 --version` |

**Project Type Detection:**

| File Present | Install Command |
|--------------|-----------------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `pip install -e .` or `uv pip install -e .` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` + `uv.lock` | `uv sync` |
| `setup.py` | `pip install -e .` |
| `Pipfile` | `pipenv install` |
| `environment.yml` | `conda env create -f environment.yml` |

**Quick Reference:**

| Task | Linux/macOS | Windows |
|------|-------------|---------|
| Create venv (uv) | `uv venv` | `uv venv` |
| Create venv (standard) | `python3 -m venv .venv` | `python -m venv .venv` |
| Activate | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| Install package (uv) | `uv pip install <pkg>` | `uv pip install <pkg>` |
| Install package (pip) | `pip install <pkg>` | `pip install <pkg>` |
| Deactivate | `deactivate` | `deactivate` |
| Conda activate | `conda activate <env>` | `conda activate <env>` |

---

### 2) `structured-workflow` — Lightweight Structured Workflow

**Core capabilities:**

- Provides default always-on lightweight workflow rules.
- Enforces Simplified Chinese output and concise, conclusion-first responses.
- Standardizes execution order: plan concept → review → task breakdown.
- Keeps advanced architecture/process checklists in `references/` for on-demand loading.

**Typical trigger conditions:**

- Any general task that benefits from structured but low-overhead execution.
- Tasks requiring consistent response style and process sequencing.

**Constraints / guardrails:**

- Output language is fixed to Simplified Chinese.
- Favor KISS and factual corrections over verbosity.
- Detailed playbooks should be loaded on demand, not by default.

**Key citations:**

> "默认启用：中文输出、结构化流程、简洁优先。适用于所有任务。"  
> — `skills/structured-workflow/SKILL.md`

> "执行顺序：构思方案 → 提请审核 → 分解任务。"  
> — `skills/structured-workflow/SKILL.md`

**Default Rules (from SKILL.md):**

1. 全部使用简体中文。
2. 先结论，后要点；最小充分输出，避免冗余。
3. 执行顺序：构思方案 → 提请审核 → 分解任务。
4. 编码前先调研并澄清疑点。
5. 保持 KISS：优先简单、可维护方案，避免过度工程化。
6. 以事实为准；发现错误时直接指出并修正。
7. 所有输出（包括 Implementation Plan、Task List、Thought）必须使用中文。

**On-demand references:**

- Complex architecture & tradeoffs: `references/architecture.md`
- Multi-step implementation template: `references/workflow.md`
- Quality gate checklist: `references/quality-gates.md`

---

### 3) `wsl-shell-reliability` — Reliability-First Shell Selection for Windows

**Core capabilities:**

- Applies reliability-first shell selection for Windows execution paths.
- Chooses WSL/bash or PowerShell/CMD by task semantics and failure risk.
- Defines explicit fallback protocol while preserving command intent.
- Includes shell-aware generation rules and translation hints for common bash/PowerShell differences.

**Typical trigger conditions:**

- Any terminal execution task on Windows.
- POSIX-heavy commands with quoting/path fragility.
- Repeated command failures caused by shell mismatch.

**Constraints / guardrails:**

- Must not silently switch shells.
- Must preserve semantics during fallback translation.
- Must not enforce one-shell purity by installing unnecessary tools.

**Key citations:**

> "Choose WSL or PowerShell based on execution risk, not preference."  
> — `skills/wsl-shell-reliability/SKILL.md`

> "This skill does not force WSL."  
> — `skills/wsl-shell-reliability/SKILL.md`

**One-screen decision table:**

| Question | If Yes | If No |
| --- | --- | --- |
| Windows-native task/tool? | Use **PowerShell/CMD** | Next question |
| POSIX/bash semantics required? | Use **WSL/bash** | Next question |
| Need Linux-first parity? | Prefer **WSL/bash** | Next question |
| High Windows-shell parse risk? | Prefer **WSL/bash** | Next question |
| Both paths low risk? | Pick shell with fewer moving parts | N/A |

**Examples:**

- **Windows-native:** `winget`, `reg`, `netsh`, `.exe/.msi`, service/system ops.
- **POSIX-heavy:** `rm -rf`, `export`, `./script.sh`, `grep/sed/awk`, complex pipes.

**Quick translation hints (bash → PowerShell):**

- `export FOO=bar` → `$env:FOO = "bar"`
- `rm -rf <path>` → `Remove-Item -Recurse -Force <path>`
- `cp -r a b` → `Copy-Item a b -Recurse`
- `mv a b` → `Move-Item a b`
- `cat file` → `Get-Content file`

**Fallback policy:**

Fallback to the other shell when:

- WSL is unavailable or unstable,
- the tool cannot be resolved in current shell,
- task is clearly Windows-native,
- command fails due to shell parsing/quoting mismatch.

When falling back, report:

1. what failed,
2. why shell changed,
3. equivalent command intent preserved.

---

## External References (Bilingual)

### Python Virtual Environment

- Python `venv` official docs: https://docs.python.org/3/library/venv.html
- Python packaging guide for venv: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- `uv` documentation: https://github.com/astral-sh/uv

### WSL (Windows Subsystem for Linux)

- WSL official docs (Microsoft Learn): https://learn.microsoft.com/windows/wsl/
- WSL troubleshooting: https://learn.microsoft.com/windows/wsl/troubleshooting

### Structured Workflow & Best Practices

- KISS principle: https://en.wikipedia.org/wiki/KISS_principle
- Agile workflow patterns: https://www.atlassian.com/agile

---

## Repository Structure

```text
skills/
  README.md                    # Unified entry point (English)
  README_CN.md                 # Unified entry point (Chinese)
  LICENSE                      # MIT license for entire repository
  .gitignore
  docs/
    SKILL_REQUIREMENTS.md      # Skill structure requirements
    skills/                    # Centralized skill documentation
      python-venv.md
      python-venv_CN.md
      structured-workflow.md
      wsl-shell-reliability.md
      wsl-shell-reliability_CN.md
  spec/
    agent-skills-spec.md
  template/
    SKILL.md
  skills/
    <skill-name>/
      SKILL.md                 # Core skill instruction for AI agents
      references/              # Supporting documentation
```

---

## Add a New Skill Project

1. Create a new folder under `skills/` with a clear kebab-case name.
2. Include all required files listed in `docs/SKILL_REQUIREMENTS.md`.
3. Add bilingual docs when possible (`README.md` + `README_CN.md`).
4. Keep project-level license consistent (MIT recommended).

---

## Recommended Next Steps

- Add CI checks (structure + markdown/link validation)
- Add CODEOWNERS for per-skill ownership
- Standardize per-skill metadata format (`skill.json`/`manifest`)

---

## License

MIT. See [LICENSE](./LICENSE).
