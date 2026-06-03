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

export async function fetchTeamSummary(options = {}) {
  const params = new URLSearchParams();

  if (options.season) {
    params.set('season', options.season);
  }
  if (options.gameType) {
    params.set('game_type', options.gameType);
  }

  const query = params.toString();
  const path = query ? `/team-summary?${query}` : '/team-summary';

  return fetchJson(path);
}
