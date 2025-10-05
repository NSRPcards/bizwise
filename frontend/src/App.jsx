import { useEffect, useState } from "react";
import { getBusinesses } from "./api";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import "leaflet/dist/leaflet.css";

function App() {
  const [businesses, setBusinesses] = useState([]);
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");

  const fetchData = async () => {
    try {
      const data = await getBusinesses({ city, category });
      setBusinesses(data);
    } catch (err) {
      console.error("Error fetching businesses:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchData();
  };

  return (
    <>
      <Navbar />
      <Home businesses={businesses} />

      <div style={{ padding: "20px" }}>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Enter city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={{ marginRight: "10px" }}
          />
          <input
            type="text"
            placeholder="Enter category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            style={{ marginRight: "10px" }}
          />
          <button type="submit">Search</button>
        </form>

        {businesses.length === 0 ? (
          <p style={{ marginTop: "20px" }}>No businesses found.</p>
        ) : (
          <ul style={{ marginTop: "20px" }}>
            {businesses.map((b) => (
              <li key={b.id}>
                {b.name} - {b.location} ({b.category})
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default App;
