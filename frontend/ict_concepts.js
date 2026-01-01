// --- ICT Concepts Visualizations for Lightweight Charts ---
// Assumes chart and candleSeries are already created

function drawFVG(fvg) {
    const box = chart.addAreaSeries({
        topColor: fvg.direction === "BEARISH"
            ? 'rgba(239,68,68,0.35)'
            : 'rgba(34,197,94,0.35)',
        bottomColor: 'rgba(0,0,0,0)',
        lineColor: 'transparent',
    });
    box.setData([
        { time: fvg.from_time, value: fvg.high },
        { time: fvg.to_time, value: fvg.high },
        { time: fvg.to_time, value: fvg.low },
        { time: fvg.from_time, value: fvg.low },
    ]);
}

function drawOrderBlock(ob) {
    const obZone = chart.addAreaSeries({
        topColor: 'rgba(59,130,246,0.4)',
        bottomColor: 'rgba(59,130,246,0.15)',
        lineColor: '#60a5fa',
    });
    obZone.setData([
        { time: ob.time, value: ob.high },
        { time: ob.time, value: ob.low }
    ]);
    return obZone;
}

function animateMitigation(obZone) {
    let opacity = 0.4;
    const interval = setInterval(() => {
        opacity -= 0.05;
        if (opacity <= 0.05) clearInterval(interval);
        obZone.applyOptions({
            topColor: `rgba(59,130,246,${opacity})`
        });
    }, 300);
}

function drawSMT(smt) {
    const color = smt.direction === "BEARISH"
        ? '#a855f7'
        : '#22c55e';
    candleSeries.setMarkers([{
        time: smt.time,
        position: 'aboveBar',
        color: color,
        shape: 'circle',
        text: 'SMT'
    }]);
}

function drawKillzone(from, to, label) {
    chart.addAreaSeries({
        topColor: 'rgba(251,146,60,0.15)',
        bottomColor: 'rgba(251,146,60,0.05)',
        lineColor: 'transparent',
    }).setData([
        { time: from, value: 99999 },
        { time: to, value: 0 }
    ]);
}

// --- Replay Mode ---
let replayIndex = 0;
function replayBars(data) {
    const interval = setInterval(() => {
        candleSeries.setData(data.slice(0, replayIndex));
        replayIndex++;
        if (replayIndex >= data.length) clearInterval(interval);
    }, 700);
}
