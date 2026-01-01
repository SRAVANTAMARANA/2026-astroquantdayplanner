"""
live_xauusd.py
--------------
Fetches live XAUUSD price from Metals-API (free tier, 1-min delay, 50 requests/month).
Docs: https://metals-api.com/
"""

import requests
import os

def get_live_xauusd_price():
    API_KEY = '4de7f6989cfe44ebc8992d0ce88ec014'
    url = f'https://api.metalpriceapi.com/v1/latest?api_key={API_KEY}&base=USD&currencies=XAU'
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if resp.status_code == 200 and 'rates' in data and 'XAU' in data['rates']:
            # Metalpriceapi returns price as USD per XAU (ounce)
            price = data['rates']['XAU']
            return price
        else:
            print(f"Metalpriceapi error: {data.get('error', resp.text)}")
            return None
    except Exception as e:
        print(f"Metalpriceapi fetch error: {e}")
        return None

if __name__ == "__main__":
    price = get_live_xauusd_price()
    print(f"Live XAUUSD price: {price}")
