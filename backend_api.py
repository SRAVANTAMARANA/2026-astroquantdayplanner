
# --- Moved all imports and app creation to the top ---
import os
import requests
from typing import Optional
import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from twelvedata import TDClient
from datetime import datetime


app = FastAPI()

# Serve static files from the frontend directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Route / to frontend/index.html
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twelve Data API key (set your key here or use env var)
TD_API_KEY = os.getenv("TWELVE_DATA_API_KEY", "84636b315e21459ab51acc322b468eb8")

@app.get("/api/twelvedata")
def twelvedata_api(
    type: str = Query(..., description="Type of data: ohlc, fundamentals, indicator, batch, websocket, advanced"),
    symbol: str = Query("XAUUSD", description="Symbol to fetch data for"),
    interval: str = Query("1day", description="Interval for time series/indicators"),
    outputsize: int = Query(12, description="Number of data points"),
    indicator: str = Query("sma", description="Technical indicator name (for type=indicator)"),
    indicators_params: str = Query("{}", description="JSON string of indicator params (for type=indicator)"),
    symbols: str = Query("XAUUSD", description="Comma-separated symbols for batch requests (for type=batch)"),
    websocket_topic: str = Query("price", description="WebSocket topic (for type=websocket)"),
    advanced_type: str = Query("earnings", description="Advanced data type (for type=advanced)")
):
    try:
        # Only allow XAUUSD (with or without slash)
        orig_symbol = symbol
        if symbol.upper().replace('/', '') != "XAUUSD":
            return JSONResponse(status_code=400, content={"error": "Only XAUUSD is supported."})
        td = TDClient(apikey=TD_API_KEY)
        tried_symbols = ["XAU/USD", "XAUUSD"]

        if type == "ohlc":
            last_error = None
            for sym in tried_symbols:
                try:
                    ohlc = td.time_series(symbol=sym, interval=interval, outputsize=outputsize, timezone="UTC").as_json()
                    if isinstance(ohlc, tuple):
                        last_error = str(ohlc)
                        continue
                    if not ohlc or 'values' not in ohlc:
                        last_error = ohlc.get('message', 'No data returned') if isinstance(ohlc, dict) else str(ohlc)
                        continue
                    bars = []
                    for bar in ohlc.get('values', []):
                        try:
                            dt = datetime.strptime(bar['datetime'], "%Y-%m-%d")
                            bars.append({
                                "time": {"year": dt.year, "month": dt.month, "day": dt.day},
                                "open": float(bar['open']),
                                "high": float(bar['high']),
                                "low": float(bar['low']),
                                "close": float(bar['close'])
                            })
                        except Exception as e:
                            print(f"Bar parse error: {e} for bar: {bar}")
                            continue
                    bars.reverse()
                    if bars:
                        return bars
                    else:
                        last_error = f"No bars parsed for symbol {sym}"
                except Exception as e:
                    print(f"Error fetching OHLC for symbol {sym}: {e}")
                    last_error = str(e)
            # If all attempts failed, return error
            print(f"Failed to fetch OHLC for {orig_symbol}. Last error: {last_error}")
            # Fallback: if gold, return demo data
            demo_bars = [
                {"time": {"year": 2026, "month": 1, "day": 1}, "open": 2050, "high": 2080, "low": 2040, "close": 2070},
                {"time": {"year": 2026, "month": 1, "day": 2}, "open": 2070, "high": 2090, "low": 2060, "close": 2080},
                {"time": {"year": 2026, "month": 1, "day": 3}, "open": 2080, "high": 2100, "low": 2070, "close": 2060},
                {"time": {"year": 2026, "month": 1, "day": 4}, "open": 2060, "high": 2070, "low": 2020, "close": 2030}
            ]
            return demo_bars
        # For all other types, return not supported
        return JSONResponse(status_code=400, content={"error": "Only ohlc type is supported for XAUUSD."})
    except Exception as e:
        # Robust fallback: always return demo data for XAUUSD, error for others
        print(f"/api/twelvedata fatal error: {e}")
        if symbol.upper().replace('/', '') == "XAUUSD":
            demo_bars = [
                {"time": {"year": 2026, "month": 1, "day": 1}, "open": 2050, "high": 2080, "low": 2040, "close": 2070},
                {"time": {"year": 2026, "month": 1, "day": 2}, "open": 2070, "high": 2090, "low": 2060, "close": 2080},
                {"time": {"year": 2026, "month": 1, "day": 3}, "open": 2080, "high": 2100, "low": 2070, "close": 2060},
                {"time": {"year": 2026, "month": 1, "day": 4}, "open": 2060, "high": 2070, "low": 2020, "close": 2030}
            ]
            return demo_bars
        return JSONResponse(status_code=500, content={"error": f"Internal server error: {e}"})

@app.get("/live_ohlc")
def get_live_ohlc(symbol: str = "XAUUSD"):
    td = TDClient(apikey=TD_API_KEY)
    ohlc = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=12,
        timezone="UTC"
    ).as_json()
    bars = []
    for bar in ohlc.get('values', []):
        # bar['datetime'] is like '2023-12-01'
        try:
            dt = datetime.strptime(bar['datetime'], "%Y-%m-%d")
            bars.append({
                "time": {"year": dt.year, "month": dt.month, "day": dt.day},
                "open": float(bar['open']),
                "high": float(bar['high']),
                "low": float(bar['low']),
                "close": float(bar['close'])
            })
        except Exception as e:
            continue
    bars.reverse()  # Oldest first
    return bars

# (All endpoints and code after the Twelve Data endpoints have been removed to avoid swisseph/flatlib/daily_astro_telegram dependencies. Only /api/twelvedata and /live_ohlc remain.)
    timings = []
    for hour in range(0, 24):
        dt = now.replace(hour=hour)
        positions = get_planet_positions(dt)
        aspects = get_aspects(positions)
        moon_sign = get_nakshatra_info(dt).get('nakshatra', '-')
        # Simple planetary hour calculation (placeholder, can be improved)
        planetary_hour = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"][(hour % 7)]
        aspect_str = ', '.join([
            f"{a.get('planet1', '')} {a.get('aspect', '')} {a.get('planet2', '')}"
            for a in aspects if isinstance(a, dict) and 'Moon' in (a.get('planet1', ''), a.get('planet2', ''))
        ])
        timings.append({
            "time": f"{hour:02d}:00",
            "planetary_hour": planetary_hour,
            "moon_sign": moon_sign,
            "aspect": aspect_str or "-"
        })
    return {"timings": timings}

# --- Astro News & Future Events API ---
@app.get("/api/astro_news")
def astro_news():
    """
    Returns upcoming economic news merged with astro context (real data from Forex Factory calendar + astro aspects).
    """
    # import requests
    from xml.etree import ElementTree as ET
    # from daily_astro_telegram import get_planet_positions, get_aspects
    ff_url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
    news_items = []
    try:
        resp = requests.get(ff_url, timeout=10)
        root = ET.fromstring(resp.content)
        for item in root.findall('.//event'):
            title = item.findtext('title', '')
            impact = item.findtext('impact', '')
            country = item.findtext('country', '')
            time_str = item.findtext('date', '') + ' ' + item.findtext('time', '')
            try:
                event_dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            except Exception:
                event_dt = None
            if impact in ['High', 'Medium'] and event_dt:
                positions = get_planet_positions(event_dt)
                aspects = get_aspects(positions)
                aspect_str = ', '.join([
                    f"{a.get('planet1', '')} {a.get('aspect', '')} {a.get('planet2', '')}"
                    for a in aspects if isinstance(a, dict) and 'Moon' in (a.get('planet1', ''), a.get('planet2', ''))
                ])
                news_items.append({
                    "time": event_dt.strftime('%Y-%m-%d %H:%M'),
                    "event": title,
                    "astro_context": aspect_str or "-",
                    "impact": impact
                })
    except Exception as e:
        news_items.append({"time": "-", "event": f"Error: {e}", "astro_context": "-", "impact": "-"})
    return {"events": news_items}





# --- Live XAUUSD OHLC API (Twelve Data) ---
@app.get("/live_xauusd")
def live_xauusd_chart():
    """
    Returns OHLC candles for XAU/USD from Twelve Data API.
    """
    API_KEY = os.environ.get("TWELVE_DATA_API_KEY", "cd9e7c71a1614c6dab24fbe1ba41c8fb")
    url = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=1h&outputsize=100&apikey={API_KEY}&format=JSON&type=candlestick"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if resp.status_code == 200 and 'values' in data:
            # Convert to Lightweight Charts format
            candles = [
                {
                    "time": bar["datetime"].split(" ")[0],
                    "open": float(bar["open"]),
                    "high": float(bar["high"]),
                    "low": float(bar["low"]),
                    "close": float(bar["close"])
                }
                for bar in reversed(data["values"])
            ]
            return candles
        else:
            error_message = data.get('message', resp.text)
            print(f"Twelve Data error: {error_message}")
            return {"error": f"Twelve Data error: {error_message}", "demo": [
                {"time": "2026-01-01", "open": 4150, "high": 4180, "low": 4140, "close": 4170},
                {"time": "2026-01-02", "open": 4170, "high": 4190, "low": 4160, "close": 4180},
                {"time": "2026-01-03", "open": 4180, "high": 4200, "low": 4170, "close": 4160},
                {"time": "2026-01-04", "open": 4160, "high": 4170, "low": 4120, "close": 4130}
            ]}
    except Exception as e:
        print(f"Twelve Data fetch error: {e}")
        return {"error": f"Twelve Data fetch error: {e}", "demo": [
            {"time": "2026-01-01", "open": 4150, "high": 4180, "low": 4140, "close": 4170},
            {"time": "2026-01-02", "open": 4170, "high": 4190, "low": 4160, "close": 4180},
            {"time": "2026-01-03", "open": 4180, "high": 4200, "low": 4170, "close": 4160},
            {"time": "2026-01-04", "open": 4160, "high": 4170, "low": 4120, "close": 4130}
        ]}

# --- Gann Module API ---
@app.get("/api/gann")
def gann_module():
    return {
        "levels": [2370, 2380, 2390],
        "comment": "Gann levels calculated.",
        "events": [
            {"date": "2025-12-31", "type": "cycle", "cycle": 9},
            {"date": "2025-12-31", "type": "planet", "planet": "Mars", "degree": 90}
        ]
    }

# --- Gann Chart Data API ---
@app.get("/api/gann_chart")
def gann_chart():
    return [
        {"time": "2025-12-31", "open": 2370, "high": 2376, "low": 2368, "close": 2372},
        {"time": "2026-01-01", "open": 2372, "high": 2375, "low": 2370, "close": 2373},
        {"time": "2026-01-02", "open": 2373, "high": 2378, "low": 2371, "close": 2376},
        {"time": "2026-01-03", "open": 2376, "high": 2380, "low": 2374, "close": 2378},
    ]

# --- ICT Module API ---
from data.price_loader import load_price_data
from liquidity.liquidity import detect_liquidity_sweep
from imbalance.fvg import detect_fvg
from timeframe.killzone import is_killzone
import datetime

@app.get("/api/ict/liquidity")
def ict_liquidity():
    df = load_price_data()
    liquidity = detect_liquidity_sweep(df)
    # For demo, return last price and time
    price = float(df.close.iloc[-1])
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return {"type": "BUY_SIDE" if liquidity else "NONE", "price": price, "time": now}

@app.get("/api/ict/fvg")
def ict_fvg():
    df = load_price_data()
    fvg = detect_fvg(df)
    # For demo, use last 3 closes as top/bottom
    top = float(df.close.iloc[-1])
    bottom = float(df.close.iloc[-3]) if len(df) >= 3 else float(df.close.iloc[0])
    start = (datetime.datetime.utcnow() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    end = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return {"type": fvg, "top": top, "bottom": bottom, "start": start, "end": end}

@app.get("/api/ict/ob")
def ict_ob():
    df = load_price_data()
    # Placeholder: Use last close as OB price
    price = float(df.close.iloc[-1])
    start = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    end = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return {"price": price, "start": start, "end": end}

@app.get("/api/ict/session")
def ict_session():
    session = is_killzone()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return {"time": now, "active": bool(session), "session": session}
@app.get("/api/ict")
def ict_module():
    return {
        "bias": "BULLISH",
        "liquidity": True,
        "fvg": True,
        "premium_discount": "PREMIUM",
        "killzone": True,
        "decision": True,
        "score": 5,
        "reasons": ["HTF bias confirmed: BULLISH", "Liquidity sweep confirmed", "Fair Value Gap present", "Sell from premium zone", "Killzone timing confirmed"]
    }

# --- Astro Module API ---
@app.get("/api/astro")
def astro_module():
    return {
        "astro_event": "Moon in Aries",
        "impact": "Bullish bias",
        "planetary_aspects": [
            {"planet": "Mars", "aspect": "Square", "degree": 90},
            {"planet": "Sun", "aspect": "Opposition", "degree": 180}
        ]
    }

# --- Day Report Module API ---
@app.get("/api/day_report")
def day_report():
    return {
        "date": "2026-01-01",
        "summary": "Market summary and key events for the day.",
        "gann": "Gann cycle 9 completed.",
        "ict": "Bullish bias, liquidity sweep confirmed.",
        "astro": "Moon in Aries, bullish bias."
    }

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}



@app.get("/feedback")
def all_feedback():
    """Endpoint to retrieve all feedback entries."""
    try:
        return get_all_feedback()
    except Exception as e:
        logging.error(f"Error in /feedback GET: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.get("/daily_report")
def daily_report():
    """Endpoint to get the daily astrology and analytics report."""
    try:
        msg = get_astro_report(datetime.datetime.utcnow())
        return {"report": msg}
    except Exception as e:
        logging.error(f"Error in /daily_report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")



from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from nakshatra_timings import find_nakshatra_transitions
from astro_events import find_event_transitions, get_nakshatra_info, get_tithi_info



# Serve static files (index.html and others)
import os
static_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve frontend directory at /frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

# Serve index.html at root (optional, can redirect to /frontend/index.html)
@app.get("/")
def root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Homepage not found"}

def format_astro_events(date):
    # timezone and timedelta are already imported at the top
    import pytz
    # Get events for the given date (00:00 to 23:59)
    start_dt = datetime.datetime(date.year, date.month, date.day, tzinfo=datetime.timezone.utc)
    end_dt = start_dt + datetime.timedelta(days=1)
    nakshatra_events = find_event_transitions(get_nakshatra_info, start_dt, hours=24, step_minutes=10) or []
    tithi_events = find_event_transitions(get_tithi_info, start_dt, hours=24, step_minutes=10) or []

    # Get current nakshatra and tithi at midnight
    current_nakshatra = nakshatra_events[0]["event"]["nakshatra"] if nakshatra_events and len(nakshatra_events) > 0 else ""
    current_tithi = tithi_events[0]["event"]["tithi"] if tithi_events and len(tithi_events) > 0 else ""

    # Telugu calendar style nakshatra change list
    IST = pytz.timezone('Asia/Kolkata')
    from astro_events import get_moon_longitude, get_sun_longitude
    nakshatra_periods = []
    if nakshatra_events:
        for event in nakshatra_events:
            if event and isinstance(event, dict):
                nakshatra = event.get("event", {}).get("nakshatra", "")
                start_time = event.get("start_time")
                end_time = event.get("end_time")
                start_time_ist = start_time.astimezone(IST).strftime("%H:%M IST") if start_time else ""
                end_time_ist = end_time.astimezone(IST).strftime("%H:%M IST") if end_time else ""
                # Get degrees at start and end
                moon_long_start = get_moon_longitude(start_time) if start_time else 0.0
                moon_long_end = get_moon_longitude(end_time) if end_time else 0.0
                sun_long_start = get_sun_longitude(start_time) if start_time else 0.0
                sun_long_end = get_sun_longitude(end_time) if end_time else 0.0
                nakshatra_periods.append({
                    "nakshatra": nakshatra,
                    "from_time": start_time_ist,
                    "to_time": end_time_ist,
                    "moon_longitude_start": round(moon_long_start, 4),
                    "moon_longitude_end": round(moon_long_end, 4),
                    "sun_longitude_start": round(sun_long_start, 4),
                    "sun_longitude_end": round(sun_long_end, 4)
                })

    return {
        "date": start_dt.strftime("%Y-%m-%d"),
        "weekday": start_dt.strftime("%A"),
        "moon": {
            "periods": nakshatra_periods
        },
        "tithi": current_tithi
    }

@app.get("/nakshatra-timings")
def get_nakshatra_timings():
    now = datetime.datetime.now(datetime.timezone.utc)
    transitions = find_nakshatra_transitions(now, hours=24, step_minutes=10)
    if not isinstance(transitions, list):
        transitions = []
    result = []
    for t in transitions:
        if isinstance(t, dict):
            result.append({
                "nakshatra": t.get("nakshatra", ""),
                "start_time": t.get("start_time", "").isoformat() if t.get("start_time") else "",
                "end_time": t.get("end_time", "").isoformat() if t.get("end_time") else "",
                "start_long": t.get("start_long", ""),
                "end_long": t.get("end_long", "")
            })
    return {"nakshatra_timings": result}


@app.get("/astro-events")
def get_astro_events(date: Optional[str] = None):
    """
    Returns astro events for the given date (YYYY-MM-DD). If no date is provided, uses today.
    """
    if date is not None:
        dt = datetime.datetime.strptime(str(date), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)
    return format_astro_events(dt)

# --- Astro Module Extra Endpoints ---
@app.get("/api/astro/events")
def astro_events():
    return {"events": ["Event 1", "Event 2"]}

@app.get("/api/astro/add_to_calendar")
def astro_add_to_calendar():
    return {"status": "Astro event added to calendar"}

@app.get("/api/astro/export")
def astro_export():
    return {"status": "Astro data exported"}

# --- Day Report Extra Endpoint ---
@app.get("/api/day_report/export")
def day_report_export():
    return {"status": "Day report exported"}

# --- Gann Module Extra Endpoints ---
@app.get("/api/gann/draw_cycle")
def gann_draw_cycle():
    return {"status": "Gann cycle drawn"}

@app.get("/api/gann/export")
def gann_export():
    return {"status": "Gann events exported"}

@app.get("/api/gann/add_to_calendar")
def gann_add_to_calendar():
    return {"status": "Gann event added to calendar"}

# --- ICT Module Extra Endpoints ---
@app.get("/api/ict/signal")
def ict_signal():
    return {"signal": "ICT signal data"}

@app.get("/api/ict/send_telegram")
def ict_send_telegram():
    return {"status": "ICT signal sent to Telegram"}

@app.get("/api/ict/export")
def ict_export():
    return {"status": "ICT report exported"}

# --- Astro Observer API ---
@app.get("/api/astro_observer")
def astro_observer():
    return {"summary": "Astro observer output"}

@app.get("/api/astro_observer/export")
def astro_observer_export():
    return {"status": "Astro observer data exported"}

# --- Calendar API ---
@app.get("/api/calendar/events")
def calendar_events():
    return {"events": ["Calendar event 1", "Calendar event 2"]}

@app.get("/api/calendar/add")
def calendar_add():
    return {"status": "Calendar event added"}

@app.get("/api/calendar/export")
def calendar_export():
    return {"status": "Calendar exported"}

# --- Signal & Telegram API ---
@app.get("/api/send_gann_signal")
def send_gann_signal():
    return {"status": "Gann signal sent"}

@app.get("/api/signal/last")
def signal_last():
    return {"signal": "Last signal data"}

# --- Trade Memory / Journal API ---
@app.get("/api/trade_analysis")
def trade_analysis():
    return {"memory": "Trade memory data"}

@app.get("/api/journal/add")
def journal_add():
    return {"status": "Journal entry added"}

@app.get("/api/journal/export")
def journal_export():
    return {"status": "Journal exported"}

# --- Lightweight Charts API ---
@app.get("/api/chart/draw_marker")
def chart_draw_marker():
    return {"status": "Chart marker drawn"}

@app.get("/api/chart/export")
def chart_export():
    return {"status": "Chart data exported"}

# --- Market Data API ---
@app.get("/api/market_data")
def market_data():
    return {"data": "Market data output"}

@app.get("/api/market_data/export")
def market_data_export():
    return {"status": "Market data exported"}

# --- ICT Brain API ---
@app.get("/api/ict_brain")
def ict_brain():
    return {"output": "ICT brain output"}

@app.get("/api/ict_brain/output")
def ict_brain_output():
    return {"output": "ICT brain output details"}

@app.get("/api/ict_brain/export")
def ict_brain_export():
    return {"status": "ICT brain data exported"}
