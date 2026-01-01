def gann_decision(time_ok, planet_ok, price_ok, state):
    if time_ok and planet_ok and price_ok and state != "TRANSITION":
        return True
    return False
