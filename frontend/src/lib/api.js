import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 15000,
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API Error:", err?.response || err);
    return Promise.reject(err);
  }
);
