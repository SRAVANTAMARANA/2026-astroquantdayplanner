from data.price_loader import load_price_data
from timeframe.htf_bias import determine_htf_bias
from liquidity.liquidity import detect_liquidity_sweep
from imbalance.fvg import detect_fvg
from timeframe.premium_discount import premium_discount_zone
from timeframe.killzone import is_killzone
from smt.smt import detect_smt
from filters.astro_gann import astro_filter, gann_filter
from brain.ict_brain import ICTBrain
from notify.telegram import send_telegram
from memory.trade_memory import save_trade

def run_ict_ai_mentor():
    df = load_price_data()

    htf_bias = determine_htf_bias(df)
    liquidity = detect_liquidity_sweep(df)
    fvg = detect_fvg(df)
    zone = premium_discount_zone(df)
    session = is_killzone()

    if not session:
        return

    direction = "SELL" if htf_bias == "BEARISH" else "BUY"

    brain = ICTBrain()
    brain.reset()

    brain.check_htf_bias(htf_bias)
    brain.check_liquidity(liquidity)
    brain.check_fvg(fvg)
    brain.check_premium_discount(zone, direction)
    brain.check_killzone(True)

    if not astro_filter() or not gann_filter():
        return

    approved, score, reasons = brain.final_decision()

    if not approved:
        return

    signal = {
        "symbol": "XAUUSD",
        "direction": direction,
        "entry": "AUTO",
        "sl": "AUTO",
        "tp": "AUTO",
        "session": session,
        "probability": score * 15,
        "reason": reasons
    }

    send_telegram(signal)
    save_trade(signal)
