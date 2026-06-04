import { initSeasonState, getSelectedSeasonId, onSeasonChange } from './seasonState.js';
import {
  initRefreshButton,
  loadSeasonSyncStatus,
  renderSyncInitError,
} from './seasonSync.js';
import { loadTeamSummary } from './summary.js';
import { loadTrends } from './trends.js';

function updateLastUpdated() {
  const el = document.getElementById('last-updated');
  if (el) {
    el.textContent = `Last updated: ${new Date().toLocaleString()}`;
  }
}

export async function refreshDashboard() {
  const season = getSelectedSeasonId();
  const options = season ? { season } : {};

  const [statusResult, summaryResult, trendsResult] = await Promise.all([
    loadSeasonSyncStatus(options),
    loadTeamSummary(options),
    loadTrends(options),
  ]);

  if (statusResult !== null || summaryResult !== null || trendsResult !== null) {
    updateLastUpdated();
  }
}

async function init() {
  try {
    await initSeasonState();
  } catch {
    renderSyncInitError();
    return;
  }

  onSeasonChange(() => {
    refreshDashboard();
  });

  initRefreshButton(refreshDashboard);

  await refreshDashboard();
}

init();
