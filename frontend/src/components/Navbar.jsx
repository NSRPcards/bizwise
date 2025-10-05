import React from "react";

function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <div className="text-xl font-bold">BizWise</div>
      <ul className="flex space-x-6">
        <li><a href="#home" className="hover:underline">Home</a></li>
        <li><a href="#search" className="hover:underline">Search</a></li>
        <li><a href="#about" className="hover:underline">About</a></li>
        <li><a href="#contact" className="hover:underline">Contact</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;
