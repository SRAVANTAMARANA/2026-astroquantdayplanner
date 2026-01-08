from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

import pandas as pd

app = FastAPI()

# Absolute path to the frontend directory
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")


# Serve index.html at the root
@app.get("/")
def read_index():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "index.html not found"}

# Catch-all route for SPA (serves index.html for any unmatched path)
from fastapi import Request
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    # Only serve index.html for GET requests that are not API/static
    if request.method == "GET" and not full_path.startswith("api") and not full_path.startswith("frontend"):
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    return {"detail": "Not Found"}


# --- New: ICT Concepts endpoint for chart overlays ---
@app.get("/concepts")
def get_concepts():
    # Example: return demo overlays for all ICT concepts
    return [
        {"type": "FVG", "from_time": "2025-01-02T10:15", "to_time": "2025-01-02T11:00", "high": 2374.5, "low": 2372.8, "direction": "BEARISH"},
        {"type": "OB", "time": "2025-01-02T09:30", "high": 2373.8, "low": 2372.9, "mitigated": False},
        {"type": "OB", "time": "2025-01-02T12:00", "high": 2377.0, "low": 2375.5, "mitigated": True},
        {"type": "SMT", "time": "2025-01-02T10:45", "direction": "BEARISH"},
        {"type": "KILLZONE", "from": "2025-01-02T13:30", "to": "2025-01-02T16:30", "label": "London"},
        {"type": "KILLZONE", "from": "2025-01-02T18:30", "to": "2025-01-02T21:30", "label": "New York"},
    ]


@app.get("/signals")
def get_signals():
    memory_path = os.path.join(os.path.dirname(__file__), "../memory/trades.json")
    with open(memory_path) as f:
        return json.load(f)

# --- New: Price data endpoint for chart ---

@app.get("/price")
def get_price():
    # Example: load from CSV or database in production
    # Here, return static sample data for demo
    data = [
        {"time": "2025-01-01", "open": 2370, "high": 2376, "low": 2368, "close": 2372},
        {"time": "2025-01-02", "open": 2372, "high": 2375, "low": 2370, "close": 2373},
        {"time": "2025-01-03", "open": 2373, "high": 2378, "low": 2371, "close": 2376},
        {"time": "2025-01-04", "open": 2376, "high": 2380, "low": 2374, "close": 2378},
    ]
    return data
