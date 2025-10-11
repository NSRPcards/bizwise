import React, { useState } from "react";
import SearchForm from "../components/SearchForm";
import AreaCard from "../components/AreaCard";
import MapView from "../components/MapView";
import { fetchRecommendations } from "../api";

export default function Home() {
  const [areas, setAreas] = useState([]);
  const [center, setCenter] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async ({ category, city, max_rent }) => {
    setLoading(true);
    try {
      const data = await fetchRecommendations({
        city,
        businessType: category,           // ✅ backend expects "businessType"
        monthlyBudget: parseFloat(max_rent || 0), // ✅ backend expects float
        targetPersonas: [],               // ✅ placeholder (you can add later)
        top: 5,                           // optional limit
      });

      setAreas(data);
      if (data.length) setCenter([data[0].lat, data[0].lng]);
    } catch (e) {
      console.error(e);
      alert("Failed to fetch recommendations (backend must be running).");
    } finally {
      setLoading(false);
    }
  };

  const viewOnMap = (area) => {
    setCenter([area.lat, area.lng]);
    const el = document.querySelector(".map-container");
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  return (
    <div className="py-8">
      <div className="max-w-6xl mx-auto px-4">
        <section className="text-center py-8">
          <h1 className="text-4xl font-bold text-slate-800">
            Find the perfect location for your business
          </h1>
          <p className="mt-2 text-gray-600">
            Search by category, city and rent — BizWise scores areas using BLSI.
          </p>
        </section>

        <SearchForm onSearch={handleSearch} />

        {loading && <p className="text-center mt-6">Loading...</p>}

        {!loading && areas.length > 0 && (
          <div className="grid md:grid-cols-2 gap-4 mt-6">
            <div className="space-y-4">
              {areas.map((a) => (
                <AreaCard key={a.areaId} area={a} onViewMap={viewOnMap} /> // ✅ areaId not id
              ))}
            </div>

            <div>
              <MapView areas={areas} center={center} />
            </div>
          </div>
        )}

        {!loading && areas.length === 0 && (
          <div className="text-center mt-8 text-gray-500">
            Search to see recommended areas.
          </div>
        )}
      </div>
    </div>
  );
}
