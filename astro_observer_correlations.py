def safe_get(func, dt):
def encode_categorical(series):
def main():

"""
astro_observer_correlations.py
-----------------------------
Computes correlations between astro features (nakshatra, tithi, planetary positions) and XAUUSD price moves.
Includes ICT pattern frequency and their impact on price.
Outputs a detailed Excel file with correlation matrices and summary analytics.
"""

import pandas as pd
from datetime import datetime, timedelta
from astro_events import get_nakshatra_info, get_tithi_info
from xauusd_chart import fetch_xauusd_ohlc
from daily_astro_telegram import detect_ict_patterns, get_planet_positions
import numpy as np
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

def encode_categorical(series):
    """Encode categorical pandas series as integer codes."""
    return pd.factorize(series)[0]

def process_day(current):
    """Process a single day's astro and price data for correlation analysis."""
    day_str = current.strftime('%Y-%m-%d')
    nakshatra = safe_get(get_nakshatra_info, current)
    tithi = safe_get(get_tithi_info, current)
    planet_pos = safe_get(get_planet_positions, current)
    ohlc = fetch_xauusd_ohlc(current)
    d1 = ohlc.get('D1', pd.DataFrame())
    d1_row = d1.loc[d1.index.date == current.date()].iloc[0] if not d1.empty and (d1.index.date == current.date()).any() else None
    ict = detect_ict_patterns(ohlc)
    return {
        'date': day_str,
        'nakshatra': nakshatra.get('nakshatra') if isinstance(nakshatra, dict) else nakshatra,
        'tithi': tithi.get('tithi') if isinstance(tithi, dict) else tithi,
        'sun': planet_pos.get('Sun') if isinstance(planet_pos, dict) else None,
        'moon': planet_pos.get('Moon') if isinstance(planet_pos, dict) else None,
        'open': d1_row['open'] if d1_row is not None else None,
        'close': d1_row['close'] if d1_row is not None else None,
        'high': d1_row['high'] if d1_row is not None else None,
        'low': d1_row['low'] if d1_row is not None else None,
        'ict_patterns': str(ict),
        'ict_displacement': ict.get('displacement') if isinstance(ict, dict) else None,
        'ict_manipulation': ict.get('manipulation') if isinstance(ict, dict) else None,
        'ict_accumulation': ict.get('accumulation') if isinstance(ict, dict) else None,
    }

def main(start_date=None, end_date=None):
    """Main function to process astro and price data for correlation analysis."""
    start_date, end_date = get_date_range(start_date, end_date)
    results = []
    current = start_date
    while current <= end_date:
        results.append(process_day(current))
        print(f"Processed {current.strftime('%Y-%m-%d')}")
        current += timedelta(days=1)
    # DataFrame
    df = pd.DataFrame(results)
    # Encode categorical astro features
    df['nakshatra_code'] = encode_categorical(df['nakshatra'])
    df['tithi_code'] = encode_categorical(df['tithi'])
    # Calculate price returns
    df['return'] = df['close'] - df['open']
    # Correlation matrix (astro features vs. price return)
    corr = df[['nakshatra_code','tithi_code','sun','moon','return']].corr()
    # ICT pattern impact
    ict_impact = df.groupby('ict_patterns')['return'].agg(['mean','std','count'])
    # Save to Excel
    with pd.ExcelWriter('astro_observer_correlations.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='AstroData')
        corr.to_excel(writer, sheet_name='Correlations')
        ict_impact.to_excel(writer, sheet_name='ICT_Impact')
    print("Saved astro_observer_correlations.xlsx")

if __name__ == "__main__":
    main()
