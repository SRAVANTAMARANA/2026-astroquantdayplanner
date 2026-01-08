
// Gann overlay data
const gannData = {
    timeMarkers: [
        {
            time: '2025-01-03',
            position: 'aboveBar',
            color: '#facc15',
            shape: 'circle',
            text: 'Cycle Complete (9)'
        }
    ],
    geometryTop: 2100,
    geometryBottom: 2090,
    signalMarkers: [
        {
            time: '2025-01-04',
            position: 'aboveBar',
            color: '#f59e0b',
            shape: 'arrowDown',
            text: 'GANN SELL'
        }
    ]
};

let gannTopLine = null;
let gannBottomLine = null;

window.updateOverlays = function() {
    // Remove all overlays first
    if (gannTopLine) { try { gannTopLine.remove(); } catch(e){} gannTopLine = null; }
    if (gannBottomLine) { try { gannBottomLine.remove(); } catch(e){} gannBottomLine = null; }
    // Only show Gann overlays if enabled
    if (window.activeOverlays.gann) {
        // Markers
        window.candleSeries.setMarkers([...gannData.timeMarkers, ...gannData.signalMarkers]);
        // Price lines
        gannTopLine = window.candleSeries.createPriceLine({
            price: gannData.geometryTop,
            color: '#38bdf8',
            lineWidth: 1,
            lineStyle: LightweightCharts.LineStyle.Dotted,
            axisLabelVisible: true,
            title: 'Gann Resistance'
        });
        gannBottomLine = window.candleSeries.createPriceLine({
            price: gannData.geometryBottom,
            color: '#38bdf8',
            lineWidth: 1,
            lineStyle: LightweightCharts.LineStyle.Dotted,
            axisLabelVisible: true,
            title: 'Gann Support'
        });
    } else {
        // Remove Gann overlays
        window.candleSeries.setMarkers([]);
    }
    // TODO: Add overlays for astro, ict, etc. here
};

// Initial overlay render
window.updateOverlays();
