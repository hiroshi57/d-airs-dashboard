"""離脱検知. 部署別の月次WAU系列から、ピーク比で大きく低下した部署を検出."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ChurnAlert:
    department: str
    peak: float
    latest: float
    drop_pct: float

    def as_dict(self):
        return {"department": self.department, "peak": self.peak,
                "latest": self.latest, "drop_pct": round(self.drop_pct, 1)}


class ChurnDetector:
    def __init__(self, drop_ratio: float = 0.5) -> None:
        self.drop_ratio = drop_ratio

    def detect(self, wau_by_dept: Dict[str, List[float]]) -> List[ChurnAlert]:
        alerts: List[ChurnAlert] = []
        for dept, series in wau_by_dept.items():
            if len(series) < 2:
                continue
            peak = max(series)
            latest = series[-1]
            if peak > 0 and (peak - latest) / peak >= self.drop_ratio:
                alerts.append(ChurnAlert(dept, peak, latest, (peak - latest) / peak * 100))
        alerts.sort(key=lambda a: a.drop_pct, reverse=True)
        return alerts
