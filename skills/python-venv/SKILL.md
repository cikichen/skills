---
name: python-venv
description: "Python 环境管理技能。自动检测项目类型和现有环境，按流行度优先级推荐方案。尽量减少用户干扰，只在必要时才询问。"
---

# Python 环境管理技能

## 核心原则

1. **现有环境优先** - 复用已有的虚拟环境，不重复创建
2. **项目类型明确时直接使用** - 根据 lock 文件自动选择
3. **按流行度推荐** - uv > pip > conda > venv
4. **尽量不打扰用户** - 只有必要时才询问

---

## 工具流行度排名

| 优先级 | 工具 | 适用场景 |
|--------|------|----------|
| 🥇 | uv | 新项目、快速安装 |
| 🥈 | pip | 兼容性优先 |
| 🥉 | conda | 数据科学、特定版本需求 |
| 4 | venv | 标准库、无需额外安装 |
| 5 | poetry | 已有 poetry.lock |
| 6 | pipenv | 已有 Pipfile（逐渐淘汰） |

---

## 决策流程

```
┌─────────────────────────────────────┐
│  检测项目依赖文件                     │
└─────────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  明确方案            无法判断
    ↓                   ↓
  直接使用         检测现有环境
                        ↓
                  ┌─────┴─────┐
                  ↓           ↓
              有环境        无环境
                  ↓           ↓
              直接复用      评估复杂度
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
              简单任务          需安装依赖
                  ↓                   ↓
            系统 Python        推荐 uv/conda
```

---

## 1. 明确方案（直接执行，不询问）

检测到以下文件时，直接使用对应工具：

| 检测文件 | 直接执行 |
|---------|----------|
| `uv.lock` 存在 | `uv sync` 或 `uv pip install -r requirements.txt` |
| `poetry.lock` 存在 | `poetry install` |
| `environment.yml` 存在 | `conda env create -f environment.yml` |
| `Pipfile.lock` 存在 | `pipenv install` |

---

## 2. 检测现有环境（复用优先）

```bash
# 优先级：uv venv > conda > venv

# 2.1 检测 uv 虚拟环境
ls -la .venv/ 2>/dev/null && uv pip list 2>/dev/null | head -3

# 2.2 检测 conda 环境
conda info --envs 2>/dev/null | grep "*" || echo $CONDA_PREFIX

# 2.3 检测标准 venv
ls -la venv/ .venv/ env/ 2>/dev/null

# 2.4 如果有 → 直接复用（激活后执行命令）
```

**复用现有环境示例：**
```
检测到现有 .venv/ 目录
→ 激活: source .venv/bin/activate
→ 执行: uv pip install <package>
```

---

## 3. 无法判断时（评估复杂度）

| 场景 | 处理方式 |
|------|----------|
| 纯标准库、无第三方依赖 | 系统 Python（python3） |
| 简单 pip install 测试 | 系统 Python（临时） |
| 有 requirements.txt | 推荐 uv > pip > venv |
| 有 pyproject.toml | 推荐 uv > pip |
| 多文件项目、需要隔离 | 推荐 uv |

---

## 4. 何时询问用户（仅限这些情况）

✅ **要问：**
1. 空项目 + 首次安装依赖 → 问用哪个工具
2. 同时存在 requirements.txt + pyproject.toml → 问用哪个
3. 用户明确要求换方案 → 如"我想用 conda"

❌ **不要问：**
- 已有 uv.lock 但用户没指定
- 已有 .venv/ 目录
- 普通 pip install 任务

---

## 5. 推荐方案（无明确指示时）

```
首选: uv
  ├── uv venv (创建)
  ├── uv pip install (安装)
  └── uv sync (同步)

备选: pip
  ├── python3 -m venv .venv
  └── pip install

特殊: conda
  ├── conda create -n envname python=x.x
  └── conda env create
```

---

## 检测命令速查

```bash
# 检测可用工具
which uv
which conda
which pip
which python3

# 检测项目文件
ls -la *.lock pyproject.toml requirements.txt environment.yml Pipfile 2>/dev/null

# 检测现有环境
ls -la .venv/ venv/ env/ 2>/dev/null
conda info --envs 2>/dev/null

# 检测当前环境
echo $VIRTUAL_ENV
echo $CONDA_PREFIX
```

---

## 交互提示示例（仅必要时）

```
🔍 检测结果：
- 项目文件: pyproject.toml
- 现有环境: 无
- 推荐方案: uv (最快)

直接执行: uv pip install <package>
```

```
🔍 检测结果：
- 项目文件: requirements.txt
- 现有环境: 无
- 推荐方案: uv

可选方案：
1) uv (推荐) - 更快
2) pip - 兼容性更好
3) venv - 使用标准库
4) conda - 如果需要特定版本

请输入选项或直接回车使用推荐方案：
```

---

## 快速命令参考

| 操作 | uv | pip | conda | venv |
|------|-----|-----|------|------|
| 创建环境 | `uv venv` | - | `conda create` | `python3 -m venv` |
| 安装包 | `uv pip install` | `pip install` | `conda install` | `pip install` |
| 安装依赖 | `uv sync` | `pip install -r` | `conda env create` | `pip install -r` |
| 激活 | (自动) | (自动) | `conda activate` | `source venv/bin/activate` |

---

## 核心原则

**"少问多做"** - 能判断的直接执行，只在无法判断时询问。
