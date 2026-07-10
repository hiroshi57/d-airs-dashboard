# d-airs-dashboard

AI定着スコアリング・ダッシュボード（**D-AIRS: Digital-identity AI Readiness Score**）。
企業のAIツール定着度を継続計測し、介入施策を提案する「導入後を科学する」商品。

## 差別化ポイント

- 研修会社/SIerが扱わない**導入後の定着を独自指標で継続計測**（DARSの商用版ポジション）
- 「定着率を数値で経営報告できる」ことが購買理由になる商品設計
- 介入施策の**前後スコア差分を効果測定**（当社研修・伴走メニューへ直結）

## ステータス

🟢 **差別化コア実装済み**（D-AIRSスコア＋プライバシーマスク＋離脱検知） / 他機能は承認後に拡張

- [docs/dairs_spec_v1.md](docs/dairs_spec_v1.md) — 4ドメイン算出式・重み・プライバシー設計
- `backend/scoring/` — D-AIRS算出(formula.yamlでバージョン管理) + 5名未満マスク + 離脱検知（tests 6件PASS）

```bash
python demo.py          # D-AIRSスコア + プライバシーマスク + 離脱検知
python -m pytest -q
```

進め方（プロンプト指定）: D-AIRS v1仕様書 → **承認** → 実装（F1取込→F2ダッシュボード→F3介入→F4レポート、dbtはテスト付き）。

## 予定フォルダ構成（実装時）

```
backend/{ingest/connectors,scoring,recommend,effect,report}
dbt/ / frontend/dashboard/{ExecutiveView,ChampionView}
scripts/gen_dummy_data.py
tests/{test_privacy_mask,test_churn_detection,test_formula_versioning}
```
