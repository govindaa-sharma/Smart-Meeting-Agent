import axios from "axios";

// Adjust if your backend host/port differs
export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});
