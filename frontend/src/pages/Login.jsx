// src/pages/Login.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";


import "../styles/Login.css"

export default function Login() {
  const nav = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log("Sumbit is pressed")

    try {
      const res = await api.post('/login/', { username, password })
      console.log("We have a response ", res);

    } catch (err) {
      setMsg.apply(err.response?.data?.detail || "Registration failed")
      console.log("Error ", err)
    }
    
  };

  return (
    <div className="login-container">
      <h3>Login</h3>
      <form onSubmit={submit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="••••••••••••"
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
