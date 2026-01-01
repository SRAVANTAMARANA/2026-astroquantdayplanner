window.onGannEventsLoaded = function() {
    const data = window.gannEvents;
    // Time cycle markers
    const timeMarkers = data.timeMarkers || [];
    // Signal markers
    const signalMarkers = data.signalMarkers || [];
    // Combine for setMarkers
    candleSeries.setMarkers([...timeMarkers, ...signalMarkers]);

    // Price geometry zones
    if (data.geometryZones && data.geometryZones.length > 0) {
        data.geometryZones.forEach(zone => {
            candleSeries.createPriceLine({
                price: zone.top,
                color: '#38bdf8',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dotted,
                axisLabelVisible: true,
                title: zone.label + ' Top'
            });
            candleSeries.createPriceLine({
                price: zone.bottom,
                color: '#38bdf8',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dotted,
                axisLabelVisible: true,
                title: zone.label + ' Bottom'
            });
        });
    }
};
