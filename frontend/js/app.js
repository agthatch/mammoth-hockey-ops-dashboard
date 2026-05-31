import { checkHealth } from './api.js';
import { initPlaceholderCharts } from './charts.js';

function updateConnectionStatus(connected, detail) {
  const badge = document.getElementById('connection-status');
  const label = document.getElementById('connection-label');

  badge.classList.remove('status-connected', 'status-error');

  if (connected) {
    badge.classList.add('status-connected');
    label.textContent = detail || 'Connected';
  } else {
    badge.classList.add('status-error');
    label.textContent = detail || 'Backend unavailable';
  }
}

function updateLastUpdated() {
  const el = document.getElementById('last-updated');
  if (el) {
    el.textContent = `Last updated: ${new Date().toLocaleString()}`;
  }
}

async function init() {
  initPlaceholderCharts();

  try {
    const health = await checkHealth();
    updateConnectionStatus(true, health.app ? `Connected — ${health.app}` : 'Connected');
  } catch {
    updateConnectionStatus(false);
  }

  updateLastUpdated();
}

init();
