from gann_tools_demo import square_of_nine_level

# Simulate a current XAUUSD price for development
current_price = 2050.0  # Example: replace with real price when available
base_price = 1800.0     # Example major low

# Calculate Gann Square of Nine levels
levels = [square_of_nine_level(base_price, deg) for deg in [90, 180, 360, 450, 720]]

# Find the closest Gann level to the current price
closest = min(levels, key=lambda x: abs(x - current_price))
diff = abs(current_price - closest)

print(f"Current XAUUSD price: {current_price}")
print(f"Gann Square of Nine levels from {base_price}: {levels}")
print(f"Closest Gann level: {closest} (diff: {diff:.2f})")

# Example: If price is within $5 of a Gann level, trigger a signal
if diff < 5:
    print(f"Signal: Price is near a key Gann level ({closest})! Watch for reversal or acceleration.")
else:
    print("No Gann signal: Price is not near a key level.")
