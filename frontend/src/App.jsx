// frontend/src/App.jsx
import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import { getBusinesses, getAreas, postRecommendations } from "./api";
import "./app.css"; // small extra styles
import "leaflet/dist/leaflet.css";

function App() {
  const [businesses, setBusinesses] = useState([]);
  const [areas, setAreas] = useState([]);
  const [city, setCity] = useState("Pune");
  const [category, setCategory] = useState("");
  const [top, setTop] = useState(5);
  const [loading, setLoading] = useState(false);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    fetchAreas();
    fetchBusinesses();
    // eslint-disable-next-line
  }, []);

  async function fetchBusinesses() {
    try {
      setLoading(true);
      const data = await getBusinesses({ city, category });
      setBusinesses(data);
    } catch (e) {
      console.error("Error fetching businesses:", e);
      setBusinesses([]);
    } finally {
      setLoading(false);
    }
  }

  async function fetchAreas() {
    try {
      const a = await getAreas();
      setAreas(a);
    } catch (e) {
      console.error("Error fetching areas:", e);
    }
  }

  async function handleRecommend(e) {
    e.preventDefault();
    try {
      const payload = {
        city: city || "Pune",
        businessType: category || "cafe",
        monthlyBudget: 40000,
        targetPersonas: ["students"],
        top: parseInt(top) || 5,
      };
      const r = await postRecommendations(payload);
      setRecs(r);
      // center map on first rec maybe (Home can accept recs)
    } catch (err) {
      console.error("Recommend error:", err);
    }
  }

  return (
    <>
      <Navbar />
      <div className="container">
        <div className="left">
          <h1>BizWise — Smart Location Finder</h1>

          <form onSubmit={(e) => { e.preventDefault(); fetchBusinesses(); }}>
            <div className="row">
              <input value={city} onChange={e => setCity(e.target.value)} placeholder="City (e.g., Pune)" />
              <input value={category} onChange={e => setCategory(e.target.value)} placeholder="Category (cafe, grocery)" />
              <button type="submit">Search Businesses</button>
            </div>
          </form>

          <div className="section">
            <h2>Businesses</h2>
            {loading ? <p>Loading...</p> : (
              businesses.length === 0 ? <p>No businesses found.</p> :
              <ul className="list">
                {businesses.map(b => (
                  <li key={b.id}>
                    <strong>{b.name}</strong><br/>
                    {b.location} — {b.category}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="section">
            <h2>Get Recommendations</h2>
            <form onSubmit={handleRecommend} className="row">
              <input value={top} onChange={e=>setTop(e.target.value)} style={{width:'80px'}}/>
              <button type="submit">Recommend Top</button>
            </form>

            {recs.length > 0 && (
              <div className="rec-list">
                {recs.map(r => (
                  <div className="rec" key={r.areaId}>
                    <h3>{r.name} — BLSI {r.blsi}</h3>
                    <p>Badges: {r.badges.join(", ")}</p>
                    <details>
                      <summary>Breakdown</summary>
                      <pre>{JSON.stringify(r.breakdown, null, 2)}</pre>
                    </details>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="right">
          <Home areas={areas} recs={recs} />
        </div>
      </div>
    </>
  );
}

export default App;
