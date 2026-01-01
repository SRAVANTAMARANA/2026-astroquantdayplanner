# AstroQuant ICT Mentor Enterprise Bundle

## Features
- Full ICT mentor chart: FVG, Order Block, SMT, Killzone, Replay
- MT5 auto-trading (Python, MetaTrader5 API)
- FastAPI backend: signals, price, ICT overlays
- Mobile-ready frontend (Lightweight Charts, HTML/JS/CSS)
- Android/WebView compatible
- Prop-firm safe logic, ICT math, and live signal flow

## Directory Structure
```
frontend/
  index.html         # Main chart UI
  style.css          # Chart styling
  chart.js           # Chart logic (loads price, overlays)
  ict_concepts.js    # ICT overlays, replay, animation
api/
  server.py          # FastAPI backend (signals, price, concepts)
execution/
  mt5_executor.py    # MT5 connect & trade
  safe_gate.py       # Trade safety logic
risk/
  sl_tp_math.py      # ICT SL/TP & lot math
memory/
  trades.json        # Trade memory (signals, history)
requirements-mt5.txt # MT5 Python requirements
config.py            # Config loader (edit for your broker, keys)
```

## Quick Start
### 1. Backend (API)
```bash
cd api
uvicorn server:app --host 0.0.0.0 --port 8000
```
- Endpoints:
  - `/signals`  — live trades
  - `/price`    — price candles (JSON)
  - `/concepts` — ICT overlays (FVG, OB, SMT, Killzone)

### 2. Frontend (Chart)
- Open `frontend/index.html` in your browser or Android WebView
- Chart auto-loads price and overlays from backend
- Use replay controls for bar-by-bar learning

### 3. MT5 Auto-Trading (Windows/MT5 machine)
- Install MetaTrader 5, Python 3.10, and run:
```bash
pip install -r requirements-mt5.txt
```
- Edit `config.py` for your broker/symbol
- Use `execution/mt5_executor.py` in your signal pipeline

## Customization
- Connect real ICT Brain overlays by updating `/concepts` endpoint in `api/server.py`
- Add multi-timeframe, click-to-inspect, or mobile push as needed

## Support
- For upgrades (multi-symbol, voice mentor, cloud deploy), just ask!

---
This bundle is ready for live, mobile, and enterprise use. 🚀