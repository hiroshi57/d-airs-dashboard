"""D-AIRS 月次HTMLレポート(経営層向け). 標準ライブラリのみで生成."""
from __future__ import annotations

import html
from typing import Dict, List


def _bar(v: float, max_v: float = 100, width: int = 160) -> str:
    w = int(max(0, min(1, v / max_v)) * width)
    return (f'<div style="background:#e4e7ee;border-radius:4px;width:{width}px;height:12px">'
            f'<div style="background:#1a5fb4;height:12px;border-radius:4px;width:{w}px"></div></div>')


def build_html_report(company: str, records: List[Dict],
                      recommendations: List[Dict] = None) -> str:
    company = html.escape(company)
    recommendations = recommendations or []
    latest = records[-1] if records else {"score": 0, "version": "-", "domains": {}, "month": "-"}
    prev = records[-2] if len(records) >= 2 else None
    delta = (latest["score"] - prev["score"]) if prev else 0.0

    trend = "".join(
        f'<tr><td>{html.escape(r["month"])}</td><td>{r["score"]:.1f}</td></tr>' for r in records)
    domains = "".join(
        f'<tr><td>{html.escape(k)}</td><td>{v:.1f}</td><td>{_bar(v)}</td></tr>'
        for k, v in latest["domains"].items())
    recs = "".join(
        f'<li>[{html.escape(r.get("master_id",""))}] {html.escape(r.get("name",""))} '
        f'({html.escape(r.get("target",""))})</li>' for r in recommendations) or "<li>該当施策なし</li>"

    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<title>D-AIRS 月次レポート - {company}</title>
<style>body{{font-family:system-ui,sans-serif;margin:24px;color:#1a1a2e}}
h1{{color:#1a5fb4}} table{{border-collapse:collapse;margin:8px 0}}
th,td{{border:1px solid #dde;padding:6px 10px}} th{{background:#eef2fb}}
.big{{font-size:40px;color:#1a5fb4;font-weight:bold}}</style></head><body>
<h1>D-AIRS 月次レポート</h1>
<p>企業: <b>{company}</b> / 対象月: {html.escape(latest["month"])} / 算出版: {html.escape(latest["version"])}</p>
<p>組織 D-AIRS スコア: <span class="big">{latest["score"]:.1f}</span> / 100
 (前月比 {delta:+.1f})</p>
<h2>4ドメイン内訳</h2>
<table><tr><th>ドメイン</th><th>スコア</th><th></th></tr>{domains}</table>
<h2>スコア推移</h2>
<table><tr><th>月</th><th>スコア</th></tr>{trend}</table>
<h2>推奨介入施策</h2><ul>{recs}</ul>
<hr><small>※個人別スコアは表示せず、最小集計単位5名でマスクしています(プライバシー設計)。</small>
</body></html>"""
