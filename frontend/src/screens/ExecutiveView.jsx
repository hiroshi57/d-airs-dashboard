import React from "react";

// 経営層ビュー: 組織D-AIRS + 4ドメイン + スコア推移。
function Bar({ v, max = 100 }) {
  return (
    <div style={{ background: "#e4e7ee", borderRadius: 4, width: 180, height: 12 }}>
      <div style={{ background: "#1a5fb4", height: 12, borderRadius: 4, width: `${Math.max(0, Math.min(1, v / max)) * 180}px` }} />
    </div>
  );
}

export default function ExecutiveView({ records }) {
  if (!records?.length) return <div className="card">データがありません。</div>;
  const latest = records[records.length - 1];
  const prev = records.length >= 2 ? records[records.length - 2] : null;
  const delta = prev ? latest.score - prev.score : 0;
  return (
    <div className="card">
      <h2>組織 D-AIRS スコア</h2>
      <div className="big">{latest.score.toFixed(1)} <small>/ 100</small></div>
      <div className={delta >= 0 ? "up" : "down"}>前月比 {delta >= 0 ? "+" : ""}{delta.toFixed(1)}</div>
      <h3>4ドメイン内訳</h3>
      {Object.entries(latest.domains).map(([k, v]) => (
        <div key={k} className="drow"><span>{k}</span><Bar v={v} /><span>{v.toFixed(0)}</span></div>
      ))}
      <h3>スコア推移</h3>
      <table><thead><tr><th>月</th><th>スコア</th></tr></thead>
        <tbody>{records.map((r) => <tr key={r.month}><td>{r.month}</td><td>{r.score.toFixed(1)}</td></tr>)}</tbody></table>
    </div>
  );
}
