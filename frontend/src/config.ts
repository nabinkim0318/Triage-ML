const isLocal = !process.env.NODE_ENV || process.env.NODE_ENV === "development";

export const API_BASE_URL = isLocal
    ? "http://localhost:8000" // Local testing URL
    : "https://triage-ml.onrender.com"; // Production backend URL