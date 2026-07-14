"""D-AIRS API(FastAPI). 月次メトリクス取込 -> スコア算出 -> レポート/推奨.
テナント分離(X-Tenant-Id)。`uvicorn backend.api.main:app --reload`
"""
from datetime import datetime, timezone

from ..db import Database
from ..report import build_html_report
from ..scoring import DairsCalculator, DomainInput, load_formula
from ..recommend import RecommendEngine

DB = Database(":memory:")
CALC = DairsCalculator(load_formula())
RECO = RecommendEngine()


def compute_and_store(tenant: str, client_id: int, month: str, di: DomainInput) -> dict:
    r = CALC.compute(di)
    DB.add_record(tenant, client_id, month, r.score, r.version, r.domains)
    recs = RECO.recommend(r.domains)
    return {"month": month, "score": r.score, "version": r.version,
            "domains": r.domains, "recommendations": [x.as_dict() for x in recs]}


def create_app():  # pragma: no cover
    from fastapi import Depends, FastAPI, Header, HTTPException
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel

    app = FastAPI(title="D-AIRS Dashboard", version="1.0.0")

    def tenant(x_tenant_id: str = Header(...)) -> str:
        if not x_tenant_id:
            raise HTTPException(401, "tenant required")
        return x_tenant_id

    class ClientIn(BaseModel):
        company: str

    class RecordIn(BaseModel):
        client_id: int
        month: str
        wau_ratio: float = 0.0
        retention_30d: float = 0.0
        usage_stage_avg: float = 1.0
        survey_score: float = 0.0
        training_ratio: float = 0.0
        governance_ratio: float = 0.0

    @app.post("/v1/clients")
    def create_client(body: ClientIn, t: str = Depends(tenant)):
        return {"client_id": DB.add_client(t, body.company)}

    @app.post("/v1/records")
    def add_record(body: RecordIn, t: str = Depends(tenant)):
        if DB.get_client(t, body.client_id) is None:
            raise HTTPException(404, "client not found")
        di = DomainInput(body.wau_ratio, body.retention_30d, body.usage_stage_avg,
                         body.survey_score, body.training_ratio, body.governance_ratio)
        return compute_and_store(t, body.client_id, body.month, di)

    @app.get("/v1/report/{client_id}", response_class=HTMLResponse)
    def report(client_id: int, t: str = Depends(tenant)):
        client = DB.get_client(t, client_id)
        if client is None:
            raise HTTPException(404, "client not found")
        records = DB.list_records(t, client_id)
        recs = []
        if records:
            recs = [x.as_dict() for x in RECO.recommend(records[-1]["domains"])]
        return build_html_report(client["company"], records, recs)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


try:  # pragma: no cover
    app = create_app()
except Exception:
    app = None
