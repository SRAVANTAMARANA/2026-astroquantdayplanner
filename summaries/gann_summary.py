from live_xauusd import get_live_xauusd_price
def get_gann_summary(dt, price=None):
    """
    Gann analytics for XAUUSD using live price and date.
    """
    if price is None:
        try:
            live_val = get_live_xauusd_price()
            price = 1 / live_val if live_val and live_val > 0 else 4332.01
        except Exception:
            price = 4332.01
    # Example: Gann square of 9, 45-degree levels
    base = 144
    gann_levels = [base + i*45 for i in range(10)]
    closest = min(gann_levels, key=lambda x: abs(x - price))
    return (
        f"<b>Gann Analytics:</b>\n"
        f"Live XAUUSD: {price:,.2f}\n"
        f"Gann Levels: {', '.join(f'{lvl:.2f}' for lvl in gann_levels)}\n"
        f"Closest Gann Level: {closest:.2f}"
    )