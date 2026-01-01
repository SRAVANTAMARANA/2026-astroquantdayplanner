def detect_fvg(df):
    if df.low.iloc[-1] > df.high.iloc[-3]:
        return "BEARISH_FVG"
    return None
