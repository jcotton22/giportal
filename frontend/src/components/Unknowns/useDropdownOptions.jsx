// useDropdownOptions.js
import api from "../../api";
import { useState, useEffect } from "react";

const toOptions = (list = []) =>
  list.map((o) => {
    if (typeof o === "string") return { value: o, label: o };
    const value = o?.value ?? o?.id ?? o?.name ?? String(o);
    const label = o?.label ?? o?.name ?? o?.value ?? String(o);
    return { value, label };
  });

export default function useDropdownOptions(path) {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!path) { setOptions([]); setLoading(false); return; }

    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(path);
        const items = Array.isArray(res.data?.results) ? res.data.results : res.data;
        if (!cancelled) setOptions(toOptions(items || []));
      } catch (e) {
        if (!cancelled) setError(e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [path]);
  return options
}
