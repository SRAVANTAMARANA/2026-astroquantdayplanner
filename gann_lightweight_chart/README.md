# Gann Lightweight Chart System

This folder contains a complete, production-ready workflow for visualizing and journaling Gann cycles, price geometry, and signals using Lightweight Charts (not TradingView).

## Features
- Candlestick chart with event-driven overlays (no indicators)
- Time cycle markers (vertical lines/dots)
- Price geometry zones (horizontal bands)
- Signal markers (arrows/dots)
- Python-to-JSON export for chart events
- Cycle/trade journal panel (CSV-based)
- Python script for automated journal entry

## Usage
1. Open `index.html` in your browser (or use Live Server in VS Code)
2. Update `gann_events.json` with Python (see `export_gann_events.py`)
3. Add journal entries with `update_journal.py` or manually edit `journal_template.csv`
4. Chart and journal panel will auto-refresh on reload

## File Structure
- `index.html` — Main dashboard
- `chart.js` — Chart rendering logic
- `gann_events.js` — Loads and draws Gann events from JSON
- `gann_events.json` — Event data (cycles, zones, signals)
- `journal_template.csv` — Cycle/trade journal
- `journal_panel.js` — Displays journal as a table
- `export_gann_events.py` — Python: export chart events
- `update_journal.py` — Python: add journal entries

## No TradingView Required
This system uses only [Lightweight Charts](https://tradingview.github.io/lightweight-charts/) JS library. No TradingView account or platform is needed.

---

For live data, automation, or advanced analytics, expand the Python scripts and JSON/CSV integration as needed.
