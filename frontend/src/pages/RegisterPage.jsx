// src/pages/RegisterPage.jsx
import { useState } from "react";
import { auth } from "../apiClient";

import "../styles/RegisterPage.css"

export default function RegisterPage(){
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      await auth.registerStart(email);
      setMsg("An activation link has been emailed.");
    } catch (err) {
      setMsg(err.response?.data?.email || err.response?.data?.detail || "Error");
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h3>Register</h3>
        <form onSubmit={submit}>
          <input
            type="email"
            placeholder="example@hospital.ca"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button>Send activation e-mail</button>
        </form>

        {msg && (
          <p className={msg.includes("Error") ? "error" : "success"}>
            {msg}
          </p>
        )}
      </div>
    </div>
  );
}
