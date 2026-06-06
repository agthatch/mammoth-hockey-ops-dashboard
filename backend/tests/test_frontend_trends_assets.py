from pathlib import Path

import pytest

from app.config.settings import settings

FRONTEND_DIR = settings.resolved_frontend_dir


@pytest.fixture
def frontend_dir():
    if not FRONTEND_DIR.is_dir():
        pytest.skip("frontend directory not available")
    return FRONTEND_DIR


def test_index_html_uses_compiled_tailwind_css(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert "cdn.tailwindcss.com" not in html
    assert 'href="css/tailwind.css"' in html
    assert "tailwind.config" not in html


def test_index_html_includes_ga4_once(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert html.count("G-WBX4XR634B") == 2
    assert html.count("googletagmanager.com/gtag/js") == 1
    assert html.count("gtag('config'") == 1


def test_index_html_includes_season_selector(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert 'id="season-select"' in html
    assert 'for="season-select"' in html
    assert ">Season</label>" in html or ">Season<" in html


def test_index_html_includes_season_sync_ui(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert 'id="season-sync-value"' in html
    assert 'id="refresh-nhl-data"' in html
    assert "Last NHL Sync" in html
    assert 'id="connection-status"' not in html
    assert 'id="connection-dot"' not in html


def test_index_html_includes_trend_chart_containers(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert 'id="trends-status"' in html
    assert 'id="chart-goal-differential-trend"' in html
    assert 'id="chart-goals-for-trend"' in html
    assert 'id="chart-goals-against-trend"' in html
    assert 'id="chart-goal-differential-error"' in html
    assert 'id="chart-goals-for-error"' in html
    assert 'id="chart-goals-against-error"' in html
    assert 'id="chart-goals-trend"' not in html
    assert 'id="chart-goal-diff"' not in html


def test_api_js_exposes_fetch_trends(frontend_dir):
    api_js = (frontend_dir / "js" / "api.js").read_text(encoding="utf-8")

    assert "export async function fetchTrends" in api_js
    assert "export async function fetchSeasons" in api_js
    assert "/trends" in api_js
    assert "/seasons" in api_js
    assert "export class ApiError" in api_js


def test_api_js_exposes_season_sync_and_ingest(frontend_dir):
    api_js = (frontend_dir / "js" / "api.js").read_text(encoding="utf-8")

    assert "export async function fetchSeasonStatus" in api_js
    assert "export async function postIngestSchedule" in api_js
    assert "/season-status" in api_js
    assert "/ingest/schedule" in api_js
    assert "export async function postJson" in api_js


def test_format_js_exports_timestamp_formatter(frontend_dir):
    format_js = (frontend_dir / "js" / "format.js").read_text(encoding="utf-8")

    assert "export function formatSyncTimestamp" in format_js
    assert "Intl.DateTimeFormat" in format_js
    assert "new Date" in format_js


def test_season_sync_js_exports_load_and_refresh(frontend_dir):
    season_sync_js = (frontend_dir / "js" / "seasonSync.js").read_text(encoding="utf-8")

    assert "export async function loadSeasonSyncStatus" in season_sync_js
    assert "export async function refreshNhlData" in season_sync_js
    assert "Never Synced" in season_sync_js
    assert "Refreshing..." in season_sync_js


def test_season_state_js_exports_season_management(frontend_dir):
    season_js = (frontend_dir / "js" / "seasonState.js").read_text(encoding="utf-8")

    assert "export async function initSeasonState" in season_js
    assert "export function getSelectedSeasonId" in season_js
    assert "export function onSeasonChange" in season_js


def test_trends_js_exports_load_trends(frontend_dir):
    trends_js = (frontend_dir / "js" / "trends.js").read_text(encoding="utf-8")

    assert "export async function loadTrends" in trends_js
    assert "Loading trend data..." in trends_js
    assert "Loading charts..." in trends_js
    assert "Unable to load trend data." in trends_js


def test_index_html_includes_highcharts_accessibility_module(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert "modules/accessibility.js" in html
    assert html.index("highcharts.js") < html.index("modules/accessibility.js")


def test_charts_js_includes_accessibility_description(frontend_dir):
    charts_js = (frontend_dir / "js" / "charts.js").read_text(encoding="utf-8")

    assert "accessibility:" in charts_js
    assert "description:" in charts_js


def test_charts_js_renders_highcharts_trend_charts(frontend_dir):
    charts_js = (frontend_dir / "js" / "charts.js").read_text(encoding="utf-8")

    assert "Highcharts.chart" in charts_js
    assert "export function renderTrendCharts" in charts_js
    assert "export function createTrendLineChart" in charts_js
    assert "initPlaceholderCharts" not in charts_js
    assert "5-Game Rolling" in charts_js
    assert "valueDecimals: 2" in charts_js
    assert "formatSharedTrendTooltip" in charts_js
    assert "Highcharts.numberFormat" in charts_js


def test_app_js_wires_season_sync_workflow(frontend_dir):
    app_js = (frontend_dir / "js" / "app.js").read_text(encoding="utf-8")

    assert "loadTrends" in app_js
    assert "refreshDashboard" in app_js
    assert "loadSeasonSyncStatus" in app_js
    assert "initSeasonState" in app_js
    assert "onSeasonChange" in app_js
    assert "getSelectedSeasonId" in app_js
    assert "initRefreshButton" in app_js
    assert "checkHealth" not in app_js
    assert "initPlaceholderCharts" not in app_js
    assert "20252026" not in app_js
    assert "20262027" not in app_js
