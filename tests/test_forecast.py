import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.forecast import forecast_dairs, early_warnings  # noqa: E402


def test_upward_trend_predicts_higher():
    f = forecast_dairs([40, 45, 50, 55])
    assert f.slope > 0 and f.trend == "up"
    assert f.next_value > 55
    assert f.at_risk is False


def test_downward_trend_flags_risk():
    f = forecast_dairs([70, 62, 54, 46])
    assert f.trend == "down"
    assert f.at_risk is True
    assert "下降" in f.reason or "閾値" in f.reason


def test_low_forecast_flags_risk():
    f = forecast_dairs([48, 47, 46, 45], risk_threshold=50)
    assert f.next_value < 50
    assert f.at_risk is True


def test_stable_not_at_risk():
    f = forecast_dairs([70, 71, 70, 69], risk_threshold=50)
    assert f.trend == "flat"
    assert f.at_risk is False


def test_early_warnings_sorted_by_forecast():
    depts = {
        "安定部": [70, 71, 72, 73],
        "危険部": [60, 52, 44, 36],
        "低迷部": [45, 44, 43, 42],
    }
    warnings = early_warnings(depts, risk_threshold=50)
    names = [w["department"] for w in warnings]
    assert "安定部" not in names
    assert set(names) == {"危険部", "低迷部"}
    assert warnings[0]["next_value"] <= warnings[1]["next_value"]


def test_single_point_history():
    f = forecast_dairs([55])
    assert f.trend == "flat"
