# Global and Gann Financial Astrology Rules for XAUUSD
# Sources: Vedic, Western, Gann astrology literature
# For use in astro analyser and Telegram summary

ASTRO_RULES = {
    'nakshatra': {
        'Rohini': {'effect': 'Bullish', 'notes': 'Growth, abundance. Vedic/Western consensus.'},
        'Magha': {'effect': 'Volatile', 'notes': 'Sudden moves, leadership.'},
        'Mula': {'effect': 'Reversal/Volatile', 'notes': 'Trend change, caution.'},
        'Pushya': {'effect': 'Safe-haven demand', 'notes': 'Auspicious, stability.'},
        'Chitra': {'effect': 'Volatile', 'notes': 'Increased trading activity.'},
        'Swati': {'effect': 'Volatile', 'notes': 'Price swings.'},
        'Vishakha': {'effect': 'Volatile', 'notes': 'Price swings.'},
        # Add all 27 nakshatras as needed
    },
    'moon_zodiac': {
        'Taurus': {'effect': 'Bullish', 'notes': 'Exaltation, strong sentiment.'},
        'Scorpio': {'effect': 'Bearish/Uncertain', 'notes': 'Debilitation, caution.'},
        'Cancer': {'effect': 'Safe-haven', 'notes': 'Optimism, stability.'},
        'Pisces': {'effect': 'Safe-haven', 'notes': 'Optimism, stability.'},
    },
    'tithi': {
        'Panchami': {'effect': 'Volatile', 'notes': 'Energetic, triggers moves.'},
        'Ekadashi': {'effect': 'Volatile', 'notes': 'Energetic, triggers moves.'},
        'Amavasya': {'effect': 'Turning point', 'notes': 'New Moon, reversals.'},
        'Purnima': {'effect': 'Turning point', 'notes': 'Full Moon, reversals.'},
    },
    'planetary_aspects': {
        'Moon_Jupiter': {'effect': 'Bullish', 'notes': 'Optimism.'},
        'Moon_Saturn': {'effect': 'Bearish/Range', 'notes': 'Caution.'},
        'Moon_Rahu': {'effect': 'Volatile', 'notes': 'Unpredictable.'},
        'Moon_Ketu': {'effect': 'Volatile', 'notes': 'Unpredictable.'},
    },
    'gann': {
        'gann_dates': {'effect': 'Major moves', 'notes': 'Gann seasonal dates, anniversaries.'},
        'planetary_cycles': {'effect': 'Trend change', 'notes': 'Jupiter/Saturn cycles, Mercury retrograde.'},
        'price_time_harmonics': {'effect': 'Support/resistance', 'notes': 'Gann angles, squares.'},
        'square_of_nine': {
            'effect': 'Major price/time turning point',
            'notes': 'Square of Nine level hit; watch for reversal or acceleration.'
        },
        'gann_fan': {
            'effect': 'Support/resistance zone',
            'notes': 'Gann Fan angle reached; trend may change or pause.'
        },
        'gann_hexagon': {
            'effect': 'Harmonic resonance',
            'notes': 'Hexagon level; price may react strongly.'
        },
        'gann_cycles': {
            'effect': 'Time/price cycle completion',
            'notes': 'Cycle level; expect volatility or trend change.'
        },
        'gann_octave': {
            'effect': 'Octave resonance',
            'notes': 'Octave level; price may vibrate or reverse.'
        },
        'gann_quadrant': {
            'effect': 'Quadrant boundary',
            'notes': 'Quadrant level; price may pause or reverse.'
        },
    }
}

# Example function to generate summary from rules

def generate_astro_summary(nakshatra, moon_zodiac, tithi, aspects, gann_date=False):
    summary = []
    if nakshatra in ASTRO_RULES['nakshatra']:
        rule = ASTRO_RULES['nakshatra'][nakshatra]
        summary.append(f"Nakshatra {nakshatra}: {rule['effect']} ({rule['notes']})")
    if moon_zodiac in ASTRO_RULES['moon_zodiac']:
        rule = ASTRO_RULES['moon_zodiac'][moon_zodiac]
        summary.append(f"Moon in {moon_zodiac}: {rule['effect']} ({rule['notes']})")
    if tithi in ASTRO_RULES['tithi']:
        rule = ASTRO_RULES['tithi'][tithi]
        summary.append(f"Tithi {tithi}: {rule['effect']} ({rule['notes']})")
    for aspect in aspects:
        if aspect in ASTRO_RULES['planetary_aspects']:
            rule = ASTRO_RULES['planetary_aspects'][aspect]
            summary.append(f"Aspect {aspect}: {rule['effect']} ({rule['notes']})")
    if gann_date:
        rule = ASTRO_RULES['gann']['gann_dates']
        summary.append(f"Gann date: {rule['effect']} ({rule['notes']})")
    return '\n'.join(summary) if summary else 'No major astro signals.'
