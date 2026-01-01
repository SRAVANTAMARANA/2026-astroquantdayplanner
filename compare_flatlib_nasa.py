# Compare flatlib planetary longitude with NASA Horizons API
"""
Compare Flatlib and NASA ephemeris calculations for Sun/Moon positions with docstrings and error handling.
"""
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib import const
import requests
from datetime import datetime

def get_flatlib_longitude(planet, dt):
    """
    Get the Flatlib longitude for a given planet.
    Args:
        planet (str): The name of the planet.
        dt (datetime): The datetime for calculation.
    Returns:
        float: The longitude of the planet.
    """
    date_str = dt.strftime('%Y/%m/%d')
    time_str = dt.strftime('%H:%M')
    pos = GeoPos(0, 0)
    chart = Chart(Datetime(date_str, time_str, '+00:00'), pos)
    return chart.get(planet).lon

def get_nasa_longitude(planet, dt):
    """
    Get the NASA longitude for a given planet using the NASA Horizons API.
    Args:
        planet (str): The name of the planet.
        dt (datetime): The datetime for calculation.
    Returns:
        float: The longitude of the planet or None if an error occurs.
    """
    planet_map = {
        'Sun': '10',
        'Moon': '301',
        'Mercury': '199',
        'Venus': '299',
        'Mars': '499',
        'Jupiter': '599',
        'Saturn': '699',
    }
    body = planet_map.get(planet)
    if not body:
        return None
    date_str = dt.strftime('%Y-%m-%d')
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='{body}'&EPHEM_TYPE=OBSERVER&CENTER='500@399'&START_TIME='{date_str} 00:00'&STOP_TIME='{date_str} 00:01'&STEP_SIZE='1 m'&QUANTITIES='1'"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    # Parse longitude from response
    for line in resp.text.splitlines():
        if '$$SOE' in line:
            idx = resp.text.splitlines().index(line)
            data_line = resp.text.splitlines()[idx+1]
            parts = data_line.split()
            if len(parts) > 4:
                return float(parts[4])
    return None

def compare_longitudes(planet, dt):
    """
    Compare the longitudes of a planet from Flatlib and NASA.
    Args:
        planet (str): The name of the planet.
        dt (datetime): The datetime for calculation.
    Returns:
        str: A string summarizing the comparison.
    """
    flatlib_lon = get_flatlib_longitude(planet, dt)
    nasa_lon = get_nasa_longitude(planet, dt)
    if flatlib_lon is None or nasa_lon is None:
        return f"Could not get longitude for {planet}"
    diff = abs(flatlib_lon - nasa_lon)
    return f"{planet} on {dt.strftime('%Y-%m-%d')}:\nFlatlib: {flatlib_lon:.4f}°\nNASA: {nasa_lon:.4f}°\nDifference: {diff:.4f}°"

if __name__ == "__main__":
    dt = datetime.utcnow()
    for planet in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        print(compare_longitudes(planet, dt))
# Compare flatlib planetary longitude with NASA Horizons API
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib import const
import requests
from datetime import datetime

def get_flatlib_longitude(planet, dt):
    date_str = dt.strftime('%Y/%m/%d')
    time_str = dt.strftime('%H:%M')
    pos = GeoPos(0, 0)
    chart = Chart(Datetime(date_str, time_str, '+00:00'), pos)
    return chart.get(planet).lon

def get_nasa_longitude(planet, dt):
    # NASA Horizons API for ecliptic longitude (degrees)
    planet_map = {
        'Sun': '10',
        'Moon': '301',
        'Mercury': '199',
        'Venus': '299',
        'Mars': '499',
        'Jupiter': '599',
        'Saturn': '699',
    }
    body = planet_map.get(planet)
    if not body:
        return None
    date_str = dt.strftime('%Y-%m-%d')
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='{body}'&EPHEM_TYPE=OBSERVER&CENTER='500@399'&START_TIME='{date_str} 00:00'&STOP_TIME='{date_str} 00:01'&STEP_SIZE='1 m'&QUANTITIES='1'"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    # Parse longitude from response
    for line in resp.text.splitlines():
        if '$$SOE' in line:
            idx = resp.text.splitlines().index(line)
            data_line = resp.text.splitlines()[idx+1]
            parts = data_line.split()
            if len(parts) > 4:
                return float(parts[4])
    return None

def compare_longitudes(planet, dt):
    flatlib_lon = get_flatlib_longitude(planet, dt)
    nasa_lon = get_nasa_longitude(planet, dt)
    if flatlib_lon is None or nasa_lon is None:
        return f"Could not get longitude for {planet}"
    diff = abs(flatlib_lon - nasa_lon)
    return f"{planet} on {dt.strftime('%Y-%m-%d')}:\nFlatlib: {flatlib_lon:.4f}°\nNASA: {nasa_lon:.4f}°\nDifference: {diff:.4f}°"

if __name__ == "__main__":
    dt = datetime.utcnow()
    for planet in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        print(compare_longitudes(planet, dt))
