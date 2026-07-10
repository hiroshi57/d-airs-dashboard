"""プライバシー設計(差別化). 最小集計単位未満のセグメントはマスクする."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MaskedValue:
    masked: bool
    value: Optional[float] = None
    reason: str = ""

    def as_dict(self):
        return {"masked": self.masked, "value": self.value, "reason": self.reason}


class PrivacyGuard:
    def __init__(self, min_segment: int = 5) -> None:
        self.min_segment = min_segment

    def aggregate(self, headcount: int, value: float) -> MaskedValue:
        if headcount < self.min_segment:
            return MaskedValue(masked=True,
                               reason=f"集計人数 {headcount} < 最小単位 {self.min_segment} のためマスク")
        return MaskedValue(masked=False, value=value)
