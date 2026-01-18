const API_URL = "http://127.0.0.1:8000";

async function apiRequest(url, options = {}) {
  const token = localStorage.getItem("token");

  const headers = options.headers || {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return fetch(API_URL + url, {
    ...options,
    headers,
  });
}