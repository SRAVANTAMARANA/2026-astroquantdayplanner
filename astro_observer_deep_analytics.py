def safe_get(func, dt):
def encode_categorical(series):
def main():

"""
astro_observer_deep_analytics.py
-------------------------------
Adds machine learning (ML) models to predict XAUUSD returns from astro and ICT features.
Computes feature importances, model accuracy, and advanced statistics.
Outputs an Excel file with all analytics, predictions, and insights.
"""

import pandas as pd
from datetime import datetime, timedelta
from astro_events import get_nakshatra_info, get_tithi_info
from xauusd_chart import fetch_xauusd_ohlc
from daily_astro_telegram import detect_ict_patterns, get_planet_positions
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
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
    """Process a single day's astro and price data for ML analysis."""
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
    """Main function to process astro and price data for ML analysis."""
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
    # ML: Predict return from astro+ICT features
    features = ['nakshatra_code','tithi_code','sun','moon','ict_displacement','ict_manipulation','ict_accumulation']
    valid_df = df.dropna(subset=features+['return'])
    print(f"Total rows: {len(df)}, valid rows for ML: {len(valid_df)}")
    if len(valid_df) == 0:
        print("No valid data available for ML modeling. Check data sources and feature extraction.")
        with pd.ExcelWriter('astro_observer_deep_analytics.xlsx') as writer:
            df.to_excel(writer, index=False, sheet_name='AstroData')
            pd.DataFrame({'error':['No valid data for ML']}).to_excel(writer, sheet_name='ML_Stats', index=False)
        return
    X = valid_df[features]
    y = valid_df['return']
    if len(X) < 2:
        print("Not enough data for train/test split. Need at least 2 valid rows.")
        with pd.ExcelWriter('astro_observer_deep_analytics.xlsx') as writer:
            df.to_excel(writer, index=False, sheet_name='AstroData')
            pd.DataFrame({'error':['Not enough data for train/test split']}).to_excel(writer, sheet_name='ML_Stats', index=False)
        return
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    importances = model.feature_importances_
    feat_imp = pd.DataFrame({'feature':features,'importance':importances}).sort_values('importance',ascending=False)
    # Save to Excel
    with pd.ExcelWriter('astro_observer_deep_analytics.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='AstroData')
        pd.DataFrame({'mse':[mse],'r2':[r2]}).to_excel(writer, sheet_name='ML_Stats', index=False)
        feat_imp.to_excel(writer, sheet_name='FeatureImportance', index=False)
        pd.DataFrame({'y_true':y_test,'y_pred':y_pred}).to_excel(writer, sheet_name='Predictions', index=False)
    print("Saved astro_observer_deep_analytics.xlsx")

if __name__ == "__main__":
    main()
