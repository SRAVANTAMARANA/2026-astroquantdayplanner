"""
Backend API for AstroQuant Day Planner
Provides endpoints for astro analytics, feedback, and reports with error handling and modular structure.
"""

from fastapi import FastAPI, Request, HTTPException
from feedback import save_feedback, get_all_feedback
from daily_astro_telegram import get_astro_report
from datetime import datetime, timedelta, timezone
import logging


app = FastAPI()

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

@app.post("/feedback")
async def feedback(request: Request):
    """
    Endpoint to receive user feedback.
    Expects JSON with 'user_id' and 'feedback'.
    """
    try:
        data = await request.json()
        user_id = data.get('user_id')
        feedback_text = data.get('feedback')
        if not user_id or not feedback_text:
            raise HTTPException(status_code=400, detail="Missing user_id or feedback.")
        if not save_feedback(user_id, feedback_text):
            raise HTTPException(status_code=500, detail="Failed to save feedback.")
        return {"status": "received"}
    except Exception as e:
        logging.error(f"Error in /feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

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
        msg = get_astro_report(datetime.utcnow())
        return {"report": msg}
    except Exception as e:
        logging.error(f"Error in /daily_report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")



from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from nakshatra_timings import find_nakshatra_transitions
from astro_events import find_event_transitions, get_nakshatra_info, get_tithi_info


app = FastAPI()

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

def format_astro_events(date: datetime):
    # timezone and timedelta are already imported at the top
    import pytz
    # Get events for the given date (00:00 to 23:59)
    start_dt = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(days=1)
    nakshatra_events = find_event_transitions(get_nakshatra_info, start_dt, hours=24, step_minutes=10)
    tithi_events = find_event_transitions(get_tithi_info, start_dt, hours=24, step_minutes=10)

    # Get current nakshatra and tithi at midnight
    current_nakshatra = nakshatra_events[0]["event"]["nakshatra"]
    current_tithi = tithi_events[0]["event"]["tithi"]

    # Telugu calendar style nakshatra change list
    IST = pytz.timezone('Asia/Kolkata')
    from astro_events import get_moon_longitude, get_sun_longitude
    nakshatra_periods = []
    for event in nakshatra_events:
        nakshatra = event["event"]["nakshatra"]
        start_time = event["start_time"]
        end_time = event["end_time"]
        start_time_ist = start_time.astimezone(IST).strftime("%H:%M IST")
        end_time_ist = end_time.astimezone(IST).strftime("%H:%M IST")
        # Get degrees at start and end
        moon_long_start = get_moon_longitude(start_time)
        moon_long_end = get_moon_longitude(end_time)
        sun_long_start = get_sun_longitude(start_time)
        sun_long_end = get_sun_longitude(end_time)
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
    now = datetime.now(timezone.utc)
    transitions = find_nakshatra_transitions(now, hours=24, step_minutes=10)
    result = [
        {
            "nakshatra": t["nakshatra"],
            "start_time": t["start_time"].isoformat(),
            "end_time": t["end_time"].isoformat(),
            "start_long": t["start_long"],
            "end_long": t["end_long"]
        }
        for t in transitions
    ]
    return {"nakshatra_timings": result}


@app.get("/astro-events")
def get_astro_events(date: str = None):
    """
    Returns astro events for the given date (YYYY-MM-DD). If no date is provided, uses today.
    """
    if date:
        dt = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    return format_astro_events(dt)
