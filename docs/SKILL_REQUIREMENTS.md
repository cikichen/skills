# Skill Repository Requirements

This document defines the recommended **required** and **optional** files for each skill project under this monorepo.

## 1) Minimum Required (per skill project)

Assume a skill project path is `skills/<project-name>/`.

- `README.md`
  - English intro, purpose, usage, examples.
- `LICENSE`
  - MIT recommended.
- `<skill-folder>/SKILL.md`
  - Core skill instruction file.

## 2) Strongly Recommended

- `README_CN.md`
  - Chinese documentation for local team usage.
- `<skill-folder>/references/`
  - Supporting docs such as patterns, troubleshooting, scenarios.
- `CHANGELOG.md`
  - Track notable updates.
- `CONTRIBUTING.md`
  - Contribution rules.

## 3) Optional but Useful

- `.gitignore`
- `examples/`
- `tests/` or validation scripts
- `meta/` or manifest file (`skill.json`, etc.)

## 4) Naming Conventions

- Project directory: `kebab-case` (e.g. `wsl-terminal-skill`)
- Skill folder name should reflect skill identity (e.g. `python-venv`, `structured-workflow`)
- Docs filenames:
  - `README.md` (EN)
  - `README_CN.md` (ZH)

## 5) Current Imported Projects Check

Imported projects in this monorepo:

1. `skills/skill-python-venv`
2. `skills/structured-workflow-skill`
3. `skills/wsl-terminal-skill`

All three currently include:

- `README.md`
- `LICENSE`
- skill core folder with `SKILL.md`

Partial coverage:

- `README_CN.md`: present in project 1 and 3, missing in project 2
- `CHANGELOG.md` / `CONTRIBUTING.md`: present in project 3 only

## 6) Suggested Normalization Actions

- Add `README_CN.md` to `structured-workflow-skill`
- Decide whether all projects should include `CHANGELOG.md` + `CONTRIBUTING.md`
- Optionally define a unified manifest schema for discovery
