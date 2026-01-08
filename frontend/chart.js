// ===============================
// TIME PANEL LOGIC
// ===============================
let timeLines = [];

function drawGannCycle(cycle) {
  clearGannTime();
  if (!priceData.length) return;
  let count = Math.floor(priceData.length / cycle);
  for (let i = 1; i <= count; i++) {
    let idx = i * cycle - 1;
    if (priceData[idx]) {
      let time = priceData[idx].time;
      let line = chart.addLineSeries({ color: '#facc15', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dotted });
      line.setData([
        { time: time, value: priceData[idx].low },
        { time: time, value: priceData[idx].high }
      ]);
      timeLines.push(line);
    }
  }
  if (typeof setStatusBox === 'function') setStatusBox({ time: `${cycle} Cycle`, action: 'Draw Time Cycle' });
}

function drawWeeklyReset() {
  clearGannTime();
  priceData.forEach((bar, i) => {
    // Assume Friday is day 5 (0=Sunday)
    let date = new Date(bar.time);
    if (date.getDay() === 5) {
      let line = chart.addLineSeries({ color: '#38bdf8', lineWidth: 1 });
      line.setData([
        { time: bar.time, value: bar.low },
        { time: bar.time, value: bar.high }
      ]);
      timeLines.push(line);
    }
  });
  if (typeof setStatusBox === 'function') setStatusBox({ time: 'Weekly Reset', action: 'Draw Weekly Reset' });
}

function drawMonthlyReset() {
  clearGannTime();
  let lastMonth = null;
  priceData.forEach((bar, i) => {
    let date = new Date(bar.time);
    let month = date.getMonth();
    if (month !== lastMonth) {
      let line = chart.addLineSeries({ color: '#0ea5e9', lineWidth: 1 });
      line.setData([
        { time: bar.time, value: bar.low },
        { time: bar.time, value: bar.high }
      ]);
      timeLines.push(line);
      lastMonth = month;
    }
  });
  if (typeof setStatusBox === 'function') setStatusBox({ time: 'Monthly Reset', action: 'Draw Monthly Reset' });
}

function clearGannTime() {
  timeLines.forEach(line => line.remove());
  timeLines = [];
  if (typeof setStatusBox === 'function') setStatusBox({ time: '—', action: 'Clear Time' });
}

// ===============================
// PRICE PANEL LOGIC
// ===============================
let priceLines = [];

function drawNaturalLevels() {
  clearGannPrice();
  if (!priceData.length) return;
  // Draw key highs/lows
  let high = Math.max(...priceData.map(b => b.high));
  let low = Math.min(...priceData.map(b => b.low));
  let highLine = candleSeries.createPriceLine({ price: high, color: '#22d3ee', lineWidth: 2, title: 'Key High' });
  let lowLine = candleSeries.createPriceLine({ price: low, color: '#f472b6', lineWidth: 2, title: 'Key Low' });
  priceLines.push(highLine, lowLine);
  if (typeof setStatusBox === 'function') setStatusBox({ price: `High: ${high}, Low: ${low}`, action: 'Draw Natural Levels' });
}

function drawGannAngles() {
  clearGannPrice();
  if (!priceData.length) return;
  // Example: Draw 1x1, 2x1, 1x2 angles as lines
  let start = priceData[0];
  let end = priceData[priceData.length - 1];
  let angle1 = chart.addLineSeries({ color: '#f59e42', lineWidth: 1 });
  let angle2 = chart.addLineSeries({ color: '#f59e42', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dotted });
  let angle3 = chart.addLineSeries({ color: '#f59e42', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed });
  angle1.setData([
    { time: start.time, value: start.open },
    { time: end.time, value: end.open + (end.time - start.time) }
  ]);
  angle2.setData([
    { time: start.time, value: start.open },
    { time: end.time, value: start.open + 2 * (end.time - start.time) }
  ]);
  angle3.setData([
    { time: start.time, value: start.open },
    { time: end.time, value: start.open + 0.5 * (end.time - start.time) }
  ]);
  priceLines.push(angle1, angle2, angle3);
  if (typeof setStatusBox === 'function') setStatusBox({ price: 'Gann Angles', action: 'Draw Gann Angles' });
}

function drawSquarePrice() {
  clearGannPrice();
  if (!priceData.length) return;
  // Example: Draw a price line at the midpoint
  let high = Math.max(...priceData.map(b => b.high));
  let low = Math.min(...priceData.map(b => b.low));
  let mid = (high + low) / 2;
  let midLine = candleSeries.createPriceLine({ price: mid, color: '#a3e635', lineWidth: 2, title: 'Square Price' });
  priceLines.push(midLine);
  if (typeof setStatusBox === 'function') setStatusBox({ price: `Mid: ${mid.toFixed(2)}`, action: 'Draw Square Price' });
}

function drawSymmetryZones() {
  clearGannPrice();
  if (!priceData.length) return;
  // Example: Draw a zone between 25% and 75%
  let high = Math.max(...priceData.map(b => b.high));
  let low = Math.min(...priceData.map(b => b.low));
  let q1 = low + 0.25 * (high - low);
  let q3 = low + 0.75 * (high - low);
  let q1Line = candleSeries.createPriceLine({ price: q1, color: '#818cf8', lineWidth: 1, title: 'Symmetry Q1' });
  let q3Line = candleSeries.createPriceLine({ price: q3, color: '#818cf8', lineWidth: 1, title: 'Symmetry Q3' });
  priceLines.push(q1Line, q3Line);
  if (typeof setStatusBox === 'function') setStatusBox({ price: `Q1: ${q1.toFixed(2)}, Q3: ${q3.toFixed(2)}`, action: 'Draw Symmetry Zones' });
}

function clearGannPrice() {
  priceLines.forEach(line => line.remove());
  priceLines = [];
  if (typeof setStatusBox === 'function') setStatusBox({ price: '—', action: 'Clear Price' });
}
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

fetch("http://localhost:8000/live_xauusd")
  .then(res => res.json())
  .then(data => {
    // If error, fallback to demo data
    if (Array.isArray(data) && data.length > 0) {
      priceData = data;
      candleSeries.setData(data);
    } else if (data.demo && Array.isArray(data.demo) && data.demo.length > 0) {
      priceData = data.demo;
      candleSeries.setData(data.demo);
      if (data.error) {
        showChartError("Live data unavailable. Showing demo data.");
        console.warn(data.error);
      }
    } else {
      showChartError("No chart data available. Please try again later.");
      candleSeries.setData([]);
      console.error("Unexpected or empty data from /live_xauusd", data);
    }
  })
  .catch(err => {
    showChartError("Failed to load chart data. Please check your connection or try again later.");
    candleSeries.setData([]);
    console.error("Fetch error for /live_xauusd", err);
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

// ===============================
// GANN PANEL LOGIC
// ===============================
let gannMarkers = [];
let gannPriceLines = [];
let gannOverlayVisible = true;

function drawGannCycles() {
  // Example: Add a time cycle marker
  const cycleMarker = {
    time: priceData.length > 2 ? priceData[2].time : '2025-01-03',
    position: 'aboveBar',
    color: '#facc15',
    shape: 'circle',
    text: 'Cycle Complete (9)'
  };
  gannMarkers.push(cycleMarker);
  updateGannMarkers();
}

function drawGannLevels() {
  // Example: Add Gann price geometry zone
  const geometryTop = priceData.length > 2 ? priceData[2].high : 2100;
  const geometryBottom = priceData.length > 2 ? priceData[2].low : 2090;
  const topLine = candleSeries.createPriceLine({
    price: geometryTop,
    color: '#38bdf8',
    lineWidth: 1,
    lineStyle: LightweightCharts.LineStyle.Dotted,
    axisLabelVisible: true,
    title: 'Gann Resistance'
  });
  const bottomLine = candleSeries.createPriceLine({
    price: geometryBottom,
    color: '#38bdf8',
    lineWidth: 1,
    lineStyle: LightweightCharts.LineStyle.Dotted,
    axisLabelVisible: true,
    title: 'Gann Support'
  });
  gannPriceLines.push(topLine, bottomLine);
}

function drawGannSquare() {
  // Placeholder: Implement Square of Nine logic or visualization here
  alert('Gann Square of Nine visualization is not implemented yet.');
}

function drawGannAngles() {
  // Placeholder: Implement Gann Angles logic or visualization here
  alert('Gann Angles visualization is not implemented yet.');
}

function gannDatePriceCalc() {
  // Placeholder: Implement Date/Price Calculator logic here
  alert('Gann Date/Price Calculator is not implemented yet.');
}

function toggleGannOverlay() {
  gannOverlayVisible = !gannOverlayVisible;
  if (gannOverlayVisible) {
    updateGannMarkers();
    gannPriceLines.forEach(line => line.applyOptions({ color: '#38bdf8' }));
  } else {
    candleSeries.setMarkers([]);
    gannPriceLines.forEach(line => line.applyOptions({ color: 'rgba(0,0,0,0)' }));
  }
}

function clearGann() {
  gannMarkers = [];
  candleSeries.setMarkers([]);
  gannPriceLines.forEach(line => line.remove());
  gannPriceLines = [];
}

function updateGannMarkers() {
  // Add a signal marker as an example
  const signalMarker = {
    time: priceData.length > 3 ? priceData[3].time : '2025-01-04',
    position: 'aboveBar',
    color: '#f59e0b',
    shape: 'arrowDown',
    text: 'GANN SELL'
  };
  candleSeries.setMarkers([...gannMarkers, signalMarker]);
}
