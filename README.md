# skills

Unified monorepo for reusable agent skills.

## Overview

This repository consolidates multiple standalone skill projects into one place for easier maintenance, discovery, and release management.

Current imported projects:

- `skills/python-venv`
- `skills/structured-workflow`
- `skills/wsl-shell-reliability`

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
