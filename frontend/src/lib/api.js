// lib/api.js
import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 15000, // prevent infinite hangs
});

// Optional: Auto error logging
api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API Error:", err?.response || err);
    return Promise.reject(err);
  }
);
