
window.chart = LightweightCharts.createChart(document.getElementById('chart'), {
    layout: {
        background: { color: '#0f172a' },
        textColor: '#d1d5db',
    },
    grid: {
        vertLines: { color: '#1f2933' },
        horzLines: { color: '#1f2933' },
    },
    timeScale: {
        timeVisible: true,
        secondsVisible: false,
    }
});

window.candleSeries = chart.addCandlestickSeries({
    upColor: '#10b981',
    downColor: '#ef4444',
    borderUpColor: '#10b981',
    borderDownColor: '#ef4444',
    wickUpColor: '#10b981',
    wickDownColor: '#ef4444',
});

// Static demo candle data
window.candleSeries.setData([
    { time: '2025-01-01', open: 2060, high: 2080, low: 2050, close: 2075 },
    { time: '2025-01-02', open: 2075, high: 2090, low: 2060, close: 2085 },
    { time: '2025-01-03', open: 2085, high: 2100, low: 2070, close: 2095 },
    { time: '2025-01-04', open: 2095, high: 2110, low: 2080, close: 2105 }
]);

// Overlay toggling logic
window.activeOverlays = {
  gann: true,
  astro: false,
  ict: false,
  imbalance: false,
  liquidity: false,
  smt: false
};

function toggleOverlay(module) {
  if (module === 'journal') {
    const jp = document.getElementById('journal-panel');
    jp.style.display = jp.style.display === 'none' ? 'block' : 'none';
    return;
  }
  window.activeOverlays[module] = !window.activeOverlays[module];
  // Call update function for overlays (to be implemented in gann_events.js and other modules)
  if (window.updateOverlays) window.updateOverlays();
}
