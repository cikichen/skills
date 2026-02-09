# Agent Skills Spec

The official specification is maintained at: https://agentskills.io/specification

This document provides a summary of the Agent Skills format for quick reference.

## Directory Structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

Optional directories:
- `scripts/` - Executable code
- `references/` - Additional documentation
- `assets/` - Static resources (templates, images, data files)

## SKILL.md Format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown content.

### Required Frontmatter

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Optional Frontmatter Fields

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
compatibility: Requires git, docker, jq, and access to the internet
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

### Field Constraints

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, hyphens only. Must match directory name. |
| `description` | Yes | Max 1024 chars. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements. |
| `metadata` | No | Arbitrary key-value mapping. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental). |

### Body Content

The Markdown body contains skill instructions. No format restrictions.

Recommended sections:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

## Progressive Disclosure

Structure skills for efficient context use:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup
2. **Instructions** (< 5000 tokens recommended): Full `SKILL.md` loaded when activated
3. **Resources** (as needed): Files loaded only when required

Keep main `SKILL.md` under 500 lines. Move detailed reference material to separate files.

## File References

Use relative paths from skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

Keep file references one level deep from `SKILL.md`.

## Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) reference library:

```bash
skills-ref validate ./my-skill
```

## Full Specification

For the complete specification, visit: https://agentskills.io/specification
