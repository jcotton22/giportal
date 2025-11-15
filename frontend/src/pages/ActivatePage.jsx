// src/pages/ActivatePage.jsx
import { useState, useMemo } from "react";
import { useLocation, Link } from "react-router-dom";
import { auth } from "../apiClient";

export default function ActivatePage() {
  const qs = new URLSearchParams(useLocation().search);
  const uid = useMemo(() => qs.get("uid") || "", [qs]);   // <-- uid (not id)
  const token = useMemo(() => qs.get("token") || "", [qs]);

  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      await auth.registerComplete({ uid, token, new_password: password }); // backend accepts both now
      setMsg("Account activated. ");
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.response?.data?.token ||
        err.response?.data?.uid ||
        err.response?.data?.password ||
        "Activation failed.";
      setMsg(String(detail));
    }
  };

  return (
    <div className="set-password-container">
      <h3>Please set your password</h3>
      {!uid || !token ? (
        <p>Missing activation token</p>
      ) : (
        <form onSubmit={submit}> {/* <-- fixed typo */}
          <input
            type="password"
            placeholder="New password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button>Activate</button>
        </form>
      )}
      {msg && (
        <p>
          {msg} {msg.includes("activated") && <Link to="/login">Login</Link>}
        </p>
      )}
    </div>
  );
}
