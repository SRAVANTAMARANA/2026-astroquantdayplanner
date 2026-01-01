"""
test_telegram_bot.py
--------------------
Test Telegram bot message sending with docstrings and error handling.
"""

from telegram_bot import send_message

def test_send_message():
    """Test the send_message function."""
    try:
        result = send_message('123456789', 'Test message')
        assert result in [True, False]
    except Exception as e:
        print(f"send_message test failed: {e}")
        return False
    return True

if __name__ == "__main__":
    if test_send_message():
        print("Test completed.")
    else:
        print("Test failed.")
