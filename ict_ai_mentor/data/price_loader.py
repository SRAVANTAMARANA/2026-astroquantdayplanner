import pandas as pd

def load_price_data():
    # TEMP: dummy data (replace later with live feed)
    data = {
        "open": [2370, 2372, 2374, 2373],
        "high": [2373, 2376, 2375, 2374],
        "low": [2368, 2370, 2372, 2371],
        "close": [2372, 2374, 2373, 2372],
    }
    return pd.DataFrame(data)
# 👉 (Later we’ll connect live data / TradingView / broker)
