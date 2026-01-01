def build_signal(htf_bias, liquidity, fvg):
    if htf_bias == "BEARISH" and liquidity and fvg:
        return {
            "symbol": "XAUUSD",
            "direction": "SELL",
            "entry": "2372 – 2373",
            "sl": 2378,
            "tp": [2362, 2354],
            "session": "NY Killzone",
            "probability": 78,
            "reason": [
                "HTF bearish structure",
                "Liquidity sweep",
                "Bearish FVG"
            ]
        }
    return None
