import axios from "axios";

const baseUrl = "http://127.0.0.1:8000"

const api = axios.create({
    baseURL: baseUrl,
    headers: {
        "Content-Type": "application/json"
    }
});


api.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    config.headers = config.headers || {};
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});


export default api;