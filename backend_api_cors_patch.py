from fastapi import Body, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from feedback import save_feedback, get_all_feedback
from daily_astro_telegram import get_astro_report
from datetime import datetime, timedelta, timezone
import logging
import requests
import time
import os

app = FastAPI()

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Print all registered routes at startup for debugging
@app.on_event("startup")
def print_routes():
    print("\nRegistered routes:")
    for route in app.routes:
        print(f"{route.path} -> {route.name}")

# ...existing code...
