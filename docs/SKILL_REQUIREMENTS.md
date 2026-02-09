# Skill Repository Requirements

This document defines the recommended **required** and **optional** files for each skill project under this monorepo.

## 1) Minimum Required (per skill project)

Assume a skill project path is `skills/<skill-name>/`.

- `SKILL.md`
  - Core skill instruction file for AI agents.
- `references/` (optional but recommended)
  - Supporting docs such as patterns, troubleshooting, scenarios.

**Note:** LICENSE, CHANGELOG.md, CONTRIBUTING.md, and .gitignore are managed at the repository level only.

## 2) Documentation Structure

**All skill documentation (README files) is centralized in `docs/skills/`:**

- `docs/skills/<skill-name>.md` - English documentation
- `docs/skills/<skill-name>_CN.md` - Chinese documentation (optional)

**Top-level README files (`README.md` and `README_CN.md`) serve as the unified entry point** for all skills.

## 3) Optional but Useful (per skill)

- `examples/` - Usage examples
- `tests/` - Validation scripts
- `meta/` - Manifest file (`skill.json`, etc.)

## 4) Naming Conventions

- Project directory: `kebab-case` (e.g. `wsl-shell-reliability`)
- Skill folder name should reflect skill identity (e.g. `python-venv`, `structured-workflow`)
- Documentation files in `docs/skills/`:
  - `<skill-name>.md` (EN)
  - `<skill-name>_CN.md` (ZH)

## 5) Current Structure

Imported projects in this monorepo:

1. `skills/python-venv`
2. `skills/structured-workflow`
3. `skills/wsl-shell-reliability`

All three follow the new structure:

- Each skill directory contains only: `SKILL.md` and `references/`
- All README documentation moved to `docs/skills/`
- Top-level README.md and README_CN.md provide comprehensive overview
- LICENSE, .gitignore managed at repository level

## 6) Benefits of This Structure

- **Minimal skill directories**: Only SKILL.md and references/
- **Centralized documentation**: All README files in one place (`docs/skills/`)
- **Unified entry point**: Top-level README serves as comprehensive guide
- **Easier maintenance**: Update documentation in one location
- **Better discoverability**: Users find all information in top-level README
- **Single source of truth**: LICENSE, CHANGELOG, CONTRIBUTING at repository level
