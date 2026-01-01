def detect_smt(xau, dxy):
    if xau.high.iloc[-1] > xau.high.iloc[-2] and \
       dxy.high.iloc[-1] <= dxy.high.iloc[-2]:
        return "BEARISH"
    return None
