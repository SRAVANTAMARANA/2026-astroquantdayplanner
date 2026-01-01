from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib import const
from datetime import datetime, timedelta, timezone
import requests
from config import TWELVEDATA_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

from xauusd_chart import get_xauusd_chart_url, download_chart_image, fetch_xauusd_ohlc
import feedparser
import pandas as pd

# Import modular summary functions
from summaries.astro_summary import get_astro_summary
from summaries.ict_summary import get_ict_summary
from summaries.gann_summary import get_gann_summary
from summaries.news_summary import get_news_summary
from summaries.global_market_summary import get_global_market_summary
from summaries.overall_summary import get_overall_summary

# --- CONFIGURATION ---
    # Now loaded from config.py

PLANETS = [
    ('Sun', const.SUN),
    ('Moon', const.MOON),
    ('Mercury', const.MERCURY),
    ('Venus', const.VENUS),
    ('Mars', const.MARS),
    ('Jupiter', const.JUPITER),
    ('Saturn', const.SATURN),
    ('Rahu', const.NORTH_NODE),
    ('Ketu', const.SOUTH_NODE),
]

from astro_events import get_nakshatra_info, get_tithi_info

def get_aspects(positions):
    aspect_angles = {
        'Conjunction': 0,
        'Opposition': 180,
        'Trine': 120,
        'Square': 90,
        'Sextile': 60
    }
    orb = 6  # degree tolerance
    aspects_found = []
    planet_names = list(positions.keys())
    for i in range(len(planet_names)):
        for j in range(i+1, len(planet_names)):
            p1, p2 = planet_names[i], planet_names[j]
            lon1, lon2 = positions[p1], positions[p2]
            diff = abs(lon1 - lon2)
            diff = min(diff, 360 - diff)  # handle wrap-around
            for aspect, angle in aspect_angles.items():
                if abs(diff - angle) <= orb:
                    aspects_found.append(f"{p1} {aspect} {p2} ({diff:.1f}°)")
    if aspects_found:
        return ", ".join(aspects_found)
    else:
        return "None"

def get_planet_positions(dt):
    # Use UTC time and a default location (0,0)
    date_str = dt.strftime('%Y/%m/%d')
    time_str = dt.strftime('%H:%M')
    pos = GeoPos(0, 0)
    chart = Chart(Datetime(date_str, time_str, '+00:00'), pos)
    positions = {}
    for name, key in PLANETS:
        positions[name] = chart.get(key).lon
    return positions

def get_astro_report(dt):
    # Compute required context for summaries
    positions = get_planet_positions(dt)
    nakshatra = get_nakshatra_info(dt)
    tithi = get_tithi_info(dt)
    # For now, create a single period for the whole day
    periods = [{
        'start_time': dt,
        'end_time': dt + timedelta(hours=24),
        'event': nakshatra
    }]

    # Compose each section using modular summary functions
    astro_summary = get_astro_summary(dt, positions, nakshatra, tithi, periods)
    ict_summary = get_ict_summary(dt)
    gann_summary = get_gann_summary(dt)
    news_summary = get_news_summary(dt)
    global_summary = get_global_market_summary(dt)
    # Compose overall report
    sections = [news_summary, global_summary, ict_summary, gann_summary, astro_summary]
    report = get_overall_summary(dt, sections)
    # Add live XAUUSD price (Metalpriceapi)
    try:
        from live_xauusd import get_live_xauusd_price
        live_val = get_live_xauusd_price()
        if live_val and live_val > 0:
            xauusd = 1 / live_val
            live_price_str = f"<b>Live XAUUSD price:</b> {xauusd:,.2f} (Metalpriceapi)\n"
        else:
            live_price_str = "<b>Live XAUUSD price:</b> N/A (Metalpriceapi)\n"
    except Exception as e:
        live_price_str = f"<b>Live XAUUSD price:</b> Error fetching ({e})\n"
    return live_price_str + report
def get_market_news(dt):
    # Forex Factory economic calendar for market-moving events
    import requests
    from xml.etree import ElementTree as ET
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
            # Parse event time (UTC)
            try:
                event_dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            except Exception:
                event_dt = None
            # Only show high/medium impact and gold/USD/major events
            if impact in ['High', 'Medium'] and (
                'USD' in country or 'Gold' in title or 'FOMC' in title or 'CPI' in title or 'NFP' in title or 'Fed' in title or 'PCE' in title or 'Unemployment' in title or 'GDP' in title):
                # Estimate realization time: event time + 15-30 min
                realization_dt = event_dt + timedelta(minutes=30) if event_dt else None
                # Get detailed aspects at event and realization time
                def detailed_aspects(dt):
                    pos = get_planet_positions(dt)
                    aspect_angles = {
                        'Conjunction': 0,
                        'Opposition': 180,
                        'Trine': 120,
                        'Square': 90,
                        'Sextile': 60
                    }
                    orb = 6
                    details = []
                    for p1, k1 in PLANETS:
                        for p2, k2 in PLANETS:
                            if p1 >= p2:
                                continue
                            lon1, lon2 = pos[p1], pos[p2]
                            diff = abs(lon1 - lon2)
                            diff = min(diff, 360 - diff)
                            for aspect, angle in aspect_angles.items():
                                if abs(diff - angle) <= orb:
                                    # Simple effect mapping
                                    if p1 == 'Moon' or p2 == 'Moon':
                                        effect = 'Short-term volatility'
                                    elif p1 == 'Sun' or p2 == 'Sun':
                                        effect = 'Trend bias'
                                    elif p1 == 'Venus' or p2 == 'Venus':
                                        effect = 'Gold demand/sentiment'
                                    elif p1 == 'Mars' or p2 == 'Mars':
                                        effect = 'Breakout/impulse risk'
                                    else:
                                        effect = 'General astro influence'
                                    details.append(f"{p1}-{p2} {aspect} ({diff:.1f}°): {effect}")
                    return ", ".join(details) if details else 'None'
                aspects_event = detailed_aspects(event_dt) if event_dt else 'N/A'
                aspects_real = detailed_aspects(realization_dt) if realization_dt else 'N/A'
                # Format times
                event_time_str = event_dt.strftime('%Y-%m-%d %H:%M UTC') if event_dt else 'N/A'
                real_time_str = realization_dt.strftime('%Y-%m-%d %H:%M UTC') if realization_dt else 'N/A'
                news_items.append(
                    f"<b>{impact} Impact</b> | {country} | {title}\n"
                    f"Release: {event_time_str} | Realization: {real_time_str}\n"
                    f"Aspects at release: {aspects_event}\nAspects at realization: {aspects_real}\n"
                )
    except Exception as e:
        news_items.append(f"Error fetching Forex Factory news: {e}")
    if not news_items:
        news_items.append("No major market-moving news events found.")
    return '\n'.join(news_items)
