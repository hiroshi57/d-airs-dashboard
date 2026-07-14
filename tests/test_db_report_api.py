import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from backend.db import Database  # noqa: E402
from backend.report import build_html_report  # noqa: E402


def test_record_roundtrip_and_trend_order():
    db = Database(":memory:")
    cid = db.add_client("t-a", "ACME")
    db.add_record("t-a", cid, "2026-05", 55.0, "v1.0", {"adoption": 50})
    db.add_record("t-a", cid, "2026-06", 60.0, "v1.0", {"adoption": 60})
    recs = db.list_records("t-a", cid)
    assert [r["month"] for r in recs] == ["2026-05", "2026-06"]   # 時系列順


def test_tenant_isolation_client_and_records():
    db = Database(":memory:")
    cid = db.add_client("t-a", "ACME")
    db.add_record("t-a", cid, "2026-06", 60.0, "v1.0", {"adoption": 60})
    assert db.get_client("t-b", cid) is None          # 越境不可
    assert db.list_records("t-b", cid) == []           # 越境不可


def test_html_report_sections_and_privacy_note():
    records = [{"month": "2026-05", "score": 55.0, "version": "v1.0", "domains": {"adoption": 50}},
               {"month": "2026-06", "score": 62.0, "version": "v1.0",
                "domains": {"adoption": 60, "application": 64}}]
    recs = [{"master_id": "M-01", "name": "基礎研修", "target": "全社"}]
    html = build_html_report("ACME", records, recs)
    assert "D-AIRS 月次レポート" in html and "ACME" in html
    assert "4ドメイン内訳" in html and "スコア推移" in html
    assert "M-01" in html
    assert "5名" in html                               # プライバシー注記
    assert "前月比 +7.0" in html


def test_html_report_escapes():
    html = build_html_report("<b>x</b>", [], [])
    assert "<b>x</b>" not in html and "&lt;b&gt;" in html


def test_api_e2e_and_tenant_isolation():
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from backend.api.main import create_app
    c = TestClient(create_app())
    ha, hb = {"X-Tenant-Id": "t-a"}, {"X-Tenant-Id": "t-b"}
    cid = c.post("/v1/clients", json={"company": "ACME"}, headers=ha).json()["client_id"]
    rec = c.post("/v1/records", json={"client_id": cid, "month": "2026-06", "wau_ratio": 0.6,
                                      "retention_30d": 0.5, "usage_stage_avg": 2.0,
                                      "survey_score": 0.7, "training_ratio": 0.6,
                                      "governance_ratio": 0.5}, headers=ha).json()
    assert 0 <= rec["score"] <= 100
    assert c.get(f"/v1/report/{cid}", headers=hb).status_code == 404   # 越境不可
    r = c.get(f"/v1/report/{cid}", headers=ha)
    assert r.status_code == 200 and "D-AIRS 月次レポート" in r.text
