def premium_discount_zone(df):
    high = df.high.max()
    low = df.low.min()
    eq = (high + low) / 2
    price = df.close.iloc[-1]

    if price > eq:
        return "PREMIUM"
    elif price < eq:
        return "DISCOUNT"
    return "EQUILIBRIUM"
