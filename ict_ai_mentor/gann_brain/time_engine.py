from datetime import datetime

GANN_CYCLES = [9, 18, 45, 90]

def time_cycle_complete(anchor_date):
    today = datetime.utcnow().date()
    days = (today - anchor_date).days
    for cycle in GANN_CYCLES:
        if days % cycle == 0:
            return True, cycle
    return False, None
