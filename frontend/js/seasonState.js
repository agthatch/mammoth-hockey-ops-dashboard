import { fetchJson } from './api.js';

let selectedSeasonId = null;
const changeListeners = new Set();

export function getSelectedSeasonId() {
  return selectedSeasonId;
}

export function onSeasonChange(callback) {
  changeListeners.add(callback);
  return () => changeListeners.delete(callback);
}

function notifySeasonChange() {
  for (const listener of changeListeners) {
    listener(selectedSeasonId);
  }
}

function populateSeasonSelect(seasons, defaultId) {
  const select = document.getElementById('season-select');
  if (!select) {
    return;
  }

  select.replaceChildren();

  for (const season of seasons) {
    const option = document.createElement('option');
    option.value = season.id;
    option.textContent = season.label;
    select.appendChild(option);
  }

  selectedSeasonId = defaultId;
  select.value = defaultId;

  select.addEventListener('change', () => {
    selectedSeasonId = select.value;
    notifySeasonChange();
  });
}

export async function initSeasonState() {
  const data = await fetchJson('/seasons');
  populateSeasonSelect(data.seasons, data.default);
  return data;
}
