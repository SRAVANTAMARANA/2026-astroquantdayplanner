const chart = LightweightCharts.createChart(document.getElementById('chart'), {
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

const candleSeries = chart.addCandlestickSeries({
    upColor: '#10b981',
    downColor: '#ef4444',
    borderUpColor: '#10b981',
    borderDownColor: '#ef4444',
    wickUpColor: '#10b981',
    wickDownColor: '#ef4444',
});

// Load Gann events from JSON (produced by Python)
fetch('gann_events.json')
    .then(response => response.json())
    .then(data => {
        candleSeries.setData(data.candles);
        window.gannEvents = data;
        // gann_events.js will use window.gannEvents
        if (window.onGannEventsLoaded) window.onGannEventsLoaded();
    });
