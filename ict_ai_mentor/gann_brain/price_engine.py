def price_at_geometry(price, level, tolerance=0.2):
    """
    price: current XAUUSD price
    level: natural geometry level
    """
    if abs(price - level) <= tolerance:
        return True
    return False
