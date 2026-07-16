"""定着スコア将来予測 + 離脱早期予兆(尖った武器).

過去のD-AIRS時系列から線形トレンドで次月を予測し、
「予測値が閾値割れ」または「下降トレンド」の部署を離脱リスクとして先回り検知する。
標準ライブラリのみ(最小二乗の線形回帰を自前実装)。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


def _linreg(ys: List[float]):
    """x=0..n-1 に対する最小二乗直線 (slope, intercept) を返す."""
    n = len(ys)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        return 0.0, ys[0]
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n)) or 1.0
    slope = num / den
    return slope, my - slope * mx


@dataclass
class Forecast:
    history: List[float]
    slope: float               # 月あたり変化
    next_value: float          # 次月予測
    trend: str                 # up / down / flat
    at_risk: bool              # 離脱予兆
    reason: str

    def as_dict(self):
        return {"slope": round(self.slope, 2), "next_value": round(self.next_value, 1),
                "trend": self.trend, "at_risk": self.at_risk, "reason": self.reason}


def forecast_dairs(history: List[float], risk_threshold: float = 50.0,
                   drop_slope: float = -3.0) -> Forecast:
    slope, intercept = _linreg(history)
    n = len(history)
    next_value = slope * n + intercept
    trend = "up" if slope > 1 else ("down" if slope < -1 else "flat")
    # 予兆: 次月予測が閾値割れ、または急降下トレンド
    at_risk = next_value < risk_threshold or slope <= drop_slope
    reasons = []
    if next_value < risk_threshold:
        reasons.append(f"次月予測 {next_value:.0f} < 閾値 {risk_threshold:.0f}")
    if slope <= drop_slope:
        reasons.append(f"下降トレンド(月{slope:.1f})")
    return Forecast(history=history, slope=slope, next_value=next_value, trend=trend,
                    at_risk=at_risk, reason="; ".join(reasons) or "安定")


def early_warnings(dept_histories: dict, risk_threshold: float = 50.0) -> List[dict]:
    """部署別に予兆を検出し、リスク部署を返す(予測値の低い順)."""
    out = []
    for dept, hist in dept_histories.items():
        f = forecast_dairs(hist, risk_threshold=risk_threshold)
        if f.at_risk:
            out.append({"department": dept, **f.as_dict()})
    out.sort(key=lambda x: x["next_value"])
    return out
