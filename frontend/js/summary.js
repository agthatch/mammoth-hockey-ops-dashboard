import { fetchTeamSummary } from './api.js';

const SUMMARY_VALUE_IDS = [
  'summary-games-played',
  'summary-record',
  'summary-points',
  'summary-goals-for',
  'summary-goals-against',
  'summary-goal-differential',
];

const PLACEHOLDER = '—';
const LOADING_LABEL = '…';

function formatRecord(wins, losses, otLosses) {
  return `${wins}-${losses}-${otLosses}`;
}

function formatGoalDifferential(value) {
  if (value > 0) {
    return `+${value}`;
  }
  return String(value);
}

function setElementText(id, text) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = text;
  }
}

function setSummaryStatus(message) {
  const status = document.getElementById('summary-status');
  if (!status) {
    return;
  }

  if (message) {
    status.textContent = message;
    status.classList.remove('hidden');
  } else {
    status.textContent = '';
    status.classList.add('hidden');
  }
}

export function setSummaryLoading(isLoading) {
  const label = isLoading ? LOADING_LABEL : PLACEHOLDER;

  for (const id of SUMMARY_VALUE_IDS) {
    const el = document.getElementById(id);
    if (!el) {
      continue;
    }
    el.textContent = label;
    el.classList.toggle('metric-value-loading', isLoading);
  }

  if (isLoading) {
    setSummaryStatus(null);
  }
}

export function renderTeamSummary(data) {
  setSummaryStatus(null);

  setElementText('summary-games-played', String(data.games_played));
  setElementText(
    'summary-record',
    formatRecord(data.wins, data.losses, data.ot_losses)
  );
  setElementText('summary-points', String(data.points));
  setElementText('summary-goals-for', String(data.goals_for));
  setElementText('summary-goals-against', String(data.goals_against));

  const diffEl = document.getElementById('summary-goal-differential');
  if (diffEl) {
    diffEl.textContent = formatGoalDifferential(data.goal_differential);
    diffEl.classList.remove('metric-value-loading', 'text-mammoth-400', 'text-red-400');
    if (data.goal_differential > 0) {
      diffEl.classList.add('text-mammoth-400');
    } else if (data.goal_differential < 0) {
      diffEl.classList.add('text-red-400');
    }
  }

  for (const id of SUMMARY_VALUE_IDS) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove('metric-value-loading');
    }
  }
}

export function renderSummaryError(message) {
  setSummaryStatus(message || 'Unable to load team summary');
  setSummaryLoading(false);

  for (const id of SUMMARY_VALUE_IDS) {
    const el = document.getElementById(id);
    if (!el) {
      continue;
    }
    el.textContent = PLACEHOLDER;
    el.classList.remove('metric-value-loading', 'text-mammoth-400', 'text-red-400');
  }
}

export async function loadTeamSummary(options = {}) {
  setSummaryLoading(true);

  try {
    const data = await fetchTeamSummary(options);
    renderTeamSummary(data);
    return data;
  } catch {
    renderSummaryError('Unable to load team summary');
    return null;
  }
}
