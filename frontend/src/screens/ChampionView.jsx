import React from "react";

// 推進者ビュー: 離脱検知 + 介入レコメンド。
export default function ChampionView({ churnAlerts, recommendations }) {
  return (
    <div className="card">
      <h2>離脱検知</h2>
      {churnAlerts?.length ? (
        <ul>{churnAlerts.map((a) => (
          <li key={a.department}>{a.department}: ピーク{a.peak}→最新{a.latest}
            <b className="down"> ▼{a.drop_pct}%</b></li>))}</ul>
      ) : <p>離脱アラートはありません。</p>}

      <h2>推奨介入施策</h2>
      <ul>{(recommendations || []).map((r) => (
        <li key={r.master_id}>[{r.master_id}] {r.name}（{r.target} / {r.effort_days}人日）</li>))}
      </ul>
    </div>
  );
}
