// minimal, axios-free fetch wrapper
const BASE = "http://127.0.0.1:8000";

export async function fetchBusinesses() {
  const res = await fetch(`${BASE}/business/`);
  if (!res.ok) throw new Error("Failed to fetch businesses");
  return res.json();
}
export async function fetchRecommendations({
  city = "",
  businessType = "",
  monthlyBudget = 0,
  targetPersonas = [],
  top = 5,
} = {}) {
  const res = await fetch(`${BASE}/recommendations/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      city,
      businessType,
      monthlyBudget,
      targetPersonas,
      top,
    }),
  });

  if (!res.ok) throw new Error("Failed to fetch recommendations");
  return res.json();
}




export async function fetchAdminStats() {
  const res = await fetch(`${BASE}/admin/stats`);
  if (!res.ok) throw new Error("Failed to fetch admin stats");
  return res.json();
}

export async function fetchTopRecommended() {
  const res = await fetch(`${BASE}/admin/top-recommended`);
  if (!res.ok) throw new Error("Failed to fetch top recommended");
  return res.json();
}
