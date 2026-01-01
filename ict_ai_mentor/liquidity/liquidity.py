def detect_liquidity_sweep(df):
    # Placeholder: Use your logic for liquidity sweep
    # For demo, return True if high > 2000
    return df.high.iloc[-1] > 2000
