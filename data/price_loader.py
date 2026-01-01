import pandas as pd

def load_price_data():
    # Placeholder: Load your price data here (e.g., from CSV, API, etc.)
    # For demo, return a DataFrame with required columns
    data = {
        'high': [2000, 2010, 2025],
        'low': [1980, 1995, 2005],
        'close': [1990, 2000, 2020]
    }
    return pd.DataFrame(data)
