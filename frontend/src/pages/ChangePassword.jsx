// src/pages/ChangePassword.jsx
import { useState } from "react";
import { auth } from "../apiClient";

export default function ChangePassword() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      await auth.changePassword({ old_password: oldPassword, new_password: newPassword });
      setMsg("Password changed.");
    } catch (err) {
      setMsg(err.response?.data?.detail || "Failed to change password.");
    }
  };

  return (
    <div className="change-password-container">
      <h3>Change password</h3>
      <form onSubmit={submit}>
        <input
          type="password"
          placeholder="Old password"
          value={oldPassword}
          onChange={(e) => setOldPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="New password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />
        <button>Change</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  );
}
