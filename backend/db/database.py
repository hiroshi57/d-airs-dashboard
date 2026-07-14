"""永続化層(SQLite, 標準ライブラリ). テナント分離 + 月次D-AIRSスコアの時系列保存.

全クエリは tenant_id で必ずフィルタ(越境アクセス不可)。
最小集計単位(5名未満)のマスクは scoring/privacy.py が担う。
"""
from __future__ import annotations

import json
import sqlite3
from typing import Dict, List, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    company TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS dairs_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    score REAL NOT NULL,
    version TEXT NOT NULL,
    domains TEXT NOT NULL
);
"""


class Database:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def add_client(self, tenant_id: str, company: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO clients(tenant_id, company) VALUES (?, ?)", (tenant_id, company))
        self.conn.commit()
        return cur.lastrowid

    def get_client(self, tenant_id: str, client_id: int) -> Optional[Dict]:
        row = self.conn.execute(
            "SELECT id, company FROM clients WHERE id=? AND tenant_id=?",
            (client_id, tenant_id)).fetchone()
        return dict(row) if row else None

    def add_record(self, tenant_id: str, client_id: int, month: str,
                   score: float, version: str, domains: Dict) -> int:
        cur = self.conn.execute(
            "INSERT INTO dairs_records(tenant_id, client_id, month, score, version, domains) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tenant_id, client_id, month, score, version, json.dumps(domains, ensure_ascii=False)))
        self.conn.commit()
        return cur.lastrowid

    def list_records(self, tenant_id: str, client_id: int) -> List[Dict]:
        rows = self.conn.execute(
            "SELECT month, score, version, domains FROM dairs_records "
            "WHERE tenant_id=? AND client_id=? ORDER BY month", (tenant_id, client_id)).fetchall()
        return [{"month": r["month"], "score": r["score"], "version": r["version"],
                 "domains": json.loads(r["domains"])} for r in rows]

    def close(self) -> None:
        self.conn.close()
