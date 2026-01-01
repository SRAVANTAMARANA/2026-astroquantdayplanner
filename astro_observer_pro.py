"""
Astro Observer Pro
------------------
Advanced analytics for 3 years of XAUUSD, astro events, ICT signals, and their timings.
Features:
- Correlates ICT pattern timings with planetary positions and astro events.
- Simulates simple trade strategies based on combined signals.
- Outputs a detailed Excel report with analytics and visualizations.
"""
def safe_get(func, dt):
def main():

import pandas as pd
from datetime import datetime, timedelta
from astro_events import get_nakshatra_info, get_tithi_info
from xauusd_chart import fetch_xauusd_ohlc
from daily_astro_telegram import detect_ict_patterns, get_planet_positions

START_DATE = datetime.utcnow() - timedelta(days=3*365)
END_DATE = datetime.utcnow()

def safe_get(func, dt):
    """Safely call a function and return its result or error as string."""
    try:
        return func(dt)
    except Exception as e:
        return str(e)

def detect_ict_timing(h1, day_str):
    """Detect ICT pattern timings and related astro data for each hour."""
    ict_timing = []
    if h1 is not None and not h1.empty:
        mean_range = h1['high'].sub(h1['low']).mean()
        for idx, row in h1.iterrows():
            patterns = []
            rng = row['high'] - row['low']
            body = abs(row['close'] - row['open'])
            if rng > mean_range * 1.5:
                patterns.append('Manipulation')
    return ict_timing
        mean_range = h1['high'].sub(h1['low']).mean()
            body = abs(row['close'] - row['open'])

            """
            astro_observer_pro.py
            --------------------
            Advanced analytics for XAUUSD using astro and ICT features.
            Computes rolling statistics, correlations, and outputs to Excel.
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

            def get_date_range(start_date=None, end_date=None, years=2):
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
                """Process a single day's astro and price data for analytics."""
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
                    'ict_displacement': ict.get('displacement') if isinstance(ict, dict) else None,
                    'ict_manipulation': ict.get('manipulation') if isinstance(ict, dict) else None,
                    'ict_accumulation': ict.get('accumulation') if isinstance(ict, dict) else None,
                }

            def main(start_date=None, end_date=None):
                """Main function to process astro and price data for analytics."""
                start_date, end_date = get_date_range(start_date, end_date)
                results = []
                current = start_date
                while current <= end_date:
                    results.append(process_day(current))
                    print(f"Processed {current.strftime('%Y-%m-%d')}")
                    current += timedelta(days=1)
                df = pd.DataFrame(results)
                df['nakshatra_code'] = encode_categorical(df['nakshatra'])
                df['tithi_code'] = encode_categorical(df['tithi'])
                df['return'] = df['close'] - df['open']
                # Rolling stats
                df['rolling_mean'] = df['return'].rolling(window=20).mean()
                df['rolling_std'] = df['return'].rolling(window=20).std()
                # Correlations
                corr = df[['nakshatra_code','tithi_code','sun','moon','ict_displacement','ict_manipulation','ict_accumulation','return']].corr()
                # Save to Excel
                with pd.ExcelWriter('astro_observer_pro.xlsx') as writer:
                    df.to_excel(writer, index=False, sheet_name='AstroData')
                    corr.to_excel(writer, sheet_name='Correlations')
                print("Saved astro_observer_pro.xlsx")

            if __name__ == "__main__":
                main()
            'high': d1_row['high'] if d1_row is not None else None,
            'low': d1_row['low'] if d1_row is not None else None,
            'close': d1_row['close'] if d1_row is not None else None,
            'ict_timing': ict_timing,
        })
        print(f"Processed {day_str}")
        current += timedelta(days=1)
    # Save to Excel
    df = pd.DataFrame(results)
    trades = pd.DataFrame(all_trade_results)
    with pd.ExcelWriter('astro_observer_pro.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='AstroData')
        # ICT timing events
        ict_events = pd.DataFrame([e for r in results for e in r['ict_timing']])
        if not ict_events.empty:
            ict_events.to_excel(writer, index=False, sheet_name='ICT_Timings')
        # Trade simulation
        if not trades.empty:
            trades.to_excel(writer, index=False, sheet_name='TradeSim')
            # Summary stats
            stats = trades.describe(include='all')
            stats.to_excel(writer, sheet_name='TradeStats')
    print("Saved astro_observer_pro.xlsx")

if __name__ == "__main__":
    main()
