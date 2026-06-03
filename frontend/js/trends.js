import { fetchTrends } from './api.js';
import { clearTrendCharts, renderTrendCharts } from './charts.js';

const CHART_CONTAINER_IDS = [
  'chart-goal-differential-trend',
  'chart-goals-for-trend',
  'chart-goals-against-trend',
];

const LOADING_MESSAGES = {
  fetch: 'Loading trend data...',
  render: 'Loading charts...',
};

function setTrendsStatus(message, options = {}) {
  const status = document.getElementById('trends-status');
  if (!status) {
    return;
  }

  const { isError = false, isLoading = false } = options;

  if (message) {
    status.textContent = message;
    status.classList.remove('hidden', 'text-red-400', 'text-slate-400');
    status.classList.add(isError ? 'text-red-400' : 'text-slate-400');
    status.setAttribute('role', isError ? 'alert' : 'status');
  } else {
    status.textContent = '';
    status.classList.add('hidden');
  }

  for (const id of CHART_CONTAINER_IDS) {
    const container = document.getElementById(id);
    if (!container) {
      continue;
    }
    container.classList.toggle('chart-loading', isLoading);
  }
}

export function setTrendsLoading(phase) {
  const message = LOADING_MESSAGES[phase];
  if (message) {
    setTrendsStatus(message, { isLoading: true });
  }
}

export function setTrendsError(message) {
  setTrendsStatus(message || 'Unable to load trend data.', { isError: true });
  clearTrendCharts();
}

export async function loadTrends(options = {}) {
  setTrendsLoading('fetch');

  try {
    const data = await fetchTrends(options);
    setTrendsLoading('render');
    renderTrendCharts(data);
    setTrendsStatus(null);
    return data;
  } catch {
    setTrendsError('Unable to load trend data.');
    return null;
  }
}
