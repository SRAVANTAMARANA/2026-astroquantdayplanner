def premium_discount_zone(df):
    high = df.high.max()
    low = df.low.min()
    eq = (high + low) / 2
    price = df.close.iloc[-1]
    return "PREMIUM" if price > eq else "DISCOUNT"
