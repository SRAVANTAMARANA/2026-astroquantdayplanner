import requests

def send_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def format_signal(direction, cycle, planet, degree, price):
    return f"""
🔯 *GANN ASTRO SIGNAL — XAUUSD*

Type: *{direction}*
Time Cycle: {cycle}
Planet: {planet} @ {degree}°
Price: {price}

Rule:
✔ Time fulfilled
✔ Planet activated
✔ Price at geometry

Risk ≤ 1%
Max trades/month: 2
"""
