// src/pages/Login.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../AuthContext";

import "../styles/Login.css"

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      await login(username, password);
      nav("/home");
    } catch (err) {
      setMsg(err.response?.data?.detail || "Login failed.");
    }
  };

  return (
    <div className="login-container">
      <h3>Login</h3>
      <form onSubmit={submit}>
        <input
          type="email"
          placeholder="email@hospital.ca"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button>Log in</button>
      </form>
      {msg && <p>{msg}</p>}
      <p>Need an account? <Link to="/register">Register</Link></p>
    </div>
  );
}
