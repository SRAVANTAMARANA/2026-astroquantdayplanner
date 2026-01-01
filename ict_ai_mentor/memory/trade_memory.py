import json
from datetime import datetime

FILE = "memory/trades.json"

def save_trade(signal):
    signal["time"] = datetime.utcnow().isoformat()
    import json, datetime
    try:
        data = json.load(open(FILE))
    except:
        data = []
    data.append(signal)
    json.dump(data, open(FILE,"w"), indent=2)
