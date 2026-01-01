def planet_trigger(active_planets):
    """
    active_planets example:
        {"Mars": 90, "Sun": 180}
    """
    KEY_DEGREES = [0, 90, 180, 270, 360]
    for planet, degree in active_planets.items():
        if degree in KEY_DEGREES:
            return True, planet, degree
    return False, None, None
