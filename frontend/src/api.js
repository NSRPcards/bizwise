// frontend/src/api.js
const BASE_URL = "http://127.0.0.1:8000";

export async function getBusinesses({ city = "", category = "" } = {}) {
  const params = new URLSearchParams();
  if (city) params.append("location", city);
  if (category) params.append("category", category);
  const url = `${BASE_URL}/business/?${params.toString()}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch businesses");
  return res.json();
}

export async function getAreas() {
  const res = await fetch(`${BASE_URL}/areas/`);
  if (!res.ok) throw new Error("Failed to fetch areas");
  return res.json();
}

export async function postRecommendations(payload) {
  const res = await fetch(`${BASE_URL}/recommendations/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error("Failed recommendations: " + text);
  }
  return res.json();
}
