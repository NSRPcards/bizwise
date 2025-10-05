// frontend/src/components/SearchForm.jsx
import { useState } from "react";

export default function SearchForm({ onSearch }) {
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ city, category });
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
      <input
        type="text"
        placeholder="City"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        className="border p-2 rounded"
      />
      <input
        type="text"
        placeholder="Business Type"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        className="border p-2 rounded"
      />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">
        Search
      </button>
    </form>
  );
}
