import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // redirect to dashboard if already logged in
    if (localStorage.getItem("adminToken")) {
      navigate("/admin/dashboard");
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await axios.post("http://localhost:8000/admin/login", {
        username,
        password,
      });

      if (res.data.success) {
        localStorage.setItem("adminToken", "true");
        navigate("/admin/dashboard"); // redirect to dashboard
      } else {
        setError("Invalid credentials");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "100px" }}>
      <form
        onSubmit={handleLogin}
        style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "10px", width: "300px" }}
      >
        <h2>Admin Login</h2>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ margin: "5px 0", padding: "8px", width: "100%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ margin: "5px 0", padding: "8px", width: "100%" }}
        />
        <button type="submit" style={{ padding: "8px 12px", marginTop: "10px", width: "100%" }}>
          Login
        </button>
      </form>
    </div>
  );
}
