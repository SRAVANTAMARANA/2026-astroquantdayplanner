
import time
import requests
import threading
import feedparser
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from daily_astro_telegram import get_market_news, get_astro_report, get_ict_ai_analysis
from datetime import datetime, timezone, timedelta

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def send_telegram_message(text, reply_to=None):
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    # Placeholder for sending a message, actual implementation below in send_message
    pass
def parse_forex_factory_events():

    """
    telegram_bot.py
    --------------
    Telegram Bot for AstroQuant Day Planner
    Handles commands, feedback, and daily reports with error handling and modular structure.
    """

    import os
    import requests
    from feedback import save_feedback
    from daily_astro_telegram import compose_message
    from datetime import datetime
    import logging

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None

    def send_message(chat_id, text):
        """
        Send a message to a Telegram chat.
        Args:
            chat_id (str): The chat ID to send the message to.
            text (str): The message text.
        Returns:
            bool: True if sent successfully, False otherwise.
        """
        if not BASE_URL:
            logging.error("TELEGRAM_TOKEN not set.")
            return False
        url = f"{BASE_URL}/sendMessage"
        payload = {'chat_id': chat_id, 'text': text}
        try:
            resp = requests.post(url, data=payload)
            if resp.status_code == 200:
                return True
            else:
                logging.error(f"Failed to send message: {resp.text}")
                return False
        except Exception as e:
            logging.error(f"Exception sending Telegram message: {e}")
            return False

    def handle_feedback(chat_id, user_id, text):
        """
        Handle feedback command from user.
        Args:
            chat_id (str): Telegram chat ID.
            user_id (str): Telegram user ID.
            text (str): The command text including feedback.
        """
        feedback_text = text.partition(' ')[2]
        if save_feedback(user_id, feedback_text):
            send_message(chat_id, "Thank you for your feedback!")
        else:
            send_message(chat_id, "Failed to save feedback. Please try again later.")

    def handle_daily_report(chat_id):
        """
        Handle daily report command.
        Args:
            chat_id (str): Telegram chat ID.
        """
        msg = compose_message(datetime.utcnow())
        send_message(chat_id, msg)

    def handle_command(chat_id, user_id, text):
        """
        Handle incoming Telegram bot commands.
        Args:
            chat_id (str): Telegram chat ID.
            user_id (str): Telegram user ID.
            text (str): The command text.
        """
        if text.startswith('/feedback'):
            handle_feedback(chat_id, user_id, text)
        elif text.startswith('/daily'):
            handle_daily_report(chat_id)
        else:
            send_message(chat_id, "Unknown command.")

    # Example usage (simulate incoming command)
    if __name__ == "__main__":
        chat_id = os.getenv('TELEGRAM_CHAT_ID') or '123456789'
        user_id = 'user_001'
        handle_command(chat_id, user_id, '/daily')
    # Parse impact and currency from title/summary
    # (The following code should be inside a function, not at top-level. If needed, refactor.)

def news_event_alert_loop():
    sent_events = set()
    while True:
        try:
            events = parse_forex_factory_events()
            now = datetime.now(timezone.utc)
            for event in events:
                # Alert 15 minutes before event
                if 0 <= (event["time"] - now).total_seconds() <= 900:
                    event_id = (event["title"], event["time"].isoformat())
                    if event_id not in sent_events:
                        # Compose alert message
                        msg = f"\U0001F514 <b>Upcoming News Event</b>\n"
                        msg += f"<b>Time:</b> {event['time'].strftime('%H:%M UTC')}\n"
                        msg += f"<b>Event:</b> {event['title']}\n"
                        msg += f"<b>Impact:</b> {event['impact']}\n"
                        msg += f"<b>Currency:</b> {event['currency']}\n"
                        msg += f"<b>Details:</b> {event['summary']}\n"
                        # Add market effect/analysis
                        if event['impact'] == 'High' and event['currency'] == 'USD':
                            msg += "\n<b>Market Effect:</b> High impact USD news can cause strong moves in XAUUSD and major pairs. Watch for volatility!\n"
                        elif event['impact'] == 'Medium':
                            msg += "\n<b>Market Effect:</b> Medium impact news may cause moderate moves.\n"
                        else:
                            msg += "\n<b>Market Effect:</b> Low impact or non-USD news, limited effect expected.\n"
                        # Add quick AI/ICT/astro forecast
                        msg += "\n<b>Current XAUUSD Analysis:</b>\n"
                        msg += get_ict_ai_analysis(now)
                        send_telegram_message(msg)
                        sent_events.add(event_id)
        except Exception as e:
            print(f"News alert error: {e}")
        time.sleep(60)

def main():
    # Start news alerting in background
    threading.Thread(target=news_event_alert_loop, daemon=True).start()
    last_update = None
    print("Bot started. Listening for messages and news events...")
    while True:
        updates = get_updates(last_update)
        for update in updates:
            msg = update.get("message")
            if msg and msg.get("chat", {}).get("id") == TELEGRAM_CHAT_ID:
                handle_message(msg)
                last_update = update["update_id"] + 1
        time.sleep(2)

if __name__ == "__main__":
    main()
