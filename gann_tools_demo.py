import math
from datetime import datetime, timedelta

# --- Gann Square of Nine Calculation ---
def square_of_nine_level(base_price, steps):
    """
    Calculate a Gann Square of Nine price level.
    base_price: starting price (e.g., major high/low)
    steps: number of steps (e.g., 90, 180, 360)
    Returns the projected price level.
    """
    return round((math.sqrt(base_price) + steps / 360) ** 2, 2)

# --- Gann Time Cycle Calculation ---
def gann_time_cycles(start_date, cycles=[30, 45, 60, 90, 180, 360]):
    """
    Calculate Gann time cycle dates from a start date.
    start_date: datetime object
    cycles: list of cycle lengths in days
    Returns a dict of cycle name to date.
    """
    return {f"{cycle}_days": start_date + timedelta(days=cycle) for cycle in cycles}

# --- Example Usage ---
if __name__ == "__main__":
    # Example: Gold made a low at 1800 on 2025-03-15
    base_price = 1800
    start_date = datetime(2025, 3, 15)
    print("Gann Square of Nine levels from 1800:")
    for steps in [90, 180, 360]:
        print(f"{steps}°: {square_of_nine_level(base_price, steps)}")
    print("\nGann time cycles from 2025-03-15:")
    cycles = gann_time_cycles(start_date)
    for name, date in cycles.items():
        print(f"{name}: {date.strftime('%Y-%m-%d')}")
