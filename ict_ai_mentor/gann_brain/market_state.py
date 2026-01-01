def market_state(trend_strength):
    if trend_strength > 70:
        return "TREND"
    elif trend_strength < 30:
        return "RANGE"
    else:
        return "TRANSITION"
