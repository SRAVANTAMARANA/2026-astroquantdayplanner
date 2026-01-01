"""
xauusd_chart.py
---------------
XAUUSD Chart Data Fetcher
Fetches OHLC data for XAUUSD from a demo API or CSV, with docstrings and error handling.
"""

import requests
import pandas as pd
from datetime import datetime
import os
import logging
import yfinance as yf
from alpha_vantage.foreignexchange import ForeignExchange
import time
from config import TWELVEDATA_API_KEY

def fetch_xauusd_ohlc(dt=None):
    """
    Fetch OHLC data for XAUUSD for the given date.
    Args:
        dt (datetime): The date for which to fetch data.
    Returns:
        dict: Dictionary with 'D1' key and DataFrame value.
    """
    # Try SteadyAPI first
    ohlc_data = {}
    import os
    import pandas as pd
    import requests
    STEADYAPI_KEY = os.getenv('STEADYAPI_KEY', 'OsRPFPXCC5pt52cRjo3hrXghPk6Ig5vJXnjFE6nn')
    try:
        url = 'https://api.steadyapi.com/v1/markets/ohlc'
        params = {
            'symbol': 'XAUUSD',
            'interval': '1d',
            'limit': 2
        }
        headers = {
            'Authorization': f'Bearer {STEADYAPI_KEY}'
        }
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            # Assume data['data'] is a list of dicts with keys: time, open, high, low, close
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                # SteadyAPI returns ISO8601 or unix timestamp for 'time'
                if 'time' in df:
                    try:
                        df['datetime'] = pd.to_datetime(df['time'], unit='s')
                    except Exception:
                        df['datetime'] = pd.to_datetime(df['time'])
                else:
                    df['datetime'] = pd.to_datetime(df['datetime'])
                df.set_index('datetime', inplace=True)
                for col in ['open', 'high', 'low', 'close']:
                    df[col] = df[col].astype(float)
                ohlc_data['D1'] = df[['open','high','low','close']]
        else:
            print(f"SteadyAPI error: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"SteadyAPI fetch error: {e}")

    # If SteadyAPI fails, fallback to Yahoo Finance (spot, then futures), then Google, then Stooq
    if 'D1' not in ohlc_data or ohlc_data['D1'].empty:
        import warnings
        # Try Yahoo Finance spot first
        for yf_symbol in ['XAUUSD=X', 'GC=F']:
            try:
                if dt is not None:
                    start = dt.strftime('%Y-%m-%d')
                    end = (dt + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    start = None
                    end = None
                ticker = yf.Ticker(yf_symbol)
                d1_df = ticker.history(start=start, end=end, interval='1d')
                if not d1_df.empty:
                    d1_df = d1_df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
                    ohlc_data['D1'] = d1_df[['open','high','low','close']]
                    break
            except Exception as e:
                print(f"Yahoo Finance D1 fetch error for {yf_symbol}: {e}")
        # H1 (hourly)
        try:
            ticker = yf.Ticker('XAUUSD=X')
            h1_df = ticker.history(start=start, end=end, interval='60m')
            if not h1_df.empty:
                h1_df = h1_df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
                ohlc_data['H1'] = h1_df[['open','high','low','close']]
            else:
                ohlc_data['H1'] = pd.DataFrame()
        except Exception as e:
            print(f"Yahoo Finance H1 fetch error: {e}")
            ohlc_data['H1'] = pd.DataFrame()
        # M15 (15min)
        try:
            ticker = yf.Ticker('XAUUSD=X')
            m15_df = ticker.history(start=start, end=end, interval='15m')
            if not m15_df.empty:
                m15_df = m15_df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
                ohlc_data['M15'] = m15_df[['open','high','low','close']]
            else:
                ohlc_data['M15'] = pd.DataFrame()
        except Exception as e:
            print(f"Yahoo Finance M15 fetch error: {e}")
            ohlc_data['M15'] = pd.DataFrame()
        # M5 (5min) not supported by Yahoo Finance
        ohlc_data['M5'] = pd.DataFrame()
        # If still empty, try Google Finance via pandas_datareader
        all_empty = all((df is None or df.empty) for df in ohlc_data.values())
        if all_empty:
            try:
                from pandas_datareader import data as pdr
                # Google Finance symbol for XAUUSD is 'CURRENCY:XAUUSD'
                if dt is not None:
                    start = dt.strftime('%Y-%m-%d')
                    end = (dt + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    start = None
                    end = None
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    g_df = pdr.DataReader('XAUUSD=X', 'yahoo', start, end)
                if not g_df.empty:
                    g_df = g_df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
                    ohlc_data['D1'] = g_df[['open','high','low','close']]
                    print("Google Finance fallback (via pandas_datareader/yahoo) succeeded.")
            except Exception as e:
                print(f"Google Finance fallback error: {e}")
        # Fallback to Investing.com CSV scrape (Stooq) if all others fail
        all_empty = all((df is None or df.empty) for df in ohlc_data.values())
        if all_empty:
            print("Yahoo/Google Finance failed. Trying Stooq fallback.")
            try:
                import io
                url = "https://stooq.com/q/d/l/?s=xauusd&d1=20250101&d2=20251231&i=d"
                resp = requests.get(url)
                if resp.status_code == 200:
                    df = pd.read_csv(io.StringIO(resp.text))
                    df['Date'] = pd.to_datetime(df['Date'])
                    df.set_index('Date', inplace=True)
                    df = df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
                    # Filter for the requested date, fallback to most recent if missing
                    if dt is not None:
                        day_df = df[df.index.date == dt.date()]
                        if not day_df.empty:
                            ohlc_data['D1'] = day_df[['open','high','low','close']]
                        else:
                            # Fallback: use the most recent available row before the requested date
                            fallback_df = df[df.index.date < dt.date()]
                            if not fallback_df.empty:
                                last_row = fallback_df.iloc[-1:]
                                ohlc_data['D1'] = last_row[['open','high','low','close']]
                                print(f"Stooq fallback: using most recent available D1 for {last_row.index[0].date()}")
                            else:
                                ohlc_data['D1'] = pd.DataFrame()
                    else:
                        ohlc_data['D1'] = df[['open','high','low','close']]
                else:
                    ohlc_data['D1'] = pd.DataFrame()
            except Exception as e:
                print(f"Stooq fallback error: {e}")
                ohlc_data['D1'] = pd.DataFrame()
    return ohlc_data

def get_xauusd_chart_url(interval="1h", outputsize=100):
    """
    Generate the chart URL for XAUUSD.
    Args:
        interval (str): The interval for the chart.
        outputsize (int): The number of data points to return.
    Returns:
        str: The chart URL.
    """
    # TradingView free chart widget URL (embed)
    # Example: https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD
    # For direct chart page:
    chart_url = f"https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD"
    return chart_url

def get_tradingview_embed_widget(symbol="OANDA:XAUUSD", interval="60", theme="light", width=600, height=400):
    """
    Returns HTML iframe code for TradingView free chart widget for the given symbol.
    Args:
        symbol (str): TradingView symbol, e.g., 'OANDA:XAUUSD'
        interval (str): Chart interval ("1", "5", "15", "60", "D", etc.)
        theme (str): 'light' or 'dark'
        width (int): Width in px
        height (int): Height in px
    Returns:
        str: HTML iframe code for embedding the chart
    """
    return f'''<iframe src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={interval}&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme={theme}&style=1&timezone=Etc/UTC&withdateranges=1&hideideas=1&studies_overrides=&overrides=&enabled_features=&disabled_features=&locale=en&utm_source=localhost&utm_medium=widget&utm_campaign=chart&utm_term={symbol}" width="{width}" height="{height}" frameborder="0" allowtransparency="true" scrolling="no"></iframe>'''
def download_chart_image(chart_url, filename="xauusd_chart.png"):
    """
    Download the chart image from the URL.
    Args:
        chart_url (str): The URL of the chart image.
        filename (str): The filename to save the image as.
    Returns:
        str: The filename of the saved image.
    """
    resp = requests.get(chart_url)
    if resp.status_code == 200:
        with open(filename, "wb") as f:
            f.write(resp.content)
        return filename
    return None

if __name__ == "__main__":
    dt = datetime.utcnow()
    print(fetch_xauusd_ohlc(dt))
