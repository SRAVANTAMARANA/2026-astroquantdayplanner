const chart = LightweightCharts.createChart(
    document.getElementById('chart'),
    {
        layout: {
            background: { color: '#0f172a' },
            textColor: '#cbd5e1',
        },
        grid: {
            vertLines: { color: '#1e293b' },
            horzLines: { color: '#1e293b' },
        },
        timeScale: { timeVisible: true },
    }
);

const candleSeries = chart.addCandlestickSeries();
let priceData = [];

fetch("http://localhost:8000/price")
  .then(res => res.json())
  .then(data => {
    priceData = data;
    candleSeries.setData(data);
  });

// Load ICT concepts (FVG, OB, SMT, Killzones) from backend
fetch("http://localhost:8000/concepts")
  .then(res => res.json())
  .then(concepts => {
    concepts.forEach(obj => {
      if (obj.type === "FVG") drawFVG(obj);
      if (obj.type === "OB") {
        const obZone = drawOrderBlock(obj);
        if (obj.mitigated) animateMitigation(obZone);
      }
      if (obj.type === "SMT") drawSMT(obj);
      if (obj.type === "KILLZONE") drawKillzone(obj.from, obj.to, obj.label);
    });
  });
