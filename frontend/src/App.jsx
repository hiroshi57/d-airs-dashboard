import React, { useState } from "react";
import ExecutiveView from "./screens/ExecutiveView.jsx";
import ChampionView from "./screens/ChampionView.jsx";

// デモデータ(バックエンド未起動でも画面確認可能)
const DEMO_RECORDS = [
  { month: "2026-04", score: 48.0, domains: { adoption: 45, application: 50, ability: 48, assurance: 50 } },
  { month: "2026-05", score: 55.5, domains: { adoption: 55, application: 58, ability: 52, assurance: 56 } },
  { month: "2026-06", score: 62.0, domains: { adoption: 60, application: 66, ability: 60, assurance: 62 } },
];
const DEMO_CHURN = [{ department: "営業部", peak: 50, latest: 24, drop_pct: 52 }];
const DEMO_RECS = [{ master_id: "M-02", name: "活用深化ワークショップ", target: "推進部署", effort_days: 3 }];

export default function App() {
  const [tab, setTab] = useState("exec");
  return (
    <div className="wrap">
      <h1>D-AIRS 定着ダッシュボード</h1>
      <nav>
        <button onClick={() => setTab("exec")} disabled={tab === "exec"}>経営層ビュー</button>
        <button onClick={() => setTab("champ")} disabled={tab === "champ"}>推進者ビュー</button>
      </nav>
      {tab === "exec"
        ? <ExecutiveView records={DEMO_RECORDS} />
        : <ChampionView churnAlerts={DEMO_CHURN} recommendations={DEMO_RECS} />}
      <p className="privacy">※個人別スコアは非表示・最小集計単位5名でマスク(プライバシー設計)</p>
    </div>
  );
}
