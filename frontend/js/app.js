import { checkHealth } from './api.js';
import { loadTeamSummary } from './summary.js';
import { loadTrends } from './trends.js';

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
  const healthPromise = checkHealth()
    .then((health) => {
      updateConnectionStatus(true, health.app ? `Connected — ${health.app}` : 'Connected');
    })
    .catch(() => {
      updateConnectionStatus(false);
    });

  const summaryPromise = loadTeamSummary();
  const trendsPromise = loadTrends();

  await Promise.all([healthPromise, summaryPromise, trendsPromise]);

  updateLastUpdated();
}

init();
