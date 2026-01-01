from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ict_ai_mentor.calendar.calendar_module import get_today, get_events
from ict_ai_mentor.day_report.day_report import generate_day_report
from ict_ai_mentor.gann.gann_module import gann_analysis
from ict_ai_mentor.charts.lightweight_charts import render_lightweight_chart
from ict_ai_mentor.ict.ict_module import ict_custom_logic
from ict_ai_mentor.astro.astro_module import astro_analysis
from ict_ai_mentor.astro_observer.astro_observer_module import observe_astro_events

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/calendar/today")
def api_calendar_today():
    return {"today": get_today()}

@app.get("/api/calendar/events")
def api_calendar_events(date: str = None):
    return {"events": get_events(date)}

@app.get("/api/day_report")
def api_day_report():
    return generate_day_report()

@app.get("/api/gann")
def api_gann():
    # Example: use dummy data for now
    return gann_analysis({})

@app.get("/api/charts")
def api_charts():
    # Example: use dummy data for now
    return {"chart_html": render_lightweight_chart({})}

@app.get("/api/ict")
def api_ict():
    # Example: use dummy data for now
    return ict_custom_logic({})

@app.get("/api/astro")
def api_astro():
    return astro_analysis(get_today())

@app.get("/api/astro_observer")
def api_astro_observer():
    return {"events": observe_astro_events()}
