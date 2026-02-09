# skills

[English](README.md)

统一管理可复用 Agent Skill 的 Monorepo。

## 仓库说明

这个仓库把多个独立 skill 项目集中到同一处，便于统一维护、检索和发布。

当前已纳入的项目：

- `skills/python-venv`
- `skills/structured-workflow`
- `skills/wsl-shell-reliability`

---

## Skill 能力详解

### 1) `python-venv` — Python 虚拟环境管理

**核心能力：**

- 在需要第三方依赖时强制使用虚拟环境。
- 优先复用已有环境（`.venv`、`venv`、`env`、`.env`），避免重复创建。
- 当不存在环境时，明确询问用户选择：创建本地 venv、使用系统 Python 或自定义路径。
- 支持 `uv`（推荐）、标准 `venv` 和 Conda 工作流。
- 允许仅使用标准库的简单命令跳过 venv。

**典型触发条件：**

- 运行包含第三方导入的 Python 脚本。
- 执行 `pip install` / `uv pip install` 和依赖安装。
- 多文件 Python 项目，包含依赖清单。

**约束 / 护栏：**

- 必须先检查已有环境，然后复用。
- 当未找到环境时，必须询问用户选择。
- 不应对仅使用标准库的快速单行命令强制 venv。

**关键引用：**

> "安装包或使用第三方依赖时必须使用 venv"  
> — `skills/python-venv/README_CN.md`

> "Before running Python scripts or installing packages, check for existing virtual environments and reuse them if found."  
> — `skills/python-venv/SKILL.md`

> "Skip venv for simple stdlib-only commands"  
> — `skills/python-venv/README.md`

**何时需要 venv：**

| 场景 | 是否必需？ | 原因 |
|----------|-----------|--------|
| `pip install` / `uv pip install` | ✅ 是 | 安装包 |
| 运行包含第三方导入的 `.py` 文件 | ✅ 是 | 需要依赖 |
| 带 `requirements.txt` 的 `python script.py` | ✅ 是 | 项目依赖 |
| 多文件 Python 项目 | ✅ 是 | 需要隔离 |

**何时不需要 venv：**

| 场景 | 示例 |
|----------|---------|
| 简单的标准库单行命令 | `python3 -c "print('hello')"` |
| 仅使用内置模块 | `python3 -c "import json; ..."` |
| 版本检查 | `python3 --version` |

**项目类型检测：**

| 存在的文件 | 安装命令 |
|--------------|-----------------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `pip install -e .` 或 `uv pip install -e .` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` + `uv.lock` | `uv sync` |
| `setup.py` | `pip install -e .` |
| `Pipfile` | `pipenv install` |
| `environment.yml` | `conda env create -f environment.yml` |

**快速参考：**

| 任务 | Linux/macOS | Windows |
|------|-------------|---------|
| 创建 venv (uv) | `uv venv` | `uv venv` |
| 创建 venv (标准) | `python3 -m venv .venv` | `python -m venv .venv` |
| 激活 | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| 安装包 (uv) | `uv pip install <pkg>` | `uv pip install <pkg>` |
| 安装包 (pip) | `pip install <pkg>` | `pip install <pkg>` |
| 停用 | `deactivate` | `deactivate` |
| Conda 激活 | `conda activate <env>` | `conda activate <env>` |

---

### 2) `structured-workflow` — 轻量结构化工作流

**核心能力：**

- 提供默认启用的轻量工作流规则。
- 强制使用简体中文输出和简洁、结论优先的响应。
- 标准化执行顺序：构思方案 → 提请审核 → 分解任务。
- 将高级架构/流程检查清单保留在 `references/` 中，按需加载。

**典型触发条件：**

- 任何受益于结构化但低开销执行的通用任务。
- 需要一致响应风格和流程排序的任务。

**约束 / 护栏：**

- 输出语言固定为简体中文。
- 优先 KISS 和事实修正，避免冗长。
- 详细手册应按需加载，而非默认加载。

**关键引用：**

> "默认启用：中文输出、结构化流程、简洁优先。适用于所有任务。"  
> — `skills/structured-workflow/SKILL.md`

> "执行顺序：构思方案 → 提请审核 → 分解任务。"  
> — `skills/structured-workflow/SKILL.md`

**默认规则（来自 SKILL.md）：**

1. 全部使用简体中文。
2. 先结论，后要点；最小充分输出，避免冗余。
3. 执行顺序：构思方案 → 提请审核 → 分解任务。
4. 编码前先调研并澄清疑点。
5. 保持 KISS：优先简单、可维护方案，避免过度工程化。
6. 以事实为准；发现错误时直接指出并修正。
7. 所有输出（包括 Implementation Plan、Task List、Thought）必须使用中文。

**按需读取的参考资料：**

- 复杂架构与权衡：`references/architecture.md`
- 多步实施模板：`references/workflow.md`
- 质量门禁清单：`references/quality-gates.md`

---

### 3) `wsl-shell-reliability` — Windows 可靠性优先的 Shell 选择

**核心能力：**

- 为 Windows 执行路径应用可靠性优先的 shell 选择。
- 根据任务语义和失败风险在 WSL/bash 或 PowerShell/CMD 之间选择。
- 定义明确的回退协议，同时保留命令意图。
- 包含 shell 感知生成规则和常见 bash/PowerShell 差异的翻译提示。

**典型触发条件：**

- Windows 上的任何终端执行任务。
- 具有引号/路径脆弱性的 POSIX 重度命令。
- 由 shell 不匹配导致的重复命令失败。

**约束 / 护栏：**

- 不得静默切换 shell。
- 在回退翻译期间必须保留语义。
- 不得通过安装不必要的工具来强制单一 shell 纯度。

**关键引用：**

> "根据任务语义与失败风险，在 WSL / PowerShell 间做可靠性优先选择。"  
> — `skills/wsl-shell-reliability/README_CN.md`

> "Choose WSL or PowerShell based on execution risk, not preference."  
> — `skills/wsl-shell-reliability/SKILL.md`

> "This skill does not force WSL."  
> — `skills/wsl-shell-reliability/SKILL.md`

**单屏决策表：**

| 问题 | 如果是 | 如果否 |
| --- | --- | --- |
| Windows 原生任务/工具？ | 使用 **PowerShell/CMD** | 下一个问题 |
| 需要 POSIX/bash 语义？ | 使用 **WSL/bash** | 下一个问题 |
| 需要 Linux 优先的对等性？ | 优先 **WSL/bash** | 下一个问题 |
| Windows shell 解析风险高？ | 优先 **WSL/bash** | 下一个问题 |
| 两条路径风险都低？ | 选择移动部件更少的 shell | N/A |

**示例：**

- **Windows 原生：** `winget`、`reg`、`netsh`、`.exe/.msi`、服务/系统操作。
- **POSIX 重度：** `rm -rf`、`export`、`./script.sh`、`grep/sed/awk`、复杂管道。

**快速翻译提示（bash → PowerShell）：**

- `export FOO=bar` → `$env:FOO = "bar"`
- `rm -rf <path>` → `Remove-Item -Recurse -Force <path>`
- `cp -r a b` → `Copy-Item a b -Recurse`
- `mv a b` → `Move-Item a b`
- `cat file` → `Get-Content file`

**回退策略：**

在以下情况下回退到另一个 shell：

- WSL 不可用或不稳定，
- 工具无法在当前 shell 中解析，
- 任务明确是 Windows 原生的，
- 命令因 shell 解析/引号不匹配而失败。

回退时，报告：

1. 失败的内容，
2. shell 更改的原因，
3. 保留的等效命令意图。

---

## 外部参考资料（双语）

### Python 虚拟环境

- Python `venv` 官方文档: https://docs.python.org/3/library/venv.html
- Python 打包与 venv 指南: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- `uv` 文档: https://github.com/astral-sh/uv

### WSL (Windows Subsystem for Linux)

- WSL 官方文档（Microsoft Learn）: https://learn.microsoft.com/zh-cn/windows/wsl/
- WSL 故障排查: https://learn.microsoft.com/zh-cn/windows/wsl/troubleshooting

### 结构化工作流与最佳实践

- KISS 原则: https://zh.wikipedia.org/wiki/KISS%E5%8E%9F%E5%88%99
- 敏捷工作流模式: https://www.atlassian.com/zh/agile

---

## 目录结构

```text
skills/
  README.md                    # 统一入口（英文）
  README_CN.md                 # 统一入口（中文）
  LICENSE                      # 整个仓库的 MIT 许可证
  .gitignore
  docs/
    SKILL_REQUIREMENTS.md      # Skill 结构要求
    skills/                    # 集中式 skill 文档
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
      SKILL.md                 # AI agent 核心指令文件
      references/              # 支持文档
```

---

## 新增 Skill 项目建议流程

1. 在 `skills/` 下新建 kebab-case 命名的目录。
2. 按 `docs/SKILL_REQUIREMENTS.md` 补齐必备文件。
3. 尽量提供双语文档（`README.md` + `README_CN.md`）。
4. 统一许可证（推荐 MIT）。

---

## 建议后续补充

- 增加 CI 校验（结构校验 + Markdown/链接校验）
- 配置 CODEOWNERS 做分目录维护
- 统一 skill 元数据格式（如 `skill.json` / manifest）

---

## 许可证

MIT，详见 [LICENSE](./LICENSE)。
