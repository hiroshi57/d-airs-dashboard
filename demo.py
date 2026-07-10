"""デモ(APIキー不要). `python demo.py`"""
from backend.scoring import (
    DairsCalculator, DomainInput, PrivacyGuard, ChurnDetector, load_formula,
)


def main():
    f = load_formula()
    calc = DairsCalculator(f)
    print("=== D-AIRS スコア ===")
    r = calc.compute(DomainInput(wau_ratio=0.6, retention_30d=0.5, usage_stage_avg=2.0,
                                 survey_score=0.7, training_ratio=0.6, governance_ratio=0.5))
    print(f"  score={r.score:.1f} (version {r.version}) domains={r.as_dict()['domains']}")

    print("\n=== プライバシーマスク(最小5名) ===")
    pg = PrivacyGuard(f["privacy"]["min_segment"])
    print(f"  3名部署: {pg.aggregate(3, 72.0).as_dict()}")
    print(f"  8名部署: {pg.aggregate(8, 72.0).as_dict()}")

    print("\n=== 離脱検知(導入2ヶ月後にWAU半減) ===")
    det = ChurnDetector(f["churn"]["drop_ratio"])
    alerts = det.detect({"営業部": [50, 48, 24], "開発部": [30, 32, 33]})
    for a in alerts:
        print(f"  {a.department}: ピーク{a.peak}→最新{a.latest} (▼{a.drop_pct:.0f}%)")


if __name__ == "__main__":
    main()
