// Dashboard frontend logic for module actions
async function callApi(endpoint, statusId, outputHandler) {
    const status = document.getElementById(statusId);
    if (status) status.textContent = 'Running...';
    try {
        const res = await fetch(endpoint);
        const data = await res.json();
        if (status) status.textContent = 'Done';
        if (outputHandler) outputHandler(data);
    } catch (e) {
        if (status) status.textContent = 'Error';
        alert('API error: ' + e);
    }
}

function showOutput(title, data) {
    let out = document.getElementById('dashboard-output');
    if (!out) {
        out = document.createElement('div');
        out.id = 'dashboard-output';
        out.style = 'max-width:900px;margin:32px auto;background:#fff;border-radius:8px;padding:18px 24px;box-shadow:0 2px 12px #0002;color:#1a237e;';
        document.querySelector('.container').appendChild(out);
    }
    out.innerHTML = `<b>${title}</b><pre style='white-space:pre-wrap;font-size:1em;'>${JSON.stringify(data, null, 2)}</pre>`;
}

// Attach actions to module buttons
document.addEventListener('DOMContentLoaded', function() {
    // Gann Module
    const gannRunBtn = document.querySelector('button[onclick*="Run Analysis"]');
    if (gannRunBtn) gannRunBtn.onclick = () => callApi('/api/gann', 'gann-status', d => showOutput('Gann Output', d));
    const gannDrawBtn = document.querySelector('button[onclick*="Draw Cycle"]');
    if (gannDrawBtn) gannDrawBtn.onclick = () => callApi('/api/gann/draw_cycle', 'gann-status', d => showOutput('Gann Cycle', d));
    const gannSendBtn = document.querySelector('button[onclick*="Send Gann Signal"]');
    if (gannSendBtn) gannSendBtn.onclick = () => callApi('/api/send_gann_signal', 'gann-status', d => showOutput('Gann Signal Sent', d));
    const gannExportBtn = document.querySelector('button[onclick*="Export Gann Events"]');
    if (gannExportBtn) gannExportBtn.onclick = () => callApi('/api/gann/export', 'gann-status', d => showOutput('Gann Export', d));
    const gannAddCalBtn = document.querySelector('button[onclick*="Add Gann Event to Calendar"]');
    if (gannAddCalBtn) gannAddCalBtn.onclick = () => callApi('/api/gann/add_to_calendar', 'gann-status', d => showOutput('Gann Event Added to Calendar', d));

    // ICT Module
    const ictRunBtn = document.querySelector('button[onclick*="Run Mentor"]');
    if (ictRunBtn) ictRunBtn.onclick = () => callApi('/api/ict', 'ict-status', d => showOutput('ICT Output', d));
    const ictShowSignalBtn = document.querySelector('button[onclick*="Show ICT Signal"]');
    if (ictShowSignalBtn) ictShowSignalBtn.onclick = () => callApi('/api/ict/signal', 'ict-status', d => showOutput('ICT Signal', d));
    const ictSendTelegramBtn = document.querySelector('button[onclick*="Send ICT Signal to Telegram"]');
    if (ictSendTelegramBtn) ictSendTelegramBtn.onclick = () => callApi('/api/ict/send_telegram', 'ict-status', d => showOutput('ICT Signal Sent to Telegram', d));
    const ictExportBtn = document.querySelector('button[onclick*="Export ICT Report"]');
    if (ictExportBtn) ictExportBtn.onclick = () => callApi('/api/ict/export', 'ict-status', d => showOutput('ICT Export', d));

    // Astro Module
    const astroRunBtn = document.querySelector('button[onclick*="Run Astro Analysis"]');
    if (astroRunBtn) astroRunBtn.onclick = () => callApi('/api/astro', 'astro-status', d => showOutput('Astro Output', d));
    const astroShowBtn = document.querySelector('button[onclick*="Show Astro Events"]');
    if (astroShowBtn) astroShowBtn.onclick = () => callApi('/api/astro/events', 'astro-status', d => showOutput('Astro Events', d));
    const astroAddCalBtn = document.querySelector('button[onclick*="Add Astro Event to Calendar"]');
    if (astroAddCalBtn) astroAddCalBtn.onclick = () => callApi('/api/astro/add_to_calendar', 'astro-status', d => showOutput('Astro Event Added to Calendar', d));
    const astroExportBtn = document.querySelector('button[onclick*="Export Astro Data"]');
    if (astroExportBtn) astroExportBtn.onclick = () => callApi('/api/astro/export', 'astro-status', d => showOutput('Astro Export', d));

    // Astro Observer
    const astroObsBtn = document.querySelector('button[onclick*="Observe Astro Events"]');
    if (astroObsBtn) astroObsBtn.onclick = () => callApi('/api/astro_observer', 'astro-observer-status', d => showOutput('Astro Observer Output', d));
    const astroObsExportBtn = document.querySelector('button[onclick*="Export Astro Observer Data"]');
    if (astroObsExportBtn) astroObsExportBtn.onclick = () => callApi('/api/astro_observer/export', 'astro-observer-status', d => showOutput('Astro Observer Export', d));

    // Calendar
    const calShowBtn = document.querySelector('button[onclick*="Show calendar events"]');
    if (calShowBtn) calShowBtn.onclick = () => callApi('/api/calendar/events', 'calendar-status', d => showOutput('Calendar Events', d));
    const calAddBtn = document.querySelector('button[onclick*="Add Event"]');
    if (calAddBtn) calAddBtn.onclick = () => callApi('/api/calendar/add', 'calendar-status', d => showOutput('Calendar Event Added', d));
    const calExportBtn = document.querySelector('button[onclick*="Export calendar"]');
    if (calExportBtn) calExportBtn.onclick = () => callApi('/api/calendar/export', 'calendar-status', d => showOutput('Calendar Export', d));

    // Day Report
    const dayBtn = document.querySelector('button[onclick*="Generate day report"]');
    if (dayBtn) dayBtn.onclick = () => callApi('/api/day_report', 'day-report-status', d => showOutput('Day Report', d));
    const dayExportBtn = document.querySelector('button[onclick*="Export day report"]');
    if (dayExportBtn) dayExportBtn.onclick = () => callApi('/api/day_report/export', 'day-report-status', d => showOutput('Day Report Export', d));

    // Signal & Telegram
    const sigBtn = document.querySelector('button[onclick*="Send test signal"]');
    if (sigBtn) sigBtn.onclick = () => callApi('/api/send_gann_signal', 'signal-status', d => showOutput('Signal Output', d));
    const sigShowBtn = document.querySelector('button[onclick*="Show Last Signal"]');
    if (sigShowBtn) sigShowBtn.onclick = () => callApi('/api/signal/last', 'signal-status', d => showOutput('Last Signal', d));

    // Trade Memory / Journal
    const memBtn = document.querySelector('button[onclick*="Show trade memory"]');
    if (memBtn) memBtn.onclick = () => callApi('/api/trade_analysis', 'memory-status', d => showOutput('Trade Memory', d));
    const memAddBtn = document.querySelector('button[onclick*="Add Entry"]');
    if (memAddBtn) memAddBtn.onclick = () => callApi('/api/journal/add', 'memory-status', d => showOutput('Journal Entry Added', d));
    const memExportBtn = document.querySelector('button[onclick*="Export Journal"]');
    if (memExportBtn) memExportBtn.onclick = () => callApi('/api/journal/export', 'memory-status', d => showOutput('Journal Export', d));

    // Lightweight Charts
    const chartBtn = document.querySelector('button[onclick*="Show chart"]');
    if (chartBtn) chartBtn.onclick = () => window.open('../gann_lightweight_chart/index.html', '_blank');
    const chartDrawBtn = document.querySelector('button[onclick*="Draw Marker"]');
    if (chartDrawBtn) chartDrawBtn.onclick = () => callApi('/api/chart/draw_marker', 'charts-status', d => showOutput('Chart Marker', d));
    const chartExportBtn = document.querySelector('button[onclick*="Export Chart Data"]');
    if (chartExportBtn) chartExportBtn.onclick = () => callApi('/api/chart/export', 'charts-status', d => showOutput('Chart Export', d));

    // Market Data
    const dataBtn = document.querySelector('button[onclick*="Load price data"]');
    if (dataBtn) dataBtn.onclick = () => callApi('/api/market_data', 'data-status', d => showOutput('Market Data', d));
    const dataExportBtn = document.querySelector('button[onclick*="Export Market Data"]');
    if (dataExportBtn) dataExportBtn.onclick = () => callApi('/api/market_data/export', 'data-status', d => showOutput('Market Data Export', d));

    // ICT Brain
    const brainBtn = document.querySelector('button[onclick*="Run ICT Brain"]');
    if (brainBtn) brainBtn.onclick = () => callApi('/api/ict_brain', 'brain-status', d => showOutput('ICT Brain Output', d));
    const brainShowBtn = document.querySelector('button[onclick*="Show ICT Brain Output"]');
    if (brainShowBtn) brainShowBtn.onclick = () => callApi('/api/ict_brain/output', 'brain-status', d => showOutput('ICT Brain Output', d));
    const brainExportBtn = document.querySelector('button[onclick*="Export ICT Brain Data"]');
    if (brainExportBtn) brainExportBtn.onclick = () => callApi('/api/ict_brain/export', 'brain-status', d => showOutput('ICT Brain Export', d));
});
