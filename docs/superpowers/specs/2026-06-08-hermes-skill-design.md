# Hermes Skill Design

## Purpose

Create a project-shipped skill for Hermes Agent users who want to run Insight
Claw stock analysis through natural language requests such as "分析 600519 股票".

The skill is for Hermes Agent to read and execute. Codex is only being used to
author and verify the skill in this repository.

## Scope

The skill will live at:

```text
skills/hermes/SKILL.md
```

It will teach Hermes Agent how to:

- detect stock analysis requests
- normalize stock inputs into stock codes when possible
- run the existing Insight Claw local CLI
- read generated Markdown reports
- return a concise result summary to the user
- diagnose common setup and runtime failures

The initial version will not add new runtime code or wrapper scripts. The
repository already exposes a usable CLI entrypoint:

```bash
python -m justice_plutus run --stocks "600519" --no-notify
```

## Trigger Behavior

The skill should trigger on user requests like:

- "分析 600519 股票"
- "分析 贵州茅台"
- "分析 600519,000001"
- "用 Insight Claw 分析这些股票"
- "生成这些 A 股的分析报告"

The skill should not require users to mention Hermes, Insight Claw, or
JusticePlutus if their intent is clearly stock analysis.

## Execution Flow

Hermes Agent should:

1. Confirm the working directory is the Insight Claw repository root.
2. Extract stock codes or stock names from the user request.
3. Normalize stock codes into comma-separated six-digit A-share codes when
   possible.
4. Run local analysis without notifications by default:

   ```bash
   python -m justice_plutus run --stocks "<codes>" --no-notify
   ```

5. Omit `--no-notify` only when the user explicitly asks to send notifications.
6. After the run, inspect the generated report directory under
   `reports/YYYY-MM-DD/`.
7. Prefer `summary.md` for the batch-level answer, and use
   `stocks/<code>.md` when the user asks for per-stock detail.
8. Reply with the actionable analysis result and the report file paths.

## Configuration Guidance

The skill should describe only the configuration Hermes Agent needs to check
before running the workflow:

- Python 3.11+ and project dependencies installed
- at least one LLM key path, such as `OPENAI_API_KEY`, `AIHUBMIX_KEY`,
  `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY`
- optional data and search enhancement keys such as `TUSHARE_TOKEN`,
  `BOCHA_API_KEYS`, `TAVILY_API_KEYS`, `SERPAPI_API_KEYS`, `WENCAI_COOKIE`,
  and iFinD-related variables
- optional notification variables, used only when the user requests delivery

Missing optional enhancement keys must not be treated as blockers for a basic
local report.

## Hermes Agent Boundary

This skill is named `hermes` because it is consumed by Hermes Agent. It must
not claim that this repository currently provides a `hermes` shell command or a
complete Hermes runtime.

The repository contains an Agent-mode branch in `src/core/pipeline.py`, but the
referenced executor module is not present in the current tree. Therefore the
skill must not enable `AGENT_MODE=true` by default. If the project later adds a
complete Hermes or Agent executor, that path can be documented as an optional
advanced mode in a future revision.

## Error Handling

The skill should guide Hermes Agent to diagnose:

- missing project dependencies or Python import failures
- absent stock input
- missing required LLM credentials
- data source failures that still allow a degraded report
- LLM failures that result in failed or placeholder analysis
- report output not found after the CLI exits
- notification failures when delivery was requested

Hermes Agent should report the failed command, the meaningful error lines, and
the next concrete fix. It should not hide runtime failures behind generic
success messages.

## File Structure

Initial implementation:

```text
skills/
└── hermes/
    └── SKILL.md
```

No `references/`, `scripts/`, or `assets/` directories are needed for the first
version. Add them later only when the skill grows beyond a concise single
document.

## Validation

Validate the skill by:

- checking the YAML frontmatter contains only `name` and `description`
- confirming the skill path matches the requested public project layout
- confirming no Codex-only instructions remain in the Hermes-facing skill
- confirming commands match the current repository CLI
- running the skill validator when available

