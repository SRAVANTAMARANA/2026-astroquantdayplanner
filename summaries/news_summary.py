def get_news_summary(dt):
    # Forex Factory economic calendar for market-moving events
    import requests
    from xml.etree import ElementTree as ET
    from datetime import datetime, timedelta
    from daily_astro_telegram import get_planet_positions, PLANETS
    ff_url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
    news_items = []
    try:
        resp = requests.get(ff_url, timeout=10)
        root = ET.fromstring(resp.content)
        for item in root.findall('.//event'):
            title = item.findtext('title', '')
            impact = item.findtext('impact', '')
            country = item.findtext('country', '')
            time_str = item.findtext('date', '') + ' ' + item.findtext('time', '')
            # Parse event time (UTC)
            try:
                event_dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            except Exception:
                event_dt = None
            # Only show high/medium impact and gold/USD/major events
            if impact in ['High', 'Medium'] and (
                'USD' in country or 'Gold' in title or 'FOMC' in title or 'CPI' in title or 'NFP' in title or 'Fed' in title or 'PCE' in title or 'Unemployment' in title or 'GDP' in title):
                # Estimate realization time: event time + 15-30 min
                realization_dt = event_dt + timedelta(minutes=30) if event_dt else None
                # Get detailed aspects at event and realization time
                def detailed_aspects(dt):
                    pos = get_planet_positions(dt)
                    aspect_angles = {
                        'Conjunction': 0,
                        'Opposition': 180,
                        'Trine': 120,
                        'Square': 90,
                        'Sextile': 60
                    }
                    orb = 6
                    details = []
                    for p1, k1 in PLANETS:
                        for p2, k2 in PLANETS:
                            if p1 >= p2:
                                continue
                            lon1, lon2 = pos[p1], pos[p2]
                            diff = abs(lon1 - lon2)
                            diff = min(diff, 360 - diff)
                            for aspect, angle in aspect_angles.items():
                                if abs(diff - angle) <= orb:
                                    # Simple effect mapping
                                    if p1 == 'Moon' or p2 == 'Moon':
                                        effect = 'Short-term volatility'
                                    elif p1 == 'Sun' or p2 == 'Sun':
                                        effect = 'Trend bias'
                                    elif p1 == 'Venus' or p2 == 'Venus':
                                        effect = 'Gold demand/sentiment'
                                    elif p1 == 'Mars' or p2 == 'Mars':
                                        effect = 'Breakout/impulse risk'
                                    else:
                                        effect = 'General astro influence'
                                    details.append(f"{p1}-{p2} {aspect} ({diff:.1f}°): {effect}")
                    return ", ".join(details) if details else 'None'
                aspects_event = detailed_aspects(event_dt) if event_dt else 'N/A'
                aspects_real = detailed_aspects(realization_dt) if realization_dt else 'N/A'
                # Format times
                event_time_str = event_dt.strftime('%Y-%m-%d %H:%M UTC') if event_dt else 'N/A'
                real_time_str = realization_dt.strftime('%Y-%m-%d %H:%M UTC') if realization_dt else 'N/A'
                news_items.append(
                    f"<b>{impact} Impact</b> | {country} | {title}\n"
                    f"Release: {event_time_str} | Realization: {real_time_str}\n"
                    f"Aspects at release: {aspects_event}\nAspects at realization: {aspects_real}\n"
                )
    except Exception as e:
        news_items.append(f"Error fetching Forex Factory news: {e}")
    if not news_items:
        news_items.append("No major market-moving news events found.")
    return '\n'.join(news_items)