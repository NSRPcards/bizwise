import React from "react";

export default function AreaCard({ area, onViewMap }) {
  if (!area) return null;

  // badges are already an array from backend
  const badgeList = area.badges || [];

  return (
    <div className="p-4 border rounded shadow hover:shadow-lg transition duration-200">
      <h2 className="text-xl font-semibold text-slate-800">{area.name}</h2>
      <p className="text-gray-600 mt-1">BLSI Score: {area.blsi}</p>

      {badgeList.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {badgeList.map((b, i) => (
            <span
              key={i}
              className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
            >
              {b}
            </span>
          ))}
        </div>
      )}

      <button
        onClick={() => onViewMap(area)}
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition duration-200"
      >
        View on Map
      </button>
    </div>
  );
}
