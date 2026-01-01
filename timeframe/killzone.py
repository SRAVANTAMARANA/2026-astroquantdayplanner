from datetime import datetime
import pytz

def is_killzone():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    h, m = now.hour, now.minute

    # London Killzone: 1:30–4:30 PM IST
    if (h == 13 and m >= 30) or (14 <= h <= 16) or (h == 16 and m <= 30):
        return "LONDON"

    # New York Killzone: 6:30–9:30 PM IST
    if (h == 18 and m >= 30) or (19 <= h <= 21) or (h == 21 and m <= 30):
        return "NEW YORK"

    return None
