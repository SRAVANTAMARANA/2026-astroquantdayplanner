import requests
from config import BOT_TOKEN, CHAT_ID

def send_telegram(signal):
    text = f"""
📊 ICT AI MENTOR SIGNAL

📌 Symbol: {signal['symbol']}
📉 Direction: {signal['direction']}
🎯 Entry: {signal['entry']}
🛑 SL: {signal['sl']}
🎯 TP: {signal['tp']}

🧠 Reason:
"""
        msg = f"""
    📊 ICT AI MENTOR SIGNAL

    Symbol: {signal['symbol']}
    Direction: {signal['direction']}
    Probability: {signal['probability']}%

    Reason:
    """ + "\n".join(signal["reason"])
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
