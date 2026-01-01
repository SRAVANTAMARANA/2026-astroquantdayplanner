def detect_smt(asset1, asset2):
    # asset1 = XAUUSD, asset2 = DXY (example)
    if asset1.high.iloc[-1] > asset1.high.iloc[-2] and \
       asset2.high.iloc[-1] <= asset2.high.iloc[-2]:
        return "BEARISH_SMT"

    if asset1.low.iloc[-1] < asset1.low.iloc[-2] and \
       asset2.low.iloc[-1] >= asset2.low.iloc[-2]:
        return "BULLISH_SMT"

    return None
