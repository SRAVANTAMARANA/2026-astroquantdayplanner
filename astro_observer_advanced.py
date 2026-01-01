def safe_get(func, dt):
def main():

"""
astro_observer_advanced.py
--------------------------
Records detailed astro events, planetary positions, nakshatra/tithi timings, and XAUUSD price for each day and hour over the past 3 years.
Outputs a detailed Excel file with summary statistics and a calendar-style sheet.
"""

import pandas as pd
from datetime import datetime, timedelta
from astro_events import get_nakshatra_info, get_tithi_info
from xauusd_chart import fetch_xauusd_ohlc
from daily_astro_telegram import detect_ict_patterns, get_planet_positions
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

def process_hour(current, hour, d1_row, ict):
    """Process a single hour's astro and price data."""
    dt_hour = current.replace(hour=hour, minute=0, second=0, microsecond=0)
    nak_hr = safe_get(get_nakshatra_info, dt_hour)
    tithi_hr = safe_get(get_tithi_info, dt_hour)
    planet_hr = safe_get(get_planet_positions, dt_hour)
    return {
        'date': current.strftime('%Y-%m-%d'),
        'hour': hour,
        'nakshatra': nak_hr.get('nakshatra') if isinstance(nak_hr, dict) else nak_hr,
        'tithi': tithi_hr.get('tithi') if isinstance(tithi_hr, dict) else tithi_hr,
        'planet_positions': str(planet_hr),
        'open': d1_row['open'] if d1_row is not None else None,
        'high': d1_row['high'] if d1_row is not None else None,
        'low': d1_row['low'] if d1_row is not None else None,
        'close': d1_row['close'] if d1_row is not None else None,
        'ict_patterns': str(ict),
    }

def main(start_date=None, end_date=None):
    """Main function to process detailed astro and price data for the given date range."""
    start_date, end_date = get_date_range(start_date, end_date)
    results = []
    current = start_date
    while current <= end_date:
        day_str = current.strftime('%Y-%m-%d')
        nakshatra = safe_get(get_nakshatra_info, current)
        tithi = safe_get(get_tithi_info, current)
        planet_pos = safe_get(get_planet_positions, current)
        ohlc = fetch_xauusd_ohlc(current)
        d1 = ohlc.get('D1', pd.DataFrame())
        d1_row = d1.loc[d1.index.date == current.date()].iloc[0] if not d1.empty and (d1.index.date == current.date()).any() else None
        ict = detect_ict_patterns(ohlc)
        for hour in range(0, 24):
            results.append(process_hour(current, hour, d1_row, ict))
        print(f"Processed {day_str}")
        current += timedelta(days=1)
    # Save to Excel
    df = pd.DataFrame(results)
    with pd.ExcelWriter('astro_observer_advanced.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='AstroData')
        # Calendar-style summary
        cal = df.groupby('date').agg({'open':'first','close':'last','nakshatra':'first','tithi':'first'}).reset_index()
        cal.to_excel(writer, index=False, sheet_name='CalendarSummary')
        # Summary stats
        stats = df.describe(include='all')
        stats.to_excel(writer, sheet_name='SummaryStats')
    print("Saved astro_observer_advanced.xlsx")

if __name__ == "__main__":
    main()
