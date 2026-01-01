def determine_htf_bias(df):
    if df.high.iloc[-1] > df.high.iloc[-2]:
        return "BEARISH"
    if df.high.iloc[-1] < df.high.iloc[-2]:
        return "BEARISH"
    if df.low.iloc[-1] > df.low.iloc[-2]:
        return "BULLISH"
    return "RANGE"
