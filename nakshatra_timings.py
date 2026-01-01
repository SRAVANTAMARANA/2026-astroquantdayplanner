"""
nakshatra_timings.py
--------------------
Calculate Nakshatra transitions using Swiss Ephemeris.
Provides functions to get moon longitude, nakshatra info, and find transitions.
"""
import swisseph as swe
from datetime import datetime, timedelta

# Nakshatra names in order
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
NAKSHATRA_SPAN = 13 + 1/3  # 13°20' = 13.333... degrees


def get_moon_longitude(dt):
    """
    Get the longitude of the Moon for a given datetime using Swiss Ephemeris.
    Args:
        dt (datetime): Datetime object (UTC recommended)
    Returns:
        float: Moon longitude in degrees
    """
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)
    moon_data = swe.calc_ut(jd, swe.MOON)
    return moon_data[0][0]  # longitude


    """
    Get nakshatra and pada for a given datetime.
    Args:
        dt (datetime): Datetime object
    Returns:
        dict: {'moon_longitude', 'nakshatra', 'pada'}
    """
def get_nakshatra_info(dt):
    lon = get_moon_longitude(dt)
    nak_num = int(lon // NAKSHATRA_SPAN)
    pada = int((lon % NAKSHATRA_SPAN) // (NAKSHATRA_SPAN / 4)) + 1
    return {
        "moon_longitude": lon,
        "nakshatra": NAKSHATRAS[nak_num],
        "pada": pada
    }


def find_nakshatra_transitions(start_dt, hours=24, step_minutes=10):
    """
    Find nakshatra transitions in the next `hours` hours from start_dt.
    Returns a list of dicts: [{nakshatra, start_time, end_time, start_long, end_long}]
    """
    results = []
    prev_info = get_nakshatra_info(start_dt)
    prev_dt = start_dt
    end_dt = start_dt + timedelta(hours=hours)
    dt = start_dt + timedelta(minutes=step_minutes)
    while dt <= end_dt:
        info = get_nakshatra_info(dt)
        if info["nakshatra"] != prev_info["nakshatra"]:
            # Nakshatra changed, record the transition
            results.append({
                "nakshatra": prev_info["nakshatra"],
                "start_time": prev_dt,
                "end_time": dt,
                "start_long": get_moon_longitude(prev_dt),
                "end_long": get_moon_longitude(dt)
            })
            prev_info = info
            prev_dt = dt
        dt += timedelta(minutes=step_minutes)
    # Add the last nakshatra till end_dt
    results.append({
        "nakshatra": prev_info["nakshatra"],
        "start_time": prev_dt,
        "end_time": end_dt,
        "start_long": get_moon_longitude(prev_dt),
        "end_long": get_moon_longitude(end_dt)
    })
def print_nakshatra_transitions(transitions):
    """Print nakshatra transitions in a readable format."""
    for t in transitions:
        print(f"Nakshatra: {t['nakshatra']}, Start: {t['start_time']}, End: {t['end_time']}, Start Long: {t['start_long']:.2f}, End Long: {t['end_long']:.2f}")
    return results


if __name__ == "__main__":
    print_nakshatra_transitions(transitions)
    for t in transitions:
        print(f"Nakshatra: {t['nakshatra']}, Start: {t['start_time']}, End: {t['end_time']}")
