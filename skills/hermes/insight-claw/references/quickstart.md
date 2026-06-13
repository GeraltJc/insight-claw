# Insight Claw Quickstart

Use this reference when the user asks Hermes Agent to set up or run Insight Claw with more detail than the main `SKILL.md` provides.

## Local Setup

First-time setup:

```bash
git clone https://github.com/GeraltJc/insight-claw.git insight-claw
cd insight-claw
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Configure at least one LLM key path before a real run:

```dotenv
AIHUBMIX_KEY=
OPENAI_API_KEY=
OPENAI_BASE_URL=https://aihubmix.com/v1
OPENAI_MODEL=gemini-flash-lite-latest
LITELLM_MODEL=openai/gemini-flash-lite-latest
```

Run the first validation without notification messages:

```bash
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Subsequent runs:

```bash
cd insight-claw
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Expected outputs:

- `reports/YYYY-MM-DD/stocks/<code>.md`
- `reports/YYYY-MM-DD/stocks/<code>.json`
- `reports/YYYY-MM-DD/summary.md`
- `reports/YYYY-MM-DD/summary.json`
- `reports/YYYY-MM-DD/run_meta.json`

## Optional Enhancements

Search intelligence:

```dotenv
BOCHA_API_KEYS=
TAVILY_API_KEYS=
SERPAPI_API_KEYS=
```

Market data and chip distribution:

```dotenv
TUSHARE_TOKEN=
ENABLE_CHIP_DISTRIBUTION=false
WENCAI_COOKIE=
HSCLOUD_AUTH_TOKEN=
```

TongHuaShun professional mode:

```dotenv
IFIND_REFRESH_TOKEN=
ENABLE_THS_PRO_DATA=false
ENABLE_IFIND_ANALYSIS_ENHANCEMENT=false
```

Notification channels:

```dotenv
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
FEISHU_WEBHOOK_URL=
```

## GitHub Actions

Use GitHub Actions when the user wants remote or scheduled execution.

1. Put secrets such as API keys and bot tokens in GitHub Actions Secrets.
2. Put non-secret defaults such as `STOCK_LIST`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `MAX_WORKERS`, and `REPORT_TYPE` in GitHub Actions Variables.
3. Trigger `.github/workflows/justice_plutus_analysis.yml` with `workflow_dispatch`.
4. Use the `stocks` input for a temporary self-selected stock override.
