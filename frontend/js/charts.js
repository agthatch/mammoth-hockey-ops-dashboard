const CHART_THEME = {
  chart: {
    backgroundColor: 'transparent',
    style: { fontFamily: 'inherit' },
  },
  title: { style: { color: '#94a3b8', fontSize: '13px', fontWeight: 'normal' } },
  subtitle: { style: { color: '#64748b' } },
  xAxis: {
    labels: { style: { color: '#94a3b8' } },
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

export function initPlaceholderCharts() {
  Highcharts.chart('chart-goals-trend', {
    ...CHART_THEME,
    chart: { ...CHART_THEME.chart, type: 'line' },
    title: { text: null },
    subtitle: { text: 'No data yet' },
    xAxis: { ...CHART_THEME.xAxis, categories: [] },
    yAxis: { ...CHART_THEME.yAxis, title: { text: 'Goals' } },
    series: [
      { name: 'Goals For', data: [], color: '#14b8a6' },
      { name: 'Goals Against', data: [], color: '#64748b' },
    ],
  });

  Highcharts.chart('chart-goal-diff', {
    ...CHART_THEME,
    chart: { ...CHART_THEME.chart, type: 'column' },
    title: { text: null },
    subtitle: { text: 'No data yet' },
    xAxis: { ...CHART_THEME.xAxis, categories: [] },
    yAxis: { ...CHART_THEME.yAxis, title: { text: 'Differential' } },
    series: [{ name: 'Goal Differential', data: [], color: '#14b8a6' }],
  });
}
