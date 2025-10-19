import React from "react";
import { Link } from "react-router-dom";

export default function Navbar(){
  return (
    <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <div className="bg-white/10 p-2 rounded"><strong>BW</strong></div>
          <div>
            <div className="text-lg font-bold">BizWise</div>
            <div className="text-xs opacity-80">Smart Business Location Intelligence</div>
          </div>
        </Link>
        <nav className="space-x-4">
          <Link to="/" className="hover:underline">Home</Link>
          <Link to="/admin/login" className="hover:underline">Admin</Link>
        </nav>
      </div>
    </header>
  );
}
