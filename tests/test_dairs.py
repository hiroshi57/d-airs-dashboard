import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.scoring import (  # noqa: E402
    DairsCalculator, DomainInput, PrivacyGuard, ChurnDetector, load_formula,
)


def test_dairs_within_bounds_and_versioned():
    r = DairsCalculator().compute(DomainInput(0.6, 0.5, 2.0, 0.7, 0.6, 0.5))
    assert 0 <= r.score <= 100
    assert r.version == "v1.0"


def test_formula_versioning():
    f2 = {"version": "v2.0",
          "weights": {"adoption": 1.0, "application": 0, "ability": 0, "assurance": 0},
          "privacy": {"min_segment": 5}, "churn": {"drop_ratio": 0.5}}
    r = DairsCalculator(f2).compute(DomainInput(1.0, 1.0, 3.0, 1.0, 1.0, 1.0))
    assert r.version == "v2.0"
    assert r.score == 100.0    # adoption=100, weight1.0


def test_privacy_mask_below_min():
    pg = PrivacyGuard(5)
    assert pg.aggregate(3, 72.0).masked is True
    v = pg.aggregate(8, 72.0)
    assert v.masked is False and v.value == 72.0


def test_churn_detection_flags_halved_dept():
    det = ChurnDetector(0.5)
    alerts = det.detect({"営業部": [50, 48, 24], "開発部": [30, 32, 33]})
    depts = [a.department for a in alerts]
    assert "営業部" in depts        # ピーク50->24 は50%減
    assert "開発部" not in depts


def test_churn_ignores_short_series():
    det = ChurnDetector(0.5)
    assert det.detect({"新部署": [10]}) == []


def test_load_formula_structure():
    f = load_formula()
    assert set(f["weights"]) == {"adoption", "application", "ability", "assurance"}
    assert f["privacy"]["min_segment"] == 5
