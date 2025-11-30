// src/api/apiClient.ts
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true, // IMPORTANT: send cookies
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
