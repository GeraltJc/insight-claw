from src.analyzer import AnalysisResult, GeminiAnalyzer


def test_prompt_includes_ifind_section_when_pack_available():
    analyzer = GeminiAnalyzer()

    prompt = analyzer._format_prompt(
        {
            "code": "600519",
            "stock_name": "贵州茅台",
            "date": "2026-03-30",
            "today": {},
            "ifind_financials": {
                "report_period": "2025-12-31",
                "revenue": 187170000000.0,
                "net_profit": 86230000000.0,
                "roe": 34.1,
            },
            "ifind_valuation": {
                "as_of_date": "2026-03-30",
                "pe_ttm": 23.6,
                "pb": 8.1,
                "total_market_value": 1964000000000.0,
            },
            "ifind_forecast": {
                "expected_growth_rate": 14.2,
                "periods": [
                    {"period_end": "2026-12-31", "net_profit": 95215849886.11},
                    {"period_end": "2027-12-31", "net_profit": 100687506345.25},
                ],
            },
            "ifind_quality_summary": {
                "profit_quality": "strong",
                "cashflow_health": "healthy",
                "leverage_risk": "low",
                "growth_visibility": "medium",
            },
        },
        "贵州茅台",
        news_context=None,
    )

    assert "## 基本面与估值增强" in prompt
    assert "最新财报期" in prompt
    assert "ROE" in prompt
    assert "一致预期净利润增速" in prompt
    assert "盈利质量" in prompt


def test_prompt_omits_ifind_section_when_no_ifind_data():
    analyzer = GeminiAnalyzer()

    prompt = analyzer._format_prompt(
        {
            "code": "600519",
            "stock_name": "贵州茅台",
            "today": {},
        },
        "贵州茅台",
    )

    assert "## 基本面与估值增强" not in prompt


def test_prompt_marks_chip_structure_unavailable_when_chip_data_missing():
    analyzer = GeminiAnalyzer()

    prompt = analyzer._format_prompt(
        {
            "code": "603986",
            "stock_name": "兆易创新",
            "date": "2026-06-07",
            "today": {
                "close": 488.0,
                "ma5": 494.45,
                "ma10": 493.06,
                "ma20": 452.03,
            },
        },
        "兆易创新",
    )

    assert "筹码分布数据缺失" in prompt
    assert "不得推断或编造获利比例、平均成本、筹码集中度" in prompt
    assert "筹码结构是否健康？若无筹码数据必须回答“数据缺失，无法判断”" in prompt


def test_system_prompt_allows_chip_structure_null_when_data_missing():
    assert '"chip_structure": null' in GeminiAnalyzer.SYSTEM_PROMPT
    assert "仅当提供了筹码分布数据时填写" in GeminiAnalyzer.SYSTEM_PROMPT
    assert "无筹码数据时必须标记为数据缺失" in GeminiAnalyzer.SYSTEM_PROMPT


def test_system_prompt_forbids_main_force_volume_claims_without_flow_data():
    assert "没有资金流、盘口、龙虎榜或筹码数据时" in GeminiAnalyzer.SYSTEM_PROMPT
    assert "不得判断主力资金未出货、正常洗盘、主力吸筹或主力出货" in GeminiAnalyzer.SYSTEM_PROMPT


def test_system_prompt_downgrades_buy_on_large_drop_below_ma5():
    assert "单日跌幅达到或超过5%" in GeminiAnalyzer.SYSTEM_PROMPT
    assert "收盘价低于MA5" in GeminiAnalyzer.SYSTEM_PROMPT
    assert "不得直接给出买入/加仓" in GeminiAnalyzer.SYSTEM_PROMPT


def test_market_consistency_guard_downgrades_buy_on_large_drop_below_ma5():
    analyzer = GeminiAnalyzer()
    result = AnalysisResult(
        code="603986",
        name="兆易创新",
        sentiment_score=76,
        trend_prediction="看多",
        operation_advice="买入",
        decision_type="buy",
        confidence_level="中",
        dashboard={
            "core_conclusion": {
                "one_sentence": "缩量回踩MA5支撑，趋势未破，可逢低布局",
                "signal_type": "🟢买入信号",
            },
            "battle_plan": {
                "action_checklist": [
                    "✅ 检查项1：多头排列",
                    "✅ 检查项2：乖离率合理",
                ],
            },
        },
    )

    analyzer._apply_market_consistency_guards(
        result,
        {
            "today": {
                "close": 488.0,
                "pct_chg": -7.8,
                "ma5": 494.45,
            }
        },
    )

    assert result.decision_type == "hold"
    assert result.operation_advice == "观望"
    assert result.confidence_level == "低"
    assert result.dashboard["core_conclusion"]["signal_type"] == "🟡持有观望"
    assert "跌幅超过5%且收盘低于MA5" in result.dashboard["core_conclusion"]["one_sentence"]
