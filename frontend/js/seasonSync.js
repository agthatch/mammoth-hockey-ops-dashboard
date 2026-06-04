import { ApiError, fetchSeasonStatus, postIngestSchedule } from './api.js';
import { formatSyncTimestamp } from './format.js';
import { getSelectedSeasonId } from './seasonState.js';

const REFRESH_LABEL = 'Refresh NHL Data';
const REFRESHING_LABEL = 'Refreshing...';
const SUCCESS_MESSAGE = '✓ Refresh Complete';
const SUCCESS_DISPLAY_MS = 2000;

const INGEST_ERROR_GENERIC = 'Unable to refresh NHL data.';
const INGEST_ERROR_NHL = 'NHL API unavailable.';
const STATUS_ERROR_MESSAGE = 'Unable to load sync status.';
const INIT_ERROR_MESSAGE = 'Backend unavailable.';

let refreshInProgress = false;

function getSyncValueEl() {
  return document.getElementById('season-sync-value');
}

function getSyncMessageEl() {
  return document.getElementById('season-sync-message');
}

function getRefreshButton() {
  return document.getElementById('refresh-nhl-data');
}

function setSyncMessage(message, options = {}) {
  const el = getSyncMessageEl();
  if (!el) {
    return;
  }

  const { isError = false, isSuccess = false } = options;

  if (message) {
    el.textContent = message;
    el.classList.remove('hidden', 'sync-message-error', 'sync-message-success');
    if (isError) {
      el.classList.add('sync-message-error');
    } else if (isSuccess) {
      el.classList.add('sync-message-success');
    }
  } else {
    el.textContent = '';
    el.classList.add('hidden');
    el.classList.remove('sync-message-error', 'sync-message-success');
  }
}

function setSyncValueLoading() {
  const el = getSyncValueEl();
  if (!el) {
    return;
  }

  el.textContent = 'Loading…';
  el.classList.remove('sync-value-never');
}

export function renderSeasonSyncStatus(data) {
  const el = getSyncValueEl();
  if (!el) {
    return;
  }

  setSyncMessage(null);

  if (!data || data.last_sync_at == null) {
    el.textContent = 'Never Synced';
    el.classList.add('sync-value-never');
    return;
  }

  const formatted = formatSyncTimestamp(data.last_sync_at);
  if (!formatted) {
    el.textContent = 'Never Synced';
    el.classList.add('sync-value-never');
    return;
  }

  el.textContent = formatted;
  el.classList.remove('sync-value-never');
}

export function renderSyncInitError() {
  const el = getSyncValueEl();
  if (el) {
    el.textContent = '—';
    el.classList.remove('sync-value-never');
  }
  setSyncMessage(INIT_ERROR_MESSAGE, { isError: true });
  setRefreshButtonEnabled(false);
}

function setRefreshButtonEnabled(enabled) {
  const button = getRefreshButton();
  if (!button) {
    return;
  }

  button.disabled = !enabled || refreshInProgress;
  button.classList.toggle('refresh-btn-disabled', button.disabled);
}

function setRefreshButtonLabel(label) {
  const button = getRefreshButton();
  if (button) {
    button.textContent = label;
  }
}

function setRefreshingState(isRefreshing) {
  refreshInProgress = isRefreshing;
  const button = getRefreshButton();
  if (!button) {
    return;
  }

  button.disabled = isRefreshing;
  button.classList.toggle('refresh-btn-disabled', isRefreshing);
  button.textContent = isRefreshing ? REFRESHING_LABEL : REFRESH_LABEL;
}

function mapIngestError(error) {
  if (error instanceof ApiError && error.status === 502) {
    return INGEST_ERROR_NHL;
  }
  return INGEST_ERROR_GENERIC;
}

export async function loadSeasonSyncStatus(options = {}) {
  if (!options.season) {
    renderSeasonSyncStatus(null);
    return null;
  }

  setSyncValueLoading();

  try {
    const data = await fetchSeasonStatus(options);
    renderSeasonSyncStatus(data);
    return data;
  } catch {
    const el = getSyncValueEl();
    if (el) {
      el.textContent = '—';
      el.classList.remove('sync-value-never');
    }
    setSyncMessage(STATUS_ERROR_MESSAGE, { isError: true });
    return null;
  }
}

/**
 * POST ingest for the season, then refresh dashboard data via callback.
 * @param {{ season?: string }} options
 * @param {() => Promise<void>} refreshDashboard
 */
export async function refreshNhlData(options, refreshDashboard) {
  if (refreshInProgress) {
    return false;
  }

  setSyncMessage(null);
  setRefreshingState(true);

  try {
    await postIngestSchedule(options);
    await refreshDashboard();
    setSyncMessage(SUCCESS_MESSAGE, { isSuccess: true });
    setTimeout(() => {
      setSyncMessage(null);
    }, SUCCESS_DISPLAY_MS);
    return true;
  } catch (error) {
    setSyncMessage(mapIngestError(error), { isError: true });
    return false;
  } finally {
    setRefreshingState(false);
    setRefreshButtonEnabled(true);
  }
}

export function initRefreshButton(refreshDashboard) {
  const button = getRefreshButton();
  if (!button) {
    return;
  }

  button.addEventListener('click', () => {
    const season = getSelectedSeasonId();
    const options = season ? { season } : {};
    refreshNhlData(options, refreshDashboard);
  });
}
