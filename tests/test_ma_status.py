from src.core.pipeline import StockAnalysisPipeline
from src.storage import DatabaseManager, StockDaily


def test_storage_ma_status_uses_ma_alignment_not_price_position():
    storage = DatabaseManager()
    bar = StockDaily(close=488.0, ma5=494.45, ma10=493.06, ma20=452.03)

    assert storage._analyze_ma_status(bar) == "多头排列 📈"


def test_pipeline_ma_status_uses_ma_alignment_not_price_position():
    assert StockAnalysisPipeline._compute_ma_status(
        close=488.0,
        ma5=494.45,
        ma10=493.06,
        ma20=452.03,
    ) == "多头排列 📈"
