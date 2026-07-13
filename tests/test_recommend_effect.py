import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.recommend import RecommendEngine  # noqa: E402
from backend.effect import EffectMeasurer  # noqa: E402


# --- F3 介入レコメンド ---
def test_recommend_all_have_master_id():
    recs = RecommendEngine().recommend(
        {"adoption": 30, "application": 30, "ability": 30, "assurance": 30})
    assert recs
    for r in recs:
        assert r.master_id.startswith("M-")   # 施策マスタID(創作なし)


def test_low_ability_low_adoption_maps_to_basic_training():
    recs = RecommendEngine().recommend(
        {"adoption": 30, "application": 50, "ability": 30, "assurance": 50})
    ids = {r.master_id for r in recs}
    assert "M-01" in ids     # ability low & adoption low -> 基礎研修


def test_high_adoption_low_application_maps_to_deepening():
    recs = RecommendEngine().recommend(
        {"adoption": 70, "application": 30, "ability": 60, "assurance": 60})
    ids = {r.master_id for r in recs}
    assert "M-02" in ids


def test_no_dupes_in_recommendations():
    recs = RecommendEngine().recommend(
        {"adoption": 30, "application": 30, "ability": 30, "assurance": 30})
    ids = [r.master_id for r in recs]
    assert len(ids) == len(set(ids))


# --- 効果測定モード ---
def test_diff_in_diff_and_disclaimer():
    m = EffectMeasurer().measure(
        intervention_before=[40, 42, 38], intervention_after=[60, 62, 58],
        control_before=[40, 41, 39], control_after=[45, 46, 44])
    assert round(m.intervention_delta) == 20
    assert round(m.control_delta) == 5
    assert round(m.diff_in_diff) == 15
    assert "因果" in m.note        # 因果注記が必ず付く


def test_effect_note_always_present():
    m = EffectMeasurer().measure([50], [50], [50], [50])
    assert m.note and m.diff_in_diff == 0.0
