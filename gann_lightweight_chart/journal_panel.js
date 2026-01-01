// Simple cycle journal panel for Gann events
// Reads journal_template.csv and displays as a table

function loadJournal() {
    fetch('journal_template.csv')
        .then(response => response.text())
        .then(csv => {
            const lines = csv.trim().split('\n');
            const headers = lines[0].split(',');
            const rows = lines.slice(1).map(line => line.split(','));
            let html = '<table style="width:100%;border-collapse:collapse;background:#fff;color:#222;font-size:1em;">';
            html += '<tr>' + headers.map(h => `<th style="border:1px solid #ccc;padding:4px 8px;background:#e3eafc;">${h}</th>`).join('') + '</tr>';
            for (const row of rows) {
                html += '<tr>' + row.map(cell => `<td style="border:1px solid #ccc;padding:4px 8px;">${cell}</td>`).join('') + '</tr>';
            }
            html += '</table>';
            document.getElementById('journal-panel').innerHTML = html;
        });
}

document.addEventListener('DOMContentLoaded', loadJournal);
