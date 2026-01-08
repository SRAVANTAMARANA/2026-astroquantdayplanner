import os
import json
import requests
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime


app = FastAPI()

# Serve static files from the 'frontend' directory at '/static'
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
from fastapi.responses import FileResponse
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TD_API_KEY = os.getenv("TWELVE_DATA_API_KEY", "YOUR_API_KEY_HERE")
print(f"[DEBUG] TWELVE_DATA_API_KEY in backend: {TD_API_KEY}")

@app.get("/api/twelvedata")
def twelvedata_api(
    type: str = Query(..., description="Type of data: ohlc, fundamentals, indicator, batch, websocket, advanced"),
    symbol: str = Query("AAPL", description="Symbol to fetch data for"),
    interval: str = Query("1day", description="Interval for time series/indicators"),
    outputsize: int = Query(12, description="Number of data points"),
    indicator: str = Query("sma", description="Technical indicator name (for type=indicator)"),
    indicators_params: str = Query("{}", description="JSON string of indicator params (for type=indicator)"),
    symbols: str = Query("AAPL,MSFT", description="Comma-separated symbols for batch requests (for type=batch)"),
    websocket_topic: str = Query("price", description="WebSocket topic (for type=websocket)"),
    advanced_type: str = Query("earnings", description="Advanced data type (for type=advanced)")
):
    if type == "ohlc":
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={TD_API_KEY}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return JSONResponse(status_code=resp.status_code, content={"error": resp.text})
        data = resp.json()
        bars = []
        for bar in data.get('values', []):
            try:
                dt = datetime.strptime(bar['datetime'], "%Y-%m-%d")
                bars.append({
                    "time": {"year": dt.year, "month": dt.month, "day": dt.day},
                    "open": float(bar['open']),
                    "high": float(bar['high']),
                    "low": float(bar['low']),
                    "close": float(bar['close'])
                })
            except Exception:
                continue
        bars.reverse()
        return bars
    elif type == "fundamentals":
        fundamentals = td.fundamentals(symbol=symbol).as_json()
        return fundamentals
    elif type == "indicator":
        # Build indicator API URL
        param_str = "".join([f"&{k}={v}" for k, v in json.loads(indicators_params).items()])
        url = f"https://api.twelvedata.com/technical_indicators?symbol={symbol}&interval={interval}&outputsize={outputsize}&indicator={indicator}{param_str}&apikey={TD_API_KEY}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return JSONResponse(status_code=resp.status_code, content={"error": resp.text})
        data = resp.json()
        return data
    elif type == "batch":
        symlist = [s.strip() for s in symbols.split(",") if s.strip()]
        batch_data = td.time_series(symbol=symlist, interval=interval, outputsize=outputsize, timezone="UTC").as_json()
        return batch_data
    elif type == "websocket":
        return {"info": "Use client-side WebSocket to connect to wss://ws.twelvedata.com/v1/price?apikey=YOUR_API_KEY"}
    elif type == "advanced":
        if advanced_type == "earnings":
            data = td.earnings(symbol=symbol).as_json()
        elif advanced_type == "splits":
            data = td.splits(symbol=symbol).as_json()
        elif advanced_type == "dividends":
            data = td.dividends(symbol=symbol).as_json()
        else:
            data = {"error": "Unknown advanced_type"}
        return data
    else:
        return JSONResponse(status_code=400, content={"error": "Unknown type"})

@app.get("/live_ohlc")
def get_live_ohlc(symbol: str = "AAPL"):
    td = TDClient(apikey=TD_API_KEY)
    ohlc = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=12,
        timezone="UTC"
    ).as_json()
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
            continue
    bars.reverse()
    return bars
