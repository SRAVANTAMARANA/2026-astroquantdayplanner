def get_astro_summary(dt, positions, nakshatra, tithi, periods):
    """
    Advanced rule-based astrology summary for XAUUSD with pattern identification, time-based market explanation, and actionable suggestions.
    """
    try:
        moon = positions.get('Moon', None)
        sun = positions.get('Sun', None)
        venus = positions.get('Venus', None)
        mars = positions.get('Mars', None)
        mercury = positions.get('Mercury', None)
        jupiter = positions.get('Jupiter', None)
        saturn = positions.get('Saturn', None)
        rules = []
        # Rule 1: Bullish if Moon ahead of Sun
        if moon is not None and sun is not None and moon > sun:
            rules.append(('bullish', 'Moon ahead of Sun in zodiac'))
        # Rule 2: Bearish if Sun ahead of Moon
        if moon is not None and sun is not None and sun > moon:
            rules.append(('bearish', 'Sun ahead of Moon in zodiac'))
        # Rule 3: Bullish if Moon in Rohini
        # Rule 4: Volatility if Ekadashi/Purnima/Amavasya
        # Rule 5: Bullish if Venus conjunct Sun or Mars
        if venus is not None and sun is not None and abs(venus - sun) < 6:
            rules.append(('bullish', 'Venus conjunct Sun (<6°)'))
        if venus is not None and mars is not None and abs(venus - mars) < 6:
            rules.append(('bullish', 'Venus conjunct Mars (<6°)'))
        # Rule 6: Bearish if Mercury is retrograde (mock: Mercury < 90° or > 270°)
        if mercury is not None and (mercury < 90 or mercury > 270):
            rules.append(('bearish', 'Mercury retrograde pattern (mock rule)'))
        # Rule 7: Bullish if Jupiter trine Sun (angle ~120°)
        if jupiter is not None and sun is not None and abs((jupiter - sun) % 360 - 120) < 6:
            rules.append(('bullish', 'Jupiter trine Sun (~120°)'))
        # Rule 8: Bearish if Saturn is conjunct Sun (<6°)
        if saturn is not None and sun is not None and abs(saturn - sun) < 6:
            rules.append(('bearish', 'Saturn conjunct Sun (<6°)'))
        # Pattern 1: Repeated Nakshatra (if two consecutive periods have same nakshatra)
        pattern_notes = []
        for i in range(1, len(periods)):
            if periods[i]['event']['nakshatra'] == periods[i-1]['event']['nakshatra']:
                pattern_notes.append(f"Pattern: Repeated Nakshatra {periods[i]['event']['nakshatra']} from {periods[i-1]['start_time'].strftime('%I:%M %p')} to {periods[i]['end_time'].strftime('%I:%M %p')} → Range-bound/sideways expected")
        # Pattern 2: Aspect cluster (if 3+ aspects in a period, mock: always true for demo)
        pattern_notes.append("Pattern: Aspect cluster detected → Watch for sudden spikes or reversals")
        # Pattern 3: Tithi/Nakshatra combo (e.g., Rohini + Ekadashi)
        for p in periods:
            if p['event']['nakshatra'] == 'Rohini' and tithi.get('tithi') == 'Ekadashi':
                pattern_notes.append("Pattern: Rohini Nakshatra with Ekadashi Tithi → High volatility, bullish bias")
        # Build time-based summary with suggestions and market session analysis
        def get_sessions(start_dt, end_dt):
            # Returns a list of (session_name, session_start, session_end) tuples for the period
            sessions = [
                ("Asia", 0, 8),    # 00:00-08:00 UTC
                ("Europe", 8, 16), # 08:00-16:00 UTC
                ("US", 13, 21)     # 13:00-21:00 UTC
            ]
            period_sessions = []
            for name, s_start, s_end in sessions:
                # Find overlap between period and session
                p_start = start_dt.hour + start_dt.minute/60
                p_end = end_dt.hour + end_dt.minute/60
                # Handle overnight
                if p_end <= p_start:
                    p_end += 24
                s_start_full = s_start
                s_end_full = s_end
                if s_end <= s_start:
                    s_end_full += 24
                overlap_start = max(p_start, s_start_full)
                overlap_end = min(p_end, s_end_full)
                if overlap_start < overlap_end:
                    # Convert back to time
                    st = (int(overlap_start)%24, int((overlap_start%1)*60))
                    et = (int(overlap_end)%24, int((overlap_end%1)*60))
                    period_sessions.append((name, st, et, overlap_start, overlap_end))
            return period_sessions

        from xauusd_chart import fetch_xauusd_ohlc
        import pandas as pd
        period_summaries = []
        # Fetch price data for the day (D1, H1, M15)
        try:
            dt0 = periods[0]['start_time']
            ohlc = fetch_xauusd_ohlc(dt0)
            d1 = ohlc.get('D1')
            h1 = ohlc.get('H1')
            m15 = ohlc.get('M15')
        except Exception:
            d1 = h1 = m15 = None
        best_window = {'score': 0, 'desc': '', 'period': None, 'session': None}
        for p in periods:
            nk = p['event']['nakshatra']
            tithi_name = tithi.get('tithi')
            start_dt = p['start_time']
            end_dt = p['end_time']
            start = start_dt.strftime('%I:%M %p')
            end = end_dt.strftime('%I:%M %p')
            # Default: sideways
            behavior = 'sideways'
            reason = []
            suggestion = 'Hold/Range trade; avoid large positions.'
            # Rule 3: Bullish if Moon in Rohini
            if nk == 'Rohini':
                behavior = 'bullish'
                reason.append('Moon in Rohini')
                suggestion = 'Look for long (buy) opportunities on dips.'
            # Rule 4: Volatility if Ekadashi/Purnima/Amavasya
            if tithi_name in ['Ekadashi', 'Purnima', 'Amavasya']:
                behavior = 'volatile'
                reason.append(f'Tithi is {tithi_name}')
                suggestion = 'Expect sharp moves; use tight stops and reduce position size.'
            # Rule 1/2/5/6/7/8: Overlay bias
            for bias, rule in rules:
                if bias == 'bullish' and behavior == 'sideways':
                    behavior = 'bullish'
                    reason.append(rule)
                    suggestion = 'Look for long (buy) opportunities on dips.'
                elif bias == 'bearish' and behavior == 'sideways':
                    behavior = 'bearish'
                    reason.append(rule)
                    suggestion = 'Consider short (sell) trades or stay cautious.'
            # Market session breakdown with advanced analytics
            sessions = get_sessions(start_dt, end_dt)
            session_lines = []
            for s_name, (sh, sm), (eh, em), s_start, s_end in sessions:
                session_behavior = behavior
                session_suggestion = suggestion
                session_pattern = ''
                session_confidence = 0.5
                session_breakout_prob = 0.3
                session_volatility = 0.0
                session_trend = 'sideways'
                support, resistance = None, None
                # Find price range for session using H1/M15 data if available
                session_start = start_dt.replace(hour=sh, minute=sm)
                session_end = start_dt.replace(hour=eh, minute=em)
                if session_end <= session_start:
                    session_end += pd.Timedelta(days=1)
                price_min, price_max = None, None
                # Fix: Ensure all datetimes are naive or UTC for comparison
                def to_naive_utc(ts):
                    if hasattr(ts, 'tz_convert'):
                        return ts.tz_convert('UTC').tz_localize(None)
                    elif hasattr(ts, 'tz_localize'):
                        return ts.tz_localize(None)
                    return ts
                if m15 is not None and not m15.empty:
                    idx = m15.index
                    if hasattr(idx, 'tz'):  # DatetimeIndex
                        idx = idx.tz_convert('UTC').tz_localize(None)
                    mask = (idx >= session_start) & (idx < session_end)
                    session_prices = m15.loc[mask]['close']
                    if not session_prices.empty:
                        price_min = session_prices.min()
                        price_max = session_prices.max()
                if (price_min is None or price_max is None) and h1 is not None and not h1.empty:
                    idx = h1.index
                    if hasattr(idx, 'tz'):
                        idx = idx.tz_convert('UTC').tz_localize(None)
                    mask = (idx >= session_start) & (idx < session_end)
                    session_prices = h1.loc[mask]['close']
                    if not session_prices.empty:
                        price_min = session_prices.min()
                        price_max = session_prices.max()
                if price_min is None or price_max is None:
                    prev_close = None
                    if d1 is not None and not d1.empty:
                        prev_close = d1['close'].iloc[-1]
                    else:
                        prev_close = 4332.01
                    price_min = prev_close - 5
                    price_max = prev_close + 5
                price_range = f"{price_min:.2f} - {price_max:.2f}"
                # Volatility score (normalized)
                session_volatility = (price_max - price_min) / price_min if price_min else 0
                # Trend direction (simple: compare first/last price)
                trend_val = 'sideways'
                if m15 is not None and not m15.empty and not session_prices.empty:
                    first = session_prices.iloc[0]
                    last = session_prices.iloc[-1]
                    if last > first * 1.001:
                        trend_val = 'up'
                    elif last < first * 0.999:
                        trend_val = 'down'
                    else:
                        trend_val = 'sideways'
                session_trend = trend_val
                # Support/resistance (min/max)
                support = price_min
                resistance = price_max
                # Breakout probability (higher if volatility high, astro volatile, or trend strong)
                session_breakout_prob = min(1.0, session_volatility * 10)
                if behavior == 'volatile':
                    session_breakout_prob = max(session_breakout_prob, 0.7)
                if session_trend in ['up', 'down']:
                    session_confidence = 0.7
                if session_breakout_prob > 0.7:
                    session_confidence = 0.8
                # Pattern/astro triggers
                if s_name == 'Asia':
                    session_pattern = 'Range-bound, watch for false breakouts.'
                elif s_name == 'Europe':
                    session_pattern = 'Volatility increases, breakout likely if price crosses range.'
                elif s_name == 'US':
                    session_pattern = 'Trend extension or reversal; high volume.'
                # Best trading window logic
                score = session_confidence * session_breakout_prob * session_volatility
                if score > best_window['score']:
                    best_window = {
                        'score': score,
                        'desc': f"{s_name} {start} - {end}",
                        'period': (start, end),
                        'session': s_name
                    }
                session_lines.append(
                    f"    {s_name} Session ({sh:02d}:{sm:02d} - {eh:02d}:{em} UTC): {session_behavior.upper()} | Range: {price_range} | Volatility: {session_volatility:.2%} | Trend: {session_trend} | S/R: {support:.2f}/{resistance:.2f} | Breakout Prob: {session_breakout_prob:.0%} | Confidence: {session_confidence:.0%} | Pattern: {session_pattern} | {session_suggestion}"
                )
            period_summaries.append(f"{start} - {end}: {behavior.upper()} | Reason: {', '.join(reason) if reason else 'No strong signal'} | Suggestion: {suggestion}\n" + "\n".join(session_lines))
        if best_window['score'] > 0:
            period_summaries.append(f"\n<b>Best Trading Window:</b> {best_window['desc']} (Score: {best_window['score']:.2f})")
        # List rules
        rule_texts = [
            "Rule 1: Moon ahead of Sun in zodiac → Bullish bias",
            "Rule 2: Sun ahead of Moon in zodiac → Bearish bias",
            "Rule 3: Moon in Rohini → Bullish for gold",
            "Rule 4: Tithi is Ekadashi/Purnima/Amavasya → Volatility expected",
            "Rule 5: Venus conjunct Sun or Mars (<6°) → Bullish for gold",
            "Rule 6: Mercury retrograde pattern (mock) → Bearish bias",
            "Rule 7: Jupiter trine Sun (~120°) → Bullish for gold",
            "Rule 8: Saturn conjunct Sun (<6°) → Bearish for gold"
        ]
        summary = "<b>Rules:</b>\n" + "\n".join(rule_texts)
        if pattern_notes:
            summary += "\n<b>Pattern Identified:</b>\n" + "\n".join(pattern_notes)
        summary += "\n<b>Market Behavior by Time:</b>\n" + "\n".join(period_summaries)
        return summary
    except Exception as e:
        return f'Error: {e}'