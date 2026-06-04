import { API_BASE } from './config.js';

export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

function formatErrorDetail(detail) {
  if (typeof detail === 'string') {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || String(item)).join('; ');
  }
  return null;
}

export async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    let detail = null;
    try {
      const body = await response.json();
      detail = formatErrorDetail(body.detail) || response.statusText;
    } catch {
      detail = response.statusText;
    }
    throw new ApiError(
      `Request failed: ${response.status} ${response.statusText}`,
      response.status,
      detail
    );
  }

  return response.json();
}

export async function checkHealth() {
  return fetchJson('/health');
}

export async function fetchSeasons() {
  return fetchJson('/seasons');
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

export async function fetchTrends(options = {}) {
  const params = new URLSearchParams();

  if (options.season) {
    params.set('season', options.season);
  }
  if (options.gameType) {
    params.set('game_type', options.gameType);
  }
  if (options.limit != null) {
    params.set('limit', String(options.limit));
  }

  const query = params.toString();
  const path = query ? `/trends?${query}` : '/trends';

  return fetchJson(path);
}
