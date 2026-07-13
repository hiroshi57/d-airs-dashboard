"""F3 介入レコメンド. スコアパターン->施策マスタ. 全レコメンドに施策マスタIDがひも付く(創作しない)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List

DEFAULT_MASTER = {"actions": [
    {"id": "M-01", "name": "AI基礎研修+業務テンプレ配布", "effort_days": 5, "target": "対象部署"},
    {"id": "M-02", "name": "活用深化ワークショップ", "effort_days": 3, "target": "推進部署"},
    {"id": "M-03", "name": "ガバナンス整備伴走", "effort_days": 8, "target": "管理部門"},
    {"id": "M-04", "name": "部署横展開キックオフ", "effort_days": 4, "target": "未導入部署"},
    {"id": "M-05", "name": "定着リマインド運用設計", "effort_days": 2, "target": "全社"},
]}
DEFAULT_RULES = {"rules": [
    {"when": {"ability": "low", "adoption": "low"}, "action": "M-01"},
    {"when": {"adoption": "high", "application": "low"}, "action": "M-02"},
    {"when": {"assurance": "low"}, "action": "M-03"},
    {"when": {"adoption": "low"}, "action": "M-04"},
    {"when": {"adoption": "high", "application": "high"}, "action": "M-05"},
]}


def _load(name: str, default: Dict) -> Dict:
    path = os.path.join(os.path.dirname(__file__), name)
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return default


def _level(v: float) -> str:
    return "high" if v >= 60 else ("low" if v < 40 else "mid")


@dataclass
class Recommendation:
    master_id: str        # ★施策マスタID(必須・創作なし)
    name: str
    target: str
    effort_days: int

    def as_dict(self):
        return self.__dict__


class RecommendEngine:
    def __init__(self, rules: Dict = None, master: Dict = None) -> None:
        self.rules = rules or _load("rules.yaml", DEFAULT_RULES)
        master = master or _load("actions_master.yaml", DEFAULT_MASTER)
        self._master = {a["id"]: a for a in master["actions"]}

    def recommend(self, domains: Dict[str, float]) -> List[Recommendation]:
        levels = {k: _level(v) for k, v in domains.items()}
        out: List[Recommendation] = []
        seen = set()
        for rule in self.rules["rules"]:
            if all(levels.get(d) == lv for d, lv in rule["when"].items()):
                mid = rule["action"]
                if mid in self._master and mid not in seen:
                    a = self._master[mid]
                    out.append(Recommendation(mid, a["name"], a["target"], a["effort_days"]))
                    seen.add(mid)
        return out
