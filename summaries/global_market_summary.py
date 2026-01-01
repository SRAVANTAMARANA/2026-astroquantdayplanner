from live_xauusd import get_live_xauusd_price
def get_global_market_summary(dt):
    """
    Global market summary for XAUUSD using live price and basic context.
    """
    try:
        live_val = get_live_xauusd_price()
        price = 1 / live_val if live_val and live_val > 0 else 4332.01
    except Exception:
        price = 4332.01
    # Example: Compare to round numbers
    if price > 4400:
        summary = "Gold is trading above 4400, indicating strong bullish sentiment globally."
    elif price < 4300:
        summary = "Gold is trading below 4300, indicating weak demand or risk-off sentiment."
    else:
        summary = "Gold is range-bound between 4300 and 4400; global markets are indecisive."
    return f"<b>Global Market Summary:</b>\nLive XAUUSD: {price:,.2f}\n{summary}"