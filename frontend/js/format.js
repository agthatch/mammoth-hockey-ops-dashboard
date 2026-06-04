const SYNC_TIMESTAMP_FORMAT = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  year: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
  timeZoneName: 'short',
});

/**
 * Format a UTC ISO sync timestamp for display in the user's locale.
 * @param {string | null | undefined} isoString
 * @returns {string | null} Formatted string, or null if invalid
 */
export function formatSyncTimestamp(isoString) {
  if (!isoString) {
    return null;
  }

  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) {
    return null;
  }

  return SYNC_TIMESTAMP_FORMAT.format(date);
}
