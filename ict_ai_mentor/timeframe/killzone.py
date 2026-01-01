from datetime import datetime
import pytz

def is_killzone():
    ist = pytz.timezone("Asia/Kolkata")
    t = datetime.now(ist)
    h, m = t.hour, t.minute
    if (13 <= h <= 16) or (18 <= h <= 21):
        return "KILLZONE"
    return None
