"""
get_telegram_chat_id.py
----------------------
Get Telegram Chat ID utility
Prints chat ID from incoming Telegram webhook JSON, with docstrings and error handling.
"""

import sys
import json
import logging

def main():
    """
    Main function to extract and print Telegram chat ID from webhook JSON file.
    Usage: python get_telegram_chat_id.py <webhook_json_file>
    """
    if len(sys.argv) < 2:
        print("Usage: python get_telegram_chat_id.py <webhook_json_file>")
        return
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        chat_id = data.get('message', {}).get('chat', {}).get('id')
        print(f"Chat ID: {chat_id}")
    except Exception as e:
        logging.error(f"Error reading chat ID: {e}")
        print("Failed to extract chat ID.")

if __name__ == "__main__":
    main()
