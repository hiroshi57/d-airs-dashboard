"""D-AIRS スコア算出(0-100). formula.yaml のバージョンをスコアにひも付ける."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict

DEFAULT_FORMULA = {
    "version": "v1.0",
    "weights": {"adoption": 0.30, "application": 0.30, "ability": 0.20, "assurance": 0.20},
    "privacy": {"min_segment": 5},
    "churn": {"drop_ratio": 0.5},
}


def load_formula(path: str = "") -> Dict:
    path = path or os.path.join(os.path.dirname(__file__), "formula.yaml")
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return DEFAULT_FORMULA


@dataclass
class DomainInput:
    wau_ratio: float          # 0-1
    retention_30d: float      # 0-1
    usage_stage_avg: float    # 1-3
    survey_score: float       # 0-1
    training_ratio: float     # 0-1
    governance_ratio: float   # 0-1


@dataclass
class DairsResult:
    score: float
    version: str
    domains: Dict[str, float]

    def as_dict(self):
        return {"score": round(self.score, 1), "version": self.version,
                "domains": {k: round(v, 1) for k, v in self.domains.items()}}


class DairsCalculator:
    def __init__(self, formula: Dict = None) -> None:
        self.formula = formula or DEFAULT_FORMULA

    def compute(self, x: DomainInput) -> DairsResult:
        domains = {
            "adoption": _clamp01((x.wau_ratio + x.retention_30d) / 2) * 100,
            "application": _clamp(x.usage_stage_avg, 0, 3) / 3 * 100,
            "ability": _clamp01((x.survey_score + x.training_ratio) / 2) * 100,
            "assurance": _clamp01(x.governance_ratio) * 100,
        }
        w = self.formula["weights"]
        tw = sum(w.values()) or 1.0
        score = sum(domains[k] * w[k] for k in w) / tw
        return DairsResult(score=score, version=self.formula.get("version", "?"), domains=domains)


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _clamp01(v):
    return _clamp(v, 0.0, 1.0)
