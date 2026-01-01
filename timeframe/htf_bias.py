def determine_htf_bias(df):
    # Placeholder: Use your logic for HTF bias
    # For demo, alternate BULLISH/BEARISH
    return "BULLISH" if df.close.iloc[-1] % 2 == 0 else "BEARISH"
