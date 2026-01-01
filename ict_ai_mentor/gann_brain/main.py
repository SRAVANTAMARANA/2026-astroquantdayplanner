from datetime import date
from config import *
from time_engine import time_cycle_complete
from planetary_engine import planet_trigger
from price_engine import price_at_geometry
from market_state import market_state
from decision_engine import gann_decision
from telegram_bot import send_telegram, format_signal

# Example anchor date (set to your fixed origin date)
anchor_date = date(2024, 1, 1)  # CHANGE THIS TO YOUR ANCHOR

# Example input data (replace with live data in production)
active_planets = {"Mars": 90}
current_price = 2332.4
geometry_level = 2332.2
trend_strength = 65

time_ok, cycle = time_cycle_complete(anchor_date)
planet_ok, planet, degree = planet_trigger(active_planets)
price_ok = price_at_geometry(current_price, geometry_level)
state = market_state(trend_strength)

direction = "SELL" if trend_strength > 50 else "BUY"

if gann_decision(time_ok, planet_ok, price_ok, state):
    msg = format_signal(direction, cycle, planet, degree, current_price)
    send_telegram(msg, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    print("✅ Gann signal sent to Telegram.")
else:
    print("❌ No valid Gann setup today.")
