import React, { createContext, useContext, useEffect, useState } from "react";
import { auth } from "./apiClient";

const AuthCtx = createContext(null);

function decodeJwt(t) {
  try { return JSON.parse(atob(t.split(".")[1])); } catch { return null; }
}
function isAccessValid() {
  const t = auth.tokens.access;
  if (!t) return false;
  const payload = decodeJwt(t);
  if (!payload?.exp) return false;
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp <= now) { auth.tokens.clear(); return false; }
  return true;
}

export function AuthProvider({ children }) {
  const [ready, setReady] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(isAccessValid());
    setReady(true);
  }, []);

  const login = async (username, password) => {
    await auth.login({ username, password });
    setIsAuthenticated(true);
  };
  const logout = async () => { await auth.logout(); setIsAuthenticated(false); };

  return (
    <AuthCtx.Provider value={{ ready, isAuthenticated, login, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}
export function useAuth() { return useContext(AuthCtx); }
