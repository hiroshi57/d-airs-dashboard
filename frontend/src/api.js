const BASE = import.meta.env?.VITE_API || "http://localhost:8000";
const h = (t) => ({ "Content-Type": "application/json", "X-Tenant-Id": t });

export async function createClient(t, company) {
  return (await fetch(`${BASE}/v1/clients`, { method: "POST", headers: h(t), body: JSON.stringify({ company }) })).json();
}
export async function addRecord(t, rec) {
  return (await fetch(`${BASE}/v1/records`, { method: "POST", headers: h(t), body: JSON.stringify(rec) })).json();
}
export function reportUrl(clientId) { return `${BASE}/v1/report/${clientId}`; }
