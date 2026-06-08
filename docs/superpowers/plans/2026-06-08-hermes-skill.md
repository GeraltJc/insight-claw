# Hermes Skill 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 新增 `skills/hermes/SKILL.md`，让 Hermes Agent 能通过“分析 xx 股票”等自然语言请求运行 Insight Claw 本地股票分析流程。

**架构：** 第一版只创建一个单文件 skill，不新增 Python 代码、shell 脚本或运行时包装层。Hermes Agent 通过 `SKILL.md` 的 YAML frontmatter 发现触发场景，通过正文执行现有 `python -m justice_plutus run` CLI 并读取报告。

**技术栈：** Hermes Agent `SKILL.md` 格式、Markdown、Insight Claw Python CLI、Git。

---

## 文件结构

- 创建：`skills/hermes/SKILL.md`
  - 责任：定义 Hermes Agent 何时触发 Insight Claw 股票分析 skill，以及如何执行命令、读取报告、诊断失败。
- 不创建：`skills/hermes/references/`
  - 原因：第一版说明足够短，拆分会增加安装和维护成本。
- 不创建：`skills/hermes/scripts/`
  - 原因：仓库已经提供 `python -m justice_plutus run`，不需要额外包装脚本。

## Task 1: 创建 Hermes Agent Skill

**文件：**
- 创建：`skills/hermes/SKILL.md`

- [ ] **Step 1: 创建 skill 目录**

运行：

```bash
mkdir -p skills/hermes
```

预期：命令成功，`skills/hermes/` 存在。

- [ ] **Step 2: 写入 `SKILL.md`**

创建 `skills/hermes/SKILL.md`，内容如下：

```markdown
---
name: hermes
description: "Use when Hermes Agent receives a request to analyze A-share stocks with Insight Claw, including Chinese requests like 分析 600519 股票, 分析 贵州茅台, 分析 600519,000001, 生成这些 A 股的分析报告, or when the user asks to run local stock analysis and return generated reports."
---

# Insight Claw 股票分析

## 目标

使用当前 Insight Claw 项目的本地 CLI，为用户分析一个或多个 A 股标的，并返回生成报告中的关键结论。

这个 skill 给 Hermes Agent 使用。不要把它解释成项目内存在 `hermes` shell 命令，也不要默认启用项目里尚未完整接通的 Agent 模式。

## 触发场景

当用户表达以下意图时使用本 skill：

- “分析 600519 股票”
- “分析 贵州茅台”
- “分析 600519,000001”
- “用 Insight Claw 分析这些股票”
- “生成这些 A 股的分析报告”
- “跑一下我的自选股分析”

如果用户只是询问项目架构、配置说明或代码实现，不要运行分析命令；先回答问题或检查相关文件。

## 前置检查

1. 确认当前工作目录是 Insight Claw 仓库根目录。仓库根目录应包含 `justice_plutus/cli.py`、`src/core/pipeline.py` 和 `README.md`。
2. 确认用户提供了股票代码或股票名称。
3. 确认可用的 Python 环境能导入项目依赖。
4. 确认至少配置一种 LLM key 路径，例如 `OPENAI_API_KEY`、`AIHUBMIX_KEY`、`GEMINI_API_KEY`、`ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY`。

缺少 `TUSHARE_TOKEN`、`BOCHA_API_KEYS`、`TAVILY_API_KEYS`、`SERPAPI_API_KEYS`、`WENCAI_COOKIE` 或 iFinD 相关变量时，不要直接阻塞基础分析；这些是增强能力。

## 股票输入处理

优先使用用户明确给出的 6 位 A 股代码。多个代码用英文逗号连接，例如：

```text
600519,000001
```

如果用户给的是股票名称，先尝试在项目的股票映射或已有数据源中找到对应代码。无法确认代码时，向用户询问，不要猜测。

## 默认执行命令

默认只生成本地报告，不发送通知：

```bash
python -m justice_plutus run --stocks "<codes>" --no-notify
```

示例：

```bash
python -m justice_plutus run --stocks "600519" --no-notify
```

批量示例：

```bash
python -m justice_plutus run --stocks "600519,000001" --no-notify
```

如果用户明确要求推送、发送通知、发送到飞书、Telegram 或其它已配置渠道，去掉 `--no-notify`：

```bash
python -m justice_plutus run --stocks "<codes>"
```

## 报告读取

命令完成后，检查最新的 `reports/YYYY-MM-DD/` 输出目录。

优先读取：

```text
reports/YYYY-MM-DD/summary.md
```

用户要求单股细节时，再读取：

```text
reports/YYYY-MM-DD/stocks/<code>.md
```

回复用户时包含：

- 股票代码和股票名称
- 核心结论
- 操作建议
- 主要风险
- 报告文件路径

不要编造报告中不存在的价格、评分、建议或数据源。

## 错误处理

如果命令失败，报告以下信息：

1. 失败命令
2. 关键错误行
3. 最可能原因
4. 下一步修复方式

常见处理：

- `ModuleNotFoundError`：提示用户安装项目依赖。
- “未提供股票列表”：要求用户提供股票代码或配置 `STOCK_LIST`。
- LLM key 缺失：提示至少配置一种 LLM key。
- 数据源失败：说明可能仍可生成降级报告，并检查报告目录是否已有输出。
- 报告目录不存在：说明 CLI 未成功生成报告，保留错误输出供用户排查。
- 通知失败：说明本地报告是否已生成，并提示检查对应通知环境变量。

## Agent 模式边界

不要默认设置：

```bash
AGENT_MODE=true
```

当前仓库存在 Agent 模式相关分支，但完整 executor 不在当前代码树中。除非仓库后续补齐 Hermes 或 Agent executor，并且用户明确要求测试高级 Agent 模式，否则始终使用 `python -m justice_plutus run` 本地 CLI。
```

预期：文件存在，frontmatter 只有 `name` 和 `description` 两个字段。

- [ ] **Step 3: 检查文件内容**

运行：

```bash
sed -n '1,240p' skills/hermes/SKILL.md
```

预期：输出完整 skill 内容；正文明确写给 Hermes Agent 使用，没有把 Codex 写成运行者。

## Task 2: 校验 Skill 格式和边界

**文件：**
- 验证：`skills/hermes/SKILL.md`

- [ ] **Step 1: 检查 frontmatter 字段**

运行：

```bash
sed -n '1,8p' skills/hermes/SKILL.md
```

预期输出开头包含：

```markdown
---
name: hermes
description: "Use when Hermes Agent receives a request to analyze A-share stocks with Insight Claw, including Chinese requests like 分析 600519 股票, 分析 贵州茅台, 分析 600519,000001, 生成这些 A 股的分析报告, or when the user asks to run local stock analysis and return generated reports."
---
```

- [ ] **Step 2: 检查禁止默认 Agent 模式**

运行：

```bash
rg -n "AGENT_MODE=true|hermes shell|Codex|python -m justice_plutus run" skills/hermes/SKILL.md
```

预期：

- `AGENT_MODE=true` 只出现在“不要默认设置”的边界说明中。
- `hermes shell` 只出现在“不要解释成项目内存在命令”的边界说明中。
- 不出现 `Codex`。
- 至少出现一次 `python -m justice_plutus run`。

- [ ] **Step 3: 运行可用的 skill 校验工具**

运行：

```bash
python /Users/jc/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/hermes
```

预期：校验通过。如果本机没有该工具或 Hermes 不需要 Codex 校验器，则至少保留前两步的结构校验结果。

## Task 3: 提交实现

**文件：**
- 提交：`skills/hermes/SKILL.md`

- [ ] **Step 1: 查看工作区**

运行：

```bash
git status --short
```

预期：只看到 `?? skills/hermes/SKILL.md`，或者只看到与本任务直接相关的文件。

- [ ] **Step 2: 暂存 skill 文件**

运行：

```bash
git add skills/hermes/SKILL.md
```

预期：暂存成功。

- [ ] **Step 3: 提交**

运行：

```bash
git commit -m "新增 Hermes 股票分析 skill"
```

预期：提交成功，提交内容只包含 `skills/hermes/SKILL.md`。

## 自检

- 规格覆盖：计划创建 `skills/hermes/SKILL.md`，覆盖触发、执行、配置、边界、错误处理、验证要求。
- 占位符检查：计划没有 `TBD`、`TODO` 或“稍后实现”。
- 类型和命令一致性：计划中的运行命令统一使用当前仓库真实入口 `python -m justice_plutus run --stocks ...`。

