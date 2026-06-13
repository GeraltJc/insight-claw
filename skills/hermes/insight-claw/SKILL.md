---
name: insight-claw
description: Download, configure, run, verify, and troubleshoot Insight Claw from OpenClaw or Hermes, producing A-share self-selected stock analysis reports through the local JusticePlutus CLI.
version: 0.2.0
author: GeraltJc
license: MIT-0
platforms: [macos, linux]
compatibility: Cross-platform macOS/Linux skill for shell-capable OpenClaw and Hermes hosts. Requires git, Python 3.11+, pip, venv, network access, and at least one OpenAI-compatible LLM key for real structured analysis.
allowed-tools: Bash Read
metadata:
  hermes:
    tags: [Finance, A-Share, CLI, Analysis, Automation]
    related_skills: []
    config:
      - key: insight-claw.repo_dir
        description: Local directory where the Insight Claw repository should be cloned or reused.
        default: "~/insight-claw"
        prompt: Insight Claw repository directory
      - key: insight-claw.default_stocks
        description: Default self-selected stocks for first validation runs.
        default: "000001,600519"
        prompt: Default stock codes for Insight Claw validation
  openclaw:
    emoji: "📈"
    homepage: https://github.com/GeraltJc/insight-claw/tree/main/skills/hermes/insight-claw
    requires:
      bins:
        - git
        - python
    primaryEnv: AIHUBMIX_KEY
    envVars:
      - name: AIHUBMIX_KEY
        required: false
        description: Recommended OpenAI-compatible AIHubMix key for structured analysis.
      - name: OPENAI_API_KEY
        required: false
        description: OpenAI-compatible API key used as primary or fallback LLM credential.
      - name: OPENAI_BASE_URL
        required: false
        description: Optional OpenAI-compatible base URL.
      - name: OPENAI_MODEL
        required: false
        description: Optional model name for structured analysis.
      - name: BOCHA_API_KEYS
        required: false
        description: Optional search intelligence provider key list.
      - name: TAVILY_API_KEYS
        required: false
        description: Optional search intelligence provider key list.
      - name: SERPAPI_API_KEYS
        required: false
        description: Optional search intelligence provider key list.
      - name: TUSHARE_TOKEN
        required: false
        description: Optional market data enhancement token.
      - name: ENABLE_CHIP_DISTRIBUTION
        required: false
        description: Optional switch for chip distribution enrichment.
      - name: WENCAI_COOKIE
        required: false
        description: Optional chip distribution provider credential.
      - name: HSCLOUD_AUTH_TOKEN
        required: false
        description: Optional chip distribution provider credential.
      - name: IFIND_REFRESH_TOKEN
        required: false
        description: Optional TongHuaShun professional data credential.
      - name: ENABLE_THS_PRO_DATA
        required: false
        description: Optional switch for TongHuaShun professional data mode.
      - name: ENABLE_IFIND_ANALYSIS_ENHANCEMENT
        required: false
        description: Optional switch for iFinD-enhanced structured analysis.
      - name: TELEGRAM_BOT_TOKEN
        required: false
        description: Optional Telegram notification credential.
      - name: TELEGRAM_CHAT_ID
        required: false
        description: Optional Telegram notification target.
      - name: FEISHU_WEBHOOK_URL
        required: false
        description: Optional Feishu notification webhook.
required_environment_variables:
  - name: AIHUBMIX_KEY
    prompt: AIHubMix API key
    help: Configure this when using the recommended OpenAI-compatible AIHubMix path.
    required_for: LLM structured analysis
  - name: OPENAI_API_KEY
    prompt: OpenAI-compatible API key
    help: Configure this as the primary key or as fallback when AIHUBMIX_KEY is not available.
    required_for: LLM structured analysis
---
# Insight Claw

Insight Claw 是面向 A 股自选股的自动化自选股分析流水线。它围绕一组自选股收集行情数据、筹码分布和搜索情报，调用模型生成结构化分析，最终产出可保存或推送的决策结果。

## When to Use

Use this skill when a user wants OpenClaw or Hermes to download, configure, run, verify, or troubleshoot Insight Claw.

## Host Compatibility

This is a shell-based skill for agent hosts that can run local commands. It follows the same operational path in OpenClaw and Hermes:

1. Reuse an existing Insight Claw checkout when one is present.
2. Clone `https://github.com/GeraltJc/insight-claw` only for first-time setup.
3. Create or reuse `.venv`.
4. Run the local JusticePlutus CLI with a temporary `--stocks` self-selected stock override.

Use OpenClaw for ClawHub installation and updates. Use Hermes when the user has already installed this skill in a Hermes skill path. Do not mix host-specific install flows in one turn; pick the host the user is actually using, then run the same local validation command.

## Quick Reference

Insight Claw is an A-share self-selected stock analysis pipeline.

For expanded commands, environment examples, GitHub Actions setup, and troubleshooting details, read:

- `references/quickstart.md`
- `references/troubleshooting.md`

| Task | Command |
| --- | --- |
| Download | `git clone https://github.com/GeraltJc/insight-claw.git insight-claw` |
| Create environment | `python -m venv .venv` |
| Install dependencies | `.venv/bin/python -m pip install -r requirements.txt` (`pip install -r requirements.txt` inside the activated environment) |
| First validation | `.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify` |

If the user is already inside an Insight Claw checkout, reuse it instead of cloning a duplicate repository.

## OpenClaw Installation

After this skill is published on ClawHub, OpenClaw users can install it from the registry:

```bash
openclaw skills search insight-claw
openclaw skills install insight-claw
```

For local development before publication, point OpenClaw at this folder or copy the folder into the active OpenClaw skills directory. The skill bundle is this directory only: `SKILL.md` plus `references/`.

OpenClaw metadata lives under `metadata.openclaw`. Optional provider keys are declared with `envVars` instead of `requires.env` because Insight Claw can run with either `AIHUBMIX_KEY` or `OPENAI_API_KEY`, and search, chip distribution, 同花顺专业数据模式, and notifications are enhancement paths rather than mandatory setup.

## Execution Contract

OpenClaw and Hermes should not clone and reinstall on every request. Use this decision flow:

### First-time setup

Run these commands only when the Insight Claw repository or `.venv` environment is missing:

```bash
git clone https://github.com/GeraltJc/insight-claw.git insight-claw
cd insight-claw
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

### Subsequent runs

When the repository and `.venv` already exist, run only the analysis command:

```bash
cd insight-claw
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Reinstall dependencies only after project updates, `requirements.txt` changes, or virtual environment failure.

## Runtime Requirements

Before running Insight Claw, confirm these requirements:

- Python 3.11+
- `git`
- `pip`
- `venv`
- Network access for dependency installation and configured data, search, LLM, or notification providers.
- At least one LLM key for real structured analysis. Prefer `AIHUBMIX_KEY`; use `OPENAI_API_KEY` as fallback or primary key when appropriate.

## Procedure

Follow the common local setup path first.

1. Locate an existing checkout by looking for `justice_plutus/`, `src/`, and `requirements.txt` in the working tree.
2. If no checkout exists, ask where the user wants the project stored, then download it from `https://github.com/GeraltJc/insight-claw` with `git clone`.
3. Change into the repository directory.
4. Create an isolated Python environment with `python -m venv .venv`.
5. Install dependencies with `pip install -r requirements.txt` from inside the isolated environment.
6. Configure at least one LLM key path before a real analysis run. Prefer `AIHUBMIX_KEY` with OpenAI-compatible settings, or use `OPENAI_API_KEY` as fallback.
7. Run the first validation without notifications:

```bash
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Equivalent command after activating the virtual environment:

```bash
python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Use `--stocks` for a temporary self-selected stock override. It does not mutate the persistent `STOCK_LIST` configuration.

## Configuration

Keep configuration layered so the first run stays small:

| Layer | Variables | Purpose |
| --- | --- | --- |
| Required LLM path | `AIHUBMIX_KEY`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` | Enables structured analysis and decision result generation. At least one usable key path is needed for real analysis. |
| Search enhancement | `BOCHA_API_KEYS`, `TAVILY_API_KEYS`, `SERPAPI_API_KEYS` | Adds search intelligence for risks, news, performance expectations, and industry context. Missing providers should degrade rather than block the whole pipeline. |
| Market data enhancement | `TUSHARE_TOKEN` | Improves行情数据 coverage. If unavailable, Insight Claw can continue through its data-source degradation chain where supported. |
| Chip distribution | `ENABLE_CHIP_DISTRIBUTION`, `WENCAI_COOKIE`, `HSCLOUD_AUTH_TOKEN` | Enables optional 筹码分布. Missing chip data should not stop the self-selected stock analysis pipeline. |
| TongHuaShun professional mode | `IFIND_REFRESH_TOKEN`, `ENABLE_THS_PRO_DATA`, `ENABLE_IFIND_ANALYSIS_ENHANCEMENT` | Enables optional 同花顺专业数据模式 for richer professional data. |
| Notification channels | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `FEISHU_WEBHOOK_URL` | Sends notification messages after reports are generated. Configure only after local no-notification validation passes. |

Use project terms consistently when explaining results:

- `行情数据`: historical daily bars and real-time quote facts.
- `搜索情报`: open search context used to enrich model input.
- `结构化分析`: model output in a parseable decision schema.
- `决策结果`: user-facing conclusion, risk, and action context.
- `分析报告`: local persisted report files.
- `批次汇总`: overview across all self-selected stocks in one run.
- `通知消息`: Telegram, Feishu, or another outbound message shape.
- `降级链`: the ordered fallback behavior for data sources, model routes, and notification outputs.

## Verification

Confirm that a no-notification validation run completes and produces reports:

- `reports/YYYY-MM-DD/stocks/<code>.md`
- `reports/YYYY-MM-DD/stocks/<code>.json`
- `reports/YYYY-MM-DD/summary.md`
- `reports/YYYY-MM-DD/summary.json`
- `reports/YYYY-MM-DD/run_meta.json`

## GitHub Actions

Use GitHub Actions only after the local flow is understood.

1. Configure GitHub Actions Secrets for secret values such as `AIHUBMIX_KEY`, `OPENAI_API_KEY`, `BOCHA_API_KEYS`, `TAVILY_API_KEYS`, `SERPAPI_API_KEYS`, `TUSHARE_TOKEN`, `TELEGRAM_BOT_TOKEN`, and optional provider tokens.
2. Configure GitHub Actions Variables for non-secret values such as `STOCK_LIST`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `MAX_WORKERS`, `REPORT_TYPE`, and `TELEGRAM_CHAT_ID` if the repository treats that chat id as non-secret.
3. Trigger `.github/workflows/justice_plutus_analysis.yml` with `workflow_dispatch`.
4. Use the `workflow_dispatch.stocks` input for a temporary self-selected stock override. This should not change the persistent `STOCK_LIST` variable.
5. Inspect the run status, generated artifacts, and notification channel separately. A notification failure does not necessarily mean analysis reports were not generated.

## Pitfalls

- Missing LLM keys block real structured analysis. Ask the user to configure a key securely; do not print raw secret values back to the conversation.
- Missing search, chip distribution, or 同花顺专业数据模式 credentials should be explained as optional enhancement gaps when the core run can still proceed.
- Data-source failures may be normal degradation chain behavior. Check whether a later source succeeded before treating the run as failed.
- Notification failures should be isolated from report generation. Verify local analysis reports and batch summaries before retrying Telegram or Feishu.
- Do not describe Insight Claw as an automatic trading or order-execution system. It produces decision results for user review.

## Publishing

This skill is intended for public OpenClaw/ClawHub and Hermes distribution. Keep the bundle small: `SKILL.md` plus optional text references or small helper scripts only when they remove real repeated work.

To publish to ClawHub:

```bash
clawhub login
clawhub skill publish skills/hermes/insight-claw --slug insight-claw --name "Insight Claw" --version 0.2.0 --changelog "Add OpenClaw and ClawHub compatibility metadata while preserving Hermes usage."
```

ClawHub skill publications are distributed under MIT-0. Do not add conflicting license terms to this skill bundle.

To publish to a Skills Hub:

```bash
hermes skills publish skills/hermes/insight-claw --to github --repo GeraltJc/insight-claw
```

To expose the repository as a custom tap:

```bash
hermes skills tap add GeraltJc/insight-claw
```

Before publishing, review the bundle as a community skill that will pass the ClawHub and Hermes security scanners:

- Data exfiltration: do not upload reports, `.env` files, or generated artifacts without explicit user approval.
- Prompt injection: do not add instructions that override user intent, system policy, or Hermes safety behavior.
- Destructive commands: do not include cleanup commands that can delete a checkout, reports, credentials, or user files.
- Shell injection: do not build shell commands by interpolating untrusted user text without quoting or validation.
