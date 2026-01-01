def safe_get(func, dt):
def main():

"""
astro_observer.py
-----------------
Analyze and record daily astro events, XAUUSD price, and ICT logic for the past 3 years.
Outputs a CSV file with all results.
"""

import pandas as pd
from datetime import datetime, timedelta
from astro_events import get_nakshatra_info, get_tithi_info
from xauusd_chart import fetch_xauusd_ohlc
from daily_astro_telegram import detect_ict_patterns
import logging

def safe_get(func, dt):
    """Safely call a function and return its result or error as string."""
    try:
        return func(dt)
    except Exception as e:
        logging.error(f"Error in {func.__name__} for {dt}: {e}")
        return str(e)

def get_date_range(start_date=None, end_date=None, years=3):
    """Get start and end datetime objects for the analysis period."""
    if start_date is None:
        start_date = datetime.utcnow() - timedelta(days=years*365)
    if end_date is None:
        end_date = datetime.utcnow()
    return start_date, end_date

def process_day(current):
    """Process a single day's astro and price data."""
    day_str = current.strftime('%Y-%m-%d')
    nakshatra = safe_get(get_nakshatra_info, current)
    tithi = safe_get(get_tithi_info, current)
    ohlc = fetch_xauusd_ohlc(current)
    d1 = ohlc.get('D1', pd.DataFrame())
    d1_row = d1.loc[d1.index.date == current.date()].iloc[0] if not d1.empty and (d1.index.date == current.date()).any() else None
    ict = detect_ict_patterns(ohlc)
    return {
        'date': day_str,
        'nakshatra': nakshatra.get('nakshatra') if isinstance(nakshatra, dict) else nakshatra,
        'tithi': tithi.get('tithi') if isinstance(tithi, dict) else tithi,
        'open': d1_row['open'] if d1_row is not None else None,
        'high': d1_row['high'] if d1_row is not None else None,
        'low': d1_row['low'] if d1_row is not None else None,
        'close': d1_row['close'] if d1_row is not None else None,
        'ict_patterns': str(ict),
    }

def main(start_date=None, end_date=None):
    """Main function to process astro and price data for the given date range."""
    start_date, end_date = get_date_range(start_date, end_date)
    results = []
    current = start_date
    while current <= end_date:
        results.append(process_day(current))
        print(f"Processed {current.strftime('%Y-%m-%d')}")
        current += timedelta(days=1)
    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv('astro_observer_report.csv', index=False)
    print("Saved astro_observer_report.csv")

if __name__ == "__main__":
    main()
