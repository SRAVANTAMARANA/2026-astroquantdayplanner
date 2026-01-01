# feedback.py
"""
Feedback module for AstroQuant Day Planner
- Collects user feedback via Telegram command or message
- Logs feedback to a file for review
"""
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

FEEDBACK_LOG = 'user_feedback.log'

def log_feedback(user_id, message):
    with open(FEEDBACK_LOG, 'a') as f:
        f.write(f"User {user_id}: {message}\n")
    logging.info(f"Feedback logged from {user_id}")

def send_feedback_request():
    text = (
        "We value your feedback!\n"
        "Reply to this message or use /feedback <your message> to help us improve the daily report."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def save_feedback(user_id, feedback_text):
    """Save user feedback to a log file."""
    log_feedback(user_id, feedback_text)
    return True

def get_all_feedback():
    """Retrieve all feedback entries from the log file."""
    feedback_list = []
    try:
        with open(FEEDBACK_LOG, 'r') as f:
            for line in f:
                if line.startswith("User "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) == 2:
                        user = parts[0][5:]
                        feedback = parts[1]
                        feedback_list.append({'user_id': user, 'feedback': feedback})
    except Exception as e:
        logging.error(f"Failed to read feedback log: {e}")
    return feedback_list
