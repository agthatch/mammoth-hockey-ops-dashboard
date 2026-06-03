const CHART_THEME = {
  chart: {
    backgroundColor: 'transparent',
    style: { fontFamily: 'inherit' },
  },
  title: { style: { color: '#e2e8f0', fontSize: '14px', fontWeight: '500' } },
  subtitle: { style: { color: '#64748b' } },
  xAxis: {
    labels: { style: { color: '#94a3b8' } },
    title: { style: { color: '#94a3b8' } },
    lineColor: '#334155',
    tickColor: '#334155',
    gridLineColor: '#1e293b',
  },
  yAxis: {
    labels: { style: { color: '#94a3b8' } },
    title: { style: { color: '#94a3b8' } },
    gridLineColor: '#1e293b',
  },
  legend: {
    itemStyle: { color: '#cbd5e1' },
    itemHoverStyle: { color: '#f1f5f9' },
  },
  credits: { enabled: false },
};

const COLOR_PRIMARY = '#14b8a6';
const COLOR_ROLLING = '#94a3b8';

const TREND_CHART_CONFIGS = [
  {
    containerId: 'chart-goal-differential-trend',
    errorId: 'chart-goal-differential-error',
    title: 'Goal Differential Trend',
    yAxisTitle: 'Goal Differential',
    valueKey: 'goal_differential',
    rollingKey: 'rolling_goal_differential',
    valueLabel: 'Goal Differential',
    rollingLabel: '5-Game Rolling Goal Differential',
  },
  {
    containerId: 'chart-goals-for-trend',
    errorId: 'chart-goals-for-error',
    title: 'Goals For Trend',
    yAxisTitle: 'Goals',
    valueKey: 'goals_for',
    rollingKey: 'rolling_goals_for',
    valueLabel: 'Goals For',
    rollingLabel: '5-Game Rolling Goals For',
  },
  {
    containerId: 'chart-goals-against-trend',
    errorId: 'chart-goals-against-error',
    title: 'Goals Against Trend',
    yAxisTitle: 'Goals',
    valueKey: 'goals_against',
    rollingKey: 'rolling_goals_against',
    valueLabel: 'Goals Against',
    rollingLabel: '5-Game Rolling Goals Against',
  },
];

const CHART_CONTAINER_IDS = TREND_CHART_CONFIGS.map((config) => config.containerId);

let resizeListenerAttached = false;

export function buildTrendCategories(games) {
  return games.map((game) => game.game_date);
}

export function buildTrendSeries(games, valueKey, rollingKey) {
  return {
    values: games.map((game) => game[valueKey]),
    rolling: games.map((game) => game[rollingKey]),
  };
}

function formatSharedTrendTooltip() {
  let html = `<b>${this.x}</b><br/>`;

  for (const point of this.points) {
    const decimals = point.series.tooltipOptions.valueDecimals ?? 0;
    const value = Highcharts.numberFormat(point.y, decimals);
    html += `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: <b>${value}</b><br/>`;
  }

  return html;
}

function destroyChart(containerId) {
  const existing = Highcharts.charts.find(
    (chart) => chart && chart.renderTo && chart.renderTo.id === containerId
  );
  if (existing) {
    existing.destroy();
  }
}

function setChartError(errorId, message) {
  const el = document.getElementById(errorId);
  if (!el) {
    return;
  }

  if (message) {
    el.textContent = message;
    el.classList.remove('hidden');
  } else {
    el.textContent = '';
    el.classList.add('hidden');
  }
}

function attachResizeListener() {
  if (resizeListenerAttached) {
    return;
  }

  window.addEventListener('resize', () => {
    for (const chart of Highcharts.charts) {
      if (chart && CHART_CONTAINER_IDS.includes(chart.renderTo?.id)) {
        chart.reflow();
      }
    }
  });
  resizeListenerAttached = true;
}

export function createTrendLineChart({
  containerId,
  title,
  yAxisTitle,
  games,
  valueKey,
  rollingKey,
  valueLabel,
  rollingLabel,
}) {
  destroyChart(containerId);

  const categories = buildTrendCategories(games);
  const { values, rolling } = buildTrendSeries(games, valueKey, rollingKey);
  const isEmpty = games.length === 0;

  return Highcharts.chart(containerId, {
    ...CHART_THEME,
    chart: {
      ...CHART_THEME.chart,
      type: 'line',
    },
    title: { ...CHART_THEME.title, text: title },
    subtitle: isEmpty
      ? { ...CHART_THEME.subtitle, text: 'No games in selected period' }
      : { text: null },
    xAxis: {
      ...CHART_THEME.xAxis,
      categories,
      title: { text: 'Game Date' },
    },
    yAxis: {
      ...CHART_THEME.yAxis,
      title: { text: yAxisTitle },
    },
    tooltip: {
      shared: true,
      formatter: formatSharedTrendTooltip,
      backgroundColor: '#1e293b',
      borderColor: '#334155',
      style: { color: '#e2e8f0' },
    },
    series: [
      {
        name: valueLabel,
        data: values,
        color: COLOR_PRIMARY,
        lineWidth: 2,
        marker: { radius: 3 },
        tooltip: {
          valueDecimals: 0,
        },
      },
      {
        name: rollingLabel,
        data: rolling,
        color: COLOR_ROLLING,
        dashStyle: 'Dash',
        lineWidth: 2,
        marker: { enabled: false },
        tooltip: {
          valueDecimals: 2,
        },
      },
    ],
  });
}

export function clearTrendCharts() {
  for (const config of TREND_CHART_CONFIGS) {
    destroyChart(config.containerId);
    setChartError(config.errorId, null);
  }
}

export function renderTrendCharts(trendsData) {
  const games = trendsData?.games ?? [];
  const errors = [];

  attachResizeListener();

  for (const config of TREND_CHART_CONFIGS) {
    setChartError(config.errorId, null);

    try {
      createTrendLineChart({
        containerId: config.containerId,
        title: config.title,
        yAxisTitle: config.yAxisTitle,
        games,
        valueKey: config.valueKey,
        rollingKey: config.rollingKey,
        valueLabel: config.valueLabel,
        rollingLabel: config.rollingLabel,
      });
    } catch {
      destroyChart(config.containerId);
      setChartError(config.errorId, 'Unable to render chart.');
      errors.push(config.containerId);
    }
  }

  return { errors };
}
