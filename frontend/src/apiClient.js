// myapp/src/apiClient.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const tokenStore = {
  get access() { return localStorage.getItem("access") || null; },
  set access(v) { v ? localStorage.setItem("access", v) : localStorage.removeItem("access"); },
  get refresh() { return localStorage.getItem("refresh") || null; },
  set refresh(v) { v ? localStorage.setItem("refresh", v) : localStorage.removeItem("refresh"); },
  clear() { localStorage.removeItem("access"); localStorage.removeItem("refresh"); },
};

export const api = axios.create({ baseURL: API_BASE });

// Attach access token
api.interceptors.request.use((config) => {
  const token = tokenStore.access;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-refresh on 401
let isRefreshing = false;
let pending = [];
function onRefreshed(newAccess) { pending.forEach((cb) => cb(newAccess)); pending = []; }

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry && tokenStore.refresh) {
      original._retry = true;

      if (isRefreshing) {
        return new Promise((resolve) => {
          pending.push((newAccess) => {
            original.headers.Authorization = `Bearer ${newAccess}`;
            resolve(api(original));
          });
        });
      }

      try {
        isRefreshing = true;
        const r = await axios.post(`${API_BASE}/auth/refresh/`, { refresh: tokenStore.refresh });
        const newAccess = r.data.access;
        tokenStore.access = newAccess;
        isRefreshing = false;
        onRefreshed(newAccess);
        original.headers.Authorization = `Bearer ${newAccess}`;
        return api(original);
      } catch {
        isRefreshing = false;
        tokenStore.clear();
      }
    }
    return Promise.reject(error);
  }
);

export const auth = {
  async login({ username, password }) {
    const r = await axios.post(`${API_BASE}/auth/login/`, { username, password });
    tokenStore.access = r.data.access;
    tokenStore.refresh = r.data.refresh;
    return r.data;
  },
  async logout() { tokenStore.clear(); },
  async registerStart(email) { return axios.post(`${API_BASE}/auth/register/`, { email }); },
  async registerComplete({ uid, token, new_password }) {
    return axios.post(`${API_BASE}/auth/activate/`, { uid, token, new_password });
  },
  async changePassword({ old_password, new_password }) {
    return api.post(`/auth/change-password/`, { old_password, new_password });
  },
  tokens: tokenStore,
};