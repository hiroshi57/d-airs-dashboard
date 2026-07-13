"""効果測定モード. 介入群/非介入群の前後スコア差分(差分の差=DID)を算出.

因果とまでは言えない旨の注記を必ず自動付与する(受け入れ基準)。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

CAUSAL_DISCLAIMER = "※本結果は相関の観察であり、因果関係を証明するものではありません(交絡の可能性)。"


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


@dataclass
class EffectResult:
    intervention_delta: float     # 介入群の前後差
    control_delta: float          # 非介入群の前後差
    diff_in_diff: float           # 差分の差(介入効果の推定)
    note: str                     # ★因果注記(必須・非空)

    def as_dict(self):
        return {"intervention_delta": round(self.intervention_delta, 2),
                "control_delta": round(self.control_delta, 2),
                "diff_in_diff": round(self.diff_in_diff, 2),
                "note": self.note}


class EffectMeasurer:
    def measure(self, intervention_before: List[float], intervention_after: List[float],
                control_before: List[float], control_after: List[float]) -> EffectResult:
        idelta = _mean(intervention_after) - _mean(intervention_before)
        cdelta = _mean(control_after) - _mean(control_before)
        return EffectResult(intervention_delta=idelta, control_delta=cdelta,
                            diff_in_diff=idelta - cdelta, note=CAUSAL_DISCLAIMER)
