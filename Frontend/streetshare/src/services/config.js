const fallbackApiBaseUrl = "http://localhost:8000";

export const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || fallbackApiBaseUrl).replace(/\/+$/, "");

export function buildApiUrl(path = "") {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${apiBaseUrl}${normalizedPath}`;
}
