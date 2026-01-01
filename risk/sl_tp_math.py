def calculate_sl_tp(df, direction):
    if direction == "SELL":
        sl = df.high.max() + 0.3  # Above liquidity
        tp1 = df.low.min()
        tp2 = tp1 - (sl - tp1) * 1.5
    else:
        sl = df.low.min() - 0.3
        tp1 = df.high.max()
        tp2 = tp1 + (tp1 - sl) * 1.5
    return round(sl, 2), round(tp1, 2), round(tp2, 2)

def lot_size(balance, risk_pct, sl_points):
    risk_amount = balance * (risk_pct / 100)
    lot = risk_amount / sl_points
    return round(lot, 2)
