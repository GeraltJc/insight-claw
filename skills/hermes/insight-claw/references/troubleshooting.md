# Insight Claw Troubleshooting

Use this reference after the main no-notification validation path fails or produces incomplete results.

## Missing LLM Configuration

A missing LLM key blocks real structured analysis. Ask the user to configure `AIHUBMIX_KEY` or `OPENAI_API_KEY` securely. Do not print raw secret values back to the user.

## Dependency Installation Fails

Confirm Python 3.11+ is available, the virtual environment is active or explicitly addressed through `.venv/bin/python`, and dependencies are installed from `requirements.txt`.

## Data Provider Gaps

Some 行情数据 sources may fail or be rate-limited. Treat this as possible degradation chain behavior until every configured provider has failed.

## Optional Enhancement Gaps

Missing search intelligence, chip distribution, or 同花顺专业数据模式 credentials can reduce context but should not be described as a full setup failure when the core analysis path still runs.

## Notification Failures

Notification failures should be isolated from report generation. First verify local analysis reports and batch summaries under `reports/YYYY-MM-DD/`, then retry Telegram or Feishu configuration.

## Empty or Incomplete Reports

Check `run_meta.json` for success and failure counts. Then inspect single-stock JSON files before rerunning the whole batch.

## Security

Do not upload `.env`, generated reports, notification payloads, or raw model inputs without explicit user approval.
