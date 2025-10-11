import React, { useState } from "react";

export default function SearchForm({ onSearch }) {
  const [category, setCategory] = useState("");
  const [city, setCity] = useState("");
  const [maxRent, setMaxRent] = useState("");

  const submit = (e) => {
    e.preventDefault();
    onSearch({ category, city, max_rent: maxRent });
  };

  return (
    <form onSubmit={submit} className="bg-white p-6 rounded-lg shadow max-w-4xl mx-auto transform -translate-y-8">
      <div className="flex flex-col md:flex-row gap-3">
        <input value={category} onChange={e=>setCategory(e.target.value)} placeholder="Business category (e.g. cafe)" className="flex-1 p-3 border rounded" />
        <input value={city} onChange={e=>setCity(e.target.value)} placeholder="City (e.g. Pune)" className="flex-1 p-3 border rounded" />
        <input value={maxRent} onChange={e=>setMaxRent(e.target.value)} placeholder="Max rent (₹)" className="w-40 p-3 border rounded" />
        <button className="bg-blue-600 text-white px-4 py-3 rounded shadow hover:bg-blue-700 transition">Find Areas</button>
      </div>
      <p className="mt-3 text-xs text-gray-500">Tip: Leave fields blank to search all.</p>
    </form>
  );
}
