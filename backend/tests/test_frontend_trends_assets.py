from pathlib import Path

import pytest

from app.config.settings import settings

FRONTEND_DIR = settings.resolved_frontend_dir


@pytest.fixture
def frontend_dir():
    if not FRONTEND_DIR.is_dir():
        pytest.skip("frontend directory not available")
    return FRONTEND_DIR


def test_index_html_includes_season_selector(frontend_dir):
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")

    assert 'id="season-select"' in html
    assert 'for="season-select"' in html
    assert ">Season</label>" in html or ">Season<" in html


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


def test_app_js_loads_trends_on_init(frontend_dir):
    app_js = (frontend_dir / "js" / "app.js").read_text(encoding="utf-8")

    assert "loadTrends" in app_js
    assert "reloadDashboard" in app_js
    assert "initSeasonState" in app_js
    assert "onSeasonChange" in app_js
    assert "getSelectedSeasonId" in app_js
    assert "initPlaceholderCharts" not in app_js
    assert "20252026" not in app_js
    assert "20262027" not in app_js
