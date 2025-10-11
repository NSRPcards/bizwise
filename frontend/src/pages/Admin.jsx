import React, { useEffect, useState } from "react";
import { fetchAdminStats, fetchTopRecommended } from "../api";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";

export default function Admin(){
  const [stats, setStats] = useState(null);
  const [top, setTop] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const s = await fetchAdminStats();
        setStats(s);
        const t = await fetchTopRecommended();
        setTop(t);
      } catch(e) {
        console.error(e);
      }
    })();
  }, []);

  if (!stats) return <div className="p-6">Loading admin...</div>;

  const catLabels = Object.keys(stats.category_count || {});
  const catData = Object.values(stats.category_count || {});

  const locLabels = Object.keys(stats.location_count || {});
  const locData = Object.values(stats.location_count || {});

  return (
    <div className="py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-2xl font-bold mb-4">Admin Dashboard</h2>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-3">Top Categories</h3>
            <Bar data={{ labels: catLabels, datasets: [{ label: "count", data: catData, backgroundColor: "rgba(59,130,246,0.6)" }] }} />
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-3">Top Locations</h3>
            <Bar data={{ labels: locLabels, datasets: [{ label: "count", data: locData, backgroundColor: "rgba(16,185,129,0.6)" }] }} />
          </div>
        </div>

        <div className="mt-6 bg-white p-4 rounded shadow">
          <h3 className="font-semibold mb-3">Top recommended areas</h3>
          <ul className="space-y-2">
            {top.map(t => <li key={t.id}>{t.name} ({t.city}) — BLSI: {Math.round(t.blsi)}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
}
