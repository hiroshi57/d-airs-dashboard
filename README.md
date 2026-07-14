# d-airs-dashboard

AI定着スコアリング・ダッシュボード（**D-AIRS: Digital-identity AI Readiness Score**）。
企業のAIツール定着度を継続計測し、介入施策を提案する「導入後を科学する」商品。

## 差別化ポイント

- 研修会社/SIerが扱わない**導入後の定着を独自指標で継続計測**（DARSの商用版ポジション）
- 「定着率を数値で経営報告できる」ことが購買理由になる商品設計
- 介入施策の**前後スコア差分を効果測定**（当社研修・伴走メニューへ直結）

## ステータス

🟢 **全機能拡張中**（D-AIRSスコア / プライバシーマスク / 離脱検知 / F3介入レコメンド / 効果測定）

- [docs/dairs_spec_v1.md](docs/dairs_spec_v1.md) — 4ドメイン算出式・重み・プライバシー設計
- `backend/scoring/` — D-AIRS算出(formula.yamlでバージョン管理) + 5名未満マスク + 離脱検知
- `backend/recommend/` — F3 介入レコメンド(スコアパターン→施策マスタ, **全推奨に施策マスタID=創作なし**)
- `backend/effect/` — 効果測定モード(介入群/非介入群の差分の差, **因果注記を自動付与**)

```bash
python demo.py          # D-AIRSスコア + プライバシーマスク + 離脱検知
python -m pytest -q     # テスト17件(DB/テナント分離/HTMLレポート/API E2E含む)
```

## 本番構成（SQLite + HTMLレポート + Vite 2画面）

- **DB**: `backend/db/`（SQLite・標準ライブラリ）。全クエリ tenant_id 強制フィルタ＝**テナント分離**（越境不可を自動テスト）
- **API**: `backend/api/main.py`（FastAPI）。clients / records(月次スコア算出) / report(HTML)
- **HTMLレポート**: `backend/report/builder.py`（4ドメイン内訳＋スコア推移＋推奨施策、プライバシー注記、XSSエスケープ）
- **フロント**: `frontend/`（React+Vite）。**経営層ビュー**＋**推進者ビュー**の2画面。ビルド不要は `frontend/standalone.html`
- **CI**: `.github/workflows/ci.yml`

```bash
uvicorn backend.api.main:app --reload
cd frontend && npm install && npm run dev     # or: open frontend/standalone.html
```

## 予定フォルダ構成（実装時）

```
backend/{ingest/connectors,scoring,recommend,effect,report}
dbt/ / frontend/dashboard/{ExecutiveView,ChampionView}
scripts/gen_dummy_data.py
tests/{test_privacy_mask,test_churn_detection,test_formula_versioning}
```
