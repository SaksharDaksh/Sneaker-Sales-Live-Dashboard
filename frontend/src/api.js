import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

/**
 * Polls a given KPI endpoint every `intervalMs` and keeps the latest
 * result in state. Used by every chart/card on the dashboard so the
 * whole page updates live as new sales come in from the generator.
 */
export function useLiveData(endpoint, intervalMs = 5000) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        const res = await fetch(`${API_URL}${endpoint}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (!cancelled) {
          setData(json);
          setError(null);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      }
    }

    fetchData();
    const id = setInterval(fetchData, intervalMs);

    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [endpoint, intervalMs]);

  return { data, error, loading };
}
