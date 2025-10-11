import React from "react";

export default function Footer(){
  return (
    <footer className="bg-gray-50 border-t mt-8">
      <div className="max-w-6xl mx-auto px-4 py-6 text-sm text-gray-600">
        BizWise — demo app. Uses OpenStreetMap data and free APIs. © {new Date().getFullYear()}
      </div>
    </footer>
  );
}
