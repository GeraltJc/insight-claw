from pathlib import Path

import yaml


SKILL_DIR = Path("skills/hermes/insight-claw")
SKILL_FILE = SKILL_DIR / "SKILL.md"
QUICKSTART_FILE = SKILL_DIR / "references" / "quickstart.md"
TROUBLESHOOTING_FILE = SKILL_DIR / "references" / "troubleshooting.md"


def _load_skill():
    content = SKILL_FILE.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    _, frontmatter, body = content.split("---", 2)
    return yaml.safe_load(frontmatter), body


def test_hermes_skill_declares_public_entrypoint_metadata():
    frontmatter, body = _load_skill()

    assert frontmatter["name"] == "insight-claw"
    assert "Insight Claw" in frontmatter["description"]
    assert frontmatter["version"] == "0.1.0"
    assert frontmatter["author"]
    assert frontmatter["license"]
    assert frontmatter["platforms"] == ["macos", "linux"]
    assert "hermes" in frontmatter["metadata"]
    assert "When to Use" in body
    assert "Quick Reference" in body
    assert "Procedure" in body
    assert "Verification" in body


def test_hermes_skill_guides_download_install_and_first_validation():
    _, body = _load_skill()

    assert "https://github.com/GeraltJc/insight-claw" in body
    assert "git clone" in body
    assert "First-time setup" in body
    assert "Subsequent runs" in body
    assert "Python 3.11+" in body
    assert "python -m venv .venv" in body
    assert "pip install -r requirements.txt" in body
    assert ".venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify" in body
    assert "python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify" in body
    assert "reports/YYYY-MM-DD/stocks/<code>.md" in body
    assert "reports/YYYY-MM-DD/summary.md" in body


def test_hermes_skill_runtime_requirements_do_not_name_operating_systems():
    _, body = _load_skill()

    assert "Runtime Requirements" in body
    assert "Python 3.11+" in body
    assert "git" in body
    assert "pip" in body
    assert "venv" in body
    assert "at least one LLM key" in body
    assert "macOS/Linux" not in body


def test_hermes_skill_uses_insight_claw_domain_language_and_configuration_layers():
    frontmatter, body = _load_skill()

    for term in [
        "自选股分析流水线",
        "行情数据",
        "搜索情报",
        "结构化分析",
        "决策结果",
        "分析报告",
        "批次汇总",
        "通知消息",
        "降级链",
        "同花顺专业数据模式",
    ]:
        assert term in body

    for env_name in [
        "AIHUBMIX_KEY",
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_MODEL",
        "BOCHA_API_KEYS",
        "TAVILY_API_KEYS",
        "SERPAPI_API_KEYS",
        "TUSHARE_TOKEN",
        "ENABLE_CHIP_DISTRIBUTION",
        "IFIND_REFRESH_TOKEN",
        "ENABLE_THS_PRO_DATA",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "FEISHU_WEBHOOK_URL",
    ]:
        assert env_name in body

    declared_secret_names = {item["name"] for item in frontmatter["required_environment_variables"]}
    assert {"AIHUBMIX_KEY", "OPENAI_API_KEY"}.issubset(declared_secret_names)


def test_hermes_skill_covers_github_actions_publishing_and_security_constraints():
    _, body = _load_skill()

    for phrase in [
        "workflow_dispatch",
        "GitHub Actions Secrets",
        "GitHub Actions Variables",
        "STOCK_LIST",
        "hermes skills publish",
        "hermes skills tap add",
        "security scanner",
        "Data exfiltration",
        "Prompt injection",
        "Destructive commands",
        "Shell injection",
    ]:
        assert phrase in body

    for forbidden in [
        "rm -rf",
        "git reset --hard",
        "curl -fsSL",
    ]:
        assert forbidden not in body


def test_hermes_skill_references_progressive_disclosure_files():
    _, body = _load_skill()
    quickstart = QUICKSTART_FILE.read_text(encoding="utf-8")
    troubleshooting = TROUBLESHOOTING_FILE.read_text(encoding="utf-8")

    assert "references/quickstart.md" in body
    assert "references/troubleshooting.md" in body
    assert "python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify" in quickstart
    assert "GitHub Actions" in quickstart
    assert "missing LLM" in troubleshooting
    assert "notification" in troubleshooting
    assert "degradation chain" in troubleshooting
