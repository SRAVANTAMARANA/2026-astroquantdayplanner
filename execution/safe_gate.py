def allow_trade(memory, session):
    today_trades = [t for t in memory if t["session"] == session]
    return len(today_trades) == 0
