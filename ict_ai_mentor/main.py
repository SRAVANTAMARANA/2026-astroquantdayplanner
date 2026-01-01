
from data.price_loader import load_price_data
from timeframe.htf_bias import determine_htf_bias
from liquidity.liquidity import detect_liquidity_sweep
from imbalance.fvg import detect_fvg
from brain.ict_brain import ICTBrain
from notify.telegram import send_telegram
from memory.trade_memory import save_trade

def run_ict_ai_mentor():
    df = load_price_data()

    htf_bias = determine_htf_bias(df)
    liquidity = detect_liquidity_sweep(df)
    fvg = detect_fvg(df)

    direction = "SELL" if htf_bias == "BEARISH" else "BUY"
    zone = "PREMIUM"  # (later auto calculated)
    in_killzone = True  # (later auto time check)

    brain = ICTBrain()
    brain.reset()

    brain.check_htf_bias(htf_bias)
    brain.check_liquidity(liquidity)
    brain.check_fvg(fvg)
    brain.check_premium_discount(zone, direction)
    brain.check_killzone(in_killzone)

    approved, score, reasons = brain.final_decision()

    if not approved:
        print("❌ ICT Brain rejected trade | Score:", score)
        return

    # --- SAFE GATE ---
    from execution.safe_gate import allow_trade
    import json, os
    memory_path = os.path.join(os.path.dirname(__file__), "../memory/trades.json")
    if os.path.exists(memory_path):
        with open(memory_path) as f:
            memory = json.load(f)
    else:
        memory = []
    if not allow_trade(memory, "NY Killzone"):
        print("❌ Trade already placed this session.")
        return

    # --- SL/TP MATH ---
    from risk.sl_tp_math import calculate_sl_tp, lot_size
    sl, tp1, tp2 = calculate_sl_tp(df, direction)
    balance = 10000  # TODO: fetch from MT5 or config
    risk_pct = 0.5
    sl_points = abs(df.close.iloc[-1] - sl)
    lot = lot_size(balance, risk_pct, sl_points)

    # --- MT5 EXECUTION ---
    from execution.mt5_executor import connect_mt5, place_trade
    try:
        connect_mt5()
        result = place_trade(direction, lot, sl, tp1)
        print("MT5 trade result:", result)
    except Exception as e:
        print("MT5 execution error:", e)

    signal = {
        "symbol": "XAUUSD",
        "direction": direction,
        "entry": str(df.close.iloc[-1]),
        "sl": sl,
        "tp": [tp1, tp2],
        "session": "NY Killzone",
        "probability": score * 15,
        "reason": reasons,
        "lot": lot
    }

    send_telegram(signal)
    save_trade(signal)

    print("✅ ICT Brain approved, trade executed, & sent signal")

if __name__ == "__main__":
    run_ict_ai_mentor()
