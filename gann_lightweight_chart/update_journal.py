import csv
from datetime import datetime

def add_journal_entry(entry, filename="journal_template.csv"):
    headers = [
        "date","time","cycle","planet","degree","price","geometry_zone","market_state","entry_type","outcome","notes"
    ]
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            existing = list(reader)
            if existing and existing[0] != headers:
                raise Exception("CSV headers do not match expected format.")
    except FileNotFoundError:
        existing = [headers]
    with open(filename, "a", newline='') as f:
        writer = csv.writer(f)
        if len(existing) == 0:
            writer.writerow(headers)
        writer.writerow([entry.get(h,"") for h in headers])

# Example usage:
if __name__ == "__main__":
    add_journal_entry({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "cycle": 9,
        "planet": "Mars",
        "degree": 90,
        "price": 2105,
        "geometry_zone": "2090-2100",
        "market_state": "TREND",
        "entry_type": "SELL",
        "outcome": "win",
        "notes": "signal fired, trade taken"
    })
    print("Journal entry added.")
