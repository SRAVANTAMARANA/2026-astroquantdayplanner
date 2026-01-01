import swisseph as swe
from datetime import datetime, timedelta, timezone

# Nakshatra names
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
NAKSHATRA_SPAN = 13 + 1/3

# Tithi names
TITHIS = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
]

TITHI_SPAN = 12  # Each tithi is 12 degrees of elongation

def get_moon_longitude(dt):
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)
    moon_data = swe.calc_ut(jd, swe.MOON)
    return moon_data[0][0]

def get_sun_longitude(dt):
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)
    sun_data = swe.calc_ut(jd, swe.SUN)
    return sun_data[0][0]

def get_nakshatra_info(dt):
    lon = get_moon_longitude(dt)
    nak_num = int(lon // NAKSHATRA_SPAN)
    pada = int((lon % NAKSHATRA_SPAN) // (NAKSHATRA_SPAN / 4)) + 1
    return {
        "moon_longitude": lon,
        "nakshatra": NAKSHATRAS[nak_num],
        "pada": pada
    }

def get_tithi_info(dt):
    sun_lon = get_sun_longitude(dt)
    moon_lon = get_moon_longitude(dt)
    diff = (moon_lon - sun_lon) % 360
    tithi_num = int(diff // TITHI_SPAN)
    tithi_name = TITHIS[tithi_num] if tithi_num < 14 else TITHIS[14]
    return {
        "tithi": tithi_name,
        "tithi_number": tithi_num + 1,
        "elongation": diff
    }

def find_event_transitions(event_func, start_dt, hours=24, step_minutes=10):
    results = []
    prev_info = event_func(start_dt)
    prev_dt = start_dt
    end_dt = start_dt + timedelta(hours=hours)
    dt = start_dt + timedelta(minutes=step_minutes)

    # Determine which field to compare (nakshatra or tithi)
    if 'nakshatra' in prev_info:
        key = 'nakshatra'
    elif 'tithi' in prev_info:
        key = 'tithi'
    else:
        key = None

    while dt <= end_dt:
        info = event_func(dt)
        if key:
            changed = info[key] != prev_info[key]
        else:
            changed = info != prev_info
        if changed:
            results.append({
                "event": prev_info,
                "start_time": prev_dt,
                "end_time": dt
            })
            prev_info = info
            prev_dt = dt
        dt += timedelta(minutes=step_minutes)
    results.append({
        "event": prev_info,
        "start_time": prev_dt,
        "end_time": end_dt
    })
    return results

if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    nakshatra_events = find_event_transitions(get_nakshatra_info, now, hours=24, step_minutes=10)
    tithi_events = find_event_transitions(get_tithi_info, now, hours=24, step_minutes=10)
    print("Nakshatra Events:")
    for e in nakshatra_events:
        print(e)
    print("\nTithi Events:")
    for e in tithi_events:
        print(e)
