import { API_BASE } from './config.js';

export async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function checkHealth() {
  return fetchJson('/health');
}
