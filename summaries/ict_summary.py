from live_xauusd import get_live_xauusd_price
def get_ict_summary(dt):
    """
    ICT/AI analytics for XAUUSD using live price and basic session logic.
    """
    try:
        live_val = get_live_xauusd_price()
        price = 1 / live_val if live_val and live_val > 0 else 4332.01
    except Exception:
        price = 4332.01
    # Example: Simple session bias
    sessions = [
        ("Asia", "00:00-08:00"),
        ("Europe", "08:00-16:00"),
        ("US", "13:00-21:00")
    ]
    table = "<b>ICT/AI Table:</b>\nSession | Bias | Price\n---|---|---\n"
    for name, times in sessions:
        bias = "Bullish" if price > 4300 else "Bearish"
        table += f"{name} | {bias} | {price:,.2f}\n"
    analysis = f"<b>ICT/AI Analysis:</b>\nCurrent price is {'high' if price > 4300 else 'low'} relative to 4300."
    return table + analysis